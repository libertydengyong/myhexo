---
title: S-UI没有内置Telegram通知，官方README里挂了个社区项目
date: 2026-09-30 23:45:00
tags:
  - S-UI教程
  - Telegram
categories:
  - vps技巧
description: S-UI本体翻遍源码没有Telegram Bot功能，跟3x-ui不是一回事；官方README的社区项目列表里链接了一个第三方Bot，用之前有几个安全上的点要想清楚。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI没有内置Telegram通知，官方README里挂了个社区项目",
      "description": "S-UI本体翻遍源码没有Telegram Bot功能，跟3x-ui不是一回事；官方README的社区项目列表里链接了一个第三方Bot，用之前有几个安全上的点要想清楚。",
      "datePublished": "2026-09-30T23:45:00+08:00",
      "dateModified": "2026-09-30T23:45:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-telegram-bot/",
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
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI有没有官方自带的Telegram Bot功能？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "没有。翻遍了官方后端service目录下所有文件、前端Settings设置页、main.go和config.go，都没有任何跟telegram、notif、webhook相关的代码或字段，这跟3x-ui是完全不同的两个项目，3x-ui确实自带Telegram机器人功能，S-UI没有对应的官方实现。"
          }
        },
        {
          "@type": "Question",
          "name": "想用Telegram管理S-UI有没有办法？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方README的社区项目列表里链接了一个第三方Bot项目SUI-Bot，功能上看起来比较完整，支持客户端管理、到期提醒、订阅链接查询等，通过S-UI的管理员API token跟面板通信。用之前要清楚这是非官方第三方项目，需要把面板的管理员token交给它，安装前建议自己先看一遍代码或者至少确认项目的活跃度和口碑，不建议盲目照抄安装命令直接跑。"
          }
        },
        {
          "@type": "Question",
          "name": "S-UI有没有其他自带的提醒机制，比如流量快用完提醒？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "没有找到。面板里能看到每个客户端的实时流量和到期状态，但都是被动查看，没有发现任何主动推送提醒（邮件、Webhook、Telegram等）的功能，需要提醒功能的话目前只能靠上面提到的第三方Bot，或者自己写脚本调用API定期检查再发通知。"
          }
        }
      ]
    }
  ]
}
</script>

先说结论，省得看到一半才发现找错方向：**S-UI 官方本体没有 Telegram Bot 通知功能**，这次没有只查前端就下结论——后端 `service` 目录下全部文件名过了一遍，`Settings.vue` 设置页、`main.go`、`config.go` 也都搜过 telegram、notif、webhook 这几个关键词，一处相关代码都没有。这跟 3x-ui 不是一回事，3x-ui 确实自带 Telegram 机器人（配置方法看[3x-ui Telegram机器人配置教程](https://vpsjq.com/2026/09/06/3x-ui-telegram-bot/)），S-UI 目前没有对应的官方实现，两个项目不能拿一套预期去套。

## 官方README里链接了一个第三方项目

翻 [S-UI 官方仓库](https://github.com/alireza0/s-ui) 的 README 时发现，社区项目列表里挂了一个专门给 S-UI 用的 Telegram Bot——[Sownix21/SUI-Bot](https://github.com/Sownix21/SUI-Bot)，官方原话是"欢迎在 S-UI 基础上做的 Bot、监控、自动化项目提 PR 加进这个列表"，说明这类第三方工具是被认可、鼓励存在的，只是没有并入官方本体。

这个项目本身功能看起来相当完整：客户端的增删改查、到期提醒、订阅链接查询、续费流程、多语言支持都有，通过调用 S-UI 的管理员 API token 跟面板通信，不需要手动折腾订阅链接或者入站配置，装好之后 Telegram 那边能直接管理面板上的用户。

## 用之前的几个考虑

这是一个**非官方的第三方项目**，安装意味着要把 S-UI 面板的管理员 API token 交给它，这个 token 拿到手基本等于拿到了面板的完全控制权。用之前建议：

- 先看一眼项目最近有没有人维护、issue 区反馈怎么样，而不是看到"支持中文、功能全"就直接装；
- 安装脚本是一键 `curl | sudo bash` 的形式，图省事之前最好先打开脚本看一眼具体做了什么，不建议不过一眼直接在生产环境的服务器上跑；
- 权限最小化原则，如果面板本身管理了不止一个人的节点和账号，给第三方工具完整管理员权限之前要想清楚风险和收益是否对等。

## 面板本身没有主动提醒功能

顺带说一下，S-UI 面板本身除了客户端列表里能看到的流量和到期状态（参考[流量清零怎么操作](https://vpsjq.com/2026/09/30/s-ui-traffic-reset/)里提到的显示方式），没有找到任何主动推送提醒的机制，不管是邮件、Webhook 还是别的形式都没有，都是要自己打开面板去看。需要主动提醒的话，目前要么用上面这个第三方 Bot，要么自己写个脚本定期调用 API 检查快到期或者流量快用完的客户端，再发到自己习惯用的通知渠道，面板自带的能力就到这里了。
