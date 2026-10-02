---
title: "Hysteria2是什么协议？工作原理和Hysteria 1代的区别，官方文档逐条对照"
date: 2026-10-02 19:30:00
tags:
  - Hysteria2
  - 协议原理
categories:
  - vps工具
description: "Hysteria2是基于QUIC的代理协议，常简称hy2。这篇按官方协议文档讲清楚它怎么握手认证、怎么转发TCP和UDP、拥塞控制怎么用，再对照官方的2 vs 1页面，说明和Hysteria 1代不兼容、新增了什么、缺了什么，以及2.12.0新加的mimic是什么。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2是什么协议？工作原理和Hysteria 1代的区别，官方文档逐条对照",
      "description": "Hysteria2是基于QUIC的代理协议，常简称hy2。这篇按官方协议文档讲清楚它怎么握手认证、怎么转发TCP和UDP、拥塞控制怎么用，再对照官方的2 vs 1页面，说明和Hysteria 1代不兼容、新增了什么、缺了什么，以及2.12.0新加的mimic是什么。",
      "datePublished": "2026-10-02T19:30:00+08:00",
      "dateModified": "2026-10-02T19:30:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/",
      "author": {"@type": "Organization", "name": "vpsjq.com"},
      "publisher": {"@type": "Organization", "name": "vpsjq.com"}
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2是什么协议？",
          "acceptedAnswer": {"@type": "Answer", "text": "Hysteria2是一个基于QUIC的TCP和UDP代理协议，官方的定位是为速度、安全和抗审查设计。协议规范要求它实现在标准QUIC传输协议（RFC 9000）之上，并使用QUIC的不可靠数据报扩展（RFC 9221）。服务端对没有认证凭据的访问者表现得和普通HTTP/3网站一样。"}
        },
        {
          "@type": "Question",
          "name": "Hysteria2和Hysteria 1代兼容吗？",
          "acceptedAnswer": {"@type": "Answer", "text": "不兼容。官方的2 vs 1页面写明协议和代码库都有重大变化，Hysteria 2不兼容1.x，客户端和服务端必须同时选用1.x或同时选用2.x。"}
        },
        {
          "@type": "Question",
          "name": "Hysteria2比Hysteria 1多了什么、少了什么？",
          "acceptedAnswer": {"@type": "Answer", "text": "官方列出的主要改进有：可伪装成HTTP/3的新协议、UDP会话首包0-RTT、新的ACL和出站系统、流量统计API以及性能改进。官方列出尚未实现的功能有客户端ACL（目前只有服务端ACL）和FakeTCP。"}
        },
        {
          "@type": "Question",
          "name": "Hysteria2的hy2是什么意思？",
          "acceptedAnswer": {"@type": "Answer", "text": "hy2是Hysteria2的常见简称，分享链接里也常见hysteria2://或hy2://这样的写法，链接参数的含义见客户端导入连接那篇。"}
        }
      ]
    }
  ]
}
</script>

搜"Hysteria2 是什么""hysteria2 原理"，常见的答案要么是一句"基于 QUIC 的高速协议"，要么直接跳到怎么搭。这篇按**官方协议规范**把它拆开讲：它怎么连上、怎么转发流量、速度那套东西到底是什么，再对照官方的 2 vs 1 页面讲和 1 代的区别。写"官方说"的地方，都核对过官方协议文档或网站文档；写"我的理解"的，是我的推断。

## 一句话：它是什么

官方协议文档的开头是这么写的：Hysteria 是一个**基于 QUIC 的 TCP 和 UDP 代理**，为速度、安全和抗审查设计。简称 hy2 是大家的习惯叫法。

它的底层要求写得很明确：**必须实现在标准 QUIC 传输协议（RFC 9000）之上，并使用 QUIC 的不可靠数据报扩展（RFC 9221）。** QUIC 跑在 UDP 上，所以 Hysteria2 也是跑在 UDP 上的，这一点决定了它大部分的优点和缺点，详见[优点和缺点](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)。

## 工作原理：四件事

### 1. 连接和认证：伪装成一个 HTTP/3 网站

