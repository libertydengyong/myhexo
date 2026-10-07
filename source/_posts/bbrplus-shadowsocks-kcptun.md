---
title: BBRplus能和Shadowsocks、kcptun一起用吗：TCP拥塞控制和KCP分别管哪一段
date: 2026-10-07 23:30:00
tags:
  - BBR加速
  - BBRplus
  - Shadowsocks
  - kcptun
categories:
  - Linux优化
description: BBR和BBRplus是内核的TCP拥塞控制，kcptun把中间一段换成了UDP上的KCP。依据kcptun和KCP的README、shadowsocks-rust的说明，讲清楚Shadowsocks加BBRplus有没有用、加kcptun后BBRplus还管不管、两者怎么分工，以及kcptun的参数和状态要注意什么。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBRplus能和Shadowsocks、kcptun一起用吗：TCP拥塞控制和KCP分别管哪一段",
      "description": "BBR和BBRplus是内核的TCP拥塞控制，kcptun把中间一段换成了UDP上的KCP。依据kcptun和KCP的README、shadowsocks-rust的说明，讲清楚Shadowsocks加BBRplus有没有用、加kcptun后BBRplus还管不管、两者怎么分工，以及kcptun的参数和状态要注意什么。",
      "datePublished": "2026-10-07T23:30:00+08:00",
      "dateModified": "2026-10-07T23:30:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/bbrplus-shadowsocks-kcptun/",
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
          "name": "Shadowsocks服务器开BBRplus有用吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Shadowsocks的TCP流量走的是系统内核的TCP，BBR和BBRplus是内核的TCP拥塞控制，所以在服务器上开启会作用在服务器作为发送方的那些TCP连接上。至于有没有感觉到提速，要看线路本身是否有丢包和高延迟，BBR不能凭空增加物理带宽。"
          }
        },
        {
          "@type": "Question",
          "name": "kcptun和BBRplus能叠加吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是叠加关系。按kcptun README里的数据流，应用到kcptun客户端是TCP，kcptun客户端到服务端是UDP，服务端到目标又是TCP。跨公网的那一段是UDP，由KCP自己的重传、窗口和纠错控制，不归内核的TCP拥塞控制管，所以服务器开BBRplus不会改变那一段的行为，只会影响两端的TCP段，而这两段通常在本机内部。这是我按数据流推出的结论，没有实测。"
          }
        },
        {
          "@type": "Question",
          "name": "kcptun现在还在维护吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "我读到的GitHub镜像README顶部有项目状态提示：该项目已归档、不再维护，上游不提供二进制。官方仓库github.com/xtaci/kcptun我这里读不到，搜索结果也给出同样的说法，请以官方仓库首页为准。"
          }
        }
      ]
    }
  ]
}
</script>

搜"ss bbrplus""bbrplus kcptun"的人，多半在想一个问题：我已经装了 Shadowsocks，又听说 kcptun 能加速、BBRplus 也能加速，**能不能叠在一起用**？这篇依据 kcptun 和 KCP 的 README，把这几样东西各自管哪一段讲清楚。结论先说：**它们不是叠加关系，而是管不同的段**。

先说明依据：kcptun 的官方仓库 github.com/xtaci/kcptun 我这里直接读不到，所以读的是 GitHub 上的镜像（fork）里的 README，里面的帮助输出版本是 20251124；另外读了 KCP 协议（skywind3000/kcp）的 README 和 shadowsocks-rust 的 README。BBR 部分用的是我之前读过的内核 `tcp_bbr.c` 和 BBRplus 补丁。**我没有搭过 kcptun，也没有测速过**，下面凡是推论的地方都会注明。

<!-- more -->

## 先看 kcptun 是什么，数据怎么走

kcptun 的 README 对自己的定位，是基于 KCP 协议的隧道，带多路复用（SMUX）、纠错（FEC，用的是 Reed-Solomon 码）和加密。README 的 QuickStart 里给了一个转发 8388 端口的例子，并把数据流画出来了：

```text
应用 -> KCP 客户端(8388/tcp) -> KCP 服务端(4000/udp) -> 目标服务器(8388/tcp)
```

也就是说，一条连接被拆成了三段：

| 段 | 协议 | 在哪里 |
| --- | --- | --- |
| 应用到 kcptun 客户端 | TCP | 一般在你自己的设备上，本机内部 |
| **kcptun 客户端到 kcptun 服务端** | **UDP（KCP）** | **跨公网** |
| kcptun 服务端到目标服务器 | TCP | 如果目标就在同一台 VPS 上，就是本机内部 |

