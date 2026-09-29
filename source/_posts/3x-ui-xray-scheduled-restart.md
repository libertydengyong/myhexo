---
title: 3x-ui定时重启Xray解决随机卡顿
date: 2026-09-29 14:00:00
tags:
  - 3x-ui
  - Xray
categories:
  - vps工具
description: Xray-core隔三差五莫名其妙卡顿、断流的老问题，用crontab定时重启是社区认可的现实解法，附两种能真正查出原因、不用靠随机两字打发的情况。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui定时重启Xray解决随机卡顿",
      "description": "Xray-core隔三差五莫名其妙卡顿、断流的老问题，用crontab定时重启是社区认可的现实解法，附两种能真正查出原因、不用靠随机两字打发的情况。",
      "datePublished": "2026-09-29T14:00:00+08:00",
      "dateModified": "2026-09-29T14:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/29/3x-ui-xray-scheduled-restart/",
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
      "name": "用crontab定时重启Xray",
      "step": [
        {
          "@type": "HowToStep",
          "name": "排查是不是有明确原因",
          "text": "先看有没有客户端到期/超流量触发的重启循环，或者端口冲突，这两种有明确原因，能查到日志证据，不是真的随机。"
        },
        {
          "@type": "HowToStep",
          "name": "用restart-xray而不是完整restart",
          "text": "x-ui restart-xray只重启Xray核心进程，不会像完整restart那样把面板web服务也带着重启一遍。"
        },
        {
          "@type": "HowToStep",
          "name": "写入crontab",
          "text": "选一个低峰时段(比如凌晨4点)，用crontab -e加一行定时任务每天执行一次restart-xray。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "为什么Xray会莫名其妙卡住、断流？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "这不是个例，XTLS/Xray-core和MHSanaei/3x-ui的issue列表里长期有用户反馈这类问题，社区目前没有一个能根治所有场景的方案。已知的两种可确认原因是：客户端到期或者超流量后面板反复重写配置重启核心形成循环，以及新配置和正在运行的核心端口冲突导致核心退出后被看门狗反复拉起。剩下确实查不出具体原因的情况，用定时重启兜底是目前社区认可的现实做法。"
          }
        },
        {
          "@type": "Question",
          "name": "restart和restart-xray有什么区别，定时任务该用哪个？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "restart会把面板web服务和Xray核心一起重启，重启期间面板登录状态也会断；restart-xray只发送重启信号给Xray核心，面板本身不受影响。定时任务优先用restart-xray，影响范围更小。"
          }
        },
        {
          "@type": "Question",
          "name": "定时重启的频率设多高合适？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "每天一次、放在凌晨低峰时段就够了，不需要设置得太频繁。重启的瞬间正在连接的客户端会断开几秒钟再自动重连，多用户场景下频繁重启会让体验变差，能解决问题的前提下间隔越长越好。"
          }
        }
      ]
    }
  ]
}
</script>

面板部分假设已经按[3x-ui安装教程](https://vpsjq.com/2026/04/30/2026-04-30-011/)装好。这篇讲的是一个老问题——Xray-core跑着跑着隔一两天就卡一次，客户端显示连接但实际不通，重启一下又好了，日志里也看不出明显报错。

## 先别急着定时重启，看看是不是有明确原因

"随机卡顿"这四个字很容易变成万能借口，实际上有两种情况是能查出具体原因的，值得先排除掉：

- **客户端到期或者超流量触发的重启循环**：3x-ui 面板检测到某个客户端到期或者流量用完，会重写 `config.json` 并重启 Xray 核心禁用这个客户端。如果这个检测逻辑本身反复触发（比如临近到期的客户端很多），就会变成频繁重写配置、反复重启核心，表现出来就是"隔三差五卡一下"。查一下面板日志里有没有密集的重启记录，跟客户端到期时间对得上的话，这就是真实原因，不是随机的。
- **端口冲突导致核心崩溃后被反复拉起**：改配置或者新建入站的时候，如果新配置和正在监听的端口有冲突，核心会直接退出，面板的看门狗机制发现进程不在了又会把它拉起来，一冲突一拉起，看着就是间歇性卡顿。检查有没有多个入站不小心用了同一个端口。

如果这两种情况都排除了，日志确实干干净净看不出问题，那就是社区里普遍反馈的那种"确实会随机卡"的情况——[XTLS/Xray-core](https://github.com/XTLS/Xray-core/issues/6204)、[MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui/issues/1106) 的 issue 列表里都有类似反馈，目前没有能根治所有场景的方案，定时重启是现实里普遍在用的兜底办法。

## 用 restart-xray，不要用完整的 restart

3x-ui 的命令行脚本里有两个不同的重启命令：

```bash
x-ui restart        # 面板web服务 + Xray核心一起重启
x-ui restart-xray   # 只重启Xray核心，面板不受影响
```

定时任务优先用 `restart-xray`，只是给 Xray 核心发一个重启信号，不会连带把整个面板服务也重启一遍，影响范围更小，也不会打断你正在面板里做的操作。

## 写入 crontab

先确认命令的实际路径：

```bash
which x-ui
```

一般脚本安装的路径是 `/usr/bin/x-ui`，确认好之后编辑 crontab：

```bash
crontab -e
```

加一行，选一个业务低峰的时段，比如凌晨 4 点：

```bash
0 4 * * * /usr/bin/x-ui restart-xray >> /var/log/xray-restart.log 2>&1
```

把 `/usr/bin/x-ui` 换成你 `which x-ui` 查到的实际路径。保存退出，crontab 会自动生效，不需要额外重启 cron 服务。

## 重启会不会影响正在用的人

会有短暂影响。重启的瞬间正在连接的客户端会断开几秒钟，大部分客户端软件会自动重连，感知不会太强烈，但如果是游戏、视频通话这类对瞬断敏感的场景，断的那几秒还是能感觉到。所以尽量选凌晨这种没什么人在用的时间点，没必要为了"保险"设置成每小时重启一次，间隔越长对正在使用的人影响越小，一天一次通常就够了。

如果排查下来发现是端口冲突问题，建议直接去检查入站配置把冲突解决掉，比反复靠定时重启掩盖问题更彻底；多用户管理和到期设置可以参考[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)，把到期时间错开也能减少上面说的第一种重启循环的概率。
