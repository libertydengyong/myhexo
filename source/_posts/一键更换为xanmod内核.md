---
title: 一键更换为XanMod内核
tags:
  - XanMod内核
id: '41'
categories:
  - vps工具
abbrlink: 405
date: 2025-05-07 21:39:51
description: 使用 ylx2016 的 tcpx.sh 经典网络加速脚本一键安装与替换 Linux 系统 XanMod 内核的命令行指南，附 Debian/Ubuntu 系发行版通用说明。
---

用 ylx2016 维护的 `tcpx.sh` 这个网络加速脚本合集，可以直接一键换成 XanMod 内核，不需要自己手动配置 APT 仓库：

```bash
wget -O tcpx.sh "https://github.com/ylx2016/Linux-NetSpeed/raw/master/tcpx.sh" && chmod +x tcpx.sh && ./tcpx.sh
```

脚本运行后会给出一个菜单，里面除了 XanMod 相关选项，也包含 BBR 加速这些功能，按提示选择对应的内核版本安装即可。

这套方法本质上是脚本自动帮你配置好了 XanMod 官方的 APT 仓库，所以 Debian 和 Ubuntu 系的发行版都适用，原理上没有区别，脚本会自动识别系统版本代号去匹配对应的仓库源。

如果不想用第三方脚本，也可以手动添加 XanMod 官方仓库自己安装，具体命令可以参考 xanmod.org 官网的安装说明。

## 相关文章

- [装了XanMod内核出问题，怎么卸载切回默认内核](https://vpsjq.com/2026/08/27/xanmod-uninstall-rollback/)
- [XanMod内核怎么更新](https://vpsjq.com/2026/08/28/xanmod-update/)
- [XanMod内核版本怎么选：edge、lts和普通版的区别](https://vpsjq.com/2026/08/28/xanmod-versions-choose/)
- [XanMod内核部署Xray、Trojan并优化服务器](https://vpsjq.com/2026/07/28/2026-07-28-001/)
- [使用USTC 公共镜像加速器](https://vpsjq.com/2025/07/24/使用ustc-公共镜像加速器/)
