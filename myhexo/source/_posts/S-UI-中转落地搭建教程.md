---
title: S-UI 中转落地搭建教程
date: 2026-01-11 12:45:22
tags:
---


来源：nodeseek

https://www.nodeseek.com/post-471245-1

<!-- more --> 
##s-ui面板安装：

Linux/macOS 安装:

bash <(curl -Ls https://raw.githubusercontent.com/alireza0/s-ui/master/install.sh)



视窗安装:

从GitHub Releases下载最新的Windows版本

解压缩ZIP文件

install-windows.bat以管理员身份运行

按安装手册操作。



搭建中转落地

落地机

1·搭建S-UI面板



2·进入入站管理

入站类型选择 Shadowsocks ;监听端口自定比如设置 8081 方法随便选比如2022-blake3-aes-;网络TCP/UDP密码自动生成例如：y2z0EU8CQ/pjt18VH0kyrg==

保存后退出



中转机操作#中转机即高速节点



1·搭建S-UI面板



2·进入入站管理

入站类型选择Vless标签日澳Trans #建议这里中文标清楚以后节点名称就是显示的这个一个；监听端口可以按系统自己生成的；模版选择自己搭建之前的我没选现实选的另一个



3·出站管理

出站类型选择落地机相同的Shadowsocks标签自定义好区分的例如：Shadowsocks- AUS

服务器地址：落地机的IP端口 落地机刚才搭建入站的8081

方法：选择落地机一致的比如2022-blake3-aes-网络TCP/UDP

密码落地机生成的 y2z0EU8CQ/pjt18VH0kyrg==

保存



4·用户管理

新建用户取名简短如日澳翻译；入站标签选择刚才建的



5·路由列表

添加规则逻辑选上小白我这里选的“用户管理”选择第4项新建的用户日澳Trans

操作就选路线模式和

出站选项选择第4步建立的Shadowsocks- AUS

注意保存#以下方弹网络错误可无视直接刷新网页



6·到用户管理里

用户日澳Trans里把配置的节点地址丢到V2RayN里实​​现

打开google就是落地机的IP啦
