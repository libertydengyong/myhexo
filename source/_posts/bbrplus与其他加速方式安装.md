---
title: BBRplus与其他加速方式一键安装
tags:
  - BBRplus
  - BBR加速
categories:
  - vps工具
abbrlink: 821
date: 2025-05-06 20:28:53
description: 用zeruns修改的tcp.sh脚本一键安装BBRplus等加速方式，附验证是否成功运行的方法。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "BBRplus与其他加速方式一键安装",
      "description": "用zeruns修改的tcp.sh脚本一键安装BBRplus等加速方式，附验证是否成功运行的方法。",
      "datePublished": "2025-05-06T20:28:53+08:00",
      "dateModified": "2025-05-06T20:28:53+08:00",
      "url": "https://vpsjq.com/2025/05/06/bbrplus与其他加速方式安装/",
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
      "name": "用zeruns的tcp.sh脚本安装BBRplus",
      "step": [
        {
          "@type": "HowToStep",
          "name": "下载运行tcp.sh脚本",
          "text": "用wget下载zeruns修改的tcp.sh脚本并赋予执行权限后运行，会出现加速方式选择菜单。"
        },
        {
          "@type": "HowToStep",
          "name": "选择要安装的加速方式",
          "text": "菜单里列出BBRplus和其他几种选项，选对应数字确认安装，安装完成后按提示重启服务器。"
        },
        {
          "@type": "HowToStep",
          "name": "验证是否生效",
          "text": "重启后用lsmod grep bbr或sysctl net.ipv4.tcp_congestion_control查看，输出里看到bbrplus就说明在跑了。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "验证结果不对是什么原因？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "先确认内核版本够不够，老内核不支持这类加速方式，装了也没用，需要先升级内核。"
          }
        }
      ]
    }
  ]
}
</script>

BBRplus 是在 Google 官方 BBR 基础上修改的第三方版本，理论上比普通 BBR 更激进一些，实际使用下来速度确实快一点，不是质的飞跃，但差距是有的。zeruns 修改的 tcp.sh 脚本把几种加速方式打包在一起，跑一遍脚本，从菜单里选你想装的，比手动配置省事很多。

安装命令：

\`\`\`bash
wget -N --no-check-certificate "https://gist.github.com/zeruns/a0ec603f20d1b86de6a774a8ba27588f/raw/4f9957ae23f5efb2bb7c57a198ae2cffebfb1c56/tcp.sh" && chmod +x tcp.sh && ./tcp.sh
\`\`\`

脚本跑完会出现一个菜单，列出可以安装的加速方式，包括 BBRplus 和其他几种选项，选对应的数字确认就行。安装完成后按提示重启服务器。

重启之后验证有没有生效，两条命令都可以：

\`\`\`bash
lsmod | grep bbr
\`\`\`

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

输出里看到 bbrplus 就说明在跑了。如果验证结果不对，先确认内核版本够不够，老内核不支持这类加速方式，装了也没用，需要先升级内核。BBR 系列加速方式的原理和适用场景可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，搞清楚原理之后对验证结果的判断会更准确。如果想搭配 XanMod 内核一起用，可以参考[XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)，XanMod 内置了 BBR3 支持，不需要额外跑这个脚本。
