---
title: "Hysteria2和AnyTLS、Trojan、WireGuard、NaiveProxy怎么选？按官方文档对比底层区别"
date: 2026-10-02 21:30:00
tags:
  - Hysteria2
  - AnyTLS
  - Trojan
  - WireGuard
  - 协议对比
categories:
  - vps工具
description: "Hysteria2、AnyTLS、Trojan、NaiveProxy、WireGuard都被拿来比较，但它们解决的问题和底层并不一样。这篇按各自官方文档，只对比传输层、认证方式、UDP处理和抗探测思路这些能核对的事实，再按网络环境给出选择思路，不下谁更快谁更强的结论。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2和AnyTLS、Trojan、WireGuard、NaiveProxy怎么选？按官方文档对比底层区别",
      "description": "Hysteria2、AnyTLS、Trojan、NaiveProxy、WireGuard都被拿来比较，但它们解决的问题和底层并不一样。这篇按各自官方文档，只对比传输层、认证方式、UDP处理和抗探测思路这些能核对的事实，再按网络环境给出选择思路，不下谁更快谁更强的结论。",
      "datePublished": "2026-10-02T21:30:00+08:00",
      "dateModified": "2026-10-02T21:30:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-vs-anytls-trojan-wireguard/",
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
          "name": "Hysteria2和AnyTLS有什么区别？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "底层不同：Hysteria2基于QUIC，跑在UDP上；AnyTLS基于TLS，跑在TCP上。AnyTLS官方说明它要缓解的是嵌套TLS握手指纹问题，做法是灵活的分包和填充、连接复用；它的FAQ还明确说，不要拿它和Hysteria这类UDP/QUIC协议比速度，因为底层拥塞控制和运营商QoS策略都不一样。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2和Trojan哪个好？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "没有绝对答案。Trojan是TLS加密之上的TCP协议，客户端先做真实TLS握手，再发送密码哈希和类SOCKS5请求，认证失败的流量会被转到预设的网站；Hysteria2是QUIC/UDP协议。UDP被限速或阻断时只能用TCP协议，UDP质量好时才谈得上Hysteria2的优势。"
          }
        },
        {
          "@type": "Question",
          "name": "WireGuard能代替Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是同一类东西。WireGuard官方定位是通用VPN，所有数据包都走UDP，对未授权的客户端完全不应答；Hysteria2是为代理场景设计的协议，带HTTP/3伪装。WireGuard官方介绍里没有写抗审查，AmneziaWG的说明里则提到原版WireGuard存在包特征明显、容易被识别的问题，所以有了它的混淆分支。"
          }
        },
        {
          "@type": "Question",
          "name": "NaiveProxy的特点是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按官方README，它复用Chromium的网络栈来伪装流量，把代理服务器藏在Caddy、HAProxy这类前端服务器后面，靠应用层路由抵御主动探测，并用填充和分片缓解基于长度的流量分析。"
          }
        }
      ]
    }
  ]
}
</script>

搜"hysteria2 和 anytls 哪个好""hysteria2 对比 trojan""hysteria2 wireguard"的人，其实在问同一件事：**手上这几种协议，我该用哪个？** 网上多数答案是"某某更快""某某更稳"，但这类结论高度依赖网络环境，也很少有人说明依据。这篇换个做法：只对比**各自官方文档里写明的设计**，也就是底层传输、认证方式、UDP 怎么处理、抗探测靠什么，能核对的写出来，核对不了的明说。**没有速度对比，没有"谁更强"的结论**，我没有做过严格的实测。

Hysteria2 本身的原理见[Hysteria2是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)，和 VLESS Reality、TUIC 的比较见[优点和缺点](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)，这篇不重复。

## 先分两类：代理协议和 VPN

对比之前先要分清，这几个东西不全是一类：

- **代理协议**：Hysteria2、AnyTLS、Trojan、NaiveProxy。目标是把你的请求转发出去，同时让流量不容易被识别。
- **VPN**：WireGuard。官方定位是通用 VPN，用来组网或建立加密隧道，不是专门为对抗审查设计的。

所以"Hysteria2 和 WireGuard 谁好"这个问题，本身有点错位，下面会分开讲。

## 逐个看官方怎么说

### Hysteria2

基于 QUIC（UDP），使用 QUIC 的不可靠数据报扩展；服务端伪装成标准 HTTP/3 网站，认证通过一个 HTTP 请求完成；TCP 请求用 QUIC 的一条双向流承载，UDP 用数据报承载。可选 Salamander 混淆（开了就不再兼容标准 QUIC）。以上都在[原理那篇](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)核对过官方协议文档。

