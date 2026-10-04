---
title: x-ui、3x-ui和Xray怎么开BBR：面板菜单做了什么，tcpcongestion又是什么
date: 2026-10-04 11:00:00
tags:
  - BBR加速
  - 3x-ui
  - Xray
  - Linux网络优化
categories:
  - Linux优化
description: 3x-ui的x-ui命令菜单里有Enable BBR选项，源码里它写了一个sysctl配置文件；Xray配置里还有tcpcongestion字段。依据3x-ui的x-ui.sh和Xray官方文档，讲清楚两种开BBR的方式和验证方法。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "x-ui、3x-ui和Xray怎么开BBR：面板菜单做了什么，tcpcongestion又是什么",
      "description": "3x-ui的x-ui命令菜单里有Enable BBR选项，源码里它写了一个sysctl配置文件；Xray配置里还有tcpcongestion字段。依据3x-ui的x-ui.sh和Xray官方文档，讲清楚两种开BBR的方式和验证方法。",
      "datePublished": "2026-10-04T11:00:00+08:00",
      "dateModified": "2026-10-04T11:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/xui-xray-enable-bbr/",
      "author": {
        "@type": "Organization",
        "name": "vpsjq.com"
      },
      "publisher": {
        "@type": "Organization",
        "name": "vpsjq.com"
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "3x-ui里怎么开启BBR？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "SSH登录后运行x-ui命令打开管理菜单，选择Enable BBR（我读到的源码里是第26项，不同版本编号可能变），再选1启用。脚本会写入/etc/sysctl.d/99-bbr-x-ui.conf，内容是net.core.default_qdisc = fq和net.ipv4.tcp_congestion_control = bbr，并用sysctl -p应用。"
          }
        },
        {
          "@type": "Question",
          "name": "面板的Enable BBR会不会检查内核版本？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "我读到的x-ui.sh里的enable_bbr函数没有检查内核版本，只是写配置再看sysctl输出是不是bbr。如果内核不支持，会提示Failed to enable BBR，需要自己排查内核。"
          }
        },
        {
          "@type": "Question",
          "name": "Xray配置里的tcpcongestion有什么用？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "它是streamSettings.sockopt里的字段，用来指定Xray这个进程的TCP连接使用的拥塞控制算法，仅Linux有效，不设置时使用系统默认。它不能让内核凭空支持BBR，内核本身得有对应算法才行。"
          }
        }
      ]
    }
  ]
}
</script>

很多人装完x-ui或3x-ui，想顺手开BBR，会发现面板网页里并没有这个选项。其实有两条路：一条是面板自带的 `x-ui` 命令菜单，一条是 Xray 配置里的 `tcpcongestion` 字段。这篇依据 3x-ui 的 `x-ui.sh` 源码和 Xray 官方文档，把两者各自做了什么讲清楚。

先说明：下面内容是读源码和文档得到的，我没有在服务器上实际跑过这两种方式，所以输出样例只写命令和判断方法，不贴"实测结果"。

<!-- more -->

## 先搞清楚：BBR是内核的事，不是Xray的事

BBR是Linux内核的TCP拥塞控制算法，由系统的 `net.ipv4.tcp_congestion_control` 控制，对这台机器上所有TCP连接生效。x-ui、3x-ui、Xray 都只是跑在系统上的程序，所以"在x-ui里开BBR"本质上是让面板脚本帮你改系统的 sysctl 配置，不是 Xray 自己有了BBR。

这也意味着：内核本身得支持BBR（主线内核从 4.9 开始自带，见 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)），否则无论用哪种方式都开不起来。

## 方式一：3x-ui 的 x-ui 命令菜单

SSH 登录服务器，直接运行：

```bash
x-ui
```

在我读到的 3x-ui（MHSanaei）`x-ui.sh` 里，主菜单有一项 `Enable BBR`（源码里是第 26 项），进去之后是一个小菜单：

```
1. Enable BBR
2. Disable BBR
0. Back to Main Menu
```

选 1 之后，`enable_bbr` 函数大致做了这些事（来自源码）：

1. 先看当前是不是已经启用：`tcp_congestion_control` 是 `bbr`，并且 `default_qdisc` 是 `fq` 或 `cake`，就直接提示 `BBR is already enabled!`。
2. 如果系统有 `/etc/sysctl.d/` 目录，就写一个 `/etc/sysctl.d/99-bbr-x-ui.conf`，第一行是用 `#` 注释保存的原来参数（方便以后禁用时还原），后面两行是：

   ```
   net.core.default_qdisc = fq
   net.ipv4.tcp_congestion_control = bbr
   ```

3. 同时把 `/etc/sysctl.conf` 里以 `net.core.default_qdisc` 和 `net.ipv4.tcp_congestion_control` 开头的行注释掉，避免跟新文件冲突。
4. 只用 `sysctl -p /etc/sysctl.d/99-bbr-x-ui.conf` 应用这一个文件，而不是 `sysctl --system`（源码注释里说明这样做是为了避免把系统其他 sysctl 文件重新应用一遍而冒出无关报错）。
5. 最后检查 `tcp_congestion_control` 是不是 `bbr`，是就提示成功，否则提示 `Failed to enable BBR. Please check your system configuration.`。

