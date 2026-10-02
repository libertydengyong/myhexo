---
title: "Hysteria2怎么用Docker部署？官方compose示例逐行讲解和三个坑"
date: 2026-10-02 18:00:00
tags:
  - Hysteria2
  - Docker
categories:
  - vps工具
description: "Hysteria2官方安装文档里有Docker镜像和compose示例。这篇逐行解释host网络、NET_ADMIN、acme卷这几处写法的含义，给出完整部署和日志、升级命令，并说明固定版本号、文件挂载、端口跳跃这三个容易踩的坑。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2怎么用Docker部署？官方compose示例逐行讲解和三个坑",
      "description": "Hysteria2官方安装文档里有Docker镜像和compose示例。这篇逐行解释host网络、NET_ADMIN、acme卷这几处写法的含义，给出完整部署和日志、升级命令，并说明固定版本号、文件挂载、端口跳跃这三个容易踩的坑。",
      "datePublished": "2026-10-02T18:00:00+08:00",
      "dateModified": "2026-10-02T18:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-docker/",
      "author": {
        "@type": "Organization",
        "name": "vpsjq.com"
      },
      "publisher": {
        "@type": "Organization",
        "name": "vpsjq.com"
      }
    },
    {
      "@type": "HowTo",
      "name": "用Docker Compose部署Hysteria2服务端",
      "step": [
        {
          "@type": "HowToStep",
          "name": "准备目录和hysteria.yaml",
          "text": "新建一个目录，在里面写好hysteria.yaml服务端配置，至少包含acme或tls证书部分和auth认证部分。"
        },
        {
          "@type": "HowToStep",
          "name": "写docker-compose.yml",
          "text": "使用官方示例：镜像tobyxdd/hysteria，network_mode设为host，把hysteria.yaml挂载到容器的/etc/hysteria.yaml，命令为server -c /etc/hysteria.yaml。"
        },
        {
          "@type": "HowToStep",
          "name": "放行UDP端口并启动",
          "text": "因为用的是host网络，没有端口映射，要在系统防火墙和服务商安全组放行配置端口的UDP，然后执行docker compose up -d启动。"
        },
        {
          "@type": "HowToStep",
          "name": "查看日志确认运行",
          "text": "执行docker compose logs -f hysteria查看日志，确认证书申请和监听都没有报错，再用客户端连接测试。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2官方有Docker镜像吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "有。官方安装文档在Docker部分给出的镜像是Docker Hub上的tobyxdd/hysteria，并提供了docker compose示例：使用host网络，挂载配置文件和一个acme卷，命令是server -c /etc/hysteria.yaml。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2的Docker部署为什么要用host网络？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方示例用的就是network_mode: host。Hysteria2跑在UDP上，host网络让容器直接使用宿主机的网络，不需要写端口映射，端口跳跃时也不需要额外处理映射。代价是容器和宿主机共用网络，端口冲突要自己留意。"
          }
        },
        {
          "@type": "Question",
          "name": "Docker部署的Hysteria2什么时候需要NET_ADMIN权限？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方文档写明，NET_ADMIN权限只在启用端口跳跃时才需要。不用端口跳跃的话，可以把这一项去掉。"
          }
        }
      ]
    }
  ]
}
</script>

之前写 Hysteria2 的时候，我一直说 Docker 部署"没有查到官方依据"，所以没有写。这次重新核对官方的安装文档，**发现它在 Docker 部分是有内容的**：给出了镜像地址，还附了一个 docker compose 示例。上一次是我查得不够，这里更正。这篇就围绕官方的这个示例来讲，每一行是什么意思、容易踩什么坑。

先说一个前提：这里讲的是**服务端**的 Docker 部署。如果你更习惯用官方脚本，直接看[一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)；服务器上没有装 Docker 的话，Docker 本身的安装不在这篇范围内。

## 官方给的 compose 示例

官方文档的原文是这样的：

```yaml
version: "3.9"
services:
  hysteria:
    image: tobyxdd/hysteria
    container_name: hysteria
    restart: always
    network_mode: "host"
    cap_add:
      - NET_ADMIN
    volumes:
      - acme:/acme
      - ./hysteria.yaml:/etc/hysteria.yaml
    command: ["server", "-c", "/etc/hysteria.yaml"]
volumes:
  acme:
```

镜像是 Docker Hub 上的 `tobyxdd/hysteria`。下面逐处解释。

### network_mode: "host"

容器直接用宿主机的网络，**不需要写 `ports:` 做端口映射**。Hysteria2 跑在 UDP 上，用 host 模式省掉了映射 UDP 端口这一步，也避免了端口跳跃时映射一大段端口的麻烦。官方示例就是这么写的。

代价是容器和宿主机共用网络，宿主机上如果已经有程序占着 UDP 443（比如你之前用官方脚本装过一个），容器会起不来，这点要先排查。

### cap_add: NET_ADMIN

官方在示例下面特别写了一句：**这个权限只在启用端口跳跃时才需要**。原因是端口跳跃要在系统里设置防火墙转发规则，需要这个能力。我看了官方仓库里的 Dockerfile，镜像里确实装了 `iptables` 和 `nftables`，也和这个说法对得上。

所以：不用端口跳跃的话，可以把 `cap_add` 这两行删掉，权限给得越少越稳妥；要用端口跳跃就保留，具体配法见[端口跳跃配置](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)。

### volumes：两个挂载

- `./hysteria.yaml:/etc/hysteria.yaml`：把当前目录下的配置文件挂进容器，容器里用的就是它。
- `acme:/acme`：一个 Docker 命名卷，用来保存 ACME 申请到的证书。底部的 `volumes: acme:` 就是在声明这个卷。

