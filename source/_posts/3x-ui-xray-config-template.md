---
title: 3x-ui的Xray配置模板在哪改：默认模板有什么、保存会发生什么、改坏了怎么恢复
date: 2026-10-04 17:00:00
tags:
  - 3x-ui
  - Xray
  - 配置模板
categories:
  - vps工具
description: 3x-ui的Xray配置模板决定路由、出站、日志和DNS。依据3x-ui源码和官方文档，讲清楚模板在面板哪里改、默认模板里有什么、保存时面板会做什么，以及改坏了怎么重置为默认配置。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui的Xray配置模板在哪改：默认模板有什么、保存会发生什么、改坏了怎么恢复",
      "description": "3x-ui的Xray配置模板决定路由、出站、日志和DNS。依据3x-ui源码和官方文档，讲清楚模板在面板哪里改、默认模板里有什么、保存时面板会做什么，以及改坏了怎么重置为默认配置。",
      "datePublished": "2026-10-04T17:00:00+08:00",
      "dateModified": "2026-10-04T17:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/04/3x-ui-xray-config-template/",
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
          "name": "3x-ui的Xray配置模板在哪里改？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在面板左侧的Xray配置页面。基础区把常用的日志、路由等字段做成了界面选项，高级区是一个JSON编辑器，页面标题是高级Xray配置模板，可以按全部、入站、出站、路由规则几种范围编辑。面板说明里写的是：最终的Xray配置文件将基于此模板生成。"
          }
        },
        {
          "@type": "Question",
          "name": "改坏了Xray配置模板怎么恢复？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在Xray配置的基础区有一个重置为默认配置的按钮，点了会弹出确认框，确认后把内置的默认模板载入编辑器。按源码，这一步只是把默认内容载入，需要再点保存才会生效；注意这也会把你加过的自定义出站、路由规则一起换回默认内容。"
          }
        },
        {
          "@type": "Question",
          "name": "直接改xray的config.json可以吗？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不可以。面板每次启动Xray之前都会根据数据库里的模板和入站重新生成config.json，直接改的内容会被覆盖。要改路由、出站、日志等内容，应该改面板里的模板。"
          }
        }
      ]
    }
  ]
}
</script>

想给 3x-ui 加一条屏蔽广告的路由、改日志级别，或者改 DNS，多数教程都会说"改 Xray 配置模板"。但模板到底在面板哪里、默认长什么样、保存之后面板会做什么，很少有人讲清楚。这篇依据 3x-ui 的源码和官方文档，把这几件事讲明白，并讲讲改坏之后怎么恢复。

先说明依据：我读的是 [MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui) 主分支的源码（读到的最新提交是 2026-10-03）、官方文档源文件，以及 `zh-CN.json` 中文翻译。我没有实际运行面板。需要特别注意版本：默认模板的内容和界面是当前主分支的样子，本站其他教程多基于 2.9.4，老版本的模板内容和界面可能不同，我没有核对。另外原版 x-ui 的界面也不同，这篇不适用于它。

<!-- more -->

## 模板是什么，和 config.json 的关系

Xray 最终运行时读的是一个 `config.json`，但这个文件是面板**自动生成**的，里面的内容由两部分拼成：

- **面板里的入站（节点）和用户**，存在数据库里；
- **Xray 配置模板**：路由、DNS、出站、日志、统计策略这些，存在数据库的 `xrayTemplateConfig` 设置项里，初始值是程序内置的一份默认模板。

