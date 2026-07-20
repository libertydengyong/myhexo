---
title: 一键root加改密码脚本
tags:
  - 一键root加改密码脚本
id: '194'
categories:
  - - vps技巧
date: 2025-12-31 16:20:33
---

来源:nodeseek   一键root加改密码脚本，包括适用于甲骨文: curl -fsSL -o root.sh “https://github.com/tonyliuzj/oneclick-root/releases/latest/download/root.sh” && chmod +x root.sh && sudo ./root.sh 或 wget -qO root.sh “https://github.com/tonyliuzj/oneclick-root/releases/latest/download/root.sh” && chmod +x root.sh && sudo ./root.sh   使用 root 权限运行脚本：sudo ./root.sh 脚本将会： 检测你的包管理器 更新软件包列表 安装 sudo 和 openssh-server 提示设置新的 root 密码 配置 SSH 允许 root 使用密码认证登录 重启 SSH 服务