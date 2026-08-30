---
title: 安装BBR时内核headers未匹配的原因和解决方法
date: 2026-08-30 23:00:00
tags:
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: 安装BBR时出现内核headers未匹配报错的原因，通常是脚本依赖的下载链接失效，解决方法是换用其他可用的BBR脚本。
---

安装 BBR 相关脚本的时候，有时候会遇到内核 headers 未匹配的报错，提示找不到对应版本的 `linux-headers` 包，或者下载失败。这个问题不是你的系统有问题，也不是配置写错了，原因通常出在脚本依赖的下载链接上。

Linux 发行版官方或者托管站会定期清理旧版本的内核包，已经停止维护的旧内核 `linux-headers` 会被移除或者归档，原来的下载地址就失效了。BBR 安装脚本如果依赖这些旧地址，运行的时候就会找不到对应的包，报出 headers 未匹配或者版本不匹配的错误。这种情况在用时间比较久的脚本、或者系统版本比较旧的 VPS 上比较常见。

遇到这个问题最直接的解决方法是**换一个更新维护的 BBR 脚本**，不要继续用报错的那个。目前几个常用的脚本里，维护比较活跃、链接相对可靠的有：

adsorgcn 的 bbr-script，支持自动升级内核，适合内核版本不够新的情况，安装命令去 `https://github.com/adsorgcn/bbr-script` 找最新的。

byJoey 的 Actions-bbr-v3，专门针对 BBR3，从 GitHub Releases 下载匹配的内核包，链接维护比较及时，具体使用方法参考[BBR3一键安装脚本](https://vpsjq.com/2026/08/28/bbr3-install/)。

换脚本之前先确认一下当前系统的内核版本：

\`\`\`bash
uname -r
\`\`\`

再确认系统版本：

\`\`\`bash
cat /etc/os-release
\`\`\`

把这两个信息对照脚本的说明，选一个支持你当前系统的脚本来跑，避免又遇到同样的兼容性问题。如果换了脚本还是有问题，也可以考虑直接升级系统到新版本，新版本的内核包维护更活跃，headers 缺失的情况更少。

装完之后用这两条命令验证 BBR 有没有真正生效：

\`\`\`bash
lsmod | grep bbr
sysctl net.ipv4.tcp_congestion_control
\`\`\`

如果验证结果正常但感觉速度没有提升，原因分析参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)。
