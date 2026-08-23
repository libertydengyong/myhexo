---
title: VPS防火墙规则设置了，IPv6那边却像没设一样
date: 2026-08-24 20:00:00
tags:
  - ip6tables
categories:
  - IPv6
description: iptables只管IPv4，IPv6得靠单独的ip6tables，很多发行版默认还把IPv6策略设成完全放行，等于留了个自己都不知道的后门。
---

辛苦用`iptables`把防火墙规则配得严严实实，只放行指定端口、指定IP，自我感觉安全性拉满，结果压根没意识到——**这些规则从头到尾只管住了IPv4这一半，IPv6完全是另一套独立体系，你写的东西对它一个字都不生效**。

## iptables和IPv6，压根不是一回事

`iptables`工作在`AF_INET`这个协议族上，专门为IPv4设计，对IPv6流量完全没有感知能力。IPv6走的是独立协议栈路径，得靠专门的`ip6tables`来管，两者共享底层netfilter框架，但分别注册、分别生效，语法长得几乎一样，管的却是两拨完全不搭界的流量。只用`iptables`配规则、以为IPv6也顺带被保护了，是个非常容易踩、后果却不轻的误区。

配置IPv6对应规则，思路照搬IPv4那一套，工具换成`ip6tables`就行：

```bash
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT
ip6tables -A INPUT -p tcp --dport 80 -j ACCEPT
ip6tables-save > /etc/iptables/rules.v6
```

## 更让人后背发凉的反过来的情况

如果说"规则没生效"只是让你以为自己被保护了、实际没有，那还只是白忙活一场；更麻烦的是**不少发行版的`ip6tables`默认策略，压根不是"拒绝"，而是"完全放行"（ACCEPT）**：

```bash
ip6tables -L INPUT
```

如果看到默认策略显示`ACCEPT`，意味着从这台VPS装好系统那一刻起，IPv6方向的流量就一直毫无过滤地大门敞开，而你可能从来没有主动碰过`ip6tables`这个东西，甚至根本不知道它的存在——不是"配置失误留了漏洞"，是**从起点开始就没设防**。

## ICMPv6不能照搬IPv4的思路一刀切

排查安全时另一个常见冲动是"干脆把ICMPv6也全部堵死，图省事"。这个思路在IPv4上问题不大，**但在IPv6里行不通**——ICMPv6承担的职责比IPv4的ICMP重要得多，邻居发现（NDP，相当于IPv6版本的ARP）、路由通告（地址自动配置全靠它）、路径MTU发现，全部依赖它正常工作。一刀切全部拦掉，轻则地址自动配置失败，重则触发之前写过的[PMTU黑洞问题](https://vpsjq.com/2026/08/21/ipv6-pmtu-blackhole/)——同样是"连接能建立，数据传不动"的诡异症状，追根溯源发现是自己手贱把ICMPv6堵死了。

## 用UFW能省心不少

如果嫌`iptables`和`ip6tables`两套分开管理麻烦，UFW（Uncomplicated Firewall）在`/etc/default/ufw`里把`IPV6`设成`yes`之后，会自动帮你同步维护IPv6对应的规则，不用两边分别敲命令，出这类"顾此失彼"漏洞的概率也小得多。

## 怎么确认自己中招没有

从外部找一台能访问IPv6的设备，实测一下端口连通性，同时对照本机监听情况：

```bash
# 从外部测试
nc -zv 服务器IPv6地址 22

# 本机确认监听状态
netstat -tulnp | grep :22
```

如果IPv4访问一切正常、限制生效，IPv6那边却怎么连都能连上（哪怕是本该被拦住的端口），基本可以确定就是这个坑。

## 顺带一提

这种"IPv6单独游离在常规配置体系之外"的情况，跟之前写的[改了disable_ipv6，IPv6却没被真正关掉](https://vpsjq.com/2026/08/20/linux-disable-ipv6-not-working/)是同一大类问题——很多人管理VPS习惯性只按IPv4思路走一遍，IPv6要么被漏掉、要么行为跟预期完全不一样。如果是排查安全问题时发现了类似的IPv6漏防情况，建议连着[VPS被暴力破解怎么查有没有被入侵](https://vpsjq.com/2026/08/15/vps-brute-force-check/)那篇一起走一遍，确认漏洞暴露的这段时间没被人趁虚而入。
