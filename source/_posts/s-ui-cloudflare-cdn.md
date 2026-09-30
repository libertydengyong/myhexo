---
title: S-UI套CDN用优选IP，面板这边配置WS+TLS就够了
date: 2026-09-30 15:00:00
tags:
  - S-UI教程
  - Cloudflare
categories:
  - vps技巧
description: S-UI要套Cloudflare CDN，传输方式必须选WebSocket这类基于HTTP的类型，Reality走裸TCP没法套；优选IP这步其实全在客户端操作，跟面板设置没关系。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI套CDN用优选IP，面板这边配置WS+TLS就够了",
      "description": "S-UI要套Cloudflare CDN，传输方式必须选WebSocket这类基于HTTP的类型，Reality走裸TCP没法套；优选IP这步其实全在客户端操作，跟面板设置没关系。",
      "datePublished": "2026-09-30T15:00:00+08:00",
      "dateModified": "2026-09-30T15:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-cloudflare-cdn/",
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
      "name": "S-UI配置节点套Cloudflare CDN",
      "step": [
        {
          "@type": "HowToStep",
          "name": "入站传输方式选WebSocket",
          "text": "协议选VLESS或VMess，传输方式必须选WebSocket这类基于HTTP的类型，Reality走的是裸TCP，CDN不认识没法转发。"
        },
        {
          "@type": "HowToStep",
          "name": "绑定TLS模板并把域名解析到Cloudflare",
          "text": "域名解析改成Cloudflare的NS，橙色云朵(代理)打开，TLS证书还是用面板的证书模板流程。"
        },
        {
          "@type": "HowToStep",
          "name": "客户端里换成优选IP",
          "text": "分享链接里的地址换成一个当前对自己网络线路好的Cloudflare IP，SNI和Host保持域名不变，这一步跟面板设置无关，纯客户端操作。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "为什么Reality不能像WebSocket一样套CDN？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Reality走的是裸TCP层的TLS伪装，CDN在转发流量之前需要能识别应用层协议(HTTP/WebSocket这类)才知道怎么处理，裸TCP流量CDN没法正常代理转发。能套CDN的都是基于HTTP的传输方式，S-UI里对应WebSocket、gRPC、HttpUpgrade这几种，Reality要抗封锁走的是完全不同的思路，两者不能混着用。"
          }
        },
        {
          "@type": "Question",
          "name": "优选IP要在S-UI面板里配置吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不需要，这一步完全在客户端操作，跟面板没关系。面板这边只需要正常配置好WebSocket+TLS，域名解析到Cloudflare并开启代理。优选IP是把客户端分享链接里的连接地址换成一个当前线路好的Cloudflare IP，SNI和Host请求头保持域名不变，Cloudflare照样能根据域名把请求路由到正确的源站，这个替换只在客户端那边做。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么找到当前好用的优选IP？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "优选IP没有固定答案，不同网络运营商、不同地区、不同时间段测出来的结果都不一样，网上流传的固定IP列表大概率已经过时。比较靠谱的做法是自己用IP测速工具(比如开源的CloudflareSpeedTest)现场测一遍，选延迟低、丢包少的IP，隔一段时间重新测一次，不要长期用同一批一成不变的IP。"
          }
        }
      ]
    }
  ]
}
</script>

套 CDN 这件事，S-UI 这边要做的事情不多，大头都在客户端。先说清楚一个容易搞混的前提：**不是所有协议、传输方式都能套 CDN**，Reality 走的是裸 TCP，CDN 没法正常转发，能套 CDN 的必须是基于 HTTP 的传输方式，S-UI 里对应的是 **WebSocket**、gRPC、HttpUpgrade 这几种。

## 面板这边：入站选WebSocket+TLS

新建入站，协议选 VLESS 或者 VMess，传输方式选 **WebSocket**。这一步有几个字段：

- **path**：自定义一段路径，默认是 `/`，建议改成不好猜的字符串
- **host**：Host 请求头，一般填你的域名
- **Max Early Data** / **Early Data Header Name**：0-RTT 相关的优化选项，默认不开（值为0），不清楚具体作用的话保持默认就行，不影响基本可用性

安全选项这边选 TLS，绑定证书模板的方式和之前讲过的[Trojan配置](https://vpsjq.com/2026/09/30/s-ui-trojan/)、[SSL证书教程](https://vpsjq.com/2026/08/28/s-ui-certificate/)里一样，先建好模板再选，不用重新填证书路径。

面板这边配置完，还需要把域名解析改成 Cloudflare 的 NS，在 Cloudflare 后台把这条 DNS 记录的云朵图标点成橙色（开启代理），这样流量才会真的走 Cloudflare 的网络。

## 客户端这边：把地址换成优选IP

这是真正跟"套 CDN"直接相关的一步，而且**完全在客户端做，S-UI 面板不需要做任何额外配置**。原理是这样：Cloudflare 的边缘节点遍布全球，直接用域名连接，DNS 解析给你的可能不是延迟最低的那个节点；把连接地址换成一个手动挑选的、延迟低的 Cloudflare IP，同时保持 SNI 和 Host 请求头还是原来的域名，Cloudflare 照样能根据域名把请求路由到正确的源站，相当于自己指定了一个更快的入口。

具体操作是在客户端里编辑这个节点，把地址（address/服务器地址）那一栏从域名换成挑好的 IP，SNI 和 Host 两个字段不要动，还是填域名。

优选 IP 没有一份能一直用的固定列表，网上搜到的很多IP列表可能已经过时了，不同地区、不同运营商测出来的结果差别也很大。比较实际的做法是自己用测速工具（比较常见的开源工具是 CloudflareSpeedTest）现场测一遍，找到当前对自己网络线路真正好用的 IP，过一段时间线路状况变了再重新测一次，不要指望一份 IP 列表一劳永逸。

套了 CDN 之后节点本身的稳定性会更依赖 Cloudflare 的网络状况，不是绝对比直连更快，具体效果因人而异，先小范围测试确认真的有改善再决定要不要长期这么用。多协议、多节点混用的管理方式可以参考[S-UI面板多用户管理](https://vpsjq.com/2026/08/29/s-ui-multi-user/)。
