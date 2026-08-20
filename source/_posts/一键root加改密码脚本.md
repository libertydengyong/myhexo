---
title: 一键root加改密码脚本
tags:
  - 一键root加改密码脚本
id: '194'
categories:
  - vps技巧
abbrlink: 60516
date: 2025-12-31 16:20:33
description: 适用于甲骨文等 VPS 的一键开启 root 登录与修改密码脚本，自动检测包管理器、安装 Sudo/SSH 并允许密码认证。
---

来源:nodeseek   一键root加改密码脚本，包括适用于甲骨文: curl -fsSL -o root.sh 原项目下载链接已失效，请查阅官方最新项目 && chmod +x root.sh && sudo ./root.sh 或 wget -qO root.sh 原项目下载链接已失效，请查阅官方最新项目 && chmod +x root.sh && sudo ./root.sh   使用 root 权限运行脚本：sudo ./root.sh 脚本将会： 检测你的包管理器 更新软件包列表 安装 sudo 和 openssh-server 提示设置新的 root 密码 配置 SSH 允许 root 使用密码认证登录 重启 SSH 服务