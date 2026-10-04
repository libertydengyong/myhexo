---
title: BBR2脚本怎么用：Jinwyp脚本开启BBR2的前提，为什么新版XanMod上找不到bbr2
date: 2026-10-04 13:00:00
tags:
  - BBR加速
  - BBR2
  - XanMod
categories:
  - Linux优化
description: 想用脚本开启BBR2，必须先有带bbr2模块的内核。依据Jinwyp一键脚本、tcpx.sh和XanMod内核源码，讲清楚BBR2脚本的前提、XanMod 5.x和6.x的区别，以及现在更合适的做法。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBR2脚本怎么用：Jinwyp脚本开启BBR2的前提，为什么新版XanMod上找不到bbr2",
      "description": "想用脚本开启BBR2，必须先有带bbr2模块的内核。依据Jinwyp一键脚本、tcpx.sh和XanMod内核源码，讲清楚BBR2脚本的前提、XanMod 5.x和6.x的区别，以及现在更合适的做法。",
      "datePublished": "2026-10-04T13:00:00+08:00",
      "dateModified": "2026-10-04T13:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/bbr2-script-xanmod/",
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
          "name": "哪个脚本可以开启BBR2？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Jinwyp的一键脚本（one_click_script）菜单里可以选择开启BBR2，但脚本要求当前内核名字里带xanmod，否则会提示无法开启BBR2并改为开启BBR。tcpx.sh里只有识别bbr2运行状态的代码，我没有在它的菜单里看到BBR2的安装项。"
          }
        },
        {
          "@type": "Question",
          "name": "为什么装了XanMod却找不到bbr2？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "我读XanMod内核源码的结果是：5.10和5.15分支带有tcp_bbr2.c，算法名是bbr2；6.1和6.6分支没有tcp_bbr2.c，tcp_bbr.c里是BBR v3的实现，算法名仍然叫bbr。所以装6.x的XanMod，系统里不会有名叫bbr2的算法，要用的是bbr（也就是BBR3）。"
          }
        },
        {
          "@type": "Question",
          "name": "现在还有必要用BBR2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "日常VPS不建议专门找BBR2。需要比原版BBR更新的版本，直接用6.x的XanMod内核和BBR3；不想换内核，用内核自带的BBR即可。"
          }
        }
      ]
    }
  ]
}
</script>

搜"bbr2 脚本"的人，多半想找一个一键装好BBR2的脚本。先说结论：BBR2 不在主线内核里，没有哪个脚本能在普通内核上"一键开启"它，要有带 `bbr2` 模块的内核才行；而新版 XanMod 内核已经没有 bbr2 了。下面依据脚本和内核源码把前提讲清楚。

先说明依据：脚本内容来自 [jinwyp/one_click_script](https://github.com/jinwyp/one_click_script) 的 `install_kernel.sh` 和 [ylx2016/Linux-NetSpeed](https://github.com/ylx2016/Linux-NetSpeed) 的 `tcpx.sh`；内核部分来自 [xanmod/linux](https://github.com/xanmod/linux) 各分支的 `net/ipv4` 目录。我没有在机器上实际运行这些脚本，凡是推断的地方都会注明。

<!-- more -->

## BBR2 在哪里能找到

BBR2 是 Google 在原版 BBR 基础上做的改进，一直没有进入主线内核（背景见 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)）。所以它只能出现在带补丁的第三方内核里。

我对照了 XanMod 内核源码的几个分支，结果是：

| XanMod 分支 | 有没有 `tcp_bbr2.c` | `tcp_bbr.c` 里的内容 |
| --- | --- | --- |
| 5.10 | 有，算法名 `bbr2` | 原版 |
| 5.15 | 有，算法名 `bbr2` | 原版 |
| 6.1 | 没有 | 里面是 "BBR v3" 的状态定义，算法名仍是 `bbr` |
| 6.6 | 没有 | 同上 |

6.12、6.18 我没有查到对应分支文件，不下结论；可以肯定的是，6.1 和 6.6 这两个常见版本上，已经没有名叫 `bbr2` 的算法，BBR3 是直接替换了 `bbr`。BBR3 的用法见 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)。

