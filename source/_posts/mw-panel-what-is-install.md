---
title: "mw面板（mdserver-web）是什么？安装命令、登录信息和安装时会改动什么"
date: 2026-10-03 00:50:00
tags:
  - mw面板
  - mdserver-web
  - 面板
categories:
  - vps工具
description: "mw面板是开源的mdserver-web，一款仿宝塔界面的Linux面板，用插件管理OpenResty、PHP、MySQL等。这篇按官方README和安装脚本，讲它是什么、安装命令、国内代理地址的选择、脚本会启用防火墙并新建www用户等改动、装完用mw default查登录信息，以及没核对的部分。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "mw面板（mdserver-web）是什么？安装命令、登录信息和安装时会改动什么",
      "description": "mw面板是开源的mdserver-web，一款仿宝塔界面的Linux面板，用插件管理OpenResty、PHP、MySQL等。这篇按官方README和安装脚本，讲它是什么、安装命令、国内代理地址的选择、脚本会启用防火墙并新建www用户等改动、装完用mw default查登录信息，以及没核对的部分。",
      "datePublished": "2026-10-03T00:50:00+08:00",
      "dateModified": "2026-10-03T00:50:00+08:00",
      "url": "https://vpsjq.com/2026/10/03/mw-panel-what-is-install/",
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
      "name": "安装mw面板（mdserver-web）",
      "step": [
        {
          "@type": "HowToStep",
          "name": "用root登录",
          "text": "用root账号SSH登录一台全新的Linux服务器，确认能访问外网，且不存在旧的/www/server/mdserver-web目录。"
        },
        {
          "@type": "HowToStep",
          "name": "运行官方安装脚本",
          "text": "执行bash <(curl --insecure -fsSL https://cdn.jsdelivr.net/gh/midoks/mdserver-web@latest/scripts/install.sh)，国内网络下会让你选择一个GitHub代理地址。"
        },
        {
          "@type": "HowToStep",
          "name": "查看登录信息",
          "text": "安装结束后执行mw default，查看面板地址、用户名和密码。"
        },
        {
          "@type": "HowToStep",
          "name": "放行面板端口",
          "text": "在云服务商安全组放行面板端口，再用浏览器打开面板地址登录。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "mw面板是什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "mw面板指开源项目mdserver-web，作者在README里说明它是仿照宝塔界面自己写的一款简单Linux面板，用插件方式管理OpenResty、PHP、MySQL、MariaDB、MongoDB、PostgreSQL、Redis、Memcached等，另有SSH终端、网站备份等功能，协议为Apache。"
          }
        },
        {
          "@type": "Question",
          "name": "mw面板怎么安装？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方README的初始安装命令是：bash <(curl --insecure -fsSL https://cdn.jsdelivr.net/gh/midoks/mdserver-web@latest/scripts/install.sh)，需要root权限。脚本会创建/www目录和www用户，下载源码并安装依赖，最后启动面板。"
          }
        },
        {
          "@type": "Question",
          "name": "装完mw面板怎么登录？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在服务器上执行mw default，会输出面板地址（含端口和安全路径）、用户名和密码。地址格式是协议://IP:端口加安全路径。端口的兜底默认值是7200，实际以mw default输出为准。云服务商安全组里要自己放行面板端口。"
          }
        },
        {
          "@type": "Question",
          "name": "mw面板和宝塔是一回事吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是。mw面板是独立的开源项目mdserver-web，作者在README里说参考了宝塔的管理界面，但代码是自己写的。两者是不同的软件，不能互相替代安装，也不要同时装在一台机器上。"
          }
        }
      ]
    }
  ]
}
</script>

搜"mw 面板"，多数人是在找一个宝塔之外的免费建站面板。先把名字说清楚：**mw 是 mdserver-web 的简称**，面板自己的命令就叫 `mw`。它和 1Panel 一样是通用的服务器管理面板，不是 x-ui 那类代理面板。

依据说明：下面内容来自 mdserver-web 官方仓库的 README、`cmd.md`、`compatibility.md`、`scripts/install.sh`、`scripts/install/debian.sh` 和面板的管理脚本。**我没有在服务器上实际安装运行**，所以安装时的真实输出、耗时、占用资源都不写。官方 Wiki 这次没有逐页核对。

## mw 面板是什么

README 开头的自述是：一款简单的 Linux 面板，作者感谢宝塔写出这样的 Web 管理软件，复制了后台管理界面，按自己想要的方式写了一版。也就是说，**界面思路参考了宝塔，但是独立项目**，不是宝塔的分支或破解版。协议是 Apache，README 的声明是"不卖、不会监控（统计使用除外）、更不会注入病毒"，这是作者的自述，我没有审计过代码，**判断要自己做**。

README 列出的功能和插件：

- SSH 终端工具、面板收藏、网站备份、插件方式管理；
- OpenResty、PHP（53 到 85）、MySQL、MariaDB、MongoDB、PostgreSQL；
- phpMyAdmin、Memcached、Redis、PureFtpd、Gogs、Rsyncd。

作者在 README 里写了"强烈推荐系统：debian"。`compatibility.md` 里列出的测试系统包括 CentOS 7 到 9 Stream、Debian 10 到 12、Ubuntu 18.04 到 22.04、Fedora、AlmaLinux、Rocky、Arch、openSUSE。这是作者自己的测试表，**我没有逐个验证**，更新的系统版本（比如 Debian 13、Ubuntu 24.04）表里没有，装之前最好先在测试机上试。

