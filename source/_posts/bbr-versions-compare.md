---
title: BBR、BBR2、BBRplus、BBR3有什么区别
date: 2026-08-28 14:00:00
updated: 2026-10-08 20:00:00
tags:
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: BBR各版本实际区别没有网上说的那么大，日常VPS用原版BBR、BBRplus或者BBR3就够了，选哪个更多取决于系统环境而不是版本本身。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBR、BBR2、BBRplus、BBR3有什么区别",
      "description": "BBR各版本实际区别没有网上说的那么大，日常VPS用原版BBR、BBRplus或者BBR3就够了，选哪个更多取决于系统环境而不是版本本身。",
      "datePublished": "2026-08-28T14:00:00+08:00",
      "dateModified": "2026-10-08T20:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/28/bbr-versions-compare/",
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
          "name": "BBR是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "BBR（Bottleneck Bandwidth and Round-trip propagation time）是Google在2016年开发的一种TCP拥塞控制算法，会持续估算网络链路真实的带宽上限和往返时间，让发送速率尽量贴着这个上限走，而不是像传统Cubic算法那样看到丢包就大幅减速。"
          }
        },
        {
          "@type": "Question",
          "name": "原版BBR、BBR2、BBRplus、BBR3各自有什么特点？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "原版BBR从Linux 4.9进入主线内核，主流发行版直接可用；BBR2优化了带宽估算精度但一直没合并进主线内核，折腾成本高收益有限；BBRplus是第三方修改版，代码上加了排空、周期随机等改动，作者自己说是实验性、不保证更快；BBR3是Google的新版本，XanMod官方6.6和6.18分支里算法名叫bbr的那个就是v3。"
          }
        },
        {
          "@type": "Question",
          "name": "日常VPS该选哪个版本？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "原版BBR、BBRplus、BBR3三个选一个就够了：内核够新直接开原版BBR最省事；想试第三方改版可以用BBRplus（作者说是实验性，需要换内核）；已装XanMod内核直接用它自带的BBR3。这几个版本不需要叠加安装，混着装容易冲突，BBR2不太推荐普通用户折腾。"
          }
        }
      ]
    }
  ]
}
</script>

BBR是什么？BBR（Bottleneck Bandwidth and Round-trip propagation time）是 Google 在 2016 年开发的一种 TCP 拥塞控制算法，用来解决传统算法在高延迟、高丢包网络下带宽利用率低的问题。简单说，BBR 会持续估算这条网络链路真实的带宽上限和往返时间，让发送速率尽量贴着这个上限走，而不是像传统 Cubic 算法那样看到丢包就本能地大幅减速。对于海外 VPS 这类高延迟线路，BBR 能帮助更充分地利用可用带宽，减少因为误判丢包而造成的速度损失。

网上一搜BBR相关的内容，各种版本的名字让人眼花缭乱：BBR、BBR2、BBRplus、BBR3、魔改BBR、锐速……标题动不动就是"最强加速"，好像不装最新版就亏了很多。实际用下来，这几个版本之间的差距没有宣传的那么大，日常VPS选哪个更多取决于你的系统和内核环境，不是版本越新越好。

原版BBR是Google推出的拥塞控制算法，从Linux 4.9开始进入主线内核，现在主流发行版基本都可以直接开启，不需要换内核。原理是持续估算链路的真实带宽上限，尽量把发送速率贴着这个上限走，而不是像传统Cubic算法那样看到丢包就大幅减速。为什么有时候开了BBR感觉没什么变化，可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，搞清楚原理之后对效果的期待会更准确。

BBR2 是 Google 在原版基础上改进的版本，主要优化了带宽估算的精度和对网络变化的响应速度，理论上在复杂网络环境下表现更稳定。但 BBR2 一直没有合并进 Linux 主线内核，需要单独打补丁或者用特定内核才能用，普通 VPS 上折腾起来比较麻烦，实际提升跟原版 BBR 差距不大，性价比不高。

BBRplus 是第三方在 BBR 基础上修改的版本，代码上和原版有几处不同（ACK 聚合窗口、排空策略、周期长度带随机成分等），作者自己说是实验性修改，不保证更快，我也没有测过它和原版的速度对比。来历和代码差异见[BBRplus是什么](https://vpsjq.com/2026/10/07/bbrplus-what-is/)。安装方式可以参考[BBRplus与其他加速方式安装](https://vpsjq.com/2025/05/06/bbrplus%E4%B8%8E%E5%85%B6%E4%BB%96%E5%8A%A0%E9%80%9F%E6%96%B9%E5%BC%8F%E5%AE%89%E8%A3%85/)，用一键脚本装比手动配置省事。

BBR3 是 Google 的 BBR 新版本。我读了 XanMod 官方 GitLab 的源码，6.6 和 6.18 分支里的 `tcp_bbr.c` 就是 v3（文件里有 `BBR_VERSION 3`），算法名仍叫 `bbr`，内核默认就是它；5.15 分支则不是 v3。装好 XanMod 之后不需要额外配置就能用（XanMod本身的安装方法参考[一键更换为XanMod内核](https://vpsjq.com/2025/05/07/一键更换为xanmod内核/)，这篇只对比BBR各版本，不是XanMod的完整教程）。BBR3 在算法上加了对丢包和 ECN 的响应、带宽和在途数据的上下界，具体对比见[XanMod和BBRplus怎么选](https://vpsjq.com/2026/10/08/xanmod-vs-bbrplus/)。至于实际速度比原版快多少，我没有测过，不下结论。

日常 VPS 使用，原版 BBR、BBRplus、BBR3 这三个选一个就够了。系统内核够新的话直接开原版 BBR 最省事；想试第三方改版可以用 BBRplus（作者说是实验性，需要换内核）；如果已经装了 XanMod 内核，它自带的 BBR3 直接用就行，不需要再叠加其他版本。BBR2 折腾成本高、收益有限，不太推荐普通用户去搞。几个版本不需要叠加安装，选一个用就够了，混着装反而容易冲突。
