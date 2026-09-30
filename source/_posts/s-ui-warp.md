---
title: S-UI配置WARP出站，注册这步是面板自动做的
date: 2026-09-30 23:30:00
tags:
  - S-UI教程
  - WARP
categories:
  - vps技巧
description: S-UI创建WARP这个Endpoint时不需要自己拿wgcf之类的工具单独注册账号，保存的那一刻面板后端会直接调用Cloudflare的注册接口自动完成。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI配置WARP出站，注册这步是面板自动做的",
      "description": "S-UI创建WARP这个Endpoint时不需要自己拿wgcf之类的工具单独注册账号，保存的那一刻面板后端会直接调用Cloudflare的注册接口自动完成。",
      "datePublished": "2026-09-30T23:30:00+08:00",
      "dateModified": "2026-09-30T23:30:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-warp/",
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
      "name": "S-UI配置WARP出站",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建Endpoint选择Warp类型",
          "text": "进入Endpoints管理，新建一个类型为Warp的条目，不需要预先准备任何密钥或账号信息。"
        },
        {
          "@type": "HowToStep",
          "name": "直接保存，面板自动完成注册",
          "text": "什么都不用填直接保存，面板后端会调用Cloudflare的官方注册接口，生成一对新的密钥并注册成免费WARP账号。"
        },
        {
          "@type": "HowToStep",
          "name": "在路由规则里把出站指向这个Endpoint",
          "text": "注册完成后回到这个Endpoint能看到设备信息，之后在Rules里把需要走WARP的流量出站指定成这个Endpoint即可。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI配置WARP需要提前用wgcf之类的工具注册账号吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不需要。翻过S-UI后端源码，注册WARP账号这一步是面板自己完成的——新建Warp类型的Endpoint保存时，后端会直接生成一对新的WireGuard密钥，调用Cloudflare官方的注册接口拿到设备ID、访问令牌和节点信息，不需要用户提前用wgcf或者其他工具单独注册好再把密钥抄进来。"
          }
        },
        {
          "@type": "Question",
          "name": "WARP在S-UI里为什么归在Endpoints而不是Outbounds？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "这是S-UI基于Sing-Box内核的架构设计，Endpoint和Outbound是两个不同的概念，Endpoint更像是一个独立注册、有自己身份信息的网络端点，WireGuard/WARP这类需要先完成密钥交换和注册流程的类型都归在这里，创建好之后可以在路由规则里像使用普通出站一样引用它。"
          }
        },
        {
          "@type": "Question",
          "name": "WARP出站有什么用？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "最常见的用途是给纯IPv4的服务器额外套一层IPv6出口，或者反过来，也有人用来给某些对Cloudflare网络环境友好的服务分流。免费版WARP本身不是用来加速或者解锁全球流媒体的工具，主要解决的是IP协议栈缺失和小范围风控绕过这类需求。"
          }
        }
      ]
    }
  ]
}
</script>

配置 WARP 之前先说个容易被忽略的省心点：**S-UI 不需要自己额外用 wgcf 这类工具单独注册 WARP 账号再把密钥抄进面板**。翻了一下[官方后端源码](https://github.com/alireza0/s-ui)才确认，这个注册步骤面板自己全包了。

## 新建Warp类型的Endpoint

进入面板的 **Endpoints** 管理，新建一个条目，类型选 **Warp**。这时候表单是空的，不需要预先准备任何密钥、Device ID 或者账号信息，直接保存。

保存的这一刻，面板后端会做几件事：生成一对新的 WireGuard 密钥，拿公钥去调用 Cloudflare 官方的注册接口（`api.cloudflareclient.com`），注册成一个全新的免费 WARP 账号，把返回的设备 ID、访问令牌、节点公钥和分配到的 IP 地址都存下来。整个过程跟你手动用 wgcf 注册再复制粘贴密钥的效果一样，只是全自动，不需要在面板外面单独操作。

## 注册完成后能看到什么

保存成功、再打开这个 Endpoint 的时候，界面上会显示注册回来的信息：Device ID、Access Token、本机私钥、分配到的本地 IP，以及对端（Cloudflare 服务器）的公钥、允许的 IP 段这些参数。正常情况下这些字段不需要手动改动，出问题需要重新注册的话，删掉这个 Endpoint 重建一个新的就行，不需要在这些字段里排查密钥对不对。

下面还有几个可选参数：

- **UDP Timeout**：UDP 连接的超时时间，默认关闭不显示，需要的话打开开关手动填
- **Workers**：WireGuard 处理线程数，机器性能一般的话不用改
- **MTU**：数据包最大传输单元，网络环境特殊（比如套了别的隧道）导致丢包严重时可以试着调小
- **System Interface**：是否创建成系统级网络接口，一般场景不需要开启，保持默认的用户态实现就够用

## 怎么用起来

Endpoint 建好只是完成了"这个出口存在"这一步，还需要在路由规则（Rules）里把想要走 WARP 的流量指定到这个 Endpoint 上才会真正生效，这部分是 S-UI 分流规则的配置范畴，思路上跟给普通出站分流一样，只是出站目标换成了这个 WARP Endpoint。

WARP 免费版本身不是拿来加速或者解锁流媒体的，比较实际的用途是给纯 IPv4 的服务器加一层 IPv6 访问能力，或者反过来，具体效果因人而异，建议先在小范围测试确认符合预期再大范围应用。如果用的是 3x-ui，配置思路和面板操作方式不一样，可以参考[3x-ui配置Warp给服务器添加IPv4/IPv6出口](https://vpsjq.com/2026/08/30/3x-ui-warp/)。
