---
title: 定期自动清理vps
tags:
  - 定期自动清理vps
id: '171'
categories:
  - - vps技巧
date: 2025-11-07 19:06:37
---

步骤一：创建脚本文件： nano /usr/local/bin/clean\_vps.sh 粘贴以下内容： #!/bin/bash docker system prune -af apt clean rm -rf /var/log/\*.gz /var/log/\*.1 /tmp/\* 保存并退出（按Ctrl+O →回车→ Ctrl+X） 赋予执行权限： chmod +x /usr/local/bin/clean\_vps.sh   步骤二：添加定时任务 运行命令默认设置编辑器为nano： export VISUAL=nano 运行crontab -e 在文件末添加 0 3 \* \* \* /usr/local/bin/clean\_vps.sh >/dev/null 2>&1   意为每天清理