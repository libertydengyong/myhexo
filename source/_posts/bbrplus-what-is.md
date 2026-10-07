---
title: BBRplus是什么：作者是谁、GitHub仓库在哪、改了什么、为什么要换内核
date: 2026-10-07 23:00:00
tags:
  - BBR加速
  - BBRplus
  - Linux网络优化
categories:
  - Linux优化
description: BBRplus是网友在dog250修正BBR的代码基础上编译出来的第三方内核方案。依据cx9208和UJX6N的仓库说明、补丁源码和Jinwyp脚本菜单，讲清楚它的来历、作者的免责声明、和主线BBR代码的区别、GitHub仓库和内核版本，以及怎么确认开启。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBRplus是什么：作者是谁、GitHub仓库在哪、改了什么、为什么要换内核",
      "description": "BBRplus是网友在dog250修正BBR的代码基础上编译出来的第三方内核方案。依据cx9208和UJX6N的仓库说明、补丁源码和Jinwyp脚本菜单，讲清楚它的来历、作者的免责声明、和主线BBR代码的区别、GitHub仓库和内核版本，以及怎么确认开启。",
      "datePublished": "2026-10-07T23:00:00+08:00",
      "dateModified": "2026-10-07T23:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/bbrplus-what-is/",
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
          "name": "BBRplus是谁写的？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "BBRplus的代码不是cx9208写的。cx9208的README说明，dog250在一篇文章里指出原版BBR有高丢包率下易失速、收敛慢两个问题，并给出了他与BBR作者讨论后的修正代码；cx9208只是把它编译成内核并做成一键脚本，叫它bbr修正版或bbrplus。后来UJX6N在此基础上维护了更新内核版本的编译。"
          }
        },
        {
          "@type": "Question",
          "name": "BBRplus一定比原版BBR快吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不一定。cx9208的README明确写着这是一个实验性的修改，没有人对它的稳定性负责，也不担保它一定能产生正向的效果，请酌情使用。"
          }
        },
        {
          "@type": "Question",
          "name": "BBRplus为什么要换内核才能用？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "因为它不只是新增一个模块，还要修改内核的部分源码，比如inet_connection_sock.h里的数据结构大小和tcp_output.c里导出的函数，所以需要重新编译整个内核，装带有bbrplus的内核后才能把拥塞控制设成bbrplus。"
          }
        }
      ]
    }
  ]
}
</script>

在各种 BBR 教程里，"BBRplus"总是和 BBR、BBR2、魔改 BBR 混在一起出现，但很少有人讲清楚：它到底是谁做的、改了什么、GitHub 上哪个仓库才是对的、为什么非要换内核。这篇依据几个原始仓库的说明和补丁源码，把这些问题一次讲清，不夸大效果。

先说明依据：我读了 [cx9208/bbrplus](https://github.com/cx9208/bbrplus) 的 README 和源码，[UJX6N](https://github.com/UJX6N) 名下三个 BBRplus 仓库的 README 和补丁文件，把 6.9 内核的补丁文件和同版本 Linux 主线的 `tcp_bbr.c` 做了对比，还看了 Jinwyp 脚本和 `tcpx.sh` 里关于 BBRplus 的菜单。README 里提到的 dog250 的原文在 CSDN 上，我这里没有打开，下面只转述 cx9208 README 里对它的概括。GitHub Release 里的预编译包我这里看不到，所以仓库的"最后提交时间"是我今天克隆仓库读到的，不能代表 Release 有没有更新。**我没有实际安装和测速过 BBRplus**。

<!-- more -->

## 一句话：它是什么

BBRplus 是一个**第三方修改过的 BBR 拥塞控制算法**，以内核的形式提供。系统里启用它的方式，是把 `net.ipv4.tcp_congestion_control` 设成 `bbrplus`，对应的内核模块叫 `tcp_bbrplus`。BBR 本身是什么，见 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)。

## 来历：dog250 的修正，cx9208 编译，UJX6N 接着维护

cx9208 的 README 是这样交代来历的：

1. **dog250** 在一篇文章里（README 给的链接是 `blog.csdn.net/dog250/article/details/80629551`），指出了**原版 BBR 初版的两个问题**：一是**在高丢包率下容易失速**，二是**收敛慢**。文章提到他本人和 BBR 作者对这两个问题做了一些修正，并在文末给出了修正后的完整代码；
2. **cx9208** 说得很清楚：他"**只是将它编译出来（不是我写的）并做成了一键脚本**"，他把它叫作"bbr 修正版"，或者 bbrplus。README 对它的描述是：基于原版 BBR，修正上述问题，**尝试**使其更好，减少排队和丢包；
3. **UJX6N** 在 cx9208 的基础上，维护了适配更多内核版本的编译（仓库 README 写着"基于原始版本 cx9208/bbrplus"）。

所以"BBRplus 的作者"准确地说是：**算法修正来自 dog250，打包和脚本来自 cx9208，后续的新内核适配来自 UJX6N**。

## 作者自己说了什么：实验性，不保证有效

