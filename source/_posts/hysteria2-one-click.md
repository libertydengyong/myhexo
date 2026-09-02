---
title: Hysteria2一键安装脚本：老王工具箱、f佬和223脚本
date: 2026-09-02 12:00:00
tags:
  - Hysteria2
  - 3x-ui
categories:
  - vps工具
description: 三个常用的Hysteria2一键安装脚本：老王工具箱、f佬脚本和223脚本，都可以从GitHub找到，也集成在老王工具箱里，安装完看节点速度验证是否生效。
---

Hysteria2 是基于 QUIC 的代理协议，在高丢包高延迟的网络环境下表现比 TCP 系协议稳定，3x-ui 面板内置了 Hysteria2 支持，可以直接在面板里配置，具体方法参考[3x-ui配置Hysteria2节点教程](https://vpsjq.com/2026/08/27/3x-ui-hysteria2/)。如果不想用面板，也可以用一键脚本直接在服务器上安装独立的 Hysteria2。

目前比较常用的 Hysteria2 一键脚本有三个：老王工具箱、f佬的脚本和223的脚本。三个脚本都有独立的 GitHub 仓库，也都集成在老王工具箱里，可以通过老王工具箱的菜单统一管理。

老王工具箱的安装命令：

\`\`\`bash
wget -qO ssh_tool.sh https://raw.githubusercontent.com/eooce/ssh_tool/main/ssh_tool.sh && chmod +x ssh_tool.sh && ./ssh_tool.sh
\`\`\`

跑完会出现一个菜单，从菜单里选择安装 Hysteria2 的选项，脚本会自动处理依赖安装和配置。f佬和223的独立脚本安装命令去各自的 GitHub 仓库找最新版本，README 里有当前维护的命令。

安装完之后验证 Hysteria2 是否正常运行，最直接的方式是把节点导入客户端测试连接速度，速度正常说明运行没有问题。也可以检查服务状态：

\`\`\`bash
systemctl status hysteria-server
\`\`\`

显示 active (running) 说明服务在跑。

Hysteria2 走的是 UDP 协议，防火墙需要单独放行 UDP 端口，不是只开 TCP 就够了：

\`\`\`bash
ufw allow 你的端口号/udp
\`\`\`

如果服务商有安全组（比如甲骨文、AWS），同样需要在控制台手动加 UDP 入站规则，光在系统防火墙放行不够。连不上的时候这是最常见的原因。

独立脚本安装的 Hysteria2 和通过 3x-ui 面板配置的 Hysteria2 在使用上没有本质区别，区别在于管理方式——独立脚本直接在服务器上管理，3x-ui 面板提供图形界面，多节点多用户的情况下面板更方便管理，参考[3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)。
