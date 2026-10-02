---
title: Hysteria2客户端怎么导入连接？hy2链接各参数含义和手动填写对照
date: 2026-10-02 15:00:00
tags:
  - Hysteria2
  - 客户端
categories:
  - vps工具
description: 服务端搭好后拿到一串hy2://链接，里面每个参数对应客户端的哪个选项？这篇逐项拆解，附手动填写对照表、官方命令行客户端的最小配置，以及导入后连不上的排查顺序。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2客户端怎么导入连接？hy2链接各参数含义和手动填写对照",
      "description": "服务端搭好后拿到一串hy2://链接，里面每个参数对应客户端的哪个选项？这篇逐项拆解，附手动填写对照表、官方命令行客户端的最小配置，以及导入后连不上的排查顺序。",
      "datePublished": "2026-10-02T15:00:00+08:00",
      "dateModified": "2026-10-02T15:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-client-import/",
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
      "name": "把Hysteria2节点导入客户端并连接",
      "step": [
        {
          "@type": "HowToStep",
          "name": "拿到分享链接",
          "text": "面板里点节点的二维码或链接图标，或者按服务端配置自己拼一条hysteria2://密码@域名或IP:端口/?参数#名称格式的链接，hy2://是等价的简写。"
        },
        {
          "@type": "HowToStep",
          "name": "导入客户端",
          "text": "复制链接，在支持Hysteria2的客户端里选从剪贴板导入或扫描二维码；客户端不支持链接导入时，就按链接各部分手动填写服务器、端口、密码、SNI等字段。"
        },
        {
          "@type": "HowToStep",
          "name": "按证书类型设置验证选项",
          "text": "服务端用自签证书，客户端要打开跳过证书验证(链接里对应insecure=1)；用真实域名证书则保持关闭。服务端开了obfs混淆的话，客户端必须填相同的混淆类型和密码。"
        },
        {
          "@type": "HowToStep",
          "name": "测试连接",
          "text": "连接后访问一个能显示出口IP的网站，确认IP变成服务器的IP；连不上就按UDP端口、证书验证、混淆密码这几项依次排查。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "hy2://和hysteria2://链接有区别吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "没有区别，官方URI规范里这两种写法都被接受，hy2://只是hysteria2://的简写，客户端导入时按同一个格式解析。"
          }
        },
        {
          "@type": "Question",
          "name": "链接里的insecure=1是什么意思，要不要保留？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "insecure=1表示客户端不验证服务端证书，服务端用自签证书时需要它才能连上。如果服务端用的是域名申请的真实证书，应该去掉或设为0，保持证书验证开启更安全。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2客户端导入后连不上怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "按顺序检查：服务器防火墙和服务商安全组是否放行了配置端口的UDP；证书类型和客户端的验证选项是否匹配；服务端若开了obfs混淆，客户端的混淆类型和密码是否一致；SNI是否和证书域名对应；最后看服务端journalctl日志有没有报错。"
          }
        }
      ]
    }
  ]
}
</script>

服务端搭好之后，面板或者脚本会给你一条这样的链接：

```
hysteria2://密码@your.domain.net:443/?sni=your.domain.net&insecure=0#我的节点
```

