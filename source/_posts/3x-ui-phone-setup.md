---
title: 手机搭建3x-ui：用Termux连VPS安装，再用手机浏览器管理面板的完整流程
date: 2026-10-07 21:00:00
tags:
  - 3x-ui
  - Termux
  - 手机
categories:
  - vps工具
description: 只有手机也能搭3x-ui：用Termux通过SSH连上VPS，运行官方安装脚本，再用手机浏览器登录面板。依据3x-ui官方安装脚本源码和文档，讲清楚安装时的SSL选项、记下哪些信息、选择仅本机访问时怎么用SSH端口转发，以及断线和安全上要注意的地方。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "手机搭建3x-ui：用Termux连VPS安装，再用手机浏览器管理面板的完整流程",
      "description": "只有手机也能搭3x-ui：用Termux通过SSH连上VPS，运行官方安装脚本，再用手机浏览器登录面板。依据3x-ui官方安装脚本源码和文档，讲清楚安装时的SSL选项、记下哪些信息、选择仅本机访问时怎么用SSH端口转发，以及断线和安全上要注意的地方。",
      "datePublished": "2026-10-07T21:00:00+08:00",
      "dateModified": "2026-10-07T21:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/3x-ui-phone-setup/",
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
      "@type": "HowTo",
      "name": "用手机搭建3x-ui",
      "step": [
        {
          "@type": "HowToStep",
          "name": "用Termux连上VPS",
          "text": "在Termux里执行pkg install openssh安装SSH客户端，再用ssh root@VPS的IP地址连接。"
        },
        {
          "@type": "HowToStep",
          "name": "运行官方安装脚本",
          "text": "执行bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)，按提示选择SSL方式，结束后记下终端打印的用户名、密码、端口、访问路径和访问地址。"
        },
        {
          "@type": "HowToStep",
          "name": "放行端口并用手机浏览器登录",
          "text": "在服务器防火墙和服务商安全组放行面板端口，然后用手机浏览器打开访问地址登录面板。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "只有手机能搭3x-ui吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "能。3x-ui装在VPS上，手机只负责远程操作：用Termux之类的SSH客户端连上VPS运行安装脚本，装完用手机浏览器登录面板管理。官方文档列出的支持系统是各类Linux发行版和Windows，没有写Android，所以不是把3x-ui直接装在手机上运行。"
          }
        },
        {
          "@type": "Question",
          "name": "安装时选了仅绑定127.0.0.1，手机怎么打开面板？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按安装脚本的提示，用SSH端口转发：在Termux里执行ssh -L 2222:127.0.0.1:面板端口 root@服务器IP，保持这个连接，然后用手机浏览器打开http://localhost:2222/访问路径。"
          }
        },
        {
          "@type": "Question",
          "name": "3x-ui面板可以像App一样装到手机主屏幕吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以。官方README写的是面板可以安装为PWA，固定到桌面或手机主屏幕。官方的PWA说明文档提到它是只走网络的PWA，不缓存面板数据、API响应和凭据。"
          }
        }
      ]
    }
  ]
}
</script>

没有电脑，只有一部手机，能不能搭 3x-ui？能，而且步骤并不比电脑上多多少。先说清楚"手机搭建"指的是什么：**3x-ui 装在 VPS 上，手机负责远程操作**，用 Termux 这类 SSH 客户端连上服务器、运行安装脚本，装完用手机浏览器登录面板管理。官方文档列出的支持系统是各类 Linux 发行版和 Windows，没有写 Android，所以**直接把 3x-ui 装在手机本机上运行**这件事我没有核实过，本文不涉及。

先说明依据：我读了 [MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui) 主分支的官方安装脚本 `install.sh`（读到的最新提交是 2026-10-06）、官方文档里的 Installation 和 First Login 页面、README，以及 PWA 说明文档。**我没有真的用手机走完这个流程**，所以手机上的操作细节（比如怎么复制文字）只写一般做法，凡是没验证的地方都会标明。另外这是当前主分支（3.x）的脚本，老版本的提示和默认值可能不同。

<!-- more -->

## 开始前要准备什么

