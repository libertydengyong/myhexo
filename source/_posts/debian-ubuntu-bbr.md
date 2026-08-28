---
title: Debian和Ubuntu开启BBR加速的两种方式
date: 2026-08-28 18:00:00
tags:
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: Debian和Ubuntu系统开启BBR的两种方式：手动修改sysctl配置和用adsorgcn的bbr-script一键脚本，附验证命令。
---

Debian 和 Ubuntu 是 VPS 上最常见的两个系统，开启 BBR 的方式比较简单，内核版本够新的话不需要换内核，直接改几行配置就能生效。主要有两种方式：手动修改系统配置，或者用一键脚本自动处理。

手动方式适合想了解具体配置的情况。先确认内核版本够不够，BBR 从 Linux 4.9 开始支持：

\`\`\`bash
uname -r
\`\`\`

内核版本在 4.9 以上就可以继续。把下面两行加到 `/etc/sysctl.conf` 里：

\`\`\`bash
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
\`\`\`

然后让配置生效：

\`\`\`bash
sysctl -p
\`\`\`

改完之后建议重启服务器，确保配置在重启后也能持久生效。

如果不想手动操作，用 adsorgcn 维护的 bbr-script 一键脚本更省事，脚本支持自动升级内核，适合内核版本不够新的情况。安装命令去 GitHub 仓库找最新的：`https://github.com/adsorgcn/bbr-script`，README 里有当前维护的命令，直接复制跑就行。脚本会自动检测系统环境，判断内核是否需要升级，升级完成后同样需要重启才能切换到新内核。

不管用哪种方式，开启之后验证一下有没有真正生效：

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

输出 `bbr` 说明拥塞控制算法已经切换成功。再检查一下队列规则：

\`\`\`bash
sysctl net.core.default_qdisc
\`\`\`

输出 `fq` 或者 `fq_codel` 说明配置完整。如果验证结果不对，先确认重启之后配置有没有持久化，有时候 `sysctl -p` 当时生效了但重启后又恢复默认，检查一下 `/etc/sysctl.conf` 里两行有没有正确写入。

开启 BBR 之后如果感觉速度提升不明显，不一定是配置有问题，更多时候是线路本身的限制，具体原因可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)。如果想进一步优化，可以结合[Linux TCP/IP和BBR参数智能优化脚本](https://vpsjq.com/2025/11/30/linux-tcp-ip-%E5%92%8C-bbr-%E5%8F%82%E6%95%B0%E6%99%BA%E8%83%BD%E4%BC%98%E5%8C%96%E8%84%9A%E6%9C%AC/)一起跑，把TCP参数也一并调优。
