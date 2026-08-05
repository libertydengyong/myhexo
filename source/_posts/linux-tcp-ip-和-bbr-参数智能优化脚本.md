---
title: Linux TCP/IP 和 BBR 参数智能优化脚本
tags:
  - Linux TCP/IP 和 BBR 参数智能优化脚本
id: '181'
categories:
  - vps技巧
abbrlink: 2207
date: 2025-11-30 20:51:47
description: Linux服务器TCP/IP和BBR参数智能优化脚本的使用方法，包括BBR加速原理、一键脚本安装步骤和优化效果验证。
---

VPS用久了会发现，同样的带宽，有的服务器传文件、访问网站就是比别的快，很大一部分原因出在TCP/IP参数和拥塞控制算法上。默认配置一般比较保守，没有针对具体网络环境做调优，而BBR这类拥塞控制算法配合合理的TCP参数，能明显改善高延迟、丢包网络下的传输速度。

手动一项项调这些内核参数比较麻烦，还容易调错导致连接不稳定，所以直接用一键脚本智能优化更省事：

```bash
bash <(curl -sL https://raw.githubusercontent.com/yahuisme/network-optimization/main/script.sh)
```

来源：https://github.com/yahuisme/network-optimization

## 这个脚本做了什么

脚本会自动检测当前系统的内核版本和网络环境，调整这几类参数：

- **拥塞控制算法**：切换到BBR（如果内核版本支持）
- **TCP缓冲区大小**：根据服务器内存和带宽调大读写缓冲区，减少高延迟场景下的等待
- **队列规则（qdisc）**：搭配BBR一起调整，进一步降低延迟和丢包影响
- **其他内核网络参数**：比如连接队列长度、TIME_WAIT状态回收等，减少高并发场景下的连接瓶颈

不需要手动挨个改 `/etc/sysctl.conf`，脚本跑完会自动应用配置。

## 执行前建议确认的事

跑脚本之前，先确认一下内核版本，BBR从Linux 4.9开始才支持：

```bash
uname -r
```

如果内核版本太旧，脚本一般会提示需要先升级内核，或者自动引导安装支持BBR的内核（比如常见的XanMod内核）。

## 验证是否生效

脚本跑完，确认一下拥塞控制算法确实切换成了BBR：

```bash
sysctl net.ipv4.tcp_congestion_control
```

正常应该输出：

```
net.ipv4.tcp_congestion_control = bbr
```

再检查一下队列规则：

```bash
sysctl net.core.default_qdisc
```

## 优化后的实际效果

<img src="/images/bbr-before-after.svg" alt="开启BBR优化前后的网络传输速度对比示意图，优化后延迟明显降低吞吐量明显提升" width="700" height="380" loading="lazy">

对高延迟的海外VPS线路来说，开启BBR之后，文件下载速度和网页打开速度的提升通常是能直接感受到的，尤其是在原本网络质量一般、丢包率偏高的线路上效果更明显；如果服务器本身网络质量已经很好（比如本地IDC、低延迟专线），提升幅度会相对有限。

如果这台VPS平时是通过手机远程管理的，跑完这个脚本之后建议顺手测一下连接体验有没有改善，具体连接方式可以参考[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)。

## 和其他加速方式的选择

BBR不是唯一的加速手段，如果这台VPS对特定场景（比如游戏加速、专线中转）有更细分的需求，也可以看看[BBRplus与其他加速方式安装](https://vpsjq.com/2025/05/06/bbrplus%E4%B8%8E%E5%85%B6%E4%BB%96%E5%8A%A0%E9%80%9F%E6%96%B9%E5%BC%8F%E5%AE%89%E8%A3%85/)这篇里提到的几种方案，根据实际网络环境挑一个更贴合需求的组合。多数情况下，普通VPS用这个智能优化脚本跑一遍BBR就已经够用了，不需要叠加太多种加速方式，反而容易互相冲突。