- **一台 VPS**：系统要是官方支持的，Ubuntu、Debian、CentOS、Alpine 等都在列表里（完整列表见 [3x-ui是什么](https://vpsjq.com/2026/10/04/3x-ui-what-is-github-docs/)），能用 root 登录；
- **手机上装好 Termux**，并能用 SSH 连上 VPS。具体步骤本站有现成的教程：[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)；
- **一个稳定的网络**：手机切网络、切后台都可能让 SSH 断线，安装脚本跑到一半断了很麻烦，建议先看 [Termux用SSH连VPS总是断线怎么办](https://vpsjq.com/2026/08/03/termux-ssh-disconnect/) 和 [Termux切后台就断连怎么办](https://vpsjq.com/2026/08/25/termux-background-keep-alive/)，把保活做好；
- **如果想用证书**：安装脚本里选 Let's Encrypt 证书需要服务器的 **80 端口**可以从外网访问（脚本原话："Options 1 & 2 require port 80 open"），所以先确认安全组放行了 80。

## 第一步：连上 VPS

在 Termux 里装 SSH 客户端并连接（详细说明见上面那篇教程）：

```bash
pkg update
pkg install openssh
ssh root@你的VPS的IP地址
```

连上之后，如果担心中途断线，可以先在服务器里开一个 tmux 会话再跑安装脚本，断线后能重新接回去。tmux 的用法见上面讲保活的那篇，这里不展开。

## 第二步：运行官方安装脚本

官方文档给的命令是：

```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

手机上输入长命令容易输错，建议从官方 README 或本站文章里**复制**后粘贴到 Termux，不要手敲。

官方文档说明，脚本安装会**随机生成**用户名、密码和访问路径（也包括端口），并装好 `x-ui` 管理命令和开机自启的服务。

## 第三步：安装过程中会问什么

我读了安装脚本，非无人值守模式下，它会让你选择 SSL 证书的设置方式：

| 选项 | 含义（脚本原文的意思） |
| --- | --- |
| 1 | 域名的 Let's Encrypt 证书，有效期 90 天，自动续期 |
| 2 | **IP 地址**的 Let's Encrypt 证书，有效期只有约 6 天，自动续期。直接回车时默认选这一项 |
| 3 | 自定义证书，要填已有证书文件的路径 |
| 4 | 跳过 SSL。脚本注明这是进阶选项，面板会用**明文 HTTP**，只有放在 Nginx 或 Caddy 反向代理后面，或者通过 SSH 隧道访问时才安全 |

怎么选：

- **没有域名**：选 2，用 IP 证书。要放行 80 端口，证书有效期短但会自动续期；
- **有域名**：选 1，先把域名解析到服务器，再选；证书怎么管见 [3x-ui配置TLS证书教程](https://vpsjq.com/2026/08/30/3x-ui-tls/)；
- **选 4 要小心**：面板在公网上走明文 HTTP，官方文档的警告是**不要把面板用明文 HTTP 暴露在公网上**。如果选 4，脚本会接着问"要不要只绑定到 127.0.0.1"（脚本的建议是绑定），下一节讲这种情况怎么用。

## 第四步：记下登录信息

安装结束时，终端会打印这些内容（脚本里的字段名）：

- `Username`（用户名）、`Password`（密码）；
- `Port`（端口）、`WebBasePath`（访问路径）；
- `Access URL`（访问地址，形如 `https://主机:端口/访问路径`）。

这些信息要**马上记下来**，可以截图，或者在 Termux 里选中文字复制到手机的备忘录。脚本也会把它们写进只有 root 能读的文件 `/etc/x-ui/install-result.env`，万一没记，可以回服务器看这个文件，或者运行 `x-ui` 打开管理菜单，选"查看当前设置"（官方文档写的是菜单里的 11，编号以你的版本为准），也可以直接运行 `x-ui settings`。

注意：本站早期的 [3x-ui安装教程](https://vpsjq.com/2026/04/30/2026-04-30-011/) 里写的是"默认用户名密码都是 admin"。按官方现在的文档，脚本安装会随机生成账号密码，旧版本才有默认的 admin，所以请以终端打印出来的为准；面板如果还在用 `admin` / `admin`，会发出警告，要立刻改掉。

## 第五步：放行端口，用手机浏览器登录

1. 在服务器防火墙和**服务商的安全组**里放行面板端口，不然面板打不开，见 [x-ui面板打不开的常见原因和解决方法](https://vpsjq.com/2026/08/29/xui-panel-not-open/)；
2. 用手机浏览器打开终端里打印的 `Access URL`，注意完整地址包含访问路径，**结尾的 `/` 也要带上**，漏掉路径就打不开；
3. 输入用户名和密码登录。如果界面是英文，见 [3x-ui面板怎么设置中文](https://vpsjq.com/2026/10/02/3x-ui-chinese-language/)。

登录后建议先去面板设置，改成更强的密码、开双重验证、确认证书，各项含义见 [3x-ui面板设置怎么设](https://vpsjq.com/2026/10/07/3x-ui-panel-settings/)。

## 如果选了"仅绑定 127.0.0.1"：用 SSH 端口转发

第三步选了 4 并且回答"绑定 127.0.0.1"，面板就**不能从公网直接访问**，脚本会打印用 SSH 端口转发的办法。在 Termux 里执行（来自脚本的提示，端口和 IP 换成你自己的）：

```bash
ssh -L 2222:127.0.0.1:面板端口 root@服务器IP
```

如果用了密钥登录，加上 `-i 密钥路径`。**保持这个 SSH 连接不要关**，然后用手机浏览器打开：

```text
http://localhost:2222/访问路径
```

这种方式最安全，但每次管理面板都要先连 SSH，适合不常登录面板的人。脚本还提到另一个办法：让 Nginx 或 Caddy 反向代理指向 `127.0.0.1:面板端口`，由它负责 HTTPS，见 [3x-ui用Nginx反向代理隐藏面板](https://vpsjq.com/2026/09/28/3x-ui-nginx-reverse-proxy/)。

## 想少打字：无人值守安装

官方 README 说明，设置环境变量 `XUI_NONINTERACTIVE=1`，脚本会**零提示**装完，随机生成凭据，并写入 `/etc/x-ui/install-result.env`。这对手机很友好，不用在小屏幕上回答一堆问题：

```bash
XUI_NONINTERACTIVE=1 bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

但要注意：我读的脚本里，无人值守模式下 SSL 方式由环境变量 `XUI_SSL_MODE` 决定，取值有 `domain`、`ip`、`none`，**不设置就是 `none`，也就是面板走明文 HTTP 并监听所有网卡**（脚本注释说云镜像必须保持公网可达）。所以用这个模式装完后，要尽快配好证书或者放到反向代理后面，不要长期裸奔。`XUI_SSL_MODE` 搭配哪些其他变量，我没有逐项验证，这里不展开。

## 装完以后，手机上怎么日常管理

- **浏览器**：直接用手机浏览器登录。我读的面板前端源码里有针对手机屏幕的布局（比如出站页有按手机屏幕切换的卡片列表）。官方 README 的社区工具列表里提到一个第三方做的 Android 客户端 3X-UI Manager，我没有用过，不评价；
- **装到主屏幕**：官方 README 说面板可以安装为 PWA，固定到桌面或手机主屏幕，打开后像 App 一样全屏。官方的 PWA 说明文档写明它是**只走网络**的 PWA，不缓存面板数据、API 响应、凭据和 WebSocket 流量，清单里的显示方式是 `standalone`。浏览器安装 PWA 通常要求 HTTPS，这是一般规则，这份文档里没有写，所以最好先把面板配上证书；
- **Telegram 机器人**：想在手机上收通知、查看状态，可以配 Telegram 机器人，见 [3x-ui Telegram 机器人配置教程](https://vpsjq.com/2026/09/06/3x-ui-telegram-bot/)；
- **出问题用 Termux 连回去**：面板打不开、忘了密码时，用 SSH 连上服务器运行 `x-ui` 命令，见 [3x-ui常用命令汇总](https://vpsjq.com/2026/08/30/3x-ui-commands/) 和 [3x-ui 忘记密码怎么办](https://vpsjq.com/2026/09/06/3x-ui-forgot-password/)。

## 手机上操作的几个注意点

- **别在不稳定的网络里装**：安装脚本要下载文件、申请证书，中途断线可能装到一半。脚本里有处理已有安装的逻辑（我没有逐行验证），所以断线后先重新连上，用 `x-ui` 菜单看看状态，不确定的话再重新运行安装命令；
- **复制比手敲可靠**：命令、密码、访问路径都又长又随机，手敲容易错；
- **别用公共 Wi-Fi 登录没有 HTTPS 的面板**：明文 HTTP 上的账号密码可能被截获；
- **纯 IPv6 的 VPS**：有额外的限制，见 [纯IPv6 VPS用3x-ui搭建节点教程](https://vpsjq.com/2026/08/29/ipv6-vps-3xui-node/)。

装好之后建节点，可以接着看 [3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)，Reality 的参数含义见 [Reality协议是什么](https://vpsjq.com/2026/10/07/reality-protocol-explained/)。

## 小结

- "手机搭建"是用手机远程操作 VPS，3x-ui 本身装在 VPS 上；官方文档没有把 Android 列入支持系统；
- 流程：Termux 连 SSH → 运行官方安装脚本 → 选 SSL 方式 → 记下终端打印的账号信息 → 放行端口 → 手机浏览器登录；
- 没有域名选 IP 证书（选项 2），选"跳过 SSL"要配合反向代理或 SSH 隧道；
- 无人值守模式（`XUI_NONINTERACTIVE=1`）省输入，但默认是明文 HTTP，装完要尽快配证书；
- 本文依据官方脚本和文档，没有真的用手机走完全程，手机上的操作细节以实际为准。
