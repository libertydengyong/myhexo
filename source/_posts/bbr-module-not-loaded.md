---
title: 已安装BBR加速内核但加速模块未加载的解决方法
date: 2026-08-30 22:00:00
tags:
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: 安装BBR之后用lsmod验证发现加速模块未加载的原因和解决方法，大多数情况下重启VPS就能解决。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "已安装BBR加速内核但加速模块未加载的解决方法",
      "description": "安装BBR之后用lsmod验证发现加速模块未加载的原因和解决方法，大多数情况下重启VPS就能解决。",
      "datePublished": "2026-08-30T22:00:00+08:00",
      "dateModified": "2026-08-30T22:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/30/bbr-module-not-loaded/",
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
          "name": "装完BBR后用lsmod验证没有输出是什么原因？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "说明BBR内核模块虽然安装了但还没有真正运行起来，不一定是配置出错，很多时候只是内核模块还没有加载生效。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么确认拥塞控制算法配置有没有生效？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "用 sysctl net.ipv4.tcp_congestion_control 查看，如果输出不是 bbr，说明配置本身没有生效，需要检查 /etc/sysctl.conf 里有没有正确写入 net.ipv4.tcp_congestion_control=bbr 和 net.core.default_qdisc=fq 这两行。"
          }
        },
        {
          "@type": "Question",
          "name": "配置写入了但模块还是没有加载怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "最直接的解决办法是重启VPS。BBR内核模块在新内核安装后需要重启才能加载，有时候跑完安装脚本没有重启，或者重启之后内核没有切换过来，模块就一直没有真正运行，重启后再验证一次即可。"
          }
        },
        {
          "@type": "Question",
          "name": "重启之后还是没有生效怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可能是内核版本不够新，BBR从Linux 4.9开始支持，旧内核装了配置也不会生效。可以用 uname -r 确认内核版本，版本低于4.9需要先升级内核再重启。"
          }
        }
      ]
    }
  ]
}
</script>

装完 BBR 之后用 `lsmod | grep bbr` 验证，结果没有任何输出，或者提示加速模块未加载，说明 BBR 内核模块虽然安装了但还没有真正运行起来。这个情况不一定是配置出错，很多时候只是内核模块还没有加载生效。

先跑一下验证命令确认具体状态：

\`\`\`bash
lsmod | grep bbr
\`\`\`

如果没有输出，再确认一下拥塞控制算法的设置有没有写进去：

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

如果输出不是 `bbr`，说明配置本身没有生效，需要检查 `/etc/sysctl.conf` 里有没有正确写入这两行：

\`\`\`bash
net.ipv4.tcp_congestion_control=bbr
net.core.default_qdisc=fq
\`\`\`

如果配置写入了但模块还是没有加载，最直接的解决办法是**重启 VPS**。BBR 内核模块在新内核安装后需要重启才能加载，有时候跑完安装脚本没有重启，或者重启之后内核没有切换过来，模块就一直没有真正运行。重启之后再跑一次验证命令：

\`\`\`bash
lsmod | grep bbr
sysctl net.ipv4.tcp_congestion_control
\`\`\`

正常情况下重启之后两条命令都能看到正确的输出，`lsmod` 能看到 `tcp_bbr` 模块，`sysctl` 输出 `bbr`。

如果重启之后还是没有生效，可能是内核版本不够新——BBR 从 Linux 4.9 开始支持，旧内核装了配置也不会生效。确认内核版本：

\`\`\`bash
uname -r
\`\`\`

版本低于 4.9 的话需要先升级内核，可以用 adsorgcn 的 bbr-script 自动升级，具体方法参考[Debian和Ubuntu开启BBR加速的两种方式](https://vpsjq.com/2026/08/28/debian-ubuntu-bbr/)。升级完内核重启之后，BBR 模块应该能正常加载。BBR 各版本的区别和选择可以参考[BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)。
