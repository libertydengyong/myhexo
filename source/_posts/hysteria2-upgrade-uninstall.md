---
title: Hysteria2怎么升级和卸载？官方脚本的版本管理与备份注意事项
date: 2026-10-02 15:35:00
tags:
  - Hysteria2
  - 升级卸载
categories:
  - vps工具
description: 官方脚本装的Hysteria2，升级就是重新跑一遍安装脚本，也能指定版本；卸载加--remove。这篇讲查看当前版本、检查更新、GitHub连不上时本地安装，以及动手前为什么要先备份配置。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2怎么升级和卸载？官方脚本的版本管理与备份注意事项",
      "description": "官方脚本装的Hysteria2，升级就是重新跑一遍安装脚本，也能指定版本；卸载加--remove。这篇讲查看当前版本、检查更新、GitHub连不上时本地安装，以及动手前为什么要先备份配置。",
      "datePublished": "2026-10-02T15:35:00+08:00",
      "dateModified": "2026-10-02T15:35:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-upgrade-uninstall/",
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
      "name": "升级或卸载官方脚本安装的Hysteria2",
      "step": [
        {
          "@type": "HowToStep",
          "name": "先备份配置",
          "text": "动手前执行cp -a /etc/hysteria /etc/hysteria.bak，把配置和证书文件备份一份，官方文档没有说明升级或卸载时配置会不会保留。"
        },
        {
          "@type": "HowToStep",
          "name": "升级到最新版或指定版本",
          "text": "重新运行bash <(curl -fsSL https://get.hy2.sh/)升级到最新版，加--version 版本号安装指定版本，GitHub连不上时可以用--local指定本地已下载的二进制文件。"
        },
        {
          "@type": "HowToStep",
          "name": "重启并确认版本",
          "text": "用systemctl restart hysteria-server.service重启服务，再用hysteria version查看当前版本，journalctl查看日志确认没有报错。"
        },
        {
          "@type": "HowToStep",
          "name": "卸载",
          "text": "运行bash <(curl -fsSL https://get.hy2.sh/) --remove卸载，之后检查/etc/hysteria目录是否还在，需要的话自己决定要不要手动清理。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2怎么升级到最新版本？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "用官方脚本安装的话，重新运行一遍bash <(curl -fsSL https://get.hy2.sh/)就是安装或升级到最新版本。升级前建议备份/etc/hysteria，升级后重启hysteria-server服务并用hysteria version确认版本。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么知道Hysteria2有没有新版本？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方命令行里有check-update子命令可以检查更新，hysteria version可以查看当前安装的版本；也可以直接到GitHub的Releases页面看最新版本号和更新说明。"
          }
        },
        {
          "@type": "Question",
          "name": "服务器连不上GitHub，Hysteria2怎么安装或升级？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方脚本支持--local参数，先在能访问GitHub的机器上下载好对应架构的hysteria二进制文件，传到服务器上，再用bash <(curl -fsSL https://get.hy2.sh/) --local /path/to/hysteria-linux-amd64安装。注意脚本本身是从get.hy2.sh下载的，这个地址也要能访问。"
          }
        }
      ]
    }
  ]
}
</script>

Hysteria2 隔一阵子就有新版本，升级和卸载的方法其实很简单，但有两件事官方文档没有说清楚，贸然操作容易出问题：升级会不会动你的配置，卸载会不会连配置一起删。所以动手前先备份一次，花几秒钟就能避免大部分麻烦。这篇针对的是[用官方脚本安装](https://vpsjq.com/2026/09/02/hysteria2-one-click/)的情况，用面板的话版本由面板管理，不适用。

## 动手前先备份

```bash
cp -a /etc/hysteria /etc/hysteria.bak
```

这样配置文件和放在这个目录里的证书都有了备份。官方文档没有明确说明升级或卸载时这个目录会不会被保留，我这里不下结论，先备份是最稳妥的。服务端配置怎么写可以看[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)，备份之后出了问题能直接还原。

## 先看当前版本，再看有没有更新

官方命令行自带两个子命令：

```bash
hysteria version
hysteria check-update
```

前者显示当前安装的版本，后者检查有没有新版本可用。也可以直接去 GitHub 上 Hysteria 的 Releases 页面看最新版本号和更新说明。**跨好几个版本升级之前，建议先看一眼更新说明**，确认有没有配置字段被改名或者废弃，这样升级后服务起不来的时候也知道往哪查。

## 升级：重新跑一遍安装脚本

官方文档里，安装和升级是同一条命令，页面上写的就是"Install or upgrade to the latest version"：

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

想装指定版本，在后面加 `--version`：

```bash
bash <(curl -fsSL https://get.hy2.sh/) --version v2.12.3
```

这里的版本号只是官方文档里的示例，换成你要的版本。需要说明的是，官方文档写的是"升级到指定版本"，没有专门说明能不能用这个参数降级到更旧的版本，要降级的话先自己在测试环境里确认一下，不要直接在正在用的服务器上试。

升级完成后，让服务用上新程序并确认状态：

```bash
systemctl restart hysteria-server.service
hysteria version
journalctl --no-pager -e -u hysteria-server.service
```

官方文档没有写脚本升级之后会不会自动重启服务，所以这里手动重启一次最保险。日志里没有报错，客户端能正常连上，升级就算完成了。

## GitHub 访问不了怎么办

有些服务器直连 GitHub 很慢甚至连不上。官方脚本提供了 `--local` 参数，可以用你自己下载好的二进制文件来安装：

```bash
bash <(curl -fsSL https://get.hy2.sh/) --local /path/to/hysteria-linux-amd64
```

做法是先在能访问 GitHub 的机器上，从 Releases 页面下载对应架构的 `hysteria-linux-amd64`（或者 `arm64` 等），上传到服务器，再把路径填到命令里。注意这条命令里的安装脚本本身仍然是从 `get.hy2.sh` 下载的，这个地址同样需要能访问，只是省掉了下载程序本体这一步。

## 卸载

```bash
bash <(curl -fsSL https://get.hy2.sh/) --remove
```

官方文档只给了命令，没有说明卸载后配置目录会不会保留。卸载完建议自己检查：

```bash
ls /etc/hysteria
systemctl status hysteria-server
```

目录还在、不需要了，就手动删掉；想以后重装复用，就留着。如果之前设置了端口跳跃用的 iptables 手动规则（见[端口跳跃配置](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)），这些规则是你自己加的，卸载程序不会替你清理，需要自己删掉，同样别忘了回服务商安全组里把不用的 UDP 端口规则关掉。

## 升级后连不上，按这个顺序查

1. **看日志**：`journalctl` 的报错通常会直接指出是哪个配置字段有问题。
2. **对照更新说明**：看新版本有没有改动配置格式。
3. **还原备份**：配置出问题就用 `/etc/hysteria.bak` 里的文件还原，重启服务。
4. **客户端和服务端版本差得太多**：客户端也考虑更新到比较新的版本，连接参数怎么对应可以回头看[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

用面板管理节点的话，升级由面板负责，不需要手动处理 Hysteria2 本身，参考[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)。

习惯用 Docker 管理服务的话，看[Hysteria2 Docker 部署](https://vpsjq.com/2026/10/02/hysteria2-docker/)。
