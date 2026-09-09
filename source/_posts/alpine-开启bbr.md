---
title: Alpine Linux开启BBR的方法
tags:
  - Alpine Linux
  - BBR加速
id: '144'
categories:
  - vps技巧
abbrlink: 48757
date: 2025-07-12 23:17:31
description: Alpine Linux系统开启BBR拥塞控制算法的命令和验证方法，适合小内存VPS使用的轻量系统。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Alpine Linux开启BBR的方法",
      "description": "Alpine Linux系统开启BBR拥塞控制算法的命令和验证方法，适合小内存VPS使用的轻量系统。",
      "datePublished": "2025-07-12T23:17:31+08:00",
      "dateModified": "2025-07-12T23:17:31+08:00",
      "url": "https://vpsjq.com/2025/07/12/alpine-开启bbr/",
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
      "name": "Alpine Linux手动开启BBR",
      "step": [
        {
          "@type": "HowToStep",
          "name": "写入模块自动加载并立即加载",
          "text": "echo \"tcp_bbr\" >> /etc/modules把模块写入开机自动加载列表，modprobe tcp_bbr立即加载这个内核模块不用等重启。"
        },
        {
          "@type": "HowToStep",
          "name": "设置拥塞控制算法和队列规则",
          "text": "echo写入net.ipv4.tcp_congestion_control=bbr和net.core.default_qdisc=fq到/etc/sysctl.conf，再执行sysctl -p让配置立即生效。"
        },
        {
          "@type": "HowToStep",
          "name": "验证是否开启成功",
          "text": "用lsmod | grep bbr确认模块已加载，再用sysctl net.ipv4.tcp_congestion_control确认输出是bbr。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "为什么Alpine不能直接用常规的BBR一键脚本？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Alpine默认用的是OpenRC而不是systemd，一些常规Linux发行版的BBR开启方式（比如某些一键脚本依赖systemd相关命令）在Alpine上未必好使，需要用更基础的手动方式开启。"
          }
        }
      ]
    }
  ]
}
</script>

Alpine 是不少小内存VPS（比如256M内存）的首选系统，比Debian/Ubuntu这类系统空载内存占用低不少。不过Alpine默认用的是OpenRC而不是systemd，一些常规Linux发行版的BBR开启方式（比如某些一键脚本依赖systemd相关命令）在Alpine上未必好使，需要用更基础的方式手动开启。

这套命令原理跟[Linux TCP/IP和BBR参数智能优化脚本](https://vpsjq.com/2025/11/30/linux-tcp-ip-%E5%92%8C-bbr-%E5%8F%82%E6%95%B0%E6%99%BA%E8%83%BD%E4%BC%98%E5%8C%96%E8%84%9A%E6%9C%AC/)一样，只是那篇的一键脚本更适合通用发行版，Alpine系统更适合手动方式：

\`\`\`bash
echo "tcp_bbr" >> /etc/modules
modprobe tcp_bbr
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
sysctl -p
\`\`\`

第一条把 tcp_bbr 模块写入开机自动加载列表，第二条立即加载这个内核模块不用等重启，后面两条分别设置拥塞控制算法为BBR、默认队列规则为fq，最后 `sysctl -p` 让配置立即生效。

执行完之后验证有没有开启成功：

\`\`\`bash
lsmod | grep bbr
\`\`\`

返回类似 `tcp_bbr 16384 5` 这样的结果说明模块已经正常加载。也可以进一步确认当前生效的拥塞控制算法：

\`\`\`bash
sysctl net.ipv4.tcp_congestion_control
\`\`\`

输出 `bbr` 就说明开启成功了。BBR的原理和为什么有时候感觉没什么效果，可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，搞清楚原理之后对验证结果的判断会更准确。如果这台Alpine VPS还打算搭代理服务，可以看看[专为Alpine定制的Xray一键脚本](https://vpsjq.com/2025/07/01/%E4%B8%93%E4%B8%BAalpine%E5%AE%9A%E5%88%B6%E7%9A%84xray%E4%B8%80%E9%94%AE%E8%84%9A%E6%9C%AC/)，跟这篇一起用能把小内存VPS的性能和网络体验调到位。
