---
title: OpenWrt怎么开BBR加速：kmod-tcp-bbr怎么装，什么情况下有用
date: 2026-10-04 14:00:00
tags:
  - BBR加速
  - OpenWrt
  - Linux网络优化
categories:
  - Linux优化
description: OpenWrt里BBR是一个内核模块包kmod-tcp-bbr。依据OpenWrt源码里的包定义，讲清楚怎么安装、怎么确认生效，以及路由器上开BBR到底对哪些流量有用。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "OpenWrt怎么开BBR加速：kmod-tcp-bbr怎么装，什么情况下有用",
      "description": "OpenWrt里BBR是一个内核模块包kmod-tcp-bbr。依据OpenWrt源码里的包定义，讲清楚怎么安装、怎么确认生效，以及路由器上开BBR到底对哪些流量有用。",
      "datePublished": "2026-10-04T14:00:00+08:00",
      "dateModified": "2026-10-04T14:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/openwrt-enable-bbr/",
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
          "name": "OpenWrt怎么开启BBR？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "安装内核模块包kmod-tcp-bbr即可，OpenWrt源码里这个包会安装/etc/sysctl.d/12-tcp-bbr.conf，内容是net.ipv4.tcp_congestion_control=bbr。装完后用sysctl net.ipv4.tcp_congestion_control确认输出为bbr；包管理器命令依固件版本是opkg还是apk而不同。"
          }
        },
        {
          "@type": "Question",
          "name": "OpenWrt开BBR需要fq吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "kmod-tcp-bbr包的说明写着BBR需要fq pacing调度器，内核4.13及以上有TCP内部pacing作为回退。fq模块在kmod-sched这个额外调度器包里。它写入的sysctl文件只设置拥塞控制算法，没有设置队列规则。"
          }
        },
        {
          "@type": "Question",
          "name": "路由器开了BBR，局域网设备上网会变快吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按TCP的工作原理，拥塞控制只作用在TCP连接的两端。路由器只是转发局域网设备的流量时，TCP连接两端是设备和远端服务器，路由器上的BBR不起作用；只有路由器自己作为一端的连接（比如路由器上运行的代理程序、自身下载）才会用到。我没有实测。"
          }
        }
      ]
    }
  ]
}
</script>

在 OpenWrt 上想开 BBR，和 VPS 上不太一样：没有"一键脚本"这回事，BBR 是以内核模块包的形式提供的，装上再确认就行。这篇依据 OpenWrt 源码里的包定义，把流程和一个常被忽略的问题（开了 BBR 到底对哪些流量有用）讲清楚。

