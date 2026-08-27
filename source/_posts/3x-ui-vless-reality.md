---
title: 3x-ui配置VLESS Reality节点教程
date: 2026-08-27 16:00:00
tags:
  - 3x-ui
  - VLESS Reality
categories:
  - vps工具
description: 在3x-ui面板里新建VLESS Reality入站节点的完整流程，包括dest目标网站、证书密钥生成和客户端连接配置。
---

VLESS Reality
cat >> ~/myhexo/source/_posts/3x-ui-vless-reality.md << 'EOF'

shortId、publicKey 和 privateKey 这三个字段面板会自动生成，点一下生成按钮就有了，不需要自己算。privateKey 是私钥，只存在面板里，不会出现在分享链接里；publicKey 是公钥，客户端连接时需要用到。shortId 是一个短字符串，客户端那边也需要填，面板生成的直接用就行，也可以自己改成别的值，只要客户端和面板两边一致就没问题。

配置填完保存之后，在入站列表找到这条记录，点二维码图标可以看到分享链接，格式是 `vless://` 开头的，链接里已经包含了 publicKey、shortId、dest 这些参数，复制到客户端直接导入就能用，不需要手动填这些字段。

客户端这边，Clash Meta、sing-box、NekoBox、v2rayN 这些主流客户端都支持 VLESS Reality，导入链接之后基本不需要额外配置。如果是手动填参数的客户端，注意 publicKey 和 shortId 不能填错，这两个填错了连接直接失败，不会有任何提示，排查的时候容易忽略。

连不上的时候先确认防火墙端口有没有放行，再对照检查客户端里的 publicKey、shortId、serverName 跟面板里的是否一致。dest 填的目标网站在你的服务器上要能正常访问，如果服务器本身访问不了 `amazon.com`，伪装就没有意义，这种情况换一个你的服务器能访问的目标网站。

VLESS Reality 跟 Hysteria2 定位不太一样，Reality 走 TCP 伪装，适合对流量特征要求高的场景；Hysteria2 走 UDP，在高丢包网络下更稳定，两个协议可以同时配置，参考[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)。多用户管理的方式两个协议都一样，具体操作看[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)。
