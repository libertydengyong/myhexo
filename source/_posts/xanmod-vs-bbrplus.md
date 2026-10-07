---
title: XanMod和BBRplus怎么选：一个是整套内核，一个是BBR改版，代码上差在哪
date: 2026-10-08 18:00:00
tags:
  - XanMod内核
  - BBRplus
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: XanMod是整套第三方内核，BBRplus是第三方改的BBR算法，两者不是同一层面的东西。对照XanMod官方源码里的BBR v3和BBRplus补丁，讲清楚各自是什么、代码差异、能不能叠加，以及该怎么选。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "XanMod和BBRplus怎么选：一个是整套内核，一个是BBR改版，代码上差在哪",
      "description": "XanMod是整套第三方内核，BBRplus是第三方改的BBR算法，两者不是同一层面的东西。对照XanMod官方源码里的BBR v3和BBRplus补丁，讲清楚各自是什么、代码差异、能不能叠加，以及该怎么选。",
      "datePublished": "2026-10-08T18:00:00+08:00",
      "dateModified": "2026-10-08T18:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/08/xanmod-vs-bbrplus/",
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
          "name": "XanMod和BBRplus有什么区别？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "XanMod是一整套第三方Linux内核，BBRplus只是一个第三方修改的BBR拥塞控制算法，要靠编译进内核才能用。XanMod的6.6和6.18官方分支里自带的tcp_bbr.c是BBR v3，算法名叫bbr；BBRplus的算法名叫bbrplus，和BBR v3是两套不同的代码。"
          }
        },
        {
          "@type": "Question",
          "name": "XanMod上能再装BBRplus吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "我没有验证。BBRplus要通过补丁重新编译内核，UJX6N仓库里的补丁文件覆盖到6.9，对应XanMod最新的6.18和7.2没有现成补丁；系统默认的拥塞控制同一时刻也只有一个，没有叠加使用的必要。"
          }
        },
        {
          "@type": "Question",
          "name": "XanMod的BBR和BBRplus哪个更快？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "我没有测过，不下结论。BBRplus作者自己说是实验性修改、不保证更快。线路本身的质量对速度的影响通常比算法大。"
          }
        }
      ]
    }
  ]
}
</script>

搜"xanmod bbrplus 对比"的人，常见的想法是：XanMod 和 BBRplus 是两种加速方案，选哪个更快？先说清楚：**它们不是同一层面的东西**。XanMod 是一整套内核，BBRplus 只是内核里的一个拥塞控制算法。真正能对比的是"XanMod 里自带的 BBR"和"BBRplus"，这篇依据官方源码把这两者的差异读出来。

我没有测过速度，所以不给"哪个更快"的结论，没核对的地方都会注明。

<!-- more -->

## 先分清层面

| | XanMod | BBRplus |
| --- | --- | --- |
| 是什么 | 一整套第三方 Linux 内核（调度、内存、网络等一堆改动） | 一个第三方改的 BBR 算法，算法名 `bbrplus` |
| 怎么用 | `apt` 装官方软件包，Debian/Ubuntu | 要装一个编译好带 `bbrplus` 的内核，或者给内核打补丁自己编译 |
| 内核里的 BBR | 算法名 `bbr`，下面读到是 BBR v3 | 不依赖 XanMod，是另一套代码 |

XanMod 的介绍见 [XanMod、Zen、Liquorix内核怎么选](https://vpsjq.com/2026/10/08/xanmod-zen-liquorix-compare/)，BBRplus 的来历、作者、仓库见 [BBRplus是什么](https://vpsjq.com/2026/10/07/bbrplus-what-is/)。

## XanMod 里的 BBR 到底是哪个版本

我读了 XanMod GitLab 官方仓库里的 `net/ipv4/tcp_bbr.c`：

| 分支 | 读到的情况 |
| --- | --- |
| 6.18 | 文件里有 `#define BBR_VERSION 3`，`MODULE_VERSION` 用的就是它，注册的算法名是 `bbr`，内核配置里 `TCP_CONG_BBR=y`，默认拥塞控制 `bbr` |
| 6.6 | 同样是 `BBR_VERSION 3`，算法名 `bbr`，配置同样默认 `bbr` |
| 5.15 | 单独的 `tcp_bbr.c`（1188 行，没有 v3 标记）加一个独立的 `tcp_bbr2.c` |

所以这解决了站内 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/) 里留的一个疑问：**XanMod 6.6 和 6.18 的 `bbr` 就是 BBR v3**，名字没改；5.15 这条分支的 `bbr` 不是 v3，BBR2 是另一个模块。

## 代码上差在哪

