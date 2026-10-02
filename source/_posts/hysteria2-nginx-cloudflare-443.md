---
title: "Hysteria2能和Nginx共用443端口吗？能套Cloudflare吗？官方文档怎么说"
date: 2026-10-02 20:00:00
tags:
  - Hysteria2
  - Nginx
  - Cloudflare
categories:
  - vps工具
description: "Hysteria2能不能套Cloudflare CDN、能不能和Nginx共用443端口、Nginx占着80端口时证书怎么申请。官方CDN页面的回答是不行，TCP和UDP端口互不冲突这一点是通用知识，这篇分开讲哪些官方明确写了、哪些是通用推断，哪些没有核对。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2能和Nginx共用443端口吗？能套Cloudflare吗？官方文档怎么说",
      "description": "Hysteria2能不能套Cloudflare CDN、能不能和Nginx共用443端口、Nginx占着80端口时证书怎么申请。官方CDN页面的回答是不行，TCP和UDP端口互不冲突这一点是通用知识，这篇分开讲哪些官方明确写了、哪些是通用推断，哪些没有核对。",
      "datePublished": "2026-10-02T20:00:00+08:00",
      "dateModified": "2026-10-02T20:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-nginx-cloudflare-443/",
      "author": {"@type": "Organization", "name": "vpsjq.com"},
      "publisher": {"@type": "Organization", "name": "vpsjq.com"}
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2能套Cloudflare CDN吗？",
          "acceptedAnswer": {"@type": "Answer", "text": "不能。官方文档里有专门的页面回答这个问题，结论是简短而明确的不行，原因有三点：认证通过后连接会切换成CDN不支持的自定义代理协议；绝大多数CDN不支持用HTTP/3回源；即使都能解决，反向代理也会抵消Hysteria自定义拥塞控制带来的速度优势。域名解析要设成仅DNS，不能走橙色云朵代理。"}
        },
        {
          "@type": "Question",
          "name": "Hysteria2和Nginx能共用443端口吗？",
          "acceptedAnswer": {"@type": "Answer", "text": "Hysteria2默认监听UDP 443，Nginx通常监听TCP 443。TCP和UDP的端口编号是各自独立的，所以同一个443可以同时被两者使用，这是操作系统层面的通用知识，不是官方文档的说法。需要注意的是，官方的HTTP/HTTPS伪装选项listenHTTP和listenHTTPS会让Hysteria自己监听TCP的80和443，开了就会和Nginx冲突。"}
        },
        {
          "@type": "Question",
          "name": "Nginx占着80端口，Hysteria2的证书怎么申请？",
          "acceptedAnswer": {"@type": "Answer", "text": "官方文档给出几种路子：用DNS验证方式申请，它不占用80和443端口；或者把HTTP验证改到别的端口，官方说明这需要端口转发或HTTP反向代理；也可以不用ACME，自己用其他工具申请证书，再用tls的cert和key指向证书文件，官方写明证书在每次TLS握手时都会重新读取，更新证书文件不需要重启服务。"}
        }
      ]
    }
  ]
}
</script>

在服务器上同时跑网站和 Hysteria2 的人，常会遇到三个问题：能不能给 Hysteria2 套 Cloudflare 的橙色云朵？Nginx 已经占着 443，Hysteria2 还能用 443 吗？Nginx 占着 80，证书怎么申请？这几个问题官方文档里有的写得很清楚，有的只能靠通用知识推。下面分开讲，标清楚依据。

## 能不能套 Cloudflare 或其他 CDN：官方明确说不行

官方有一页专门叫"Can I use a CDN?"，开头就回答了：**简短而明确的答案是"不"，它根本行不通。** 官方给的三个原因：