### AnyTLS

AnyTLS 的 README 对自己的描述是：**一个试图缓解"嵌套的 TLS 握手指纹（TLS in TLS）"问题的代理协议**。官方列出的特点是灵活的分包和填充策略、连接复用、配置简洁。

我对照协议文档看到的设计：

- 底层是 **TLS（TCP）**。TLS 握手完成后，客户端立即发送认证请求，内容是密码的 SHA-256 加一段可变长度的填充；认证失败时服务器会关闭连接，或者回落到 HTTP 服务。
- 认证之后在 TLS 上开一层会话层，用 frame（SYN 开流、PSH 推数据、FIN 关流等）复用多个流，所以多个请求可以共用一条连接。
- **填充方案（paddingScheme）可以由服务器下发更新**：客户端第一次连接用默认方案，服务器发现两边不一致，就会发更新指令让客户端后续连接改用新方案。官方的想法是：当默认方案的流量特征被封锁方盯上，可以靠更新参数来改变特征。FAQ 里也直说，默认方案只是示例，**不保证不会被封**。
- UDP：README 里说示例客户端的 SOCKS5 支持 UDP，是通过 UDP over TCP 传输的。

官方 FAQ 里有一条很值得读：速度慢请不要和 Hysteria 这类 UDP/QUIC 协议做对比，因为底层的拥塞控制以及运营商的 QoS 策略不一样，"完全没有可比性"。我认同这个说法的前提：两者走的是 UDP 和 TCP 两条不同的路径。

另外，仓库自述是**参考实现**，示例服务器和客户端默认使用不安全的配置，日常使用推荐第三方兼容软件。sing-box 的 AnyTLS 入站文档标注"Since sing-box 1.12.0"，也就是说要用 sing-box 内核的话，版本要不低于 1.12.0；其他软件的支持版本，我没有逐个核对。

### Trojan

按 Trojan 官方协议文档：客户端先和服务器做一次**真实的 TLS 握手**，成功后所有流量受 TLS 保护，失败则服务器像普通 HTTPS 服务器一样直接关闭连接。握手之后客户端发送的结构是：56 字节的 SHA224(密码) 十六进制串、CRLF、一个类 SOCKS5 的请求、CRLF、负载。命令只有 CONNECT 和 UDP ASSOCIATE 两种。

要点：

- 底层是 **TLS（TCP）**，UDP 通过 UDP ASSOCIATE 封装在这条 TLS 连接里。
- 服务器收到第一个数据包时校验哈希密码和请求，**不合法的就当作"其他协议"**，转发到一个预设的端点（官方文档里这就是回落，通常指向一个正常的网站），所以探测者看到的是一个正常的 HTTPS 站点。
- 官方特别提到，第一个数据包会把负载一起附上，这样可以避免长度规律被识别，也能少发几个包。

