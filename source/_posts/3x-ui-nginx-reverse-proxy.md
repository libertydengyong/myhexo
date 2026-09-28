---
title: 3x-ui用Nginx反向代理隐藏面板
date: 2026-09-28 18:00:00
tags:
  - 3x-ui
  - Nginx
categories:
  - vps工具
description: 给3x-ui面板套一层Nginx反代，用真实域名+HTTPS访问，裸端口对公网整个收起来，比单纯改访问路径多一层防护。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui用Nginx反向代理隐藏面板",
      "description": "给3x-ui面板套一层Nginx反代，用真实域名+HTTPS访问，裸端口对公网整个收起来，比单纯改访问路径多一层防护。",
      "datePublished": "2026-09-28T18:00:00+08:00",
      "dateModified": "2026-09-28T18:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/28/3x-ui-nginx-reverse-proxy/",
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
      "name": "用Nginx反向代理隐藏3x-ui面板",
      "step": [
        {
          "@type": "HowToStep",
          "name": "准备域名和证书",
          "text": "给面板单独解析一个域名，申请Let's Encrypt证书。"
        },
        {
          "@type": "HowToStep",
          "name": "写Nginx反代配置",
          "text": "location路径要跟面板的访问路径完全一致，必须转发Upgrade/Connection头以支持WebSocket。"
        },
        {
          "@type": "HowToStep",
          "name": "收紧裸端口的防火墙规则",
          "text": "反代生效后，面板原来监听的裸端口不再需要对公网开放，只留给本机访问即可。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "已经改过访问路径了，为什么还要多此一举做反代？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "改访问路径能防住不知道路径的人，但服务器上那个端口本身还在裸露监听，端口扫描工具能识别出这是个3x-ui面板的特征端口，照样可能被针对性攻击或者暴力破解密码。做了反代之后，公网只看到Nginx上一个普通的HTTPS网站，裸端口可以直接从防火墙层面收起来，安全层级不是一回事。"
          }
        },
        {
          "@type": "Question",
          "name": "Nginx配置里的location路径和面板的访问路径必须完全一样吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "必须一样，包括开头结尾的斜杠。不一致的话页面能打开登录框，但登录后静态资源(JS/CSS)和WebSocket连接会加载不出来，界面显示异常或者直接卡在登录后的空白页。"
          }
        },
        {
          "@type": "Question",
          "name": "反代之后原来的裸端口还要不要对公网开放？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不需要了。反代生效后所有正常访问都走Nginx的443端口，裸端口只是Nginx本机转发用的，在防火墙或安全组里把这个端口改成只允许本机(127.0.0.1)或者内网访问，对公网直接不开放，进一步缩小暴露面。"
          }
        }
      ]
    }
  ]
}
</script>

面板部分假设已经按[3x-ui安装教程](https://vpsjq.com/2026/04/30/2026-04-30-011/)装好，端口和访问路径也已经按那篇教程里说的改成了不好猜的值。这篇讲的是再往前一步——把面板整个藏到 Nginx 反代后面，用真实域名和 HTTPS 访问，公网上看起来就是个普通网站。

## 为什么裸端口+随机路径还不够

改访问路径能挡住不知道具体路径的人，但服务器上那个端口本身还在裸露监听。批量端口扫描工具扫到这个端口、发现响应特征符合 3x-ui 面板，照样可能被列入定向攻击的目标列表，接下来就是对着登录框做密码暴力破解——3x-ui 官方仓库的 issue 列表里能看到不少用户反馈过类似的困扰和"如何用 nginx 反代复用 443 端口"这类问题（[issue #4845](https://github.com/MHSanaei/3x-ui/issues/4845)）。做了反代之后，公网层面只暴露 Nginx 上一个普通的 HTTPS 站点，裸端口可以直接从防火墙收起来，不再对公网开放，攻击面小了一层。

## 准备域名和证书

给面板单独解析一个域名（跟节点用的域名分开或者共用都行，分开更保险）。证书申请流程和[3x-ui配置TLS证书教程](https://vpsjq.com/2026/08/30/3x-ui-tls/)里讲的 acme 申请方法一样，这里不重复，用 certbot 单独给这个域名签一张也可以，效果一样。

## 写 Nginx 反代配置

面板本身的访问路径（比如 `/a1b2c3d4/`）要原样保留在 Nginx 的 `location` 里，官方文档给出的参考配置是这样的：

```nginx
server {
    listen 443 ssl http2;
    server_name panel.example.com;

    ssl_certificate     /etc/letsencrypt/live/panel.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/panel.example.com/privkey.pem;

    location /a1b2c3d4/ {
        proxy_pass http://127.0.0.1:2053;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }
}
```

把 `panel.example.com`、证书路径、`location` 里的访问路径、`proxy_pass` 里的端口号换成自己的实际值。**`Upgrade`/`Connection` 这两行必须保留**，面板界面有些数据是通过 WebSocket 实时推送的，缺了这两行会导致登录后界面数据加载不出来，容易被误判成配置错误或者面板故障。

如果面板设置里还开了独立的订阅服务端口，订阅链接也建议照同样的思路走一遍反代，保证客户端拉取订阅走的也是 HTTPS。

## 收紧裸端口的防火墙规则

反代跑起来验证没问题之后，去防火墙或者安全组里把面板原来的裸端口改成只允许 `127.0.0.1` 或者内网访问，对公网直接不放行。Nginx 和面板在同一台机器上走的是本地回环地址，不受影响，公网这边就再也扫不到这个端口了。

## 常见问题排查

如果配置完打不开或者界面异常，按这个顺序查：

1. 先确认 Nginx 的 `location` 路径和面板里的访问路径是不是完全一致，连开头结尾的斜杠都要对上，不一致的话登录框能看到但资源加载不全；
2. 确认 `Upgrade`/`Connection` 这两个头有没有漏配，界面卡在登录后空白页大概率是这个问题；
3. 确认证书路径和域名解析没问题，这部分排查方法跟[TLS证书教程](https://vpsjq.com/2026/08/30/3x-ui-tls/)里的一致；
4. 收紧裸端口防火墙规则之前，先确认反代本身能正常登录，避免两头都进不去。

面板安全这块，反代只是其中一环，配合定期改密码、参考[3x-ui忘记密码怎么办](https://vpsjq.com/2026/09/06/3x-ui-forgot-password/)里提到的重置方式留好退路，整体会更稳妥。
