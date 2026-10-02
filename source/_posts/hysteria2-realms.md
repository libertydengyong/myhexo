---
title: "Hysteria2 Realms是什么？没有公网IP怎么搭服务端，NAT打洞的限制和风险"
date: 2026-10-02 22:00:00
tags:
  - Hysteria2
  - Realms
  - NAT
categories:
  - vps工具
description: "Hysteria 2.9.0新增的Realms模式让服务端在没有公网IP、没有端口转发的情况下运行，靠会合服务和UDP打洞让客户端直连。这篇按官方文档讲清它的原理、realm地址写法、服务端和客户端配置、证书三种做法、NAT兼容表，以及公共会合服务的风险。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2 Realms是什么？没有公网IP怎么搭服务端，NAT打洞的限制和风险",
      "description": "Hysteria 2.9.0新增的Realms模式让服务端在没有公网IP、没有端口转发的情况下运行，靠会合服务和UDP打洞让客户端直连。这篇按官方文档讲清它的原理、realm地址写法、服务端和客户端配置、证书三种做法、NAT兼容表，以及公共会合服务的风险。",
      "datePublished": "2026-10-02T22:00:00+08:00",
      "dateModified": "2026-10-02T22:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-realms/",
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
          "name": "Hysteria2 Realms是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Realms是Hysteria 2.9.0加入的点对点模式：服务端不需要公网IP和端口转发，由一个会合服务（rendezvous）帮服务端和客户端互相找到对方，然后双方通过UDP打洞建立直连的QUIC连接。官方说明会合服务只负责介绍，不转发任何流量。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2没有公网IP能用吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以用Realms模式。官方列出的适用场景包括家宽NAT后面、咖啡店酒店或手机热点这类无法控制路由器的网络、CGNAT环境。前提是服务端和客户端都有能出站的UDP通路，并且NAT类型允许打洞；任何一方是随机端口的对称NAT，而另一方不是公网IP或全锥型时，官方标注通常会失败。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2 Realms的服务端怎么配？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "把listen写成realm://令牌@会合服务地址/realm名称，其余的auth、tls、obfs等字段保持不变；客户端的server字段写同一个realm地址，再配auth密码。官方提示realm名称要用足够长的随机字符串，因为知道名称的人可以探测到你服务器的IP。"
          }
        },
        {
          "@type": "Question",
          "name": "用官方公共会合服务realm.hy2.io安全吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方明确写了：这是免费的尽力而为服务，没有任何保证，可能随时失效、改限制或被封；所有realm都是用户自己运营的，官方不审核也不背书，别人的realm可能记录你的流量、做中间人或本身就是蜜罐。需要认真使用的话，官方建议自建会合服务。"
          }
        }
      ]
    }
  ]
}
</script>

搜"hysteria2 realm""hysteria2 没有公网 ip"的人，要解决的是同一类问题：**服务端放在家里的宽带、手机热点、或者运营商给的是 CGNAT，没有公网 IP，也没法做端口转发，Hysteria2 还能不能用？** 官方在 2.9.0 版本给出的答案就是 Realms。这篇按官方的 Realms 文档讲清它是什么、怎么配、什么情况下会失败。

先说明：以下内容来自官方文档和更新记录，**我没有搭过 Realms 服务端，也没有测过打洞成功率**。本站其他搭建文章都是按有公网 IP 的常规搭法写的，Realms 是另一种模式，不是替代。Realms 的背景在[Hysteria2是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)里提过一段，这篇展开。

## Realms 是什么

官方的描述：Realms 是一种点对点（P2P）模式，让 Hysteria 服务端**不需要公网 IP，也不需要端口转发**就能运行。靠一个小的**会合服务（rendezvous）**让服务端和客户端互相认识，然后双方做 **UDP 打洞（hole punching）**，建立直连的 QUIC 连接。打洞成功后会合服务就不再参与，流量在客户端和服务端之间直接走。官方强调：**会合服务只负责介绍，不转发任何流量。**

官方列出的适用场景：

