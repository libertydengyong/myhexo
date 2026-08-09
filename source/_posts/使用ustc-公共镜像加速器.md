---
title: 使用USTC 公共镜像加速器
tags:
  - USTC 公共镜像加速器
id: '154'
categories:
  - Linux优化
abbrlink: 49188
date: 2025-07-24 19:47:47
---

创建 Docker 配置目录：

```bash
mkdir -p /etc/docker
```

创建 Docker 配置文件：

```bash
cat > /etc/docker/daemon.json
```

输入以下内容：

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```

终端新的一行按下 Ctrl + D，结束输入并保存文件。

验证配置：

```bash
cat /etc/docker/daemon.json
```

重启 Docker 服务：

```bash
systemctl restart docker
```
```
