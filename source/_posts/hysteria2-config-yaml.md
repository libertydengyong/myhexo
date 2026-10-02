---
title: Hysteria2官方脚本装完起不来？手写config.yaml的最小配置
date: 2026-10-02 12:00:00
tags:
  - Hysteria2
  - 配置教程
categories:
  - vps工具
description: Hysteria2官方脚本只装程序不配置，装完必须自己写/etc/hysteria/config.yaml。这篇给出ACME自动证书和自有证书两套最小配置，以及密码、伪装、混淆、带宽几个字段怎么填。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2官方脚本装完起不来？手写config.yaml的最小配置",
      "description": "Hysteria2官方脚本只装程序不配置，装完必须自己写/etc/hysteria/config.yaml。这篇给出ACME自动证书和自有证书两套最小配置，以及密码、伪装、混淆、带宽几个字段怎么填。",
      "datePublished": "2026-10-02T12:00:00+08:00",
      "dateModified": "2026-10-02T12:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-config-yaml/",
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
      "name": "手写Hysteria2服务端config.yaml并启动",
      "step": [
        {
          "@type": "HowToStep",
          "name": "选证书方式",
          "text": "有域名且已解析到服务器，就用acme字段让Hysteria自动申请证书；没有域名或已有证书文件，就用tls字段填cert和key路径。acme和tls只能二选一。"
        },
        {
          "@type": "HowToStep",
          "name": "写入配置文件",
          "text": "编辑/etc/hysteria/config.yaml，写入证书部分、auth密码和masquerade伪装，监听端口默认是UDP 443，不写listen就用默认值。"
        },
        {
          "@type": "HowToStep",
          "name": "启动并查看状态",
          "text": "执行systemctl enable --now hysteria-server.service启动，再用systemctl status hysteria-server和journalctl --no-pager -e -u hysteria-server.service确认没有报错。"
        },
        {
          "@type": "HowToStep",
          "name": "放行UDP端口",
          "text": "系统防火墙和服务商安全组都要放行配置里的UDP端口，只放TCP客户端连不上。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2的config.yaml最少要写哪些字段？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "最少要有证书(acme或tls二选一)和auth认证两部分，listen不写默认监听UDP 443，masquerade伪装可选，不需要抗封锁时可以去掉。"
          }
        },
        {
          "@type": "Question",
          "name": "acme和tls字段能同时写吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不能，官方配置里tls和acme只能二选一。有域名想自动签证书用acme，已经有证书文件或者用自签证书用tls。"
          }
        },
        {
          "@type": "Question",
          "name": "自签证书用tls字段时客户端要怎么设置？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "自签证书不被系统信任，客户端需要打开跳过证书验证(不同客户端叫法不同，有的叫允许不安全连接)，才能连上。用acme申请的真实证书则不需要这一步。"
          }
        }
      ]
    }
  ]
}
</script>

用[官方脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)装完 Hysteria2，`systemctl start` 一下发现起不来，是正常现象：脚本只装程序、放一份示例配置，真正能用的 `config.yaml` 得自己写。好在最小配置很短，十来行就够。配置文件在 `/etc/hysteria/config.yaml`，下面的字段都对照过官方文档。

## 先选证书方式：acme 还是 tls

这是配置里唯一需要先想清楚的事，两个字段**只能二选一**。

**情况一：有域名，已经解析到这台服务器。** 用 `acme`，Hysteria 自己去申请和续期证书：

```yaml
acme:
  domains:
    - your.domain.net
  email: your@email.com

auth:
  type: password
  password: 换成你自己的密码

masquerade:
  type: proxy
  proxy:
    url: https://news.ycombinator.com/
    rewriteHost: true
```

ACME 默认走 HTTP 验证，验证时会用到 80 端口，所以申请证书那段时间要保证 80 端口没被别的程序占着。域名没解析到本机、或者 80 被占，证书会申请失败，这是最常见的起不来原因。

**情况二：没有域名，或者已经有证书文件。** 用 `tls` 填文件路径：

```yaml
tls:
  cert: /etc/hysteria/server.crt
  key: /etc/hysteria/server.key

auth:
  type: password
  password: 换成你自己的密码

masquerade:
  type: proxy
  proxy:
    url: https://news.ycombinator.com/
    rewriteHost: true
```

