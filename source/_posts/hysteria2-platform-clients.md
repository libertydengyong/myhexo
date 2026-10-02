---
title: "Hysteria2客户端怎么选？Windows、Mac、Linux、安卓、iOS和OpenWrt能确认什么"
date: 2026-10-02 18:30:00
tags:
  - Hysteria2
  - 客户端
  - OpenClash
categories:
  - vps工具
description: "Hysteria2各平台客户端怎么选：官方只提供Windows、macOS、Linux的命令行程序，安卓官方文件不是APK，iOS和OpenWrt官方文档没有写。这篇分开说哪些是官方文档能核对的，哪些只是推断，以及OpenClash（Mihomo内核）怎么用Hysteria2节点。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2客户端怎么选？Windows、Mac、Linux、安卓、iOS和OpenWrt能确认什么",
      "description": "Hysteria2各平台客户端怎么选：官方只提供Windows、macOS、Linux的命令行程序，安卓官方文件不是APK，iOS和OpenWrt官方文档没有写。这篇分开说哪些是官方文档能核对的，哪些只是推断，以及OpenClash（Mihomo内核）怎么用Hysteria2节点。",
      "datePublished": "2026-10-02T18:30:00+08:00",
      "dateModified": "2026-10-02T18:30:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-platform-clients/",
      "author": {"@type": "Organization", "name": "vpsjq.com"},
      "publisher": {"@type": "Organization", "name": "vpsjq.com"}
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2官方有安卓客户端吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方安装文档提供的安卓文件是用NDK编译的Linux ELF可执行文件，不是APK安装包，文档建议使用第三方应用。文档没有给出具体的应用名称。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2官方客户端有图形界面吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方提供的是命令行程序，用config.yaml配置，快速入门里开的是本地SOCKS5和HTTP代理。图形界面需要使用支持Hysteria2的第三方客户端。"
          }
        },
        {
          "@type": "Question",
          "name": "OpenClash支持Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "OpenClash的说明写明它是Mihomo(Clash)客户端，而mihomo从v1.16.0起支持Hysteria2，所以使用Mihomo内核时可以用hysteria2类型的节点。具体的界面操作步骤我没有核对，内核版本过旧时会提示不支持的类型。"
          }
        }
      ]
    }
  ]
}
</script>

搜"Hysteria2 客户端"，会看到一堆各平台的应用推荐。问题是官方文档对第三方应用几乎没有点名，市面上的推荐文章大多没法逐个核对。所以这篇换个写法：**先写官方文档能确认的，再写能从别处推出来的，核对不了的明说。** 服务端怎么搭，看[一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)；拿到链接后怎么填参数，看[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

## 官方文档能确认的

官方安装页列出的是各平台的**命令行可执行文件**：

| 平台 | 官方提供的文件 |
|---|---|
| Windows | `hysteria-windows-amd64.exe`、`-amd64-avx.exe`、`-386.exe`、`-arm64.exe` |
| macOS | `hysteria-darwin-amd64`、`-amd64-avx`、`-arm64`（M1 及更新） |
| Linux | amd64、amd64-avx、386、arm、armv5、arm64、s390x、mipsle、mipsle-sf、riscv64 |
| Android | 文件不是 APK，是 NDK 编译的 Linux ELF 可执行文件，官方建议用第三方应用 |
| iOS、OpenWrt | 官方安装页没有写 |

带 `avx` 的版本要求 CPU 支持 AVX 指令集，不确定就先用不带 avx 的。

官方客户端的快速入门，是用一个 `config.yaml` 在本机开 SOCKS5 和 HTTP 代理：

```yaml
server: your.domain.net:443
auth: Se7RAuFZ8Lzg
bandwidth:
  up: 20 mbps
  down: 100 mbps
socks5:
  listen: 127.0.0.1:1080
http:
  listen: 127.0.0.1:8080
```

运行 `./hysteria-linux-amd64-avx -c config.yaml`（文件名换成你平台的）。注意这只是**本机代理端口**，浏览器或系统要手动指向它才会走代理。`bandwidth` 不要超过线路真实带宽，原因见[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)。官方客户端页面快速入门里只演示了这两种模式；侧边栏提到的 TProxy 等进阶用法，我这次没有核对，不写。

所以：**Windows、macOS、Linux 想用官方客户端，就是命令行加配置文件，没有图形界面。** 想要图形界面，只能用第三方客户端。

## 安卓和 iOS：只能选第三方，我没法替你背书

官方明确说安卓文件不是 APK，建议用第三方应用，但没有点名；iOS 官方根本没写。市面上各个应用对 Hysteria2 的支持情况、什么版本开始支持，我没有逐个核对，也拿不到可靠的官方清单，所以**不推荐具体应用名**，免得写出来过期或者错误。

选的时候可以自己核对三点：

1. 应用的更新说明或文档里有没有明确写 **Hysteria2**（注意不是旧的 Hysteria 1）；
2. 能不能导入 `hysteria2://` 链接，参数对照见[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)；
3. 报"不支持的类型"时，多半是内核或版本太旧，思路见[Clash 报 unsupported proxy type](https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/)。

用 Termux 在手机上跑官方 ELF 文件理论上可行，但我没有验证过，不写步骤。

## OpenWrt：OpenClash 能用 Hysteria2 吗

OpenClash 项目首页写得很明确：它是一个运行在 OpenWrt 上的 **Mihomo(Clash) 客户端**，内核用的是 MetaCubeX 的 mihomo。我查到的最新发布版本是 v0.47.156（2026 年 8 月 10 日）。

而 mihomo 从 v1.16.0 起支持 Hysteria2，官方文档里有 hysteria2 节点的字段说明（`type: hysteria2`、`server`、`port`、`password`、`sni`、`skip-cert-verify`、`ports`、`hop-interval`、`obfs` 等）。所以从这两条事实**推断**：OpenClash 使用 Mihomo 内核、版本够新时，可以使用 hysteria2 节点。节点怎么写，见上面那篇 Clash 的文章。

我没有核对的部分，请自行确认：

- OpenClash 界面里添加节点的具体菜单和选项；
- 你路由器当前装的内核是不是 mihomo、版本多少；
- OpenClash 页面是否会在内核过旧时给出提示。

另外，官方安装页没有 OpenWrt 条目，但列了 `mipsle`、`arm`、`arm64` 等架构的 Linux 文件，所以**理论上**可以在 OpenWrt 上直接跑官方客户端。具体要选哪个架构、怎么做开机启动，我没有实测，不写步骤；而且路由器上跑 UDP 代理，防火墙和转发规则都要自己处理，这块官方也没有写。

## 怎么选

- **只想快速验证服务端通不通**：官方命令行客户端最直接，能排除第三方软件的干扰。
- **日常使用**：选一个明确支持 Hysteria2 的图形客户端，按上面三点自己核对。
- **全屋设备走代理**：OpenClash（Mihomo 内核）是方向，先确认内核版本。
- 连不上：先看[timeout 报错排查](https://vpsjq.com/2026/10/02/hysteria2-timeout-no-recent-network-activity/)。UDP 通路本身有问题的话，回头看[优缺点](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)里的选型。

## 没有覆盖的

具体的第三方应用名称和使用步骤、iOS 各应用的支持情况、OpenClash 的界面操作、Termux 或路由器上直接跑官方客户端的步骤：都没有可靠依据，所以没有写。有实测过的，可以留言补充。
