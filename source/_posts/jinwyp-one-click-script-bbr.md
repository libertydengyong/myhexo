---
title: Jinwyp一键脚本安装BBR和BBRplus内核教程
date: 2026-09-06 21:00:00
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
      "dateModified": "2026-09-06T21:00:00+08:00",
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
          "text": "CentOS/AlmaLinux/Rocky选31装5.16内核或35装LTS 5.10内核，Debian选41装LTS 5.10内核，Ubuntu选45装LTS 5.10内核，装内核过程会重启两次属于正常现象。"
        },
        {
          "@type": "HowToStep",
          "name": "重新运行脚本启用加速算法",
          "text": "内核装完后重新运行同一个脚本，选2启用BBR（会询问是否搭配Cake或FQ，官方推荐Cake），如果之前选的是BBRplus内核编号（61或66），则选3启用BBRplus。"
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
            "text": "脚本里选51装XanMod LTS 5.10内核，重启完成后重新运行脚本选2启用BBR2；如果只想用XanMod自带的BBR3方案，可以直接参考XanMod内核搭配BBR3使用教程，不需要跑这个脚本。"
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

跑起来之后会出现菜单，根据自己的系统选对应的编号：

- **CentOS / AlmaLinux / Rocky Linux**：选31装最新5.16内核，或者选35装LTS 5.10内核（官方建议选这个，稳定性更好）
- **Debian**：选41装LTS 5.10内核
- **Ubuntu**：选45装LTS 5.10内核

装内核这一步过程中会重启两次，属于正常现象，不用担心。重启过程中如果出现警告界面提示删除旧内核，选"No"继续，不要中断。

内核装完之后，重新运行一次同一个脚本，这时候菜单里选2，就能启用BBR拥塞控制算法（会问你要不要搭配Cake或者FQ，官方推荐Cake）。如果想用BBRplus而不是普通BBR，装内核那一步就要选不一样的编号：选61装BBRplus 4.14.129内核，或者选66装BBRplus 5.10 LTS内核，同样会重启两次，装完后重新运行脚本选3来启用BBRplus。

如果想用XanMod内核搭配BBR2，脚本里也有对应选项：选51装XanMod LTS 5.10内核，重启完成后重新运行脚本选2启用BBR2。这个跟单独装XanMod的思路是一致的，如果只想用XanMod自带的BBR3方案，可以直接参考[XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)，不需要额外跑这个脚本。

装完不管选的哪种加速方式，验证有没有生效的方法都一样：

```bash
lsmod | grep bbr
```

看到对应的模块名（bbr、bbrplus）就说明启用成功了。如果验证结果不对，或者感觉不到明显提速，可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，排查一下是不是别的原因导致的。