cx9208 的 README 里有一段加粗的话，我原文摘一下意思：**这是一个实验性的修改，没有人对它的稳定性负责，也不担保它一定能产生正向的效果，请酌情使用（at your own risk）**。另外还有：**不要在生产环境使用一键脚本，建议手动安装，进不了系统就用 VNC 切换内核**。

这一点值得单独说，因为网上不少教程写"BBRplus 比 BBR 更快"。从作者自己的说明看，这是一个试验性质的方案，**并没有承诺过更快**。站内 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/) 里写的"实际用下来比原版 BBR 快一点"，是实际使用感受的说法，不是作者的保证，也不是我测出来的，看的时候要有这个区分。

## 它到底改了什么：对比代码看到的

README 只给了一句"修正失速和收敛慢"，没有逐项说明。我把 UJX6N 仓库里的 6.9 内核补丁，和同版本 Linux 主线的 `net/ipv4/tcp_bbr.c` 做了对比。cx9208 的原版 4.14 代码里，我确认能看到其中的 ACK 聚合窗口、`bbr_drain_to_target` 和周期长度这几项，其余几项我只对比了 6.9 的补丁。能确认的区别有：

| 项目 | 主线 `tcp_bbr.c` | BBRplus |
| --- | --- | --- |
| 算法名 | `bbr` | `bbrplus`（模块描述文字仍是 "TCP BBR"） |
| ACK 聚合窗口 `bbr_extra_acked_win_rtts` | 5 | **10** |
| `bbr_drain_to_target` | 没有 | **新增，默认开启**，代码注释是"每个周期里，尽量保持小于 1 的增益，直到在途数据不超过 BDP" |
| PROBE_BW 周期长度 | 固定 8 个阶段 | 新增 `cycle_len`，周期长度**带随机成分** |
| `restore_cwnd` 标志 | 没有 | 有，注释是"决定把 cwnd 恢复到旧值" |
| 主线的 `bbr_pacing_margin_percent`（按估计带宽的约 1% 以下发送，以减少瓶颈排队） | 有，值为 1 | 这个常量在 BBRplus 的文件里没有出现 |
| 对 `tcp_congestion_ops` 的改动 | — | 补丁新增了 `tso_segs_goal` 回调，并修改了 `inet_connection_sock.h` 里私有数据区的大小 |

我要强调：**这些是代码层面的区别，我没有逐项分析它们对实际速度的影响，也没有做过测速**，所以不能据此说"哪个更快"。能说的只有：它确实不是原版 BBR 的简单换名，而是改了一些参数和逻辑；主线的 BBR 这几年也在更新，二者不能直接画等号。

UJX6N 的 6.x 仓库 README 还特别说明：它**并不是基于 6.x 版本的 BBR 修改的，只是把 4.14 版本的 BBRplus 简单移植了过去**，同时合并了 2018 到 2023 年之间官方 tcp_bbr 的补丁，并且保留了官方的 `tcp_bbr` 模块，所以在这个内核里，`bbrplus` 和 `bbr` 都可以选。

## 为什么要换内核

这是 BBRplus 和主线 BBR 最大的使用差别。主线 BBR 在较新的内核里已经内置，开启只要改 sysctl；而 BBRplus **要重新编译整个内核**。cx9208 的 README 给出的理由是：修正后的模块需要修改内核的部分源码。他的编译步骤里能看到具体改了哪里：

- 把 `include/net/inet_connection_sock.h` 里拥塞控制算法私有数据区的大小（`icsk_ca_priv`）改成 112 字节，对应的 `ICSK_CA_PRIV_SIZE` 改成 14 个 `u64`；
- 在 `net/ipv4/tcp_output.c` 里导出 `tcp_snd_wnd_test` 函数；
- 加入 `tcp_bbrplus.c`，并在 Makefile 里把原来的 `tcp_bbr` 换成 `tcp_bbrplus`。

所以 BBRplus **只有装了带它的内核才有**。README 的卸载方法也很干脆：装别的内核，bbrplus 就自动失效；卸载这个内核即可。cx9208 还特别提醒，他的内核编译方法只能用于 4.14.x，更高版本的 TCP 部分源码有改动，要移植得自己研究。这也是为什么后来需要有人（UJX6N）按内核版本逐个出补丁。

## GitHub 仓库一览

