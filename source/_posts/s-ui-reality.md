---
title: S-UI面板搭建VLESS Reality节点
date: 2026-08-28 23:00:00
tags:
  - S-UI教程
  - VLESS Reality
categories:
  - vps技巧
description: 在S-UI面板里配置VLESS Reality节点的完整流程，包括dest目标网站设置、密钥生成和客户端连接配置。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI面板搭建VLESS Reality节点",
      "description": "在S-UI面板里配置VLESS Reality节点的完整流程，包括dest目标网站设置、密钥生成和客户端连接配置。",
      "datePublished": "2026-08-28T23:00:00+08:00",
      "dateModified": "2026-08-28T23:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/28/s-ui-reality/",
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
      "name": "S-UI配置VLESS Reality入站",
      "step": [
        {
          "@type": "HowToStep",
          "name": "新建入站选择Reality",
          "text": "进入S-UI面板找到入站管理，新建入站，协议选VLESS，传输方式选TCP，安全选项选Reality，顺序不能搞错，先选协议再选传输方式最后才能选到Reality。"
        },
        {
          "@type": "HowToStep",
          "name": "设置dest伪装目标网站",
          "text": "dest填一个真实存在的大流量网站，比如amazon.com，访问量大流量特征复杂不容易被识别，serverName填跟dest一样的值。"
        },
        {
          "@type": "HowToStep",
          "name": "生成密钥",
          "text": "shortId、publicKey和privateKey面板会自动生成，点生成按钮即可，privateKey只存在面板里不会出现在分享链接中。"
        },
        {
          "@type": "HowToStep",
          "name": "设置端口并放行",
          "text": "端口随机生成或自己填，Reality走TCP，放行对应TCP端口即可，不需要像Hysteria2那样单独放行UDP。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI的Reality节点连不上怎么排查？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "先确认防火墙端口是否放行，再对照检查客户端的publicKey、shortId、serverName跟面板是否一致，最后确认dest填的目标网站在服务器上能正常访问。"
          }
        }
      ]
    }
  ]
}
</script>

S-UI 配置 VLESS Reality 的流程跟 3x-ui 基本一样，操作逻辑相同，只是界面布局有些差别。Reality 不需要自己的域名和证书，这是它比普通 VLESS TLS 省事的地方，不用提前申请证书，也不用配置[SSL证书路径](https://vpsjq.com/2026/08/28/s-ui-certificate/)。

进入 S-UI 面板后，找到入站管理，新建入站，协议选 VLESS，传输方式选 TCP，安全选项选 Reality，下面会展开 Reality 相关的配置项。这几个选项的顺序不能搞错，先选协议，再选传输方式，最后才能选到 Reality。

dest 那一栏填伪装的目标网站，需要填一个真实存在的大流量网站，流量会伪装成访问这个网站。填 `amazon.com` 是比较常见的选择，访问量大、流量特征复杂，伪装进去不容易被识别。serverName 跟 dest 填一样的值就行。

shortId、publicKey 和 privateKey 这三个字段面板会自动生成，点生成按钮就有了，不需要手动计算。privateKey 只存在面板里，不会出现在分享链接里；publicKey 和 shortId 客户端连接时需要用到，导入链接的时候会自动带进去，不需要手动填。

端口随机生成或者自己填都可以，填完记得在防火墙放行。Reality 走的是 TCP，放行 TCP 端口就行，不需要像 Hysteria2 那样单独放行 UDP。

配置填完保存之后，在入站列表找到这条记录，点二维码图标可以看到分享链接，格式是 `vless://` 开头的，复制到客户端导入就能用。Clash Meta、sing-box、NekoBox、v2rayN 这些主流客户端都支持 VLESS Reality，导入链接之后基本不需要额外配置。

连不上的时候按这个顺序排查：先确认防火墙端口有没有放行，再对照检查客户端里的 publicKey、shortId、serverName 跟面板里的是否一致，最后确认 dest 填的目标网站在你的服务器上能正常访问。S-UI 和 3x-ui 的 Reality 配置思路完全一样，如果你之后考虑换到 3x-ui，可以参考[3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)，操作流程基本一致。
