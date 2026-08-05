---
title: 一个轻量级 Xray 面板
tags:
  - 轻量级 Xray 面板
id: '137'
categories:
  - vps工具
abbrlink: 38147
date: 2025-07-09 12:32:25
description: FranzKafkaYu/x-ui是vaxilu原版x-ui的一个分支，单端口支持多协议多用户，目前该仓库已归档不再更新。
---

**轻量级 Xray 面板** bash <(curl -Ls https://raw.githubusercontent.com/FranzKafkaYu/x-ui/master/install.sh)   项目来源:   https://github.com/FranzKafkaYu/x-ui?tab=readme-ov-file#%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85

这是**FranzKafkaYu/x-ui**，同样是vaxilu原版x-ui的一个分支（fork），特点是单端口支持多协议多用户，同时支持英文界面和Telegram机器人集成，操作体验做了不少优化。

需要说明的是，这个仓库目前在GitHub上标注为**"Public archive"（已归档）**，意味着作者已经停止更新维护了。

## 主要功能

- 单端口多用户多协议，不用为每个用户/协议单独开端口
- 支持中英文双语界面
- 面板管理菜单里直接有"一键安装BBR"选项，装完面板顺手就能优化网络
- 默认端口54321，默认账号admin/admin，安装或更新时会提示修改，不修改则保持默认值

## 安装时的注意事项

装的时候如果不想用默认端口和账号密码，记得在安装过程或者装完后通过面板菜单里的"重置用户名密码""设置面板端口"选项及时改掉，避免使用默认凭据被扫描发现。

由于这个仓库已经不再更新，如果比较在意能不能持续获得新协议支持（比如VLESS Reality这类近几年才出现的协议），建议直接看活跃维护的[xui官网一键安装脚本](https://vpsjq.com/2026/04/30/2026-04-30-011/)（MHSanaei/3x-ui），功能更新更及时。
