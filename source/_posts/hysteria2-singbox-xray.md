---
title: "sing-box和Xray里怎么配Hysteria2？字段、版本要求和userpass的坑"
date: 2026-10-02 20:30:00
tags:
  - Hysteria2
  - sing-box
  - Xray
categories:
  - vps工具
description: "sing-box和Xray都能跑Hysteria2，但配法和官方客户端差别不小。这篇按两家官方文档整理sing-box的出入站字段、Xray把协议和传输拆开的写法、各自从哪个版本开始支持，以及userpass要把用户名和密码拼起来填这个容易踩的坑。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "sing-box和Xray里怎么配Hysteria2？字段、版本要求和userpass的坑",
      "description": "sing-box和Xray都能跑Hysteria2，但配法和官方客户端差别不小。这篇按两家官方文档整理sing-box的出入站字段、Xray把协议和传输拆开的写法、各自从哪个版本开始支持，以及userpass要把用户名和密码拼起来填这个容易踩的坑。",
      "datePublished": "2026-10-02T20:30:00+08:00",
      "dateModified": "2026-10-02T20:30:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-singbox-xray/",
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
          "name": "sing-box支持Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "支持，type写hysteria2，出站和入站都有。出站要填server、server_port、password，并且tls是必填；端口跳跃的server_ports和hop_interval从sing-box 1.11.0开始有，realm、bbr_profile等字段是1.14.0新增的。具体以你所用版本的官方文档为准。"
          }
        },
        {
          "@type": "Question",
          "name": "Xray支持Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "支持，但写法和别的协议不一样：Xray把hysteria拆成协议层和传输层两部分。官方文档里hysteria出站在v26.1.23加入，入站和传输配置在v26.3.27加入，旧版本的Xray没有这个功能。"
          }
        },
        {
          "@type": "Question",
          "name": "sing-box连官方Hysteria2服务端，userpass怎么填？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "sing-box没有userpass这种写法。官方Hysteria2的userpass本质上是把用户名:密码拼成一个字符串当密码，所以在sing-box里要把这个组合整体填进password字段。"
          }
        }
      ]
    }
  ]
}
</script>

搜"hysteria2 sing-box 配置"或者"xray hysteria2"的人，手里通常已经有一个 Hysteria2 节点，想在 sing-box 或 Xray 这类内核里使用，或者想直接用它们来搭服务端。两家都支持，但**字段和官方 Hysteria2 的 `config.yaml` 不是一一对应的**，照搬官方客户端的写法会出问题。这篇按两家的官方文档整理。

