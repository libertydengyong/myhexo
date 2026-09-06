---
title: 3x-ui纯IPv6 VPS申请SSL证书失败：acme.sh --listen-v6解决方法
date: 2026-09-06 16:00:00
tags:
  - 3x-ui教程
  - IPv6
  - SSL证书
categories:
  - vps技巧
description: 纯IPv6环境下用3x-ui面板申请证书一直失败或超时的原因排查，acme.sh standalone模式默认只监听IPv4，需要手动加--listen-v6参数才能完成验证。
---
如果服务器是纯IPv6（没有IPv4地址），用3x-ui面板自带的证书申请功能经常会一直卡住或者直接报错超时，具体的证书配置入口可以先参考[3x-ui配置TLS证书教程](https://vpsjq.com/2026/08/27/3x-ui-tls/)，本篇专门讲纯IPv6环境下失败的原因和解决办法。
<!-- more -->
3x-ui面板申请证书这个功能，底层调用的是acme.sh，走的是standalone模式验证。acme.sh的standalone模式有个默认行为：只监听IPv4地址，不会自动监听IPv6。纯IPv4或者双栈（IPv4+IPv6都有）的服务器不会遇到这个问题，因为总有IPv4地址可以监听；但纯IPv6服务器根本没有IPv4地址，acme.sh却还是只尝试监听IPv4，导致Let's Encrypt发起的验证请求根本连不上，证书申请自然失败。

判断是不是这个原因，先看服务器有没有配置IPv4地址：

```bash
ip -4 addr show
```

如果输出为空或者只有本地回环地址（127.0.0.1），说明确实是纯IPv6环境，大概率就是这个问题。

面板内置的申请入口通常不暴露`--listen-v6`这个参数，遇到这种情况需要绕开面板，手动用acme.sh命令行申请一次，再把证书路径填回面板。手动申请命令：

```bash
~/.acme.sh/acme.sh --issue --standalone --listen-v6 -d 你的域名
```

`--listen-v6`这个参数强制acme.sh监听IPv6地址，而不是默认的IPv4。申请成功后，acme.sh会把证书文件保存在`~/.acme.sh/你的域名/`这个目录下，把这个目录里的`fullchain.cer`和`你的域名.key`这两个文件路径，填到3x-ui面板设置里对应的证书路径和私钥路径字段，保存重启面板就能生效，具体填写位置可以参考前面提到的TLS配置教程。

如果加了`--listen-v6`还是不行，先确认acme.sh本身是不是最新版本，旧版本个别情况下这个参数不生效：

```bash
~/.acme.sh/acme.sh --upgrade
```

升级完再重新执行一次申请命令。另外申请前记得确认80端口本身没有被面板或者其它服务占用，纯IPv6环境下端口冲突的报错信息有时会跟"监听失败"混在一起，容易误判成同一个问题，可以用`netstat -tlnp | grep :80`先检查一下80端口有没有被占用。

这个问题只在纯IPv6服务器上出现，如果服务器是双栈的，直接用面板自带的申请功能就行，不需要走这套手动流程，纯IPv6节点的其它配置注意事项可以参考[IPv6 VPS配置3x-ui节点教程](https://vpsjq.com/2026/08/27/ipv6-vps-3xui-node/)。