| 仓库 | 内容 | 最后一次提交（我克隆时读到的） |
| --- | --- | --- |
| [cx9208/bbrplus](https://github.com/cx9208/bbrplus) | 原版，4.14.129 内核，含 CentOS 7 的 rpm、Debian 9 的 deb 和 `tcp_bbrplus.c`，仓库带 GPL v3 的 LICENSE | 2019-07-10 |
| [UJX6N/bbrplus](https://github.com/UJX6N/bbrplus) | 4.14 自编译版，README 说明加了一个补丁避免部分虚拟机启动变慢，并合并了 2018 到 2021 年的官方 4.14 tcp_bbr 补丁 | 2022-12-16 |
| [UJX6N/bbrplus-5.10](https://github.com/UJX6N/bbrplus-5.10) | 5.10 版 | 2023-10-30 |
| [UJX6N/bbrplus-6.x_stable](https://github.com/UJX6N/bbrplus-6.x_stable) | 6.x 版，仓库里的补丁文件覆盖 6.0、6.2、6.3、6.4、6.5、6.7、6.8、6.9 | 2024-05-19 |
| [ylx2016/Linux-NetSpeed](https://github.com/ylx2016/Linux-NetSpeed) | 一键脚本 `tcpx.sh`，菜单里有 BBRplus 内核和"BBRplus 新版内核"两项 | 脚本更新频繁，见站内 [常用VPS TCP加速脚本汇总](https://vpsjq.com/2026/08/29/vps-tcp-scripts/) |

要留意两点：

- **仓库的最后提交时间是仓库本身的，预编译内核放在 Release 里，Release 有没有更新我这里看不到**。我只能说：UJX6N 的 6.x 仓库里，我没有看到 6.10 及以上版本的补丁文件；
- 站内 [BBRplus内核版本不支持怎么办](https://vpsjq.com/2026/09/06/bbrplus-kernel-version-unsupported/) 讲了脚本指向旧仓库导致"内核版本不支持"的排查办法，那里写"UJX6N 目前比较活跃"这一点，和这里看到的提交时间有出入，使用前请以你当时看到的仓库和 Release 页面为准。

## 内核版本怎么选

Jinwyp 脚本的菜单里，BBRplus 内核的选项是这样排的（编号以脚本当前版本为准）：

| 编号 | 内核 | 编译者 |
| --- | --- | --- |
| 61 | 4.14.129 LTS，菜单标注"cx9208 编译的 dog250 原版，推荐使用" | cx9208 |
| 62 到 67 | 4.14、4.19、5.10、5.15、6.1、6.6 的 LTS 版 | UJX6N |
| 68 | "最新版内核 6.7 或更高版本" | UJX6N |

`tcpx.sh` 里则是"安装 BBRplus 版内核"（装 cx9208 的 4.14.129 包）和"安装 BBRplus 新版内核"（从 UJX6N 的 6.x 仓库的 Release 里取包）两项。具体怎么选，主要看你的系统和内核，装之前要先对上系统版本，见 [Jinwyp一键脚本安装BBR和BBRplus内核教程](https://vpsjq.com/2026/09/06/jinwyp-one-click-script-bbr/)。

## 怎么确认 BBRplus 真的开了

按 cx9208 的 README，装完内核重启后检查三项：

```bash
uname -r                                  # 内核版本带有 bbrplus 字样
lsmod | grep bbrplus                      # 能看到 tcp_bbrplus
sysctl net.ipv4.tcp_congestion_control    # 输出 bbrplus
```

README 里的手动步骤还把队列规则设成 `fq`（`net.core.default_qdisc=fq`）。UJX6N 的 6.x 仓库 README 则明确写着：**`fq` 是唯一推荐的队列调度器，不要用 `fq_codel`、`fq_pie`、`cake` 等**。这一点我在 [BBRplus要不要搭配FQ](https://vpsjq.com/2026/10/04/bbrplus-fq-qdisc/) 里当时没有查到，这里补上。

没有生效的话，常见原因和处理见 [已安装BBR加速内核但加速模块未加载的解决方法](https://vpsjq.com/2026/08/30/bbr-module-not-loaded/) 和 [BBRplus报错sysctl No such file or directory的三个真实原因](https://vpsjq.com/2026/09/07/bbrplus-sysctl-no-such-file/)；换内核重启后连不上服务器，见 [装BBRplus重启后连不上服务器怎么办](https://vpsjq.com/2026/09/06/bbrplus-reboot-connection-lost/)。

## 该不该用

结合上面这些：

- 作者自己写明是实验性方案，不保证效果，也不建议在生产环境用一键脚本；
- 它需要换内核，换内核本身就有"重启后进不了系统"的风险，所以要有 VNC 或控制台可以救急；
- 容器类的机器（比如 OpenVZ、LXC）共用宿主机内核，没法换内核，用不了；
- 日常用途，内核自带的 BBR，或者 XanMod 内核的 BBR3（见 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)），换内核的风险和维护成本都更低；
- 想比较锐速、BBR、BBRplus 怎么选，见 [锐速（LotServer）是什么，跟BBR/BBRplus怎么选](https://vpsjq.com/2026/09/06/lotserver-vs-bbr/)；
- 脚本里还有"魔改 BBR""暴力 BBR"这类名字，别和 BBRplus 混为一谈，见 [BBR魔改版是什么](https://vpsjq.com/2026/10/04/bbr-modified-tsunami-nanqinlang/)。

## 小结

- BBRplus 的算法修正来自 dog250，cx9208 负责编译和脚本，UJX6N 后续维护新内核版本；
- 作者明确说是实验性修改，不保证更快，也不建议生产环境用一键脚本；
- 它和主线 BBR 在代码上有区别（ACK 聚合窗口、drain_to_target、周期长度随机等），但这些对速度的实际影响我没有测过；
- 需要重新编译内核，所以只有装了带 bbrplus 的内核才能用，容器里用不了；
- 确认方法：`uname -r`、`lsmod | grep bbrplus`、`sysctl net.ipv4.tcp_congestion_control`；
- 本文依据仓库说明和补丁源码，没有实际安装和测速。