先说明一个前提：**我没有在本机运行 sing-box，也没有用 Xray 实测过 Hysteria2**（这台机器上的 Xray 只跑着一个 VLESS Reality 节点，我没有去改它）。下面的字段、版本号都来自官方文档和更新记录，示例是我按字段说明拼出来的，没有跑通过，抄之前请对照你自己版本的官方文档。官方客户端和服务端本身的配法，见[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)和[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。

## 先看版本：太旧的内核没有这个功能

- **sing-box**：outbound 的 `server_ports`（端口跳跃）和 `hop_interval` 是 **1.11.0** 加的；`hop_interval_max`、`bbr_profile`、`disable_chrome_parrot`、`realm` 是 **1.14.0** 加的；Gecko 混淆相关的 `obfs.min_packet_size`、`obfs.max_packet_size` 也是 1.14.0。Hysteria2 的基本出入站更早就有，我没有逐版本去查最早是哪一版。
- **Xray**：按官方文档，hysteria 出站是 **v26.1.23**，入站和传输配置是 **v26.3.27** 才加入的。再旧的版本里写 `hysteria` 会直接不认。

所以第一步永远是 `sing-box version` 或 `xray version` 看一眼，版本不够先升级。

## sing-box：出站（当客户端用）

官方文档里的结构是这样的（节选常用字段，其余如 `realm`、`brutal_debug` 我没有展开）：

```json
{
  "type": "hysteria2",
  "tag": "hy2-out",
  "server": "your.domain.net",
  "server_port": 443,
  "password": "你的密码",
  "tls": {
    "enabled": true,
    "server_name": "your.domain.net"
  }
}
```

要点：

- `tls` 在出站里是**必填**的，别省。`tls` 里具体能写哪些字段（`insecure`、证书指纹等），见 sing-box 官方的 TLS 页面，我这里只用了最基本的两项。
- `server_ports` 写成 `["2080:3000"]` 这种形式，配合 `hop_interval` 做端口跳跃，服务端怎么配见[端口跳跃配置](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)。
- `up_mbps` / `down_mbps`：官方文档在入站部分的说明是，不设置时服务端会指示客户端用 BBR，设置了就拒绝客户端用 BBR。出站这边我只确认了字段存在，**具体怎么影响拥塞控制我没有核对**，不确定就先不填，原因见[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)。
- `obfs`：`type` 填 `salamander`，再配 `password`，要和服务端一致。官方文档标注 1.14.0 对 `obfs` 有改动，用新版本时看一下更新说明。

### 最容易踩的坑：userpass

官方文档有一条专门的警告：官方 Hysteria2 支持 `userpass` 认证，实质是把 `<用户名>:<密码>` 组合起来当作真正的密码，**sing-box 没有 userpass 这种别名**。所以如果服务端用的是官方程序的 userpass（多用户的做法见[多用户配置](https://vpsjq.com/2026/10/02/hysteria2-multi-user/)），sing-box 里要把 `用户名:密码` 整个填进 `password`。

## sing-box：入站（当服务端用）

入站里和官方服务端相比，几个对应关系：

- `users`：每个用户一个 `password`。
- `tls`：**必填**，证书要自己准备好，sing-box 这边的 TLS 字段写法见官方 TLS 页面。
- `obfs`：salamander 混淆，和客户端一致。
- `masquerade`：认证失败时的 HTTP/3 行为，可以写成 URL 字符串（`file://` 当文件服务器、`http(s)://` 当反向代理），也可以用 `masquerade.type` 写成对象，类型有 `file`、`proxy`、`string`。**这两种写法互斥**；不配置时返回 404 页面。
- `ignore_client_bandwidth`：没设 `up_mbps`、`down_mbps` 时，让客户端用 BBR；设了就禁止客户端用 BBR。

和官方服务端对比，这里能看出：官方 `config.yaml` 里的 `masquerade` 同样是 `file`、`proxy`、`string` 三类，思路一致，只是 sing-box 用的是 JSON 和蛇形命名。

## Xray：协议和传输是拆开的

Xray 的写法和另外两者最不同：官方文档明确说，hysteria 在 Xray 里被拆成**一个简单的代理控制协议**和**一个调优过的 QUIC 传输**，两部分分开配置。

**出站的协议部分**官方示例非常简单：

```json
{
  "protocol": "hysteria",
  "settings": {
    "version": 2,
    "address": "192.168.108.1",
    "port": 3128
  }
}
```

`version` 必须是 2，`address` 和 `port` 必填。认证密码、伪装这些不在这里，而在传输层的 `hysteriaSettings` 里：

- `auth`：认证密码，两端要一致；搭配入站时，如果入站配了 `users`，会覆盖这里的值。
- `udpIdleTimeout`：单位秒，默认 60，单条 QUIC 原生 UDP 连接的空闲等待时间。
- `masquerade`：HTTP/3 页面伪装，有 `type`、`dir`、`url`、`rewriteHost`、`insecure`、`content`、`headers`、`statusCode` 这些字段。

官方还有一条提示：**hysteria 协议本身无认证，如果不搭配 `hysteria` 传输层，就无法代理 UDP**，也不推荐搭配其他传输层。换句话说，写了 `protocol: hysteria` 就应该把传输也设成 hysteria，不要混搭。

传输的 `streamSettings` 怎么写、字段名是 `network` 还是 `method`，我对照官方传输文档和源码时看到的不完全一致：文档里写的是 `method`，源码里有按名称解析 `hysteria` 的逻辑，我没有确认你那个版本的实际键名。**这部分我没有给完整示例，请直接看你所用版本的官方传输页面。**

另外两处我只看到文档提及、没有展开核对：端口跳跃（`udpHop`）和 Salamander 混淆在 Xray 里归 `finalmask` 管，拥塞相关的 `quicParams` 也在那里；brutal 的说明在 `hysteriaSettings` 的文档里。要用这些，请去看官方的 finalmask 页面。

## 对照表

| 要配的东西 | 官方 Hysteria2 | sing-box | Xray |
|---|---|---|---|
| 配置格式 | YAML | JSON | JSON |
| 认证 | `auth`（含 userpass） | `password`，userpass 要手动拼 | `hysteriaSettings.auth` |
| 证书/TLS | `acme` 或 `tls` | `tls`，出入站都必填 | 走 Xray 通用的 TLS 配置，我没有逐项核对 |
| 伪装 | `masquerade` | `masquerade` | `hysteriaSettings.masquerade` |
| 混淆 | `obfs` | `obfs` | `finalmask` |
| 端口跳跃 | 服务端用防火墙转发 | `server_ports`、`hop_interval`（1.11.0+） | `finalmask` 里的 `udpHop` |

Clash 类内核（mihomo）的写法见[Clash 报 unsupported proxy type](https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/)，各平台客户端汇总见[平台客户端](https://vpsjq.com/2026/10/02/hysteria2-platform-clients/)。

## 排查顺序

1. 内核版本够不够（上面的版本表）。
2. 密码是不是和服务端一致；服务端用 userpass 的，sing-box 里填的是 `用户名:密码`。
3. 混淆、端口跳跃两端是否都开了、参数是否一致。
4. TLS 的域名、证书校验选项是否对应；自签证书要么装指纹要么关校验，关校验有安全影响。
5. 以上都对仍连不上，回到[超时报错排查](https://vpsjq.com/2026/10/02/hysteria2-timeout-no-recent-network-activity/)，先确认 UDP 端口放行。

## 没有覆盖的

- sing-box 的 `realm` 字段（对应官方 Realms 模式）：只看到字段存在，没有核对用法，不写。协议层面的背景见[Hysteria2是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)。
- Xray 入站的完整写法和 finalmask 的细节：只在文档里确认了存在，没有逐项核对，不写。
- 任何实机速度对比：我没有测过，不给结论。
