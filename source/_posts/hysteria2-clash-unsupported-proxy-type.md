---
title: Clash报unsupported proxy type hysteria2怎么办？换mihomo内核和手写节点配置
date: 2026-10-02 17:00:00
tags:
  - Hysteria2
  - Clash
  - mihomo
categories:
  - vps工具
description: Clash导入Hysteria2节点提示unsupported proxy type，多半是内核太旧，不认识hysteria2这个类型。这篇讲怎么判断自己用的内核、mihomo从哪个版本开始支持，以及按官方文档手写一个能用的Hysteria2节点配置。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Clash报unsupported proxy type hysteria2怎么办？换mihomo内核和手写节点配置",
      "description": "Clash导入Hysteria2节点提示unsupported proxy type，多半是内核太旧，不认识hysteria2这个类型。这篇讲怎么判断自己用的内核、mihomo从哪个版本开始支持，以及按官方文档手写一个能用的Hysteria2节点配置。",
      "datePublished": "2026-10-02T17:00:00+08:00",
      "dateModified": "2026-10-02T17:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-clash-unsupported-proxy-type/",
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
      "name": "解决Clash不支持Hysteria2节点的问题",
      "step": [
        {
          "@type": "HowToStep",
          "name": "确认当前使用的内核",
          "text": "在客户端的设置里找到内核或Core的信息，确认它是mihomo（也叫Clash Meta）内核，以及具体版本号。"
        },
        {
          "@type": "HowToStep",
          "name": "换成或升级到mihomo内核",
          "text": "mihomo在v1.16.0版本的更新说明里加入了对Hysteria2的支持，内核比这个版本更旧，或者根本不是mihomo内核，就需要更换或升级。"
        },
        {
          "@type": "HowToStep",
          "name": "检查节点配置字段",
          "text": "节点类型必须写成hysteria2，并按mihomo官方文档填写server、port、password、sni、skip-cert-verify等字段。"
        },
        {
          "@type": "HowToStep",
          "name": "重新加载配置并测试",
          "text": "保存配置后重启内核或重新加载配置，节点正常出现后测试连通性，仍不通就回到服务端和客户端的参数对照排查。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Clash提示unsupported proxy type hysteria2是什么原因？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "这个提示表示内核不认识hysteria2这种节点类型，最常见的原因是内核太旧或者用的不是mihomo（Clash Meta）内核。mihomo在v1.16.0的更新说明里加入了对Hysteria2的支持，需要换成mihomo内核，或者把它升级到支持的版本。"
          }
        },
        {
          "@type": "Question",
          "name": "Clash支持Hysteria2吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "取决于内核。mihomo（Clash Meta）内核支持Hysteria2，并在官方文档里给出了hysteria2节点的完整配置字段。原版Clash的仓库我查询时已经无法访问，没有官方文档可以核对，但它停止更新的时间早于mihomo加入支持，所以不支持是合理的推断。"
          }
        },
        {
          "@type": "Question",
          "name": "mihomo里Hysteria2节点怎么写？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "type写hysteria2，再填server、port、password，证书和域名相关的字段是sni和skip-cert-verify，服务端开了混淆还要填obfs和obfs-password。端口跳跃用ports和hop-interval字段。具体字段以mihomo官方文档为准。"
          }
        }
      ]
    }
  ]
}
</script>

导入 Hysteria2 节点时，Clash 类客户端提示 `unsupported proxy type: hysteria2`，或者带着节点序号的 `proxy 0 unsupport proxy type hysteria2`，这是搜这个问题的人最常看到的几种写法。意思其实很直接：**内核不认识 `hysteria2` 这个节点类型**。节点本身大概率没有问题，问题出在跑配置的那个内核。服务端有没有搭好，可以先对照[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)里的排查顺序确认一遍。

## 先分清：Clash 不是一个东西

"Clash"这个名字现在指的是好几个东西，只有搞清楚你用的是哪一个，才知道该怎么办：

- **原版 Clash 内核**：原作者的仓库我查询时已经访问不到（GitHub 接口返回 404），所以没有官方文档可以核对它是否支持 Hysteria2。它不再更新是确定的，而 Hysteria2 的支持是后来才加到 mihomo 里的，所以**原版不支持是合理推断**，不是我从官方文档查到的结论。
- **mihomo 内核（也叫 Clash Meta）**：目前社区在维护的 Clash 内核。我查了它的更新记录：**v1.16.0（2023 年 9 月 25 日发布）的更新说明里就有 `support Hysteria2`**。官方文档里有专门的 hysteria2 节点配置页。
- **各种客户端**：很多图形客户端只是壳，里面装的是 mihomo 内核。比如 OpenClash 的说明里写明它是 Mihomo(Clash) 客户端，clash-verge-rev 的说明里写着内置 Clash.Meta(mihomo) 内核，并支持切换 Alpha 版本内核。

所以报错的几种可能是：用的是不带 Hysteria2 的旧内核；内核是 mihomo 但版本比 v1.16.0 还老；或者节点配置本身写错了。

## 第一步：确认你用的内核和版本

不同客户端看内核信息的入口不一样，我不逐个写菜单路径，免得写错。通用的做法是：

