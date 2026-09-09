---
title: "一行代码部署极简开源网页版 SSH 管理工具"
tags:
  - "网页版 SSH 管理"
id: '159'
categories:
  - vps技巧
abbrlink: 31186
date: 2025-07-28 12:36:20
description: Managi是一款极简开源的网页版SSH管理工具，一行docker命令部署，不用装客户端，浏览器直接管理服务器。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "一行代码部署极简开源网页版 SSH 管理工具",
      "description": "Managi是一款极简开源的网页版SSH管理工具，一行docker命令部署，不用装客户端，浏览器直接管理服务器。",
      "datePublished": "2025-07-28T12:36:20+08:00",
      "dateModified": "2025-07-28T12:36:20+08:00",
      "url": "https://vpsjq.com/2025/07/28/一行代码部署极简、开源的网页版-ssh-管理/",
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
      "name": "部署Managi网页版SSH管理工具",
      "step": [
        {
          "@type": "HowToStep",
          "name": "执行Docker一行命令部署",
          "text": "docker run -d --network host hochenggang/managi:0.5.0，--network host表示容器直接使用宿主机网络。"
        },
        {
          "@type": "HowToStep",
          "name": "浏览器访问管理界面",
          "text": "部署完成后通过http://VPS_IP:18001访问，打开浏览器输入网址就能连VPS，不用在设备上装SSH客户端。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Managi适合什么场景？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "适合临时借用别人电脑操作服务器（用完关掉浏览器不留痕迹）、平板手机等不方便装客户端的设备、或者快速给团队成员一个统一的管理入口不用每人各自配置SSH客户端和密钥。"
          }
        }
      ]
    }
  ]
}
</script>

一行代码部署极简、开源的**网页版 SSH** 管理: docker run -d --network host hochenggang/managi:0.5.0 访问 http://VPS_IP:18001

这个工具叫**Managi**，是作者hochenggang开发的一款轻量级网页SSH管理工具（GitHub: hochenggang/managi-backend），核心思路很简单——把SSH客户端搬到浏览器里，不用在电脑上装PuTTY、Xshell这些客户端，也不用在手机上找专门的SSH App，打开浏览器输入网址就能连VPS。

## 适合的场景

- **临时借用别人电脑操作服务器**：不想在陌生电脑上装客户端软件，网页版用完关掉浏览器就行，不留痕迹
- **平板/手机等不方便装客户端的设备**：只要有浏览器就能用
- **快速给团队成员一个统一的管理入口**：不用每个人各自配置SSH客户端和密钥

## 部署说明

原文的一行命令用的是Docker，`--network host` 表示容器直接使用宿主机网络，部署完成后通过 `http://VPS_IP:18001` 访问即可。作为一个极简工具，它的部署方式也确实符合"极简"这个定位——一条命令、一分钟内就能跑起来，没有复杂的配置文件需要提前准备。

如果更习惯纯命令行操作、不想额外跑一个Docker容器占用资源，也可以看看[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)里介绍的直接用SSH客户端连接的方式，两种各有适合的场景，网页版胜在跨设备方便，命令行版胜在轻量、不依赖额外服务。
