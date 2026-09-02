---
title: BBR3一键安装脚本：byJoey Actions-bbr-v3 GitHub安装教程
date: 2026-08-28 16:00:00
tags:
  - BBR3
  - BBR加速
categories:
  - Linux优化
description: 用byJoey的Actions-bbr-v3脚本一键安装BBR3内核的完整流程，包括安装命令、重启验证和实际使用感受。
---

BBR3 是目前 BBR 系列里最新的版本，已经合并进较新的 Linux 主线内核。网上流传的 BBR3 安装方式主要有两种：一种是装 XanMod 内核（内置了 BBR3 支持），另一种是用专门的脚本直接把 BBR3 内核装到现有系统上，byJoey 维护的 Actions-bbr-v3 属于后者。

这个脚本会自动识别当前系统架构，从 GitHub Releases 下载匹配的 BBR3 内核 .deb 包，安装完之后还能切换加速模式。一条命令跑完整个安装流程，不需要手动下载或者配置内核参数。

安装命令直接去 byJoey 的 GitHub 仓库找最新的，地址是 `https://github.com/byJoey/Actions-bbr-v3`，README 里有当前维护的安装命令，直接复制跑就行。脚本跑完之后建议重启服务器，让新内核生效：

\`\`\`bash
reboot
\`\`\`

重启之后验证 BBR3 有没有生效：

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

输出 `bbr` 说明生效了。再确认一下内核版本有没有切换过来：

\`\`\`bash
uname -r
\`\`\`

输出里应该能看到新的内核版本号，跟安装之前不一样。

实际用下来，装完 BBR3 之后代理节点的速度提升不算明显，跟原版 BBR 或者 BBRplus 的差距在日常使用中感觉不出太大区别。BBR 系列各版本之间本来差距就不大，可以参考[BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)，搞清楚各版本的定位之后对效果的期待会更准确。如果你的服务器已经装了 XanMod 内核，不需要额外跑这个脚本，XanMod 内置的 BBR3 直接开就行，具体参考[XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)。
