---
title: S-UI改面板端口和访问路径，改完别忘了这一步
date: 2026-09-30 16:00:00
tags:
  - S-UI教程
  - 故障排查
categories:
  - vps技巧
description: S-UI改面板端口、访问路径、订阅端口、订阅路径这四项都在同一个终端菜单里，改完常被漏掉的是重启面板这一步，附直接查看完整访问地址的命令。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI改面板端口和访问路径，改完别忘了这一步",
      "description": "S-UI改面板端口、访问路径、订阅端口、订阅路径这四项都在同一个终端菜单里，改完常被漏掉的是重启面板这一步，附直接查看完整访问地址的命令。",
      "datePublished": "2026-09-30T16:00:00+08:00",
      "dateModified": "2026-09-30T16:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-change-port-webpath/",
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
      "name": "S-UI修改面板端口和访问路径",
      "step": [
        {
          "@type": "HowToStep",
          "name": "运行s-ui命令选第9项",
          "text": "菜单第9项Set Panel Settings会依次询问面板端口、面板路径、订阅端口、订阅路径，不想改的留空回车跳过即可。"
        },
        {
          "@type": "HowToStep",
          "name": "重启面板服务",
          "text": "改设置只是写数据库，不会自动重启进程，必须手动重启s-ui服务新端口新路径才会真正生效。"
        },
        {
          "@type": "HowToStep",
          "name": "查看完整访问地址",
          "text": "用菜单第10项View Panel Settings能直接看到当前配置和完整可访问的URL，不用自己拼端口和路径。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "改完端口和访问路径为什么面板还是打不开？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "最常见的原因是忘了重启s-ui服务——设置命令只是把新值写进数据库，正在运行的面板进程不会自动感知变化，必须手动重启才会用新端口监听。其次要检查防火墙有没有放行新端口，改端口前只放行了旧端口的话，新端口一样连不上。"
          }
        },
        {
          "@type": "Question",
          "name": "订阅端口/路径和面板端口/路径是一回事吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是一回事，是两套独立的配置。面板端口和路径是你登录管理后台用的，订阅端口和路径是客户端拉取订阅链接用的，两者可以设成不一样的值，改的时候菜单会分开问，不要混着填。"
          }
        },
        {
          "@type": "Question",
          "name": "改完之后忘了自己设的端口和路径是什么，怎么查？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "用s-ui命令菜单第10项View Panel Settings，会直接显示当前的配置和完整可以访问的URL，不需要自己拼端口和路径去猜。如果连这个也进不去(比如忘了SSH密码之类的)，才需要考虑更彻底的处理方式。"
          }
        }
      ]
    }
  ]
}
</script>

S-UI 改面板端口、访问路径这些设置走的是终端命令，不是在网页里的某个设置页面点一点就行——这点跟很多人的第一直觉不太一样。SSH 进服务器，运行 `s-ui` 调出管理菜单，跟设置相关的是这三项：

- **8. Reset Panel Settings** —— 重置成默认值
- **9. Set Panel Settings** —— 直接设置成指定的值
- **10. View Panel Settings** —— 查看当前配置

## 用第9项一次性改四个值

选第9项，会依次问你四样东西：

- 面板端口（panel port）
- 面板访问路径（panel path）
- 订阅端口（subscription port）
- 订阅访问路径（subscription path）

**面板和订阅是两套完全独立的配置**，登录管理后台用的是前两个，客户端拉取订阅链接用的是后两个，可以设成完全不一样的值。哪一项不想改，直接回车留空跳过就行，不会动到原来的值。

## 改完一定要重启，这步最容易漏

这是最容易被忽略的一步：**Set Panel Settings 只是把新的端口和路径写进数据库，不会自动重启面板进程**。正在运行的 S-UI 服务是启动的时候读一次配置，不会实时感知数据库里的变化，端口和路径改了但没重启，实际监听的还是旧端口——很多人以为设置没生效或者面板坏了，其实只是少了重启这一步：

```bash
systemctl restart s-ui
```

重启之后新的端口和路径才会真正生效。改端口之前记得把新端口在防火墙里放行，不然重启完新端口一样连不上。

## 忘了改成了什么，直接查

改完之后如果记混了自己设的端口和路径，不用自己拼URL去试，用第 **10 项 View Panel Settings**，会直接显示当前配置，还会把完整能访问的URL打印出来，照着打开就行。

如果连密码都一起忘了、或者想干脆重置回默认值重新设置，可以参考[S-UI忘记密码怎么办](https://vpsjq.com/2026/09/29/s-ui-forgot-password/)，里面第8项Reset Panel Settings也会顺带提到，两个问题一起处理更省事。改完端口和路径别忘了同步告诉正在用的人，[订阅链接](https://vpsjq.com/2026/08/29/s-ui-subscription/)也会因为路径变化而失效，需要重新导出发给他们。
