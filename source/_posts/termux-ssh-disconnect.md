---
title: Termux SSH连接VPS断线怎么办
date: 2026-08-03 10:00:00
tags:
  - Termux
categories:
  - vps技巧
description: 手机Termux用SSH连VPS总是断线的原因和解决办法，包括网络切换导致断连和长时间无操作自动断开这两种最常见的情况。
---

用手机连VPS，最烦的就是敲着敲着命令突然掉线，尤其是走在路上或者信号不太好的地方，WiFi和移动数据一切换连接就断了。这篇整理一下Termux里SSH断线的两种常见原因和对应的解决办法。

<img src="/images/ssh-vs-mosh.svg" alt="手机终端界面对比：普通SSH网络切换后连接断开需要重新登录，Mosh网络切换后会话自动恢复命令继续执行" width="700" height="748" loading="lazy">

同样是网络切换这一下，普通SSH直接断线重来，Mosh这边命令、光标全都还在原地——之前写过[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)，里面提到过用Mosh代替SSH能缓解这个问题，这篇展开说说具体是怎么回事、还有哪些别的办法。

## 网络切换导致断线

手机在WiFi和移动数据之间切换的时候，IP地址会变，原来那条SSH连接建立在旧IP上，网络一换连接自然就断了。这跟VPS那边没关系，纯粹是手机这一侧网络环境变化导致的。

普通SSH对这种情况没什么好办法，连接一断就得重新登录，之前敲了一半的命令也没了。真正解决这个问题得换工具——用Mosh代替SSH：

```bash
pkg install mosh
```

VPS那边也要装：

```bash
apt install mosh
```

之后连接方式：

```bash
mosh root@你的VPS的IP地址
```

Mosh的原理是它不像SSH那样依赖一条持续的TCP连接，而是用UDP维护会话状态，网络环境变了（比如IP换了），只要能重新连上，会话会自动恢复，之前没敲完的命令、光标位置都还在，不用重新登录。

如果VPS的防火墙比较严格，记得给Mosh用的UDP端口范围（默认60000-61000）放行，不然连不上：

```bash
ufw allow 60000:61000/udp
```

## 长时间不操作自动断开

这种断线跟网络切换没关系，是SSH本身的机制——连接空闲太久，中间的路由器/防火墙会把这条连接当成"死连接"清理掉，或者SSH服务端配置了超时自动断开。

解决办法是让SSH定期发送一个"心跳包"，告诉中间设备这条连接还活着。在Termux这边配置：

```bash
cat >> ~/.ssh/config << 'EOF'
Host *
  ServerAliveInterval 60
  ServerAliveCountMax 3
EOF
```

这样设置之后，每60秒会自动发一次心跳，连续3次没收到服务器响应才会真正判定断线，一般家里/公司网络这样配置就能解决大部分空闲断线的问题。

如果配置了心跳还是会断，问题可能出在VPS一侧的SSH服务端配置上，检查一下：

```bash
grep -i "clientalive" /etc/ssh/sshd_config
```

如果没有这两行，加上去再重启SSH服务：

```bash
ClientAliveInterval 60
ClientAliveCountMax 3
```

```bash
systemctl restart sshd
```

## 两种问题一起解决

日常用手机管理VPS，网络切换和空闲超时这两种断线经常混在一起遇到，比较省事的做法是**直接把Mosh当成默认连接方式**，配合上面的SSH心跳配置一起用——网络切换的时候靠Mosh自动恢复会话，长时间挂机不操作的时候靠心跳包保活，基本上就不会再遇到莫名其妙掉线的情况了。

如果断线之后发现连IPv6地址都连不上，那大概率不是这篇说的这两种情况，而是VPS本身的IPv6配置有问题，可以看这篇[IPv6 VPS服务无法访问的常见原因与排查方法](https://vpsjq.com/2026/07/22/2026-07-22-005/)，从DNS解析和防火墙规则那几个方向查起。
