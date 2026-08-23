---
title: VPS配了IPv6，Docker容器里却死活连不上
date: 2026-08-25 10:00:00
tags:
  - Docker-IPv6
categories:
  - vps技巧
description: 宿主机IPv6配置得再完美，Docker容器默认也不会继承这个能力，得手动改daemon.json开启才行，这是Docker的默认行为，不是配置出了问题。
---

VPS本身IPv6配置得妥妥当当，`ping -6`一测宿主机畅通无阻，装进容器里的服务却怎么都连不上IPv6，`docker exec`进去一试，IPv6网络对这个容器来说压根不存在。折腾半天以为是容器内部网络设置有问题，其实**Docker默认根本不会把宿主机的IPv6能力传给容器**，这是设计上的默认行为，不是哪里配错了。

## Docker压根没把IPv6当默认选项

Docker对IPv6的支持长期不如IPv4积极，容器网络默认走的是私有的IPv4段，宿主机有没有IPv6跟容器能不能用IPv6，是两件完全不搭界的事。想让容器拿到IPv6能力，得手动改Docker的配置文件：

```bash
vi /etc/docker/daemon.json
```

加上这两项：

```json
{
  "ipv6": true,
  "fixed-cidr-v6": "fd00:db8:1::/64"
}
```

`fixed-cidr-v6`给的是一个私有IPv6网段，容器之间用这个网段互相通信；`fd00::/8`这类前缀是IPv6里对应IPv4私有地址（`10.0.0.0/8`那种）的等价物，专门留给内网场景用，照抄这个格式就行，不用自己纠结换成别的网段。

改完重启Docker服务让配置生效：

```bash
systemctl restart docker
```

## 确认有没有真的生效

```bash
docker network inspect bridge
```

看输出里`EnableIPv6`这一项是不是`true`，`IPAM.Config`里有没有出现你刚才配的那个IPv6网段。这一步能省掉后面很多冤枉排查——如果这里显示没生效，再怎么折腾容器内部网络设置都是白费功夫。

## 光配置daemon.json，可能还不够

**如果宿主机的网关分配的是私网IPv6**（不是公网直连），上面这套配置一般能直接生效；但如果宿主机拿到的是公网IPv6网关，情况会复杂一些，理论上还得配合`iptables`（准确说是IPv6对应的`ip6tables`）做地址映射才能真正打通，光改daemon.json不一定够用，具体取决于VPS服务商分配IPv6的方式。

确认改动生效后，实际测试一下：

```bash
docker run --network=bridge --rm -it busybox ping -6 -c4 google.com
```

## 只是临时用一下，也可以走host网络模式

如果不想动全局的Docker配置，只是某个容器临时需要用IPv6，还有个更简单的旁路方案——用host网络模式跑这个容器，直接借用宿主机自己的网络协议栈，宿主机能访问IPv6，容器立刻就能访问，不需要额外配置：

```bash
docker run --network=host 镜像名
```

缺点是host模式下容器和宿主机共用同一套网络命名空间，端口映射这些跟bridge模式的逻辑不一样，适合临时验证或者单容器场景，如果是多容器长期跑的生产环境，还是建议老老实实按上面的方式把daemon.json配好，更规范也更好维护。

## 顺带一提

这种"宿主机能力齐全，但容器/子系统默认不继承"的情况，跟之前写的[VPS重启后Docker容器为什么没有自动启动](https://vpsjq.com/2026/08/17/docker-restart-policy/)是同一个脾气——Docker很多行为默认都偏保守，不会自作主张帮你把宿主机的能力透传进去，重启策略是这样，IPv6支持也是这样，新装的服务多留意一下默认值，别想当然。如果这台VPS本身的IPv6配置就有问题（不只是Docker层面），可以先看[VPS防火墙规则设置了，IPv6那边却像没设一样](https://vpsjq.com/2026/08/24/ipv6-ip6tables-not-working/)那篇，排查一下宿主机这一层的IPv6是不是真的健康，再往Docker这一层深入。