1. **认证之后就不是 HTTP/3 了。** Hysteria 伪装成 HTTP/3 服务器只是伪装，只在客户端认证成功之前遵守标准 HTTP/3；认证通过后连接会切换成自定义的代理协议，Cloudflare 或任何 CDN 都不支持。协议的细节见[Hysteria2 是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)。
2. **CDN 基本不支持用 HTTP/3 回源。** 这些服务通常期望源站使用基于 TCP 的 HTTP/1 或 HTTP/2。
3. **就算前两条都能解决，也会失去速度优势。** 官方的说法是 Hysteria 快的主要原因之一是自定义的拥塞控制和调优参数，加一层反向代理后，客户端对话的是 CDN 的 QUIC 实现，不是 Hysteria 优化过的那一套。

官方提到这个问题的背景是：一些网络环境里，人们用 Cloudflare 来绕开托管 WebSocket 代理（比如 v2ray）的服务器 IP 被封的问题，所以会想到给 Hysteria2 也这么做。官方的回答是别这么想。

**所以怎么做：** 域名解析到 Hysteria2 服务器时，要设成**仅 DNS 解析**（Cloudflare 里是灰色云朵），不要开橙色云朵代理。这条是根据官方"不能套 CDN"推出来的做法；Cloudflare 里具体怎么切换我没有逐步核对，不写菜单路径。如果你的节点是 TCP 协议（比如基于 WebSocket 的），套 CDN 是另一回事，见 [S-UI 配合 Cloudflare CDN](https://vpsjq.com/2026/09/30/s-ui-cloudflare-cdn/)，不适用于 Hysteria2。

## 能不能和 Nginx 共用 443

先说结论：**默认情况下不冲突，开了某个选项就会冲突。**

### 为什么默认不冲突（通用知识）

官方服务端配置里，`listen` 不写的时候，服务端监听的是 `:443`，也就是 **UDP 的 443**（因为 443 是 HTTP/3 的默认端口）。而 Nginx 提供 HTTPS 网站，通常监听的是 **TCP 的 443**。

**TCP 和 UDP 的端口编号是各自独立的**，同一个数字可以在 TCP 和 UDP 上分别被不同程序使用，所以两者可以同时在 443 上工作。这是操作系统的通用知识，不是官方文档里的说法。你可以用 `ss -tlnp | grep :443` 看 TCP、`ss -ulnp | grep :443` 看 UDP，自己确认。

如果你的 Nginx 也开了 HTTP/3（监听 UDP 443），那就是两个程序抢 UDP 443，会冲突，这时要给 Hysteria2 换个端口。这一条是推断，我没有在 Nginx 上实测。

### 什么时候会冲突：HTTP/HTTPS 伪装选项

官方的 `masquerade` 里有两个可选项，`listenHTTP` 和 `listenHTTPS`，用来让服务器**同时在 TCP 的 80 和 443 上也提供伪装网站**，更像一个真正的网站：

```yaml
masquerade:
  listenHTTP: :80
  listenHTTPS: :443
  forceHTTPS: true
```

开了它，Hysteria 自己占用 TCP 80 和 443，**就不能和 Nginx 共用这两个端口了。** 官方在这里特别写了一句：没有证据表明有防火墙把"缺少 TCP 的 HTTP/HTTPS 服务"当作检测 Hysteria 的手段，这个选项只提供给想"多走一步"的用户。所以，**你已经有 Nginx 在跑网站，就别开这两个选项。**

### 伪装站点怎么选

服务器上既然已经有真实的网站，`masquerade` 可以选 `file`（用一个目录里的静态文件）或 `proxy`（反向代理另一个网站）。官方的 proxy 选项里有 `rewriteHost`、`insecure` 这些字段，用法见[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。至于把 `proxy.url` 指向本机自己的 Nginx 站点，官方没有这么写过，我也没有测试，所以不给配置。

## Nginx 占着 80 端口，证书怎么办

Hysteria2 用 ACME 自动申请证书时，默认的 HTTP 验证需要 80 端口，这和 Nginx 冲突，[config.yaml 那篇](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)里提醒过要让 80 端口空着。官方文档里有几条出路：

### 路子一：用 DNS 验证

官方说 ACME 的 DNS 方式通过 DNS 服务商的 API 申请证书，**不依赖具体端口，不占用 80 和 443，也不需要外部访问**。配置里把 `type` 设成 `dns`，再填 DNS 服务商和密钥。官方文档里只列了少数几个常见的 DNS 服务商，并且说明**他们只测试过 Cloudflare 的配置**，其他服务商要自己研究该填什么。如果你的域名在不支持的服务商那里买的，官方说可以把域名的 DNS 托管指向一个支持的服务商（比如 Cloudflare），这样也能用。这里的 Cloudflare 只是用来管理 DNS 记录，和上面不能套 CDN 不矛盾。

### 路子二：把 HTTP 验证改到别的端口

配置里 `acme.http.altPort` 可以改 HTTP 验证监听的端口，但官方的注释写得很明确：**改成 80 以外的端口，需要端口转发或者 HTTP 反向代理，否则验证会失败。** 也就是说，要让外面访问 80 的验证请求，通过 Nginx 转到你改的端口上。具体的 Nginx 配置官方没有给，我也没有实测，所以只讲方向，不写配置。TLS-ALPN 验证同理，`tls.altPort` 改成 443 以外的端口也需要转发。

### 路子三：不用 ACME，自己的证书

如果 Nginx 那边已经在用 certbot 之类的工具续签证书，可以让 Hysteria 直接用同一份证书文件：

```yaml
tls:
  cert: /path/to/fullchain.pem
  key: /path/to/privkey.pem
```

官方文档写明：**证书在每次 TLS 握手时都会重新读取，更新证书文件不需要重启服务。** 所以证书续签后，Hysteria 不用手动重启。这条对省事很有用。但要注意：证书里的域名要和客户端用的 `sni` 一致，这点同样在[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)里讲过。另外，官方还有一个 `sniGuard` 选项，默认是 `dns-san`，会校验客户端传来的 SNI 是否和证书匹配，不匹配就终止握手，SNI 写错时要想到它。

## 把 Hysteria2 放在 Nginx 后面转发，我没有核对

搜索词里有"hysteria2 behind nginx""hysteria2 nginx"，指的是用 Nginx 去转发 UDP 流量给 Hysteria。官方文档没有写这种用法，我也没有核对过，所以**不写步骤**。有两点可以先想一想：Hysteria 是靠自己的 QUIC 来工作的，中间多一层转发会多出来的东西（比如客户端地址怎么传、对速度的影响），官方没有说明；而且官方 CDN 页里关于"反向代理会抵消速度优势"的话，是针对 CDN 的，不能直接当成对 Nginx 的结论。想用的话建议自己在测试环境里对比，用[被封还是被 QoS](https://vpsjq.com/2026/10/02/hysteria2-blocked-or-qos/)里的方法测同一时段的速度。

## 快速对照

| 问题 | 结论 | 依据 |
|---|---|---|
| 套 Cloudflare 橙色云朵 | 不行，域名设成仅 DNS | 官方 CDN 页面 |
| 和 Nginx 共用 443 | 默认可以（UDP 对 TCP） | 通用知识 + 官方默认监听 UDP 443 |
| 开 `listenHTTPS` 后再用 Nginx | 会冲突 | 官方这两个选项监听 TCP 80/443 |
| Nginx 占着 80 申请证书 | 用 DNS 验证、改端口加转发，或自己的证书 | 官方文档 |
| 放在 Nginx 后面转发 | 没核对，不写 | 官方没写 |

## 这篇的局限

- "TCP 和 UDP 端口互不冲突"是通用知识，我在这台服务器上没有实测 Nginx 和 Hysteria 同时跑；你的 Nginx 如果开了 HTTP/3，请先检查 UDP 443。
- 官方文档没有给 Nginx 的具体配置，我这里一律不写，免得给出没验证过的配置。
- 官方只测试过 Cloudflare 的 DNS 验证，用其他 DNS 服务商时，密钥和字段要对着官方文档自己核对。

想先把基础打好，看[一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)和[Docker 部署](https://vpsjq.com/2026/10/02/hysteria2-docker/)。
