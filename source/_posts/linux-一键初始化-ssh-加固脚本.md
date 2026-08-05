---
title: Linux 一键初始化 & SSH 加固脚本
tags:
  - Linux 一键初始化 &amp; SSH 加固脚本
id: '184'
categories:
  - vps技巧
abbrlink: 5233
date: 2025-12-12 21:12:01
description: Linux VPS拿到手后的初始化和SSH安全加固脚本，降低暴力破解风险，新服务器上线前建议先跑一遍。
---

Linux 一键初始化 & SSH 加固脚本 curl -fsSL https://raw.githubusercontent.com/247like/linux-ssh-init-sh/main/init.sh -o ./init.sh && chmod +x init.sh && ./init.sh   来源：https://github.com/247like/linux-ssh-init-sh

公网上的VPS只要开着SSH默认端口，几分钟内就会有自动化脚本开始扫描尝试暴力破解，这不是危言耸听，而是新服务器上线后几乎必然会遇到的情况。这类"初始化加固脚本"存在的意义，就是把几项关键的安全加固操作打包，新VPS到手先跑一遍，比裸奔状态直接用安全得多。

## 这类脚本通常会处理哪些事

具体到这个脚本能做到哪几项，建议实际跑一遍看交互过程，通用的SSH加固类脚本一般会覆盖：

- **修改SSH默认端口**：22端口是扫描重灾区，换成非默认端口能过滤掉大部分无脑扫描
- **禁用密码登录，强制密钥认证**：暴力破解密码的攻击对纯密钥认证基本无效
- **限制root直接登录**：改用普通用户+sudo的方式管理，降低root账号被直接攻破的风险
- **安装fail2ban类工具**：检测到多次登录失败自动封禁来源IP一段时间

## 使用建议

新VPS到手，建议**先跑加固脚本，再部署具体的业务/代理服务**，顺序很重要——如果先装好一堆服务再加固，中间这段裸奔窗口期风险最高。

跑完这个脚本，如果VPS上还想装点常用管理工具，可以看看之前写的[VPS一键系统管理](https://vpsjq.com/2025/11/25/vps%E4%B8%80%E9%94%AE%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%EF%BC%9A-bash/)，两篇一个管安全加固、一个管日常系统维护，配合起来用比较完整。
