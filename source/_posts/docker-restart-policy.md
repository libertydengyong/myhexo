---
title: VPS重启后Docker容器为什么没有自动启动
date: 2026-08-17 10:00:00
tags:
  - Docker重启策略
categories:
  - vps工具
description: Docker容器默认不会在VPS重启后自动启动，需要设置restart策略，docker update命令能在不重建容器的情况下直接修复。
---

VPS因为维护或者别的原因重启了一下，回去一看，之前跑得好好的Docker容器全没了，得手动一个个`docker start`才能拉起来。这不是Docker出故障了，是**容器的默认重启策略本来就是"不自动重启"**，这个坑几乎每个刚开始用Docker的人都会踩一次。

## 默认策略是"no"，不是"always"

`docker run`起容器的时候，如果没有额外指定`--restart`参数，Docker默认用的策略是`no`——容器进程一旦退出（不管是正常退出还是宿主机重启导致的），Docker都不会主动把它拉起来，得手动干预。这是设计上的默认行为，不是bug。

Docker一共提供四种策略：`no`（默认，从不自动重启）、`on-failure`（只有异常退出才重启，正常退出不管）、`always`（不管什么原因退出都会重启，哪怕是你自己手动停掉的，Docker服务一重启它也会被拉起来）、`unless-stopped`（跟`always`几乎一样，唯一区别是如果容器是你主动停掉的，宿主机重启后也会保持停止状态，不会被硬拉起来）。

对大部分长期跑着的服务（面板、监控探针这类），**`unless-stopped`最推荐**，既保证意外情况下能自动恢复，又不会在你主动停掉之后被强行拉起来打乱操作。

## 已经在跑的容器，不用重新创建

如果容器已经跑起来了，只是想给它补上重启策略，不需要删掉重建，直接改：

```bash
docker update --restart unless-stopped 容器名或ID
```

## 新建容器时直接带上参数

以后每次`docker run`，习惯性带上这个参数：

```bash
docker run -d --restart unless-stopped --name 容器名 镜像名
```

## 补上策略了，重启还是没自动起来

如果确认容器已经设置好`unless-stopped`或者`always`，重启VPS之后依然没有自动拉起来，问题可能出在更底层——**Docker这个服务本身有没有设置成开机自启**。容器的重启策略是Docker daemon负责执行的，如果Docker服务自己都没跟着系统一起启动，容器策略再对也没用：

```bash
systemctl enable docker
systemctl status docker
```

确认状态是`enabled`，这一步经常被忽略，是"明明设置了restart策略但还是没生效"的常见原因。

## 顺带一提

之前写的几篇Docker部署文章，命令示例不是每个都带了`--restart`参数——[Uptime Kuma探针](https://vpsjq.com/2026/04/16/wunao-yijian-tanzhen/)那篇带了`--restart=always`，重启不用管；但[Managi网页版SSH管理](https://vpsjq.com/2025/07/28/%E4%B8%80%E8%A1%8C%E4%BB%A3%E7%A0%81%E9%83%A8%E7%BD%B2%E6%9E%81%E7%AE%80%E3%80%81%E5%BC%80%E6%BA%90%E7%9A%84%E7%BD%91%E9%A1%B5%E7%89%88-ssh-%E7%AE%A1%E7%90%86/)那篇当时没加，长期用着的话建议照这篇的方法自己补上。
