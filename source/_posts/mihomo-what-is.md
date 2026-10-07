---
title: Mihomo是什么：和Clash的关系、官方仓库和文档入口、怎么运行、配置文件结构
date: 2026-10-07 17:00:00
tags:
  - Mihomo
  - Clash
categories:
  - vps工具
description: Mihomo是Clash Meta内核，没有界面，要靠第三方客户端或自己写YAML来用。依据官方仓库和文档源文件，讲清楚它是什么、官方入口、Release和Alpha的区别、怎么在Linux上运行，以及配置文件的基本结构。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Mihomo是什么：和Clash的关系、官方仓库和文档入口、怎么运行、配置文件结构",
      "description": "Mihomo是Clash Meta内核，没有界面，要靠第三方客户端或自己写YAML来用。依据官方仓库和文档源文件，讲清楚它是什么、官方入口、Release和Alpha的区别、怎么在Linux上运行，以及配置文件的基本结构。",
      "datePublished": "2026-10-07T17:00:00+08:00",
      "dateModified": "2026-10-07T17:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/mihomo-what-is/",
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
          "name": "Mihomo是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Mihomo是一个代理内核，README里叫它Meta Kernel，副标题是Another Mihomo Kernel。它本身没有图形界面，功能包括本地HTTP/HTTPS/SOCKS代理、多种协议支持、内置DNS、按规则分流、策略组和远程节点订阅、RESTful API。要用它，一般是通过带界面的第三方客户端，或者自己写YAML配置运行。"
          }
        },
        {
          "@type": "Question",
          "name": "Mihomo的官方文档在哪？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按仓库README，文档在wiki.metacubex.one；文档的源文件在MetaCubeX/meta-docs仓库里。内核代码在github.com/MetaCubeX/mihomo的Meta和Alpha分支。"
          }
        },
        {
          "@type": "Question",
          "name": "Mihomo的Release版和Alpha版有什么区别？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方文档的常见问题写的是：alpha分支是最新提交的分支，meta分支每隔一段时间合并alpha分支的代码，所以meta分支不一定比alpha分支更稳定。文档的下载页同时提供Release稳定版和Alpha版两种下载。"
          }
        }
      ]
    }
  ]
}
</script>