BBRplus 的改动见 [BBRplus是什么](https://vpsjq.com/2026/10/07/bbrplus-what-is/) 里的对比表，下面把 XanMod 6.18 里读到的 BBR v3 放在旁边：

| 项目 | BBRplus | XanMod 6.18 的 BBR v3 |
| --- | --- | --- |
| 算法名 | `bbrplus` | `bbr` |
| ACK 聚合窗口 `bbr_extra_acked_win_rtts` | 10 | 5（和老版主线一样） |
| `bbr_pacing_margin_percent` | 文件里没有 | 有，值为 1 |
| `bbr_drain_to_target`、周期长度带随机成分 | 有 | 没有这两项 |
| 对丢包和 ECN 的响应 | 站内那篇对比表里没有这一项，我这次没有逐行重新核对 | 有：`bbr_loss_thresh`（丢包率阈值 2%）、`bbr_beta`（0.3）、`bbr_ecn_thresh`（50%）、`bbr_full_loss_cnt`（6）、`bbr_inflight_headroom`（15%） |
| 带宽/在途数据的上下界 | 没有 | 有，文件头部注释写有 `bw_lo`/`bw_hi`、`inflight_lo`/`inflight_hi` |

这些常量都是我读源码看到的。**它们对实际速度影响多大，我没有测**；BBRplus 作者自己也说是实验性修改，不保证更快。

从代码看，两者的思路不一样：BBRplus 是在老版 BBR 上加几个策略（排空、随机周期等），BBR v3 是在模型里加上了对丢包和 ECN 的响应，以及带宽和在途数据的上下界。至于哪种在你的线路上更合适，只能自己测。

## 队列规则：都建议 fq

- 内核 BBR 源码注释写的是：BBR 可以搭配开启 pacing 的 `fq`，否则 TCP 协议栈会退回内部 pacing，每个 socket 用一个高精度定时器，可能占用更多资源。这段注释在 XanMod 6.18 的 `tcp_bbr.c` 里也保留着。
- UJX6N 的 BBRplus 6.x 仓库 README 写明，在它编译的内核里 `fq` 是唯一推荐的，不要用 `fq_codel`、`fq_pie`、`cake`。
- 注意 XanMod 6.18 的配置里 `NET_SCH_DEFAULT` 没有设置，`fq` 是以模块提供的，不会自动变成默认队列规则，需要自己设 `net.core.default_qdisc=fq`。设置和确认方法见 [BBRplus要不要搭配FQ](https://vpsjq.com/2026/10/04/bbrplus-fq-qdisc/)。

## 能不能叠加

- 系统的默认拥塞控制 `net.ipv4.tcp_congestion_control` 同一时刻只有一个值，所以不存在"两个同时跑"。
- BBRplus 靠补丁重新编译内核，UJX6N 6.x 仓库里的补丁文件覆盖到 6.9，仓库最后提交是 2024-05-19；XanMod 现在最新的是 6.18 和 7.2，我没有看到对应的 BBRplus 补丁。
- 把 BBRplus 补丁打到 XanMod 上这件事，我没有验证过，不建议这么做。

## 怎么选

1. **Debian / Ubuntu 的 KVM VPS，想换内核**：装 XanMod，6.6 和 6.18 的 `bbr` 就是 v3，不用额外找补丁，见 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)。换内核前先看 [XanMod内核安装失败怎么办](https://vpsjq.com/2026/08/27/xanmod-install-fail/)。
2. **想试 BBRplus**：它要换成专门编译的内核，作者自己说是实验性、不建议生产环境用一键脚本，风险见 [装BBRplus重启后连不上服务器怎么办](https://vpsjq.com/2026/09/06/bbrplus-reboot-connection-lost/)。
3. **CentOS、Rocky、AlmaLinux**：XanMod 没有官方 RPM，见 [CentOS、Rocky、AlmaLinux能装XanMod内核吗](https://vpsjq.com/2026/10/08/xanmod-centos-rocky-alma/)；BBRplus 的老内核包在站内文章里提过，但要先确认内核版本，见 [BBRplus内核版本不支持怎么办](https://vpsjq.com/2026/09/06/bbrplus-kernel-version-unsupported/)。
4. **OpenVZ、LXC 这类容器**：共用宿主机内核，两个都装不了。
5. **只是想开 BBR**：系统内核够新就直接开自带的 BBR，不一定要换内核，见 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)。

## 常见问题

**XanMod 和 BBRplus 哪个更快？**
我没有测过，不下结论。线路本身的质量对速度的影响通常比算法大。

**装了 XanMod 还要装 BBRplus 吗？**
不需要，也没必要叠加。XanMod 6.6 和 6.18 里 `bbr` 已经是 v3。

**怎么确认 XanMod 里的 `bbr` 是 v3？**
看内核版本：6.6 和 6.18 的官方分支是 v3；5.15 分支不是。我没有在运行中的系统里找到比"看分支源码"更直接的方法，所以这条是依据源码，不是实测。

## 小结

- XanMod 是整套内核，BBRplus 是一个第三方改的算法，不在同一层面。
- XanMod 官方 6.6 和 6.18 分支里的 `bbr` 是 BBR v3（源码有 `BBR_VERSION 3`），5.15 分支不是。
- BBRplus 的改动是排空、周期随机、ACK 窗口加大等；BBR v3 加的是丢包和 ECN 响应、带宽和在途数据的上下界。
- 两者都建议搭配 `fq`；XanMod 6.18 默认没有把 `fq` 设为默认队列规则。
- 没有测过速度，没有验证过把 BBRplus 打到 XanMod 上。
- 依据：GitLab `xanmod/linux` 的 6.18、6.6、5.15 分支的 `tcp_bbr.c` 和内核配置，以及站内已写的 BBRplus 补丁分析，读取时间 2026-10-07。
