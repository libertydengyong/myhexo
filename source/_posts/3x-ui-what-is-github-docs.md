---
title: 3x-ui是什么？官方GitHub仓库、文档入口、功能和优缺点
date: 2026-10-04 15:00:00
tags:
  - 3x-ui
  - Xray
  - 面板
categories:
  - vps工具
description: 3x-ui是MHSanaei基于x-ui做的Xray管理面板。依据官方README整理它是什么、官方GitHub仓库和文档在哪、支持哪些协议和系统，以及用之前要注意的几点。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui是什么？官方GitHub仓库、文档入口、功能和优缺点",
      "description": "3x-ui是MHSanaei基于x-ui做的Xray管理面板。依据官方README整理它是什么、官方GitHub仓库和文档在哪、支持哪些协议和系统，以及用之前要注意的几点。",
      "datePublished": "2026-10-04T15:00:00+08:00",
      "dateModified": "2026-10-04T15:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/3x-ui-what-is-github-docs/",
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
          "name": "3x-ui是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "3x-ui是一个开源的网页控制面板，用来管理Xray-core服务器，可以在网页里添加和管理VLESS、VMess、Trojan、Shadowsocks、Hysteria2等协议的入站、用户、流量和订阅。官方README称它是原版X-UI项目的增强分支。"
          }
        },
        {
          "@type": "Question",
          "name": "3x-ui的官方GitHub仓库和文档在哪？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方仓库是github.com/MHSanaei/3x-ui，README里给出的官方文档站是docs.sanaei.dev，内容包括安装、配置、运维和完整的API参考。"
          }
        },
        {
          "@type": "Question",
          "name": "3x-ui能用在生产环境吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方README的重要提示写的是：本项目仅供个人使用，请不要用于非法用途，也不要用于生产环境。所以它更适合个人自用的节点管理，而不是承载关键业务。"
          }
        }
      ]
    }
  ]
}
</script>

搜"3x-ui"的人，一般想先弄清楚三件事：它到底是什么、官方仓库和文档在哪、值不值得用。这篇依据官方 README 把这几件事讲清楚，再说说用之前要注意什么。

先说明：下面内容来自 [MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui) 仓库的 README 和 LICENSE，以及 `x-ui.sh` 源码。官方文档站 docs.sanaei.dev 我这里访问不了，没读到里面的内容，所以文档站只说"README 里给出了这个入口"，不转述它的具体内容。GitHub 上的最新版本号、星标数这些实时信息我也没法查，文中不写。

<!-- more -->

## 3x-ui是什么