很多人是在 Clash 类客户端的设置里，看到"内核"这一项写着 mihomo 或者 Clash Meta，才开始想弄清楚它到底是什么。这篇依据官方仓库和文档源文件，讲清楚 Mihomo 是什么、和 Clash 什么关系、官方入口在哪、怎么在服务器或路由器上直接运行它，以及配置文件长什么样。至于它对 Hysteria2 和 Reality 的支持，另见 [v2rayNG、Hiddify、Mihomo能导入Hysteria2和Reality吗](https://vpsjq.com/2026/10/07/v2rayng-hiddify-mihomo-hysteria2-reality/)。

先说明依据：我读了 [MetaCubeX/mihomo](https://github.com/MetaCubeX/mihomo) 的 `Meta` 分支（最新提交 2026-09-30）和 `Alpha` 分支（2026-10-02）的 README 与 `main.go`，以及官方文档仓库 [MetaCubeX/meta-docs](https://github.com/MetaCubeX/meta-docs) 的源文件（最新提交 2026-10-03）。文档站 wiki.metacubex.one 我没直接打开，读的是它的源文件。**我没有安装运行过 Mihomo**，文中的配置示例是按文档字段拼出来的，没有验证过，实际使用前请先用后面讲的测试命令检查。

<!-- more -->

## 一句话：它是什么

Mihomo 的 README 标题是 "Meta Kernel"，副标题是 "Another Mihomo Kernel"。它是一个**代理内核**，没有图形界面。README 的功能列表是：

- 本地 HTTP/HTTPS/SOCKS 服务，支持用户验证；
- 支持 VMess、VLESS、Shadowsocks、Trojan、Snell、TUIC、Hysteria 等协议；
- 内置 DNS 服务器，支持 DoH/DoT 上游和 fake IP；
- 按域名、GEOIP、IP-CIDR、进程等规则决定把流量转发给哪个节点；
- 远程策略组，支持自动回退、负载均衡和按延迟自动选择；
- 远程节点提供者，可以远程获取节点列表而不用写死在配置里；
- 基于 Netfilter 的 TCP 重定向，可以用 `iptables` 部署在网关上；
- 完整的 HTTP RESTful API 控制接口。

README 还提到一个官方的网页面板 [metacubexd](https://github.com/MetaCubeX/metacubexd)。

## 和 Clash 是什么关系

README 的致谢（Credits）里第一项是 `Dreamacro/clash`，也有 sing-box、v2ray-core 等；官方文档里给出的 systemd 服务文件的描述是 "mihomo Daemon, Another Clash Kernel"。结合 README 的写法，可以看出 Mihomo 是在 Clash 基础上发展出来的另一个内核，也就是人们常说的 Clash Meta 内核。

这里要分清两件事：

- **原版 Clash 内核**已经不再更新。站内 [Clash报unsupported proxy type hysteria2怎么办](https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/) 里查过，原作者仓库当时已经访问不到；
- 很多客户端界面上叫"Clash"，里面装的其实是 Mihomo 内核。

所以"我用的是 Clash"这句话本身说不清楚，真正要看的是**你的客户端里装的是哪个内核、哪个版本**。

另外 README 的许可证部分写的是 GPL-3.0，并且额外规定：任何与 MetaCubeX 无关的下游项目，名字里不得包含 `mihomo` 这个词。

## 官方入口

| 入口 | 地址 | 说明 |
| --- | --- | --- |
| 内核仓库 | https://github.com/MetaCubeX/mihomo | 内核代码在 `Meta` 和 `Alpha` 分支 |
| Releases | https://github.com/MetaCubeX/mihomo/releases | 下载预编译文件 |
| 官方文档 | https://wiki.metacubex.one/ | README 里给出的文档地址 |
| 文档源文件 | https://github.com/MetaCubeX/meta-docs | 文档的 Markdown 源文件 |
| 网页面板 | https://github.com/MetaCubeX/metacubexd | README 里推荐的面板 |
| 配置完整示例 | 仓库里的 `docs/config.yaml` | README 指向 Alpha 分支，文档里指向 Meta 分支 |

有一个我这次遇到的情况要提醒：我通过代理 `git clone` 这个仓库时，默认拿到的 `main` 分支里是一个**无关的 Python 项目**（说明里写的是解析《崩坏：星穹铁道》数据的库），不是内核代码。内核代码在 `Meta` 和 `Alpha` 这两个分支上。这是我这次操作的观察，仓库设置以后可能会变；如果你要看源码或自己编译，要明确指定分支，比如 `git clone -b Meta ...`，不要想当然地认为默认分支就是内核。

## Release、Meta 和 Alpha 怎么区别

官方文档的常见问题里有两条：

1. **alpha 和 meta 分支的区别**：alpha 分支是最新提交的分支，meta 分支每隔一段时间合并 alpha 的代码，所以 meta 分支**不一定比 alpha 分支更稳定**；
2. **该下载哪个文件**：Release 里的文件名包含程序名（`mihomo`）、操作系统（android、darwin、freebsd、linux、windows 等）、架构（386、amd64、arm32v7、arm64 等）、编译方式和分支，还有提交的 git hash。其中 `v1`、`v2`、`v3` 仅适用于 AMD64 平台，用来标记 CPU 指令集等级；`go120` 表示用 Go 1.20 编译，是为了兼容特定的系统或架构。

文档的下载页同时提供两类下载：**Release（稳定版）**，以及 **Alpha**（来自 `Prerelease-Alpha` 这个预发布标签）。想稳妥就选 Release。文档里列了 Windows、Linux、macOS、FreeBSD、Android 的二进制文件，Linux 还有 deb 和 rpm 包。

## 它不是客户端：第三方客户端从哪找

官方文档里有一页"三方工具/客户端"，开头就说明：这些工具或客户端都使用或带有 mihomo 内核，官方**并不直接控制**它们的开发，它们未必包含内核最新的功能和修复，非内核产生的问题请反馈给对应的第三方项目。

页面按平台分了几类：Windows、macOS、Linux、Android、iOS、Merlin 和 OpenWrt 固件等，每一项带一个"维护状态"，有的备注"不开源"或"前端开源，构建不可复现"。举几个例子，状态是文档当前页面里的标注：

| 平台 | 举例（文档的维护状态标注） |
| --- | --- |
| Windows | clash-verge-rev（维护中）、sparkle（维护中）、v2rayN（维护中）、clash-verge（停止维护）、clashN（停止维护） |
| Android | FlClash（维护中）、其他若干个 |
| OpenWrt | OpenClash（维护中） |

我不在这里推荐具体哪个，因为我没有逐个用过，这页状态也会变化，选之前以文档页面最新内容和各项目自己的仓库为准。

## 怎么直接运行（Linux）

官方文档里给了用 systemd 跑成服务的方法，步骤是：

1. 从 Releases 下载对应的二进制文件，重命名为 `mihomo`，放到 `/usr/local/bin/`；
2. 配置文件放到 `/etc/mihomo`；
3. 创建服务文件 `/etc/systemd/system/mihomo.service`。

文档给出的服务文件内容：

```ini
[Unit]
Description=mihomo Daemon, Another Clash Kernel.
After=network.target NetworkManager.service systemd-networkd.service iwd.service

[Service]
Type=simple
LimitNPROC=500
LimitNOFILE=1000000
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
Restart=always
ExecStartPre=/usr/bin/sleep 1s
ExecStart=/usr/local/bin/mihomo -d /etc/mihomo
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

然后执行：

```bash
systemctl daemon-reload
systemctl enable mihomo
systemctl start mihomo
systemctl status mihomo
journalctl -u mihomo -o cat -e
```

文档说明，`systemctl reload mihomo` 可以重新加载配置。

命令行参数我读了 `main.go`，常用的有：

| 参数 | 含义（源码里的说明） |
| --- | --- |
| `-d` | 设置配置目录 |
| `-f` | 指定配置文件 |
| `-t` | 测试配置并退出 |
| `-v` | 显示当前版本 |
| `-ext-ctl`、`-secret`、`-ext-ui` | 覆盖外部控制接口地址、API 密钥、面板目录 |

所以改完配置，先用 `mihomo -t -d /etc/mihomo` 测试一下再重启服务会更稳（`-t` 的含义来自源码说明，我没有实际运行）。`mihomo -v` 可以查看版本，这也是判断自己内核够不够新的办法。

## 配置文件长什么样

官方文档把配置分成六块：**流量入站**、**路由规则**、**出站代理**、**DNS**、**策略组**，外加完整示例。配置是 YAML 格式，风格和 Clash 一致。常用的全局字段（来自"全局配置"页）：

| 字段 | 含义 |
| --- | --- |
| `allow-lan` | 是否允许局域网内其他设备通过代理端口上网 |
| `bind-address` | 允许哪个地址访问，`"*"` 表示绑定所有 IP |
| `authentication` | 对 http、socks、mixed 代理设置用户名密码 |
| `mode` | 运行模式：`rule` 规则、`global` 全局代理、`direct` 全局直连，默认 `rule` |
| `mixed-port`、`port`、`socks-port` | 代理端口，文档示例分别是 7892、7890、7891 |

注意 `allow-lan: true` 会让局域网里的设备都能用你的代理端口，如果机器暴露在公网，要配合 `authentication` 和防火墙。

按文档里的字段拼一个最小示例（**未运行验证**，用前请先 `-t` 测试，节点信息要换成你自己的）：

```yaml
mixed-port: 7892
mode: rule

proxies:
  - name: hy2-node
    type: hysteria2
    server: 你的服务器地址
    port: 443
    password: 你的密码
    sni: 你的sni
    skip-cert-verify: false

proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - hy2-node

rules:
  - GEOIP,CN,DIRECT
  - MATCH,Proxy
```

几块的要点：

- **出站代理（`proxies`）**：官方文档的 `proxies` 目录里有这些类型：`anytls`、`hysteria`、`hysteria2`、`masque`、`mieru`、`shadowquic`、`snell`、`ss`、`ssr`、`ssh`、`sudoku`、`tailscale`、`trojan`、`trusttunnel`、`tuic`、`vless`、`vmess`、`wg`、`zerotier`、`openvpn`、`easytier`，以及 `http`、`socks`、`direct`、`dns` 等。它比 README 的功能列表更新更全，以文档为准；
- **策略组（`proxy-groups`）**：类型有 `select`（手动选择）、`url-test`（自动测速选择）、`fallback`（故障回退）、`load-balance`（负载均衡）、`relay`（链式）；
- **路由规则（`rules`）**：从上到下匹配，文档示例里的规则类型包括 `DOMAIN`、`DOMAIN-SUFFIX`、`GEOSITE`、`IP-CIDR`、`GEOIP`、`DST-PORT`、`PROCESS-NAME`、`RULE-SET` 等，最后用 `MATCH` 兜底；
- **节点订阅（`proxy-providers`）**：可以远程拉取节点列表，文档示例里有 `type: http`、`url`、`path`、`interval`（秒）和 `health-check` 等字段。

Hysteria2 节点各字段的含义，见 [v2rayNG、Hiddify、Mihomo能导入Hysteria2和Reality吗](https://vpsjq.com/2026/10/07/v2rayng-hiddify-mihomo-hysteria2-reality/) 里的表格；Reality 节点的参数见 [Reality协议是什么](https://vpsjq.com/2026/10/07/reality-protocol-explained/)。

## 导入节点时常见的问题

- **提示不认识 hysteria2 类型**：多半是内核太旧，见 [Clash报unsupported proxy type hysteria2怎么办](https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/)；
- **从 3x-ui 订阅导入**：见 [3x-ui订阅链接导入Clash for Android方法](https://vpsjq.com/2026/08/30/3x-ui-clash/)；
- **Reality 节点连不上**：Mihomo 官方文档对较新版本的 Xray 内核有兼容性警告，详细见上面那篇客户端支持情况里的说明。

## 小结

- Mihomo 是代理内核，不是客户端，很多叫"Clash"的客户端里装的就是它；
- 文档是 wiki.metacubex.one，内核代码在 `Meta` 和 `Alpha` 分支，不要只看默认分支；
- 想稳妥选 Release，meta 分支不一定比 alpha 更稳定；
- 直接运行用 `mihomo -d 配置目录`，改配置先用 `-t` 测试；
- 本文依据仓库和文档源文件，我没有运行过 Mihomo，配置示例未验证，客户端的维护状态以文档页面当前内容为准。
