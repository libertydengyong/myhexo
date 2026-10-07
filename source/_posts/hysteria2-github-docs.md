---
title: Hysteria2官方GitHub仓库和文档在哪：apernet/hysteria、中文文档站、安装脚本和支持平台
date: 2026-10-07 14:00:00
tags:
  - Hysteria2
  - GitHub
categories:
  - vps工具
description: Hysteria2的官方GitHub仓库是apernet/hysteria。依据仓库源码和README整理官方文档站、Releases、协议规范的入口，官方安装脚本的参数，命令行子命令和支持的平台，以及和Hysteria 1代的区分。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2官方GitHub仓库和文档在哪：apernet/hysteria、中文文档站、安装脚本和支持平台",
      "description": "Hysteria2的官方GitHub仓库是apernet/hysteria。依据仓库源码和README整理官方文档站、Releases、协议规范的入口，官方安装脚本的参数，命令行子命令和支持的平台，以及和Hysteria 1代的区分。",
      "datePublished": "2026-10-07T14:00:00+08:00",
      "dateModified": "2026-10-07T14:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/hysteria2-github-docs/",
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
          "name": "Hysteria2的官方GitHub仓库是哪个？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "是github.com/apernet/hysteria。仓库名里没有2，README的标题是Hysteria 2；1代的旧版文档单独放在v1.hysteria.network。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2的官方文档在哪？有中文吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按仓库README给出的链接，英文文档是v2.hysteria.network，中文文档是v2.hysteria.network/zh/，1代的旧文档是v1.hysteria.network。仓库里的CHANGELOG.md也只是指向文档站的更新日志页面。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2官方安装脚本有哪些参数？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按仓库里的install_server.sh，参数有-f/--force强制重装、-l/--local指定本地二进制文件、--version指定版本、--remove卸载、-c/--check检查更新、-h/--help帮助。脚本只支持带systemd的Linux。"
          }
        }
      ]
    }
  ]
}
</script>

搜 "hysteria github" 或 "hysteria2 github" 的人，多半想弄清楚几件事：官方仓库是哪个、文档在哪、怎么安装、有没有适合自己系统的版本。这篇把官方入口一次讲清楚，再接着说下一步该读什么。

