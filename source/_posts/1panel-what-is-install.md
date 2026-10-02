---
title: "1Panel是什么？和宝塔的区别、一键安装命令和安装时会发生什么"
date: 2026-10-03 00:20:00
tags:
  - 1Panel
  - 面板
  - 安装
categories:
  - vps工具
description: "1Panel是开源的Linux服务器管理面板，用网页界面管理网站、文件、容器、数据库和应用商店。这篇按官方README和安装脚本，讲它是什么、要不要Docker、安装命令、安装时会改动什么、装完怎么登录，以及它和x-ui这类代理面板用途完全不同。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "1Panel是什么？和宝塔的区别、一键安装命令和安装时会发生什么",
      "description": "1Panel是开源的Linux服务器管理面板，用网页界面管理网站、文件、容器、数据库和应用商店。这篇按官方README和安装脚本，讲它是什么、要不要Docker、安装命令、安装时会改动什么、装完怎么登录，以及它和x-ui这类代理面板用途完全不同。",
      "datePublished": "2026-10-03T00:20:00+08:00",
      "dateModified": "2026-10-03T00:20:00+08:00",
      "url": "https://vpsjq.com/2026/10/03/1panel-what-is-install/",
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
      "name": "安装1Panel",
      "step": [
        {
          "@type": "HowToStep",
          "name": "用root登录服务器",
          "text": "用root或具备root权限的账号SSH登录一台全新的Linux服务器，确认能访问外网。"
        },
        {
          "@type": "HowToStep",
          "name": "运行官方安装命令",
          "text": "执行curl -sSL https://resource.1panel.pro/quick_start.sh -o quick_start.sh && bash quick_start.sh。"
        },
        {
          "@type": "HowToStep",
          "name": "按提示设置",
          "text": "依次确认安装目录、是否安装Docker、面板端口、安全入口和面板账号密码，端口和入口默认是随机生成的。"
        },
        {
          "@type": "HowToStep",
          "name": "放行端口并登录",
          "text": "在云服务商安全组放行面板端口，然后用安装结束时输出的地址、用户名和密码登录。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "1Panel是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "1Panel是一款开源的Linux服务器运维管理面板，官方README的介绍是用网页界面管理网站、文件、容器、数据库和LLM，并带应用商店、备份恢复和防火墙、日志审计等功能。开源协议是GPL v3。"
          }
        },
        {
          "@type": "Question",
          "name": "1Panel需要Docker吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方安装脚本会检测服务器上有没有Docker，没有就询问是否安装，可以使用安装包内置的Docker离线安装，也可以在线安装。脚本里的提示还说明Docker问题可能影响应用商店的正常使用。"
          }
        },
        {
          "@type": "Question",
          "name": "1Panel怎么安装？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方README给出的命令是：curl -sSL https://resource.1panel.pro/quick_start.sh -o quick_start.sh && bash quick_start.sh，然后按提示设置安装目录、端口、安全入口和账号密码。国内服务器的安装脚本，官方README指向中文文档页面。"
          }
        },
        {
          "@type": "Question",
          "name": "装完1Panel怎么登录？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "安装结束会显示面板地址、用户名和密码，格式是协议://地址:端口/安全入口。忘记了，用root运行1pctl user-info查看。别忘了在云服务商安全组放行面板端口。"
          }
        }
      ]
    }
  ]
}
</script>

搜"1panel 面板""1p 面板"的人，多半是在教程里看到这个名字，想弄清它是干什么的、能不能装。先说结论：**1Panel 是通用的 Linux 服务器管理面板，不是代理面板**，和 x-ui、3x-ui 用途不同。想搭代理节点，选 3x-ui 这类；想用网页界面管网站、文件、数据库、容器，才是 1Panel 的场景。

依据说明：下面的内容来自 1Panel 官方主仓库的 README、官方 `installer` 仓库的安装脚本（`quick_start.sh`、`install.sh`）和 `1pctl`。**我没有在全新的服务器上完整跑一遍安装**，所以安装时的真实屏幕输出、耗时不写。官方文档站（docs.fit2cloud.com）这次访问很慢，没有逐页核对。国内服务器适用的安装脚本，官方 README 只给了文档页面的指引，我这次没能打开那个页面，所以国内脚本的命令我不写。

## 1Panel 是什么

官方 README 的描述是：1Panel 提供直观的网页界面和 MCP Server，用来管理 Linux 服务器上的网站、文件、容器、数据库和 LLM。具体功能，README 里列的有：

- **主机监控、文件管理、数据库管理、容器管理、LLM 管理**；
- **快速建站**：和 WordPress 深度集成，绑定域名、配置 SSL 证书可以一键完成；
- **应用商店**：收录一批开源应用，方便安装和更新；
- **安全**：通过容器化和安全的应用部署方式减少漏洞暴露，并带防火墙管理和日志审计；
- **一键备份恢复**：支持多种云存储；
- **MCP Server**：官方单独提供，用自然语言执行服务器操作。

开源协议是 GPL v3（README 里的徽章）。官方文档里把版本分成社区版和专业版，两者的功能差异我没有核对，这篇讲的是开源社区版的安装。

## 它和宝塔、x-ui 有什么区别

我不对宝塔下评价，没有核对过它的最新功能，只讲能确定的：