README 示例转发的是一个 TCP 端口，**我读到的 README 里没有提到 Shadowsocks**，端口号 8388 只是例子里的数字（它恰好也是 Shadowsocks 常用的默认端口）。

## KCP 是什么

KCP 来自另一个项目（skywind3000/kcp）。它的 README 对自己的说明是：一个高性能的可靠传输协议，设计目标是比传统 TCP 显著降低延迟，**能把平均延迟降低 30% 到 40%，最大延迟最多低到约三分之一，代价是多花 10% 到 20% 的带宽**。这是 KCP 作者自己的说法，不是我测的。

README 还提到：KCP 默认遵循和 TCP 类似的公平流控，会考虑发送缓冲、接收缓冲、**拥塞控制和慢启动**；但对延迟敏感的小数据，可以配置成绕开拥塞控制和慢启动，只靠缓冲区大小来限制。kcptun 的 FAQ 里对应的写法是手动模式：

```text
-mode manual -nodelay 1 -interval 20 -resend 2 -nc 1
```

README 同时警告，改这些底层参数之前要完全理解每一项，否则可能让性能或稳定性变差。

## BBR 和 BBRplus 管的是哪一段

BBR 和 BBRplus 是 **Linux 内核里的 TCP 拥塞控制算法**，决定的是内核里 TCP 连接"发多快"（BBRplus 的来历见 [BBRplus是什么](https://vpsjq.com/2026/10/07/bbrplus-what-is/)）。它们只作用在**TCP 连接**上，并且作用在**发送方**一侧。

把这个和上面的数据流放在一起看：

- 跨公网的那一段是 **UDP（KCP）**，不是 TCP，所以**不归内核的 TCP 拥塞控制管**，由 KCP 自己的重传、窗口、拥塞控制（或被 `-nc` 关掉）和 FEC 负责；
- 内核的 BBR 或 BBRplus 只会管那两段 TCP，而这两段通常在本机内部，不是瓶颈所在。

所以按数据流推：**服务器上开了 BBRplus，也不会改变 kcptun 那一段跨公网的行为**。这是我根据 README 里的数据流得出的推论，没有实测。

## 几种方案对比

| 方案 | 跨公网的那一段 | 拥塞控制由谁管 | 内核 BBR 或 BBRplus 有用吗 |
| --- | --- | --- | --- |
| Shadowsocks 直连（TCP） | TCP | 内核 | 有，作用在服务器发给客户端的方向（发送方在服务器） |
| Shadowsocks 的 UDP 转发 | UDP | 不是 TCP 拥塞控制 | 没有直接作用 |
| Shadowsocks 加 kcptun | UDP（KCP） | KCP 自己 | 对跨公网那段没有直接作用 |
| Hysteria2 | UDP（QUIC） | Hysteria 自己 | 没有直接作用 |

最后一行补充一下：站内 [Hysteria2速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/) 里讲过，Hysteria2 客户端写了 `bandwidth` 就启用 Brutal，不写则用它自己的 BBR，那是 Hysteria 自己 QUIC 实现里带的拥塞控制（QUIC 跑在用户态程序里），**和内核里的 `tcp_bbr` 模块不是一回事**。

上传方向要留意一点：TCP 的拥塞控制在**发送方**生效，所以客户端上传时起作用的是客户端系统的拥塞控制，服务器上的设置管不到。这是 TCP 的一般原理。

## Shadowsocks 这边是怎么回事

shadowsocks-rust 的 README 显示它支持 TCP 和 UDP 转发（配置里有 `mode: tcp_and_udp`），也支持 SIP003 插件（示例里写的是 `--plugin "v2ray-plugin"`）。我读到的 README **没有提到 kcptun**。常见的做法是把 kcptun 当成**另一个独立的进程**，放在 Shadowsocks 前面，让 kcptun 服务端把流量转给 Shadowsocks 的 TCP 端口。

按 README 里的命令格式套用，大致是这样（**我没有实际跑过**，端口和密码换成自己的）：

```bash
# 服务端：把 UDP 4000 收到的流量转给本机的 Shadowsocks 端口
./server_linux_amd64 -t "127.0.0.1:你的SS端口" -l ":4000" -mode fast3 -nocomp -sockbuf 16777217

# 客户端：本地监听 TCP 端口，通过 KCP 发给服务端
./client_linux_amd64 -r "服务器IP:4000" -l ":本地端口" -mode fast3 -nocomp -sockbuf 16777217
```

README 特别说明，这几项参数必须在客户端和服务端**完全一致**，否则连不上：`--key` 和 `--crypt`、`--QPP` 和 `--QPPCount`、`--nocomp`、`--smuxver`。

注意，这样套出来之后，Shadowsocks 客户端要把服务器地址改成指向本地的 kcptun 客户端端口。按 README 的示例，kcptun 转发的是 **TCP** 端口，Shadowsocks 的 UDP 转发不会自动走这条隧道，这一点 README 没有展开，我没有验证。

## 用 kcptun 要考虑的几点（都来自 README）

- **状态**：我读到的镜像 README 顶部有一条项目状态提示：这个项目**已归档、不再维护，上游不提供二进制**，仅供研究和参考。搜索结果也给出了同样的说法。官方仓库我这里读不到，请你以 github.com/xtaci/kcptun 首页的最新说明为准。新部署前要把这一点考虑进去；
- **带宽开销**：FEC 默认是 10 个数据包配 3 个冗余包，README 给的开销公式是 `parityshard / datashard`，也就是默认**多占约 30% 的带宽**；线路好的话可以调小 `-parityshard`，设成 0 就关掉 FEC；
- **CPU**：Reed-Solomon 纠错比较吃 CPU，README 说低端 ARM 设备可能有性能问题，建议关掉 FEC（`--datashard 0 --parityshard 0`）并用 `--crypt salsa20`；
- **系统设置**：README 建议提高打开文件数限制（`ulimit -n 65535`），并给了一组改善 UDP 处理的 sysctl 参数，比如 `net.core.rmem_max` 和 `wmem_max` 调到 26214400，慢速处理器上还要把 `-sockbuf` 调大。这和 Hysteria2 调大 UDP 缓冲区是同一类问题，见 [Hysteria2速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)；
- **UDP 的现实问题**：UDP 流量在一些网络里可能被限速或封端口，判断方法可以参考 [Hysteria2被封还是被QoS限速](https://vpsjq.com/2026/10/02/hysteria2-blocked-or-qos/)；
- **免责声明**：README 开头有免责声明，要求使用者遵守当地法律法规，也说明这是通用的网络传输加速工具。

## 那想"加速 Shadowsocks"该怎么做

按这篇的逻辑，思路是：

1. 如果走的是 TCP 直连，先开内核的 BBR，见 [x-ui、3x-ui和Xray怎么开BBR](https://vpsjq.com/2026/10/04/xui-xray-enable-bbr/) 里讲的内核层面开启和验证方法（对 Shadowsocks 同样适用，因为是内核设置）；要用 BBRplus 就要换内核，先看 [BBRplus是什么](https://vpsjq.com/2026/10/07/bbrplus-what-is/)，它是实验性方案，不保证更快；
2. 开了还慢，别在 BBR 上死磕，先判断是不是线路本身的问题，见 [为什么开了BBR，网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/) 和 [VPS网络测速用什么工具最好](https://vpsjq.com/2026/08/15/vps-speedtest-tools/)；
3. 想换一种 UDP 方案，现在更常见的做法是直接用自带 UDP 传输的协议，比如 Hysteria2，对比见 [Hysteria2节点的优点和缺点是什么](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)；
4. 如果一定要用 Shadowsocks，注意它的抗封锁问题，见 [3x-ui配置Shadowsocks节点及抗封锁分析](https://vpsjq.com/2026/08/31/3x-ui-shadowsocks/) 和 [S-UI配置Shadowsocks](https://vpsjq.com/2026/09/30/s-ui-shadowsocks/)。

## 小结

- BBR 和 BBRplus 是内核的 TCP 拥塞控制，只管 TCP 连接，并且在发送方生效；
- Shadowsocks 走 TCP 时，服务器开 BBR 或 BBRplus 对服务器发出的流量有作用，但能不能提速要看线路；
- kcptun 把跨公网的一段换成了 UDP 上的 KCP，那一段不归内核 TCP 拥塞控制管，所以**它们不是叠加，而是管不同的段**；
- kcptun 有 FEC 带宽开销、CPU 开销和 UDP 缓冲区要求，我读到的镜像 README 提示项目已归档、不再维护；
- 本文依据 README 和数据流做的推论，没有搭建 kcptun，也没有测速，请以实际测试为准。
