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

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "专为alpine定制的Xray一键脚本",
      "description": "专为 Alpine Linux 系统定制的轻量级 Xray 节点一键部署脚本，适合小内存 VPS 快速搭建代理。",
      "datePublished": "2025-07-01T15:45:48+08:00",
      "dateModified": "2025-07-01T15:45:48+08:00",
      "url": "https://vpsjq.com/2025/07/01/专为alpine定制的xray一键脚本/",
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
      "name": "在Alpine上安装Xray一键脚本",
      "step": [
        {
          "@type": "HowToStep",
          "name": "下载并运行安装脚本",
          "text": "执行wget https://raw.githubusercontent.com/miku111/XrayOnAlpine/main/install-release.sh && bash install-release.sh，或者用curl -L -s下载后执行。"
        },
        {
          "@type": "HowToStep",
          "name": "启动Xray服务",
          "text": "执行sudo service xray start启动服务，Alpine用的是OpenRC而不是systemd，用service命令而不是systemctl。"
        }
      ]
    }
  ]
}
</script>

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
