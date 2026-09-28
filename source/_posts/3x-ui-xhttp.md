---
title: 3x-ui配置XHTTP节点：搭配Reality怎么设置
date: 2026-09-28 16:00:00
tags:
  - 3x-ui
  - XHTTP
categories:
  - vps工具
description: 在3x-ui面板里给VLESS Reality换上XHTTP传输层的配置步骤，重点讲mode模式怎么选、flow字段要不要填——这是很多教程都写错的一个细节。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui配置XHTTP节点：搭配Reality怎么设置",
      "description": "在3x-ui面板里给VLESS Reality换上XHTTP传输层的配置步骤，重点讲mode模式怎么选、flow字段要不要填——这是很多教程都写错的一个细节。",
      "datePublished": "2026-09-28T16:00:00+08:00",
      "dateModified": "2026-09-28T16:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/28/3x-ui-xhttp/",
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
      "name": "3x-ui配置XHTTP+Reality节点",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建入站选择VLESS+Reality",
          "text": "协议选VLESS，安全选项选Reality，dest、serverName、密钥这些Reality基础配置照常填。"
        },
        {
          "@type": "HowToStep",
          "name": "传输方式选XHTTP并填path",
          "text": "Transport一栏选XHTTP，path自定义一段不好猜的字符串，其他字段留默认即可。"
        },
        {
          "@type": "HowToStep",
          "name": "选择mode模式",
          "text": "默认auto一般够用，兼容性要求最高选packet-up，追求效率且服务器/反代支持的话选stream-up。"
        },
        {
          "@type": "HowToStep",
          "name": "确认flow留空并获取分享链接",
          "text": "XHTTP不需要也不支持flow字段，留空即可，保存后点二维码获取vless://分享链接。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "XHTTP要不要填flow=xtls-rprx-vision？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不要填，留空即可。网上不少教程会照抄普通VLESS+Reality的配置把flow也填上，但Vision解决的是裸TCP层面的TLS握手时序特征问题，XHTTP从应用层用HTTP请求包装流量，走的是完全不同的思路，两者不是配套使用的东西，Xray-core官方关于XHTTP的完整文档里也没有提到flow字段。"
          }
        },
        {
          "@type": "Question",
          "name": "XHTTP的mode应该选哪个？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不确定就用默认的auto。如果套了CDN或者反代软件不确定支不支持流式上传，选packet-up兼容性最强；如果服务器和反代都能配合（比如Nginx改用grpc_pass），选stream-up效率更高；stream-one上下行共用一条连接，效果上接近普通VLESS套了层HTTP包装。"
          }
        },
        {
          "@type": "Question",
          "name": "XHTTP比普通的Reality（裸TCP+Vision）有什么优势？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "普通Reality走裸TCP，长时间维持一条加密长连接，这种稳定的流量模式本身也是一种可被统计分析识别的特征；XHTTP把流量拆成一个个HTTP请求，行为上更接近正常的网页浏览或下载，抗流量分析的思路不一样。代价是配置项更多、部分模式对服务器和反代软件有额外要求，追求配置简单可以继续用裸TCP+Vision的Reality。"
          }
        }
      ]
    }
  ]
}
</script>

