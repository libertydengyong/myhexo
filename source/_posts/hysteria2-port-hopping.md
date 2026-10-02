---
title: Hysteria2端口跳跃怎么配？官方脚本版：listen端口范围与客户端hopInterval
date: 2026-10-02 15:25:00
tags:
  - Hysteria2
  - 端口跳跃
categories:
  - vps工具
description: 用官方脚本装的Hysteria2做端口跳跃，服务端直接把listen写成端口范围就行，客户端地址写范围并设置hopInterval。这篇按官方文档讲清配置、手动iptables备选方案，以及端口跳跃什么情况下根本没用。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2端口跳跃怎么配？官方脚本版：listen端口范围与客户端hopInterval",
      "description": "用官方脚本装的Hysteria2做端口跳跃，服务端直接把listen写成端口范围就行，客户端地址写范围并设置hopInterval。这篇按官方文档讲清配置、手动iptables备选方案，以及端口跳跃什么情况下根本没用。",
      "datePublished": "2026-10-02T15:25:00+08:00",
      "dateModified": "2026-10-02T15:25:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-port-hopping/",
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
      "name": "配置Hysteria2端口跳跃",
      "step": [
        {
          "@type": "HowToStep",
          "name": "服务端listen写成端口范围",
          "text": "在/etc/hysteria/config.yaml里把listen改成端口范围，例如listen: :20000-50000，Linux上服务端会监听范围内第一个端口，并自动设置防火墙规则转发，需要系统装有nftables或iptables并有相应权限。"
        },
        {
          "@type": "HowToStep",
          "name": "放行整段UDP端口",
          "text": "系统防火墙和服务商安全组都要放行这一整段UDP端口范围，只放行单个端口，跳到其他端口时就会连不上。"
        },
        {
          "@type": "HowToStep",
          "name": "客户端地址写成端口范围",
          "text": "客户端server字段写成example.com:20000-50000，也支持用逗号分隔的单个端口和混合写法，再用hopInterval设置跳跃间隔。"
        },
        {
          "@type": "HowToStep",
          "name": "重启服务并测试",
          "text": "执行systemctl restart hysteria-server.service，客户端连接后正常使用一段时间，确认跳跃切换端口时连接不中断。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2端口跳跃对什么情况有用？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "官方文档说明，端口跳跃只在运营商针对某些特定UDP端口做限制时才有帮助，客户端会随机选一个端口发起连接，并定期切换到别的端口。如果运营商是对UDP流量整体限制，端口跳跃不会有帮助。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2端口跳跃的hopInterval怎么设置？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "客户端的hopInterval可以设为固定间隔，例如30s，官方说明最小值是5秒；也可以用minHopInterval和maxHopInterval设置随机间隔范围，两种方式只能用其中一种，不能同时设置。"
          }
        },
        {
          "@type": "Question",
          "name": "服务端不想用内置的端口范围监听，能手动转发吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以，用iptables的REDIRECT规则把一段UDP端口范围转发到Hysteria2实际监听的单个端口，IPv6需要用ip6tables再加一条对应规则，同样要在服务商安全组放行整段端口，并且要自己做规则持久化，否则重启后失效。"
          }
        }
      ]
    }
  ]
}
</script>

端口跳跃是针对一种很具体的情况：运营商或者防火墙对你用的某个 **UDP 端口**限速或者干扰，换个端口就好了，但换完一阵子又被盯上。让客户端在一整段端口里随机选、定期换，就不容易被卡在某一个端口上。

