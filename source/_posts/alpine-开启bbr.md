---
title: Alpine 开启bbr
tags:
  - Alpine 开启bbr
id: '144'
categories:
  - - vps技巧
date: 2025-07-12 23:17:31
---

Alpine 开启bbr: echo "tcp\_bbr" >> /etc/modules && modprobe tcp\_bbr echo "net.ipv4.tcp\_congestion\_control=bbr" >> /etc/sysctl.conf echo "net.core.default\_qdisc=fq" >> /etc/sysctl.conf sysctl -p 验证    lsmod grep bbr