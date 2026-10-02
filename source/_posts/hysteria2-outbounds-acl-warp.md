---
title: "Hysteria2服务端怎么分流？outbounds和ACL写法，以及接WARP的思路"
date: 2026-10-02 21:00:00
tags:
  - Hysteria2
  - ACL
  - WARP
categories:
  - vps工具
description: "Hysteria2服务端自带outbounds和ACL两个功能，可以屏蔽地址、按域名换出口、把部分流量交给SOCKS5代理。这篇按官方文档讲清三种出站类型、ACL规则语法和匹配顺序，再说明怎么把WARP本地代理接成出口，以及geoip数据库只在启动时下载这类坑。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2服务端怎么分流？outbounds和ACL写法，以及接WARP的思路",
      "description": "Hysteria2服务端自带outbounds和ACL两个功能，可以屏蔽地址、按域名换出口、把部分流量交给SOCKS5代理。这篇按官方文档讲清三种出站类型、ACL规则语法和匹配顺序，再说明怎么把WARP本地代理接成出口，以及geoip数据库只在启动时下载这类坑。",
      "datePublished": "2026-10-02T21:00:00+08:00",
      "dateModified": "2026-10-02T21:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-outbounds-acl-warp/",
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
          "name": "Hysteria2服务端能做分流吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "能。服务端配置里的outbounds定义出口，acl定义规则，规则按从上到下的顺序匹配，第一条命中的生效。出站类型有direct、socks5、http三种，另外内置direct、reject、default三个出口名。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2的ACL规则怎么写？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "格式是出口名(地址)、出口名(地址, 协议/端口)或出口名(地址, 协议/端口, 劫持地址)。地址可以是IP、CIDR、域名、通配域名、suffix:域名后缀、geoip:国家代码、geosite:分类或all。例如reject(all, udp/443)表示拒绝所有UDP 443连接。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2服务端没写ACL时，配了多个outbounds会怎样？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方文档写明，不使用ACL时，所有连接都只会走outbounds列表里的第一个出站，其余的会被忽略。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2的geoip数据库会自动更新吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不写geoip和geosite路径时，服务端会自动下载数据库到工作目录，只有ACL里至少有一条规则用到它们才会下载。官方文档说目前只在启动时下载一次，geoUpdateInterval要配合外部工具定期重启服务才会生效。"
          }
        }
      ]
    }
  ]
}
</script>

Hysteria2 服务端除了"收到请求就直接发出去"，还可以决定**每个请求从哪里出去、要不要放行**，这就是配置里的 `outbounds`（出口）和 `acl`（规则）。想屏蔽某些地址、让某些网站走 IPv6 或另一台代理、或者给流媒体换一个出口，都靠这两块。这篇按官方文档整理写法，最后讲怎么把 WARP 接进来。

