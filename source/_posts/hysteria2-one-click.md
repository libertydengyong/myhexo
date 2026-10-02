---
title: Hysteria2一键安装脚本：官方脚本、老王工具箱、f佬和233boy
date: 2026-09-02 12:00:00
updated: 2026-10-02 12:00:00
tags:
  - Hysteria2
  - 3x-ui
categories:
  - vps工具
description: Hysteria2一键安装脚本汇总：官方脚本、老王工具箱、f佬(fscarmen)和233boy的sing-box脚本，说明各自区别和安装后的验证、UDP放行方法。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2一键安装脚本：官方脚本、老王工具箱、f佬和233boy",
      "description": "Hysteria2一键安装脚本汇总：官方脚本、老王工具箱、f佬(fscarmen)和233boy的sing-box脚本，说明各自区别和安装后的验证、UDP放行方法。",
      "datePublished": "2026-09-02T12:00:00+08:00",
      "dateModified": "2026-10-02T12:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/02/hysteria2-one-click/",
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
      "name": "用一键脚本安装独立Hysteria2",
      "step": [
        {
          "@type": "HowToStep",
          "name": "运行官方安装脚本",
          "text": "执行bash <(curl -fsSL https://get.hy2.sh/)安装Hysteria2，脚本只会装好程序并生成示例配置，还需要手动编辑/etc/hysteria/config.yaml，再用systemctl enable --now hysteria-server.service启动。想要菜单式一键体验，也可以用老王工具箱。"
        },
        {
          "@type": "HowToStep",
          "name": "验证服务是否运行",
          "text": "官方脚本安装的服务名是hysteria-server.service，用systemctl status hysteria-server查看，显示active (running)说明服务在跑，也可以直接把节点导入客户端测试连接速度。"
        },
        {
          "@type": "HowToStep",
          "name": "放行UDP端口",
          "text": "Hysteria2走UDP协议，需要用ufw allow端口号/udp单独放行，只开TCP不够；服务商有安全组的话同样需要在控制台加UDP入站规则。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "独立脚本装的Hysteria2和3x-ui面板配置的有区别吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "使用上没有本质区别，区别在管理方式，独立脚本直接在服务器上管理，3x-ui面板提供图形界面，多节点多用户的情况下面板更方便管理。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2官方安装脚本装完就能用吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不能直接用。官方脚本只安装程序并生成示例配置，需要自己编辑/etc/hysteria/config.yaml写入监听端口、证书和认证密码，再执行systemctl enable --now hysteria-server.service启动服务。"
          }
        }
      ]
    }
  ]
}
</script>

Hysteria2 是基于 QUIC 的代理协议，在高丢包高延迟的网络环境下表现比 TCP 系协议稳定，3x-ui 面板内置了 Hysteria2 支持，可以直接在面板里配置，具体方法参考[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)。如果不想用面板，也可以用一键脚本直接在服务器上安装独立的 Hysteria2。

## 官方安装脚本

最稳妥的是官方文档给的脚本，不依赖第三方：

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

需要注意：这个脚本**只负责安装程序并生成示例配置**，装完服务还起不来，必须手动编辑 `/etc/hysteria/config.yaml`，写入监听端口、证书和认证密码（最小配置怎么写看[这篇](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)），然后再启动：

```bash
systemctl enable --now hysteria-server.service
```

改完配置后用 `systemctl restart hysteria-server.service` 重启，出问题时看日志：

```bash
journalctl --no-pager -e -u hysteria-server.service
```

默认情况下服务以 `hysteria` 这个普通用户运行，如果证书文件权限读不了，可以改成 root 运行：`HYSTERIA_USER=root bash <(curl -fsSL https://get.hy2.sh/)`。卸载用 `bash <(curl -fsSL https://get.hy2.sh/) --remove`，指定版本在命令后面加 `--version 版本号`。升级、备份配置等注意事项看[Hysteria2升级和卸载](https://vpsjq.com/2026/10/02/hysteria2-upgrade-uninstall/)。

## 菜单式一键脚本

不想手写配置的话，可以用第三方整合脚本，老王工具箱、f佬的脚本和 233boy 的脚本是常见的几个，都能在 GitHub 找到。老王工具箱的安装命令：

```bash
wget -qO ssh_tool.sh https://raw.githubusercontent.com/eooce/ssh_tool/main/ssh_tool.sh && chmod +x ssh_tool.sh && ./ssh_tool.sh
```

跑完会出现一个菜单，从菜单里选择安装 Hysteria2 的选项，脚本会自动处理依赖安装和配置。另外两个脚本都是 sing-box 多协议脚本，Hysteria2 只是其中一个协议：

- **f佬（fscarmen）的 Sing-box 全家桶**：仓库在 [GitHub](https://github.com/fscarmen/sing-box)，作者主页在 [GitLab](https://gitlab.com/fscarmen)。支持 Reality、Hysteria2、TUIC、Trojan、AnyTLS 等一堆协议，不需要域名，还带多客户端订阅。安装命令：`bash <(wget -qO- https://raw.githubusercontent.com/fscarmen/sing-box/main/sing-box.sh)`，装完用 `sb` 命令管理。
- **233boy 的 sing-box 脚本**：仓库在 [GitHub](https://github.com/233boy/sing-box)，主打"一条命令添加、修改、查看、删除配置"，可以一键添加 Hysteria2、TUIC、Reality 等。安装和用法看作者的[文档页](https://233boy.com/sing-box/sing-box-script/)，命令以文档为准。

第三方脚本的服务名、配置路径可能和官方脚本不同，装完以脚本输出的提示为准。

安装完之后验证 Hysteria2 是否正常运行，最直接的方式是把节点导入客户端测试连接速度，速度正常说明运行没有问题。官方脚本安装的话也可以检查服务状态：

```bash
systemctl status hysteria-server
```

显示 active (running) 说明服务在跑；用的是第三方脚本的话，服务名以脚本提示为准。

Hysteria2 走的是 UDP 协议，防火墙需要单独放行 UDP 端口，不是只开 TCP 就够了：

```bash
ufw allow 你的端口号/udp
```

如果服务商有安全组（比如甲骨文、AWS），同样需要在控制台手动加 UDP 入站规则，光在系统防火墙放行不够。连不上的时候这是最常见的原因。

独立脚本安装的 Hysteria2 和通过 3x-ui 面板配置的 Hysteria2 在使用上没有本质区别，区别在于管理方式——独立脚本直接在服务器上管理，3x-ui 面板提供图形界面，多节点多用户的情况下面板更方便管理，参考[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)。


用 Docker 部署的做法见[Hysteria2 Docker 部署](https://vpsjq.com/2026/10/02/hysteria2-docker/)。

想先了解协议原理和 1 代、2 代的区别，看[Hysteria2是什么协议](https://vpsjq.com/2026/10/02/hysteria2-what-is-and-v1-vs-v2/)。