官方 README 对它的定义是：一个先进的、开源的网页控制面板，用来管理 [Xray-core](https://github.com/XTLS/Xray-core) 服务器，界面是多语言的，可以部署、配置和监控多种代理和 VPN 协议。README 同时说明它是原版 X-UI 项目的增强分支，增加了更广的协议支持、更好的稳定性、按客户端的流量统计等功能。

用大白话说：Xray 本身是一个靠 JSON 配置文件运行的程序，手写配置对新手门槛高。3x-ui 在它外面加了一层网页界面，点点鼠标就能添加节点、用户，生成分享链接和订阅，查看流量。x-ui 和 3x-ui 的传承关系见 [x-ui和3x-ui是什么关系，为什么现在教程都推荐3x-ui](https://vpsjq.com/2026/09/06/x-ui-vs-3x-ui-history/)。

## 官方入口在哪

| 入口 | 地址 | 说明 |
| --- | --- | --- |
| GitHub 仓库 | https://github.com/MHSanaei/3x-ui | 源码、Releases、Issues 都在这里 |
| 官方文档 | https://docs.sanaei.dev | README 里标注的文档站，内容包括安装、配置、运维和 API 参考（我没能打开，内容未核对） |
| 许可证 | GPL v3 | README 的徽章和仓库里的 LICENSE 文件都是 GNU GPL v3 |

注意区分：网上有不少第三方的"优化版""汉化版"分支，本站 [所谓的3X-UI优化版](https://vpsjq.com/2025/05/21/66/) 介绍过其中一个（安装地址是 xeefei/3x-ui，不是官方仓库）。第三方分支的更新节奏和改动内容跟官方不同，我没有逐个核对，想要稳妥就认准上面的官方仓库；中文方面，[3x-ui面板怎么设置中文](https://vpsjq.com/2026/10/02/3x-ui-chinese-language/) 里说明了官方版自带简体中文，不一定需要找汉化版。

## 能做什么

下面是 README 的功能列表，我按用途归了类，并附上本站对应的教程：

**协议和传输**

- 入站协议：VLESS、VMess、Trojan、Shadowsocks、WireGuard、AmneziaWG、TUIC v5、Hysteria2、MTProto、HTTP、SOCKS、Dokodemo-door/Tunnel、TUN；
- 传输方式：TCP、mKCP、WebSocket、gRPC、HTTPUpgrade、XHTTP，安全层支持 TLS、XTLS、REALITY；
- 支持 Fallback，一个端口上同时跑多种协议（例如在 443 上同时放 VLESS 和 Trojan）。

对应教程：[VLESS Reality](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)、[普通 VLESS](https://vpsjq.com/2026/08/30/3x-ui-vless/)、[VMess WS+TLS](https://vpsjq.com/2026/09/23/3x-ui-vmess/)、[Trojan](https://vpsjq.com/2026/09/23/3x-ui-trojan/)、[Shadowsocks](https://vpsjq.com/2026/08/31/3x-ui-shadowsocks/)、[Hysteria2](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)、[XHTTP](https://vpsjq.com/2026/09/28/3x-ui-xhttp/)、[TLS 证书](https://vpsjq.com/2026/08/30/3x-ui-tls/)。

**用户和流量管理**

- 按客户端设置流量额度、到期时间、IP 连接数限制，查看在线状态，一键生成分享链接、二维码和订阅；
- 流量统计按入站、按客户端、按出站分别统计，可以重置；
- 内置订阅服务，输出原始、JSON、Clash 格式，按客户端的 User-Agent 自动选择。

对应教程：[多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)、[限制 IP 连接数](https://vpsjq.com/2026/09/29/3x-ui-ip-limit/)、[订阅链接](https://vpsjq.com/2026/08/30/3x-ui-subscription/)、[导入 Clash for Android](https://vpsjq.com/2026/08/30/3x-ui-clash/)、[流量统计不准怎么办](https://vpsjq.com/2026/09/28/3x-ui-traffic-reset/)。

**出站和路由**

- WARP、NordVPN、PIA，自定义路由规则，负载均衡，出站代理链；规则编辑器里可以直接浏览内置的 geosite 和 geoip 分类。

对应教程：[路由规则](https://vpsjq.com/2026/08/29/3x-ui-routing/)、[Warp 出口](https://vpsjq.com/2026/08/30/3x-ui-warp/)、[面板中转](https://vpsjq.com/2026/10/02/xui-panel-relay/)。

**运维和其他**

- Telegram 和 Discord 机器人，用于远程监控和管理；
- 带 REST API，支持有范围、可设过期的令牌，面板内有 API 参考；
- 可安装为 PWA，固定到桌面或手机主屏幕；
- 多节点：在一个面板里管理多台服务器；
- 存储默认 SQLite，也可选 PostgreSQL；
- 界面有 13 种语言（含简体中文和繁体中文），带深色和浅色主题；
- 集成 Fail2ban，用来落实按客户端的 IP 限制。

对应教程：[Telegram 机器人](https://vpsjq.com/2026/09/06/3x-ui-telegram-bot/)、[迁移与备份](https://vpsjq.com/2026/08/27/3x-ui-backup-migrate/)、[配置文件在哪](https://vpsjq.com/2026/10/02/3x-ui-config-file-location/)。

## 怎么安装

README 的快速开始是一条命令：

```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

README 里还写了几点：

- 想装指定版本，在命令后面追加版本标签（README 的例子是 `v3.7.0`，只是示例）；追加 `dev-latest` 会装滚动更新的开发版，不是稳定版；
- 安装过程会随机生成用户名、密码和访问路径；装完后运行 `x-ui` 打开管理菜单；
- 每个发布的文件旁边都有 `.sha256` 校验值，安装脚本和升级脚本会校验，不一致就中止；
- 可以无人值守安装：设置 `XUI_NONINTERACTIVE=1`（或在没有终端时管道运行），会零提示装完，随机凭据写入 `/etc/x-ui/install-result.env`。

完整的安装、配置步骤见本站 [3x-ui安装：MHSanaei版官方脚本与面板配置](https://vpsjq.com/2026/04/30/2026-04-30-011/)，管理菜单里的命令见 [3x-ui常用命令汇总](https://vpsjq.com/2026/08/30/3x-ui-commands/)。

支持的系统（README 原文列出）：Ubuntu、Debian、Armbian、Fedora、CentOS、RHEL、AlmaLinux、Rocky Linux、Oracle Linux、Amazon Linux、Virtuozzo、Arch、Manjaro、Parch、openSUSE、Alpine 和 Windows；架构有 amd64、386、arm64、armv7、armv6、armv5、s390x。

也可以用 Docker：镜像是 `ghcr.io/mhsanaei/3x-ui`，仓库里有 `docker-compose.yml`。镜像里自带 Fail2ban，它用 `iptables` 封禁违规 IP，所以容器需要 `NET_ADMIN` 权限，README 写了 `docker-compose.yml` 已经授权，用 `docker run` 的话要自己加 `--cap-add=NET_ADMIN --cap-add=NET_RAW`。Docker 部署的延迟问题可看 [3x-ui用Docker部署延迟暴涨，问题出在哪](https://vpsjq.com/2026/08/27/3x-ui-docker-latency/)。

## 怎么样：优点和要注意的地方

先说结论：对个人自用、想用网页管理 Xray 节点的人，它功能全、教程多，是常见选择；但下面几点要心里有数。

**优点**

- **功能覆盖广**：主流协议、Reality、XHTTP、订阅、流量统计、机器人都有，上面的功能列表基本能满足个人使用；
- **有简体中文界面**：README 列出了 13 种语言，含中文（简体）；
- **维护中**：项目有 Release 流水线、完整的 README 和文档站（具体更新频率我没法实时查，请自己去仓库看提交记录）；
- **教程多、问题好查**：绝大多数面板教程针对的都是 3x-ui。

**要注意的地方**

- **官方明确不建议用于生产**：README 的重要提示是"本项目仅供个人使用，请勿用于非法用途，也勿用于生产环境"。它适合自用节点，不适合承载关键业务；
- **面板暴露在公网**：面板本身是个网站，安全要自己做好。安装时随机生成的访问路径和账号是第一道防线，进一步可以 [用Nginx反向代理隐藏面板](https://vpsjq.com/2026/09/28/3x-ui-nginx-reverse-proxy/)；
- **版本选择**：README 里的例子和功能列表是 3.x 时代的。本站 [3x-ui面板升级与降级教程](https://vpsjq.com/2026/08/27/3x-ui-upgrade/) 提到，3.0 发布后有用户反映稳定性不如 2.x，社区里认为 2.9.4 比较稳。这是社区反馈，我这次没法逐版本核实，装之前建议先看仓库 Issues，必要时指定版本安装；
- **它只是个管理面板**：真正处理流量的是 Xray-core，面板出问题（比如 [打不开](https://vpsjq.com/2026/08/29/xui-panel-not-open/)、[启动失败](https://vpsjq.com/2026/10/02/xui-panel-start-failed/)）和节点本身出问题，要分开排查；
- **别和别的面板混淆**：想对比同类产品，可以看 [S-UI 和 3x-ui 有什么区别](https://vpsjq.com/2026/09/06/s-ui-vs-3x-ui/)。

## 小结

- 3x-ui 是管理 Xray-core 的开源网页面板，官方仓库是 MHSanaei/3x-ui，README 里给出的文档站是 docs.sanaei.dev；
- 一条命令安装，装完用 `x-ui` 命令管理，功能涵盖主流协议、订阅、流量和用户管理；
- 官方提示仅供个人使用、不要用于生产环境；
- 版本上要留意 3.x 的稳定性反馈，必要时指定版本安装。
