---
title: Hysteria2一键安装脚本：官方脚本、老王工具箱、f佬和233boy
date: 2026-09-02 12:00:00
updated: 2026-10-07 12:00:00
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
      "dateModified": "2026-10-07T12:00:00+08:00",
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
          "name": "Hysteria2一键安装脚本哪个最省事？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "只想快速得到一个Hysteria2节点，老王的Hysteria2.sh最直接：它会装依赖、调用官方脚本、生成自签证书和配置，并输出hysteria2://链接。想一次装多个协议并带订阅，选f佬的Sing-box全家桶；想用一条命令增删改查多个配置，选233boy的sing-box脚本。官方脚本只装程序，装完还要手写配置。"
          }
        },
        {
          "@type": "Question",
          "name": "不用域名能装Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "能。老王脚本和233boy脚本按源码都会在本机生成自签证书，f佬的README写明所有协议均不需要域名。代价是客户端要允许不安全连接或固定证书指纹，导入的链接里一般已经带了insecure=1。"
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

## 先说结论：该选哪个脚本

先说依据：下面的内容来自我读这几个脚本的源码和 README，**没有在机器上逐个实际运行**；脚本会更新，菜单编号和细节以你运行时屏幕上显示的为准。

| 脚本 | 装完能直接用吗 | 要域名吗 | 证书 | 适合谁 |
| --- | --- | --- | --- | --- |
| 官方 `get.hy2.sh` | 不能，只装程序和示例配置，要手写 `config.yaml` | 取决于你自己怎么配证书 | 自己配置 | 想自己掌控配置、不想用第三方脚本 |
| 老王 `Hysteria2.sh` | 能，装完直接输出链接 | 不要 | 脚本生成自签证书 | 只想快速要一个 Hysteria2 节点 |
| f佬 Sing-box 全家桶 | 能，多协议一起装 | 不要（README 写明所有协议均不需要域名） | 我没核对 | 想一次装多个协议，并要订阅链接 |
| 233boy sing-box | 能，一条命令添加 | 不要 | sing-box 生成的自签证书 | 想用命令随时增删改查多个配置 |

简单说：**最快要一个节点选老王**，**要多协议加订阅选 f佬**，**要方便管理多个配置选 233boy**，**想自己掌控就用官方脚本**。

第三方脚本一般需要 root 运行，并且会从网上下载再执行别的脚本，跑之前最好先看一眼内容；不放心的话，用官方脚本加[手写最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)最稳。

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

## 老王工具箱（eooce）：最快出节点

老王工具箱是一个综合脚本，Hysteria2 只是里面的一项。README 给的运行命令是：

```bash
bash <(curl -fsSL ssh_tool.eooce.com)
```

也可以用下载文件的方式：

```bash
wget -qO ssh_tool.sh https://raw.githubusercontent.com/eooce/ssh_tool/main/ssh_tool.sh && chmod +x ssh_tool.sh && ./ssh_tool.sh
```

进去之后按我读到的菜单：主菜单选 **12. 节点搭建合集**，再选 **9. 老王Hysteria2一键脚本**，然后选 **1. 安装Hysteria2**。这个子菜单里还有 2 卸载和 3 更换端口。安装时会问端口，直接回车就用随机端口，脚本会先检查这个 UDP 端口有没有被占用。

菜单里实际执行的就是下面这条，所以也可以跳过菜单直接跑（Alpine 系统走的是另一个脚本）：

```bash
HY2_PORT=你的端口 bash -c "$(curl -L https://raw.githubusercontent.com/eooce/scripts/master/Hysteria2.sh)"
```

不写 `HY2_PORT` 的话，脚本会在 2000-65000 之间随机选一个端口；密码是随机生成的 UUID。

按源码，这个脚本依次做了这些事：

1. 要求用 root 运行，脚本里判断的系统有 Debian、Ubuntu、CentOS、Oracle、RHEL、Fedora、Rocky、AlmaLinux、Alpine，其他系统直接退出；
2. 安装 `openssl`、`unzip`、`wget`、`curl`、`sudo`；
3. **调用官方脚本** `get.hy2.sh` 安装 Hysteria2；
4. 用 `openssl` 生成一张**自签证书**（CN 是 `bing.com`，有效期 36500 天）；
5. 写入 `/etc/hysteria/config.yaml`：监听你选的端口、密码认证、开启 fastOpen，并把伪装（masquerade）指向 `https://bing.com`；
6. 启动 `hysteria-server.service` 并设为开机自启；
7. 输出 V2rayN/NekoBox 用的 `hysteria2://` 链接，以及 Surge 和 Clash 的配置片段。

所以它本质上是"官方脚本加一份预设配置"，装出来的服务名、配置路径和官方脚本一致，后面的验证和排错可以直接按官方脚本的来。

有两点要知道：**脚本没有放行防火墙**，UDP 端口要自己放行（见后面）；它输出的链接带 `insecure=1`，因为用的是自签证书。

## f佬（fscarmen）的 Sing-box 全家桶：多协议加订阅

仓库在 [GitHub](https://github.com/fscarmen/sing-box)，作者主页在 [GitLab](https://gitlab.com/fscarmen)。首次运行：

```bash
bash <(wget -qO- https://raw.githubusercontent.com/fscarmen/sing-box/main/sing-box.sh)
```

之后再进入管理界面只需要输入 `sb`。按 README 的说明：

- 可以单选、多选或全选协议，包括 Reality、Hysteria2、TUIC v5、Trojan、AnyTLS 等，**所有协议均不需要域名**；
- 节点信息会输出到 V2rayN、Clash Verge、小火箭、sing-box 等客户端，订阅会按客户端自动适配；
- 有无交互的快速安装模式，运行参数里 `-l` 是"使用中文快速安装"；
- 针对 Hysteria2，README 的更新记录里提到：支持端口跳跃（装完后可以用 `sb -d` 开关和修改范围）、可以自定义上下行带宽、有 Realm 模式（给没有公网入口的机器用）。

我只读了 README，没有读 `sing-box.sh` 里 Hysteria2 的安装细节，所以它用的证书怎么生成、默认配置长什么样，这里不下结论。端口跳跃的官方做法可以看[Hysteria2端口跳跃怎么配](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)，Realm 看[Hysteria2 Realms是什么](https://vpsjq.com/2026/10/02/hysteria2-realms/)。

## 233boy 的 sing-box 脚本：一条命令管理多个配置

仓库在 [GitHub](https://github.com/233boy/sing-box)。安装命令和完整用法以作者的[文档页](https://233boy.com/sing-box/sing-box-script/)为准。装好之后管理命令就是 `sing-box`，README 里的帮助显示常用的有：

| 命令 | 作用 |
| --- | --- |
| `sing-box add [协议]` | 添加配置，README 列出可以一键添加 Hysteria2、TUIC、Reality、Trojan、AnyTLS 等 |
| `sing-box info [名字]`、`url [名字]`、`qr [名字]` | 查看配置、导出链接、二维码 |
| `sing-box port` / `passwd` | 修改端口、密码 |
| `sing-box del [名字]` | 删除配置 |
| `sing-box restart`、`log` | 重启、查看日志 |

按我读到的源码，Hysteria2 这一项的做法是：

- 证书用 sing-box 自己生成的自签证书，放在 `/etc/sing-box/bin/tls.cer` 和 `tls.key`，**不依赖域名**；
- 密码不指定的话用随机 UUID；
- 导出的链接形如 `hysteria2://密码@地址:端口?alpn=h3&insecure=1&allowInsecure=1&pinSHA256=证书指纹`，除了允许不安全连接，还带了证书的 SHA-256 指纹，支持的客户端可以用它固定证书。

它的服务名、配置路径都是 sing-box 的（配置在 `/etc/sing-box/` 下），和官方脚本的 `hysteria-server.service` 不同。

## 自签证书和 insecure：连接时客户端要怎么设

老王脚本和 233boy 脚本装出来的 Hysteria2 用的是自签证书，所以客户端导入的链接里都有 `insecure=1`。意思是客户端要**允许不安全的证书**（有的客户端叫"跳过证书验证"）才能连上；如果你手动填配置，要记得打开这个选项。链接各参数的含义和手动填写方法见[Hysteria2客户端怎么导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

装完连不上时，先查 UDP 端口有没有放行，再看[Hysteria2报错timeout: no recent network activity怎么办](https://vpsjq.com/2026/10/02/hysteria2-timeout-no-recent-network-activity/)；连上了但很慢，看[Hysteria2速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)。

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
