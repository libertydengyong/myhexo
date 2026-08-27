---
title: XanMod内核搭配BBR3使用教程
date: 2026-08-27 14:00:00
tags:
  - XanMod内核
  - BBR3
categories:
  - Linux优化
description: XanMod内核安装后开启BBR3的完整流程，包括版本选择、安装后内核验证和BBR3启用方法。
---

XanMod 内核内置了 BBR3 支持，装好之后理论上不需要额外操作就能用，但实际情况是安装完重启后有时候内核没有切换过去，还在跑原来的系统内核，这时候 BBR3 自然也没有生效。所以安装完之后先确认内核有没有真的切换，再去看 BBR3 的状态，顺序不能反。

在装 XanMod 之前，先确认你的 VPS 虚拟化方案支不支持自定义内核。KVM 架构的 VPS 一般没有问题，OpenVZ 的 VPS 通常不允许更换内核，装了也没用甚至会出问题。不确定自己 VPS 是什么架构的话，跑一下这条命令：

\`\`\`bash
systemd-detect-virt
\`\`\`

输出 `kvm` 或者 `none` 的话可以继续，输出 `openvz` 或者 `lxc` 的话就不适合装 XanMod。

XanMod 有几个不同的版本，常见的有 `linux-xanmod`、`linux-xanmod-edge` 和 `linux-xanmod-lts`。edge 版本用的是最新的内核，功能最新但稳定性相对差一点；lts 版本基于长期支持内核，稳定性更好，适合长期运行的服务器；普通版在两者之间。如果 VPS 主要跑代理节点或者网站，lts 版本是比较稳妥的选择，edge 版本适合想尝鲜或者对特定新特性有需求的情况。

安装完成后重启服务器，重启之后先确认内核有没有切换过去：

\`\`\`bash
uname -r
\`\`\`

输出里应该能看到 `xanmod` 字样，比如 `6.x.x-xanmod1` 这种格式。如果输出还是原来的系统内核版本，说明引导程序没有切换到 XanMod，需要手动设置默认启动内核。用 `grub-set-default` 或者直接编辑 `/etc/default/grub` 把默认内核改成 XanMod 那一条，改完跑一下 `update-grub` 再重启。

内核确认切换之后，看一下 BBR3 有没有自动生效：

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

输出 `net.ipv4.tcp_congestion_control = bbr` 说明 BBR 已经在跑了。XanMod 装好后 BBR 通常会自动启用，但不一定是 BBR3，取决于内核版本。确认是不是 BBR3 可以用这条命令：

\`\`\`bash
sysctl net.ipv4.tcp_available_congestion_control
\`\`\`

如果输出里有 `bbr` 并且内核版本在 6.x 以上，跑的基本就是 BBR3。如果 BBR 没有自动启用，手动开启：

\`\`\`bash
echo "net.ipv4.tcp_congestion_control = bbr" >> /etc/sysctl.conf
echo "net.core.default_qdisc = fq" >> /etc/sysctl.conf
sysctl -p
\`\`\`

跑完再用 `sysctl net.ipv4.tcp_congestion_control` 确认一下，输出 `bbr` 就说明生效了。

XanMod 搭配 BBR3 的组合在代理节点服务器上用得比较多，跟[XanMod内核从性能优化到实际使用](https://vpsjq.com/2026/07/28/2026-07-28-002/)里提到的适用场景一致，如果同时跑着 3x-ui 或者 S-UI 这类面板，BBR3 对多连接场景下的网络吞吐有一定帮助，实际效果还是要看线路本身的质量。更多 VPS 网络优化的思路可以参考[一键cat命令完成vps所有优化](https://vpsjq.com/2026/04/17/2026-04-17-006/)。