为什么是 `/acme`？我查了官方源码：配置里 `acme.dir` 不写的时候，默认用的目录名是 `acme`，是相对路径；镜像的 Dockerfile 里没有设置工作目录，所以相对路径落在根目录下，也就是 `/acme`。这是我对照源码的推断，**官方文档里没有明确写这一点**，但解释了为什么示例要挂这个路径。这个卷的作用是：容器删了重建，证书不用重新申请，避免触发证书机构的频率限制。

### command

`["server", "-c", "/etc/hysteria.yaml"]`：以服务端模式运行，配置文件指向挂载进去的那个。镜像的入口是 `hysteria`，所以这里只写子命令和参数。

## 完整部署步骤

### 第一步：准备目录和配置文件

```bash
mkdir -p /opt/hysteria && cd /opt/hysteria
nano hysteria.yaml
```

配置内容用官方的最小示例，带域名自动申请证书的写法：

```yaml
acme:
  domains:
    - your.domain.net
  email: your@email.com
auth:
  type: password
  password: 换成你自己的强密码
masquerade:
  type: proxy
  proxy:
    url: https://news.ycombinator.com/
    rewriteHost: true
```

这些字段的含义、`acme` 和 `tls` 怎么选，在[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)里讲过。注意域名要先解析到这台服务器，ACME 默认用 HTTP 验证，会用到 80 端口，这段时间别让别的程序占着。

### 第二步：写 docker-compose.yml

把上面官方示例原样存成 `docker-compose.yml`。不用端口跳跃，就删掉 `cap_add` 两行。

### 第三步：放行端口，启动

因为是 host 网络，没有端口映射，防火墙要直接放行**宿主机**上的端口：

```bash
ufw allow 443/udp
ufw allow 80/tcp
```

服务商的安全组里也要放行：UDP 443 给连接用，TCP 80 给证书验证用（用 HTTP 验证时）。然后启动：

```bash
docker compose up -d
```

### 第四步：看日志确认

```bash
docker compose logs -f hysteria
```

日志里能看到证书申请和监听的情况，没有报错，再用客户端去连。连不上的话，按[timeout 报错排查](https://vpsjq.com/2026/10/02/hysteria2-timeout-no-recent-network-activity/)逐条对照，Docker 部署和脚本部署在这方面的原因是一样的。

## 三个容易踩的坑

### 坑 1：不写版本号，升级时可能"自己变了"

示例里的 `image: tobyxdd/hysteria` 没有写标签，等于 `latest`。我查了 Docker Hub，目前有 `latest`、`v2` 和具体的版本号标签，比如 `v2.12.3`。官方文档没有说明该用哪个标签，我的建议是：**想稳定就写死具体版本号**，升级时自己改，这样每次升级都是你主动决定的。写成 `tobyxdd/hysteria:v2.12.3` 这样。具体用哪个版本，以 Docker Hub 上的标签为准。

### 坑 2：`./hysteria.yaml` 文件不存在，Docker 会建成目录

这是 Docker 挂载文件的一个常见现象：如果宿主机上 `hysteria.yaml` 这个路径不存在，Docker 会把它创建成一个**同名目录**，容器里就会因为读不了配置而起不来。这个行为不是 Hysteria 特有的，也不在官方文档里，我是按 Docker 的通用表现提醒的。所以**先写好配置文件，再启动**；万一已经出现了同名目录，删掉目录，建好文件，重新启动。

### 坑 3：端口跳跃要 NET_ADMIN，还得放行整段端口

用了端口跳跃，`cap_add: NET_ADMIN` 必须保留，否则容器里没有权限去设置规则；同时系统防火墙和服务商安全组都要放行**整段** UDP 端口，只放第一个会表现为用一会儿就断。

## 日常管理命令

下面这些是 Docker Compose 的通用命令，不是 Hysteria 特有的：

```bash
docker compose logs -f hysteria     # 看日志
docker compose restart hysteria     # 改了配置后重启
docker compose pull && docker compose up -d   # 拉新镜像并重建
docker compose down                 # 停止并删除容器
```

`docker compose down` 默认**不会**删除命名卷，所以 `acme` 卷里的证书会保留；加了 `-v` 才会连卷一起删，不想重新申请证书的话别加。升级前建议备份一下 `hysteria.yaml` 和证书卷。

另外，官方示例开头的 `version: "3.9"`，在较新的 Compose 版本里可能提示这个字段已经过时，那只是个警告，不影响运行，可以删掉这一行。这是 Compose 的通用表现，不是官方文档里的说明。

## Docker 和官方脚本怎么选

| | 官方脚本 | Docker |
|---|---|---|
| 安装方式 | 一条命令，装成 systemd 服务 | 要先有 Docker，写 compose 文件 |
| 升级 | 重新运行脚本，见[升级和卸载](https://vpsjq.com/2026/10/02/hysteria2-upgrade-uninstall/) | 拉新镜像并重建 |
| 隔离性 | 直接装在系统里 | 在容器里，卸载干净 |
| 适合 | 只跑 Hysteria2 的小鸡 | 本来就用 Docker 管理多个服务 |

服务器上已经有一堆 Docker 服务，习惯统一管理的，用 Docker 方便；只是单独跑一个 Hysteria2，官方脚本更省事。我这台机器上没有安装 Docker，所以**这篇里的 compose 内容来自官方文档，我没有在实机上跑过一遍**，命令都是常规用法，遇到差异以官方文档为准。

## 没有覆盖的

- 客户端用 Docker 运行：官方文档里没有看到专门的说明，镜像里应该也带有客户端模式，但我没有核对具体用法，所以不写。
- 群晖、威联通等 NAS 的 Docker 界面操作：每个系统的界面不同，我没有核对，不写。
