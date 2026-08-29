---
title: 常用VPS TCP加速脚本汇总
date: 2026-08-29 20:00:00
tags:
  - BBR加速
  - Linux网络优化
categories:
  - Linux优化
description: 四个常用VPS TCP加速脚本的特点和适用场景对比，包括Eric86777/vps-tcp-tune、zeruns/tcp.sh、adsorgcn/bbr-script和yahuisme的优化脚本。
---

VPS 网络优化的脚本很多，功能侧重不一样，选错了要么效果不明显，要么跟现有环境冲突。这篇整理了几个实际用过的脚本，说一下各自的特点和适用场景。

**Eric86777/vps-tcp-tune** 是日常用得最多的一个，主要做 TCP 参数调优，包含33项实用优化功能，安装命令去 GitHub 仓库找最新的：`https://github.com/Eric86777/vps-tcp-tune`。这个脚本的特点是专注 TCP 层面的参数调整，不涉及内核替换，适合不想动内核但又想优化网络的场景，稳定性比较好，日常维护服务器首选这个。

**zeruns/tcp.sh** 是一个五合一的加速脚本，把 BBRplus、BBR 魔改版、暴力 BBR 等几种加速方式打包在一起，安装时从菜单里选要装哪种，具体安装方法可以参考[BBRplus与其他加速方式安装](https://vpsjq.com/2025/05/06/bbrplus%E4%B8%8E%E5%85%B6%E4%BB%96%E5%8A%A0%E9%80%9F%E6%96%B9%E5%BC%8F%E5%AE%89%E8%A3%85/)。适合想一次性试几种加速方式、看哪个效果好的情况，但需要注意这个脚本会安装第三方内核，装之前确认 VPS 支持换内核。

**adsorgcn/bbr-script** 的特点是支持自动升级内核，适合内核版本太旧、不支持 BBR 的 VPS。脚本会检测当前内核版本，如果不够新会自动引导升级，升级完重启就能开启 BBR，省去了手动升级内核的麻烦。具体使用方法参考[Debian和Ubuntu开启BBR加速的两种方式](https://vpsjq.com/2026/08/28/debian-ubuntu-bbr/)，里面有完整的安装命令和验证步骤。适合 Debian 和 Ubuntu 系统，内核版本在 4.9 以下的 VPS 用这个最省事。

**yahuisme/network-optimization** 是一个综合优化脚本，同时调整 BBR 和 TCP 缓冲区、队列规则等多个参数，不需要手动挨个改配置文件，跑完自动应用，适合想一次性把网络参数都调好的场景，具体效果和使用方法参考[Linux TCP/IP和BBR参数智能优化脚本](https://vpsjq.com/2025/11/30/linux-tcp-ip-%E5%92%8C-bbr-%E5%8F%82%E6%95%B0%E6%99%BA%E8%83%BD%E4%BC%98%E5%8C%96%E8%84%9A%E6%9C%AC/)。

这四个脚本不需要叠加使用，选一个适合自己场景的就行，混着装容易参数冲突。如果只是想快速优化一台新 VPS，Eric86777/vps-tcp-tune 是最省事的选择；如果内核版本太旧需要升级，用 adsorgcn/bbr-script；如果想试试 BBRplus 这类第三方加速，用 zeruns/tcp.sh；想一次性把 BBR 和 TCP 参数都调好，用 yahuisme/network-optimization。各版本 BBR 之间的区别和选择思路可以参考[BBR、BBR2、BBRplus、BBR3有什么区别](https://vpsjq.com/2026/08/28/bbr-versions-compare/)。