用面板的话，S-UI 里的做法可以看[S-UI 端口跳跃配置教程](https://vpsjq.com/2026/09/06/s-ui-port-hopping/)，那篇是手动用 iptables 转发。这篇讲的是**用官方脚本单独装的 Hysteria2**，官方服务端本身就内置了端口范围的支持，比手动写防火墙规则省事。服务端还没装好的话，先看[一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)和[config.yaml 最小配置](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)。

## 先确认值不值得配

官方文档说得很明确：端口跳跃**只在运营商针对特定端口限制时才有用**。如果是 UDP 整体被限速或者干扰，不管你跳到哪个端口都一样慢，配了也没效果。所以如果你的情况是"UDP 整体就慢"，应该先看[Hysteria2速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)里的排查顺序，不要上来就折腾端口跳跃。

官方还提到一点：端口跳跃和 Mimic（把 UDP 伪装成 TCP 的方案）不能同时用。

## 服务端：listen 直接写端口范围

Linux 上最简单的做法，是把配置里的 `listen` 从单个端口改成范围：

```yaml
listen: :20000-50000
```

官方说明里，这样服务端会监听范围内的第一个端口，并且**自动设置防火墙规则**，把范围内其他端口的流量转发过来。前提是系统里装有 `nftables` 或 `iptables`，并且服务有足够的权限去设置规则。官方脚本默认用 `hysteria` 这个普通用户跑服务，如果规则没生效，权限不够是可能的原因之一（官方文档没有专门说明，以日志里的报错为准），可以参考[一键安装脚本](https://vpsjq.com/2026/09/02/hysteria2-one-click/)里 `HYSTERIA_USER=root` 的说明。

改完之后重启：

```bash
systemctl restart hysteria-server.service
journalctl --no-pager -e -u hysteria-server.service
```

## 放行整段 UDP 端口

这一步最容易漏。系统防火墙和服务商安全组都要放行**整段**端口，不是只放行 `20000`：

```bash
ufw allow 20000:50000/udp
```

云服务商的安全组里同样加一条 UDP 的 `20000-50000` 入站规则。只放行第一个端口的话，客户端一跳到别的端口就连不上了，表现出来是用一会儿就断，很容易误判成线路不稳定。

## 客户端：地址写端口范围，设置跳跃间隔

客户端的 `server` 字段支持几种多端口写法：

```yaml
server: example.com:20000-50000          # 端口范围
# server: example.com:1234,5678,9012     # 几个单独的端口
# server: example.com:1234,5000-6000,7044  # 混合写法
auth: 你的密码
```

跳跃的间隔通过 `transport` 下的字段设置，默认是 30 秒，最小 5 秒：

```yaml
transport:
  udp:
    hopInterval: 30s
```

也可以不用固定间隔，改成随机范围，每次在两个值之间随机取一个：

```yaml
transport:
  udp:
    minHopInterval: 15s
    maxHopInterval: 45s
```

固定间隔和随机范围**只能二选一**，不要同时写。使用图形客户端的话，一般是在端口那一栏直接填范围，间隔如果有对应选项就按需要设置，没有的话保持客户端默认值也能用。分享链接里端口位置也支持这种多端口写法，细节可以看[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)那篇里的参数表。

## 不想用内置功能：手动 iptables 转发

内置的端口范围监听依赖服务端自己去设置防火墙规则，如果你的系统环境不适合，或者想自己管理规则，官方文档也给了手动方式：服务端 `listen` 保持单个端口（比如 443），用 iptables 把一段端口范围转发过去：

```bash
iptables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:50000 -j REDIRECT --to-ports 443
```

IPv6 要用 `ip6tables` 再加一条对应的规则：

```bash
ip6tables -t nat -A PREROUTING -i eth0 -p udp --dport 20000:50000 -j REDIRECT --to-ports 443
```

其中 `eth0` 要换成你服务器实际的网卡名，用 `ip a` 可以看。这种手动规则重启后会丢失，需要自己做持久化，具体做法在[S-UI 端口跳跃那篇](https://vpsjq.com/2026/09/06/s-ui-port-hopping/)里有写（用 `iptables-persistent` 保存），这里不重复。

## 配完怎么确认有没有生效

1. **服务端日志**：`journalctl` 里没有关于防火墙规则的报错。
2. **规则是否存在**：手动 iptables 方式用 `iptables -t nat -L PREROUTING -n` 看规则有没有加载。
3. **客户端实际使用**：连上后正常用一段时间，跨过一两个跳跃间隔，连接没有中断，说明端口转发是通的。如果用一小会儿就断，大概率是安全组没放行整段端口。

配完之后如果还是连不上，回到[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)里的排查顺序，先确认单端口的情况下能不能正常连，再去怀疑端口跳跃本身。
