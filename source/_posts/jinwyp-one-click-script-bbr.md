---
title: Jinwyp一键脚本安装BBR和BBRplus内核教程
date: 2026-09-06 21:00:00
tags:
  - Jinwyp
  - BBR加速
  - 一键脚本
categories:
  - vps工具
description: Jinwyp的one_click_script脚本安装BBR和BBRplus的完整步骤，包括CentOS/Debian/Ubuntu各系统对应的菜单选项和安装后启用的方法。
---
Jinwyp这个GitHub作者维护的one_click_script脚本包，是圈子里流传比较广的一键工具箱之一，里面装内核、启用BBR/BBRplus的那部分功能一直有人在用。跟[BBRplus一键安装教程](https://vpsjq.com/2025/05/06/bbrplus与其他加速方式安装/)里的zeruns版本比，两者思路类似，都是先装对应内核再启用加速算法，具体选哪个看个人习惯，功能上没有本质区别。
<!-- more -->
下载运行这个脚本包里专门管内核和BBR的部分：

```bash
wget --no-check-certificate https://raw.githubusercontent.com/jinwyp/one_click_script/master/install_kernel.sh && chmod +x ./install_kernel.sh && ./install_kernel.sh
```

跑起来之后会出现菜单，根据自己的系统选对应的编号：

- **CentOS / AlmaLinux / Rocky Linux**：选31装最新5.16内核，或者选35装LTS 5.10内核（官方建议选这个，稳定性更好）
- **Debian**：选41装LTS 5.10内核
- **Ubuntu**：选45装LTS 5.10内核

装内核这一步过程中会重启两次，属于正常现象，不用担心。重启过程中如果出现警告界面提示删除旧内核，选"No"继续，不要中断。

内核装完之后，重新运行一次同一个脚本，这时候菜单里选2，就能启用BBR拥塞控制算法（会问你要不要搭配Cake或者FQ，官方推荐Cake）。如果想用BBRplus而不是普通BBR，装内核那一步就要选不一样的编号：选61装BBRplus 4.14.129内核，或者选66装BBRplus 5.10 LTS内核，同样会重启两次，装完后重新运行脚本选3来启用BBRplus。

如果想用XanMod内核搭配BBR2，脚本里也有对应选项：选51装XanMod LTS 5.10内核，重启完成后重新运行脚本选2启用BBR2。这个跟单独装XanMod的思路是一致的，如果只想用XanMod自带的BBR3方案，可以直接参考[XanMod内核搭配BBR3使用教程](https://vpsjq.com/2026/08/27/xanmod-bbr3/)，不需要额外跑这个脚本。

装完不管选的哪种加速方式，验证有没有生效的方法都一样：

```bash
lsmod | grep bbr
```

看到对应的模块名（bbr、bbrplus）就说明启用成功了。如果验证结果不对，或者感觉不到明显提速，可以参考[为什么开了BBR网速却感觉一点没提升](https://vpsjq.com/2026/08/18/bbr-no-improvement/)，排查一下是不是别的原因导致的。
