---
title: 纯IPv6 VPS用3x-ui搭建节点教程
date: 2026-08-29 12:00:00
tags:
  - 3x-ui
  - IPv6
categories:
  - vps技巧
description: 在纯IPv6 VPS上用3x-ui搭建代理节点的完整流程，包括先添加IPv4出口、安装3x-ui面板和客户端连接注意事项。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "纯IPv6 VPS用3x-ui搭建节点教程",
      "description": "在纯IPv6 VPS上用3x-ui搭建代理节点的完整流程，包括先添加IPv4出口、安装3x-ui面板和客户端连接注意事项。",
      "datePublished": "2026-08-29T12:00:00+08:00",
      "dateModified": "2026-08-29T12:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/29/ipv6-vps-3xui-node/",
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
      "name": "纯IPv6 VPS搭建3x-ui节点",
      "step": [
        {
          "@type": "HowToStep",
          "name": "先添加IPv4出口",
          "text": "纯IPv6 VPS上很多命令和脚本依赖IPv4网络，没有IPv4出口直接跑3x-ui安装脚本会卡住或报错，需要先给服务器加一个IPv4出口。"
        },
        {
          "@type": "HowToStep",
          "name": "安装3x-ui面板",
          "text": "IPv4出口配置好之后，正常运行3x-ui一键安装脚本即可，跟普通VPS没有区别，安装完终端会打印面板地址、端口、用户名密码。"
        },
        {
          "@type": "HowToStep",
          "name": "配置入站监听地址",
          "text": "新建入站节点时，纯IPv6服务器监听地址不能填0.0.0.0（只监听IPv4），需要填::才能同时监听IPv6地址，或者直接填服务器的IPv6地址。"
        },
        {
          "@type": "HowToStep",
          "name": "处理客户端IPv6兼容性",
          "text": "客户端连接纯IPv6节点需要客户端本身和所在网络都支持IPv6，可以先访问test-ipv6.com测试；如果客户端网络不支持，可以在面板里额外配置一个走IPv4的入站端口。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "纯IPv6节点连不上怎么排查？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "先检查面板端口有没有在防火墙放行，纯IPv6服务器防火墙需要同时处理IPv4和IPv6两套规则，只放行IPv4端口在IPv6环境下不一定生效。"
          }
        }
      ]
    }
  ]
}
</script>

纯IPv6 VPS价格通常比较低，AWS EC2、EUserv、hax.co.id这类平台都有免费或者低价的纯IPv6机器，但用起来有一个绕不开的问题：很多命令和脚本依赖IPv4网络，没有IPv4出口的情况下直接运行往往会失败，包括3x-ui的安装脚本。所以在纯IPv6 VPS上搭节点，第一步不是装面板，而是先给服务器加一个IPv4出口。

添加IPv4出口的方法站内有两篇记录，可以先参考[IPv6 only VPS添加IPv4](https://vpsjq.com/2026/07/26/2026-07-26-002/)或者[为纯IPv6的小鸡添加v4出口](https://vpsjq.com/2026/04/30/2026-04-30-002/)，把IPv4出口加好之后再继续下面的步骤。没有IPv4出口直接装3x-ui，安装脚本下载依赖的时候就会卡住或者报错，很多apt包也拉不下来。

IPv4出口配置好之后，3x-ui的安装跟普通VPS没有区别，直接跑一键安装脚本：

\`\`\`bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
\`\`\`

安装完之后终端会打印面板地址、端口、用户名和密码，照着登录就行。

登录面板之后新建入站节点，协议和配置跟普通VPS上的操作一样，具体可以参考[3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)或者[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)。纯IPv6 VPS上配置节点有一个地方需要注意：监听地址如果填的是 `0.0.0.0`，只会监听IPv4地址，纯IPv6服务器上需要填 `::` 才能同时监听IPv6地址，或者直接填服务器的IPv6地址。

客户端连接纯IPv6节点，需要客户端本身支持IPv6，而且客户端所在的网络也要能访问IPv6地址。如果你的手机或者电脑网络本身不支持IPv6，就算服务器端配置完全正确，客户端也连不上。可以先在客户端设备上测试一下有没有IPv6网络，访问 `test-ipv6.com` 看一下结果。

如果客户端网络不支持IPv6，有两个解决办法：一是给服务器加IPv4出口之后，在面板里同时配置一个走IPv4的入站端口，客户端用IPv4地址连；二是找一台支持IPv6的中转机做中转，落地到这台纯IPv6服务器。对于大多数用户来说，加了IPv4出口之后直接配置IPv4入站是最简单的方案。

节点搭好之后建议测试一下连接是否正常，客户端导入节点链接，连上之后检查一下出口IP，确认流量走的是这台服务器而不是本地网络。如果连不上，先检查面板端口有没有在防火墙放行，纯IPv6服务器上防火墙规则需要同时处理IPv4和IPv6两套规则，只放行IPv4端口在IPv6环境下不一定生效。
