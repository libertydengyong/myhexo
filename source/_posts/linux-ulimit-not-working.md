---
title: 为什么ulimit设置了文件描述符限制，服务还是报Too many open files
date: 2026-08-20 10:00:00
tags:
  - ulimit文件描述符
categories:
  - Linux优化
description: 修改了limits.conf、ulimit -a也确认生效了，systemd管理的服务却依然报错文件句柄不够，因为systemd根本不看这个配置文件。
---

服务并发一上来，日志里开始刷屏`Too many open files`，查了一圈发现是文件描述符（也就是`nofile`）限制不够用，照着教程改了`/etc/security/limits.conf`，重新登录敲一下`ulimit -a`，数字确实变大了，满心以为解决了，结果服务重启之后照样报同样的错，跟没改过一模一样。

## 你改对了地方，但改错了对象

问题的根源在于——`/etc/security/limits.conf`这个文件，**从来就不是给系统服务用的**。它的官方文档说得很直白："This file sets the resource limits for the users logged in via PAM...It does not affect resource limits of the system services."（这个文件设置的是通过PAM登录的用户的资源限制，不影响系统服务的资源限制。）

你改完这个文件，重新SSH登录一次，确实能看到`ulimit -a`里的数字变了——但那只是**你这次登录会话**通过PAM认证之后继承到的限制，跟你用`systemctl start`、`docker run`这类方式启动的后台服务完全是两码事。这些服务压根不是通过你的登录会话拉起来的，自然也就轮不到`limits.conf`来管它们。有人真的做过对比实验：改完`limits.conf`，自己的shell里`ulimit -a`显示正常，但MySQL服务本身查询它实际生效的`open_files_limit`，数值纹丝不动还是原来的1024。

## systemd是故意这么设计的，不是漏掉了

更准确地说，这不是"没生效"，是**systemd在设计上就故意无视这个全局配置文件**，官方文档原话是"Systemd does not support global limits, the file is intentionally ignored"（systemd不支持全局限制，这个文件被有意忽略）。systemd有自己独立的一套限制机制，得单独针对每个服务去配置。

## 正确的改法：给具体服务单独配置

以Nginx为例，给它专门建一个systemd覆盖配置，不用去动主配置文件：

```bash
mkdir -p /etc/systemd/system/nginx.service.d/
cat > /etc/systemd/system/nginx.service.d/override.conf << EOF
[Service]
LimitNOFILE=100000
EOF
systemctl daemon-reload
systemctl restart nginx
```

把`nginx`换成你实际要调整的服务名（比如`docker`、`mysqld`，或者你在跑的某个代理面板对应的服务名），思路都一样。

## 还有两层隐藏的天花板

就算这一步配对了，也可能碰到另外两层限制：一是内核本身有个硬顶`/proc/sys/fs/nr_open`，你设置的数值不能超过这个内核级上限；二是CentOS 7上曾经存在过一个已知的systemd bug（低于240版本），`LimitNOFILE`这个参数即使写了也不生效，需要额外手动干预才能真正吃到配置。遇到配置写对了但还是不生效的情况，这两个方向值得往下查。

## 顺带一提

如果这台VPS上跑着[Uptime Kuma](https://vpsjq.com/2026/04/16/wunao-yijian-tanzhen/)这类需要同时维持大量监控连接的探针服务，文件描述符不够用的问题会比一般场景更容易碰到，配置的时候可以适当留足余量。之前写[VPS磁盘空间满了怎么排查](https://vpsjq.com/2026/08/15/vps-disk-space-full/)那篇里提到用`lsof`排查文件占用的方法，跟这篇讲的文件描述符本质上是同一套底层机制，遇到跟"打开的文件太多"相关的报错，这两篇可以放一起对照着看。
