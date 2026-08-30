---
title: 3x-ui配置Warp给服务器添加IPv4/IPv6出口
date: 2026-08-30 22:00:00
tags:
  - 3x-ui
  - Warp
  - IPv6
categories:
  - vps工具
description: 在3x-ui面板里配置Cloudflare Warp，给服务器添加IPv4或IPv6出口，包括warp安装和Xray出站配置步骤。
---

Cloudflare Warp 可以给服务器添加一个额外的网络出口，纯 IPv6 的 VPS 可以通过 Warp 获得 IPv4 出口，纯 IPv4 的服务器可以通过 Warp 获得 IPv6 出口。3x-ui 面板里有专门的 Warp 配置入口，在 Xray 设置里添加 Warp 出站，不需要手动编辑配置文件。

第一步先在服务器上安装 Warp，用 fscarmen 维护的一键安装脚本，安装命令去 GitHub 仓库找最新的：`https://github.com/fscarmen/warp`，README 里有当前维护的安装命令，根据你的需求选择添加 IPv4 还是 IPv6 出口。安装完之后 Warp 会在服务器上创建一个虚拟网络接口，流量可以通过这个接口走 Cloudflare 的网络出去。

安装完 Warp 之后，进入 3x-ui 面板，点左侧 **Xray** 选项，找到出站（Outbounds）配置，添加一个新的出站，类型选 Warp 或者按 fscarmen 脚本说明里对应的配置方式填写。配置好出站之后，在路由规则里把需要走 Warp 的流量指向这个出站，比如某些特定域名或者 IP 段走 Warp，其他流量还是走原来的出口。路由规则的配置方式参考[3x-ui路由规则配置](https://vpsjq.com/2026/08/29/3x-ui-routing/)。

配置完之后验证一下 Warp 有没有生效，访问 `ip.sb` 或者 `ifconfig.me` 看一下出口 IP，如果显示的是 Cloudflare 的 IP 段说明流量走了 Warp 出口。速度上 Warp 不会明显变慢，日常使用基本感觉不到差别。

对于纯 IPv6 的 VPS 来说，加了 Warp 之后可以访问只支持 IPv4 的网站和服务，也可以直接用来安装 3x-ui 这类需要从 GitHub 拉取文件的脚本，不需要额外折腾其他添加 IPv4 出口的方案。纯 IPv6 VPS 搭节点的完整流程可以参考[纯IPv6 VPS用3x-ui搭建节点教程](https://vpsjq.com/2026/08/29/ipv6-vps-3xui-node/)。
