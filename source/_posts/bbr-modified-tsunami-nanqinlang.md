---
title: BBR魔改版是什么：tsunami、暴力BBR怎么识别，值不值得装
date: 2026-10-04 10:00:00
tags:
  - BBR加速
  - 魔改BBR
  - Linux网络优化
categories:
  - Linux优化
description: 脚本里说的BBR魔改版和暴力BBR，对应内核里的tsunami和nanqinlang两个拥塞控制模块。依据Linux-NetSpeed的tcpx.sh源码，讲清怎么识别、怎么验证，以及为什么日常VPS不建议装。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBR魔改版是什么：tsunami、暴力BBR怎么识别，值不值得装",
      "description": "脚本里说的BBR魔改版和暴力BBR，对应内核里的tsunami和nanqinlang两个拥塞控制模块。依据Linux-NetSpeed的tcpx.sh源码，讲清怎么识别、怎么验证，以及为什么日常VPS不建议装。",
      "datePublished": "2026-10-04T10:00:00+08:00",
      "dateModified": "2026-10-04T10:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/bbr-modified-tsunami-nanqinlang/",
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
          "name": "BBR魔改版和暴力BBR在系统里是什么名字？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在Linux-NetSpeed的tcpx.sh里，BBR魔改版对应net.ipv4.tcp_congestion_control的值tsunami（模块tcp_tsunami），暴力BBR魔改版对应nanqinlang（模块tcp_nanqinlang）。脚本靠这个值加上lsmod里是否有对应模块来判断启动成功还是失败。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么确认自己的服务器跑的是不是魔改BBR？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "执行sysctl net.ipv4.tcp_congestion_control，输出为bbr说明是内核自带的BBR，输出为bbrplus是BBRplus，输出为tsunami或nanqinlang才是魔改版，再用lsmod确认对应模块有没有加载。"
          }
        },
        {
          "@type": "Question",
          "name": "日常VPS要不要装魔改BBR？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不建议。魔改模块依赖对应内核版本编译，换内核后容易加载失败，而主线内核自带的BBR或XanMod的BBR3已经够用；我读到的tcpx.sh当前菜单里也不再提供这两种的安装项。"
          }
        }
      ]
    }
  ]
}
</script>

搜BBR加速，经常看到"BBR魔改版""暴力BBR"这些名字，跟BBRplus放在一起，看着像是更强的版本。这篇不推荐也不吹，只把能从脚本源码里核对到的事实讲清楚：它们在系统里到底叫什么、怎么确认自己有没有装、为什么日常VPS没必要碰。

