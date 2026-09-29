---
title: S-UI搭建Trojan节点，跟3x-ui比少了回落这一步
date: 2026-09-30 10:00:00
tags:
  - S-UI教程
  - Trojan
categories:
  - vps技巧
description: S-UI面板配置Trojan节点的实际步骤，密码认证加一个TLS模板就能用，面板前端代码里确认过并没有回落(Fallback)这个配置项，跟3x-ui的思路不完全一样。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI搭建Trojan节点，跟3x-ui比少了回落这一步",
      "description": "S-UI面板配置Trojan节点的实际步骤，密码认证加一个TLS模板就能用，面板前端代码里确认过并没有回落(Fallback)这个配置项，跟3x-ui的思路不完全一样。",
      "datePublished": "2026-09-30T10:00:00+08:00",
      "dateModified": "2026-09-30T10:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-trojan/",
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
      "name": "S-UI配置Trojan节点",
      "step": [
        {
          "@type": "HowToStep",
          "name": "准备一个TLS模板",
          "text": "Trojan必须用TLS，先在面板的TLS管理里创建好证书模板，域名证书或自签证书都可以。"
        },
        {
          "@type": "HowToStep",
          "name": "新建入站选择Trojan",
          "text": "协议选Trojan，密码自动生成或手动填，网络类型留默认TCP/UDP即可。"
        },
        {
          "@type": "HowToStep",
          "name": "绑定TLS模板",
          "text": "在TLS这一项选择刚才创建好的证书模板，而不是重新填一遍证书路径。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI的Trojan节点能不能配置回落(Fallback)？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不能，面板界面上没有这个选项。翻过S-UI前端的开源代码，Trojan这部分组件只有密码和网络类型两个字段，跟3x-ui基于Xray-core、把回落当作核心配置项的做法不一样，属于两个项目的设计差异，不是哪边少配了或者版本问题。"
          }
        },
        {
          "@type": "Question",
          "name": "没有回落是不是意味着S-UI的Trojan不安全？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不算不安全，只是抗探测的手段少了一层。回落的作用是把不符合Trojan协议的探测流量转发到一个真实网站上，没有这一层，探测方发起非法连接时服务端的反应可能会跟正常网站略有区别，理论上多一点点被识别的可能，但密码认证和TLS加密这两层核心防护是不受影响的，正常使用没有问题。"
          }
        },
        {
          "@type": "Question",
          "name": "TLS模板要给每个入站都重新填一次证书路径吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不用。S-UI是先在TLS管理里建好一个证书模板，后面新建任何需要TLS的入站(Trojan、TLS方式的VLESS等)时，直接选这个模板就行，不需要每个入站都重新填一遍证书文件路径，这点比按入站单独配置证书的做法省事。"
          }
        }
      ]
    }
  ]
}
</script>

翻了一下 [alireza0/s-ui-frontend](https://github.com/alireza0/s-ui-frontend) 的开源代码才确认，S-UI 的 Trojan 入站组件只有密码和网络类型两个可填字段，没有 3x-ui 那种专门的回落（Fallback）配置区。不是少了什么或者哪个版本的bug，两个项目基于的核心不一样（S-UI用的是Sing-Box，3x-ui用的是Xray-core），对Trojan的实现思路本来就有差异，配置起来也确实比 3x-ui 简单一截。

Trojan 这个协议核心思路是让代理流量看起来跟访问一个正常 HTTPS 网站没有区别，认证方式是密码而不是 UUID，这点两边都一样。安全性上必须搭配 TLS，这也是硬性要求，没有 none 这个选项可选。

## 先准备一个TLS模板

S-UI 处理证书的方式是先在面板的 TLS 管理里建一个模板，后面任何需要 TLS 的入站直接选这个模板就行，不用每次都重新填证书路径。如果还没建过，参考[S-UI面板申请和配置SSL证书](https://vpsjq.com/2026/08/28/s-ui-certificate/)，自签证书和正式域名证书这篇里都讲了，先把这一步做完。

## 新建Trojan入站

进入入站管理，新建入站，协议选 **Trojan**。密码这一栏可以让面板自动生成一串随机字符串，也可以手动填，客户端连接时用的就是这个密码，不涉及 UUID。网络类型留默认的 TCP/UDP 就行，不需要额外选。

## 绑定TLS模板

TLS 这一项从下拉列表里选刚才建好的证书模板，选完保存。这一步跟前面提到的一样，是直接引用模板而不是重新填证书文件路径，如果这一步找不到刚建的模板，回头确认一下 TLS 管理那边是不是真的保存成功了。

## 获取分享链接

保存之后在入站列表点二维码图标，能看到 `trojan://` 开头的分享链接，格式和字段跟 3x-ui 生成的基本一样，主流客户端（NekoBox、Clash Meta、Shadowrocket 等）都认。

连不上的时候先确认域名解析和证书本身没问题，这部分排查方法跟[SSL证书教程](https://vpsjq.com/2026/08/28/s-ui-certificate/)里说的一致；再确认客户端填的密码跟面板一致，Trojan 只认密码，填错了不会有明确报错，就是直接连不上。如果之前在 3x-ui 上配过 Trojan、习惯了先想"回落配置对不对"，在 S-UI 这边可以跳过这一步，没有这个选项也不影响正常使用。