官方规范里最有特点的一点：**对没有认证凭据的第三方（中间人或主动探测者），Hysteria 服务端的表现和一个标准 HTTP/3 网站一样**，并且客户端和服务端之间加密的流量，看起来和正常的 HTTP/3 流量没有区别。所以服务端必须实现一个 HTTP/3 服务器，规范还建议使用者要么放真实内容，要么把它设成别的网站的反向代理，这就是配置里 `masquerade` 的由来，见[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。

真正的客户端连上之后，会先发一个特殊的 HTTP/3 请求：

```
:method: POST
:path: /auth
:host: hysteria
Hysteria-Auth: [认证凭据]
Hysteria-CC-RX: [客户端最大接收速率，字节/秒，0 表示未知]
Hysteria-Padding: [随机填充]
```

服务端识别出这个请求，就**不会**当作普通网页请求处理，而是用 `Hysteria-Auth` 验证客户端。验证通过，服务端返回的 HTTP 状态码是 **233**（`233 HyOK`），同时告诉客户端是否支持 UDP 转发；验证不过，服务端要么表现得像一个不认识这个请求的普通网站，要么（如果是反向代理）把请求转给上游网站。客户端只要看到状态码不是 233，就认为认证失败并断开。

这也解释了排错时的一个现象：认证失败时报的是 `authentication error`，而不是超时，因为握手是成功的，见[timeout 报错排查](https://vpsjq.com/2026/10/02/hysteria2-timeout-no-recent-network-activity/)里的对照。`Hysteria-Padding` 是可选的，只用来打乱请求和响应的长度特征，双方都应该忽略它的内容。

### 2. 转发 TCP：每个连接一条 QUIC 流

对每一个 TCP 连接，客户端新开一条 QUIC 双向流，先发一个 TCPRequest 消息（消息 ID 是 `0x401`，后面是目标地址和随机填充），服务端回一个 TCPResponse（状态 OK 或错误），OK 之后就在客户端和目标地址之间双向转发数据，直到任意一方关闭。

### 3. 转发 UDP：用 QUIC 的不可靠数据报

UDP 包被封装成 UDPMessage（包含会话 ID、包 ID、分片 ID、分片数、目标地址和负载），通过 QUIC 的**不可靠数据报**发送，客户端到服务端、服务端到客户端都是这样。规范里还有两点值得知道：

- 超过 QUIC 最大数据报大小的 UDP 包，**要么分片，要么丢弃**；分片的包，只要有一片丢了，整个包就作废。
- 协议里没有显式关闭 UDP 会话的方式，服务端会在一段时间没有流量后回收会话。

### 4. 速度：客户端告诉服务端"我能收多快"

官方称之为**一个独特的功能**：可以在客户端设置上传和下载速率。认证时，客户端用 `Hysteria-CC-RX` 把自己的接收速率告诉服务端，服务端也在响应里回复自己的接收速率。三种特殊情况：

- 客户端发 0：表示不知道自己的接收速率，服务端**必须**使用拥塞控制算法（规范举例 BBR、Cubic）自己调速。
- 服务端回 0：表示没有带宽限制，客户端可以按自己的想法发。
- 服务端回 `auto`：表示不指定速率，客户端**必须**用拥塞控制算法自己判断。

所以 `bandwidth` 填多少，不是一个"越大越好"的开关，而是你在**告诉对方你的真实能力**，填错就会适得其反，这点见[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)。

### 可选的混淆

协议还支持可选的混淆层 **Salamander**：把每个 QUIC 包封装成"8 字节盐值加负载"，用盐值和预共享密钥算出 BLAKE2b-256 哈希来处理数据。另外官方更新记录里，2.9.2 版本加入了 **Gecko**，标注为实验性，会把 QUIC 握手包拆成多个片段。混淆和 HTTP/3 伪装之间的取舍，见[优点和缺点](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)。

## Hysteria2 和 Hysteria 1 的区别

官方有一页专门讲 2 和 1 的区别，核心结论只有一句加粗的话：**Hysteria 2 与 Hysteria 1.x 不兼容，客户端和服务端必须同时选 1.x，或者同时选 2.x。** 协议和代码库都发生了重大变化，它只是"继承了 1.x 几乎所有的功能"。

### 官方列出的主要改进

| 改进 | 官方的说法 |
|---|---|
| 新协议 | 重新设计的协议可以伪装成 HTTP/3，提升抗审查能力 |
| UDP 首包 0-RTT | UDP 会话的第一个包没有建立连接的延迟 |
| 新的 ACL 和出站系统 | 不同请求可以走不同的出站 |
| 流量统计 API | 便于监控和管理，见[多用户配置](https://vpsjq.com/2026/10/02/hysteria2-multi-user/) |
| 性能改进 | 底层的各种优化，提升性能和稳定性 |

### 官方列出的暂时没有的功能

- **客户端 ACL**：ACL 目前只在服务端可用。
- **FakeTCP 协议**：官方说它一直是比较小众的功能，还在评估是否加回来。

### FakeTCP 没有，但有了 mimic

官方 2 vs 1 页面写的是 FakeTCP 没有实现。不过官方更新记录里，**2.12.0 版本加入了 mimic 集成**：它把 UDP 包伪装成 TCP，用于限制 UDP 的网络。我看了官方文档，这几点最容易被误解：

- 它**不是**把协议换成 TCP。官方原话的意思是，连接仍然是 QUIC over UDP，只是在网线上看起来像 TCP，是一种**混淆，不是协议变更**。
- **只支持 Linux**，mimic 不随 Hysteria 一起提供，要单独安装，并且 Hysteria 需要 root 权限（要挂载 eBPF 程序）。
- **服务端和客户端必须同时开启**：开了 mimic 的服务端，不用 mimic 的客户端完全收不到响应，看起来像网络问题而不是配置错误。
- **不能和端口跳跃一起用**，同时配置的话 Hysteria 在启动时会拒绝。

这些都来自官方 mimic 文档。我没有在实机上跑过 mimic，所以只讲官方写的，不评价它的实际效果。它是否对你的网络有用，可以先看[被封还是被 QoS](https://vpsjq.com/2026/10/02/hysteria2-blocked-or-qos/)里的对照测试，确认是 UDP 的问题再考虑。

### 其他版本里加的功能

官方更新记录里还有一个值得知道的：**2.9.0 版本加入了 Hysteria Realms**，官方的说法是"没有公网 IP 也行"，通过 NAT 穿透让你在家里、蜂窝网络里托管服务端，客户端点对点直连，不需要端口转发和中继。我没有试过，不写步骤。官方的服务端快速入门里写的是需要公网 IP、域名要指向服务器，那是**常规搭法**的前提，本站搭建类文章也都是按这种搭法写的；Realms 是官方另外提供的一种不需要公网 IP 和端口转发的模式，需要一个会合服务（rendezvous）来帮双方互相找到对方，流量不经过它，两端仍然需要能出站发 UDP。

## 怎么看 1 代和 2 代的名字

- 搜"hysteria 2.0""hysteria v2"的，说的都是同一个东西，也就是 2 代。
- 现在教程里的 `hysteria2://` 链接、官方一键脚本、配置文件里的 `server`、`auth` 这些写法，都是 2 代的。
- **1 代和 2 代不能混着用。** 你在客户端里选的是 hysteria 还是 hysteria2 节点类型，要和服务端装的版本一致，客户端报"不支持的类型"的处理见[Clash 报 unsupported proxy type](https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/)。

## 想接着了解

- 准备搭一台：[一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)；习惯 Docker 的看[Docker 部署](https://vpsjq.com/2026/10/02/hysteria2-docker/)。
- 想知道值不值得用、和其他协议怎么选：[优点和缺点](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)。
- 客户端用哪个：[各平台客户端](https://vpsjq.com/2026/10/02/hysteria2-platform-clients/)。

## 这篇的局限

- 协议细节来自官方协议规范的当前版本，客户端和服务端的实际表现以你装的版本为准。
- "我的理解"只出现在个别地方，已经标出；mimic 和 Realms 我没有实机验证。
- 2 vs 1 页面对 FakeTCP 的说法，和后来加入的 mimic 在时间上有先后，我把两者并列写出来，没有判断官方是否会更新那一页。
