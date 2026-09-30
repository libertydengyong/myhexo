---
title: S-UI升级到新版本，出问题了怎么退回旧版本
date: 2026-09-30 20:00:00
tags:
  - S-UI教程
  - 故障排查
categories:
  - vps技巧
description: S-UI升级本质上是原地重跑一遍安装脚本，数据不会丢；新版本用着有问题的话，面板菜单里也有专门指定回退到某个具体版本号的选项。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI升级到新版本，出问题了怎么退回旧版本",
      "description": "S-UI升级本质上是原地重跑一遍安装脚本，数据不会丢；新版本用着有问题的话，面板菜单里也有专门指定回退到某个具体版本号的选项。",
      "datePublished": "2026-09-30T20:00:00+08:00",
      "dateModified": "2026-09-30T20:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-upgrade/",
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
      "name": "S-UI升级到最新版本",
      "step": [
        {
          "@type": "HowToStep",
          "name": "运行s-ui命令选第2项Update",
          "text": "会先弹出确认提示，说明这个操作会强制重装到最新版但数据不会丢，确认后自动下载安装并重启面板。"
        },
        {
          "@type": "HowToStep",
          "name": "遇到问题时用第3项指定版本号回退",
          "text": "新版本用着不顺手，选第3项Custom Version输入想要的具体版本号(比如0.0.1)，会重新安装到指定版本。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "升级会不会把已经配置好的节点和用户都清空？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不会。官方脚本里升级前的确认提示原话就写着这个操作不会丢失数据，升级本质是重新拉取最新的程序文件替换掉旧的，数据库文件不会被这个流程动到，节点配置、用户信息都会保留。"
          }
        },
        {
          "@type": "Question",
          "name": "升级到新版本后发现有问题，怎么退回旧版本？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "用s-ui命令菜单里的第3项Custom Version，输入想要回退到的具体版本号，脚本会重新安装到指定版本，不需要手动卸载重装。版本号可以去GitHub仓库的Releases页面查。"
          }
        },
        {
          "@type": "Question",
          "name": "有没有办法不用交互确认、直接在脚本里跑升级？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "有，直接执行s-ui update这个命令即可，不需要先进交互菜单再选第2项，适合写进自动化脚本或者远程一条命令搞定的场景。"
          }
        }
      ]
    }
  ]
}
</script>

S-UI 的升级机制比想象中简单一些——不是那种下载安装包覆盖安装的思路，本质上就是**重新跑一遍安装脚本**，脚本会自动拉取最新版本的程序文件替换掉旧的，数据库不会被碰。

SSH 进服务器，运行 `s-ui` 调出管理菜单，升级相关的是这两项：

- **2. Update** —— 更新到最新版本
- **3. Custom Version** —— 安装/回退到指定的具体版本号

## 更新到最新版

选第 2 项，会先弹出一句确认提示，原话大意是"这个操作会强制重装到最新版本，但数据不会丢失"，确认之后脚本会自动下载安装最新版本，装完自动重启面板，整个过程不需要额外操作。

不想走交互菜单的话，也可以直接在命令行执行：

```bash
s-ui update
```

效果跟菜单里选第2项一样，适合写进自动化脚本或者懒得进菜单、想一条命令搞定的场景。

## 新版本有问题，怎么退回去

升级之后如果发现新版本有 bug、用着不顺手，想退回之前的版本，用第 **3 项 Custom Version**。选中之后会让你输入一个具体的版本号（比如 `0.0.1`），脚本会重新安装到这个指定版本，不需要先手动卸载。版本号去 [alireza0/s-ui 的 Releases 页面](https://github.com/alireza0/s-ui/releases)查，确认好想回退到哪个版本再操作。

这个功能不只是用来回退，需要在多台服务器上保持同一个版本号（比如生产环境不想随便用最新版，想固定用某个已经验证过稳定的版本）时也能用上，指定版本号装就行。

## 升级前后要注意的

虽然官方保证数据不会丢，稳妥起见升级之前手动备份一下 `db/` 目录还是有必要的，具体位置和备份方法参考[alireza0/s-ui官方仓库与常用命令](https://vpsjq.com/2026/09/06/s-ui-alireza0-guide/)里"关于删库"那一节提到的路径。升级过程中面板会有短暂的重启，正在连接的节点会断开几秒钟，选一个没什么人用的时间段操作，影响会小一些。

如果升级之后面板彻底打不开了，先别急着删库重装，按[S-UI忘记密码怎么办](https://vpsjq.com/2026/09/29/s-ui-forgot-password/)和[改面板端口和访问路径](https://vpsjq.com/2026/09/30/s-ui-change-port-webpath/)里提到的排查思路先确认是不是端口、路径或者密码的问题，这几个原因比"升级升坏了"常见得多。
