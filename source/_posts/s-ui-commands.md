---
title: S-UI命令大全：s-ui管理菜单20项、sui命令行子命令、查看面板地址和重置密码
date: 2026-10-08 10:00:00
tags:
  - S-UI
  - 命令
categories:
  - vps工具
description: S-UI有两层命令：s-ui管理脚本（菜单和start、stop等子命令）和sui程序自带的admin、setting、uri、backup等子命令。依据alireza0/s-ui源码，整理每项的作用、参数和注意事项，包括改端口、改路径、重置密码、备份和BBR菜单做了什么。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI命令大全：s-ui管理菜单20项、sui命令行子命令、查看面板地址和重置密码",
      "description": "S-UI有两层命令：s-ui管理脚本（菜单和start、stop等子命令）和sui程序自带的admin、setting、uri、backup等子命令。依据alireza0/s-ui源码，整理每项的作用、参数和注意事项，包括改端口、改路径、重置密码、备份和BBR菜单做了什么。",
      "datePublished": "2026-10-08T10:00:00+08:00",
      "dateModified": "2026-10-08T10:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/08/s-ui-commands/",
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
          "name": "S-UI怎么打开管理菜单？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "脚本方式安装后，在服务器上直接输入s-ui就会出现S-UI Admin Management Script菜单，选项从0到20。也可以不进菜单，直接用s-ui start、stop、restart、status、enable、disable、log、update、install、uninstall这些子命令。"
          }
        },
        {
          "@type": "Question",
          "name": "S-UI怎么查看面板地址、端口和路径？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在s-ui菜单里选10查看面板设置，它会显示面板端口、路径等并附上面板地址；也可以直接运行/usr/local/s-ui/sui setting -show和/usr/local/s-ui/sui uri。"
          }
        },
        {
          "@type": "Question",
          "name": "S-UI忘记密码怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在服务器上运行s-ui，选5会把管理员重置为用户名admin、密码admin（有确认提示），然后立刻用选项6或/usr/local/s-ui/sui admin -username 新用户名 -password 新密码改成自己的。重置到admin之后到你改掉之前，任何能访问面板的人都能登录，所以要马上改。"
          }
        }
      ]
    }
  ]
}
</script>

