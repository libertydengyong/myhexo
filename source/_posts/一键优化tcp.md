---
title: 一键优化TCP
tags:
  - 优化TCP
  - BBR
  - BBRplus
description: VPS 一键优化 TCP、开启 BBR、BBRplus、Alpine Linux 开启 BBR 等常见网络优化方法整理，提高服务器网络传输效率与访问体验。
id: '58'
categories:
  - vps优化
abbrlink: 50945
date: 2025-05-14 10:10:41
---
很多 VPS 刚开通时都保持默认网络参数，对于建站、代理服务、远程连接来说，默认配置虽然可以正常使用，但并不能发挥服务器的全部性能。

如果希望减少网络延迟、提高 TCP 传输效率，一般都会对服务器进行一些基础优化，例如开启 BBR、调整 TCP 参数、优化系统网络栈等。

<!-- more -->

不同 Linux 系统支持的优化方式有所不同。

Debian、Ubuntu、CentOS 大多数情况下可以直接开启官方 BBR，而部分老内核或者特殊环境则会选择 BBRplus、BBR 魔改版等方案。

如果不知道不同加速方式之间有什么区别，可以先参考之前整理过的文章：

[BBRplus与其他加速方式安装](https://freedomgpt.top/2025/05/06/bbrplus%E4%B8%8E%E5%85%B6%E4%BB%96%E5%8A%A0%E9%80%9F%E6%96%B9%E5%BC%8F%E5%AE%89%E8%A3%85/?highlight=bbr)

里面介绍了官方 BBR、BBRplus 等多种网络加速方式的安装方法以及适用场景，可以根据服务器内核选择合适的方案。

很多一键 TCP 优化脚本通常会完成下面几项配置：

- 开启 BBR 或 BBRplus；
- 调整 TCP 缓冲区大小；
- 开启 TCP Fast Open；
- 优化队列算法（fq、fq_codel 等）；
- 调整网络连接参数；
- 提高大量连接情况下的稳定性。

这些优化虽然不会让带宽变大，但可以改善高延迟线路上的传输效率，尤其对于海外 VPS 会有一定帮助。

如果服务器本身线路较差，再好的 TCP 参数也无法完全解决网络质量问题，因此线路质量仍然是影响速度的重要因素，推荐一个一键优化TCP，代码:

wget https://github.com/BlueSkyWithWhiteClouds/Optimize-Tcp-Cache/releases/download/v1.0/Optimize\_Tcp\_Cache.sh ; chmod +x Optimize_Tcp_Cache.sh ; ./Optimize_Tcp_Cache.sh


不少用户使用 Alpine Linux 部署代理服务或者 Docker，由于 Alpine 默认配置与 Debian 有一些区别，开启 BBR 的方法也有所不同。

如果服务器运行的是 Alpine，可以参考：

[Alpine 开启bbr](https://freedomgpt.top/2025/07/12/alpine-%E5%BC%80%E5%90%AFbbr/?highlight=bbr)

文章中介绍了不同 Linux 系统支持的优化方式有所不同。

Debian、Ubuntu、CentOS 大多数情况下可以直接开启官方 BBR，而部分老内核或者特殊环境则会选择 BBRplus、BBR 魔改版等方案。

如果不知道不同加速方式之间有什么区别，可以先参考之前整理过的文章：

[BBRplus与其他加速方式安装](https://freedomgpt.top/2025/05/06/bbrplus%E4%B8%8E%E5%85%B6%E4%BB%96%E5%8A%A0%E9%80%9F%E6%96%B9%E5%BC%8F%E5%AE%89%E8%A3%85/?highlight=bbr)

里面介绍了官方 BBR、BBRplus 等多种网络加速方式的安装方法以及适用场景，可以根据服务器内核选择合适的方案。

很多一键 TCP 优化脚本通常会完成下面几项配置：

- 开启 BBR 或 BBRplus；
- 调整 TCP 缓冲区大小；
- 开启 TCP Fast Open；
- 优化队列算法（fq、fq_codel 等）；
- 调整网络连接参数；
- 提高大量连接情况下的稳定性。

这些优化虽然不会让带宽变大，但可以改善高延迟线路上的传输效率，尤其对于海外 VPS 会有一定帮助。

如果服务器本身线路较差，再好的 TCP 参数也无法完全解决网络质量问题，因此线路质量仍然是影响速度的重要因素，推荐一个一键优化TCP，代码:

wget https://github.com/BlueSkyWithWhiteClouds/Optimize-Tcp-Cache/releases/download/v1.0/Optimize\_Tcp\_Cache.sh ; chmod +x Optimize_Tcp_Cache.sh ; ./Optimize_Tcp_Cache.sh


不少用户使用 Alpine Linux 部署代理服务或者 Docker，由于 Alpine 默认配置与 Debian 有一些区别，开启 BBR 的方法也有所不同。

如果服务器运行的是 Alpine，可以参考：

[Alpine 开启bbr](https://freedomgpt.top/2025/07/12/alpine-%E5%BC%80%E5%90%AFbbr/?highlight=bbr)

文章中介绍了 Alpine 系统开启 BBR 的步骤以及需要注意的地方。

进行 TCP 优化之前，建议先确认当前内核是否支持相关功能，例如：

```bash
uname -r
```

查看当前拥塞算法：

```bash
sysctl net.ipv4.tcp_congestion_control
```

查看当前队列算法：

```bash
sysctl net.core.default_qdisc
```

如果已经显示：

```text
bbr
```

说明服务器已经开启了官方 BBR。

完成优化之后，还可以通过下载测速、大文件传输、延迟测试等方式，对比优化前后的网络表现。

需要注意的是，并不是所有 VPS 都适合使用第三方内核或者魔改 BBR。如果服务器主要用于生产环境，优先建议使用官方内核提供的 BBR，在兼容性和稳定性方面通常更有保障。

对于个人建站、小型代理服务以及远程管理来说，一键优化 TCP 配合合适的网络线路，一般已经能够满足日常使用需求。
```
<br>
<br>
<br>
相关内容
[**TCP 迷之调参**](https://freedomgpt.top/2025/05/14/tcp-%E8%BF%B7%E4%B9%8B%E8%B0%83%E5%8F%82/)

[**Linux TCP/IP 和 BBR 参数智能优化脚本**](https://freedomgpt.top/2025/11/30/linux-tcp-ip-%E5%92%8C-bbr-%E5%8F%82%E6%95%B0%E6%99%BA%E8%83%BD%E4%BC%98%E5%8C%96%E8%84%9A%E6%9C%AC/?highlight=%E4%BC%98%E5%8C%96)
