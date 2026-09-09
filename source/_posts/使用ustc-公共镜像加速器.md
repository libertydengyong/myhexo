---
title: 使用USTC 公共镜像加速器
tags:
  - USTC 公共镜像加速器
id: '154'
categories:
  - Linux优化
abbrlink: 49188
date: 2025-07-24 19:47:47
description: 配置中国科学技术大学（USTC）Docker 公共镜像加速器的目录创建与 daemon.json 参数修改步骤。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "使用USTC 公共镜像加速器",
      "description": "配置中国科学技术大学（USTC）Docker 公共镜像加速器的目录创建与 daemon.json 参数修改步骤。",
      "datePublished": "2025-07-24T19:47:47+08:00",
      "dateModified": "2025-07-24T19:47:47+08:00",
      "url": "https://vpsjq.com/2025/07/24/使用ustc-公共镜像加速器/",
      "author": {
        "@type": "Organization",
        "name": "vpsjq.com"
      },
      "publisher": {
        "@type": "Organization",
        "name": "vpsjq.com"
      }
    },
    {
      "@type": "HowTo",
      "name": "配置USTC Docker镜像加速器",
      "step": [
        {
          "@type": "HowToStep",
          "name": "创建Docker配置目录",
          "text": "执行mkdir -p /etc/docker创建配置目录。"
        },
        {
          "@type": "HowToStep",
          "name": "写入daemon.json配置",
          "text": "创建/etc/docker/daemon.json文件，写入registry-mirrors指向https://docker.mirrors.ustc.edu.cn。"
        },
        {
          "@type": "HowToStep",
          "name": "重启Docker服务生效",
          "text": "执行systemctl restart docker让配置生效。"
        }
      ]
    }
  ]
}
</script>

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
