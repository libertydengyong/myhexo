---
title: Termux备份和恢复环境的方法
date: 2026-08-29 14:00:00
tags:
  - Termux
categories:
  - vps技巧
description: Termux备份和恢复环境的完整方法，包括备份命令、备份文件存储位置和恢复步骤，适合换手机或者重装Termux时快速恢复环境。
---

Termux 装了一堆包、配置好了 SSH 密钥和各种工具之后，换手机或者重装 Termux 的时候从头来过非常麻烦。Termux 自带备份和恢复功能，把整个环境打包成一个文件，恢复的时候一条命令还原，不需要重新装包和配置。

备份命令：

\`\`\`bash
termux-backup ~/storage/shared/termux-backup.tar.gz
\`\`\`

这条命令会把 Termux 的 home 目录和已安装的包打包成一个 tar.gz 文件，保存到手机的公共存储目录里（也就是文件管理器里能看到的位置）。备份文件可能比较大，取决于你安装了多少包和 home 目录里有多少文件，几百 MB 到几 GB 都有可能，备份之前确认一下手机存储空间够不够。

备份文件存在手机本地存储，可以在文件管理器里找到 `termux-backup.tar.gz` 这个文件。如果担心手机丢失或者损坏导致备份也一起丢失，可以把这个文件上传到云盘（Google Drive、百度网盘等都行），异地备份更安全。备份文件包含了你的 SSH 私钥、配置文件和所有安装的包，属于敏感文件，上传云盘的时候注意不要上传到公开分享的目录里。

恢复备份的命令：

\`\`\`bash
termux-restore ~/storage/shared/termux-backup.tar.gz
\`\`\`

恢复之前需要先给 Termux 申请存储权限（如果是新安装的 Termux），跑一下：

\`\`\`bash
termux-setup-storage
\`\`\`

申请完权限之后再跑恢复命令。恢复过程会把备份文件里的内容覆盖到当前 Termux 环境，恢复完之后重启 Termux，之前安装的包和配置基本都会恢复回来。

备份建议定期做，尤其是在做了比较大的改动之后——比如装了新的工具、改了 SSH 配置、或者添加了新的 VPS 连接信息。如果你平时用 Termux 管理 VPS，SSH 密钥和连接配置都在里面，一旦丢失重新配置比较麻烦，定期备份能省不少事。具体怎么用 Termux 管理 VPS 可以参考[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)，SSH 断线问题可以参考[Termux SSH连接VPS断线怎么办](https://vpsjq.com/2026/08/03/termux-ssh-disconnect/)。