先说明依据：我拉取了 [apernet/hysteria](https://github.com/apernet/hysteria) 主分支的源码（读到的最新提交是 2026-10-04），读了 README、`LICENSE.md`、`platforms.txt`、安装脚本 `scripts/install_server.sh` 和命令行部分的源码。官方文档站 v2.hysteria.network 和安装地址 get.hy2.sh 在我这里访问不了，所以文档站里的具体内容我没读到，文中只写"README 给出了这些链接"；我也没有在机器上运行过这些命令。GitHub 上的最新版本号和星标数这类实时信息我查不到，文中不写。

<!-- more -->

## 官方入口一览

下面这些链接都出自仓库 README：

| 入口 | 地址 | 说明 |
| --- | --- | --- |
| GitHub 仓库 | https://github.com/apernet/hysteria | 源码、Releases、Issues、Discussions 都在这里 |
| 官方文档（英文） | https://v2.hysteria.network/ | README 里的 "Get Started" |
| 官方文档（中文） | https://v2.hysteria.network/zh/ | README 里的 "中文文档" |
| 1 代旧文档 | https://v1.hysteria.network/ | README 里标注为 legacy（遗留版） |
| Releases | https://github.com/apernet/hysteria/releases | 下载各平台程序，README 的版本徽章也指向这里 |
| 讨论区 | https://github.com/apernet/hysteria/discussions | README 的徽章链接 |
| Telegram 群 | https://t.me/hysteria_github | README 的徽章链接 |

仓库根目录里还有两个值得一提的文件：

- `PROTOCOL.md`：协议规范，想了解协议细节的话看它；
- `CHANGELOG.md`：里面只有一行，指向文档站的更新日志页面 `https://v2.hysteria.network/docs/Changelog/`，更新内容要去那里看。

要注意名字：仓库属于 `apernet` 这个组织，仓库名叫 `hysteria`，没有 "2"；README 的标题是 "Hysteria 2"，说明这个仓库现在维护的就是 2 代。1 代的文档是单独一个站，别和 2 代混着读。两代的区别见 [Hysteria2是什么协议？工作原理和Hysteria 1代的区别](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)。

仓库的许可证：README 的徽章写的是 MIT，`LICENSE.md` 的正文也是 MIT 许可文本。

## 它是什么

README 里的一句话介绍是：一个强大、快速、抗审查的代理（"powerful, lightning-fast, and censorship-resistant proxy"）。README 列出的特点有：

- **多种模式**：SOCKS5、HTTP 代理、TCP/UDP 转发、Linux TProxy、TUN；
- **速度**：基于定制的 QUIC 协议，设计目标是在不稳定、丢包的网络上也能跑得快；
- **抗审查**：协议伪装成标准的 HTTP/3 流量；
- **跨平台**：各主要平台和架构都有构建；
- **易集成**：内置自定义认证、流量统计、访问控制；
- 有规范文档，方便开发者自己做应用。

我读到的客户端配置源码里，对应的模式字段有 `socks5`、`http`、`tcpForwarding`、`udpForwarding`、`tcpTProxy`、`udpTProxy`、`tcpRedirect` 和 `tun`，和 README 说的能对上。想了解这个协议的优缺点，看 [Hysteria2节点的优点和缺点是什么](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)。

## 怎么安装

官方的安装方式是 `get.hy2.sh` 这条命令：

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

仓库里 `scripts/_redirects` 文件只有一行，内容是把根路径 `/` 以 301 跳转到 `/install_server.sh`，结合脚本放在仓库的 `scripts/` 目录下，说明 get.hy2.sh 指向的就是仓库里的 `install_server.sh`（这是我读文件得出的判断，没有访问 get.hy2.sh 验证）。

按这个脚本的帮助信息和源码，它有这些特点：

| 参数 | 作用 |
| --- | --- |
| `-f`、`--force` | 即使已经安装了，也强制重新安装最新版或指定版本 |
| `-l`、`--local <文件>` | 用你指定的本地二进制文件安装，不下载 |
| `--version <版本>` | 安装指定版本，而不是最新版 |
| `--remove` | 卸载 |
| `-c`、`--check` | 检查更新 |
| `-h`、`--help` | 显示帮助 |

- **只支持 Linux，并且要求系统用 systemd**，否则脚本会报错退出；
- 它会把程序安装到 `/usr/local/bin/hysteria`，并在 `/etc/systemd/system` 下放 systemd 服务文件；
- 架构判断里支持 386、amd64、arm、arm64、mipsle、s390x 和 loong64；遇到不支持的架构，脚本会提示可以用环境变量 `ARCHITECTURE` 绕过检查。

这个脚本只负责安装程序，装完还要自己写配置，最小配置怎么写见 [Hysteria2官方脚本装完起不来？手写config.yaml的最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)；升级和卸载的注意事项见 [Hysteria2怎么升级和卸载](https://vpsjq.com/2026/10/02/hysteria2-upgrade-uninstall/)；不想手写配置，可以看 [Hysteria2一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)；Docker 部署见 [Hysteria2 Docker 部署](https://vpsjq.com/2026/10/02/hysteria2-docker/)。

## 命令行里有什么

仓库的命令行部分（`app/cmd`）里注册的子命令，我读到的简介是：

| 命令 | 简介（源码里的说明） |
| --- | --- |
| `hysteria server` | 服务端模式 |
| `hysteria client` | 客户端模式 |
| `hysteria ping 地址` | Ping 模式 |
| `hysteria speedtest` | 测速模式 |
| `hysteria check-update` | 检查更新 |
| `hysteria version` | 显示版本 |
| `hysteria share` | 生成分享链接（Generate share URI） |
| `hysteria cert` | 生成自签 TLS 证书 |

后两个比较实用：`share` 按源码说明是从客户端配置文件生成 `hysteria2://` 分享链接，带 `--qr` 参数还能显示二维码（`--notext` 则不显示文字链接）；`cert` 可以生成自签证书，没有域名时可能用得上。这些命令我只读了源码里的名字和简介，没有逐个运行，具体参数以 `hysteria 命令 --help` 为准。分享链接各参数的含义见 [Hysteria2客户端怎么导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

## 支持哪些平台

仓库的 `platforms.txt` 文件注释写着"控制发布时构建哪些平台和架构组合"，我读到的当前内容是：

| 系统 | 架构 |
| --- | --- |
| Windows | amd64、amd64-avx、386、arm64 |
| macOS | amd64、amd64-avx、arm64 |
| Linux | amd64、amd64-avx、386、arm、armv5、arm64、s390x、mipsle、mipsle-sf、riscv64、loong64 |
| Android | 386、amd64、armv7、arm64 |
| FreeBSD | amd64、amd64-avx、386、arm、arm64 |

注意这些是**命令行程序**，不是带界面的应用，Android 那一项也不是 APK。想在手机或电脑上用图形界面客户端，要用第三方应用，各平台怎么选见 [Hysteria2客户端怎么选](https://vpsjq.com/2026/10/02/hysteria2-platform-clients/)。

## 官方仓库之外的东西

在 GitHub 上搜 hysteria 会看到很多别的项目，要分清：

- **面板里的 Hysteria2**：3x-ui、S-UI 这类面板内置了 Hysteria2 的支持，是面板项目自己做的集成，不是这个仓库的内容，用法见 [3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)；
- **第三方客户端和一键脚本**：不在 apernet/hysteria 里，用之前先确认作者和更新情况；
- **Hysteria Realms**：官方的一项功能，没有公网 IP 的机器也能搭服务端，见 [Hysteria2 Realms是什么](https://vpsjq.com/2026/10/02/hysteria2-realms/)。

## 接下来读什么

按"先懂再装再用"的顺序：

1. [Hysteria2是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)：原理，以及和 1 代的区别；
2. [Hysteria2一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/) 或 [手写config.yaml的最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)：装好服务端；
3. [客户端怎么导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/) 和 [客户端怎么选](https://vpsjq.com/2026/10/02/hysteria2-platform-clients/)：连上；
4. 连不上或太慢：[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/) 和 [timeout: no recent network activity怎么办](https://vpsjq.com/2026/10/02/hysteria2-timeout-no-recent-network-activity/)。

## 小结

- 官方仓库是 `github.com/apernet/hysteria`，文档站是 `v2.hysteria.network`（中文在 `/zh/`），1 代旧文档在 `v1.hysteria.network`；
- 官方安装脚本只支持带 systemd 的 Linux，只装程序，不写配置；
- 命令行有 `server`、`client`、`ping`、`speedtest`、`share`、`cert` 等子命令；
- 官方构建覆盖 Windows、macOS、Linux、Android、FreeBSD，都是命令行程序；
- 本文依据仓库源码和 README，文档站内容没有读到，命令没有实际运行。
