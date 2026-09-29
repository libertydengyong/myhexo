---
title: S-UI配置普通VLESS节点：不用域名和证书的简单方案
date: 2026-09-29 22:00:00
tags:
  - S-UI教程
  - VLESS
categories:
  - vps技巧
description: S-UI面板配置普通VLESS节点的步骤，不需要域名和证书，几个基本参数填完就能用，适合测试场景，附长期使用的升级建议。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI配置普通VLESS节点：不用域名和证书的简单方案",
      "description": "S-UI面板配置普通VLESS节点的步骤，不需要域名和证书，几个基本参数填完就能用，适合测试场景，附长期使用的升级建议。",
      "datePublished": "2026-09-29T22:00:00+08:00",
      "dateModified": "2026-09-29T22:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/29/s-ui-vless/",
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
      "name": "S-UI配置普通VLESS节点",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建入站选择VLESS",
          "text": "进入S-UI面板入站管理，新建入站，协议选VLESS，传输方式选TCP，安全选项选none，不会展开额外配置项。"
        },
        {
          "@type": "HowToStep",
          "name": "设置端口并放行防火墙",
          "text": "端口随机生成或自己填，填完在防火墙放行对应端口。"
        },
        {
          "@type": "HowToStep",
          "name": "保存并获取分享链接",
          "text": "UUID自动生成不需要手动填，保存后在入站列表点二维码图标获取vless://分享链接。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI的普通VLESS节点连不上怎么排查？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "先确认防火墙端口是否放行，这是最常见的原因；再确认客户端的UUID、端口、服务器地址跟面板一致；最后确认客户端安全选项也选的是none，不能选TLS，否则握手会直接失败。"
          }
        },
        {
          "@type": "Question",
          "name": "普通VLESS适合长期用吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不太适合。安全选项选none时流量是明文传输的，容易被中间设备识别，只建议用来测试面板和客户端配置是否正常。长期稳定使用建议换成抗检测能力更强的VLESS Reality，S-UI原生支持，配置也不复杂。"
          }
        }
      ]
    }
  ]
}
</script>

面板部分假设已经按[S-UI面板搭建教程](/2025/11/17/s-ui面板搭建/)装好。S-UI 支持的协议里，普通 VLESS 是配置最简单的一种——不需要域名、不需要证书、不需要生成密钥对，跟已经讲过的[VLESS Reality](https://vpsjq.com/2026/08/28/s-ui-reality/)相比，少了 dest 伪装和密钥这些步骤，几个基本参数填完就能用，代价是抗封锁能力比较弱。

进入 S-UI 面板，找到**入站管理**，新建入站，协议选 **VLESS**，传输方式选 **TCP**，安全选项选 **none**。这几项选完之后不会展开额外的配置项，比 Reality 简单很多，选项顺序跟配置 Reality 时一样，都是先选协议、再选传输方式，最后才能选到安全选项。

端口随机生成或者自己填一个，填完记得在防火墙放行这个端口。UUID 那一栏面板会自动生成，不需要手动填。保存之后在入站列表找到这条记录，点二维码图标可以看到分享链接，格式是 `vless://` 开头的，复制到客户端导入就能用，Clash Meta、sing-box、NekoBox、v2rayN 这些主流客户端都支持。

连不上的时候按这个顺序排查：先确认防火墙端口有没有放行，这是最常见的原因；再确认客户端里的 UUID、端口、服务器地址跟面板一致；最后确认客户端的安全选项也选的是 **none**，不能选 TLS，两边不一致的话握手会直接失败，不会有明确的报错提示。

安全选项用 none 的时候流量是明文传输的，在网络环境复杂的地方容易被中间设备识别甚至篡改，这种配置更适合用来快速测试面板和客户端能不能正常通信，不建议长期当主力节点用。测试没问题之后，想换成抗检测能力更强的方案，可以参考[S-UI面板搭建VLESS Reality节点](https://vpsjq.com/2026/08/28/s-ui-reality/)，不需要域名，配置步骤也不复杂；如果服务器已经有域名和证书，也可以考虑配置 TLS，证书申请方法参考[S-UI面板申请和配置SSL证书](https://vpsjq.com/2026/08/28/s-ui-certificate/)。多个节点或者多个用户的管理方式可以参考[S-UI面板多用户管理](https://vpsjq.com/2026/08/29/s-ui-multi-user/)。