- 住在 NAT 后面的家庭宽带。
- 咖啡店、酒店、手机热点这类控制不了路由器的网络。
- 不想为一次小实验去开一台带开放端口的 VPS。
- 处于 CGNAT 后面、完全拿不到入站端口的环境。

**前提**：官方写得很清楚，你仍然需要一条通向会合服务、通向对端网络的**可用的出站 UDP 通路**，大多数 NAT 允许这样做。

### 什么时候不需要它

有一台带公网 IP 的 VPS，按[一键脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)或[config.yaml](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)常规搭就行，不需要 Realms。官方在 NAT 兼容表里的结论也是：打洞失败的时候，退回有公网 IP 的服务器。

## 工作流程

按官方文档，过程是这样：

1. 服务端向会合服务**注册一个 realm**（一个你起的名字），同时上报它通过 STUN 探测到的自己的 UDP 公网地址。
2. 客户端给出同一个 realm 地址，请求会合服务帮忙连接。会合服务把服务端的地址发给客户端，同时把客户端的地址推给服务端。
3. 双方**同时**向对方发 UDP 包，在各自的 NAT 上打出洞。
4. 洞打通后，正常的 Hysteria QUIC 握手在这条直连上进行，包括 TLS 验证和密码认证。

## realm 地址怎么写

服务端和客户端都用同一种 URI 来标识 realm：

```
realm://<令牌>@<会合服务主机>[:端口]/<realm名称>
```

- `realm://` 用 HTTPS 和会合服务通信（默认 443），官方推荐。
- `realm+http://` 用明文 HTTP（默认 80），仅限开发用。
- `<令牌>` 是会合服务的共享 Bearer 令牌。
- `<realm名称>` 是你起的名字，两端必须一致。

另外 URL 支持两个可选查询参数：`stun=<主机:端口>`（覆盖 STUN 服务器，可重复写多个，优先级高于 YAML 里的 `realm.stunServers`）和 `lport=<1-65535>`（把本地 UDP 套接字绑定到指定源端口，方便做防火墙放行或让 NAT 映射更可预测，默认随机）。

## 选会合服务：公共的还是自建

### 公共会合服务

Hysteria 项目运营着一个公共的会合服务 `realm.hy2.io`，令牌是 `public`：

```
realm://public@realm.hy2.io/你的realm名称
```

官方对它的警告非常重，我原样转述要点：

- **没有任何保证。** 免费、尽力而为，可能宕机、改限制、被封、或者不通知就消失，**不要用它承载重要的东西**。
- **所有 realm 都是用户自己运营的。** 官方不运营、不背书、不审核注册在上面的任何代理服务，将来也不会。任何人都能用任何名字注册 realm。**只连你信任的运营者的 realm**：陌生人的 realm 可能记录你的流量、做中间人，或者本身就是蜜罐，对待它要像对待一个随机的 VPN 服务商一样。
- **令牌是共享的，所以知道或猜到你 realm 名称的人，可以探测到你服务器的 IP。** 他们不能用你的代理（Hysteria 自己的认证仍然有效），但能知道你在哪里。官方的建议是：realm 名称取**长且随机**的（比如 `my-cabin-1f3a8c2e9b` 就比 `home` 难猜得多），把它当成秘密；避免用能识别你身份的名字（用户名、主机名等）；这些对你很重要的话，**自建**。

当前限制（官方写明可能随时变化）：realm 名称 6 到 64 个字符，以字母或数字开头，其余只能是字母、数字、`-`、`_`；每个客户端 IP 同时最多注册 2 个 realm。

### 自建

会合服务端是开源的，仓库在 GitHub 的 apernet/hysteria-realm-server。官方说自建加一个强而私有的令牌，是任何正式使用的正确选择：只有知道令牌的客户端和服务端才能注册和连接，运行时间、限制、日志都由你控制，每个 realm 只占几 KiB 内存。部署方法看那个仓库的 README，我没有核对，不写。

## 服务端配置

把 `listen` 写成 realm 地址就行。服务端会通过出站 TCP 连接到会合服务、注册 realm，然后等待连接，**不需要入站端口**：

```yaml
listen: realm://public@realm.hy2.io/你的realm名称
```

