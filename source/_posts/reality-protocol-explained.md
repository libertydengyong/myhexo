---
title: Reality协议是什么：不用域名和证书的伪装原理、必备参数和常见坑
date: 2026-10-07 15:00:00
tags:
  - Reality
  - VLESS
  - Xray
categories:
  - vps工具
description: Reality是对TLS的一种修改，借用别人网站的TLS握手来伪装，自己不需要域名和证书。依据XTLS/REALITY项目说明和Xray官方文档，讲清楚它的原理、target、serverNames、shortId、password等参数，以及选目标网站和配置时的常见坑。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Reality协议是什么：不用域名和证书的伪装原理、必备参数和常见坑",
      "description": "Reality是对TLS的一种修改，借用别人网站的TLS握手来伪装，自己不需要域名和证书。依据XTLS/REALITY项目说明和Xray官方文档，讲清楚它的原理、target、serverNames、shortId、password等参数，以及选目标网站和配置时的常见坑。",
      "datePublished": "2026-10-07T15:00:00+08:00",
      "dateModified": "2026-10-07T15:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/reality-protocol-explained/",
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
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Reality协议是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Reality是Xray里的一种传输安全方案，官方文档的说法是它对TLS做了修改，通过借用目标站点的TLS外观和握手特征来完成伪装。它不需要服务端自己有域名和证书，常和VLESS协议以及xtls-rprx-vision流控搭配使用。"
          }
        },
        {
          "@type": "Question",
          "name": "用Reality需要自己的域名和证书吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不需要。REALITY项目的说明写的是它可以指向别人的网站，无需自己买域名、配置TLS服务端。服务端配置里要填的是借用的目标站点target和对应的serverNames。"
          }
        },
        {
          "@type": "Question",
          "name": "Reality可以和哪些传输方式一起用？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Xray官方文档写明REALITY仅支持与RAW、XHTTP、gRPC三种传输方式组合使用。"
          }
        }
      ]
    }
  ]
}
</script>

搜"reality 协议"的人，多半在配置教程里看到了 `dest`、`serverNames`、`shortIds`、`publicKey` 这些字段，却不知道它们是干什么的。这篇不讲面板上怎么点，先把原理和每个参数的含义讲清楚，再说选目标网站和配置时容易踩的坑。具体的面板配置步骤，可以接着看本站的 [3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)。