## Jinwyp 脚本怎么开启 BBR2

我读到的 Jinwyp 脚本，菜单里"开启 BBR 或 BBR2"这一项做的事情大致是：

1. 先问你选 `1` BBR 还是 `2` BBR2，并提示"选 2 BBR2 需要内核为 XanMod"；
2. 选 2 时检查当前内核名字里有没有 `xanmod`。没有的话，脚本会红字提示"当前系统内核没有安装 XanMod 内核, 无法开启BBR2, 改为开启BBR"，然后写入 BBR；
3. 有 `xanmod` 的话，还会问要不要开 ECN，并红字提醒"开启 ECN 可能会造成网络设备无法访问"；
4. 接着让你选队列算法（FQ / FQ-Codel / FQ-PIE / CAKE），然后把 `net.core.default_qdisc`、`net.ipv4.tcp_congestion_control=bbr2`、`net.ipv4.tcp_ecn` 追加写进 `/etc/sysctl.conf`，执行 `sysctl -p`。

注意脚本判断"能不能开 BBR2"的条件只是**内核名字里有 xanmod**，没有再检查内核里是否真有 `bbr2` 模块。结合上一节的结论，我推断：如果装的是 6.x 的 XanMod（脚本当前菜单里的 51 是 XanMod 6.6 LTS，52 是 XanMod 6.11），选 2 虽然能通过脚本的检查，但内核里并没有 `bbr2` 这个算法，设置不会成功。这是我读代码和源码后的推断，没有实测，实际表现请以你机器上的输出为准。

另外，我之前写的 [Jinwyp一键脚本安装BBR和BBRplus内核教程](https://vpsjq.com/2026/09/06/jinwyp-one-click-script-bbr/) 里写的是"选 51 装 XanMod LTS 5.10 内核再启用 BBR2"，对照当前脚本菜单，51 是 6.6 LTS 而不是 5.10，那篇的编号可能是旧版本的，使用前以脚本屏幕上显示的菜单为准。

## tcpx.sh 里有 BBR2 吗

`tcpx.sh` 里只有一处和 bbr2 相关：判断运行状态时，如果 `tcp_congestion_control` 的值是 `bbr2`，就显示"BBR2启动成功"。我读到的当前菜单里（内核安装、加速启用两组）没有 BBR2 的安装或启用项。所以它只是兼容以前装过 BBR2 的机器，不是现在拿来装 BBR2 的脚本。

## 怎么确认自己的内核有没有 bbr2

不用装任何东西，两条命令就能知道：

```bash
sysctl net.ipv4.tcp_available_congestion_control
modprobe tcp_bbr2 && lsmod | grep bbr2
```

- 第一条列出的算法里有 `bbr2`，才能用；
- 第二条是尝试加载模块，提示找不到模块，说明内核里没有 BBR2。

没有的话，写再多 `tcp_congestion_control=bbr2` 也没用。内核没带 BBR 模块的常见症状见 [已安装BBR加速内核但加速模块未加载的解决方法](https://vpsjq.com/2026/08/30/bbr-module-not-loaded/)。

## 现在该怎么选

- **只想让 BBR 跑起来**：内核 4.9 以上直接开原版 BBR 就行；
- **想用更新的算法**：装 6.x 的 XanMod，用的是 BBR3，不需要再找 BBR2；也可以用 byJoey 的脚本，见 [BBR3一键安装脚本](https://vpsjq.com/2026/08/28/bbr3-install/)；
- **一定要用 BBR2**：只能装 5.10 或 5.15 的 XanMod，再开 `bbr2`。这两个内核比较旧，我不推荐为了 BBR2 专门去装。

## 小结

- BBR2 不在主线内核里，脚本只能在带 `bbr2` 模块的内核上开启它；
- Jinwyp 脚本只检查内核名里有没有 `xanmod`，不检查 `bbr2` 模块在不在；
- 我对照 XanMod 源码，5.10 和 5.15 有 `bbr2`，6.1 和 6.6 没有，用的是 `bbr`（BBR3）；
- tcpx.sh 里只有 BBR2 的状态识别，没有安装项。