其余字段（`auth`、`tls`、`obfs`、`bandwidth` 等）保持不变，见[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。STUN、打洞超时、心跳这些调优项，在官方 Full Server Config 的 `realm` 段里，字段有 `stunServers`、`stunTimeout`、`punchTimeout`、`heartbeatInterval`、`ipMode`（`dual`、`v4`、`v6`）、`portMapping`（UPnP/NAT-PMP，默认关）等，默认值对大多数人够用。

官方还有一个提醒：Realms 模式下服务端监听的是一个**随机 UDP 端口**，而不是 443，而非标准端口上的 HTTP/3 流量本身可能就是被检测的特征。**担心深度包检测的话，建议开启 `obfs`**，见[协议原理那篇](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)里关于混淆的部分。

## 客户端配置

`server` 写同一个 realm 地址，再配认证密码：

```yaml
server: realm://public@realm.hy2.io/你的realm名称
auth: 你的Hysteria密码
```

客户端流程是：STUN 探测、请求会合服务介绍、打洞、然后正常的 Hysteria QUIC 握手，**包括 TLS 验证和密码认证**。官方特别说明：**realm 令牌不能代替 Hysteria 服务端的密码**，两个是独立的。

## 证书怎么办：官方给了三种做法

Realms 模式下客户端没有域名可以用来校验证书，它连的是会合服务返回的 IP。不做配置的话，客户端会拿会合服务的主机名当 SNI，和普通证书对不上。官方给了三个选项：

1. **自签证书加 `pinSHA256`**：在服务端运行 `hysteria cert`，它会生成密钥和证书，并打印出可以直接粘贴的 `tls` 配置块，服务端用 cert/key，客户端用 `insecure: true` 加 `pinSHA256`。指纹固定保证客户端只接受这张证书，所以 SNI 和 CA 校验都不重要了。
2. **真正的 CA 证书加 `tls.sni` 覆盖**：用 DNS-01 方式的 ACME 为你控制的域名申请证书（没有公网 IP 时 HTTP-01 和 TLS-ALPN-01 没法用），服务端用它，客户端用 `tls.sni` 设成这个域名。DNS 验证见[Nginx 和证书那篇](https://vpsjq.com/2026/10/02/hysteria2-nginx-cloudflare-443/)。
3. **给会合服务主机名签证书**：只在两个服务都是你自建时才实际可行，服务端证书的域名就是会合服务的主机名，客户端默认的 SNI 就能对上。

关于自签证书的一个坑，官方文档和更新记录里有出入需要留意：文档里写 v2.9.0 上 `hysteria cert` 生成的证书会让客户端报 `tls: internal error`，临时办法是在服务端 `tls` 里加 `sniGuard: disable`；而 v2.9.1 的更新说明写的是，`hysteria cert` 的示例服务端配置现在已经自带了 `sniGuard: disable`，自签证书开箱即用。**所以用 2.9.1 以后的版本，一般不用再手动加**；如果还是遇到这个报错，再按文档加上，相关字段的含义见[Nginx 那篇](https://vpsjq.com/2026/10/02/hysteria2-nginx-cloudflare-443/)里对 `sniGuard` 的说明。

## NAT 兼容性：什么情况下会失败

打洞能不能成功，取决于两端的 NAT 类型。官方给了一张兼容矩阵，我把它整理成文字（双方不分谁是客户端谁是服务端）：

- **一方是公网 IP 或全锥型（Full cone）**：和任何类型配对都能可靠成功。
- **双方都是受限或端口受限型（Restricted / Port-restricted）**：可靠成功。
- **受限或端口受限型 对 可预测的对称型（Sym predictable）**：有时成功，取决于 Hysteria 能不能预测对方下一个端口。
- **可预测的对称型 对 可预测的对称型**：同样是"有时成功"。
- **随机的对称型（Sym random）对 受限、端口受限或对称型**：官方标注通常失败，并说这是 UDP 打洞本身的性质，不是 Hysteria 的限制。

官方还说明，"可预测对称型"的情况依赖 Hysteria 观察多个 STUN 服务器返回的地址，端口落在较近的范围里，默认的 3 个 STUN 服务器通常能暴露这个规律，**只用 1 个 STUN 服务器会让这个启发式失效**。官方的结论是：Realms 在你的网络里不工作的话，最可能的原因是至少一端是对称 NAT，这时退回有公网 IP 的服务器。

### STUN 服务器

两端都要用 STUN 探测自己的公网 UDP 地址。不配置时，Hysteria 用内置的一小份公共 STUN 列表：`stun.nextcloud.com:3478`、`stun.sip.us:3478`、`global.stun.twilio.com:3478`。官方说这些由第三方运营，只是"出于礼貌提供"，可能宕机、被限速或在你的网络里被封，正式一点的使用请通过两端的 `realm.stunServers` 指向你自己的或信得过的 STUN 服务器。

## 版本和已知问题

按官方更新记录：

- **v2.9.0（2026-05-10）**：加入 Realms。
- **v2.9.1**：修复客户端连接对称 NAT 后面的服务端失败的问题，提高打洞成功率；`hysteria cert` 示例配置带 `sniGuard: disable`。
- **v2.9.3**：加入 Realms 的 UPnP/NAT-PMP 端口映射支持，以及 `ipMode` 选项。
- **v2.12.3（2026-09-16）**：修复 Linux 内置[端口跳跃](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)的规则错误地重定向了出站 UDP 流量，**可能导致 Realms 连接和同一台机器上的其他 UDP 流量出问题**。

所以：要用 Realms，先升级到较新的版本，升级方法见[升级和卸载](https://vpsjq.com/2026/10/02/hysteria2-upgrade-uninstall/)；同一台机器上同时用 Realms 和端口跳跃的，要特别留意这一条。

## 排查顺序

1. **版本够不够**：不低于 2.9.0，建议用较新的版本。
2. **出站 UDP 通不通**：Realms 要求通向会合服务和对端的 UDP 通路。参考[被封还是被 QoS](https://vpsjq.com/2026/10/02/hysteria2-blocked-or-qos/) 判断是不是 UDP 被限制。
3. **NAT 类型**：对照上面的兼容矩阵，任何一端是随机对称 NAT 且对端不是公网 IP 或全锥型，就基本不用试了。
4. **STUN 服务器**：默认的公共 STUN 在你的网络里可能连不上，换成自己的。
5. **证书**：客户端报 TLS 相关错误，对照上面的三种证书做法。
6. **提 issue 之前**：官方要求两端都用 `HYSTERIA_LOG_LEVEL=debug` 运行，并把两边的完整输出一起附上，因为 Realms 涉及 STUN、会合服务、打洞、TLS、QUIC 握手多个环节，只有一端的日志很难定位。

## 值得想清楚的几点

- **Realms 不等于更隐蔽**。官方自己提醒了随机端口加 HTTP/3 本身可能是特征，要开混淆。
- **公共会合服务是别人的服务器**：它能知道你的 IP 和 realm 名称；官方对此的态度是"自建才适合认真使用"。我这里的建议和官方一致：只是试一试可以用公共的，要长期用就自建。
- **官方对这个模式的定位**：官方在适用场景里写的是家宽、热点、临时实验。在这个场景之外，是否值得用它替代一台有公网 IP 的 VPS，没有官方结论，我也没有实测，不下判断。

## 没有覆盖的

- **会合服务的自建步骤**：没核对，不写。
- **客户端侧的 STUN、打洞调优字段**：官方放在 Full Client Config，我没有逐项核对，不写。
- **实际打洞成功率、延迟、速度**：没有测过，不给数据。
- **其他软件（sing-box、mihomo 等）对 Realms 的支持**：sing-box 的出站文档里有 `realm` 字段，我只确认了字段存在，见[sing-box 和 Xray 那篇](https://vpsjq.com/2026/10/02/hysteria2-singbox-xray/)；其他软件我没有核对，不写。
- **Realms 能不能和[端口跳跃](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)一起用**：我只确认了上面那条 v2.12.3 的修复说明，除此之外没有官方的组合说明。
