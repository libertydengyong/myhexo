---
title: alireza0/s-ui 是什么？官方仓库、Docker 安装与常用命令一览
date: 2026-09-06 21:50:00
updated: 2026-09-06 21:50:00
tags:
  - S-UI教程
  - Docker
  - 面板对比
categories:
  - vps技巧
description: alireza0/s-ui 是 S-UI 面板的官方原始仓库，这篇文章说清楚它和社区分叉版本的关系，并提供 Docker 部署方式和常用管理命令。
keywords: alireza0 s-ui,s-ui docker安装,s-ui命令,s-ui删库,s-ui官方仓库
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "alireza0/s-ui 是什么？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "alireza0/s-ui 是 S-UI 面板的官方原始 GitHub 仓库，作者是 Alireza Ahmadi，项目基于 SagerNet/Sing-Box 构建。目前市面上看到的各种 S-UI 教程和分发版本，绝大多数都是围绕这个官方仓库展开或者在其基础上做的二次分发。"
      }
    },
    {
      "@type": "Question",
      "name": "S-UI 支持 Docker 安装吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "支持，官方提供了 docker-compose 和 docker run 两种方式，镜像地址是 alireza7/s-ui，安装前需要先装好 Docker 环境。"
      }
    }
  ]
}
</script>

搜"alireza0 s-ui"这个词的人，通常是想确认一件事：**自己在教程里看到的 S-UI，到底是不是官方正版，装的时候该认准哪个仓库**。这篇文章把这个问题讲清楚，顺带把 Docker 安装方式和常用命令也一起补上。

## alireza0/s-ui 到底是什么

S-UI 这个项目的官方仓库地址是 `github.com/alireza0/s-ui`，作者是 Alireza Ahmadi，基于 SagerNet/Sing-Box 内核构建，目前仓库有接近一万的 star 数，仍在持续更新维护。之前几篇教程里用到的安装命令：

```bash
bash <(curl -Ls https://raw.githubusercontent.com/alireza0/s-ui/master/install.sh)
```

这条命令拉取的就是这个官方仓库的安装脚本，认准这个域名路径基本不会装错。

## 和 X-UI、3X-UI 是什么关系

这个问题之前在 [S-UI 和 3x-ui 有什么区别](https://vpsjq.com/2026/09/06/s-ui-vs-3x-ui/) 里已经详细讲过，简单重复一句结论：**S-UI 和 X-UI/3X-UI 不是同一条家族线**，S-UI 是基于 sing-box 独立开发的项目，X-UI/3X-UI 是基于 Xray-core 那条分支，两者除了都叫"UI 面板"之外没有代码传承关系，不要混为一谈。

值得一提的是，S-UI 这边也开始出现社区分叉版本，比如有基于官方 v1.4.1 做增强开发的"Pro Panel"分支。这跟当年 X-UI 停更、社区分叉出 3X-UI 接手的路径有点像，但目前官方仓库本身还在正常更新，不必因为出现了分叉版本就觉得官方项目要"凉了"，两者可以并存，具体用哪个看你的需求（要稳定就跟官方主线，要抢先用某些增强功能可以看看分叉版本的具体更新内容）。

## Docker 安装方式

如果不想用脚本直接跑在宿主机上，官方也提供了 Docker 部署方式。

**第一步：安装 Docker**（如果还没装）

```bash
curl -fsSL https://get.docker.com | sh
```

**第二步：用 docker-compose 方式安装**

```bash
mkdir s-ui && cd s-ui
wget -q https://raw.githubusercontent.com/alireza0/s-ui/master/docker-compose.yml
docker compose up -d
```

**或者用 docker run 方式**

```bash
mkdir s-ui && cd s-ui
docker run -itd \
    -p 2095:2095 -p 2096:2096 -p 443:443 -p 80:80 \
    -v $PWD/db/:/usr/local/s-ui/db/ \
    -v $PWD/cert/:/root/cert/ \
    --name s-ui --restart=unless-stopped \
    alireza7/s-ui:latest
```

两种方式效果一样，`docker-compose.yml` 方式更方便后续管理（改配置、重启都更直观），`docker run` 适合想一条命令搞定的场景。挂载出来的 `db/` 目录就是数据库文件所在位置，备份的时候记得把这个目录一起备份。

## 常用命令

**脚本安装方式**下，装完之后系统里会有一个 `s-ui` 命令可以直接调用，跟 3x-ui 的 `x-ui` 命令类似，用来打开管理菜单：

```bash
s-ui
```

具体菜单里有哪些选项（启动/停止/重启/查看日志/卸载等）以你安装时拉取到的脚本版本为准，进菜单看一遍就知道。

**卸载 S-UI**（脚本安装方式）：

```bash
sudo -i
systemctl disable s-ui --now
rm -f /etc/systemd/system/sing-box.service
systemctl daemon-reload
rm -fr /usr/local/s-ui
rm /usr/bin/s-ui
```

## 关于"删库"这件事

搜"S-UI 删库"的人，大概率是想解决账号密码忘记、或者想彻底清空配置重新搭建这两类需求。这里需要提醒：**删库等于清空所有已配置的入站、用户、订阅信息**，操作前务必先备份 `db/` 目录（脚本安装方式在 `/usr/local/s-ui/db/`，Docker 方式在你挂载出来的本地 `db/` 目录）。删库不是解决忘记密码的首选方案，只有在确实想推倒重来的时候才考虑，普通的密码找回应该优先看面板本身有没有更轻量的重置方式，而不是直接删数据库这种"杀鸡用牛刀"的做法。

如果这台机器上的 S-UI 还没搭起来，可以先参考 [S-UI面板搭建教程](https://vpsjq.com/2025/11/17/s-ui%E9%9D%A2%E6%9D%BF%E6%90%AD%E5%BB%BA/)，用脚本方式先跑起来，等熟悉了面板操作再考虑要不要换成 Docker 部署。
