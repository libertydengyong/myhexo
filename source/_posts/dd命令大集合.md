---
title: dd命令大集合
tags:
  - dd命令
id: '49'
categories:
  - Linux优化
abbrlink: 64275
date: 2025-05-11 19:41:02
description: VPS用dd方式重装Windows系统的常用命令合集，基于InstallNET.sh脚本，覆盖Windows Server和桌面版多个版本。
---

https://gist.github.com/barkpixels/da77865ac6f59b24f567912939ab82b0

VPS圈子里说的"DD重装系统"，指的是用 `dd` 命令把一份完整的系统镜像直接写入硬盘，跳过传统的图形化安装向导，几分钟就能把一台Linux VPS换成Windows系统（或者反过来），比用服务商自带的重装面板灵活很多，尤其适合服务商没有提供你想要的系统版本的情况。

上面这个链接里收集的是基于 `InstallNET.sh` 这个通用DD脚本的具体命令，涵盖了Windows Server 2008到2022各个版本，以及Windows 7/8.1/10的精简版和完整版镜像，部分系统还附带了对应的KMS激活密钥参考。

## 使用前必须知道的事

- **会清空硬盘上的所有数据**：DD是把镜像直接写入磁盘，执行前VPS上原有的所有数据都会被覆盖，操作前务必确认没有需要保留的东西
- **确认服务商允许DD操作**：不是所有VPS服务商都支持DD重装，部分厂商的KVM/Xen虚拟化方案下这类操作可能导致系统无法启动，操作前最好先查一下自己用的服务商社区里有没有人验证过
- **境外服务器谨慎DD国内镜像源**：链接里的镜像托管在 `oss.sunpma.com`，网络环境不同下载速度可能有差异，如果卡住很久没有进度，可以考虑换其他线路或者镜像源

## 基本命令格式

以DD Windows Server 2022为例：

```bash
wget --no-check-certificate -qO InstallNET.sh 'https://moeclub.org/attachment/LinuxShell/InstallNET.sh' && bash InstallNET.sh -dd '镜像地址.gz'
```

不同系统版本只是替换命令最后的镜像地址链接，具体版本对应的完整命令列表可以看上面的gist原文。云平台（比如Google Cloud）网络环境特殊，可能还需要额外指定 `--ip-addr`、`--ip-mask`、`--ip-gate` 这几个网络参数，具体写法gist里也有对应示例。

执行DD命令之后，VPS会重启进入安装环境，整个过程一般需要几分钟到十几分钟不等，取决于VPS网络速度和镜像大小，安装完成后用面板提供的IP和默认账号密码登录即可。
