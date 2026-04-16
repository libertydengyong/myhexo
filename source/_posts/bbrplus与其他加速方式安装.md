---
title: BBRplus与其他加速方式安装
tags:
  - BBRplus
id: '37'
categories:
  - - vps工具
date: 2025-05-06 20:28:53
---

wget -N --no-check-certificate "https://gist.github.com/zeruns/a0ec603f20d1b86de6a774a8ba27588f/raw/4f9957ae23f5efb2bb7c57a198ae2cffebfb1c56/tcp.sh" && chmod +x tcp.sh && ./tcp.sh 重启 接着 **./tcp.sh** 检测是否在运行，输入:    lsmod grep bbr 或   sysctl net.ipv4.tcp\_congestion\_control 如果都有bbrplus ，则表明bbrplus在运行。