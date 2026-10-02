---
title: "x-ui和3x-ui的配置文件在哪？数据库、xray的config.json、日志路径一次说清"
date: 2026-10-02 23:00:00
tags:
  - 3x-ui
  - x-ui
  - 配置文件
categories:
  - vps工具
description: "x-ui和3x-ui没有一个单独的配置文件：面板设置在/etc/x-ui/x-ui.db数据库里，xray的config.json是启动时自动生成的，直接改会被覆盖。这篇按3x-ui源码列出数据库、config.json、日志、环境变量文件的默认路径，并说明改哪里才有效。"
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "x-ui和3x-ui的配置文件在哪？数据库、xray的config.json、日志路径一次说清",
      "description": "x-ui和3x-ui没有一个单独的配置文件：面板设置在/etc/x-ui/x-ui.db数据库里，xray的config.json是启动时自动生成的，直接改会被覆盖。这篇按3x-ui源码列出数据库、config.json、日志、环境变量文件的默认路径，并说明改哪里才有效。",
      "datePublished": "2026-10-02T23:00:00+08:00",
      "dateModified": "2026-10-02T23:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/3x-ui-config-file-location/",
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
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "3x-ui的配置文件在哪里？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "没有单独的面板配置文件。按3x-ui源码，面板设置和节点数据都在SQLite数据库里，默认路径是/etc/x-ui/x-ui.db；xray内核用的config.json在安装目录的bin文件夹里，默认是/usr/local/x-ui/bin/config.json。"
          }
        },
        {
          "@type": "Question",
          "name": "可以直接编辑xray的config.json吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不建议。源码里每次启动xray之前都会把config.json重新写出来，直接改的内容会被覆盖。想改xray配置，在面板的Xray相关设置页里改，那里改的是数据库里保存的模板。"
          }
        },
        {
          "@type": "Question",
          "name": "3x-ui的日志文件在哪？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "源码里默认的日志目录是/var/log/x-ui，可以用环境变量XUI_LOG_FOLDER改。面板自身的日志用journalctl -u x-ui查看。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么备份x-ui的配置？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "核心是备份/etc/x-ui/x-ui.db这个数据库文件。迁移和还原的步骤见3x-ui备份和迁移那篇。"
          }
        }
      ]
    }
  ]
}
</script>

搜"x-ui 配置文件"的人，多半想找一个像 Nginx 的 `nginx.conf` 那样的文件，改完重启就生效。x-ui 和 3x-ui **没有这样的文件**。这篇把几个"看起来像配置文件"的位置分清楚：哪个是真正存设置的，哪个是自动生成的、改了没用，哪个只是日志。

依据说明：路径来自我读 3x-ui（MHSanaei 版）当前主分支的源码、`x-ui.sh` 和 systemd 服务文件，**没有在多个系统上逐一登录核对**。老版本（比如 2.9.4）、原版 x-ui（vaxilu）以及 Docker 部署，路径可能不同，这几种我没有核对。

## 一览表

| 内容 | 默认路径 | 能不能直接改 |
|---|---|---|
| 面板设置、用户、节点（入站）数据 | `/etc/x-ui/x-ui.db` | 不要手改，用面板或命令改 |
| xray 实际运行的配置 | `/usr/local/x-ui/bin/config.json` | 可以看，改了会被覆盖 |
| 面板程序和 xray 内核 | `/usr/local/x-ui/` | 不是配置 |
| 日志目录 | `/var/log/x-ui/` | 只读 |
| 服务的环境变量文件 | `/etc/default/x-ui`（Debian/Ubuntu 一类） | 可以建、可以改 |
| systemd 服务文件 | `/etc/systemd/system/x-ui.service` | 一般不用动 |

## 1. 数据库：真正存设置的地方

