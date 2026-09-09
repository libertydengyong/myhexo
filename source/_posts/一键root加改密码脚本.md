---
title: 一键root加改密码脚本
tags:
  - 一键root加改密码脚本
id: '194'
categories:
  - vps技巧
abbrlink: 60516
date: 2025-12-31 16:20:33
description: 适用于甲骨文等 VPS 的一键开启 root 登录与修改密码脚本，自动检测包管理器、安装 Sudo/SSH 并允许密码认证。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "一键root加改密码脚本",
      "description": "适用于甲骨文等 VPS 的一键开启 root 登录与修改密码脚本，自动检测包管理器、安装 Sudo/SSH 并允许密码认证。",
      "datePublished": "2025-12-31T16:20:33+08:00",
      "dateModified": "2025-12-31T16:20:33+08:00",
      "url": "https://vpsjq.com/2025/12/31/一键root加改密码脚本/",
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
      "name": "用一键脚本开启root密码登录",
      "step": [
        {
          "@type": "HowToStep",
          "name": "下载脚本",
          "text": "执行curl -fsSL -o root.sh \"https://github.com/tonyliuzj/oneclick-root/releases/latest/download/root.sh\" && chmod +x root.sh。"
        },
        {
          "@type": "HowToStep",
          "name": "以root权限运行脚本",
          "text": "执行sudo ./root.sh，脚本会自动检测包管理器、更新软件包列表、安装sudo和openssh-server。"
        },
        {
          "@type": "HowToStep",
          "name": "设置新密码并完成配置",
          "text": "脚本会提示设置新的root密码，随后自动配置SSH允许root使用密码认证登录，并重启SSH服务使配置生效。"
        }
      ]
    }
  ]
}
</script>

来源:nodeseek   一键root加改密码脚本，包括适用于甲骨文：

```bash
curl -fsSL -o root.sh "https://github.com/tonyliuzj/oneclick-root/releases/latest/download/root.sh" && chmod +x root.sh && sudo ./root.sh
```

项目地址：https://github.com/tonyliuzj/oneclick-root   使用 root 权限运行脚本：sudo ./root.sh 脚本将会： 检测你的包管理器 更新软件包列表 安装 sudo 和 openssh-server 提示设置新的 root 密码 配置 SSH 允许 root 使用密码认证登录 重启 SSH 服务