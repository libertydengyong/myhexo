---
title: 最最最无脑的一键探针
abbrlink: 49231
date: 2026-04-16 22:30:00
tags:
  - Uptime-Kuma
categories:
  - vps工具
description: Uptime Kuma是一款开源自托管监控工具，Docker一键部署，支持HTTP、TCP、Ping、Docker容器等多种监控方式。
---

这个工具叫**Uptime Kuma**，作者louislam，是一款开源的自托管监控工具，作用类似Uptime Robot这类第三方监控服务，区别是完全自己部署、自己掌控数据，没有第三方平台的使用限制。

```bash
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1
```

运行后以 IP:3001打开即可

## 主要功能

- **多种监控类型**：HTTP(s)、TCP、Ping、DNS记录、Docker容器状态、Steam游戏服务器等，覆盖场景比较全
- **丰富的通知方式**：支持微信、钉钉、邮件、Webhook等90多种告警渠道，服务异常能第一时间收到通知
- **美观的仪表盘**：界面比较精致，多个监控项的状态一目了然，还支持多语言
- **轻量**：基于Node.js和Vue 3开发，Docker部署几分钟就能跑起来

## 首次使用

容器启动后访问 `http://VPS的IP:3001`，首次打开会要求创建管理员账号，设置好之后就能在后台添加监控项——填入要监控的服务地址、选择监控类型、设置检测间隔和通知方式，保存就能开始监控了。

如果是想用手机随时看服务器状态，Uptime Kuma走的是网页Dashboard的路线，跟之前写的[Mdpings另一个手机探针App](https://freedomgpt.top/2025/07/24/mdpings-%E5%8F%A6%E4%B8%80%E4%B8%AA%E6%89%8B%E6%9C%BA%E6%8E%A2%E9%92%88app/)不太一样——Uptime Kuma是自己搭建监控服务端，Mdpings则是连接哪吒面板的手机客户端，两者定位不同，可以按自己的使用习惯选。
