---
title: Hysteria2速度慢怎么办？bandwidth设置不当反而更慢
date: 2026-10-02 15:20:00
tags:
  - Hysteria2
  - 速度优化
categories:
  - vps工具
description: Hysteria2连上了但速度慢，最常见的原因是bandwidth填得不对：写了就启用Brutal，不写走BBR。这篇按官方文档讲清怎么选，再补UDP缓冲区、服务端限速和线路因素的排查顺序。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Hysteria2速度慢怎么办？bandwidth设置不当反而更慢",
      "description": "Hysteria2连上了但速度慢，最常见的原因是bandwidth填得不对：写了就启用Brutal，不写走BBR。这篇按官方文档讲清怎么选，再补UDP缓冲区、服务端限速和线路因素的排查顺序。",
      "datePublished": "2026-10-02T15:20:00+08:00",
      "dateModified": "2026-10-02T15:20:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/hysteria2-slow-speed/",
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
      "name": "排查并改善Hysteria2速度慢",
      "step": [
        {
          "@type": "HowToStep",
          "name": "先检查客户端bandwidth",
          "text": "客户端配置里写了bandwidth就会启用Brutal拥塞控制，不写则使用默认的BBR。先删掉bandwidth对比测速，如果更快，说明之前填的值超过了线路实际能力。"
        },
        {
          "@type": "HowToStep",
          "name": "再看服务端是否限速",
          "text": "服务端bandwidth.up/down是对每个客户端的限速，默认不限制；确认配置里没有填一个偏低的值，客户端下载速度对应服务端的上传限速。"
        },
        {
          "@type": "HowToStep",
          "name": "调大系统UDP缓冲区",
          "text": "官方建议在Linux上把net.core.rmem_max和net.core.wmem_max都设为16777216(16MB)，写入sysctl配置文件让它重启后仍然生效。"
        },
        {
          "@type": "HowToStep",
          "name": "对比其他协议判断是否线路问题",
          "text": "同一台服务器上换成基于TCP的协议(例如VLESS Reality)测速，如果TCP协议明显更快，问题可能出在运营商对UDP的处理上，而不是配置。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Hysteria2的bandwidth是不是填得越大越快？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是。官方文档明确提醒，带宽值不是越大越好，千万不要超过当前网络实际能支持的最大带宽，否则会适得其反，造成网络拥塞和连接不稳定。应该填接近线路真实带宽的值，或者干脆不填让它使用BBR。"
          }
        },
        {
          "@type": "Question",
          "name": "Hysteria2用的是BBR还是Brutal？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "取决于客户端配置：写了bandwidth的方向使用Brutal拥塞控制，删掉bandwidth或不写，就使用congestion字段指定的算法，默认是BBR。上行和下行是分别判断的。"
          }
        },
        {
          "@type": "Question",
          "name": "服务端bandwidth和客户端bandwidth是什么关系？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "服务端的bandwidth是对每个客户端的限速，不填或填0表示不限；服务端的上传速度就是客户端的下载速度，反过来也一样。服务端还可以开ignoreClientBandwidth，无视客户端填的带宽值并改用非Brutal的拥塞控制。"
          }
        }
      ]
    }
  ]
}
</script>

