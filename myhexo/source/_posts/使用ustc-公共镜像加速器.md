---
title: 使用USTC 公共镜像加速器
tags:
  - USTC 公共镜像加速器
id: '154'
categories:
  - - uncategorized
date: 2025-07-24 19:47:47
---

创建/etc/docker/ 目录: mkdir -p /etc/docker/ **创建 `/etc/docker/daemon.json` 文件并粘贴配置：**使用 USTC 的加速器地址 `https://docker.mirrors.ustc.edu.cn` 输入    cat > /etc/docker/daemon.json

按下 Enter 键后，光标会停留在新行等待输入，输入:

{

  "registry-mirrors": \["https://docker.mirrors.ustc.edu.cn"\]

}

终端的新的一行按下 Ctrl + D ，结束输入并保存文件。

验证文件:

cat /etc/docker/daemon.json

**重启 Docker 服务：**

service docker restart