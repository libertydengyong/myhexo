---
title: XanMod、Zen、Liquorix内核怎么选：区别、CacULE还在不在、VPS该装哪个
date: 2026-10-08 14:00:00
tags:
  - XanMod内核
  - Zen内核
  - Liquorix内核
  - Linux内核
categories:
  - Linux优化
description: 对照XanMod、Zen、Liquorix三个第三方内核的官方源码和配置文件，讲清楚各自是什么、调度器和抢占模式有什么不同、CacULE和TT调度器为什么找不到了，以及跑代理或建站的VPS该选哪个。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "XanMod、Zen、Liquorix内核怎么选：区别、CacULE还在不在、VPS该装哪个",
      "description": "对照XanMod、Zen、Liquorix三个第三方内核的官方源码和配置文件，讲清楚各自是什么、调度器和抢占模式有什么不同、CacULE和TT调度器为什么找不到了，以及跑代理或建站的VPS该选哪个。",
      "datePublished": "2026-10-08T14:00:00+08:00",
      "dateModified": "2026-10-08T14:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/08/xanmod-zen-liquorix-compare/",
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
          "name": "XanMod和Zen内核有什么区别？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "两者都是第三方修改的Linux内核，但取向不同。Zen内核源码里的ZEN_INTERACTIVE选项（默认开启）自述是用吞吐量和功耗换响应速度，面向桌面交互；XanMod官方配置则是PREEMPT_LAZY加HZ=250，没有开启这类交互优先的调整。Zen本身主要是源码和补丁，Liquorix是基于Zen源码打包的发行版。"
          }
        },
        {
          "@type": "Question",
          "name": "XanMod的CacULE调度器还在吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "XanMod官方仓库里只有5.9到5.14这几条独立的cacule分支，5.15之后没有对应分支，我读到的6.18官方配置里也没有CACULE选项。想用最新版XanMod的话，调度器是内核自带的，没有CacULE可选。"
          }
        },
        {
          "@type": "Question",
          "name": "跑代理节点的VPS应该装XanMod、Zen还是Liquorix？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按官方说明，Zen和Liquorix偏桌面交互，服务器没有响应延迟方面的需求，没有必要选它们。要换第三方内核的话，XanMod更常见，也有更新到最新内核的官方源码。我没有做过这三个内核的速度对比，线路本身的质量对速度的影响通常比内核大。"
          }
        }
      ]
    }
  ]
}
</script>

搜"xanmod zen""xanmod cacule""xanmod 游戏""xanmod内核和zen内核"的人，大多是想弄清楚：这几个第三方内核到底有什么区别，该装哪个。这篇不测速度，只依据官方源码仓库和配置文件，把它们的真实差异摆出来，没核对到的地方会直接标明。

先说结论：**XanMod、Zen、Liquorix 是三个不同的东西**，Liquorix 是用 Zen 源码打包的，XanMod 是另一条独立的线；Zen 和 Liquorix 的取向是桌面交互，跑 VPS 没有必要选它们。

<!-- more -->

## 先分清三个名字

| 名字 | 是什么 | 官方源码位置 |
| --- | --- | --- |
| XanMod | 独立维护的第三方内核，作者在提交里署名 Alexandre Frade | GitLab：`xanmod/linux` |
| Zen | `zen-kernel` 项目，主要是一套源码树和补丁 | GitHub：`zen-kernel/zen-kernel` |
| Liquorix | 用 Zen 源码打成 Debian/Ubuntu 等发行版软件包的内核 | GitHub：`damentz/liquorix-package` |

Liquorix 这一点有明确依据：它的 Fedora 打包文件写的是"built from the Zen kernel sources"（基于 Zen 内核源码构建），Debian 打包里的补丁文件名是 `zen/v7.2.9-lqx2.patch`，README 也指向 `zen-kernel/zen-kernel`。所以 Zen 和 Liquorix 是一脉，XanMod 是另一脉。

## 一个常被忽略的事：XanMod 的 GitHub 仓库已经不更新了

我用 `git ls-remote` 看了 GitHub 上的 `xanmod/linux`：分支只到 6.11，最新标签是 `6.11.5-xanmod1`。而 GitLab 上的 `xanmod/linux` 分支一直到 7.2，我查看时最新标签是 `7.2.9-xanmod1`，LTS 的 `6.18.55-xanmod1` 提交日期是 2026-10-03。

所以想看 XanMod 最新源码或配置，要去 GitLab，别看 GitHub 上的旧镜像。GitHub 上很多旧教程引用的就是这个已经停在 6.11 的仓库。

## 配置对比：从官方文件里读到的

下面的数字来自官方仓库里的实际配置文件，不是宣传页：

