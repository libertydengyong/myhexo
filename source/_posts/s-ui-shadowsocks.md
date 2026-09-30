---
title: S-UI配置Shadowsocks，2022版加密方式密码别自己瞎填
date: 2026-09-30 14:00:00
tags:
  - S-UI教程
  - Shadowsocks
categories:
  - vps技巧
description: S-UI的Shadowsocks入站支持2022版加密方式，这几种方式的密码有固定的格式要求，直接用面板生成按钮比自己手打靠谱，顺带讲一下managed这个开关是干嘛的。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI配置Shadowsocks，2022版加密方式密码别自己瞎填",
      "description": "S-UI的Shadowsocks入站支持2022版加密方式，这几种方式的密码有固定的格式要求，直接用面板生成按钮比自己手打靠谱，顺带讲一下managed这个开关是干嘛的。",
      "datePublished": "2026-09-30T14:00:00+08:00",
      "dateModified": "2026-09-30T14:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-shadowsocks/",
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
      "name": "S-UI配置Shadowsocks节点",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建入站选择Shadowsocks",
          "text": "协议选Shadowsocks，加密方式(method)从下拉列表选一个，推荐2022-blake3-aes-128-gcm或者chacha20-ietf-poly1305。"
        },
        {
          "@type": "HowToStep",
          "name": "用面板生成密码，不要手动填",
          "text": "选完加密方式点密码框旁边的刷新图标自动生成，2022版方式对密码格式有固定要求，手动瞎填大概率连不上。"
        },
        {
          "@type": "HowToStep",
          "name": "决定是否开启managed多用户",
          "text": "managed开关决定这个入站是单一固定密码，还是交给S-UI的用户管理系统分配多个独立子密钥。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI的Shadowsocks加密方式应该选哪个？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "面板列出的选项里有none、传统AEAD方式(aes-128/192/256-gcm、chacha20-ietf-poly1305、xchacha20-ietf-poly1305)和2022版(2022-blake3开头的三个)。新装节点建议直接选2022版，是目前协议设计上比较新的一代，兼容性和安全性都不差；如果客户端比较老不支持2022版，退回chacha20-ietf-poly1305这类传统AEAD方式也可以，none基本不用，等于不加密。"
          }
        },
        {
          "@type": "Question",
          "name": "为什么2022版加密方式的密码不能自己随便填？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "2022版的密钥不是随便一串字符就行，需要是特定长度的base64编码内容(128位方式对应16字节，256位方式对应32字节)，面板选完加密方式之后密码框旁边有个刷新图标，点一下会自动生成符合格式要求的密钥，手动瞎打一串字符大概率格式不对，客户端连不上或者握手失败。传统AEAD方式对密码格式没这么严格，可以自己填好记的内容。"
          }
        },
        {
          "@type": "Question",
          "name": "managed这个开关是做什么的？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "决定这个Shadowsocks入站是单一固定密码，还是交给S-UI的用户管理系统去分配。开启之后可以像VLESS、Trojan那样给这个入站添加多个用户，每个用户有自己独立的凭据、可以单独设置流量配额和到期时间；不开启就是最基础的单密码模式，谁知道密码谁就能连，适合只给自己一个人用的场景。"
          }
        }
      ]
    }
  ]
}
</script>

面板前端的[开源代码](https://github.com/alireza0/s-ui-frontend)里能看到，S-UI 的 Shadowsocks 加密方式（method）选项比想象中要多，除了常见的几种 AEAD 加密，还包括三种 2022 版方式：`2022-blake3-aes-128-gcm`、`2022-blake3-aes-256-gcm`、`2022-blake3-chacha20-poly1305`。这是 Shadowsocks 协议这几年更新出来的新一代实现，S-UI 基于 Sing-Box 内核，对这几种新方式的支持是原生的。

## 新建入站，选加密方式

进入入站管理，新建入站，协议选 **Shadowsocks**。加密方式（method）这一栏下拉列表里能看到全部选项：

- `none` —— 不加密，基本用不上
- `aes-128-gcm` / `aes-192-gcm` / `aes-256-gcm` —— 传统 AEAD 加密
- `chacha20-ietf-poly1305` / `xchacha20-ietf-poly1305` —— 同样是传统 AEAD，性能和兼容性都不错
- `2022-blake3-aes-128-gcm` / `2022-blake3-aes-256-gcm` / `2022-blake3-chacha20-poly1305` —— 2022 版

新装节点没有兼容性顾虑的话，直接选 2022 版三选一即可；如果客户端比较老、不确定支不支持新版本，退回 `chacha20-ietf-poly1305` 这种传统 AEAD 方式更稳妥。

## 密码用生成按钮，别自己手打

选完加密方式之后，密码输入框旁边有个刷新图标（点一次会重新生成）。**2022 版加密方式对密码格式有固定要求**——本质上是特定长度的 base64 编码密钥，128 位对应的方式需要 16 字节，256 位的需要 32 字节，不是随便一串字符都能用。自己手动填一个"看起来像密码"的字符串，格式大概率不对，客户端要么直接握手失败，要么显示连接成功但实际不通。点那个刷新图标让面板自动生成，省心也不容易出错。

传统 AEAD 方式（`aes-*-gcm`、`chacha20-ietf-poly1305` 这几种）对密码格式没那么严格，自己填一个好记的字符串也没问题，这点跟 2022 版不一样。

## managed 开关：单用户还是多用户

面板里还有个 **managed** 开关（标签一般显示类似"可管理"的字样），决定这个 Shadowsocks 入站的用户模式：

- **关闭**：最基础的单密码模式，一个入站对应一个固定密码，谁知道密码谁就能用，适合自己一个人用或者不需要精细管理的场景。
- **开启**：这个入站交给 S-UI 的用户管理系统处理，可以像配置 VLESS、Trojan 那样在这个入站下面添加多个独立用户，每个用户有自己的凭据，能单独设置流量配额和到期时间，管理方式参考[S-UI面板多用户管理](https://vpsjq.com/2026/08/29/s-ui-multi-user/)。

不确定选哪个的话，只给自己用就关掉，需要分给多个人用、还要分别控制流量就打开。

## 连不上的时候

先确认防火墙端口有没有放行；再确认客户端选的加密方式跟面板完全一致，2022 版尤其要注意客户端支持不支持这个具体方式；密码确认是不是用面板生成的那一串，没有手动改动过。

Shadowsocks 的流量特征相对容易被识别，不管是 S-UI 还是 3x-ui，长期稳定使用建议还是换成抗检测能力更强的 VLESS Reality，配置方法参考[S-UI面板搭建VLESS Reality节点](https://vpsjq.com/2026/08/28/s-ui-reality/)。如果是从 3x-ui 过来的，两边配置思路和密码格式要求都一致，可以对照[3x-ui配置Shadowsocks节点及抗封锁分析](https://vpsjq.com/2026/08/31/3x-ui-shadowsocks/)里关于封锁风险的分析部分。
