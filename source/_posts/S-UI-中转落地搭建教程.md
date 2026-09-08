---
title: S-UI 中转落地搭建教程
abbrlink: 49079
date: 2026-01-11 12:45:22
categories:
  - vps技巧
tags:
  - S-UI中转落地
  - S-UI教程
description: S-UI面板搭建中转落地代理架构的完整步骤，涵盖落地机入站配置、中转机出站设置和路由规则建立。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI 中转落地搭建教程",
      "description": "S-UI面板搭建中转落地代理架构的完整步骤，涵盖落地机入站配置、中转机出站设置和路由规则建立。",
      "datePublished": "2026-01-11T12:45:22+08:00",
      "dateModified": "2026-01-11T12:45:22+08:00",
      "url": "https://vpsjq.com/2026/01/11/S-UI-中转落地搭建教程/",
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
      "name": "S-UI搭建中转落地架构",
      "step": [
        {
          "@type": "HowToStep",
          "name": "落地机配置Shadowsocks入站",
          "text": "进入落地机面板入站管理，入站类型选Shadowsocks，监听端口自定，方法选2022-blake3-aes这类，网络选TCP/UDP，密码自动生成并记下备用。"
        },
        {
          "@type": "HowToStep",
          "name": "中转机配置VLESS入站",
          "text": "进入中转机面板入站管理，入站类型选VLESS，标签设置好认的名字，监听端口用系统生成的即可。"
        },
        {
          "@type": "HowToStep",
          "name": "中转机新建Shadowsocks出站",
          "text": "出站管理里新建出站，类型选Shadowsocks，服务器地址填落地机IP，端口、方法、密码填跟落地机一致的值。"
        },
        {
          "@type": "HowToStep",
          "name": "新建用户并配置路由规则",
          "text": "用户管理里新建用户并绑定到VLESS入站，路由列表里添加规则把这个用户的流量指向刚建的Shadowsocks出站。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "怎么验证中转落地配置成功？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "把用户的节点链接复制导入客户端连接后打开网页检查IP，显示的应该是落地机的IP而不是中转机的IP，说明流量已经正确走了中转落地的路径。"
          }
        }
      ]
    }
  ]
}
</script>

来源：NodeSeek（原帖已设为私有）

<!-- more -->

中转落地的思路是把入口和出口分开部署在两台服务器上，入口用高速线路接入，出口负责实际访问目标网站，两台机器之间通过内部协议打通。S-UI 面板对这种架构支持比较完整，入站、出站、路由规则都可以在面板里直接配置。S-UI 的安装方式和基础配置可以先参考[S-UI面板搭建教程](https://vpsjq.com/2025/11/17/s-ui面板搭建/)，两台服务器都需要先装好面板再继续下面的步骤。

安装命令：

\`\`\`bash
bash <(curl -Ls https://raw.githubusercontent.com/alireza0/s-ui/master/install.sh)
\`\`\`

落地机配置：

进入面板入站管理，入站类型选 Shadowsocks，监听端口自定，比如 8081，方法随便选，比如 `2022-blake3-aes`，网络选 TCP/UDP，密码自动生成，保存退出。记下生成的密码，中转机那边要用。

中转机配置：

进入面板入站管理，入站类型选 VLESS，标签写清楚，比如"日澳Trans"，这个标签名后面会显示在节点名称里，建议取得好认一点。监听端口用系统生成的就行。

出站管理里新建一条出站，类型选 Shadowsocks，标签自定义一个好区分的名字，比如"Shadowsocks-AUS"。服务器地址填落地机 IP，端口填刚才落地机设置的 8081，方法和密码填跟落地机一致的值。保存。

用户管理里新建用户，名字简短好认，比如"日澳"，入站标签选刚才建的 VLESS 入站。

路由列表里添加规则，用户选刚才新建的用户，出站选刚才建的 Shadowsocks-AUS。注意保存，如果弹出网络错误可以直接无视，刷新页面继续。

配置完成后去用户管理，把这个用户的节点链接复制出来导入客户端，连上之后打开网页检查 IP，显示的应该是落地机的 IP 而不是中转机的 IP，说明流量已经正确走了中转落地的路径。如果想用其他协议搭建中转，也可以参考[Vmess+WebSocket搭建中转服务器](https://vpsjq.com/2025/05/09/vmesswebsocket搭建中转服务器/)，思路类似但协议不同。