| 项目 | XanMod 6.18（x64v3 构建） | Liquorix（Debian 配置，7.2） |
| --- | --- | --- |
| 抢占模式 | `PREEMPT_LAZY`，同时开启 `PREEMPT_DYNAMIC` | `PREEMPT`（完全抢占） |
| 时钟频率 | `HZ=250` | `HZ=1000` |
| 调度器 | 内核自带调度器，没有第三方替换 | `SCHED_ALT` + `SCHED_PDS`（PDS 调度器） |
| 交互优先调整 | 没有 `ZEN_INTERACTIVE` | `ZEN_INTERACTIVE=y` |
| 默认拥塞控制 | `bbr`（`TCP_CONG_BBR=y`） | `bbr3`（没有启用名为 `bbr` 的那个） |
| 默认队列规则 | `NET_SCH_DEFAULT` 未设置，`fq` 等以模块提供 | `fq_codel` |

几点说明：

- XanMod 6.6 的配置是 `PREEMPT=y`（完全抢占）加 `HZ=250`，到 6.18 变成了 `PREEMPT_LAZY`。同样是 XanMod，不同版本差别不小。
- XanMod 6.18 配置里还有 `SCHED_CLASS_EXT=y`、`SCHED_AUTOGROUP` 默认开启、`LRU_GEN` 默认开启、`ZSWAP` 默认开启、`TRANSPARENT_HUGEPAGE_ALWAYS`。这些是我读到的开关，它们对实际体验的影响我没有测。
- Liquorix 默认拥塞控制名字叫 `bbr3`，不是 `bbr`。如果你装了 Liquorix 后用 `sysctl net.ipv4.tcp_congestion_control` 看到 `bbr3`，是正常的。XanMod 6.1、6.6 里 BBR v3 用的名字是 `bbr`，这点在 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/) 里提过。至于 XanMod 6.18 里 `bbr` 具体是哪个版本，我没有核对。
- Liquorix 默认队列规则是 `fq_codel`。前面写过的 [BBRplus要不要搭配FQ](https://vpsjq.com/2026/10/04/bbrplus-fq-qdisc/) 讲的是内核原版 BBR 注释推荐搭配 fq，对 `bbr3` 和 `fq_codel` 的搭配我没有读过源码，不下结论。

## Zen 内核：ZEN_INTERACTIVE 到底调了什么

我读了 `zen-kernel/zen-kernel` 7.2/main 分支的 `init/Kconfig`，里面有个 `ZEN_INTERACTIVE` 选项，默认就是 `y`，帮助文字的第一句是：

> Tunes the kernel for responsiveness at the cost of throughput and power usage.

意思是"为了响应速度，牺牲吞吐量和功耗"。后面列出的调整包括：

- 块设备调度器：单队列从 `mq-deadline` 改成 `bfq`，多队列从 `none` 改成 `kyber`；
- 虚拟内存：swap 预读从 3 改成 0 等；
- EEVDF 调度器的几个时间参数调小（最小粒度 0.7→0.4 ms、迁移开销 0.5→0.3 ms 等）；
- PDS/BMQ 调度器的时间片从 4 ms 改成 2 ms；
- CPU 频率调节器（ondemand）更积极地升频。

这些调整的目标是桌面端响应更快。对 VPS 来说，吞吐量和稳定性通常比点击一下的响应更重要，而且云主机的 CPU 频率、块设备调度是宿主机说了算，这些调整未必有机会生效，我没有验证。

另外，Zen 的仓库里除了 `main`，还有 `prjc`（PDS/BMQ 调度器补丁）、`zen-sauce`（零散补丁）、`bbr3` 等分支，说明它是"补丁集合"的形态。**直接装 Zen 一般是通过发行版打包好的软件包**（比如 Arch 的 linux-zen，Liquorix 也是一种），我没有逐个核对这些发行版软件包用的配置。

## CacULE 和 TT 调度器：为什么现在找不到了

很多关键词是"xanmod cacule"。我在 XanMod 的 GitLab 分支列表里看到：

- `5.9-cacule`、`5.10-cacule`、`5.11-cacule`、`5.12-cacule`、`5.13-cacule`、`5.14-cacule`：这六条独立分支；
- `5.15-tt`：一条用 TT 调度器的分支；
- 5.15 之后再没有 cacule 或 tt 分支，6.6 和 6.18 的配置里也没有 `CACULE_SCHED`、`TT_SCHED` 这两项。

我读了其中两条旧分支的配置：5.14-cacule 是 `CACULE_SCHED=y`、`PREEMPT_VOLUNTARY`、`HZ=500`、默认拥塞控制 `bbr2`；5.15-tt 是 `TT_SCHED=y`、`HZ=1000`、默认也是 `bbr2`。

所以：

- **XanMod 现在的版本没有 CacULE 可选**，这是个历史上的独立分支，不是新版 XanMod 里的开关；
- 老文章里说的"装 XanMod 选 cacule 版"，对应的是 5.14 及更早的内核，今天在新机器上装不到；
- CacULE 具体怎么调度，我没有读过它的源码，所以不对它做评价。

## 关于"XanMod 游戏"

XanMod 在游戏场景下的评价，我没有找到官方文档里有针对游戏的说明，也没有做过帧率或延迟的对比测试，所以不下结论。从配置能看到的客观事实只有上面那些：抢占模式、时钟频率、`SCHED_CLASS_EXT` 等开关。如果主要是桌面玩游戏，Liquorix 和 Zen 的官方定位更贴近这个场景；但这是看它们自述的取向，不是我测出来的。

## VPS 该选哪个

结合上面读到的：

1. **不想折腾、只是想要新内核**：换 XanMod 的 LTS 或 main 版本，见 [XanMod内核版本怎么选：edge、lts和普通版的区别](https://vpsjq.com/2026/08/28/xanmod-versions-choose/)。
2. **想开 BBR3**：XanMod 就有，见 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)。
3. **Zen 和 Liquorix**：官方自述是面向桌面交互，Zen 的帮助文字直接写了牺牲吞吐量和功耗，跑代理或网站没有明显理由选它们。
4. **x64v3 要看 CPU**：XanMod 6.18 的这份配置是 `X86_64_VERSION=3`（`LOCALVERSION="-x64v3"`），按 x86-64-v3 的定义这需要较新的 CPU 指令集（如 AVX2），旧 CPU 上要选 v1 或 v2 的包。我没有在本机运行过这些包，所以不确认各包具体对应哪个 CPU。

需要明确的是，我没有做过任何一个内核的速度对比。站内 [XanMod内核版本怎么选](https://vpsjq.com/2026/08/28/xanmod-versions-choose/) 里也说过，从 Debian 默认内核换到 XanMod 之后体感没有明显差别，线路质量对速度的影响通常比内核大。

## 想自己编译

官方源码在 GitLab，配置文件放在仓库的 `CONFIGS/` 目录下：6.18 分支的是 `CONFIGS/x86_64/config`，6.6 分支的是 `CONFIGS/xanmod/gcc/config_x86-64-v1`、`config_x86-64-v2`、`config_x86-64-v3` 三个文件，不同分支目录结构不一样。我只读了配置，没有实际编译过，具体编译步骤这里不写；一般 VPS 直接装官方软件包更省事。

## 装了不满意怎么回退

三个内核都是装在 `/boot` 里的额外内核，默认内核通常还在。回退步骤见 [装了XanMod内核出问题，怎么卸载切回默认内核](https://vpsjq.com/2026/08/27/xanmod-uninstall-rollback/)，装不上或启动黑屏见 [XanMod内核安装失败怎么办](https://vpsjq.com/2026/08/27/xanmod-install-fail/)。

## 常见问题

**XanMod 和 Zen 有什么区别？**
Zen 的 `ZEN_INTERACTIVE` 默认开启，自述牺牲吞吐量和功耗换响应速度；XanMod 官方配置没有这个选项。Zen 本身主要是源码和补丁，Liquorix 是基于它的发行版。

**XanMod 的 CacULE 还在吗？**
只存在于 5.9 到 5.14 的独立分支，之后没有；6.18 的官方配置里也没有。

**跑代理节点装哪个？**
我没有测过。按官方定位，Zen 和 Liquorix 偏桌面，XanMod 更常见于服务器和通用场景。

## 小结

- XanMod 是独立的一条线，Liquorix 基于 Zen 源码，Zen 是源码树。
- XanMod 的 GitHub 仓库停在 6.11，最新源码在 GitLab。
- Zen 的 `ZEN_INTERACTIVE` 默认开启，官方自述牺牲吞吐量和功耗换响应速度。
- Liquorix 默认 PDS 调度器、`HZ=1000`、拥塞控制名叫 `bbr3`、默认队列规则 `fq_codel`。
- CacULE、TT 调度器是 5.9–5.15 时期的 XanMod 独立分支，现在的版本里没有。
- 依据：GitLab `xanmod/linux`（6.6、6.18、5.14-cacule、5.15-tt 分支的配置文件）、GitHub `zen-kernel/zen-kernel` 7.2/main 的 `init/Kconfig`、GitHub `damentz/liquorix-package` 7.2/master 的 Debian 配置和 Fedora spec，读取时间 2026-10-07。没有运行过这些内核，没有做过性能测试；xanmod.org 和 liquorix.net 当时无法访问，所以官方网站上的安装说明没有核对。
