---
title: CentOS、Rocky、AlmaLinux能装XanMod内核吗：官方只有APT，第三方Copr的现状
date: 2026-10-08 16:00:00
tags:
  - XanMod内核
  - CentOS
  - Linux内核
categories:
  - Linux优化
description: XanMod官方只提供Debian和Ubuntu的APT仓库，CentOS、Rocky、AlmaLinux没有官方RPM。依据XanMod官方GitLab和第三方Copr仓库的源码，说明现状、风险，以及没法核实的部分。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "CentOS、Rocky、AlmaLinux能装XanMod内核吗：官方只有APT，第三方Copr的现状",
      "description": "XanMod官方只提供Debian和Ubuntu的APT仓库，CentOS、Rocky、AlmaLinux没有官方RPM。依据XanMod官方GitLab和第三方Copr仓库的源码，说明现状、风险，以及没法核实的部分。",
      "datePublished": "2026-10-08T16:00:00+08:00",
      "dateModified": "2026-10-08T16:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/08/xanmod-centos-rocky-alma/",
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
          "name": "CentOS能装XanMod内核吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "XanMod官方只提供Debian和Ubuntu的APT仓库，官方GitLab上也没有RPM打包相关的项目，所以没有官方支持的装法。网上能搜到的是第三方在Fedora Copr上打的包，我没能核实它们现在是否还支持CentOS、Rocky、AlmaLinux。"
          }
        },
        {
          "@type": "Question",
          "name": "xanmod的copr仓库能用在Rocky和AlmaLinux上吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "有一个我读过源码的Copr仓库（cache8749/xanmod-copr）明确是只给Fedora用的，不适用于Rocky和AlmaLinux。另一个更老的rmnscnce/kernel-xanmod据搜索结果曾提供EPEL构建，但它现在是否还在更新、是否支持EL9以上，我没能核实。"
          }
        },
        {
          "@type": "Question",
          "name": "为什么不建议在生产VPS上用第三方内核包？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "换内核装错了会导致重启后连不上服务器，而第三方打包不是发行版官方维护，更新是否持续、有没有签名和安全补丁都要自己判断。需要内核更新的话优先看发行版自带内核的更新通道。"
          }
        }
      ]
    }
  ]
}
</script>

很多人会搜"xanmod 内核 centos""xanmod 内核 rocky"，想知道 CentOS 系的 VPS 能不能换 XanMod。这篇先给结论，再说我查了什么、哪些没能核实。

结论：**XanMod 官方没有给 CentOS、Rocky、AlmaLinux 提供 RPM 包，没有官方支持的装法**。网上能找到的是第三方打包，我读到的一个明确只给 Fedora，另一个的现状没能核实，所以这篇不写安装步骤。

<!-- more -->

## 官方只有 APT

