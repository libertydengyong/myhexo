---
title: 3x-ui配置Trojan节点：回落网站怎么设置
date: 2026-09-23 12:00:00
tags:
  - 3x-ui
  - Trojan
categories:
  - vps工具
description: 在3x-ui面板里配置Trojan节点的完整步骤，重点讲回落(Fallback)这个伪装成真实网站的配置，附密码认证和证书要求说明。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui配置Trojan节点：回落网站怎么设置",
      "description": "在3x-ui面板里配置Trojan节点的完整步骤，重点讲回落(Fallback)这个伪装成真实网站的配置，附密码认证和证书要求说明。",
      "datePublished": "2026-09-23T12:00:00+08:00",
      "dateModified": "2026-09-23T12:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/23/3x-ui-trojan/",
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
      "name": "3x-ui配置Trojan节点并设置回落",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建Trojan入站",
          "text": "入站列表点添加入站，协议选Trojan，密码自动生成，安全选项固定是TLS，需要先申请好域名证书。"
        },
        {
          "@type": "HowToStep",
          "name": "配置回落(Fallback)",
          "text": "在入站的回落设置里填一个真实网站的地址或者本地静态页面端口，探测流量不是Trojan协议的连接会被转发到这个回落目标，而不是直接报错。"
        },
        {
          "@type": "HowToStep",
          "name": "保存并获取分享链接",
          "text": "保存后点二维码图标获取trojan://开头的分享链接，导入客户端测试连接。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Trojan为什么必须用TLS？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Trojan的设计思路就是让流量看起来跟正常的HTTPS网站访问一模一样，靠的就是标准TLS握手这层伪装，如果不用TLS，流量特征会跟普通HTTPS网站完全不同，失去了Trojan最核心的伪装能力，所以协议本身就要求必须配TLS，面板里也没有其他安全选项可选。"
          }
        },
        {
          "@type": "Question",
          "name": "不配置回落会怎么样？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不配置回落，探测方（比如用浏览器直接访问这个端口，或者GFW的主动探测）发起非Trojan协议的连接时，服务端要么直接断开连接要么报错，这种反应本身就是一种特征，容易被用来识别这是个代理端口；配了回落之后，这类非法流量会被转发到一个正常网站，表现得跟一个真的HTTPS网站完全一样，抗探测能力更强。"
          }
        },
        {
          "@type": "Question",
          "name": "Trojan和VLESS Reality该选哪个？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "两者都是走伪装思路，但实现方式不同：Trojan需要真实域名和证书，靠真实TLS握手加回落网站伪装；Reality不需要自己的域名证书，直接借用目标网站的证书链伪装，配置更省事。不想折腾域名解析和证书申请的话，Reality更省心；已经有域名和证书在手上，Trojan也是成熟稳定的选择。"
          }
        }
      ]
    }
  ]
}
</script>

面板部分假设已经按[3x-ui安装教程](https://vpsjq.com/2026/04/30/2026-04-30-011/)装好。Trojan 是比较经典的伪装类协议，思路是让代理流量看起来跟访问一个正常 HTTPS 网站没有区别，核心机制是**回落（Fallback）**——探测流量不是合法的 Trojan 连接时，服务端会把它转发到一个真实网站，而不是直接报错暴露自己是个代理端口。

进入 3x-ui 面板，点**入站列表**，点**添加入站**，协议选 Trojan。密码这一栏面板会自动生成一串随机字符串，不需要手动填，这就是客户端连接时用的认证凭据，Trojan 不像 VMess/VLESS 那样用 UUID，用的是密码认证。

Trojan **必须**配 TLS，面板里安全选项这一栏没有 none 可选，直接就是 TLS 相关配置。需要先有一个解析好的域名并申请好证书，具体申请步骤参考[3x-ui配置TLS证书教程](https://vpsjq.com/2026/08/30/3x-ui-tls/)，证书路径填法跟其他协议用 TLS 时完全一样。

## 回落（Fallback）怎么配

这是 Trojan 配置里最容易被忽略、但也最关键的一步。入站配置展开之后能看到**回落设置**这一项，这里填的是一个"挡箭牌"——当有人（不管是随手拿浏览器访问这个端口的普通用户，还是网络审查系统的主动探测）发起的连接不符合 Trojan 协议的握手格式时，流量会被转发到回落设置里填的这个目标，而不是让服务端直接报错断开。

常见的回落目标有两种：

- **转发到本机的一个静态网站**：先在服务器上用 Nginx 或者随便一个静态文件服务器起一个看起来正常的网页，监听在一个本地端口（比如 8080），回落地址填 `127.0.0.1:8080`。
- **转发到一个真实的外部网站**：直接填一个正常网站的地址，效果类似 VLESS Reality 里的 dest 伪装，但实现层面不完全一样，具体选哪种网站的思路可以参考[3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)里对 dest 伪装网站的选择建议。

回落这一步不是可选项，不配的话安全性会打折扣——探测方虽然拿不到你的密码，但能通过"连接被异常断开"这个反应本身判断出这个端口有问题，间接暴露了这是个代理端口。

## 获取分享链接并导入客户端

保存入站配置之后，在入站列表找到这条记录，点二维码图标查看分享链接，格式是 `trojan://` 开头的。主流客户端（NekoBox、Clash Meta、Shadowrocket 等）都支持 Trojan 协议，导入链接之后基本不需要额外配置。

连不上的时候按这个顺序排查：

1. 域名解析和证书是否正常，参考 TLS 那篇文章里的排查方法；
2. 客户端里的密码是否跟面板一致，Trojan 认证只看密码，填错了直接连不上；
3. 回落配置本身有没有把真正的 Trojan 流量也错误转发出去——回落只应该拦截"不符合协议格式"的流量，正常的 Trojan 握手不会被误判，如果配置有问题导致正常流量也走了回落，客户端会显示连接成功但实际不通。

如果不想折腾域名和证书，可以考虑换成 [VLESS Reality](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)，不需要自己的证书，配置思路更简单。多用户管理可以参考[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)。
