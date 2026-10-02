---
title: Hysteria2多用户怎么配？userpass认证和流量统计API
date: 2026-10-02 15:30:00
tags:
  - Hysteria2
  - 多用户
categories:
  - vps工具
description: 官方脚本装的Hysteria2默认所有人共用一个密码。想给几个人分开用，把auth改成userpass就行；再开trafficStats接口，能查每个用户的流量、在线情况，还能踢人。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2多用户怎么配？userpass认证和流量统计API",
      "description": "官方脚本装的Hysteria2默认所有人共用一个密码。想给几个人分开用，把auth改成userpass就行；再开trafficStats接口，能查每个用户的流量、在线情况，还能踢人。",
      "datePublished": "2026-10-02T15:30:00+08:00",
      "dateModified": "2026-10-02T15:30:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-multi-user/",
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
      "name": "配置Hysteria2多用户并查看流量",
      "step": [
        {
          "@type": "HowToStep",
          "name": "把auth改成userpass",
          "text": "编辑/etc/hysteria/config.yaml，把auth的type改成userpass，并在userpass下面按用户名: 密码的格式添加每个用户。"
        },
        {
          "@type": "HowToStep",
          "name": "客户端用用户名:密码认证",
          "text": "客户端的auth字段（链接里@前面的部分）写成用户名:密码，不同用户用各自的用户名和密码。"
        },
        {
          "@type": "HowToStep",
          "name": "开启流量统计API",
          "text": "在配置里加trafficStats，设置listen和secret，secret一定要设，否则任何能访问这个地址的人都能看流量统计并踢人。"
        },
        {
          "@type": "HowToStep",
          "name": "查询流量和在线情况",
          "text": "用curl带上Authorization请求头访问/traffic查看每个用户的上下行流量，访问/online查看在线用户和设备数，必要时用/kick踢人。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2怎么设置多个用户？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "把服务端auth的type设为userpass，在userpass下按用户名: 密码添加多个用户即可。客户端认证时用用户名:密码的形式，不同用户用各自的账号，服务端就能区分是谁。改完配置需要重启hysteria-server服务。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2能查看每个用户用了多少流量吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以。开启trafficStats接口后，访问/traffic会返回以用户名为键的上传和下载字节数，/online会返回在线用户和各自的设备数。不过这只是数据查询接口，官方配置里没有看到自动按流量封号或到期停用的功能，需要自己写脚本处理。"
          }
        },
        {
          "@type": "Question",
          "name": "trafficStats接口不设secret有什么风险？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方文档明确提醒，不设secret的话，任何能访问这个监听地址的人都能看流量统计并踢掉用户，强烈建议设置。除了设secret，也可以让接口只监听本机127.0.0.1，不暴露到公网。"
          }
        }
      ]
    }
  ]
}
</script>

用官方脚本装的 Hysteria2，默认是 `password` 认证：所有人共用同一个密码。自己一个人用没问题，但想分给家人朋友用，就会遇到两个麻烦：不知道谁用了多少流量，想让某个人停用也没办法单独处理，只能把所有人的密码一起换掉。官方其实内置了多用户认证，改一处配置就能用。服务端配置的基础写法先看[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。

## 把 auth 改成 userpass

原来的配置大概是这样：

```yaml
auth:
  type: password
  password: 共用的密码
```

改成多用户，就是把 `type` 换成 `userpass`，然后在下面逐个列出用户：

```yaml
auth:
  type: userpass
  userpass:
    alice: 密码一
    bob: 密码二
    carol: 密码三
```

左边是用户名，右边是该用户的密码。改完保存，重启服务生效：

```bash
systemctl restart hysteria-server.service
```

增加、删除用户都是改这一段再重启。要删掉某个人，把他那一行删掉后重启即可，旧账号以后就认证不过了。

## 客户端怎么填

客户端的认证字段要写成 `用户名:密码`，比如 alice 填 `alice:密码一`。分享链接里就是 `@` 前面那一段，官方 URI 规范里也说明了，`userpass` 类型的服务器，认证部分要写成 `username:password`：

```
hysteria2://alice:密码一@your.domain.net:443/?sni=your.domain.net#alice
```

密码里如果有特殊字符，链接里需要做百分号转义，否则解析会出错，建议给用户设密码时就避开 `@`、`:`、`/`、`#` 这类字符。各个参数的含义可以看[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

## 开启流量统计 API，看谁用了多少

光有多用户还不够，想知道每个人的用量，需要开启官方的 Traffic Stats API。在服务端配置里加这一段：

```yaml
trafficStats:
  listen: 127.0.0.1:9999
  secret: 换成一串随机字符串
```

两个字段都值得认真对待：

- **`secret` 一定要设。** 官方文档明确说，不设的话，任何能访问这个监听地址的人都能看流量统计、踢掉用户，强烈建议设置。
- **`listen` 建议写成 `127.0.0.1`**，只让本机能访问。官方示例写的是 `:9999`，会监听所有网卡；多加一层限制更保险，需要从别的机器查询时，可以用 SSH 隧道。这是我的建议，不是官方要求。

改完重启服务，就可以在服务器上用 curl 查询了。

### 查每个用户的流量

```bash
curl -H 'Authorization: 你设的secret' http://127.0.0.1:9999/traffic
```

返回的是以用户名为键的 JSON，每个用户有 `tx` 和 `rx` 两个字节数：

```json
{
  "alice": {"tx": 514, "rx": 4017},
  "bob": {"tx": 7790, "rx": 446623}
}
```

在地址后面加 `?clear=1`，会在返回数据的同时把统计清零，适合按周期（比如每月）统计用量。

### 查谁在线

```bash
curl -H 'Authorization: 你设的secret' http://127.0.0.1:9999/online
```

返回每个在线用户和他当前的设备连接数，比如 `{"alice": 2, "bob": 1}`，可以看出某个账号有没有被多人同时使用。

### 踢人

```bash
curl -X POST -H 'Authorization: 你设的secret' -d '["bob"]' http://127.0.0.1:9999/kick
```

官方文档提醒，被踢的客户端通常会自动重连，所以这只是临时断开。真想让某个人彻底用不了，要从 `userpass` 里删掉账号再重启服务。

## 它不能做到什么

要分清这套方案的边界，免得期望过高：

- **只是查询接口。** 官方配置里我没有看到"流量用完自动停用"或者"到期自动封号"这类功能，要做的话得自己写脚本，定时读取 `/traffic`，超额了就从配置里删掉账号并重启。
- **没有按用户单独限速。** 服务端的 `bandwidth` 是对每个客户端统一的限速，没有看到针对单个用户设不同速度的字段，具体见[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)里的说明。
- **官方还支持 `http` 和 `command` 两种认证类型**，可以把认证交给你自己的后端服务或脚本，更灵活，但需要自己开发。简单的多人分享，`userpass` 已经够用。

## 如果觉得手动管理太麻烦

用户一多，手动改配置文件再重启会很累，而且没有现成的到期、流量额度管理。这时候用面板更省事，比如 3x-ui 里的[用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)，Hysteria2 的搭建可以看[3x-ui 配置 Hysteria2](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)，面板自带流量和到期的设置。两种方式怎么选，取决于你是只想自己加两三个人，还是需要长期管理一批用户。