源码里数据库目录默认是 `/etc/x-ui`，文件名是 `x-ui.db`，也就是 `/etc/x-ui/x-ui.db`。这是 SQLite 数据库，面板的端口、账号、访问路径、证书路径，以及你建的所有入站和用户，都存在这里。**备份、迁移、还原，动的就是这一个文件**，步骤见[面板备份和迁移](https://vpsjq.com/2026/08/27/3x-ui-backup-migrate/)。

几点要注意：

- 数据库目录可以用环境变量 `XUI_DB_FOLDER` 改掉。有人改过的话，上面的路径就不对了。
- 新版本还支持 PostgreSQL：环境变量里设 `XUI_DB_TYPE` 和 `XUI_DB_DSN` 之后，数据不再在这个 SQLite 文件里。`x-ui.sh` 里显示数据库信息的地方写的也是默认的 SQLite 路径。我没有试过 PostgreSQL 模式，不展开。
- **不要用文本编辑器打开改**，它是二进制数据库。要改端口、密码这类设置，用面板界面，或者命令：`/usr/local/x-ui/x-ui setting ...`。端口和路径怎么查，见[常用命令](https://vpsjq.com/2026/08/30/3x-ui-commands/)；忘记密码见[重置方法](https://vpsjq.com/2026/09/06/3x-ui-forgot-password/)。
- 动数据库之前，先复制一份备份。

## 2. xray 的 config.json：自动生成，改了会被覆盖

xray 的配置文件路径来自源码：xray 目录默认是相对路径 `bin`（可用 `XUI_BIN_FOLDER` 改），而 systemd 服务文件里的工作目录是 `/usr/local/x-ui/`，所以实际是：

```
/usr/local/x-ui/bin/config.json
```

这个文件不是用来手改的。源码里每次启动 xray 之前，都会把当前配置序列化后**重新写入**这个文件（权限 600），之后用 `-c` 参数让 xray 读取。结论很直接：**你直接编辑它，下次面板重启 xray 时内容就被覆盖了**。

那 xray 的配置从哪来？由两部分拼出来：

- 面板里的**入站（节点）、用户**，存在数据库里；
- **Xray 配置模板**（路由、DNS、出站、日志等），源码里存在数据库的 `xrayTemplateConfig` 设置项中，初始值是程序内置的一个 `config.json` 模板。

想改路由规则、出站、日志级别这类内容，应该在面板里"Xray 相关设置"一类的页面改模板，改的是数据库里的值，重启后生效。具体菜单文字不同版本可能有差异，以你面板上的为准。

顺带，这里能看到源码内置模板的日志设置：`access` 是 `none`，`loglevel` 是 `warning`，也就是默认**不记录访问日志**。这是新装的默认值，你改过就不同了。

想只是看看 xray 现在实际用的配置，`cat /usr/local/x-ui/bin/config.json` 是可以的，只读不改。

## 3. 安装目录 /usr/local/x-ui/

`x-ui.sh` 里面板主目录默认是 `/usr/local/x-ui`，里面放面板的可执行文件、xray 内核（文件名形如 `xray-linux-amd64`）、`geoip.dat`、`geosite.dat` 等。这里是**程序文件**，不是配置。需要记住的只有：

- 管理命令 `x-ui` 本身是 `/usr/bin/x-ui`；
- 升级会替换这个目录，所以别把自己的东西放进去，见[升级和降级](https://vpsjq.com/2026/08/27/3x-ui-upgrade/)。

## 4. 日志

源码里日志目录默认是 `/var/log/x-ui`，可以用 `XUI_LOG_FOLDER` 改。里面能看到的内容，我从源码确认的有：IP 限制相关日志（`3xipl.log`、`3xipl-banned.log`）和 xray 崩溃时保存的崩溃报告文件。面板自己的运行日志，用 systemd 看：

```bash
journalctl -u x-ui -n 50 --no-pager
```

启动失败时怎么读它，见[面板启动失败怎么办](https://vpsjq.com/2026/10/02/xui-panel-start-failed/)。

## 5. 环境变量文件：改行为，不是改配置

服务文件里有一行 `EnvironmentFile=-/etc/default/x-ui`（前面的 `-` 表示文件不存在也不报错）。我对比了三份服务文件，**不同发行版家族路径不同**：

- Debian、Ubuntu 一类：`/etc/default/x-ui`
- RHEL 系（CentOS、Rocky 等）：`/etc/sysconfig/x-ui`
- Arch 系：`/etc/conf.d/x-ui`

这个文件默认不一定存在，需要时自己建。里面写 `KEY=value`，可以放的变量，我从源码确认的有：

| 变量 | 作用 |
|---|---|
| `XUI_DB_FOLDER` | 数据库目录 |
| `XUI_LOG_FOLDER` | 日志目录 |
| `XUI_BIN_FOLDER` | xray 内核目录 |
| `XUI_PORT` | 覆盖面板端口 |
| `XUI_LOG_LEVEL` / `XUI_DEBUG` | 日志级别、调试开关 |
| `XUI_DB_TYPE` / `XUI_DB_DSN` | 改用 PostgreSQL |

改完后重启服务：`systemctl restart x-ui`。**一般用户用不到这个文件**，只有在你想改目录、换数据库时才需要。

## 常见的几个问题

- **想改面板端口**：用面板设置，或 `/usr/local/x-ui/x-ui setting -port 新端口`，不是去改文件。
- **想改访问路径、账号密码**：同上，数据在数据库里。
- **想改证书路径**：在面板设置里填证书文件路径，配置方法见[TLS 证书配置](https://vpsjq.com/2026/08/30/3x-ui-tls/)。
- **想整体搬家**：备份 `/etc/x-ui/x-ui.db`，在新机器装好面板后还原，见[备份和迁移](https://vpsjq.com/2026/08/27/3x-ui-backup-migrate/)。
- **想自己写一份完整 xray 配置**：改模板，别改 `config.json`。

## 没有覆盖的

- **Docker 部署的路径**：脚本里 Docker 环境用的主目录和这里不同，我没有核对容器里的实际挂载方式，不写。
- **原版 x-ui（vaxilu）和其他分叉版**：没有核对。
- **模板在面板里的具体菜单位置和字段**：不同版本界面有变化，我没有逐版本核对。
- **Windows 版**：源码里有不同的默认路径，这里只讲 Linux。