Hysteria2 连得上、但速度比预期慢很多，先别急着怀疑服务器线路。这个协议有个和别的协议不太一样的地方：**你在配置里有没有写 `bandwidth`，会直接决定它用哪种拥塞控制算法**。很多人为了"跑满带宽"把数字填得很大，结果反而更慢，下面按官方文档把这件事讲清楚，再说其他几个常见原因。配置怎么写、客户端怎么连，前面两篇有讲：[服务端 config.yaml](https://vpsjq.com/2026/10/02/hysteria2-config-yaml/)、[客户端导入连接](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。

## 第一步：看客户端有没有写 bandwidth

客户端配置里长这样的一段：

```yaml
bandwidth:
  up: 20 mbps
  down: 100 mbps
```

按官方文档的说法，写了 `bandwidth` 的方向就会启用 **Brutal** 拥塞控制，也就是按你填的速度硬推流量，丢包时还会尝试比设定值稍快一点发送来补偿；不写或者删掉整段，就使用默认的 **BBR**，让算法自己探测线路能跑多快。上行、下行是分别判断的。

官方对这个值的提醒很直接：**不是越大越好，千万别超过当前网络真正能支持的最大带宽，否则会适得其反，造成拥塞和连接不稳定。**

所以速度慢时最快的排查方法就是：

1. 先把客户端的 `bandwidth` 整段删掉，用 BBR 测一次速。
2. 如果比之前快，说明之前填的数字超过了线路实际能力，要么保持不填，要么改成接近你**实测**带宽的值。
3. 如果删掉后更慢，再去填一个贴近实测的值，不要凭感觉往大了填。

`up` 是客户端上传，`down` 是客户端下载。图形客户端里一般也有对应的上传、下载带宽两栏，导入链接时如果客户端自动填了很大的默认值，也要留意。

如果担心丢包导致 Brutal 发得太猛，客户端还有一个 `disableLossCompensation` 选项，开启后只按设定速度发送，不再多发来补偿丢包，官方说明这个选项只对本端生效。

## 第二步：看服务端有没有限速

服务端配置里也有 `bandwidth`，但含义不同：它是**对每个客户端的限速**，不写或者写 0 就是不限制。官方特别说明了方向：服务端的上传速度就是客户端的下载速度，反过来也一样。所以如果你的服务端配置里写过类似 `up: 10 mbps` 的值，客户端的下载就会被卡在这个速度上。

```yaml
bandwidth:
  up: 100 mbps
  down: 100 mbps
```

排查时直接确认服务端配置文件里有没有这段，没有特殊需要就删掉。

另外服务端还有一个 `ignoreClientBandwidth` 选项，开启后服务端会无视客户端填的带宽值，强制使用非 Brutal 的拥塞控制。官方说它主要给想让流量对其他网络流量更公平、或者不信任用户自己填的带宽值的服务器管理者用，自己一个人用的话一般不需要打开。

## 第三步：调大系统的 UDP 缓冲区

官方的性能调优页面建议，Linux 上把 UDP 的收发缓冲区都设成 16 MB：

```bash
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
```

这样设置重启就失效了，想长期生效就写到配置文件里：

```bash
cat > /etc/sysctl.d/99-hysteria.conf <<'EOF'
net.core.rmem_max=16777216
net.core.wmem_max=16777216
EOF
sysctl --system
```

服务端和客户端所在的机器都可以这样设。缓冲区太小在高速或高延迟线路上，会让 UDP 包来不及收而被丢掉。

## 第四步：QUIC 窗口和进程优先级（一般不用动）

官方还提供了几个 QUIC 流控窗口的参数，比如 `initStreamReceiveWindow`、`maxConnReceiveWindow` 等，默认值是单个流 8 MB、整个连接 20 MB。官方给的建议是保持流窗口和连接窗口大约 2:5 的比例，避免某一个卡住的流占满整个连接。默认值本身就满足这个比例，没有明确理由不用改，乱调反而可能出问题。

进程优先级方面，官方给了用 systemd 把服务的 `Nice` 值设成 `-5` 的做法，也提醒了实时调度会影响其他进程的响应，要先小幅调整测试。这条对大部分场景提升有限，放在最后再考虑。

## 第五步：判断是不是线路本身的问题

上面几项都排除了还是慢，就要考虑线路。这一条官方文档里没有明确说明，是实际使用中常见的情况，**没有官方依据，请当作经验参考**：部分网络环境对 UDP 流量的处理不如 TCP，高峰时段 UDP 可能被限速或者丢包更多。

判断方法很简单，在同一台服务器上同时搭一个基于 TCP 的节点，比如 [VLESS Reality](https://vpsjq.com/2026/08/27/3x-ui-vless-reality/)，在相同时间、相同网络下分别测速：

- TCP 节点明显更快、Hysteria2 慢，而且删掉 `bandwidth` 也没改善，问题更可能在这条线路上对 UDP 的处理。
- 两个都慢，那是服务器线路或本地网络本身的问题，换协议没用。

也可以对比同样基于 QUIC/UDP 的 [TUIC 节点](https://vpsjq.com/2026/09/06/s-ui-tuic/)，看是不是 Hysteria2 特有的现象。换端口、换时间段多测几次，比只测一次可靠得多。

## 速度慢排查清单

1. 客户端 `bandwidth` 先删掉，用 BBR 对比一次。
2. 服务端 `bandwidth` 有没有填了偏低的限速。
3. UDP 缓冲区是否按官方建议设为 16 MB。
4. 用 TCP 协议和 TUIC 做对照，判断是不是线路问题。
5. 连不上或者握手失败是另一类问题，对照[客户端导入那篇的排查顺序](https://vpsjq.com/2026/10/02/hysteria2-client-import/)。
