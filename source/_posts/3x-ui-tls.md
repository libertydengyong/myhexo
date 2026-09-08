---
title: 3x-ui配置TLS证书教程
date: 2026-08-30 23:00:00
tags:
  - 3x-ui
  - TLS
categories:
  - vps工具
description: 在3x-ui面板里申请Let's Encrypt证书并配置TLS的完整步骤，需要域名，证书路径在入站设置里单独填写。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui配置TLS证书教程",
      "description": "在3x-ui面板里申请Let's Encrypt证书并配置TLS的完整步骤，需要域名，证书路径在入站设置里单独填写。",
      "datePublished": "2026-08-30T23:00:00+08:00",
      "dateModified": "2026-08-30T23:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/30/3x-ui-tls/",
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
      "name": "3x-ui申请Let's Encrypt证书并配置TLS",
      "step": [
        {
          "@type": "HowToStep",
          "name": "确认域名解析和80端口",
          "text": "域名的A记录要已经指向服务器IP，且80端口需要开放，用ufw allow 80放行，因为Let's Encrypt的HTTP验证需要从外部访问80端口完成。"
        },
        {
          "@type": "HowToStep",
          "name": "在面板申请证书",
          "text": "进入面板点左侧面板设置，找到SSL证书管理入口，填入域名点申请证书，申请成功后面板会显示证书文件保存路径。"
        },
        {
          "@type": "HowToStep",
          "name": "在入站设置里填写证书路径",
          "text": "新建入站时安全选项选TLS，展开的配置项里把证书文件路径(.crt)和私钥文件路径(.key)分别填好，每个需要TLS的入站都要单独填一次，不是全局统一配置。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "TLS和VLESS Reality该怎么选？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "TLS需要域名和证书但兼容性更好，几乎所有客户端都支持；Reality不需要域名，配置方法参考3x-ui配置VLESS Reality节点教程，不想折腾域名的话可以选Reality。"
          }
        },
        {
          "@type": "Question",
          "name": "证书到期了怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "证书有效期90天，到期前Let's Encrypt会自动续期，面板申请的证书通常也会自动续期。如果没有自动续期导致节点因证书过期无法连接，手动重新申请一次即可。"
          }
        }
      ]
    }
  ]
}
</script>

3x-ui 配置 TLS 需要有自己的域名，域名解析到服务器 IP 之后，可以在面板里直接申请 Let's Encrypt 免费证书，不需要额外用 acme.sh 这类命令行工具。申请完证书之后在入站设置里填好证书路径，安全选项选 TLS 就能用了。

申请证书之前先确认两件事：域名的 A 记录已经指向这台服务器的 IP，解析生效需要一点时间，没生效的话申请会失败；80 端口要开放，Let's Encrypt 的 HTTP 验证需要从外部访问服务器的 80 端口完成验证：

\`\`\`bash
ufw allow 80
\`\`\`

确认好之后进入 3x-ui 面板，点左侧 **面板设置**，找到 SSL 证书管理的入口，填入你的域名，点申请证书。申请成功后面板会显示证书文件的保存路径，记下来，后面配置入站的时候要用。

新建入站的时候，协议选好之后，安全选项那一栏选 **TLS**，下面会展开证书相关的配置项，把刚才申请证书时的路径填进去——证书文件路径（.crt 文件）和私钥文件路径（.key 文件）分别填好，保存就行。每个需要 TLS 的入站都要单独填一次证书路径，不是在面板全局设置里统一配置的。

TLS 比普通 none 安全很多，流量加密传输，不容易被中间设备识别和篡改。跟 VLESS Reality 相比，TLS 需要域名和证书，Reality 不需要，但 TLS 的兼容性更好，几乎所有客户端都支持。如果不想折腾域名，可以用 Reality 代替，配置方法参考[3x-ui配置VLESS Reality节点教程](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)。

证书有效期是90天，到期前 Let's Encrypt 会自动续期，面板里申请的证书通常也会自动续期，不需要手动操作。如果证书到期后没有自动续期，节点会因为证书过期无法连接，这时候手动重新申请一次就行。