没有 `/etc/sysctl.d/` 目录的系统，会走另一个分支：直接把这两项写进 `/etc/sysctl.conf` 再 `sysctl -p`。

有两点要注意：

- **不检查内核版本**：我读到的 `enable_bbr` 里没有判断内核版本或模块是否存在，直接写配置，失败了只靠最后一步的提示。内核不支持BBR时，需要自己排查，参考 [已安装BBR加速内核但加速模块未加载的解决方法](https://vpsjq.com/2026/08/30/bbr-module-not-loaded/)。
- **菜单编号会变**：26 是我读到的当前版本里的编号，不同版本、不同分支（原版 x-ui、3x-ui、甬哥版等）菜单不一样，以你实际看到的菜单文字为准。至于其他分支的菜单，我没有逐个核对。

选 2 可以关闭：如果存在 `99-bbr-x-ui.conf`，会读出第一行保存的旧参数，用 `sysctl -w` 还原，然后删掉这个文件；找不到这个文件时，会改 `/etc/sysctl.conf`，把 `fq` 换成 `pfifo_fast`、把 `bbr` 换成 `cubic`。

## 方式二：Xray 配置里的 tcpcongestion

Xray 的 `streamSettings.sockopt` 里有一个字段 `tcpcongestion`。官方文档对它的描述是：

- 指定 TCP 拥塞控制算法，**仅 Linux 有效**；
- 不设置时使用操作系统默认值；
- 常见取值有 `bbr`（文档里标为推荐）、`cubic` 等；
- 可以用 `sysctl net.ipv4.tcp_congestion_control` 查看系统当前默认值。

文档里的示例写法是：

```json
"streamSettings": {
  "sockopt": {
    "tcpcongestion": "bbr"
  }
}
```

这个设置只作用于 Xray 这个进程建立的连接，不会改系统里其他程序的算法。要注意它也需要内核里有对应算法才有效，它不能让不支持BBR的内核突然支持。

3x-ui 面板里 inbound/outbound 的"sockopt"高级设置能不能直接填这个字段，我没有逐版本核对；如果面板界面里没有对应输入框，需要改 Xray 配置的 JSON 模板，改之前先备份。

## 两种方式怎么选

| | 系统 sysctl（方式一） | Xray `tcpcongestion`（方式二） |
| --- | --- | --- |
| 作用范围 | 整台机器所有TCP连接 | 只对Xray进程的连接 |
| 改在哪里 | `/etc/sysctl.d/99-bbr-x-ui.conf` | Xray 配置的 `sockopt` |
| 需要内核支持 | 是 | 是 |
| 适合 | 想让整机开BBR，最常见 | 想只给Xray指定算法 |

多数情况直接用方式一就够了，面板脚本帮你做好了开启和关闭。

## 怎么验证BBR真的开了

不管用哪种方式，都用这三条命令确认：

```bash
sysctl net.ipv4.tcp_congestion_control
sysctl net.core.default_qdisc
lsmod | grep bbr
```

- 第一条输出 `bbr`，说明系统当前用的是BBR；
- 第二条输出 `fq`（或 `cake`），是面板脚本写入的队列规则；
- 第三条能看到 `tcp_bbr`，说明模块已加载。有些内核把BBR编译进内核本体，这时 `lsmod` 里可能没有输出，不一定是出错，以前两条为准。

重启之后再看一遍，确认配置是持久化的。如果开了BBR但网速没变化，先看 [为什么开了BBR，网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，BBR主要改善高延迟、有丢包的链路，跟面板是否限速、线路本身质量关系更大。

## 几个常见情况

- **用 Docker 部署的 3x-ui**：BBR是宿主机内核的设置，容器里改 `net.*` 参数通常受限（这一点我没有实测）。应该在宿主机上开BBR，不是进容器里开。Docker 部署带来的延迟问题可看 [3x-ui用Docker部署延迟暴涨，问题出在哪](https://vpsjq.com/2026/08/27/3x-ui-docker-latency/)。
- **Alpine 系统**：面板脚本对 Alpine 有没有专门处理，我没有核对源码确认；Alpine 开BBR的手动方法见 [Alpine Linux开启BBR的方法](https://vpsjq.com/2025/07/12/alpine-开启bbr/)。
- **Debian / Ubuntu 手动开启**：不想用面板菜单，可以看 [Debian和Ubuntu开启BBR加速的两种方式](https://vpsjq.com/2026/08/28/debian-ubuntu-bbr/)。
- **想用更新的 BBR3**：需要换 XanMod 之类的内核，见 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)。

3x-ui 的安装和面板配置可参考 [3x-ui安装：MHSanaei版官方脚本与面板配置](https://vpsjq.com/2026/04/30/2026-04-30-011/)。

## 小结

- BBR是内核的设置，x-ui、3x-ui、Xray 只是帮你改配置或指定算法。
- 最省事：运行 `x-ui`，选 Enable BBR；它写 `/etc/sysctl.d/99-bbr-x-ui.conf`，不检查内核版本。
- Xray 的 `tcpcongestion` 可以只给 Xray 指定算法，仅 Linux 有效，同样依赖内核支持。
- 开完用 `sysctl net.ipv4.tcp_congestion_control` 验证，重启后再确认一次。
