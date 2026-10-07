---
title: v2rayNG、Hiddify、Mihomo能导入Hysteria2和Reality吗：各自支持什么，源码和文档里能确认的
date: 2026-10-07 16:00:00
tags:
  - v2rayNG
  - Hiddify
  - Mihomo
  - Hysteria2
  - Reality
categories:
  - vps工具
description: 依据v2rayNG源码、Hiddify源码和README、Mihomo官方文档，逐个确认这三个客户端对Hysteria2和Reality链接的支持情况、能读取哪些参数、怎么导入，以及Reality版本不兼容时要注意什么。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "v2rayNG、Hiddify、Mihomo能导入Hysteria2和Reality吗：各自支持什么，源码和文档里能确认的",
      "description": "依据v2rayNG源码、Hiddify源码和README、Mihomo官方文档，逐个确认这三个客户端对Hysteria2和Reality链接的支持情况、能读取哪些参数、怎么导入，以及Reality版本不兼容时要注意什么。",
      "datePublished": "2026-10-07T16:00:00+08:00",
      "dateModified": "2026-10-07T16:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/v2rayng-hiddify-mihomo-hysteria2-reality/",
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
          "name": "v2rayNG能导入Hysteria2链接吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "能。我读到的v2rayNG源码里，协议类型包含HYSTERIA2，导入时同时识别hysteria2://和hy2://两种链接，也可以在添加菜单里手动添加Hysteria2。它会读取链接里的密码、sni、alpn、insecure、obfs-password、mport端口跳跃和pinSHA256证书指纹。"
          }
        },
        {
          "@type": "Question",
          "name": "Hiddify支持Reality和Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Hiddify的README写它基于sing-box，协议支持列表里有Vless、Vmess、Reality、TUIC、Wireguard、Hysteria、SSH，写的是Hysteria没有单独写2。我读到的应用源码里，代理类型枚举有Hysteria2，导入解析也识别hy2://和hysteria2://链接。实际连接由sing-box内核处理，那部分在另一个子模块仓库里，我没有读。"
          }
        },
        {
          "@type": "Question",
          "name": "Mihomo是客户端吗？它支持Hysteria2和Reality吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Mihomo是内核，不是带界面的应用。官方文档里有hysteria2类型的节点配置（server、port、password、sni、obfs等字段），VLESS节点的reality-opts里有public-key、short-id等字段，所以YAML里能配置这两种。要注意Mihomo文档对较新的Xray内核版本的Reality兼容性有明确的警告。"
          }
        }
      ]
    }
  ]
}
</script>

搜 Hysteria2、Reality 的人，常会连带搜 v2rayNG、Hiddify、Mihomo，想确认的其实是同一件事：**我手上这个客户端，能不能导入我的 Hysteria2 链接或 Reality 链接？** 这篇不教具体点哪里，只把源码和官方文档里能确认的事实摆出来：支持不支持、能读哪些参数、有什么限制。

