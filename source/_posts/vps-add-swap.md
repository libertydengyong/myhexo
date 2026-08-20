---
title: VPS怎么添加SWAP虚拟内存
date: 2026-08-16 10:00:00
tags:
  - SWAP虚拟内存
categories:
  - vps工具
description: VPS内存不够用时添加SWAP虚拟内存的完整步骤，fallocate创建、mkswap格式化、写入fstab永久生效。
---

小内存VPS（512M、1G这种）跑着跑着突然卡死、甚至直接断连，很多时候不是CPU的问题，是内存被吃满之后系统开始疯狂调度，最后干脆被OOM Killer强制杀进程。加一块SWAP能给系统一个缓冲，扛住突发的内存峰值。

## 创建SWAP文件

```bash
fallocate -l 2G /swapfile
```

这条最快，2G大小按需要调整。如果提示`fallocate failed`（有些VPS的文件系统不支持这个方式），换成dd代替，慢一点但更保险：

```bash
dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress
```

## 格式化并启用

**权限一定要先改，再执行mkswap**，顺序不能反：

```bash
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

先收紧权限是因为SWAP文件默认权限是所有用户可读，如果反过来先mkswap再改权限，中间那个时间窗口里，本机其他用户理论上能读到SWAP里的内容（可能包含敏感数据），顺序调换一下就避免了这个风险。

跑完用`free -h`看一眼，Swap那一行应该已经显示出对应的容量了。

## 让它重启后依然生效

上面的步骤重启就没了，得写进`/etc/fstab`才能永久生效：

```bash
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

## 大小怎么定

没有一刀切的标准，常见的参考是跟物理内存差不多大——1G内存配1-2G SWAP，2G内存配2-4G SWAP。内存越大，SWAP的边际作用其实越小，几十G内存的机器一般不太需要靠SWAP兜底。

## 调一下系统用SWAP的积极程度

系统默认不会等到内存完全用尽才动用SWAP，有个`swappiness`参数控制着系统"多主动"往SWAP里挪数据，数值范围0-100，默认通常是60。这个值调低一点，能让系统尽量优先用物理内存，只有真的紧张了才动用SWAP：

```bash
sysctl vm.swappiness=10
echo "vm.swappiness=10" >> /etc/sysctl.conf
```

第二条是为了重启后依然生效。这个值不是越低越好，调到0基本等于关闭SWAP的主动使用，只在内存彻底耗尽才会启用，对于本来内存就紧张的VPS，适度保留一点SWAP使用倾向反而更稳妥。

## SWAP不是内存不够的根本解法

如果加了SWAP之后发现它长期被占用大半，这其实是内存真的不够用了的信号，不是SWAP没配够。SWAP的读写速度跟物理内存差几个数量级，长期依赖SWAP运行，性能会明显下降，遇到这种情况该考虑升级内存套餐或者优化程序本身的内存占用，而不是一味把SWAP开得更大。

另外SWAP文件本身也占磁盘空间，如果这台VPS磁盘本来就紧张，加之前最好先看看[VPS磁盘空间满了怎么排查是什么占用的](https://vpsjq.com/2026/08/15/vps-disk-space-full/)，确认还有余量再操作；如果不想每次都手动敲这几条命令，[VPS一键系统管理](https://vpsjq.com/2025/11/25/vps%E4%B8%80%E9%94%AE%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%EF%BC%9A-bash/)这类脚本里通常也集成了添加SWAP的选项。