先说明范围：以下字段和规则语法来自官方的 Full Server Config 和 ACL 两页文档，示例是我按文档拼的，**没有在这台机器上跑过**，WARP 那一段尤其只给思路，具体命令请以你装的版本为准。服务端基本配置见[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。

## 先搞清楚：谁在分流

ACL 是写在**服务端**的，处理的是客户端发来的请求。官方说明里，请求带域名时，服务端会**先解析域名，再同时用域名规则和 IP 规则去匹配**，所以一条 IP 规则会命中所有最终解析到那个 IP 的连接，不管客户端发的是域名还是 IP。

这和客户端侧的分流（Clash 规则、sing-box 路由）是两层东西：客户端规则决定"这条流量要不要进 Hysteria2 隧道"，服务端 ACL 决定"进来之后从哪出去"。官方的 2 vs 1 页面提到 2 代**没有客户端 ACL**，分流要在客户端软件里做，见[Hysteria2 是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)。

## outbounds：定义出口

官方支持三种出站类型：

- `direct`：从本机网卡直接出去。
- `socks5`：转给一个 SOCKS5 代理。
- `http`：转给 HTTP/HTTPS 代理。

官方文档里的写法（我把示例主机名换成了占位）：

```yaml
outbounds:
  - name: my_direct
    type: direct
  - name: my_socks
    type: socks5
    socks5:
      addr: 127.0.0.1:1080
      username: 可选
      password: 可选
  - name: my_http
    type: http
    http:
      url: http://用户名:密码@代理地址:8081
      insecure: false
```

几点官方说明：

- `name` 就是 ACL 规则里引用的出口名。
- **不使用 ACL 时，所有连接只走列表里的第一个出站，其余的会被忽略。** 所以光写多个出站、不写 ACL 是不会分流的。
- HTTP/HTTPS 代理在协议层面不支持 UDP，发给 http 出站的 UDP 流量会被拒绝。SOCKS5 出站对 UDP 的情况，文档里没有写，我没有核对，需要代理 UDP 的话先自己测。

### direct 出站可以调的选项

`direct` 下面可以写 `mode`、`bindIPv4`、`bindIPv6`、`bindDevice`、`fastOpen`。其中：

- `mode`：`auto`（默认，IPv4/IPv6 双栈择优）、`64`（优先 IPv6，没有再用 IPv4）、`46`（优先 IPv4）、`6`（只用 IPv6，没有就失败）、`4`（只用 IPv4）。
- `bindIPv4`、`bindIPv6`、`bindDevice` 互斥：要么写前两者（可以只写一个），要么只写 `bindDevice`。

这几个组合起来，就能做出"这个出口只走 IPv6""这个出口绑定某个网卡"之类的出口。

## acl：写规则

规则可以写在配置文件里（`inline`），也可以放进单独的文件（`file`），**两者只能选一个**：

```yaml
acl:
  inline:
    - reject(suffix:v2ex.com)
    - reject(all, udp/443)
    - direct(all)
```

### 语法

每条规则是下面三种格式之一，`#` 开头是注释：

```
出口名(地址)
出口名(地址, 协议/端口)
出口名(地址, 协议/端口, 劫持地址)
```

**地址**可以是：

| 写法 | 含义 |
|---|---|
| `1.1.1.1`、`2606:4700:4700::1111` | 单个 IP |
| `73.0.0.0/8` | CIDR 网段 |
| `example.com` | 域名，**不包含子域名** |
| `*.example.com`、`*.google.*` | 通配域名 |
| `suffix:example.com` | 域名后缀，匹配它和所有子域名 |
| `geoip:cn` | 按国家代码匹配 IP |
| `geosite:netflix` | 按分类匹配域名，支持属性，如 `geosite:google@cn` |
| `all` | 匹配全部，一般放在最后当兜底 |

**协议/端口**：`tcp`、`udp/53`、`tcp/80`、`udp/20000-30000`、`*/443`（TCP 和 UDP 的 443）、`*` 或省略（全部）。

**劫持地址**：命中规则的连接会被改去连这个地址，必须是 IP，不能是域名。

### 匹配顺序和内置出口

- 规则**从上到下**匹配，第一条命中的生效；都没命中，走默认出口（outbounds 列表的第一个）。
- 内置出口始终可用，哪怕 outbounds 是空的：`direct`（默认配置的直连）、`reject`（拒绝连接）、`default`（用列表第一个出站，列表为空时等同 direct）。除非你在 outbounds 里用同名的覆盖它。

所以最常见的用法其实不需要写 outbounds，只用 ACL 屏蔽一些地址，官方示例就有：

```
reject(geoip:cn)
reject(geosite:facebook)
reject(10.0.0.0/8)
reject(172.16.0.0/12)
reject(192.168.0.0/16)
reject(fc00::/7)
```

后面几条是屏蔽内网网段，避免通过代理去访问服务器所在内网。这是我对这几行用途的解读，官方示例只是列了出来。

## 几个常见写法

假设已经定义了 `v4_only`（direct，mode 4）、`v6_only`（direct，mode 6）和一个 `some_proxy`（socks5）：

```
v6_only(suffix:google.com)        # Google 只走 IPv6
v4_only(suffix:twitter.com)       # Twitter 只走 IPv4
some_proxy(ipinfo.io)             # ipinfo.io 交给 SOCKS5 代理
reject(all, udp/443)              # 拒绝 QUIC
reject(all, tcp/25)               # 拒绝 SMTP，防止被拿去发垃圾邮件
direct(all)                       # 其余直连
```

这些都是官方示例里的写法。其中 `reject(all, udp/443)` 要想清楚：它拒绝的是**客户端通过隧道发来的所有 UDP 443 连接**，也就是浏览器的 HTTP/3（QUIC）。被拒绝后浏览器一般会退回 TCP，但这点是我的常识判断，官方没写，你开了之后如果某些应用变慢，先把这条去掉对比。

## 接 WARP：把它当成一个 SOCKS5 出口

Hysteria 官方文档里**没有提到 WARP**，也没有专门的 WARP 出站类型。能确认的是 Hysteria 有 `socks5` 出站，而 Cloudflare 官方文档里 WARP 客户端有一个"本地代理"（Local proxy）模式：只有配置了使用代理的应用才会走 WARP，支持 HTTPS 或 SOCKS5，**目前只在桌面客户端上提供**。

所以接法的思路是：

1. 在服务器上装好 WARP 客户端，让它运行在本地代理模式，监听 `127.0.0.1` 上某个端口。具体命令，Cloudflare 的 Linux 文档里给了注册（`warp-cli registration new`）、连接（`warp-cli connect`）和用 `warp-cli mode --help` 查看可切换模式。**代理模式具体怎么开、默认端口是多少，我没有在官方文档里核对到**，本站的[3x-ui 配置 Warp](https://vpsjq.com/2026/08/30/3x-ui-warp/)、[S-UI 配置 WARP 出站](https://vpsjq.com/2026/09/30/s-ui-warp/)里有面板场景的做法，端口以你实际 `warp-cli` 的输出为准。
2. 在 Hysteria2 的 outbounds 里加一个 socks5 出口，地址填那个本地端口。
3. 在 ACL 里把需要走 WARP 的域名指向这个出口，其余走 direct。

大致像这样（端口、域名都是占位，需要你替换并实测）：

```yaml
outbounds:
  - name: direct_out
    type: direct
  - name: warp
    type: socks5
    socks5:
      addr: 127.0.0.1:你的WARP本地端口

acl:
  inline:
    - warp(geosite:netflix)
    - direct_out(all)
```

注意两点：

- **第一个出站是默认出口**。上面把 `direct_out` 放第一个，没命中规则的流量才不会误走 WARP。
- Cloudflare 文档特别声明：WARP **不提供匿名性，也不能让你假装在另一个国家访问网络**。所以别指望它能解决"换地区解锁"这类需求，它更多的用途是换出口 IP、补 IPv4 或 IPv6，具体效果因目标网站而异，我没有逐个测试。
- 要代理 UDP 的话，前面说了 SOCKS5 出站对 UDP 的支持我没核对，先在小范围内测。

## 三个容易踩的坑

### 坑 1：写了多个出站，却没有规则

官方明确说了：没有 ACL 时只用第一个出站。想分流，必须写规则。

### 坑 2：geoip / geosite 数据库只在启动时下载

规则里用了 `geoip:`、`geosite:`，又没写数据库路径时，服务端会自动下载（来源是官方文档里写的 Loyalsoldier/v2ray-rules-dat）到工作目录，且**只有 ACL 里至少有一条规则用到它们才会下载**。官方文档同时说明：目前**只在启动时下载一次**，`geoUpdateInterval`（默认 168 小时）想真正起作用，需要你用外部工具定期重启服务。也就是说，不重启就永远是启动那天的数据。数据库用的是 v2ray 的 dat 格式。

服务器如果访问不了 GitHub，启动时下载就会失败，这时可以自己下载好文件，再用 `geoip`、`geosite` 字段指定路径。下载失败具体表现为什么，我没有实测，不乱写。

### 坑 3：流量统计 API 别裸奔

和这篇相关的一条官方提醒：配置了 `trafficStats` 却不设 `secret`，任何能访问监听地址的人都能看流量统计、踢用户。官方建议设置 secret，或者至少用 ACL 把用户访问这个 API 的路径挡住。多用户和统计的配法见[多用户配置](https://vpsjq.com/2026/10/02/hysteria2-multi-user/)。

## 排查顺序

1. 规则没生效：先看是不是**写了出站但没写 ACL**；再看规则顺序，是不是前面有条更宽的规则先命中了（比如 `direct(all)` 放在了前面）。
2. 域名规则不生效：`example.com` 不含子域名，要含子域名写 `suffix:example.com` 或通配。
3. geoip、geosite 报错或不更新：对照上面的坑 2。
4. 走了 WARP 出口却连不上：先在服务器上直接用代理端口测试 WARP 本身是否通，再回头查 Hysteria2 的 socks5 配置。
5. 修改后没效果：改完配置要重启服务，重启方式见[升级和卸载](https://vpsjq.com/2026/10/02/hysteria2-upgrade-uninstall/)。

## 没有覆盖的

- ACL 文件（`file`）的完整格式细节：只确认了语法与 inline 相同，没有逐行核对，所以只用了 inline。
- sing-box、Xray 里的路由写法：那是另一套体系，见[sing-box 和 Xray 里怎么配 Hysteria2](https://vpsjq.com/2026/10/02/hysteria2-singbox-xray/)。
- WARP 的具体安装命令、WARP+ 订阅和实际速度：没有实测，不写。