- 在客户端设置里找"内核""Core"之类的页面，看它显示的是不是 mihomo 或者 Clash Meta，以及版本号。
- 能进命令行的环境（比如 OpenWrt），可以直接运行 `mihomo -v` 查看版本，具体可执行文件名以你实际安装的为准。

如果显示的是原版 Clash 或者 Premium，就需要换内核；如果是 mihomo 但版本低于 v1.16.0，就升级。

## 第二步：换成 mihomo 内核

- **图形客户端**：换一个内置 mihomo 内核的客户端，或者在设置里把内核切换成 mihomo。
- **OpenWrt 的 OpenClash**：它本身就是 Mihomo 客户端，按它的说明更新内核。
- **只想先验证节点是否可用**：直接下载 mihomo 的官方发布版本，用它加载你的配置，能排除客户端软件的干扰。

这里要提醒：内核升级之后，**配置字段也可能随版本有新增**，比如端口跳跃相关的字段。想用新字段，除了内核要新，也要看更新说明有没有相应的支持，我这里没有逐个字段去核对是哪个版本加的。

## 第三步：按官方文档检查节点配置

mihomo 官方文档给的 Hysteria2 节点示例是这样的（只摘了常用字段）：

```yaml
proxies:
  - name: "hysteria2"
    type: hysteria2
    server: server.com
    port: 443
    password: yourpassword
    sni: server.com
    skip-cert-verify: false
```

需要时再加上这些：

```yaml
    ports: 20000-50000      # 端口跳跃的范围
    hop-interval: 30        # 切换端口的间隔，单位秒，也可以写成 "15-30" 这样的随机范围
    obfs: salamander        # 混淆类型，服务端开了才填
    obfs-password: yourpassword
    fingerprint: xxxx       # 证书的 SHA256 指纹
    alpn:
      - h3
```

官方文档里几点说明：

- `port` 在配置了 `ports` 时会被忽略，也就是用端口跳跃时以 `ports` 为准。
- `up` 和 `down` 是带宽，没写单位的时候，默认单位是 Mbps。
- `obfs` 可以填 `salamander` 或 `gecko`，留空就表示不使用混淆。
- `skip-cert-verify` 是跳过证书验证，官方提示它有安全上的影响。

### 分享链接的参数怎么对应

如果你手里是一条 `hysteria2://` 链接，各参数和上面字段的对应关系，我是对照字段含义整理的，不是官方给出的一张对照表，仅供参考：

| 链接里 | mihomo 里 |
|---|---|
| `@` 前面的认证信息 | `password` |
| 主机、端口 | `server`、`port` |
| `sni=` | `sni` |
| `insecure=1` | `skip-cert-verify: true` |
| `obfs=salamander`、`obfs-password=` | `obfs`、`obfs-password` |
| `pinSHA256=` | `fingerprint`（官方文档描述为 SHA256 证书指纹） |

链接各参数本身的含义，见[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)那篇的表格。端口跳跃的服务端怎么配，见[端口跳跃配置](https://vpsjq.com/2026/10/02/hysteria2-port-hopping/)。

### 关于 up 和 down

在 Hysteria 官方的说法里，客户端写了带宽就启用 Brutal，不写就用 BBR，填大了会适得其反。这是 Hysteria 官方客户端的行为，**mihomo 里 `up`、`down` 具体怎么影响拥塞控制，我没有核对过**。不确定的话，先不要填一个很大的值，具体可以看[速度慢怎么办](https://vpsjq.com/2026/10/02/hysteria2-slow-speed/)里的排查思路。

## 订阅导入的几个注意点

用订阅链接导入时，还有两类常见情况：

1. **订阅里根本没有 Hysteria2 节点**：订阅是面板生成的，格式和内容取决于面板和订阅类型。面板导出的订阅里没有这个节点，客户端当然不会显示，先确认面板端节点是不是启用了、订阅有没有包含它。3x-ui 的 Clash 订阅导入可以看[这篇](https://vpsjq.com/2026/08/30/3x-ui-clash/)。
2. **订阅转换服务不认识新协议**：如果中间经过订阅转换，转换器本身也可能不支持 Hysteria2，导致生成的配置里这个节点被丢掉或者写错。这时候换成手写节点配置，能最快判断问题出在哪一层。

## 排查顺序

1. **看报错是不是"unsupported proxy type"**：是，就是内核不认识，先看内核。
2. **确认内核是 mihomo，并且版本不低于 v1.16.0**。
3. **节点 `type` 写成 `hysteria2`**，不是 `hy2`，也不是旧的 `hysteria`。
4. **字段名和官方文档逐项对照**，尤其是 `password`、`sni`、`skip-cert-verify`。
5. **内核认出来了但连不上**：这是另一类问题，回到服务端和客户端参数的对照，先确认 UDP 端口放行、证书验证选项和混淆设置，见[客户端导入那篇的排查顺序](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

## 这篇没有覆盖的

Surge、Loon、Quantumult X、Shadowrocket 这类 iOS 客户端对 Hysteria2 的支持，和 Clash 内核是两套体系，我没有核对它们各自的文档，所以这篇不写。想了解 Hysteria2 本身值不值得用，可以看[优点和缺点](https://vpsjq.com/2026/10/02/hysteria2-pros-cons/)那篇。
