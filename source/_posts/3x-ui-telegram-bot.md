---
title: 3x-ui Telegram 机器人配置教程：通知、命令与常见问题
date: 2026-09-06 21:20:00
updated: 2026-09-06 21:20:00
tags:
  - 3x-ui
  - Telegram机器人
categories:
  - vps技巧
description: 3x-ui 面板 Telegram 机器人配置完整步骤，包含创建机器人、获取 Token 和 Chat ID、开启流量与到期提醒，以及机器人不工作的排查方法。
keywords: 3x-ui telegram机器人,3x-ui telegram bot配置,3x-ui telegram bot not working,3x-ui机器人通知,x-ui telegram bot
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "3x-ui 的 Telegram 机器人能做什么？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "可以推送每日流量统计、面板登录提醒、CPU 使用率告警，并支持设置流量阈值和到期时间阈值提前提醒，部分版本还支持通过机器人命令直接查询和管理入站信息。"
      }
    },
    {
      "@type": "Question",
      "name": "3x-ui Telegram 机器人配置了但收不到消息怎么办？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "先确认 Bot Token 和 Chat ID 是否填写正确且没有多余空格，再确认服务器所在网络环境能否正常访问 Telegram 的 API（部分地区网络会屏蔽 Telegram），另外要检查是否已经先手动给机器人发送过一条消息激活对话，机器人是无法主动私聊一个从未联系过它的用户的。"
      }
    }
  ]
}
</script>

3x-ui 自带 Telegram 机器人通知功能，可以把面板登录提醒、流量统计、到期提醒这些消息直接推送到 Telegram，不用每次都登录面板去看。这篇教程把配置步骤和常见的"配置了但不工作"问题说清楚。

## 第一步：找 BotFather 创建机器人

Telegram 机器人都是通过官方的 `@BotFather` 账号创建的：

1. 在 Telegram 里搜索并打开 `@BotFather`。
2. 发送 `/newbot` 命令。
3. 按提示依次输入机器人的显示名称和用户名（用户名必须以 `bot` 结尾）。
4. 创建成功后，BotFather 会返回一段 Token，形如 `123456789:ABCdefGhIJKlmNoPQRstuVwxYZ`，这个 Token 就是等下要填到面板里的 Bot Token，注意保管好，不要泄露给别人（拿到这个 Token 就能控制这个机器人）。

## 第二步：获取你的 Chat ID

面板需要知道往哪个 Telegram 账号推送消息，这就是 Chat ID：

1. 在 Telegram 里找到刚创建的机器人，点击开始对话，随便发一条消息（比如 `/start`），**这一步不能跳过**，机器人没办法主动私聊一个从来没联系过它的人。
2. 在浏览器打开这个地址（把 `<your_bot_token>` 换成你的 Token）：
```
   https://api.telegram.org/bot<your_bot_token>/getUpdates
```
3. 返回的 JSON 里找 `"chat":{"id":` 后面的数字，这就是你的 Chat ID。

## 第三步：在面板里配置

登录 3x-ui 后台，进入设置里的 Telegram 机器人相关选项，把下面这些信息填好：

- **Bot Token**：第一步拿到的那串。
- **Chat ID**：第二步拿到的数字。
- **通知周期**：用 crontab 语法设置多久推送一次，比如每天固定时间推送一次流量汇总。
- **到期提醒阈值**：还剩多少天到期开始提醒。
- **流量提醒阈值**：剩余流量低于多少开始提醒。
- **CPU 告警阈值**（如果版本支持）：CPU 占用超过多少触发告警。

保存后可以先手动触发一次测试通知（不同版本入口可能不太一样，找一下设置页面里有没有"测试"按钮），确认能正常收到消息再关闭这个页面。

## 常见问题：机器人配置了但不工作

按下面顺序排查：

1. **Token 和 Chat ID 有没有复制错**：最常见的问题是复制的时候带了多余的空格或者换行符，重新复制一遍确认干净。
2. **有没有先手动给机器人发过消息**：这是最容易被忽略的一步，机器人在你主动跟它说过话之前，是没办法给你发消息的。
3. **服务器网络能不能访问 Telegram**：Telegram 的 API 域名在部分网络环境下会被屏蔽，如果你的 VPS 所在地区或者线路本身对 Telegram 访问不通畅，机器人自然发不出消息去，这种情况通常需要给面板所在服务器额外配置出站代理才能让机器人正常工作。这属于服务器所在网络环境限制，不是配置填错的问题，遇到这种情况可以到项目 GitHub 的 Issues 里搜一下有没有针对性的解决方案，因为具体能不能顺利支持全靠出站配置这块功能是否成熟，随版本会有变化，这里不下绝对结论。
4. **面板服务本身是否需要重启**：改完设置有些版本需要重启一次面板服务配置才会生效，重启命令参考 [3x-ui常用命令汇总](https://vpsjq.com/2026/08/30/3x-ui-commands/)。

## 机器人支持哪些命令

不同版本机器人支持的命令可能有差异，比较通用的功能包括查看当前系统状态、查看入站流量统计等，具体命令列表建议直接在 Telegram 里跟机器人对话发送 `/help` 或类似命令，面板更新之后命令集也可能跟着调整，与其记一份可能过时的命令表，不如让机器人自己告诉你当前支持什么。

如果这台服务器上的 3x-ui 还没搭起来，可以先参考 [3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/) 把节点跑起来，Telegram 机器人这块属于锦上添花的运维功能，不影响节点本身的可用性，不着急的话可以放在最后配置。