先说明依据：下面的内容来自 [ylx2016/Linux-NetSpeed](https://github.com/ylx2016/Linux-NetSpeed) 的 `tcpx.sh` 源码。我没有在机器上装过魔改BBR，也没有读过 tsunami、nanqinlang 两个模块本身的源码，所以"它们的算法具体怎么改的"这部分不展开，没核对的地方都会注明。

<!-- more -->

## 魔改BBR在系统里叫什么

`tcpx.sh` 里有一段判断当前加速状态的代码，它读取 `net.ipv4.tcp_congestion_control` 的值，按下面的对应关系给出状态：

| `tcp_congestion_control` 的值 | 脚本显示的状态 |
| --- | --- |
| `bbr` | BBR启动成功 |
| `bbr2` | BBR2启动成功 |
| `tsunami` | BBR魔改版（要求 `lsmod` 里有 `tcp_tsunami` 模块，否则显示"启动失败"） |
| `nanqinlang` | 暴力BBR魔改版（要求 `lsmod` 里有 `tcp_nanqinlang` 模块，否则显示"启动失败"） |
| `bbrplus`（在BBRplus内核上） | BBRplus启动成功 |

也就是说，所谓"BBR魔改版"就是内核里名叫 `tsunami` 的拥塞控制模块，"暴力BBR"就是名叫 `nanqinlang` 的模块。它们和 BBRplus 一样，都是第三方在BBR基础上改出来的，以模块形式加载；和内核自带的 `bbr` 是不同的算法名。

## 怎么确认自己用的是哪一种

不用跑任何脚本，三条命令就能看出来：

```bash
sysctl net.ipv4.tcp_congestion_control
sysctl net.ipv4.tcp_available_congestion_control
lsmod | grep -E 'bbr|tsunami|nanqinlang'
```

- 第一条输出 `bbr`：用的是内核自带的BBR，不是魔改版。
- 输出 `bbrplus`：BBRplus，见[BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)。
- 输出 `tsunami` 或 `nanqinlang`：才是魔改版。
- 第二条列出的是当前内核"能用"的算法；某个算法没在列表里，就没法选它。

如果你是用别人的一键脚本装过东西，现在想知道机器到底跑的什么，看第一条命令的输出最直接。

## 现在的脚本还装魔改版吗

我读到的 `tcpx.sh` 当前菜单里，内核安装项只有自编BBR内核、BBRplus内核、BBRplus新版内核、锐速、官方内核、XanMod、Zen 这些，加速启用项是 BBR+FQ、BBR+FQ_PIE、BBR+CAKE、BBRplus+FQ、锐速等，**没有看到 tsunami 或 nanqinlang 的安装入口**；它们只出现在上面那段"状态识别"里，用来兼容以前装过魔改版的机器。

所以如果在别的文章里看到"选菜单里的魔改BBR"，要留意那是旧版本脚本。比如[常用VPS TCP加速脚本汇总](https://vpsjq.com/2026/08/29/vps-tcp-scripts/)里提到的 zeruns/tcp.sh，是把BBRplus、魔改版、暴力BBR放进同一个菜单的五合一脚本，用之前要先看清它当前版本的菜单。

## 日常VPS为什么不建议装

下面几点里，第一点来自脚本源码，后面是我的判断，没有实测：

1. **依赖特定内核**：脚本是先判断内核类型，再判断模块是否加载，模块没加载就直接报"启动失败"。换了内核、升级了内核而模块没跟着装，加速就失效，系统回退到默认算法。
2. **收益说不清**：[BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)里讲过，各版本差别没有宣传的那么大。主线内核自带的BBR、XanMod 的 BBR3 已经够用，没必要为了几个百分点的传闻去装来路更杂的模块。
3. **"暴力"意味着更激进**：按名字和社区的说法，这类版本会更主动地占用带宽。我没有读过源码，不下结论，但在共享带宽的机器上，激进发包有可能引来对方机房的限速或被判定为滥用，这一点属于推测。

另外 [Linux VPS 一键优化 TCP 网络性能与 BBR 加速脚本](https://vpsjq.com/2025/05/14/一键优化tcp/)里也建议：生产环境优先用官方内核提供的BBR，兼容性和稳定性更有保障。

## 已经装了魔改版，怎么换回去

先确认当前算法，再切回内核自带的BBR（内核够新、`tcp_available_congestion_control` 里有 `bbr` 才行）：

```bash
sysctl net.ipv4.tcp_available_congestion_control
```

确认列表里有 `bbr` 之后，把 `/etc/sysctl.conf` 里相关两行改成：

```
net.core.default_qdisc=fq
net.ipv4.tcp_congestion_control=bbr
```

再执行 `sysctl -p`，用 `sysctl net.ipv4.tcp_congestion_control` 确认输出是 `bbr`。如果列表里没有 `bbr`，说明当前内核不带BBR模块，可参考[已安装BBR加速内核但加速模块未加载的解决方法](https://vpsjq.com/2026/08/30/bbr-module-not-loaded/)。想用更新的BBR3，看 [XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)。

## 小结

- BBR魔改版 = `tsunami`，暴力BBR = `nanqinlang`，都是第三方算法模块，和内核自带的 `bbr` 不是同一个东西。
- 想知道自己跑的是哪个，看 `sysctl net.ipv4.tcp_congestion_control` 的输出。
- 日常VPS用内核自带BBR或XanMod的BBR3就行，不必专门去找魔改版。
