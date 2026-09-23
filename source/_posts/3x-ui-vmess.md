---
title: 3x-ui配置VMess节点：WS+TLS怎么设置
date: 2026-09-23 10:00:00
tags:
  - 3x-ui
  - VMess
categories:
  - vps工具
description: 在3x-ui面板里配置VMess节点的完整步骤，重点讲WebSocket+TLS这种适合套CDN的组合怎么填，以及alterId为什么现在都建议填0。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui配置VMess节点：WS+TLS怎么设置",
      "description": "在3x-ui面板里配置VMess节点的完整步骤，重点讲WebSocket+TLS这种适合套CDN的组合怎么填，以及alterId为什么现在都建议填0。",
      "datePublished": "2026-09-23T10:00:00+08:00",
      "dateModified": "2026-09-23T10:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/23/3x-ui-vmess/",
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
      "name": "3x-ui配置VMess节点(WS+TLS)",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建VMess入站",
          "text": "入站列表点添加入站，协议选VMess，传输方式选ws，安全选项选tls，需要一个已经解析好的域名。"
        },
        {
          "@type": "HowToStep",
          "name": "填写WebSocket路径并申请证书",
          "text": "路径自定义一段不好猜的字符串，证书可以用面板自带的acme申请，域名解析要先做好。"
        },
        {
          "@type": "HowToStep",
          "name": "确认加密方式和alterId",
          "text": "加密方式选auto，alterId填0，这是现在版本的标准做法，不需要跟老教程一样填64。"
        },
        {
          "@type": "HowToStep",
          "name": "保存并获取分享链接",
          "text": "保存后点二维码图标获取vmess://开头的分享链接，导入客户端测试连接。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "VMess的alterId应该填多少？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "现在的Xray-core版本统一建议填0。alterId是VMess早期为了防重放攻击设计的机制，后来VMess AEAD协议出来后这个机制已经过时，非0的alterId反而会被判定成旧协议，新装节点填0就行，不用照抄网上填64的老教程。"
          }
        },
        {
          "@type": "Question",
          "name": "VMess和VLESS该选哪个？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "新装节点优先选VLESS。VMess协议本身自带一层加密，套上TLS之后相当于加密了两次，白白消耗性能；VLESS没有这层内置加密，完全依赖外层TLS，效率更高。VMess胜在客户端兼容性好、老设备和老客户端基本都支持，如果是给不方便升级客户端的老设备用，VMess仍然是稳妥的选择。"
          }
        },
        {
          "@type": "Question",
          "name": "VMess套WebSocket之后可以过CDN吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以，这是VMess+WS+TLS这个组合最常见的用法。WebSocket走的是标准HTTPS端口和协议，Cloudflare这类CDN能正常识别转发，能在一定程度上隐藏服务器真实IP，代价是会比不套CDN多一次转发，延迟会增加一些。"
          }
        }
      ]
    }
  ]
}
</script>

面板部分假设已经按[3x-ui安装教程](https://vpsjq.com/2026/04/30/2026-04-30-011/)装好。3x-ui 支持的协议里，VMess 是资历最老的一个，现在新装节点更多人会优先选 [VLESS](https://vpsjq.com/2026/08/30/3x-ui-vless/) 或者 [VLESS Reality](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)，但 VMess 胜在客户端兼容性好，一些老设备、老客户端只认 VMess，这种情况下还是得配 VMess。这篇讲的是最常见的用法——VMess 套 WebSocket+TLS，方便后续接 CDN。

进入 3x-ui 面板，点**入站列表**，点**添加入站**，协议选 VMess，传输方式选 `ws`，安全选项选 `tls`。用 TLS 就需要一个已经解析到这台服务器的域名，纯 IP 没法申请证书。

路径（Path）这一栏自定义一段不好猜的字符串，比如 `/a1b2c3-ws`，不要用 `/` 这种默认值，容易被扫描到。证书可以用面板自带的 acme 功能自动申请 Let's Encrypt 证书，前提是域名已经解析好，80/443 端口没被占用：

```bash
ufw allow 80
ufw allow 443
```

加密方式（Security）选 `auto`，客户端和服务端会自动协商用哪种加密算法，不需要手动指定。

**alterId 这一栏填 0**。alterId 是 VMess 早期为了防重放攻击设计的一个机制，后来 VMess AEAD 协议出来之后这个机制已经过时了，现在的 Xray-core 版本看到非 0 的 alterId 反而会当成旧版协议处理，新装节点统一填 0 就行，网上一些老教程写的填 64、填 100 都是过时的做法，不要照抄。

端口用系统随机生成或者自己填一个都可以，因为走的是标准 HTTPS 端口（443），实际对外暴露的是 443，面板里填的这个端口是服务器内部监听用的，不需要额外放行。

保存之后在入站列表找到这条记录，点二维码图标可以看到分享链接，格式是 `vmess://` 开头，复制到客户端导入。主流客户端（NekoBox、Clash Meta、v2rayN 等）都支持 VMess+WS+TLS 这个组合，导入之后基本不需要额外配置。

连不上的时候按这个顺序排查：

1. 域名解析是否正确指向这台服务器，用 `ping 你的域名` 确认解析生效；
2. 证书是否申请成功，面板证书管理里能看到证书状态和到期时间；
3. WebSocket 路径客户端和服务端是否完全一致，包括开头的 `/`，多一个少一个都连不上；
4. alterId 客户端和服务端是否一致，新客户端填 0 一般没问题，如果客户端是很老的版本可能默认值不是 0，需要手动改成一致。

VMess 套 WebSocket+TLS 之后，走的是标准 HTTPS 流量，Cloudflare 这类 CDN 能正常识别转发，能在一定程度上隐藏服务器真实 IP，具体套 CDN 的思路和这篇[Vmess+WebSocket搭建中转服务器](https://vpsjq.com/2025/05/09/vmesswebsocket搭建中转服务器/)类似，只是入站协议换成了 3x-ui 面板里配置。如果客户端不需要考虑兼容老设备，直接用 VLESS Reality 会更省心，不需要自己折腾域名和证书。多用户管理可以参考[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)，给不同设备分开建用户方便管理。