先说明依据：下面的内容来自 [XTLS/REALITY](https://github.com/XTLS/REALITY) 项目的说明、Xray 官方文档仓库里的 REALITY 页面（文档站 xtls.github.io 在我这里打不开，我读的是文档仓库里的同一份源文件），以及 3x-ui 官方文档里的 REALITY 页面。我没有自己搭建和抓包验证过，文中凡是"官方说"的话，都是转述；任何伪装方案都不能保证永远不被识别或封锁，这一点官方文档也没有做这种保证。

<!-- more -->

## 一句话：它是什么

Xray 官方文档对它的定义是：**REALITY 是对 TLS 的一种修改，通过借用目标站点的 TLS 外观与握手特征来完成伪装。**

换成大白话：普通的 TLS 代理，服务器要自己有一个域名和一张证书，别人一看就知道"这是个陌生域名的 TLS 服务"。REALITY 的做法是，让你的服务器在握手时看起来像是在和一个**真实的、知名的网站**（也就是 `target`）通信，自己不需要域名和证书。

官方文档还有两点说明：

- 它**仅支持与 RAW、XHTTP、gRPC 三种传输方式组合使用**；
- 官方文档的提示称，启用 REALITY 并配上合适的 XTLS Vision 流控，性能可以有数倍甚至十几倍的提升（这是官方的说法，我没有测过）。

## 它和普通 TLS 有什么区别

XTLS/REALITY 项目的说明里列了几点，我只转述，不加评价：

- 用 REALITY 取代 TLS，**可以消除服务端的 TLS 指纹特征**，并且仍有前向保密性；
- 它的说明认为，证书链攻击对它无效；
- **可以指向别人的网站**，不需要自己买域名、配置 TLS 服务端；
- 实现的效果是向中间人呈现指定 SNI 的全程真实 TLS。

| | 普通 TLS 代理 | REALITY |
| --- | --- | --- |
| 域名和证书 | 需要自己的域名和证书 | 不需要，借用目标站点 |
| 握手看起来像 | 一个陌生域名的 TLS 服务 | 一个真实的知名网站 |
| 服务端要配置的 | 域名、证书、私钥 | 目标站点、SNI 列表、密钥对、shortId |

## 工作原理：认证通过走代理，认证失败转给真网站

按 REALITY 项目说明，大致流程是：

1. 客户端发起一个看起来正常的 TLS 握手，里面带着 REALITY 的认证信息（用到的就是后面讲的密钥和 shortId）；
2. 服务端**验证通过**，就把这条连接当作代理流量处理，客户端会收到一张由"临时认证密钥"签发的**临时可信证书**；
3. 服务端**验证不通过**（比如是别人在探测），Xray 会把这条流量**直接转发给 `target` 那个真实网站**，对方看到的就是目标网站的真实响应。

项目说明里提到，客户端有三种情况会收到目标网站的真证书：服务端拒绝了客户端的握手、握手被中间人重定向到目标网站、遭遇中间人攻击。REALITY 客户端能区分临时可信证书、真证书和无效证书：收到临时可信证书，连接可用；收到真证书，进入"爬虫模式"；收到无效证书，直接断开。

这里有一个官方文档特别提醒的地方：认证失败的流量会被**直接转发**到 `target`。如果目标网站的 IP 比较特殊（比如用了 Cloudflare CDN 的网站），相当于你的服务器给对方做了端口转发，被人扫描后可能偷跑流量。官方给的办法是前置 Nginx 过滤掉不符合要求的 SNI，或者用 `limitFallbackUpload`、`limitFallbackDownload` 限速；同时官方又说回落限速本身是一种特征，不建议随便启用，写面板或一键脚本的人要让这些参数随机化。

## 要配哪些参数

Xray 文档里的参数分服务端和客户端两边。下面按 Xray 当前文档的叫法列出，括号里是旧叫法，教程和面板里常见：

| 参数 | 在哪一端 | 含义 |
| --- | --- | --- |
| `target`（旧称 `dest`） | 服务端 | 要借用的目标网站，写成 `域名:端口`，如 `example.com:443`。文档说当前版本两个字段互为别名 |
| `serverNames` | 服务端 | 客户端可以使用的 SNI 列表，不支持 `*` 通配符，一般和 `target` 保持一致 |
| `privateKey` | 服务端 | 服务端私钥，用 `xray x25519` 生成 |
| `shortIds` | 服务端 | 客户端可用的 shortId 列表，用来区分不同客户端 |
| `serverName` | 客户端 | 服务端 `serverNames` 里的一个 |
| `password`（旧称 `publicKey`） | 客户端 | 服务端私钥对应的公钥，用 `xray x25519 -i "服务端私钥"` 得到 |
| `shortId` | 客户端 | 服务端 `shortIds` 里的一个 |
| `fingerprint` | 客户端 | 用 uTLS 模拟的客户端 TLS 指纹，默认 `chrome` |
| `spiderX` | 客户端 | 爬虫初始路径和参数，官方建议每个客户端不同 |
| `flow` | 两端一致 | 一般是 `xtls-rprx-vision` |

几个容易搞错的细节，都来自官方文档：

- **`password` 就是旧的 `publicKey`**。文档说改名是为了防止误解：它在地位上是 x25519 公钥，但在 REALITY 的设计里是**由客户端持有、不能公开**的东西。所以教程里说"只把公钥给客户端，私钥留在服务器"，和这个说法并不矛盾，意思是别把服务端私钥泄露出去。
- **`shortId`** 是 0 到 f 组成的十六进制字符串，长度必须是**偶数**，上限 16 位。比如 `aa1234` 会被自动补成 `aa12340000000000`，但 `aaa1234`（7 位）会报错。如果服务端 `shortIds` 里有空字符串，客户端的 `shortId` 也可以为空。
- **`fingerprint`** 在 REALITY 里不支持用 `unsafe` 关掉 uTLS，因为 REALITY 的实现要靠这个库操作底层 TLS 参数。
- `target` 字段只填在**服务端**，官方文档说核心靠这个字段是否存在来区分当前是服务端还是客户端配置，客户端不要填，否则会识别异常。

除此之外还有 `minClientVer`、`maxClientVer`、`maxTimeDiff`、`mldsa65Seed`（后量子签名）等可选项，普通使用用不到，不展开。

分享链接里这些参数对应成了 `vless://` 链接的字段，3x-ui 官方文档的说明是：`pbk` 是公钥，`sid` 是 shortId，`sni` 是服务器名，`fp` 是客户端指纹，`spx` 是 spiderX，`flow` 是流控。导入客户端时，链接各参数怎么对应，可以参考 [Hysteria2客户端怎么导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/) 里讲链接结构的思路。

## 目标网站怎么选

这是最影响效果的一步。XTLS/REALITY 项目说明给出的标准是：

**最低要求**：国外网站，支持 TLS 1.3 和 H2（HTTP/2），域名**不是用来跳转的**（主域名可能被用来跳转到 `www`，所以要选实际提供服务的那个域名）。

**加分项**：

- IP 和你的服务器相近（更像，延迟也低）；
- 在 Server Hello 之后的握手消息也一起加密（项目说明举的例子是 dl.google.com）；
- 支持 OCSP Stapling。

**配置层面的加分项**：禁止回国流量，TCP/80 和 UDP/443 也一并转发，因为 REALITY 对外表现就是端口转发，目标 IP 偏冷门或许更好。

Xray 文档还有一条实用建议：REALITY 的最佳实践是**偷同 ASN 的证书**（也就是和你的服务器同一个网络运营方的网站）。文档接着说，照这个做的话，大概率就用不到前面提到的回落限速功能了。

选好之后，可以用 `xray tls ping 域名` 检查目标网站的响应情况。文档还提到：如果目标支持后量子密钥交换算法 X25519MLKEM768，REALITY 客户端也会自动用它协商，是否支持同样用 `xray tls ping` 查看。

## 为什么总和 XTLS Vision 一起出现

REALITY 只负责"握手伪装"这一层。项目说明提到，REALITY 也可以搭配 XTLS 以外的代理协议，**但不建议这样做**，因为它们存在明显且已被针对的 TLS in TLS 特征。所以教程里一般是 **VLESS + REALITY + `xtls-rprx-vision`** 这个组合，`flow` 在服务端的用户配置和客户端链接里要一致。

## 配置时最常见的坑

下面这些来自 3x-ui 官方文档和 Xray 官方文档：

- **目标网站选错**：必须是真实、可访问、支持 TLS 1.3 和 H2、没有在你所在地区被屏蔽的网站，最好是你不拥有、流量很大的网站。
- **SNI 和目标证书不匹配**：`serverNames` 要和目标网站真实证书里的名字对得上，否则握手会暴露伪装。一般参考目标返回证书的 SAN。
- **`flow` 不一致**：REALITY 配 XTLS Vision，服务端用户和分享链接里都要是 `xtls-rprx-vision`。
- **服务端私钥泄露**：`privateKey` 只能留在服务器上。
- **客户端版本限制**：3x-ui 文档提到，Xray-core 某些版本对"最低客户端版本"有内置值，可能拒绝第三方客户端，即使密钥都对；新版本里留空时不再设最低版本，但如果你明确保存过一个最低版本，它仍然生效。遇到连不上，要看服务端 Xray 内核的实际版本。
- **Mihomo（Clash）与后量子**：3x-ui 文档里有一条：新版 Xray 内核要求握手里带 `X25519MLKEM768` 密钥交换；Clash/Mihomo 订阅里会为 REALITY 节点打开 `support-x25519mlkem768`，指纹留空时用 `chrome`；如果你显式指定了不支持 ML-KEM 的老指纹，不会被自动改掉。这条涉及具体内核版本号，我没有逐版本验证，遇到 Mihomo 连不上可以先查这一条。

## 什么时候用 Reality

- 你**没有域名**，或者不想为代理单独买域名、配证书，REALITY 是常见选择；
- 你想用 TCP 协议（RAW、XHTTP、gRPC 这几种传输）并且追求伪装度。

如果你更在意高丢包线路上的速度，可以看 [Hysteria2节点的优点和缺点是什么？和VLESS Reality、TUIC怎么选](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)；Reality 搭配 XHTTP 的做法见 [3x-ui配置XHTTP节点：搭配Reality怎么设置](https://vpsjq.com/2026/09/28/3x-ui-xhttp/)。

## 想直接动手配

- 面板里一步步配置：[3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)、[S-UI面板搭建VLESS Reality节点](https://vpsjq.com/2026/08/28/s-ui-reality/)；
- 想知道 3x-ui 是什么、官方入口在哪：[3x-ui是什么？](https://vpsjq.com/2026/10/04/3x-ui-what-is-github-docs/)；
- 想直接改 Xray 配置：[3x-ui的Xray配置模板在哪改](https://vpsjq.com/2026/10/04/3x-ui-xray-config-template/)。

## 小结

- REALITY 是对 TLS 的修改，借用目标站点的握手来伪装，服务端不需要自己的域名和证书；
- 认证通过的走代理，认证失败的会被转发给目标网站，所以目标网站的选择很关键；
- 参数新旧叫法对照：`dest` 对应 `target`，`publicKey` 对应 `password`；`shortId` 要偶数位、最多 16 位；
- 仅支持和 RAW、XHTTP、gRPC 搭配，通常配 VLESS 和 `xtls-rprx-vision`；
- 本文是转述官方说明，我没有自己搭建和抓包验证，任何伪装方案都不保证永不被识别。
