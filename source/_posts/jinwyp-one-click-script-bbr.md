---
title: Jinwyp一键脚本安装BBR和BBRplus内核教程
date: 2026-09-06 21:00:00
updated: 2026-10-08 21:00:00
tags:
  - Jinwyp
  - BBR加速
  - 一键脚本
categories:
  - vps工具
description: Jinwyp的one_click_script脚本安装BBR和BBRplus的完整步骤，包括CentOS/Debian/Ubuntu各系统对应的菜单选项和安装后启用的方法。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Jinwyp一键脚本安装BBR和BBRplus内核教程",
      "description": "Jinwyp的one_click_script脚本安装BBR和BBRplus的完整步骤，包括CentOS/Debian/Ubuntu各系统对应的菜单选项和安装后启用的方法。",
      "datePublished": "2026-09-06T21:00:00+08:00",
      "dateModified": "2026-10-08T21:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/06/jinwyp-one-click-script-bbr/",
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
      "name": "用Jinwyp脚本安装BBR或BBRplus内核",
      "step": [
        {
          "@type": "HowToStep",
          "name": "下载运行脚本",
          "text": "wget下载install_kernel.sh脚本并赋予执行权限后运行，会出现内核安装菜单。"
        },
        {
          "@type": "HowToStep",
          "name": "按系统选择内核编号",
          "text": "按我读到的脚本（头部日期2025-06-12，读取于2026-10-08）：CentOS系选36装5.10 LTS内核（Teddysun编译，菜单标注推荐安装），Debian 10/11选41装5.10 LTS内核，Ubuntu选46装5.10 LTS内核。编号随脚本版本变化，以屏幕菜单文字为准。装内核过程会重启两次属于正常现象。"
        },
        {
          "@type": "HowToStep",
          "name": "重新运行脚本启用加速算法",
          "text": "内核装完后重新运行同一个脚本，选2启用BBR（会让你选队列算法：FQ、FQ-Codel、FQ-PIE或CAKE，选CAKE要求内核在5.5以上），如果之前选的是BBRplus内核编号（61到68），则选3启用BBRplus。"
        },
        {
          "@type": "HowToStep",
          "name": "验证启用是否成功",
          "text": "用lsmod grep bbr查看，看到对应模块名（bbr、bbrplus）说明启用成功。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "装内核过程中提示删除旧内核怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "选No继续，不要中断，重启两次属于正常安装流程的一部分。"
          }
        },
        {
          "@type": "Question",
          "name": "想用XanMod内核搭配BBR2怎么操作？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "我读到的当前脚本里，51装的是XanMod 6.6 LTS，52装的是XanMod 6.11。这两个版本的XanMod里没有bbr2模块，算法名bbr的就是BBR3，所以不需要也无法再开bbr2，具体见BBR2脚本怎么用那篇；只想用XanMod自带的BBR3，可以直接参考XanMod内核搭配BBR3使用教程。"
          }
        }
      ]
    }
  ]
}
</script>

Jinwyp这个GitHub作者维护的one_click_script脚本包，是圈子里流传比较广的一键工具箱之一，里面装内核、启用BBR/BBRplus的那部分功能一直有人在用。跟[BBRplus一键安装教程](https://vpsjq.com/2025/05/06/bbrplus与其他加速方式安装/)里的zeruns版本比，两者思路类似，都是先装对应内核再启用加速算法，具体选哪个看个人习惯，功能上没有本质区别。
<!-- more -->
下载运行这个脚本包里专门管内核和BBR的部分：

```bash
wget --no-check-certificate https://raw.githubusercontent.com/jinwyp/one_click_script/master/install_kernel.sh && chmod +x ./install_kernel.sh && ./install_kernel.sh
```

跑起来之后会出现菜单，根据自己的系统选对应的编号（注意：菜单编号随脚本版本变化，下面的编号只是写这篇时的情况，请以脚本屏幕上显示的菜单文字为准）：

- **CentOS / AlmaLinux / Rocky Linux**：我读到的菜单里，31 是 elrepo 的 6.1 内核，32 和 35 是 5.4 LTS，36 是 Teddysun 编译的 5.10 LTS（标注“推荐安装”），37 到 39 是 5.15、6.1、6.6 LTS，40 是 elrepo 的 6.11
- **Debian**：Debian 10 和 11 选 41 装 5.10 LTS（官方源）；Debian 11 还有 42（5.19）和 43（6.1 或更高）；Debian 12 菜单里只有 43（6.1 LTS）
- **Ubuntu**：44 到 49 依次是 4.19、5.4、5.10、5.15、5.19、6.1（来自 Ubuntu kernel mainline），想要 5.10 选 46

这些编号是我对着脚本头部日期 2025-06-12 的版本读出来的，旧教程里常见的“31 装 5.16、35 装 5.10、45 装 5.10”已经对不上了，一定以你屏幕上的菜单文字为准。

装内核这一步过程中会重启两次，属于正常现象，不用担心。重启过程中如果出现警告界面提示删除旧内核，选"No"继续，不要中断。

内核装完之后，重新运行一次同一个脚本，这时候菜单里选2，就能启用BBR拥塞控制算法（会让你选队列算法：FQ、FQ-Codel、FQ-PIE或CAKE，选CAKE要求内核在5.5以上；脚本注释里说优质线路用cake带宽跑得更足，这是作者的经验，我没有测过）。如果想用BBRplus而不是普通BBR，装内核那一步就要选不一样的编号：选61装BBRplus 4.14.129内核，或者选64装BBRplus 5.10 LTS内核（62到68依次是UJX6N编译的4.14、4.19、5.10、5.15、6.1、6.6，以及“6.7或更高”，我读到的菜单里66是6.1 LTS），同样会重启两次，装完后重新运行脚本选3来启用BBRplus。

脚本里也有XanMod选项：我读到的菜单里，51装XanMod 6.6 LTS，52装XanMod 6.11（仅Debian/Ubuntu类系统显示）。注意这两个版本的XanMod里没有bbr2模块，算法名bbr的就是BBR3，菜单第2项虽然写着“BBR或BBR2”，在这种内核上开出来的是bbr，原因见[BBR2脚本怎么用](https://vpsjq.com/2026/10/04/bbr2-script-xanmod/)。如果只想用XanMod自带的BBR3方案，可以直接参考[XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)，不需要额外跑这个脚本。

装完不管选的哪种加速方式，验证有没有生效的方法都一样：

```bash
lsmod | grep bbr
```

看到对应的模块名（bbr、bbrplus）就说明启用成功了。如果验证结果不对，或者感觉不到明显提速，可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，排查一下是不是别的原因导致的。
