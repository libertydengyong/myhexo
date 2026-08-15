---
title: VPS流量监控用什么工具
date: 2026-08-15 21:00:00
tags:
  - vnstat
categories:
  - vps工具
description: vnstat是Linux下常用的VPS流量监控工具，能统计每日每月流量使用情况，避免超出服务商的流量限额。
---

不少VPS套餐带月流量限制，超了轻则限速重则额外收费，但服务商自己的面板经常只给一个模糊的进度条，具体每天用了多少、哪天用得特别猛，压根查不到。vnstat能把这块补上，装一次之后随时能查详细的流量记录。

## 安装

```bash
apt-get install vnstat -y
```

CentOS系统用yum，如果提示找不到包，先装epel源：

```bash
yum install epel-release -y && yum install -y vnstat
```

## 找到要监控的网卡名字

```bash
ifconfig -a
```

如果系统没有`ifconfig`命令，装一下net-tools或者直接用`ip a`代替。常见的网卡名是`eth0`，也有些VPS是`ens5`这类名字，装完vnstat如果发现数据一直是空的，多半是网卡名没对上，改一下`/etc/vnstat.conf`里`Interface`后面的值就行。

## 查看流量数据

装好之后不用额外配置就能看：

```bash
vnstat -d
```

看每日流量明细。想看每月汇总：

```bash
vnstat -m
```

需要实时监控当前网速，用：

```bash
vnstat -l
```

## 让统计周期对上服务商的计费日期

vnstat默认按每月1号重新计算流量，但服务商的流量重置日不一定是1号，对不上的话月流量统计会跟服务商后台显示的对不上。改一下配置文件：

```bash
vim /etc/vnstat.conf
```

找到`MonthRotate`这一项，改成服务商实际的流量重置日期（比如服务商是每月15号重置，就填15）。

## 顺带一提

vnstat不需要root权限也能跑，因为它读的是`/proc`文件系统里的数据，不是直接抓网络包，所以对系统性能影响很小，常年挂着也不用担心占用太多资源。

## 想要接近实时的流量预警，还可以这样用

单纯查历史数据只能"事后知道超没超"，如果想在流量快用完之前提前收到提醒，可以写个简单的定时脚本，每天跑一次`vnstat -m`把当月流量读出来，跟服务商给的限额比较，超过某个百分比（比如80%）就发个通知（邮件、Telegram机器人都行）。这个思路配合vnstat已有的数据，不用额外抓包分析，实现起来比想象中简单，很多"流量预警脚本"本质上就是在做这件事。

如果这台VPS本身已经装了[VPS一键系统管理](https://vpsjq.com/2025/11/25/vps%E4%B8%80%E9%94%AE%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86%EF%BC%9A-bash/)那类脚本，流量监控功能可能已经集成在里面了，不用重复装vnstat；如果流量之外还想顺便看看这台VPS的带宽实际跑得怎么样，可以配合[VPS网络测速用什么工具最好](https://vpsjq.com/2026/08/15/vps-speedtest-tools/)一起用。
