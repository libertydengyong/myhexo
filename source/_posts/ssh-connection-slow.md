---
title: VPS SSH连接很慢是什么原因
tags:
  - SSH连接慢
date: 2026-08-15 20:00:00
categories:
  - vps技巧
description: SSH连接VPS时卡顿几秒才弹出密码提示的常见原因，多数不是网络问题，而是服务端在做没用上的反向DNS解析和GSSAPI认证。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "VPS SSH连接很慢是什么原因",
      "description": "SSH连接VPS时卡顿几秒才弹出密码提示的常见原因，多数不是网络问题，而是服务端在做没用上的反向DNS解析和GSSAPI认证。",
      "datePublished": "2026-08-15T20:00:00+08:00",
      "dateModified": "2026-08-15T20:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/15/ssh-connection-slow/",
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
      "name": "解决SSH连接卡顿几秒才弹出密码提示",
      "step": [
        {
          "@type": "HowToStep",
          "name": "用-v参数确认卡在哪一步",
          "text": "执行ssh -v root@IP查看详细握手过程，如果在gssapi-keyex、gssapi-with-mic这几行卡住或者迟迟不往下走，说明是在等DNS解析或GSSAPI认证。"
        },
        {
          "@type": "HowToStep",
          "name": "关闭反向DNS解析",
          "text": "在/etc/ssh/sshd_config里加一行UseDNS no，SSH默认会对客户端IP做反向PTR查询再做正向A记录确认，绝大多数IP没配PTR记录导致查询超时白等几秒。"
        },
        {
          "@type": "HowToStep",
          "name": "关闭GSSAPI认证",
          "text": "加一行GSSAPIAuthentication no，这套机制是给Kerberos环境用的，普通VPS没配置Kerberos，服务端却仍会尝试走一遍直到超时才轮到正常认证。"
        },
        {
          "@type": "HowToStep",
          "name": "重启SSH服务生效",
          "text": "执行systemctl restart sshd，之后再连接密码提示框基本瞬间弹出。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "两个选项都关了还是慢怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "大概率是真实的网络线路问题，不是配置能解决的，可以测一下到VPS的延迟和丢包情况。"
          }
        }
      ]
    }
  ]
}
</script>

敲下`ssh root@IP`之后，屏幕愣是卡个三五秒才弹出密码提示，很多人第一反应是这台VPS线路不行，实际上大部分时候锅不在网络，是SSH服务端自己在做两件你压根用不上的事，白白耗掉了这几秒。

## 先确认卡在哪一步

带上`-v`参数连接，能看到详细的握手过程：

```bash
ssh -v root@IP
```

输出里如果在`gssapi-keyex`、`gssapi-with-mic`这几行卡了好一会儿，或者迟迟没往下走就是在等DNS解析，基本可以确定是下面这两个原因。

## 反向DNS解析在拖后腿

SSH服务端默认开着`UseDNS`这个选项，客户端一连上来，服务器就会先拿客户端的IP去做一次反向PTR查询，查出对应的主机名，再拿这个主机名反过来做一次正向A记录查询，确认两边对得上——这套流程是防止IP欺骗用的，但绝大多数家庭宽带和VPS的IP根本没配PTR记录，查询注定超时，白白等上好几秒。

关掉就行：

```bash
echo "UseDNS no" >> /etc/ssh/sshd_config
```

## GSSAPI认证同样是白等

GSSAPI这套认证机制是给Kerberos环境用的，普通VPS压根没配置Kerberos，但服务端默认还是会尝试走一遍这个认证流程，等它自己超时放弃才轮到正常的密码或密钥认证：

```bash
echo "GSSAPIAuthentication no" >> /etc/ssh/sshd_config
```

两条改完，重启服务生效：

```bash
systemctl restart sshd
```

改完之后再连一次，之前那几秒的卡顿基本就没了，密码提示框差不多是瞬间弹出来的。

## 频繁登录同一台机器，还是觉得慢

上面两个改完是单次连接不卡了，但如果习惯开好几个终端窗口、或者用scp传文件，每次还是要重新走一遍完整的认证握手，累积起来还是烦。这种场景下该用连接复用，把认证过的通道留着给后面的连接直接用，具体怎么配置在[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)里写过（ControlMaster那部分），手机和电脑上用的思路是一样的。

## 排除掉这两个原因，还是慢

如果`UseDNS`和`GSSAPIAuthentication`都关了，卡顿依然明显，那大概率是真的网络线路问题了，不是配置能解决的，可以测一下到VPS的延迟和丢包，或者考虑给网络本身做一下优化。

顺带一提，如果SSH连接时弹出的不是"卡顿"而是一大段REMOTE HOST IDENTIFICATION HAS CHANGED的红色警告，那是另一码事，跟这篇讲的连接慢没关系，具体可以看[这篇](https://vpsjq.com/2026/08/15/ssh-remote-host-identification-changed/)。