## 和 1Panel、宝塔的区别

只讲能从资料确认的：

- **mw 面板靠 OpenResty、PHP 这些软件直接装在系统里**，网站环境由插件安装；1Panel 的 README 强调容器化。两者思路不同，具体哪种更省资源，我没有实测。
- **都不是代理面板**。想搭节点，用 [3x-ui](https://vpsjq.com/2026/04/30/2026-04-30-011/) 这类。
- 1Panel 的介绍见[1Panel 是什么、怎么安装](https://vpsjq.com/2026/10/03/1panel-what-is-install/)。宝塔我这次没有查，不写。

## 安装命令

README 给的初始安装命令（jsDelivr 地址）：

```bash
bash <(curl --insecure -fsSL https://cdn.jsdelivr.net/gh/midoks/mdserver-web@latest/scripts/install.sh)
```

README 还给了几个备用地址（GitHub raw 的 dev 分支、作者自建的 code.midoks.icu）。注意两点：

1. 命令里有 `--insecure`，意思是**不校验 HTTPS 证书**，这是官方命令的写法，我不建议无脑照抄。更稳妥的做法是先把脚本下载下来看一遍，再运行；
2. 官方 README 里的 `dev` 分支地址是开发版，**生产环境用 master 或 jsDelivr 的 latest 地址**。

## 安装脚本会做什么

读 `install.sh` 和 `debian.sh` 能确认的：

- **要 root**，否则退出；
- **目录已存在旧版就拒绝安装**：如果有 `/www/server/mdserver-web/tools.py`，提示存在旧版代码，不能安装；
- **新建 `www` 用户和组**，以及 `/www/server`、`/www/wwwroot`、`/www/wwwlogs`、`/www/backup` 等目录；
- **从 GitHub 下载源码**，并安装 acme.sh（证书申请用）；
- **国内网络要选 GitHub 代理**：脚本用 ipinfo.io 判断地区，列出 gh-proxy.com、ghfast.top 等一批代理地址让你选，回车默认选第一个，选了还会 ping 一下检查是否可用。这些代理是第三方站点，**源码是通过它们下载的**，对安全敏感的机器，要考虑这一点；
- **改写系统防火墙**：在 Debian 的安装脚本里，如果有 ufw 就 **`ufw enable`**，放行 SSH 端口、80/tcp、443/tcp 和 443/udp；没有 ufw 就**安装并启用 firewalld**，放行同样的端口。**这是对系统防火墙的实质改动**，已经有自己防火墙规则的机器要特别留意；
- 注意，**面板自己的端口没有出现在放行列表里**，要自己放行（见下）；
- 装完启动面板，写一个 `mw` 命令。

CentOS、Ubuntu 等系统用的是对应的脚本，我只读了 Debian 的，其他系统的细节没有核对。

## 装完怎么登录

在服务器上运行：

```bash
mw default
```

从管理脚本看，它会输出面板地址、用户名和密码，地址格式是 `协议://IP:端口+安全路径`，并提示在安全组放行端口。其中：

- **端口**：脚本里的兜底默认值是 7200，但如果 `data/port.pl` 存在就用文件里的值。**实际装完是不是 7200，以 `mw default` 输出为准**，我没有实测；
- **安全路径**：地址最后那一段，`mw default` 会一并输出。只输 `IP:端口` 进不去的话，先检查这个；
- **云服务器**的安全组要自己放行面板端口，脚本只会放行系统内的防火墙。

## 常用命令

来自官方 `cmd.md`：

| 命令 | 作用 |
|---|---|
| `mw start / stop / restart` | 启动、停止、重启面板 |
| `mw default` | 显示登录信息 |
| `mw open / close` | 开启、关闭面板 |
| `mw update` | 更新到正式版 |
| `mw dev` / `mw update_dev` | 更新到开发版 |
| `mw mirror` | 切换镜像 |
| `mw db` / `mw redis` | 快捷连接 MySQL、Redis |
| `service mw [start\|stop\|reload\|restart\|status]` | 通过服务管理 |

`mw dev` 会切到开发版，**生产机器别随手运行**。卸载脚本 README 里也有，我没有核对它会清理哪些内容，**卸载前先备份 `/www` 下的网站和数据库**。

## 适合谁

- **适合**：想要宝塔式的网页界面管 PHP 网站、数据库，又希望开源的人；
- **要考虑**：项目主要是个人维护，README 本身说"基本上可以使用，后续会继续优化"，**长期维护和安全响应的情况我没有评估**；脚本会改防火墙、从第三方代理下载源码，装在重要生产机之前要慎重；
- **不适合**：只想跑一个代理节点的小鸡。

## 没有覆盖的

- **实际安装过程和耗时、资源占用**：没有实测；
- **面板默认端口和安全路径**：只读了脚本逻辑，没有在装好的机器上核对；
- **CentOS、Ubuntu 等系统的安装脚本差异**：只读了 Debian 的；
- **官方 Wiki 的内容、插件的使用**：没有逐页核对；
- **和宝塔的功能对比、代码安全性**：没有评估。

同类的面板还有 1Panel，见[1Panel是什么、怎么安装](https://vpsjq.com/2026/10/03/1panel-what-is-install/)。