我读到的 `GetXrayConfig` 的逻辑是：先读出模板，再把数据库里启用的入站逐个并进去，生成最终配置。所以直接改 `config.json` 没用，下次面板启动 Xray 时会被重新写入覆盖。这一点在 [x-ui和3x-ui的配置文件在哪](https://vpsjq.com/2026/10/02/3x-ui-config-file-location/) 里也讲过，这篇接着讲"那应该改哪里"。

## 在面板哪里改

面板左侧菜单的 **Xray 配置** 页面，按源码分成 basic、routing、outbound、balancer、dns、advanced 几个区，和模板相关的主要是两处：

**基础区**：把模板里常用的字段做成了界面选项，比如日志级别和访问日志、屏蔽或直连的 IP 和域名、IPv4 路由、屏蔽 BitTorrent、Freedom 协议策略、出站测试 URL 等。大多数简单需求在这里点选就行，不用碰 JSON。基础区里还有"**重置为默认配置**"按钮，后面会讲。

**高级区**：页面标题是"高级 Xray 配置模板"，说明文字是"最终的 Xray 配置文件将基于此模板生成"。里面是一个 JSON 编辑器，上方可以切换编辑范围：**全部**（整份模板）、**入站**、**出站**、**路由规则**。其中"全部"改整份 JSON；后三项按源码分别编辑模板里的 `inbounds` 数组、`outbounds` 数组和 `routing.rules` 数组，所以在这三个范围里填的内容必须是合法的 JSON 数组，不合法时编辑内容不会被应用。注意"入站"范围里的 `inbounds` 是模板自带的（默认只有一个 api 入站），你在面板里建的节点不在这里。点保存时如果整份 JSON 不合法，页面会报 `Advanced JSON: …` 的错误并停留在高级区。

另外"出站"和"路由"、"负载均衡"、"DNS"这几个区，改的其实也是同一份模板，只是把对应部分做成了专门的界面。出站页的用法见 [3x-ui出站设置怎么用](https://vpsjq.com/2026/10/04/3x-ui-outbounds/)，路由规则见 [3x-ui路由规则配置](https://vpsjq.com/2026/08/29/3x-ui-routing/)。

## 默认模板里有什么

3x-ui 源码里内置了一份 `config.json` 作为默认模板，我读到的当前版本内容大致是：

| 部分 | 默认内容 |
| --- | --- |
| `api` | 启用 HandlerService、LoggerService、StatsService、RoutingService 四个服务，标签 `api` |
| `inbounds` | 一个标签为 `api` 的 `tunnel` 入站，监听 `127.0.0.1:62789`（面板和 Xray 通信用） |
| `log` | `access` 为 `none`，`loglevel` 为 `warning`，也就是默认不记录访问日志 |
| `metrics` | 监听 `127.0.0.1:11111`，标签 `metrics_out` |
| `outbounds` | 两个：标签 `direct` 的 freedom（带 `finalRules`：先屏蔽 `geoip:private`，再放行其他），标签 `blocked` 的 blackhole |
| `policy` | 开启用户级和入站的上下行流量统计，出站的统计默认关闭 |
| `routing` | `domainStrategy` 为 `AsIs`，三条规则：api 入站走 api 出站；`geoip:private` 走 `blocked`；`bittorrent` 协议走 `blocked` |
| `stats` | 空对象，表示启用统计 |

有两个细节值得注意：

- **默认的出站标签是 `direct` 和 `blocked`**，而官方文档里的示例用的是 `direct` 和 `block`（少个 d）。照抄文档示例时，如果规则里的 `outboundTag` 写成 `block`，而你模板里的标签是 `blocked`，规则就指向了一个不存在的出站。按 Xray 的行为这类引用对不上通常会出问题，我没实测，建议以你自己模板里的标签为准；
- **`finalRules` 是 freedom 出站里的新写法**，我没有细究它的完整语义，按字面理解是对直连目标做最后一道过滤。这是主分支的默认值，老版本的默认模板不一定有它。

另外，面板在生成配置时会补齐 api 服务和统计策略（源码里的 `ensureAPIServices`、`ensureStatsPolicy`），所以别想着把 api 入站、统计相关的内容删掉来"精简"，面板的流量统计要靠它们（这一点是我的推断，没实测）。

## 改之前先做三件事

1. **备份**：改模板属于改核心配置，先备份数据库，方法见 [3x-ui面板迁移与备份教程](https://vpsjq.com/2026/08/27/3x-ui-backup-migrate/)；
2. **改最小的范围**：能在基础区点选解决的，就别去改整份 JSON；要改 JSON，优先在"出站"或"路由规则"范围里改，不要动"全部"；
3. **JSON 要合法**：保存时面板会校验，不合法会直接被拒绝（见下一节）。

## 点保存会发生什么

按源码，点"保存"之后依次发生这些事：

1. **校验**：先检查是不是合法 JSON，`outbounds` 是不是数组，然后用 Xray 内核的校验逻辑逐个检查每个出站。有一条值得知道：较新的校验器会拒绝"没有 TLS 或其他加密、并且目标是公网地址"的出站，报错里的原文是 `without TLS or other encryption is prohibited unless the server address is a private IP or domain`。如果你运行的 Xray 内核版本比较旧，面板会放宽这条限制（源码里以内核 26.7.11 为界）；
2. **自动整理**：校验通过后，面板会自动补一些路由相关内容，比如统计相关的路由和 DNS 服务器的路由（源码里的 `EnsureStatsRouting`、`EnsureDnsServerRouting`），所以保存后你再打开，JSON 可能和你提交的有细微差别；
3. **写入数据库**：存进 `xrayTemplateConfig`；
4. **出站测试 URL**：同时保存；如果留空，会用默认的 `https://www.google.com/generate_204`；
5. **应用到运行中的 Xray**：控制器的注释写得很清楚——**只有入站、出站、路由规则变了时，通过 gRPC 接口直接热应用；其他改动则重启 Xray 进程**。如果 Xray 是你手动停掉的，保存后它仍保持停止，不会被自动拉起。

所以改完保存，多数情况下不用手动重启。如果改的是日志、DNS、策略这类，会触发 Xray 进程重启，已有连接会断一下（官方 README 在讲隧道健康监测时提到，重启会断开所有客户端）。

保存后如果 Xray 没起来，先看面板首页的 Xray 状态和日志，再对照 [x-ui面板启动失败怎么办](https://vpsjq.com/2026/10/02/xui-panel-start-failed/) 里的排查思路。

## 改坏了怎么恢复

基础区有一个红色的 **重置为默认配置** 按钮，点了会弹出确认框，确认按钮是"重置"。按源码，它做的是从面板取回内置的默认模板，**载入到编辑器里**。我读到的代码里这一步只改了页面上的编辑内容，并没有直接写入数据库，所以重置之后还需要点**保存**才会真正生效（这是读代码的结论，我没有实际点过）。

重置要注意：

- **它会把你自己加的内容一起换回默认**：自定义的出站（比如 WARP 出站）、路由规则、DNS 设置都会回到默认内容。想保留的话，先把 JSON 复制出来存一份；
- **出站订阅不受影响**：官方文档说明，出站订阅导入的出站是运行时注入进去的，不会改动你保存的模板；
- **入站和用户不受影响**：它们存在数据库里，不属于模板。

如果面板已经打不开了，没法点按钮，就要从命令行或数据库层面处理，具体位置见 [x-ui和3x-ui的配置文件在哪](https://vpsjq.com/2026/10/02/3x-ui-config-file-location/)，操作之前同样先备份。

## 一个最常见的修改示例

按官方文档的写法，在路由里加一条屏蔽广告的规则：

```json
{ "type": "field", "domain": ["geosite:category-ads-all"], "outboundTag": "blocked" }
```

要点：

- `outboundTag` 要写成你模板里**真实存在**的出站标签，默认模板里屏蔽出站的标签是 `blocked`；
- 官方文档强调路由规则是**从上到下、第一条匹配的生效**，所以具体的规则要放在宽泛的规则之上；
- 这样的小改动，直接在面板的"路由规则"页面里加更不容易出错。

## 小结

- 模板存在数据库里，面板每次启动 Xray 时用"模板 + 入站"生成 `config.json`，所以要改模板，不要改文件；
- 入口：Xray 配置 → 基础区点选常用项，高级区编辑 JSON；
- 默认模板里的出站标签是 `direct` 和 `blocked`，照抄文档示例时留意标签对不对得上；
- 保存时面板会校验并整理 JSON；出站、路由规则变化会热应用，其他改动会重启 Xray；
- 改坏了用基础区的"重置为默认配置"，再点保存；它会把自定义内容一起换回默认，改之前先备份。
