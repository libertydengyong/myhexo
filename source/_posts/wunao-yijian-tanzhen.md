---
title: 最最最无脑的一键探针
date: 2026-04-16 22:30:00
tags:
categories:
---
这里写正文
docker run -d --restart=always -p 3001:3001 -v uptime-kuma:/app/data --name uptime-kuma louislam/uptime-kuma:1

运行后以 IP:3001打开即可
