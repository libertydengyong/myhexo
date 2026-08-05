---
title: Alpine 开启bbr
tags:
  - Alpine 开启bbr
id: '144'
categories:
  - vps技巧
abbrlink: 48757
date: 2025-07-12 23:17:31
description: Alpine Linux系统开启BBR拥塞控制算法的命令和验证方法，适合小内存VPS使用的轻量系统。
---

Alpine 开启bbr: echo "tcp_bbr" >> /etc/modules && modprobe tcp_bbr echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf sysctl -p 验证    lsmod grep bbr

Alpine是不少小内存VPS（比如256M内存）的首选系统，比Debian/Ubuntu这类系统空载内存占用低不少。不过Alpine默认用的是OpenRC而不是systemd，一些常规Linux发行版的BBR开启方式（比如某些一键脚本依赖systemd相关命令）在Alpine上未必好使，需要用上面这种更基础的方式手动开启。

## 命令说明

- `echo "tcp_bbr" >> /etc/modules`：把tcp_bbr模块写入开机自动加载列表
- `modprobe tcp_bbr`：立即加载这个内核模块，不用等重启
- 后面两条 `sysctl.conf` 配置：分别设置拥塞控制算法为BBR、默认队列规则为fq

执行完 `sysctl -p` 让配置立即生效，不需要重启服务器。

## 验证是否开启成功

```bash
lsmod | grep bbr
```

如果返回类似 `tcp_bbr    16384    5` 这样的结果，说明模块已经正常加载，BBR开启成功。也可以用下面这条进一步确认当前生效的拥塞控制算法：

```bash
sysctl net.ipv4.tcp_congestion_control
```

## 相关内容

这套手动命令跟之前写的[Linux TCP/IP和BBR参数智能优化脚本](https://freedomgpt.top/2025/11/30/linux-tcp-ip-%E5%92%8C-bbr-%E5%8F%82%E6%95%B0%E6%99%BA%E8%83%BD%E4%BC%98%E5%8C%96%E8%84%9A%E6%9C%AC/)原理是一样的，只是那篇的一键脚本更适合通用发行版，Alpine系统更适合这种手动方式。如果这台Alpine VPS还打算搭代理服务，可以看看[专为Alpine定制的Xray一键脚本](https://freedomgpt.top/2025/07/01/%E4%B8%93%E4%B8%BAalpine%E5%AE%9A%E5%88%B6%E7%9A%84xray%E4%B8%80%E9%94%AE%E8%84%9A%E6%9C%AC/)，跟这篇一起用能把小内存VPS的性能和网络体验都调到位。