装好 S-UI 之后，日常维护基本靠命令行：看面板地址、改端口、重置密码、查日志、备份。S-UI 的命令分**两层**，很多人分不清：一层是 `s-ui` 管理脚本，一层是程序本体 `sui` 自带的子命令。本站 [alireza0/s-ui 是什么](https://vpsjq.com/2026/09/06/s-ui-alireza0-guide/) 里讲"常用命令"时只写了一句"进菜单看一遍就知道"，这篇把它们逐项列清楚。

先说明依据：我读了 [alireza0/s-ui](https://github.com/alireza0/s-ui) 的源码（读到的最新提交是 2026-09-30），主要是管理脚本 `s-ui.sh`、命令行入口 `cmd/` 下的几个文件和安装脚本 `install.sh`。菜单文字在脚本里是英文，中文说明是我翻译的。**我没有实际运行这些命令**，行为按源码描述。这是原版 S-UI，社区分叉版的菜单可能不同，见 [S-UI官方原版和社区分叉版有什么区别](https://vpsjq.com/2026/09/07/s-ui-pro-panel-fork/)。

<!-- more -->

## 两层命令的关系

| | `s-ui` | `sui` |
| --- | --- | --- |
| 是什么 | 管理脚本，安装后放在 `/usr/bin/s-ui` | 面板程序本体，在 `/usr/local/s-ui/sui` |
| 怎么用 | 直接输入打开菜单，或带子命令 | 带子命令：`admin`、`setting`、`uri`、`backup`、`migrate`、`healthcheck` |
| 关系 | 菜单里的"重置密码""设置面板"等项，**内部就是调用 `sui` 的子命令** | 直接操作数据库里的账号和设置 |

## 一、s-ui 管理菜单（0 到 20）

在服务器上输入 `s-ui`，会出现 "S-UI Admin Management Script" 菜单。我读到的选项是：

| 编号 | 菜单（原文） | 作用 |
| --- | --- | --- |
| 0 | Exit | 退出 |
| 1 | Install | 安装（菜单会先检查是否已经安装） |
| 2 | Update | 更新。脚本提示：**强制重装最新版，数据不会丢失**，要确认 |
| 3 | Custom Version | 输入版本号（如 `0.0.1`），安装指定版本 |
| 4 | Uninstall | 卸载，要确认 |
| 5 | Reset admin credentials to default | 把管理员重置为默认账号，见下文警告 |
| 6 | Set admin credentials | 设置新的用户名和密码 |
| 7 | View admin credentials | 查看当前管理员账号 |
| 8 | Reset Panel Settings | 把面板设置重置为默认值，要确认 |
| 9 | Set Panel settings | 设置面板端口、路径、订阅端口、订阅路径，留空表示保持现有值 |
| 10 | View Panel Settings | 查看面板设置，并显示面板地址 |
| 11 | S-UI Start | 启动 |
| 12 | S-UI Stop | 停止 |
| 13 | S-UI Restart | 重启 |
| 14 | S-UI Check State | 查看运行状态 |
| 15 | S-UI Check Logs | 查看日志 |
| 16 | S-UI Enable Autostart | 开启开机自启 |
| 17 | S-UI Disable Autostart | 关闭开机自启 |
| 18 | Enable or Disable BBR | 开启或关闭 BBR，下面单独讲 |
| 19 | SSL Certificate Management | 证书管理 |
| 20 | Cloudflare SSL Certificate | 用 Cloudflare 的 DNS 验证申请证书 |

菜单编号以你安装的脚本版本为准。**不进菜单也能用**的子命令（脚本最后的分支里能看到）：

```bash
s-ui start        # 启动
s-ui stop         # 停止
s-ui restart      # 重启
s-ui status       # 查看状态
s-ui enable       # 开机自启
s-ui disable      # 取消开机自启
s-ui log          # 查看日志
s-ui update       # 更新
s-ui install      # 安装
s-ui uninstall    # 卸载
```

### 重置密码要小心（菜单 5）

选 5 会先打印警告"不建议把管理员重置为默认值"，并要求确认。对应的 `sui admin -reset` 的提示更直白：这会把第一个管理员账号重置为用户名 `admin`、密码 `admin`，**在你改掉之前，任何能访问面板的人都能登录**。源码注释里还解释了为什么加这道确认：以前敲错命令，就会让一个在线的面板变成"全网最广为人知的默认账号"，而且没有任何像警告的输出。所以重置后要**马上**用菜单 6 改成自己的。

### 设置面板（菜单 9）

选 9 会依次问四项：面板端口、面板路径、订阅端口、订阅路径，**留空表示保持现有值**，然后调用 `sui setting` 写入。菜单 9 的脚本里没有"重启"这一步，我没有验证面板是不是会自动读取新设置，保险起见改完后用 `s-ui restart` 重启，再用选项 10 确认。端口和路径的完整改法见 [S-UI修改面板端口和访问路径](https://vpsjq.com/2026/09/30/s-ui-change-port-webpath/)。

### BBR 菜单（18）做了什么

菜单 18 里有 1 开启、2 关闭。我读到的 `enable_bbr`：

1. 如果 `/etc/sysctl.conf` 里已经有 `net.core.default_qdisc=fq` 和 `net.ipv4.tcp_congestion_control=bbr`，就提示已经开启；
2. 否则先按发行版装 `ca-certificates`，Debian 和 Ubuntu 系会先 `apt-get update`；**CentOS 系（centos、almalinux、rocky、oracle）会执行 `yum -y update`，也就是会把整个系统的软件包都升级一遍**，这一点要留意；Alpine 用 `apk`；不认识的系统会直接退出；
3. 把上面两行**追加**到 `/etc/sysctl.conf`，执行 `sysctl -p`，再检查输出是不是 `bbr`。

关闭则是把 `fq` 换成 `pfifo_fast`、`bbr` 换成 `cubic`。脚本没有检查内核版本，内核不支持时会提示开启失败。BBR 本身的原理和验证见 [x-ui、3x-ui和Xray怎么开BBR](https://vpsjq.com/2026/10/04/xui-xray-enable-bbr/)，那篇讲的 3x-ui 菜单写的是单独的 sysctl 配置文件，S-UI 这里是直接改 `/etc/sysctl.conf`，做法不同。

### 证书菜单（19、20）

- 19 证书管理里有：1 申请证书（Get SSL）、2 吊销（Revoke）、3 强制续期（Force Renew）、4 自签名证书（Self-signed Certificate）；
- 20 Cloudflare 证书会让你选凭据类型：脚本推荐的是**限定到 `Zone:DNS:Edit` 的 API Token**，另一种是全局 API Key 加账号邮箱（权限等于整个账号，不推荐）。

证书在面板里怎么用，见 [S-UI面板申请和配置SSL证书](https://vpsjq.com/2026/08/28/s-ui-certificate/)。

## 二、sui 命令行子命令

程序本体的子命令，源码里注册了这几个（`/usr/local/s-ui/sui` 后面接）：

| 子命令 | 作用 |
| --- | --- |
| `admin` | 设置、重置、查看第一个管理员账号 |
| `setting` | 设置、重置、查看面板设置 |
| `uri` | 显示面板地址 |
| `backup` | 创建数据库备份 |
| `migrate` | 从旧版本迁移数据 |
| `healthcheck` | 面板在配置的端口上监听就返回 0，否则非 0 |
| `-v` | 显示面板版本，以及内置的 sing-box 版本 |

### admin：账号

```bash
/usr/local/s-ui/sui admin -show                              # 查看当前账号
/usr/local/s-ui/sui admin -username 新用户名 -password 新密码   # 修改
/usr/local/s-ui/sui admin -reset                             # 重置为 admin/admin，会要求确认
/usr/local/s-ui/sui admin -reset -yes                        # 跳过确认（脚本里用，别手滑）
```

源码里确认提示在没有终端可以询问时会**直接取消**，这样误触发的脚本不会在无人值守时执行重置。

### setting：设置

```bash
/usr/local/s-ui/sui setting -show                     # 查看当前设置
/usr/local/s-ui/sui setting -port 2095                # 面板端口
/usr/local/s-ui/sui setting -path /app/               # 面板路径
/usr/local/s-ui/sui setting -subPort 2096             # 订阅端口
/usr/local/s-ui/sui setting -subPath /sub/            # 订阅路径
/usr/local/s-ui/sui setting -reset                    # 重置全部设置
```

`-show` 会打印面板端口、路径等当前值。各项设置的含义和默认值见 [S-UI面板设置总览](https://vpsjq.com/2026/10/08/s-ui-panel-settings/)。

### uri：面板地址

`sui uri` 按设置拼出面板地址：有证书和密钥就是 `https://`，否则 `http://`；端口是 443（https）或 80（http）时省略端口；优先用设置里的域名，其次用监听地址，都没有就列出本机网卡的地址。

### backup：备份

```bash
/usr/local/s-ui/sui backup -output /root/s-ui-backup.db
/usr/local/s-ui/sui backup -output - > backup.db      # 输出到标准输出
/usr/local/s-ui/sui backup -output /root/s.db -exclude changes,stats
```

`-output` 是必填的，`-` 表示写到标准输出；文件权限是 600（只有所有者可读写）；`-exclude` 可以排除 `changes`（变更记录）和 `stats`（流量统计）两类表，让备份小一点。备份和迁移的完整流程见 [S-UI备份与迁移](https://vpsjq.com/2026/09/30/s-ui-backup-migrate/)。

### healthcheck：给容器用

`sui healthcheck` 从数据库里读出当前配置的端口，然后拨一下这个端口，能连上就退出 0。源码注释说明它用于容器的健康检查，所以**不把端口写死**（用户随时能在面板里改端口，写死会让容器被误判不健康），也**不发 HTTP 请求**，因为面板配了证书就是 HTTPS，没配就是 HTTP，直接拨端口两种情况都适用。

## 常见任务对照

| 想做什么 | 命令 |
| --- | --- |
| 看面板地址、端口、路径 | `s-ui` 选 10，或 `sui setting -show` 加 `sui uri` |
| 忘了密码 | `s-ui` 选 5 重置，再选 6 改掉，见 [S-UI忘记密码怎么办](https://vpsjq.com/2026/09/29/s-ui-forgot-password/) |
| 改端口或路径 | `s-ui` 选 9，或 `sui setting -port ... -path ...`，再 `s-ui restart` |
| 看日志 | `s-ui log` |
| 备份 | `sui backup -output 文件` |
| 升级 | `s-ui update`，见 [S-UI升级](https://vpsjq.com/2026/09/30/s-ui-upgrade/) |
| 卸载 | `s-ui uninstall`（菜单 4） |

和 3x-ui 的命令对比，可以看 [3x-ui常用命令汇总](https://vpsjq.com/2026/08/30/3x-ui-commands/)，两者思路类似，但 S-UI 的命令更少，设置项也更少。

## 安装时的账号是怎么来的

安装脚本跑完后会问"安装或更新完成，出于安全建议修改面板设置，是否继续"（脚本原文意思）：

- 选 **y**：依次问端口、路径、订阅端口、订阅路径，然后问是否设置管理员账号；不设置的话会显示当前账号；
- 选 **n**：如果是**全新安装**，脚本会**随机生成**用户名和密码并打印出来，提醒你自己记好；如果是升级，则保留原有账号。

官方 README 的"默认安装信息"写的是用户名密码都是 admin，端口 2095，路径 `/app/`，订阅端口 2096，订阅路径 `/sub/`。结合安装脚本，实际拿到的账号取决于你装的时候选了什么，**以终端当时打印的为准**，拿不准就用 `sui admin -show` 看。

## 小结

- S-UI 有两层命令：`s-ui` 管理脚本（菜单 0 到 20 加几个子命令）和 `sui` 程序子命令（admin、setting、uri、backup、migrate、healthcheck）；
- 菜单里重置密码、改设置，内部就是调用 `sui`；
- 重置密码会变成 admin/admin，要马上改；改完设置后用 `s-ui restart` 重启最稳；
- BBR 菜单直接改 `/etc/sysctl.conf`，CentOS 系还会先 `yum -y update`；
- 本文依据源码，没有实际运行，菜单文字是我翻译的，以你的脚本版本为准。