本站的搭建教程见[3x-ui 配置 Trojan 节点](https://vpsjq.com/2026/09/23/3x-ui-trojan/)，其中回落网站的设置是关键。

### NaiveProxy

按官方 README：**复用 Chromium 的网络栈**来伪装流量。它列出的几类攻击及应对是：

- 网站指纹、流量分类：靠 HTTP/2 里的流量多路复用，以及模仿浏览器的前导。
- TLS 参数指纹：直接用 Chrome 的网络栈，从根上避开。
- 主动探测：靠"应用层前置"，把代理服务器藏在一个常见的前端服务器后面，由前端做应用层路由。
- 基于长度的流量分析：靠填充和分片缓解。

架构上，前端可以是 Caddy（带 forwardproxy 插件）或 HAProxy 这类能按 HTTP 认证头路由 HTTP/2 流量的反向代理。部署起来比其他几个多一个前端这一层，这点是我从架构图得出的判断。官方还提醒用户总是用最新版本，以保持和 Chrome 的签名一致。

### WireGuard

按官方介绍：是一个简单、快速、使用现代密码学的 VPN，加密用到 Noise 协议框架、Curve25519、ChaCha20、Poly1305 等。从协议页看：

- **所有数据包都通过 UDP 发送**，握手用 Noise_IK。
- 对未授权的客户端，服务器**完全不应答**，官方原话的意思是"静默且不可见"。
- 配置思路接近 SSH：交换公钥即可，支持在不同 IP 之间漫游。

注意：官方介绍里讲的是简单、速度、安全，**没有提抗审查或流量伪装**。它的包有明显的特征，AmneziaWG 的说明里就写到，原版 WireGuard 存在"独特的包特征导致容易被识别"的问题，AmneziaWG 是它的一个 fork，用混淆方法来对抗 DPI。这是 AmneziaWG 自己的说法，我没有去验证它的实际效果。

## 对照表

| | Hysteria2 | AnyTLS | Trojan | NaiveProxy | WireGuard |
|---|---|---|---|---|---|
| 类型 | 代理 | 代理 | 代理 | 代理 | VPN |
| 底层传输 | QUIC（UDP） | TLS（TCP） | TLS（TCP） | HTTP/2（TLS，TCP） | UDP |
| 认证 | 多种方式（密码、userpass 等） | 密码哈希 | 密码哈希 | HTTP 认证（前端按认证头路由） | 公钥 |
| UDP 处理 | QUIC 数据报 | UDP over TCP | 封装在 TLS 里（UDP ASSOCIATE） | 我没有核对 | 原生 UDP |
| 抗探测思路 | 伪装 HTTP/3 站点，可选混淆 | 填充方案，认证失败可回落 HTTP | 认证失败转到预设站点 | 藏在前端服务器之后，复用 Chrome 栈 | 对未授权包不应答，无伪装 |
| 部署 | 官方脚本，较简单 | 需要第三方软件或内核支持 | 需要证书和回落站 | 需要前端（Caddy 等） | 交换公钥即可 |

表里"部署"一行是我的主观归纳，其余来自上文的官方文档；"我没有核对"的格子就是没核对。

## 怎么选：按网络环境想

下面是**选择的思路**，不是谁优谁劣：

1. **UDP 通路好，想要速度上的潜力**：Hysteria2 值得试。注意 `bandwidth` 不要乱填，见[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)。
2. **UDP 被限速或阻断**：Hysteria2、WireGuard 这类纯 UDP 协议帮不上忙，选 TCP 协议：AnyTLS、Trojan、NaiveProxy、[VLESS Reality](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/) 之一。判断是不是 UDP 的问题，见[被封还是被 QoS](https://vpsjq.com/2026/10/02/hysteria2-blocked-or-qos/)。
3. **已经有网站、想让代理藏在同一个域名里**：Trojan 的回落、NaiveProxy 的前端思路，都是围绕"让服务器看起来像正常网站"设计的。Hysteria2 想和网站共用 443，见[Nginx 和 Cloudflare 那篇](https://vpsjq.com/2026/10/02/hysteria2-nginx-cloudflare-443/)。
4. **要的是组网、远程访问内网，而不是翻墙代理**：WireGuard 更对口，Hysteria2 不是干这个的。
5. **想先少折腾**：官方脚本能直接跑的 Hysteria2 比较省事；AnyTLS 的官方参考实现本身只是示例，日常使用要找兼容软件。

最稳妥的做法和之前一样：**同一台服务器上同时开一个 UDP 协议和一个 TCP 协议**，在自己的网络、不同时段各测几次。同台机器、同一时间的对比，比任何文章的结论都可靠。

## 几个常见的误解

- **"TCP 协议一定比 UDP 协议慢"或者反过来**：没有这样的一般规律，官方 FAQ 就明确说两类协议的拥塞控制和运营商 QoS 待遇不同，不能直接比。
- **"套了 TLS 就不会被识别"**：AnyTLS 的存在恰恰说明，TLS 里再套一层 TLS 本身会留下特征，它就是为了缓解这个问题。Trojan、AnyTLS 都不能保证不被封，AnyTLS 官方自己也这么写。
- **"WireGuard 速度快，所以代理场景也用它"**：官方介绍的"快"指的是作为 VPN 的性能，它没有为抗识别做设计，包特征明显。

## 没有覆盖的

- **各协议的实测速度、稳定性、被封概率**：没测，不给结论。
- **Hysteria2 对 AnyTLS 的"谁更难被识别"**：没有官方依据，也没有可靠的第三方研究被我核对过，不写。
- **AmneziaWG、TUIC、Shadowsocks 的细节**：AmneziaWG 只引了它的自述，TUIC 在[S-UI 那篇](https://vpsjq.com/2026/09/06/s-ui-tuic/)里讲过，Shadowsocks 没有核对，所以没放进表里。
- **各客户端对这些协议的支持情况**：客户端和内核的版本要求变化很快，以各自官方文档为准；sing-box 里 Hysteria2 的写法见[这篇](https://vpsjq.com/2026/10/02/hysteria2-singbox-xray/)。
