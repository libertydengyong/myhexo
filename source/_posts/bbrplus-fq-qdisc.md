---
title: BBRplus要不要搭配FQ：fq、fq_pie、cake怎么选，怎么确认生效
date: 2026-10-04 12:00:00
tags:
  - BBR加速
  - BBRplus
  - Linux网络优化
categories:
  - Linux优化
description: 脚本里的BBRplus+FQ指的是拥塞控制用bbrplus、队列规则用fq。依据Linux内核tcp_bbr.c注释和Linux-NetSpeed的tcpx.sh源码，讲清楚FQ是什么、不配会怎样、fq_pie和cake怎么选，以及怎么确认真的生效。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBRplus要不要搭配FQ：fq、fq_pie、cake怎么选，怎么确认生效",
      "description": "脚本里的BBRplus+FQ指的是拥塞控制用bbrplus、队列规则用fq。依据Linux内核tcp_bbr.c注释和Linux-NetSpeed的tcpx.sh源码，讲清楚FQ是什么、不配会怎样、fq_pie和cake怎么选，以及怎么确认真的生效。",
      "datePublished": "2026-10-04T12:00:00+08:00",
      "dateModified": "2026-10-04T12:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/bbrplus-fq-qdisc/",
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
          "name": "BBRplus+FQ是什么意思？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "是两个独立的设置：net.ipv4.tcp_congestion_control设成bbrplus（拥塞控制算法），net.core.default_qdisc设成fq（队列规则）。tcpx.sh菜单里的23号选项就是写入这两项。"
          }
        },
        {
          "@type": "Question",
          "name": "BBR一定要配FQ吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是必须。Linux内核tcp_bbr.c的注释写的是BBR可以搭配开启pacing的fq队列规则使用，否则TCP协议栈会退回到内部pacing，每个TCP连接用一个高精度定时器，可能占用更多资源。所以配fq是推荐做法，但没配也不会让BBR直接失效。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么确认fq真的生效了？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "先用sysctl net.core.default_qdisc看配置值，再用tc qdisc show看网卡上实际挂的是什么队列规则。配置写入后如果网卡上还不是fq，重启一次再看。"
          }
        }
      ]
    }
  ]
}
</script>

脚本菜单里经常看到"使用BBRplus+FQ版加速""使用BBR+FQ加速"这类选项，很多人会问：FQ是什么？不选FQ会怎么样？旁边的 fq_pie、cake 又是什么？这篇依据 Linux 内核源码里的注释和 [Linux-NetSpeed](https://github.com/ylx2016/Linux-NetSpeed) 的 `tcpx.sh` 源码，把这几个问题理一遍。

先说明：下面是读源码得到的结论，我没有做过 fq、fq_pie、cake 的速度对比测试，所以不会给"哪个更快"的结论；没有核对的地方都会注明。

<!-- more -->

## "BBRplus+FQ"其实是两个独立的设置

Linux 里和这件事相关的有两个 sysctl 参数：

| 参数 | 作用 | 例子 |
| --- | --- | --- |
| `net.ipv4.tcp_congestion_control` | 拥塞控制算法，决定"发多快" | `bbr`、`bbrplus`、`cubic` |
| `net.core.default_qdisc` | 默认队列规则，决定"包怎么排队发出网卡" | `fq`、`fq_pie`、`cake`、`pfifo_fast` |

"BBRplus+FQ"就是前者设成 `bbrplus`，后者设成 `fq`。两个参数可以分开设置，脚本只是把它们打包成一个菜单选项。BBRplus 本身是什么，见 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)。

## 不配FQ会怎样

Linux 内核里 BBR 的源码 `net/ipv4/tcp_bbr.c` 有一段注释，大意是：

> BBR 可以搭配开启 pacing 的 fq 队列规则使用；否则 TCP 协议栈会退回到内部的 pacing 实现，每个 TCP 套接字使用一个高精度定时器，可能占用更多资源。

所以对原版 BBR 来说，结论是：

- **推荐配 fq**：这是内核作者自己写的搭配方式；
- **不配也不是直接失效**：没有 fq 时内核会自己做 pacing，只是代价是 CPU 等资源占用可能更高。

这和站内另一篇 [为什么开了BBR，网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/) 里"必须设成 fq，否则 BBR 效果会打折扣"的说法相比，要更谨慎一些：从内核注释看，不配 fq 的主要影响是资源占用，至于对实际速度的影响，我没有测过，不下结论。

BBRplus 是第三方内核里的算法，我没有读过它的源码，不确定它是否有和原版 BBR 一样的 pacing 行为，所以"BBRplus 不配 fq 会怎样"这一点我没有核对，只能说脚本给 BBRplus 配的默认搭配是 fq。