很多人把它整条复制进客户端就完事了，导入失败或者连不上时却不知道该改哪里。这条链接其实就是把客户端要填的字段拼在了一起，拆开看一遍，以后不管用哪个客户端都能对上号。服务端那边的配置如果还没写，先看[手写 config.yaml 的最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。

## 链接各部分是什么

官方的 URI 规范里，格式是 `hysteria2://[认证]@主机[:端口]/?参数#名称`，`hy2://` 和 `hysteria2://` 两种写法都认，只是简写区别。

| 链接里的部分 | 含义 | 客户端里对应的选项 |
|---|---|---|
| `@` 前面的字符串 | 认证密码（服务端 `auth` 里设的那个） | 密码 / Auth |
| 主机 | 服务器域名或 IP | 服务器地址 |
| 端口 | 不写默认 443，这是 **UDP** 端口 | 端口 |
| `sni=` | TLS 握手时用的服务器名 | SNI / 服务器名称 |
| `insecure=1` | 不验证服务端证书 | 跳过证书验证 / 允许不安全连接 |
| `obfs=salamander` | 混淆类型 | 混淆 |
| `obfs-password=` | 混淆密码，必须和服务端一致 | 混淆密码 |
| `pinSHA256=` | 证书指纹校验 | 证书指纹 |
| `#` 后面 | 节点备注名，不影响连接 | 节点名称 |

另外官方规范里端口那一栏还支持"多端口"写法，用来做端口跳跃，这部分可以看 [S-UI 端口跳跃配置教程](https://vpsjq.com/2026/09/06/s-ui-port-hopping/)。如果认证用的是 `userpass` 类型，`@` 前面要写成 `用户名:密码`，密码里有特殊字符的话需要做百分号转义，否则链接会被解析错。

## 导入到客户端

主流的支持 Hysteria2 的客户端有 Clash Meta 系、sing-box 系、NekoBox，v2rayN 的部分版本也支持，导入前先确认你用的版本带 Hysteria2。具体按钮名称和菜单位置每个客户端、每个版本都不太一样，我这里不逐个写界面步骤，通用的思路只有两条：

1. **整条导入**：复制那条 `hy2://` 链接，客户端里找"从剪贴板导入"，或者面板里点二维码用手机扫。
2. **手动填写**：客户端不认链接的话，新建一个 Hysteria2 节点，把上面表格里的各项对着填进去。

## 两个最容易填错的选项

**证书验证（insecure）**：这个要看服务端到底用的哪种证书。服务端用 `tls` 字段配的自签证书，客户端要打开跳过证书验证，链接里就是 `insecure=1`；服务端用 `acme` 申请的真实域名证书，就不需要打开，打开了反而降低了安全性。官方文档里也建议如果非要用 insecure，最好配合 `pinSHA256` 指纹校验一起用，这样至少能确认连的是你自己的服务器。

**混淆（obfs）**：服务端配置里加了 `obfs`，客户端就**必须**填同样的类型和密码，少填、填错都会直接连不上，而且报错不一定会明确告诉你是混淆的问题。服务端没开混淆的话，客户端这几项留空。

## 电脑上用官方命令行客户端测试

怀疑是客户端软件的问题时，用官方命令行客户端测一下最干净。准备一个 `config.yaml`：

```yaml
server: your.domain.net:443
auth: 你的密码

socks5:
  listen: 127.0.0.1:1080
http:
  listen: 127.0.0.1:8080
```

用自签证书的话，再加上这一段：

```yaml
tls:
  insecure: true
```

运行官方二进制文件（`-c` 可以指定配置文件路径），它会在本地开一个 SOCKS5 端口 1080 和一个 HTTP 代理端口 8080，把浏览器或者其他程序的代理指向它们就能走 Hysteria2。如果官方客户端能连上而图形客户端连不上，问题就在图形客户端的设置，不在服务端。

## 导入后连不上，按这个顺序查

1. **UDP 端口放行了没有**：系统防火墙和服务商安全组两边都要放行配置端口的 UDP，只放 TCP 是最常见的原因，具体可以看[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)。
2. **证书验证选项对不对**：自签证书没开跳过验证，或者真实证书却填了不匹配的 SNI，都会握手失败。
3. **混淆是否一致**：服务端有 obfs，客户端类型和密码要一模一样。
4. **端口、密码有没有复制错**：多了空格或者少了字符，肉眼很难发现，重新复制一遍。
5. **看服务端日志**：`journalctl --no-pager -e -u hysteria-server.service`，用官方脚本装的话服务名是这个，其他方式安装的以实际为准。

服务端还没装的话，安装方式可以看[Hysteria2一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)。

连上之后觉得速度慢，先看[Hysteria2速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)，bandwidth 填得不对反而更慢。