- **1Panel 和宝塔属于同一类**：都是面向建站和服务器运维的网页面板；
- **1Panel 的应用和网站依赖容器**：官方 README 强调了容器化部署，安装脚本也会装 Docker（下面细讲），这点是和很多传统面板不同的地方；
- **x-ui、3x-ui、s-ui 是 xray / sing-box 的代理管理面板**，管的是节点、用户和流量，不是网站和数据库。两类面板可以同时装在一台服务器上，但要注意端口不要冲突，也要考虑小内存机器是否扛得住，这点我没有实测。

## 安装前要知道的

从安装脚本里能确认的：

- **要 root 权限**（`1pctl` 和安装脚本开头都有 root 检查）；
- **支持的 CPU 架构**：`quick_start.sh` 里识别的是 amd64、arm64、armv7、ppc64le、s390x、riscv64，识别不了会直接退出；
- **下载来源**：脚本从 `resource.1panel.pro` 取最新版本号，下载对应的安装包并校验 checksum；
- **安装模式**：默认是 `stable`（稳定版），脚本里还接受 `dev`，**生产环境用稳定版**；
- **需要访问外网**：脚本要下载安装包，Docker 没装时还要下载 Docker。

操作系统支持列表，我没有从官方文档里核对，不在这里给结论，安装前请自己去官方文档确认。

## 安装命令

官方 README 里给出的命令是：

```bash
curl -sSL https://resource.1panel.pro/quick_start.sh -o quick_start.sh && bash quick_start.sh
```

这条会下载 `quick_start.sh` 再执行。执行之前，建议先自己看一遍脚本内容再运行，这是装任何面板脚本的好习惯。

## 安装过程中会问你什么

从 `install.sh` 里读到的流程，大致是下面几步：

1. **安装目录**：默认 `/opt`，面板数据放在其下的 `1panel` 目录。已存在 `core.db` 会提示是否覆盖安装，**别在已有数据的机器上随手重装**；
2. **Docker**：检测不到 Docker 时会问"是否安装"。安装包里如果内置了 Docker，可以选离线安装，选否则在线安装最新版；已经装了 Docker 就跳过。脚本里的提示写明，Docker 服务的问题可能影响应用商店的正常使用。Docker 版本低于 20 时脚本会建议手动升级；
3. **镜像加速**：在国内网络（脚本用 `ipinfo.io` 判断地区）时，可能会提示配置 Docker 镜像加速，并改写 `/etc/docker/daemon.json`，**原有文件会备份为 `daemon.json.1panel_bak`**。这是**会改动你现有 Docker 配置**的一步，已经有自己的 Docker 配置的话，要留意；
4. **端口**：默认随机 10000 到 65534 之间的数字，也可以自己输，被占用会让你重输；
5. **安全入口**：只允许字母、数字、下划线，长度 3 到 30；
6. **账号密码**：设置面板登录用的用户名和密码；
7. **防火墙**：检测到 firewalld 或 ufw 在运行时，会自动放行面板端口；防火墙没启用就跳过。**云服务商的安全组脚本不会替你开**，安装结束会提示你去安全组放行。

脚本还支持非交互安装，用环境变量或参数传入，比如 `PANEL_PORT`、`PANEL_ENTRANCE`、`PANEL_USERNAME`、`PANEL_PASSWORD`、`PANEL_INSTALL_DOCKER`。脚本的帮助里写明：非交互模式下，安装 Docker 和配置镜像加速默认都是"否"，要显式设置。**别把密码直接写进命令行参数**，脚本自己也提示优先用环境变量 `PANEL_PASSWORD`。

## 装完怎么登录

安装结束，脚本会输出面板地址、用户名和密码。地址的格式是：

```
协议://地址:端口/安全入口
```

**必须带上最后的安全入口**，只输 `IP:端口` 通常进不去。云服务器记得先在安全组放行面板端口。忘了地址或密码：

```bash
1pctl user-info
```

打不开的各种情况（安全入口、授权 IP、绑定域名、返回 404 或空白页等），见[1Panel面板打不开怎么办](https://vpsjq.com/2026/10/02/1panel-cannot-open/)。

## 常用管理命令

这些来自 `1pctl` 的帮助输出：

| 命令 | 作用 |
|---|---|
| `1pctl status` | 查看服务状态 |
| `1pctl start/stop/restart all` | 启动、停止、重启（也可指定 core 或 agent） |
| `1pctl user-info` | 查看面板地址和账号信息 |
| `1pctl update password` | 修改密码 |
| `1pctl update port` | 修改端口 |
| `1pctl version` | 查看版本 |
| `1pctl uninstall` | 卸载 |

**`uninstall` 会卸载面板，`restore` 会恢复服务及数据，没弄清楚之前不要运行。**

## 适合谁，不适合谁

- **适合**：想用网页界面管几个网站、数据库、容器，不想每次都敲命令的人；
- **要考虑**：它会装 Docker、跑多个服务，**小内存的机器占用多少，我没有实测，不给数字**；
- **不适合**：只想跑一个代理节点的小鸡，这时官方脚本或 x-ui 类面板更直接，见[3x-ui 安装](https://vpsjq.com/2026/04/30/2026-04-30-011/)。

## 没有覆盖的

- **官方支持的操作系统和最低配置**：没有从文档核对，不给结论；
- **国内服务器适用的安装脚本和命令**：没能打开官方页面，不写；
- **社区版和专业版的功能差异**：没有核对；
- **实际安装耗时、占用的内存和磁盘**：没有实测；
- **应用商店里具体应用的安装和使用**：这篇只讲面板本身。
