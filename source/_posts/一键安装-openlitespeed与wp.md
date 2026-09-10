---
title: 一键安装 OpenLiteSpeed与WP
tags:
  - OpenLiteSpeed与wp
id: '29'
categories:
  - vps工具
abbrlink: 30137
date: 2025-05-06 12:00:43
description: 使用官方 ols1clk.sh 自动化脚本一键快速部署 OpenLiteSpeed Web 服务器以及 WordPress 站点环境。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "一键安装 OpenLiteSpeed与WP",
      "description": "使用官方 ols1clk.sh 自动化脚本一键快速部署 OpenLiteSpeed Web 服务器以及 WordPress 站点环境。",
      "datePublished": "2025-05-06T12:00:43+08:00",
      "dateModified": "2025-05-06T12:00:43+08:00",
      "url": "https://vpsjq.com/2025/05/06/一键安装-openlitespeed与wp/",
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
      "name": "一键安装OpenLiteSpeed和WordPress",
      "step": [
        {
          "@type": "HowToStep",
          "name": "安装OpenLiteSpeed",
          "text": "执行wget下载官方ols1clk.sh脚本后bash运行，或者直接用bash <(curl -k https://raw.githubusercontent.com/litespeedtech/ols1clk/master/ols1clk.sh)一步到位。"
        },
        {
          "@type": "HowToStep",
          "name": "安装WordPress",
          "text": "在同样的命令后加上-w参数，即bash <(curl -k https://raw.githubusercontent.com/litespeedtech/ols1clk/master/ols1clk.sh) -w，会在装好OpenLiteSpeed的同时一并部署WordPress站点环境。"
        }
      ]
    }
  ]
}
</script>

一键安装 OpenLiteSpeed与WP 运行wget https://raw.githubusercontent.com/litespeedtech/ols1clk/master/ols1clk.sh && bash `ols1clk.sh` 或 bash <( curl -k https://raw.githubusercontent.com/litespeedtech/ols1clk/master/ols1clk.sh )   安装 WordPress: bash <( curl -k https://raw.githubusercontent.com/litespeedtech/ols1clk/master/ols1clk.sh ) -w