没有证书的话可以先生成一张自签的：

```bash
openssl req -x509 -nodes -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
  -keyout /etc/hysteria/server.key -out /etc/hysteria/server.crt \
  -subj "/CN=你的域名或IP" -days 3650
```

自签证书不被系统信任，**客户端要打开"跳过证书验证"**（有的客户端叫"允许不安全连接"）才连得上，真实证书不需要这一步。

## 其他字段怎么填

**监听端口 `listen`**：不写就是默认的 `:443`，注意这是 **UDP** 端口。想换端口就加一行，比如 `listen: :8443`。只想监听 IPv4 写 `0.0.0.0:8443`，只监听 IPv6 写 `[::]:8443`。

**认证 `auth`**：上面用的是 `password` 类型，所有客户端共用一个密码，个人使用够了。多个用户想分开管理，官方还支持 `userpass`（用户名加密码）、`http`、`command` 几种类型，多用户的具体配法看[Hysteria2多用户](https://vpsjq.com/2026/10/02/hysteria2-multi-user/)。密码随便挑一个够长的随机字符串，`openssl rand -base64 18` 就能生成。

**伪装 `masquerade`**：别人直接访问你的服务器端口时，Hysteria 会假装成一个正常的 HTTP/3 网站。上面用的 `proxy` 类型会把请求转发到你指定的真实网站，另外还有 `file`（返回本地静态文件）和 `string`（返回固定字符串）两种。如果你不在意抗封锁，这一段可以整个删掉。

**混淆 `obfs`**：可选项，类型是 `salamander`，需要设一个密码，**客户端那边必须填同样的密码**。不确定要不要就先不加，配置越少越不容易出错。

```yaml
obfs:
  type: salamander
  salamander:
    password: 另一个密码
```

**带宽 `bandwidth`**：可选，限制服务端的上下行速度，单位支持 mbps、gbps 等。不写就是不限制。速度慢的问题通常不在服务端这里，排查顺序看[Hysteria2速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)。

## 启动、检查、放行端口

配置存好之后启动并设为开机自启：

```bash
systemctl enable --now hysteria-server.service
```

确认状态和日志：

```bash
systemctl status hysteria-server
journalctl --no-pager -e -u hysteria-server.service
```

以后改了配置，用 `systemctl restart hysteria-server.service` 重启生效。

最后别忘了**放行 UDP 端口**，系统防火墙和服务商安全组两边都要放：

```bash
ufw allow 443/udp
```

只放 TCP 的话客户端是连不上的，具体可以看[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)里的说明。

## 起不来时按这个顺序看

1. **看日志**：`journalctl` 那条命令的报错基本会直接告诉你原因，比如证书申请失败、端口被占用、YAML 缩进错误。
2. **YAML 缩进**：只能用空格，不能用 Tab，同级字段对齐，冒号后面要有空格。
3. **证书文件读不了**：官方脚本默认让服务以 `hysteria` 这个普通用户运行，如果证书文件只有 root 能读，服务会起不来。可以改文件权限，或者按[一键安装脚本那篇](https://vpsjq.com/2026/09/02/hysteria2-one-click/)里说的用 `HYSTERIA_USER=root` 重新装。
4. **端口冲突**：UDP 443 如果被其他程序占用，换一个端口，同时改 `listen` 和防火墙。

如果想用端口范围做端口跳跃，Hysteria 的 `listen` 支持写端口范围，配法看[Hysteria2端口跳跃配置](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)，用 S-UI 的话看[S-UI端口跳跃教程](https://vpsjq.com/2026/09/06/s-ui-port-hopping/)。不想手写配置、想要图形界面的话，用面板更省事，对比可以看 [S-UI 搭建 Hysteria2 节点教程](https://vpsjq.com/2026/09/06/S-UI-%E6%90%AD%E5%BB%BA-Hysteria2-%E8%8A%82%E7%82%B9%E6%95%99%E7%A8%8B/)。

服务端跑起来之后，客户端怎么导入、链接里每个参数对应什么，看[Hysteria2客户端导入和连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

Nginx 占着 80 端口、没法申请证书的处理办法，见[Hysteria2 和 Nginx、Cloudflare](https://vpsjq.com/2026/10/02/hysteria2-nginx-cloudflare-443/)。
