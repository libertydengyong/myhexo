---
title: S-UI数据库备份和迁移到新服务器，命令不在菜单里
date: 2026-09-30 22:00:00
tags:
  - S-UI教程
  - 故障排查
categories:
  - vps技巧
description: S-UI其实自带一个专门的备份命令，但没有放进交互菜单里，容易被忽略；迁移到新服务器也没有单独的恢复命令，直接换文件就行。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "S-UI数据库备份和迁移到新服务器，命令不在菜单里",
      "description": "S-UI其实自带一个专门的备份命令，但没有放进交互菜单里，容易被忽略；迁移到新服务器也没有单独的恢复命令，直接换文件就行。",
      "datePublished": "2026-09-30T22:00:00+08:00",
      "dateModified": "2026-09-30T22:00:00+08:00",
      "url": "https://vpsjq.com/2026/09/30/s-ui-backup-migrate/",
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
      "name": "S-UI备份数据库并迁移到新服务器",
      "step": [
        {
          "@type": "HowToStep",
          "name": "在旧服务器执行备份命令",
          "text": "运行/usr/local/s-ui/sui backup -output 备份文件路径，导出一份完整的数据库备份文件。"
        },
        {
          "@type": "HowToStep",
          "name": "把备份文件传到新服务器",
          "text": "用scp把备份文件传到已经装好S-UI的新服务器上。"
        },
        {
          "@type": "HowToStep",
          "name": "停止服务替换数据库文件",
          "text": "systemctl stop s-ui停掉新服务器上的面板，用备份文件覆盖/usr/local/s-ui/db/s-ui.db，再systemctl start s-ui启动，版本不一致时会自动迁移数据库结构。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "S-UI的备份命令在管理菜单里吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不在。翻过官方脚本源码，backup这个功能确实存在，但s-ui交互菜单里没有把它列成一个编号选项，得直接敲命令行调用底层的sui二进制，命令是/usr/local/s-ui/sui backup -output 文件路径，不是在菜单里点出来的。"
          }
        },
        {
          "@type": "Question",
          "name": "备份的时候要不要先停止面板服务？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不需要。备份命令是通过程序自己的数据库连接读取数据再导出，不是直接复制正在被使用的数据库文件，面板可以照常运行。不过迁移到新服务器、要把备份文件放回去覆盖的时候，这一步必须先停止服务，不然文件被占用中途替换容易出问题。"
          }
        },
        {
          "@type": "Question",
          "name": "备份命令里的-exclude参数是做什么的？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "用来排除不想备份的数据表，官方支持的值是changes和stats，对应的是变更记录和流量统计这类历史数据。只想备份节点、用户这些真正的配置内容、不想把一堆历史流量记录也搬过去的话，可以加上-exclude changes,stats让备份文件更小更干净。"
          }
        }
      ]
    }
  ]
}
</script>

翻 S-UI 官方源码的时候发现一个容易被忽略的地方：它其实自带一个专门的数据库备份命令，功能完整，但**没有放进 `s-ui` 那个交互式管理菜单里**，光看菜单选项完全不会发现这东西存在，得直接敲命令行调用。

## 备份：直接敲命令，不在菜单里

在旧服务器上，SSH 进去直接执行：

```bash
/usr/local/s-ui/sui backup -output /root/s-ui-backup.db
```

会把当前的节点配置、用户信息这些数据导出成一个备份文件，存到指定路径。这个命令是通过程序自己的数据库连接读数据再导出的，不是直接复制正在使用中的文件，所以**备份的时候不需要先停止面板服务**，跑这条命令的时候面板照常运行不受影响。

如果不想把历史流量统计这类数据也一起备份进去，只保留节点和用户这些真正的配置，可以加上 `-exclude` 参数：

```bash
/usr/local/s-ui/sui backup -output /root/s-ui-backup.db -exclude changes,stats
```

`changes` 和 `stats` 对应的是变更记录和流量统计表，排除掉之后备份文件更小，内容也更纯粹。

## 迁移到新服务器：没有恢复命令，直接换文件

这里有个跟很多人预期不一样的地方：**S-UI 没有单独的"恢复"命令**，翻了一圈源码只有 backup，没有对应的 restore。实际迁移的做法是把备份文件直接当成数据库文件用：

1. 新服务器先按[S-UI面板搭建教程](/2025/11/17/s-ui面板搭建/)正常装好 S-UI，装完先别急着配置任何节点；
2. 把旧服务器导出的备份文件传到新服务器：

```bash
scp /root/s-ui-backup.db root@新服务器IP:/root/
```

3. 在新服务器上停掉面板服务，用备份文件覆盖掉默认的数据库文件，再重新启动：

```bash
systemctl stop s-ui
cp /root/s-ui-backup.db /usr/local/s-ui/db/s-ui.db
systemctl start s-ui
```

**停止服务这一步不能省**，数据库文件正在被占用的时候直接覆盖容易出问题，一定要先停服务再替换。

如果新旧服务器上 S-UI 的版本号不完全一致，不用太担心——程序自带数据库结构迁移的机制，启动的时候如果发现数据库版本跟当前程序版本对不上，会自动处理差异，不需要手动改数据库内容。当然还是建议两边尽量用同一个版本，能减少不必要的意外，升级和版本管理可以参考[S-UI升级到新版本](https://vpsjq.com/2026/09/30/s-ui-upgrade/)。

## 定期备份，别等出事才想起来

这个备份命令跑起来很轻量，值得写进 crontab 定期自动执行，比如每天备份一次到本地或者同步到别的地方存起来：

```bash
0 4 * * * /usr/local/s-ui/sui backup -output /root/s-ui-backup-$(date +\%Y\%m\%d).db -exclude changes,stats
```

配合定时清理超过一定天数的旧备份文件，就不用每次想起来才手动备份一次。忘记密码这类问题不需要靠数据库备份解决，直接看[S-UI忘记密码怎么办](https://vpsjq.com/2026/09/29/s-ui-forgot-password/)更快；备份主要是应对换服务器、系统重装、或者误操作把配置搞乱了想恢复到之前状态这几种场景。
