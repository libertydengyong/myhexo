---
title: 专为alpine定制的Xray一键脚本
tags:
  - Xray一键脚本
id: '134'
categories:
  - vps技巧
abbrlink: 106
date: 2025-07-01 15:45:48
description: 专为 Alpine Linux 系统定制的轻量级 Xray 节点一键部署脚本，适合小内存 VPS 快速搭建代理。
---

专为 alpine 定制的 Xray 一键脚本：

```bash
wget https://raw.githubusercontent.com/miku111/XrayOnAlpine/main/install-release.sh && bash install-release.sh
```

或者：

```bash
curl -L -s https://raw.githubusercontent.com/miku111/XrayOnAlpine/main/install-release.sh
```

启动 Xray：

```bash
sudo service xray start
```

项目来源：

```text
https://github.com/miku111/XrayOnAlpine
```