面板部分假设已经按[3x-ui安装教程](https://vpsjq.com/2026/04/30/2026-04-30-011/)装好，Reality 基础配置（dest、serverName、密钥生成）可以参考[3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)，这篇不重复讲那部分，只讲多出来的 XHTTP 传输层怎么配。

XHTTP 是 Xray-core 里比较新的一种传输方式，思路跟裸 TCP 不一样：裸 TCP + Reality 靠一条长时间维持的加密连接伪装成真实网站的 TLS 握手，本身这种"长连接、稳定时序"的流量模式也是可以被统计分析盯上的特征；XHTTP 换了个思路，把代理流量拆成一个个真实的 HTTP 请求（能流式收发数据，不会牺牲下行速率），行为上更接近正常的网页浏览或者文件下载，同时天然支持套 CDN。

## 新建入站，协议和安全层照常配

进入面板**入站列表**，点**添加入站**，协议选 **VLESS**，安全选项选 **Reality**，dest、serverName、shortId、publicKey/privateKey 这些照 [VLESS Reality教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/) 里的方法填就行，这部分两种传输方式共用，没有区别。

## Transport 选 XHTTP

关键的区别在**传输方式（Transport）**这一栏，默认是 `RAW`（也就是裸 TCP），改选 **XHTTP**。

XHTTP 的配置项看着不少，但官方文档原话是"一般来说 XHTTP 配置只需填 path，其它不填即可"——大部分场景真不需要动额外参数：

- **path**：自定义一段不好猜的字符串，比如 `/a1b2c3-xh`，不要用默认的 `/`。
- **host**：留空即可，面板会自动处理，非要自定义 Host 头的场景才需要填。
- 其余的 `xPaddingBytes`（包大小随机填充）、`xmux`（连接复用参数）都有兼顾兼容性和抗特征识别的默认值，不清楚具体含义的话不建议手动改。

## mode 怎么选

Transport 展开后有个 **mode** 字段，几个选项分别是：

- **auto**（默认）：客户端会根据情况自动选——用 TLS 时倾向 stream-up，用 Reality 时倾向 stream-one，其他情况用 packet-up。大部分人直接用这个就行。
- **packet-up**：兼容性最强的模式，穿透各种 CDN、反代软件的能力最好。如果你的节点套了 CDN，或者不确定中间的反代软件支不支持流式上传，选这个最保险。
- **stream-up**：上下行都是流式的，效率比 packet-up 更高，但对服务端有要求——用 Nginx 反代的话，要把 `proxy_pass` 改成 `grpc_pass` 才能正常穿透；套 Cloudflare 的话，需要在 CF 面板里开启 gRPC 支持。
- **stream-one**：上下行共用一条连接，效果上比较接近普通 VLESS 套了层 HTTP 包装，兼容性和 stream-up 接近。

不确定选哪个的话，先用 auto，遇到连不上或者速度异常再按上面的场景换成具体的模式测试。

## flow 字段留空，不要填 xtls-rprx-vision

这是最容易抄错的一个地方。普通裸 TCP + Reality 的配置里，flow 通常会填 `xtls-rprx-vision` 来解决 TLS 握手时序特征的问题；但换成 XHTTP 之后，**flow 留空就行，不要照抄裸 TCP 那一套填 vision**。

原因是两者解决的是不同层面的问题：Vision 是在裸 TCP 层面调整 TLS 握手的时序特征，XHTTP 是在应用层把流量包装成一个个 HTTP 请求，从设计上就是两条不同的技术路线，不是搭配使用的关系。Xray-core 官方那篇详细说明 XHTTP 原理和参数的文档里，通篇没有提到 flow 字段，也从侧面印证了这一点。网上能搜到一些教程把两者混着写，属于以讹传讹。

## 获取分享链接并导入客户端

配置保存之后，在入站列表找到这条记录，点二维码图标获取 `vless://` 开头的分享链接，链接里已经包含 XHTTP 的 path、mode 等参数。客户端这边，NekoBox、sing-box、v2rayN 目前主流版本都已经支持 XHTTP 传输，导入链接后不需要额外配置。

如果导入后连不上，按这个顺序排查：

1. 先确认裸 Reality 部分本身没问题——dest、publicKey、shortId 有没有填错，参考 [VLESS Reality教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)里的排查方法；
2. 客户端和面板的 path 是否完全一致，大小写、开头的 `/` 都要对上；
3. 如果套了 CDN 或者 Nginx 反代，确认 mode 选的是 packet-up（兼容性最强），Nginx 反代还要检查 `proxy_pass` 有没有改成 `grpc_pass`；
4. 确认 flow 字段是空的，填了 `xtls-rprx-vision` 的话客户端可能直接连不上。

如果不想折腾这么多传输层参数，直接用裸 TCP + Reality 也完全够用，配置更简单，参考前面链接的那篇教程即可。多用户管理的方式两种传输方式通用，具体看[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)。
