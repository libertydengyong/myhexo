---
title: Jinwyp一键脚本：VPS安装BBR和网络优化工具
date: 2026-09-02 10:00:00
tags:
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: Jinwyp的one_click_script是一个常用的VPS一键安装管理工具，支持安装Linux内核、开启BBR、配置WARP和多种代理协议，安装命令去GitHub找最新版本。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Jinwyp一键脚本：VPS安装BBR和网络优化工具",
      "description": "Jinwyp的one_click_script是一个常用的VPS一键安装管理工具，支持安装Linux内核、开启BBR、配置WARP和多种代理协议，安装命令去GitHub找最新版本。",
      "datePublished": "2026-09-02T10:00:00+08:00",
      "dateModified": "2026-09-02T10:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/02/jinwyp-one-click-script/",
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
      "name": "用Jinwyp脚本开启BBR加速",
      "step": [
        {
          "@type": "HowToStep",
          "name": "下载运行脚本",
          "text": "去GitHub仓库jinwyp/one_click_script找最新安装命令运行，脚本会自动检测系统环境列出可用操作选项。"
        },
        {
          "@type": "HowToStep",
          "name": "从菜单选择安装内核并开启BBR",
          "text": "跑完脚本从菜单选择安装内核和开启BBR的选项，脚本自动处理内核安装和参数配置，装完提示重启。"
        },
        {
          "@type": "HowToStep",
          "name": "重启后验证",
          "text": "用sysctl net.ipv4.tcp_congestion_control查看，输出bbr说明生效了。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "这个脚本除了BBR还能做什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "还支持安装XanMod内核、配置Cloudflare WARP给服务器加IPv4或IPv6出口、以及安装各类代理协议，功能比较多，按需选择就行，不用的功能不装不会影响已有配置。"
          }
        },
        {
          "@type": "Question",
          "name": "跟byJoey的BBR3专用脚本有什么区别？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Jinwyp的脚本功能更综合，覆盖内核安装、BBR、WARP、代理协议等多个方面；byJoey的Actions-bbr-v3脚本专门针对BBR3内核安装，功能更聚焦。"
          }
        }
      ]
    }
  ]
}
</script>

Jinwyp 是 GitHub 上一个比较活跃的开源项目，主要维护一个叫 one_click_script 的 VPS 一键安装管理脚本。这个脚本把常见的 VPS 优化操作打包在一起，包括安装 Linux 内核、开启 BBR 网络加速、配置 Cloudflare WARP、以及集成多种代理协议，不需要一条一条手动跑命令，从菜单里选要做的操作就行。

安装命令去 GitHub 仓库找最新的：`https://github.com/jinwyp/one_click_script`，README 里有当前维护的安装命令，直接复制跑就行。脚本会自动检测系统环境，列出可用的操作选项。

日常用得最多的功能是开启 BBR。跑完脚本之后从菜单选择安装内核和开启 BBR 的选项，脚本会自动处理内核安装和参数配置，装完提示重启，重启之后验证一下：

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

输出 `bbr` 就说明生效了。跟手动改 sysctl.conf 相比，用脚本省去了自己查参数和逐行写入的麻烦，出错概率也更低。

除了 BBR，脚本还支持安装 XanMod 内核、配置 Cloudflare WARP（给服务器加 IPv4 或 IPv6 出口）、以及安装各类代理协议。功能比较多，不需要全部用到，按需选择就行，不用的功能不装不会影响已有的配置。

BBR 各版本的区别和适用场景可以参考[BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)，如果想用更专门的 BBR3 安装脚本，可以参考[BBR3一键安装脚本：byJoey Actions-bbr-v3 GitHub安装教程](https://vpsjq.com/2026/08/28/bbr3-install/)，两者的区别在于 Jinwyp 的脚本功能更综合，byJoey 的脚本专门针对 BBR3 内核安装。
