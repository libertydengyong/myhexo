---
title: 装了XanMod内核出问题，怎么卸载切回默认内核
date: 2026-08-27 10:00:00
tags:
  - XanMod回退
categories:
  - Linux优化
description: XanMod内核装完之后出现无法启动、网络异常这类问题，怎么安全切回原来的默认内核，以及为什么绝对不能急着把旧内核删掉。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "装了XanMod内核出问题，怎么卸载切回默认内核",
      "description": "XanMod内核装完之后出现无法启动、网络异常这类问题，怎么安全切回原来的默认内核，以及为什么绝对不能急着把旧内核删掉。",
      "datePublished": "2026-08-27T10:00:00+08:00",
      "dateModified": "2026-08-27T10:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/27/xanmod-uninstall-rollback/",
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
          "name": "XanMod出问题后能不能直接卸载旧内核重装？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "绝对不能。旧内核在确认新内核没问题之前必须保留，如果在没确认新内核能正常启动前就卸载了发行版自带的旧内核，一旦新内核有任何问题，机器会陷入无限重启循环，连救援模式都进不去，只能靠服务商VNC或救援系统从底层介入。"
          }
        },
        {
          "@type": "Question",
          "name": "怎么临时测试新内核而不影响正常使用？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "用grub-reboot做一次性的启动选择，先用grep menuentry查看grub.cfg里旧内核对应的条目名，执行grub-reboot加条目名再reboot，这次重启会用旧内核启动，之后的重启会恢复成GRUB默认设置，不会永久改变引导配置。"
          }
        },
        {
          "@type": "Question",
          "name": "确认新内核有问题，怎么永久切回旧内核？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "编辑/etc/default/grub，把GRUB_DEFAULT这一行改成旧内核对应的条目名，保存后执行update-grub再reboot。"
          }
        },
        {
          "@type": "Question",
          "name": "什么时候才能真正卸载XanMod？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "确认旧内核用着一切正常、不再需要XanMod之后才可以卸载，执行apt purge linux-xanmod-*，再update-grub和reboot，用uname -r确认当前跑的是默认内核。"
          }
        }
      ]
    }
  ]
}
</script>

之前写[XanMod内核从性能优化到实际使用](https://vpsjq.com/2026/07/28/2026-07-28-002/)那篇提过一句——**换了XanMod之后如果出现无法启动、网络异常、服务不稳定，需要及时恢复原来的内核**。这句话背后具体怎么操作，值得单独展开说清楚，因为这一步如果搞错顺序，后果比"内核换得不理想"严重得多。

## 黄金原则：旧内核在你确认新内核没问题之前，绝对不能删

这条规矩不是危言耸听。有真实的翻车案例——Debian 12上装XanMod 6.1 LTS版本，如果在还没确认新内核能正常启动之前，就把发行版原本自带的内核包卸载掉，一旦新内核这边有任何差池，机器会直接陷入**无限重启循环**，连救援模式都进不去，只能靠服务商的VNC/救援系统从底层介入才能挽救。装XanMod的正确顺序应该是：**装新内核、保留旧内核、先测试新内核能正常用，观察一段时间确认稳定了，再考虑要不要清理旧内核**，不能图省事一步到位。

## 临时切回旧内核测试（不删除任何东西）

如果新内核已经装上但还没重启验证过，想先小心翼翼地测试一下能不能正常启动新内核（同时留好后路），可以用`grub-reboot`只做**一次性**的启动选择，这次重启用了指定内核，之后恢复默认按原来的设置来：

```bash
grep menuentry /boot/grub/grub.cfg
```

先看一下这个列表，确认旧内核对应的条目名字，然后：

```bash
grub-reboot "对应旧内核的条目名"
reboot
```

这样重启这一次会用旧内核启动，验证完成之后系统之后的重启又会恢复成GRUB默认设置的那个内核，不会永久改变引导配置。

## 确认新内核彻底有问题，想永久切回旧内核

如果已经确认新内核有问题、决定长期用回旧内核，编辑GRUB配置，把默认启动项改成旧内核：

```bash
vi /etc/default/grub
```

找到`GRUB_DEFAULT`这一行，改成旧内核对应的条目名（跟上面`grep menuentry`看到的一致），保存后更新GRUB配置：

```bash
update-grub
reboot
```

## 真正想彻底卸载XanMod

确认旧内核用着一切正常、不再需要XanMod之后，才轮到卸载这一步：

```bash
apt purge linux-xanmod-*
update-grub
reboot
```

卸载完重启，用`uname -r`确认一下当前跑的确实是默认内核，不再是XanMod。

## 顺带一提

这套"先留后路、观察确认再清理"的思路，也适用于其他系统级配置改动——不管是换内核、调BBR参数（可以参考[XanMod内核配合BBR3的相关配置](https://vpsjq.com/2026/08/27/xanmod-bbr3/)）还是装代理面板，操作前先想清楚"万一不行怎么退回去"，比事后补救省心得多。如果是刚接触XanMod、还没决定要不要换，可以先看[一键更换为XanMod内核](https://vpsjq.com/2025/05/07/%E4%B8%80%E9%94%AE%E6%9B%B4%E6%8D%A2%E4%B8%BAxanmod%E5%86%85%E6%A0%B8/)那篇了解一下基础的安装方法，这篇算是给已经装了、遇到问题想退回去的人准备的后续操作指南。