先说明依据和范围：我读了 [2dust/v2rayNG](https://github.com/2dust/v2rayNG) 的源码（最新提交 2026-10-06）、[hiddify/hiddify-app](https://github.com/hiddify/hiddify-app) 的 README 和应用源码（最新提交 2026-10-07），以及 Mihomo 官方文档仓库里关于 hysteria2、vless 和 tls 的页面。**我没有在手机或电脑上实际安装和导入验证过**，所以下面说的"能"，指的是源码或文档里写明了支持，不等于我亲手连成功过。凡是没读到的部分（比如 Hiddify 的内核），都会标明。

<!-- more -->

## 先看结论

| | v2rayNG | Hiddify | Mihomo |
| --- | --- | --- | --- |
| 是什么 | Android 客户端 | 多平台客户端 | 内核，不带界面 |
| 内核 | Xray core 或 v2fly core | sing-box | Mihomo 自己 |
| 平台 | Android（minSdk 24，即 Android 7.0 及以上） | Android、iOS、Windows、macOS、Linux（README） | 取决于你用的外壳 |
| Hysteria2 | 源码里有，识别 hysteria2:// 和 hy2:// | README 写的是 Hysteria；源码里有 Hysteria2 类型并识别两种链接 | 文档里有 hysteria2 节点配置 |
| Reality | 能读 pbk、sid、spx 等参数 | README 的协议列表里有 Reality | 文档里 VLESS 的 reality-opts |
| 怎么导入 | 扫码、剪贴板、本地文件、手动添加、订阅 | 订阅链接和多种配置格式 | 写 YAML 配置 |

## v2rayNG：Hysteria2 和 Reality 都能读

v2rayNG 的 README 对自己的定位是：Android 上的 V2Ray 客户端，支持 Xray core 和 v2fly core；电脑版是另一个项目 v2rayN。许可证是 GPL v3。

按源码，我能确认这几点：

**1. 协议类型里有 Hysteria2。** 配置类型的枚举里有 `VMESS`、`SHADOWSOCKS`、`SOCKS`、`VLESS`、`TROJAN`、`WIREGUARD`、`HYSTERIA2`、`HYSTERIA`、`HTTP` 等，其中 TUIC 在源码里被注释掉了，说明当前版本没有启用它。

**2. 导入时同时识别两种 hy2 链接。** 解析表里 `hysteria2://` 和 `hy2://` 都对应 Hysteria2 的解析函数。解析时会读取：

| 链接参数 | 含义 |
| --- | --- |
| `用户信息@服务器:端口` | 密码、服务器和端口 |
| `sni`、`alpn` | 证书服务器名、ALPN |
| `insecure`（也认 `allowInsecure`、`allow_insecure`） | 值为 1 就当作允许不安全证书 |
| `obfs-password` | 混淆密码（导出时会把 `obfs` 写成 `salamander`） |
| `mport` | 端口跳跃范围 |
| `pinSHA256` | 证书指纹 |

所以 [Hysteria2客户端怎么导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/) 里讲的那些参数，v2rayNG 大部分都认。

**3. Reality 参数能读。** 解析 VLESS 等链接的通用代码里，`security` 只接受 `tls` 和 `reality` 两种，`pbk`（公钥）、`sid`（shortId）、`spx`（spiderX）、`fp`（指纹）、`flow`（流控）、`sni` 都会读取，另外还有 `pqv`（后量子验证公钥）。Reality 各字段的含义，见 [Reality协议是什么](https://vpsjq.com/2026/10/07/reality-protocol-explained/)。

**4. 导入方式。** 添加配置的菜单里有：扫描二维码、从剪贴板导入、从本地导入，以及手动添加 VMess、VLESS、Shadowsocks、SOCKS、HTTP、Trojan、WireGuard、Hysteria2，还有"策略组"和"链式代理"。源码里也有订阅更新的模块。

## Hiddify：基于 sing-box，协议列表里写的是 Hysteria

Hiddify 的 README 说它是基于 sing-box 的多平台代理客户端，支持 Android、iOS、Windows、macOS 和 Linux。README 里的协议支持写的是："Vless、Vmess、Reality、TUIC、Wireguard、Hysteria、SSH"，订阅和配置格式支持 "Sing-box、V2ray、Clash、Clash meta"。

要注意 README 写的是 **Hysteria**，没有明确写"Hysteria2"。我在应用源码里补查了：

- 代理类型的枚举里同时有 `hysteria` 和 `hysteria2`；
- 导入时识别链接名称的代码，`hy2`、`hysteria2` 都归到 Hysteria2，`hy`、`hysteria` 归到 Hysteria；
- 同一份枚举里还有 VLESS、VMess、Trojan、TUIC、WireGuard、SSH 等。

所以从应用这一层看，Hysteria2 是被认出来的。但**真正解析链接参数、建立连接的是 sing-box 内核**，它在一个单独的子模块仓库（`hiddify-core`）里，我没有读，所以 hy2 链接里的 `obfs`、`mport`、`pinSHA256` 这些参数它具体认哪些，我这里没法确认。Reality 同理，只能依据 README 说它支持。

另外一个值得知道的点：Hiddify 的许可证是 "Hiddify Extended GPL v3"，在 GPL v3 之上加了附加条件，包括要求公开源码、保留署名、**仅限非商业使用**等。自己用不受影响，但如果你想基于它二次开发，要先看 `LICENSE.md`。

## Mihomo：是内核，不是应用

Mihomo 的 README 把自己叫 "Meta Kernel"，功能列表里写着 VMess、VLESS、Shadowsocks、Trojan、Snell、TUIC、Hysteria 协议支持。它本身没有界面，你要用它，是通过各种带界面的外壳，或者在路由器上跑（站内 [Hysteria2客户端怎么选](https://vpsjq.com/2026/10/02/hysteria2-platform-clients/) 里讲过 OpenClash）。官方文档给的配置写法都是 YAML。

**Hysteria2**：官方文档里有 `type: hysteria2` 的节点，字段包括：

| 字段 | 含义 |
| --- | --- |
| `server`、`port`、`password` | 服务器、端口、认证密码 |
| `ports`、`hop-interval` | 端口跳跃的端口范围和间隔（秒，默认 30） |
| `up`、`down` | brutal 速率控制，不写单位默认 Mbps |
| `obfs`、`obfs-password` | 混淆类型（文档写支持 salamander 和 gecko）和密码 |
| `sni`、`skip-cert-verify`、`alpn` | 证书相关 |
| `fingerprint` | 证书指纹，文档说配置后能起到 SSL Pinning 的效果 |

链接里的 `insecure=1` 大致对应 YAML 里的 `skip-cert-verify: true`，`pinSHA256` 看起来对应 `fingerprint`，这是我按字段含义做的对应，没有逐项验证。Mihomo 从哪个版本开始支持 Hysteria2，我在站内 [Clash报unsupported proxy type hysteria2怎么办](https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/) 里已经写过，这里不重复。

**Reality**：在 `type: vless` 的节点里，用 `reality-opts` 配置，有 `public-key` 和 `short-id`，还有 `support-x25519mlkem768`（支持 X25519-MLKEM768 密钥交换）；`client-fingerprint` 可以选 `chrome`、`firefox`、`safari` 等；`flow` 写 `xtls-rprx-vision`。

## 用 Reality 连不上时，先看版本

Reality 这块，Mihomo 官方文档里有一条**明确的警告**：由于 Xray-core 有意做的不兼容改动，Mihomo **不会考虑 Xray v26.7.11 及以上版本的兼容性**；如果连不上，建议换服务端（比如 Mihomo 自己的 listener、sing-box 或旧版 Xray-core），或者换用别的协议。

而 3x-ui 官方文档里的说法是另一个角度：新版 Xray 内核（v26.9.8 起）要求握手里带 `X25519MLKEM768` 密钥交换，Clash/Mihomo 订阅里会为 Reality 节点自动打开 `support-x25519mlkem768`。

这两份文档来自不同的项目、不同的时间点，我**没有实测过它们的组合到底能不能连**。可以确定的是：Reality 在新版服务端内核和 Mihomo 之间存在已知的兼容问题，遇到连不上，别只检查密钥和 shortId，要同时看服务端 Xray 内核的版本和客户端内核的版本。3x-ui 面板生成 Clash 订阅的做法见 [3x-ui订阅链接导入Clash for Android方法](https://vpsjq.com/2026/08/30/3x-ui-clash/)。

## 怎么选

我只能按源码和文档里确认的信息给方向，不替你背书某个具体应用：

- **Android，想直接导入链接**：v2rayNG 对 hy2 和 Reality 链接的读取，源码里写得很明确；
- **想要一个跨平台的客户端**：Hiddify 的 README 写明有 Android、iOS、Windows、macOS、Linux，基于 sing-box；它对 Hysteria2 的支持细节我没能确认；
- **用 Clash 系的订阅或路由器上的 OpenClash**：要看你的外壳用的是不是 Mihomo 内核，以及 Mihomo 和服务端的内核版本是否匹配；
- 电脑上用 v2rayN 的话，v2rayNG 的 README 说它是电脑版，我这次没有读它的源码。

服务端怎么搭，看 [Hysteria2一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/) 和 [3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)；官方仓库和文档入口见 [Hysteria2官方GitHub仓库和文档在哪](https://vpsjq.com/2026/10/07/hysteria2-github-docs/)。

## 小结

- v2rayNG：源码里能确认识别 `hysteria2://` 和 `hy2://`，也能读取 Reality 的 `pbk`、`sid`、`spx` 等参数；
- Hiddify：README 的协议列表写的是 Hysteria 和 Reality，应用源码里有 Hysteria2 类型，实际解析在 sing-box 内核里，我没读；
- Mihomo：是内核，YAML 里有 hysteria2 节点和 vless 的 `reality-opts`，但官方文档对 Xray v26.7.11 及以上版本的 Reality 兼容性有警告；
- 以上都是读源码和文档的结论，我没有在设备上实际导入验证，版本更新后细节可能变化。