XanMod 官方的安装方式是 APT 仓库，面向 Debian 和 Ubuntu，站内的安装教程也是这个路线，见 [一键更换为XanMod内核](https://vpsjq.com/2025/05/07/一键更换为xanmod内核/) 和 [XanMod内核版本怎么选](https://vpsjq.com/2026/08/28/xanmod-versions-choose/)。

我核对的证据：

- 官方源码在 GitLab 的 `xanmod/linux`，这个组下面只有 `linux` 和 `linux-patches` 两个项目，没有任何 RPM 打包相关的仓库；
- `xanmod/linux` 根目录里有 `CONFIGS` 目录存放内核配置，没有 `.spec` 文件；
- 搜索近期的 XanMod 发布报道，说的都是"Debian 和 Ubuntu 可用"。

要说明的是：xanmod.org 官网在我的环境里打不开，所以"官网没有 RPM"这个结论是从上面三点推出来的，不是在官网页面上直接读到的。

## 第三方 Copr：一个只给 Fedora，另一个没法核实

RPM 系统上能装到 XanMod，靠的是第三方在 Fedora Copr 上打的包。我看到两个：

**cache8749/xanmod-copr**（我读了它的 GitHub 仓库）

- README 标题是"XanMod for Fedora"，构建时同步 Fedora 的内核打包，只会选 Fedora 的 `fNN` 分支，我看到的最近一次构建是 2026-10-04 的 `7.2.9-xanmod1`，对应 Fedora f45；
- 它用 XanMod 官方 `CONFIGS/x86_64/config` 里的 x86-64-v3 配置构建，README 明确写了"需要支持 v3 的 CPU，这是有意为之"；
- 它的 spec 里还特意保留 Fedora 的 SELinux 默认设置，说明是为 Fedora 调的。

所以它**不是**给 CentOS、Rocky、AlmaLinux 用的，别把它的 `dnf copr enable` 命令照搬到这些系统上。

**rmnscnce/kernel-xanmod**（只看到搜索结果，没读到仓库）

- 搜索结果显示它提供过 `kernel-xanmod-lts`、`kernel-xanmod-edge`、`kernel-xanmod-rt` 等包，也有人写过在 Rocky 8、AlmaLinux 8 上装的教程；
- 这些教程提到的 `cacule`、`tt` 变体，在新版 XanMod 里已经没有了（见 [XanMod、Zen、Liquorix内核怎么选](https://vpsjq.com/2026/10/08/xanmod-zen-liquorix-compare/)），说明资料已经过时；
- 它现在是否还在更新、是否支持 EL9 或更新的版本，我没能核实：Copr、Fedora 讨论区和这些教程网站在我的环境里都访问不了；它在 GitHub 上的同名仓库我也没能打开。

所以我对这个仓库**没有结论**，既不能说它还能用，也不能说它不能用。

## 为什么我不写安装步骤

两个原因：

1. 上面这个能装的第三方源，我没法核实现状，照着旧教程写出来的命令，读者装上去可能直接失败；
2. 换内核是有风险的操作。装错了或者引导没切换成功，重启后可能连不上服务器，处理思路见 [装BBRplus重启后连不上服务器怎么办](https://vpsjq.com/2026/09/06/bbrplus-reboot-connection-lost/)，这类问题在 CentOS 系的 VPS 上同样会碰到，而且要靠面板的 VNC 或救援模式才能处理。

第三方打包也不是发行版官方维护的：有没有持续更新、有没有签名、安全补丁跟不跟得上，都要自己判断。

## 如果你想要的其实是 BBR

很多人想装 XanMod，真正的目的是开 BBR。这件事不一定要换内核：

- 开 BBR 只需要内核支持 BBR 模块并改两项 sysctl 设置，原理见 [BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)；
- 我没有在本机核对过各个版本的 CentOS、Rocky、AlmaLinux 默认内核是否带 BBR，开之前建议先用 `sysctl net.ipv4.tcp_available_congestion_control` 看有没有 `bbr`，没有再考虑别的办法；
- 如果你的服务器是 Debian 或 Ubuntu，想用 XanMod 就直接用官方 APT 仓库，不用折腾第三方源。

## 小结

- XanMod 官方只提供 Debian 和 Ubuntu 的 APT 仓库，官方 GitLab 里没有 RPM 打包。
- 我读到的 `cache8749/xanmod-copr` 明确只给 Fedora，不适用于 CentOS、Rocky、AlmaLinux。
- `rmnscnce/kernel-xanmod` 曾提供 EPEL 构建，但现状没能核实，网上相关教程已经过时（里面的 cacule、tt 变体已不存在）。
- 在生产 VPS 上，不建议为了"新内核"去装没法确认来源和更新状态的第三方内核包。
- 依据：GitLab `xanmod/linux` 和 `cache8749/xanmod-copr` 的仓库内容，读取时间 2026-10-07；搜索结果仅用于了解 `rmnscnce` 仓库。没有在 CentOS、Rocky、AlmaLinux 上实际安装过 XanMod；xanmod.org、Copr、Fedora 讨论区、LinuxCapable、ELRepo 在我的环境里都无法访问。