## tcpx.sh 菜单里这几项分别是什么

我读到的 `tcpx.sh` 里，"加速启用"这一组菜单是：

| 编号 | 菜单文字 | 实际写入 |
| --- | --- | --- |
| 20 | 使用BBR+FQ加速 | `default_qdisc=fq`，`tcp_congestion_control=bbr` |
| 21 | 使用BBR+FQ_PIE加速 | `default_qdisc=fq_pie`，`tcp_congestion_control=bbr` |
| 22 | 使用BBR+CAKE加速 | `default_qdisc=cake`，`tcp_congestion_control=bbr` |
| 23 | 使用BBRplus+FQ版加速 | `default_qdisc=fq`，`tcp_congestion_control=bbrplus` |

注意两点：

- **菜单里只有 BBRplus+FQ 这一种 BBRplus 搭配**，没有 BBRplus+CAKE 或 BBRplus+FQ_PIE 的选项。
- 这个编号是我读到的当前版本里的，不同版本可能会变，以你屏幕上看到的菜单文字为准。

这几项都走同一个函数 `enable_acceleration`，它大致做了这些事（来自源码）：

1. 先清理旧的 BBR 或锐速配置；
2. 用 `modprobe sch_fq`（或对应的 `sch_fq_pie`、`sch_cake`）加载队列规则模块，并把模块名写进 `/etc/modules-load.d/tcpx-qdisc.conf`，让它开机自动加载；
3. 把 `net.core.default_qdisc=…` 和 `net.ipv4.tcp_congestion_control=…` 追加写进 sysctl 配置文件；
4. 执行 `sysctl --system` 应用，并提示"如果未立即生效，请重启服务器"。

其中第 2 步说明：fq_pie、cake 要内核里有对应模块才能用，不是所有精简内核都带。

## fq、fq_pie、cake怎么选

我没有做过对比测试，下面只列出来源明确的信息：

- **fq**：内核 BBR 源码注释里点名的搭配，也是脚本里 BBR 和 BBRplus 两种算法都提供的选项，没有特殊需求就选它。
- **fq_pie、cake**：脚本只给原版 BBR 提供了这两个选项。我之前在 [Jinwyp一键脚本安装BBR和BBRplus内核教程](https://vpsjq.com/2026/09/06/jinwyp-one-click-script-bbr/)里记录过，Jinwyp 脚本启用 BBR 时会问"搭配 Cake 还是 FQ"，并推荐 Cake。这是该脚本的建议，不是我实测的结论。

所以比较稳妥的做法是：BBRplus 就选脚本给的 BBRplus+FQ；原版 BBR 默认选 fq，想试 cake 的话，先确认内核有 `sch_cake` 模块，再换一次对比，别只听一面之词。

## 怎么确认fq真的生效了

三条命令，看配置和实际状态：

```bash
sysctl net.ipv4.tcp_congestion_control
sysctl net.core.default_qdisc
tc qdisc show
```

- 第一条应该输出 `bbr` 或 `bbrplus`（和你选的一致）；
- 第二条应该输出 `fq`，这是"默认值"的配置；
- 第三条列出每块网卡上实际挂着的队列规则，能看到 `qdisc fq` 才说明网卡上真的在用 fq。

如果第二条是 `fq`，第三条却不是，按我的理解（没有实测），`default_qdisc` 是新建队列规则时用的默认值，已经在运行的网卡不一定立刻换掉，重启一次再看最稳；脚本自己也提示"如果未立即生效，请重启服务器"。

如果重启后第一条没变成 `bbrplus`，那是算法没加载成功的问题，和队列规则无关，可以看 [已安装BBR加速内核但加速模块未加载的解决方法](https://vpsjq.com/2026/08/30/bbr-module-not-loaded/) 和 [BBRplus报错sysctl No such file or directory的三个真实原因](https://vpsjq.com/2026/09/07/bbrplus-sysctl-no-such-file/)。

## 小结

- "BBRplus+FQ"是两个独立设置：`bbrplus` 管发多快，`fq` 管怎么排队。
- 内核 BBR 源码注释推荐搭配 fq，不配则退回内核内部 pacing，代价是可能占用更多资源，不会让 BBR 直接失效。
- tcpx.sh 里 BBRplus 只有 BBRplus+FQ 一种搭配，fq_pie 和 cake 只给原版 BBR。
- 验证看 `sysctl` 的两个值，再用 `tc qdisc show` 看网卡上实际挂的队列规则。
