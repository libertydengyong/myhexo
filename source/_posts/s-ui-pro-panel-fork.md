---
title: S-UI 原版和分叉版（S-UI Pro Panel）有什么区别
date: 2026-09-07 09:30:00
updated: 2026-09-07 09:30:00
tags:
  - S-UI教程
  - 面板对比
categories:
  - vps技巧
description: S-UI 官方原版（alireza0/s-ui）和社区分叉版 S-UI Pro Panel（vchan-ui/s-ui）有什么区别，该装哪个，这篇文章说清楚两者的功能差异和安装方式。
keywords: s-ui原版分叉区别,s-ui pro panel,vchan-ui s-ui,s-ui分叉版,alireza0 s-ui区别
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "S-UI 有分叉版本吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "有，社区在 alireza0/s-ui v1.4.1 基础上做了一个增强二次开发版本，仓库地址是 vchan-ui/s-ui，项目名叫 S-UI Pro Panel，主打结构优化、界面升级和功能扩展。"
      }
    },
    {
      "@type": "Question",
      "name": "该装原版还是 S-UI Pro Panel？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "官方原版更新持续、社区资料和已有教程都基于它，求稳定优先选原版；S-UI Pro Panel 在原版基础上做了功能扩展和界面优化，如果想尝试增强功能可以考虑，但相对小众、踩坑时能查到的资料会少一些。"
      }
    }
  ]
}
</script>

搜"S-UI 原版 分叉 区别"的人，大概率是在网上看到了两个不同的 S-UI 安装命令，分不清哪个是正版、该装哪个。这篇文章把官方原版和目前已知的分叉版本放在一起说清楚。

## 官方原版：alireza0/s-ui

站内之前所有教程默认用的都是这个官方仓库，安装命令：

```
bash <(curl -Ls https://raw.githubusercontent.com/alireza0/s-ui/master/install.sh)
```

这是项目的原始出处，作者持续在维护更新，社区资料和踩坑经验也基本都是围绕这个版本积累的。

## 分叉版：S-UI Pro Panel（vchan-ui/s-ui）

这是社区基于 alireza0/s-ui v1.4.1 做的增强二次开发版本，官方 Wiki 里的自我介绍是"结构优化、界面升级与功能扩展"，安装命令是：

```
bash <(curl -Ls https://raw.githubusercontent.com/vchan-ui/s-ui/main/install.sh)
```

**默认安装信息**（和原版基本一致）：

| 项目 | 默认值 |
|---|---|
| 面板端口 | 2095 |
| 面板路径 | /app/ |
| 订阅端口 | 2096 |
| 订阅路径 | /sub/ |
| 用户名/密码 | admin/admin |

**支持的功能**：多协议、多语言、多客户端/入站、高级流量路由界面、客户端与系统状态查看、订阅链接（link/json/clash + info）、深色/浅色主题、API 接口、增强路由与可视化优化。

**支持平台**：Linux（amd64/arm64/armv7/armv6/armv5/386/s390x）、Windows（amd64/386/arm64）、macOS（实验性支持，amd64/arm64）。

从功能列表能看出来，Pro Panel 在原版基础上主要加强了两块：**API 接口**和**流量路由的可视化/增强能力**，这跟前面那条搜索结果里提到的"以 API 优先、自动化部署为目标"是对得上的，适合想通过接口做自动化管理、批量部署节点的场景。

## 该选哪个

- **想跟着现成教程走，少踩坑**：选官方原版 alireza0/s-ui，本站目前所有 S-UI 教程都是基于这个版本写的，包括 [Hysteria2 节点搭建](https://vpsjq.com/2026/09/06/S-UI-%E6%90%AD%E5%BB%BA-Hysteria2-%E8%8A%82%E7%82%B9%E6%95%99%E7%A8%8B/)、[TUIC 节点搭建](https://vpsjq.com/2026/09/06/s-ui-tuic/) 这些，直接照搬能用。
- **需要 API 自动化管理，或者想要更完善的路由可视化界面**：可以考虑试试 S-UI Pro Panel，但要有心理准备——这是相对小众的分叉版本，遇到问题能查到的中文资料会比原版少很多，官方 Wiki 是目前最直接的参考来源。
- **两者能不能混用/迁移**：Pro Panel 基于 v1.4.1 分叉，理论上数据结构接近，但没有验证过双向迁移是否完全兼容，如果要切换建议先在测试环境验证，不要直接在生产节点上冒险迁移。

如果你还没决定用哪个，建议先按官方原版把节点跑起来熟悉一遍操作逻辑，再决定要不要为了某个具体功能（比如 API 自动化）切换到分叉版本，不用一开始就纠结这个选择。
