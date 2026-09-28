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
          "text": "80端口配置301跳转到443，location路径要跟面板的访问路径完全一致，必须转发Upgrade/Connection头以支持WebSocket。"
        },
        {
          "@type": "HowToStep",
          "name": "验证配置并重载Nginx",
          "text": "执行nginx -t检查语法，确认无误后systemctl reload nginx，再用curl -Ik测试反代是否生效。"
        },
        {
          "@type": "HowToStep",
          "name": "收紧裸端口的防火墙规则",
          "text": "确认反代能正常访问后，用ufw只放行本机访问面板原监听端口，拒绝公网直接访问，云服务商的安全组也要同步收紧。"
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

给面板单独解析一个域名（跟节点用的域名分开或者共用都行，分开更保险）。证书申请流程和[3x-ui配置TLS证书教程](https://vpsjq.com/2026/08/30/3x-ui-tls/)里讲的方法一样，这里不重复，注意一点：**用面板自带的 acme 证书管理申请，证书实际存在 `/root/cert/<域名>/` 目录下**（`fullchain.pem`、`privkey.pem`）；如果是另外用 certbot 单独签的，才是常见的 `/etc/letsencrypt/live/<域名>/` 路径，两种工具存放位置不一样，下面配置里按自己实际用的工具改路径。

## 写 Nginx 反代配置

面板本身的访问路径（比如 `/a1b2c3d4/`）要原样保留在 Nginx 的 `location` 里，官方文档给出的参考配置是这样的：

```nginx
# 80端口：纯做跳转，不处理业务
server {
    listen 80;
    server_name panel.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name panel.example.com;

    # 面板自带acme申请的证书在/root/cert/下；certbot单独签的在/etc/letsencrypt/live/下
    ssl_certificate     /root/cert/panel.example.com/fullchain.pem;
    ssl_certificate_key /root/cert/panel.example.com/privkey.pem;

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

把 `panel.example.com`、证书路径、`location` 里的访问路径、`proxy_pass` 里的端口号换成自己的实际值，新建的配置文件放进 `/etc/nginx/conf.d/` 或者 `/etc/nginx/sites-available/`（再软链到 `sites-enabled/`）都行，看你系统用的是哪套目录结构。**`Upgrade`/`Connection` 这两行必须保留**，面板界面有些数据是通过 WebSocket 实时推送的，缺了这两行会导致登录后界面数据加载不出来，容易被误判成配置错误或者面板故障。

配置写完先测语法、没问题再重载，不要直接重启：

```bash
nginx -t
systemctl reload nginx
```

`nginx -t` 显示 `syntax is ok` 才说明配置没写错；如果这一步就报错，Nginx 不会重载新配置，原来能访问的站点也不受影响，可以放心改。

保存后用浏览器或者 curl 测一下反代是否生效：

```bash
curl -Ik https://panel.example.com/a1b2c3d4/
```

能看到 `HTTP/2 200` 或者 `30x` 跳转到登录页，说明反代通了；如果还是老样子先确认域名解析、证书路径没填错。

如果面板设置里还开了独立的订阅服务端口，订阅链接也建议照同样的思路走一遍反代，保证客户端拉取订阅走的也是 HTTPS。

## 收紧裸端口的防火墙规则

反代跑起来、用上面的 curl 命令验证没问题之后，再去收紧防火墙，顺序不要反了：

```bash
ufw allow from 127.0.0.1 to any port 2053
ufw deny 2053/tcp
```

把 `2053` 换成面板实际监听的端口。这两条命令的顺序也有讲究——先放行本机访问，再拒绝外部访问，避免中间出现一个"两边都进不去"的空档。云服务商的安全组如果单独控制了这个端口，也要去那边同步改一下，只靠服务器本地的 ufw 规则不够，安全组层面没收紧的话端口其实还是对公网开放的。

## 常见问题排查

如果配置完打不开或者界面异常，按这个顺序查：

1. 先跑 `nginx -t` 确认配置语法没错，再确认 `location` 路径和面板里的访问路径是不是完全一致，连开头结尾的斜杠都要对上，不一致的话登录框能看到但资源加载不全；
2. 确认 `Upgrade`/`Connection` 这两个头有没有漏配，界面卡在登录后空白页大概率是这个问题；
3. 确认证书路径和域名解析没问题，注意面板自带acme证书和certbot证书路径不一样，这部分排查方法跟[TLS证书教程](https://vpsjq.com/2026/08/30/3x-ui-tls/)里的一致；
4. 收紧裸端口防火墙规则之前，先用 curl 确认反代本身能正常访问，避免两头都进不去；万一已经改完防火墙导致连不上了，先把 `ufw deny 2053/tcp` 那条规则删掉或者改回 `allow`，裸端口能访问了再回头排查 Nginx 配置。

面板安全这块，反代只是其中一环，配合定期改密码、参考[3x-ui忘记密码怎么办](https://vpsjq.com/2026/09/06/3x-ui-forgot-password/)里提到的重置方式留好退路，整体会更稳妥。