先说明：下面的包定义来自 [openwrt/openwrt](https://github.com/openwrt/openwrt) 仓库的 `package/kernel/linux/modules/netsupport.mk`。OpenWrt 官网文档在我这里访问不了，所以包管理器的具体命令、各版本的差异我没有核对，也没有在路由器上实测，凡是没核对的地方都会注明。

<!-- more -->

## OpenWrt 里 BBR 是什么

OpenWrt 把内核里的 BBR 做成了一个独立的内核模块包，源码里的定义是：

- 包名：`kmod-tcp-bbr`，标题 "BBR TCP congestion control"；
- 对应内核配置 `CONFIG_TCP_CONG_BBR`，模块文件 `tcp_bbr.ko`，开机自动探测加载（`AutoProbe,tcp_bbr`）；
- 安装时会放一个配置文件 `/etc/sysctl.d/12-tcp-bbr.conf`，我读到的内容是：

```
# Do not edit, changes to this file will be lost on upgrades
# /etc/sysctl.conf can be used to customize sysctl settings

net.ipv4.tcp_congestion_control=bbr
```

这个文件开头注释说明了两点：不要直接改它（升级会丢），要自定义就写在 `/etc/sysctl.conf` 里。

## 包说明里提到的 fq

`kmod-tcp-bbr` 的描述写着：BBR 需要 fq（Fair Queue）pacing 数据包调度器；内核 4.13 及以上，TCP 内部 pacing 会作为回退。这和内核 `tcp_bbr.c` 注释的说法一致（详见 [BBRplus要不要搭配FQ](https://vpsjq.com/2026/10/04/bbrplus-fq-qdisc/)）：配 fq 是推荐的，不配不会直接失效。

要注意两点：

- `12-tcp-bbr.conf` 里**只设置了拥塞控制算法**，没有设置 `net.core.default_qdisc`；
- `sch_fq` 模块在 OpenWrt 里属于另一个包 `kmod-sched`（"Extra traffic schedulers"，源码里的额外调度器列表包含 `sch_fq`），不在 `kmod-tcp-bbr` 里。cake 和 fq_pie 则是各自独立的包 `kmod-sched-cake`、`kmod-sched-fq-pie`。

所以想搭配 fq，需要另外装 `kmod-sched`，再自己在 `/etc/sysctl.conf` 里加一行 `net.core.default_qdisc=fq`。是否值得这么折腾，我没有测过。

## 安装步骤

我只能给出基于包名的步骤，命令没有在路由器上跑过。

先看内核里是不是已经有 BBR（有些固件已经内置，或者装过）：

```bash
sysctl net.ipv4.tcp_available_congestion_control
```

列表里已经有 `bbr`，就不用装模块了，只需要确认当前使用的算法（见下面验证部分）。

没有的话，安装 `kmod-tcp-bbr`。OpenWrt 的包管理器随版本不同，旧版本用 `opkg`，较新的版本可能是 `apk`（我没有核对哪个版本用哪个，以你固件里实际有的命令为准）：

```bash
# opkg 版本
opkg update
opkg install kmod-tcp-bbr

# apk 版本
apk update
apk add kmod-tcp-bbr
```

注意：内核模块包必须和路由器**正在运行的内核**完全匹配，这是 OpenWrt 内核模块的通用约束（我没有在源码里单独核对）。如果是自己编译的固件、第三方固件，或者固件版本和软件源对不上，可能装不上，甚至装上了也加载不了。这种情况要么换成和固件匹配的软件源，要么在编译固件时把 `CONFIG_TCP_CONG_BBR` 对应的 `kmod-tcp-bbr` 选上。

## 怎么确认生效

```bash
sysctl net.ipv4.tcp_congestion_control
sysctl net.ipv4.tcp_available_congestion_control
lsmod | grep bbr
```

- 第一条输出 `bbr`，说明当前使用的是 BBR；
- 第二条列表里有 `bbr`，说明内核支持；
- 第三条能看到 `tcp_bbr`，说明模块已经加载。

如果刚装完输出还是 `cubic`，可以先重启路由器再看，因为配置文件是开机时由 sysctl 载入的。重启后仍然不是 `bbr`，多半是模块没加载成功，排查思路和 VPS 上相同，见 [已安装BBR加速内核但加速模块未加载的解决方法](https://vpsjq.com/2026/08/30/bbr-module-not-loaded/)。

## 路由器开了 BBR，到底对谁有用

这一点最容易被误解。TCP 拥塞控制是 **TCP 连接两端**各自使用的算法：

- 局域网里的手机、电脑访问外网，TCP 连接的两端是"设备"和"远端服务器"，路由器只负责转发。这种流量由设备自己的系统和远端服务器的算法决定发送速度，**路由器上开 BBR 不起作用**；
- 只有**路由器自己作为一端**的连接才会用到路由器上的算法，比如路由器上运行的代理程序（连接到上游节点的那段）、路由器自身的下载、SSH、DDNS 请求等。

这是按 TCP 的工作原理推出来的，我没有实测。所以如果你想改善的是"局域网设备上网速度"，光在路由器上开 BBR 效果有限；如果路由器上跑着代理客户端，它到上游服务器的那段连接就会受益，另一端的服务器同样需要开 BBR，才是两头都生效。服务器端怎么开，可以看 [Debian和Ubuntu开启BBR加速的两种方式](https://vpsjq.com/2026/08/28/debian-ubuntu-bbr/)，或者 [x-ui、3x-ui和Xray怎么开BBR](https://vpsjq.com/2026/10/04/xui-xray-enable-bbr/)。

## 小结

- OpenWrt 的 BBR 是内核模块包 `kmod-tcp-bbr`，装上后会放一个 sysctl 配置，把拥塞控制设成 `bbr`；
- fq 在另一个包 `kmod-sched` 里，需要自己装、自己在 `/etc/sysctl.conf` 里设置 `default_qdisc`；
- 先用 `sysctl net.ipv4.tcp_available_congestion_control` 看内核是不是已经带 BBR；
- 路由器上的 BBR 只对路由器自己发起或终结的 TCP 连接有用，不影响局域网设备经路由器转发的流量。
