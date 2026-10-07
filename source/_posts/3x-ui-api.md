---
title: 3x-ui API怎么用：Bearer令牌怎么创建，有哪些接口，admin、monitor、node-sync三种权限的区别
date: 2026-10-07 19:00:00
tags:
  - 3x-ui
  - API
categories:
  - vps工具
description: 3x-ui面板自带REST API，可以用Bearer令牌做脚本、监控和多面板管理。依据3x-ui源码和官方OpenAPI文档，讲清楚令牌在哪创建、三种权限范围的区别、接口分了哪几类、怎么发请求，以及要注意的安全问题。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui API怎么用：Bearer令牌怎么创建，有哪些接口，admin、monitor、node-sync三种权限的区别",
      "description": "3x-ui面板自带REST API，可以用Bearer令牌做脚本、监控和多面板管理。依据3x-ui源码和官方OpenAPI文档，讲清楚令牌在哪创建、三种权限范围的区别、接口分了哪几类、怎么发请求，以及要注意的安全问题。",
      "datePublished": "2026-10-07T19:00:00+08:00",
      "dateModified": "2026-10-07T19:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/07/3x-ui-api/",
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
          "name": "3x-ui的API令牌在哪里创建？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "在面板设置的安全设定里管理API令牌，OpenAPI文档的说明是Settings → Security → API Token。创建时可以填名称、权限范围和过期时间，令牌的明文只在创建时显示一次，面板里只存它的SHA-256哈希。脚本安装时还会生成一个令牌，写在/etc/x-ui/install-result.env里。"
          }
        },
        {
          "@type": "Question",
          "name": "3x-ui API怎么认证？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "有两种方式：浏览器会话用POST /login拿到的cookie；脚本和程序用Bearer令牌，在请求头里写Authorization: Bearer 令牌。两种方式对/panel/api/下的接口都有效。用Bearer令牌的请求不需要再带CSRF令牌。"
          }
        },
        {
          "@type": "Question",
          "name": "admin、monitor、node-sync三种令牌权限有什么区别？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "admin是默认权限，等同于管理员，可以访问全部接口；monitor只能用GET和HEAD访问一小批状态和监控类接口；node-sync只能访问多面板同步需要的一批指定接口。monitor和node-sync是按源码里的白名单限制的，访问白名单以外的接口会返回403。"
          }
        }
      ]
    }
  ]
}
</script>

3x-ui 面板除了网页界面，还自带一套 REST API，用来做自动化：比如写脚本批量加用户、拿监控数据、定时备份，或者让一个主面板管理多个远程面板。很多人只知道面板有"API 令牌"这个选项，不清楚怎么用、有什么风险。这篇依据 3x-ui 的源码和官方的 OpenAPI 规范，把认证方式、三种令牌权限、接口分类和请求写法讲清楚。

先说明依据：我读了 [MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui) 主分支的源码（读到的最新提交是 2026-10-06）、官方文档里的 API 页面、仓库里的 OpenAPI 规范文件（版本标注为 3.x），以及控制 API 权限的代码。**我没有实际调用过这些接口**，文中的请求示例是按规范拼出来的，先在测试环境试过再用。另外这是 3.x 的接口，本站其他教程多基于 2.9.4，老版本的接口路径和功能可能不同，我没有核对。

<!-- more -->

## 认证：两种方式

官方文档和规范里写的认证方式有两种：

1. **会话 cookie**：先 `POST /login` 登录，面板返回一个名叫 `3x-ui` 的 cookie，后面的请求带着它。这种主要是浏览器界面用的；
2. **Bearer 令牌**：在请求头里写 `Authorization: Bearer <令牌>`。脚本、机器人、远程面板用这种。

两种对 `/panel/api/` 下的接口都有效。登录接口接收 JSON，字段是 `username`、`password`，开了双重验证的话再加 `twoFactorCode`：

```json
{ "username": "你的用户名", "password": "你的密码", "twoFactorCode": "123456" }
```

返回的统一格式是 `{"success": true/false, "msg": "...", "obj": ...}`，数据在 `obj` 里。

规范里还说明：用 cookie 登录的浏览器会话，在发"不安全"请求（比如 POST）时要带 CSRF 令牌，先 `GET /csrf-token` 取，放进 `X-CSRF-Token` 请求头；而**用 Bearer 令牌的请求不需要**，中间件对已认证的 API 请求会跳过 CSRF。所以写脚本用 Bearer 令牌更省事。

## 令牌在哪里创建

规范对令牌的描述是：在 **Settings → Security → API Token** 里取，对应中文界面的面板设置里"安全设定"页。我读到的中文界面有这些文字：新建令牌、名称（占位示例 `central-panel-a`）、"暂无令牌——创建一个用于认证机器人或远程面板"、删除时的警告"使用此令牌的任何调用方将立即无法认证"，以及创建成功后的提示"**请立即复制此令牌。出于安全考虑，它不会以可读形式存储，也不会再次显示**"。

按规范，创建令牌的请求（`POST /panel/api/setting/apiTokens/create`）有三个字段：

| 字段 | 含义 |
| --- | --- |
| `name` | 必填，一个好认的名字 |
| `scope` | 权限范围：`admin`（默认）、`monitor` 或 `node-sync` |
| `expiresAt` | 过期时间，未来的 Unix 毫秒时间戳，填 `0` 表示永不过期 |

关于令牌的几个事实：

- **只存哈希**：数据库里存的是令牌的 SHA-256 哈希，明文只在创建时返回一次，丢了只能删掉重建；
- **可以停用**：有"启用/停用"开关，被停用的令牌在下次请求时就会被拒绝；
- **脚本安装时会送你一个**：官方文档的 First Login 页说，脚本安装结束会把凭据写进只有 root 可读的 `/etc/x-ui/install-result.env`，里面有一项 `XUI_API_TOKEN`。这个令牌默认也是 admin 权限，要保管好，不用的话可以在面板里删掉。

## 三种权限范围的区别

这是最值得讲清楚的一点。我读了控制权限的源码，结论是：

| 范围 | 能做什么 |
| --- | --- |
| `admin`（默认） | 全部接口，和管理员登录后的权限一样 |
| `monitor` | 只能用 **GET 和 HEAD**，并且只能访问一份很短的白名单，全是状态和监控类 |
| `node-sync` | 只能访问多面板同步用的一份指定接口（按路径和方法限定） |

**monitor** 的白名单（源码里的原文路径）是：

- `/server/status`（CPU、内存、磁盘、网络等实时状态）
- `/server/cpuHistory/:bucket`、`/server/history/:metric/:bucket`（历史曲线）
- `/server/xrayMetricsState`、`/server/xrayMetricsHistory/...`（Xray 运行指标）
- `/server/xrayObservatory`、`/server/xrayObservatoryHistory/...`（出站健康观测）
- `/server/getXrayVersion`、`/server/getPanelUpdateInfo`（版本和更新信息）
- `/nodes/history/...`（节点历史）

用 monitor 或 node-sync 令牌访问白名单以外的接口，会返回 **403**，提示"this API token is not permitted to access this endpoint"。

所以**给监控脚本、探针用的令牌，一定要建成 monitor**，这样令牌即使泄露，也只能看状态，不能改配置。admin 令牌等同管理员密码，官方文档也明确说它们是完整的管理员凭据，要安全保存。

**node-sync** 是给多面板管理用的：让一个主面板去同步远程面板（节点）的入站和客户端，白名单里有 `/server/status`、`/inbounds/list`、`/inbounds/add`、`/inbounds/update/:id`、`/clients/add` 等。多节点管理的背景见官方文档的 multi-node 页，我这次没有深读，不展开。

## 一个小细节：认证失败时返回什么

源码里对未认证请求有特殊处理：

- 带了 Bearer 令牌但令牌错误或被停用：返回 **401**；
- 没带任何凭据的裸请求：返回 **404**（让扫描器分辨不出这里有没有面板）。

所以调接口时如果得到 404，先检查是不是路径写错、URI 路径（面板路径）漏了，还是根本没带令牌。

## 接口地址怎么拼

规范里的服务器地址写的是 `/`，说明接口地址**跟着面板的 URI 路径走**（"basePath aware"）。也就是说，如果你的面板地址是 `https://域名:端口/abc/`，那么接口地址就是：

```text
https://域名:端口/abc/panel/api/...
```

面板路径是什么，见 [3x-ui面板设置怎么设](https://vpsjq.com/2026/10/07/3x-ui-panel-settings/)。

## 接口分了哪几类

规范按标签分了这些组（括号里是接口数量，按我读到的版本）：

| 分类 | 数量 | 大致用途 |
| --- | --- | --- |
| Authentication | 5 | 登录、登出、取 CSRF 令牌、是否开启 2FA |
| Inbounds | 18 | 入站的列表、增删改、启停、重置流量、导入、回落规则 |
| Clients | 48 | 客户端的增删改、批量操作、分组、流量、在线状态、订阅链接 |
| Server | 40 | 服务器状态、重启/停止 Xray、装 Xray、日志、备份和恢复数据库、生成密钥 |
| Nodes | 16 | 多面板管理：远程节点的增删改和探测 |
| Hosts | 12 | 主机组管理 |
| Settings | 11 | 读取和保存面板设置、修改管理员账号、重启面板、测试 SMTP 和机器人 |
| API Tokens | 4 | 令牌的列表、创建、删除、启停 |
| Xray Settings | 26 | Xray 配置模板、出站、WARP/Nord/PIA、路由测试、geo 数据、出站订阅 |
| Subscription Balancers | 5 | 订阅负载均衡 |
| Subscription Server | 4 | 订阅内容本身（base64、JSON、Clash） |
| WebSocket、Backup | 各 1 | 实时推送、备份发送到 Telegram |

面板自己也能提供这份规范：`GET /panel/api/openapi.json` 返回完整的 OpenAPI 文档，并且面板里有"API 文档"菜单项，可以边看边试。

## 请求示例

下面的示例都是**按规范拼的，我没有实际调用过**，`令牌`、地址和路径要换成你自己的。

查看服务器状态（monitor 令牌也能用）：

```bash
curl -H "Authorization: Bearer 你的令牌" \
  "https://域名:端口/你的面板路径/panel/api/server/status"
```

列出所有入站：

```bash
curl -H "Authorization: Bearer 你的令牌" \
  "https://域名:端口/你的面板路径/panel/api/inbounds/list"
```

列出所有客户端：

```bash
curl -H "Authorization: Bearer 你的令牌" \
  "https://域名:端口/你的面板路径/panel/api/clients/list"
```

生成一个新的 UUID（建客户端时用）：

```bash
curl -H "Authorization: Bearer 你的令牌" \
  "https://域名:端口/你的面板路径/panel/api/server/getNewUUID"
```

重启 Xray（需要 admin 令牌）：

```bash
curl -X POST -H "Authorization: Bearer 你的令牌" \
  "https://域名:端口/你的面板路径/panel/api/server/restartXrayService"
```

几点说明：

- 面板用自签证书时，不要图省事用 `curl -k` 关掉校验，最好给面板配上正规证书，或者让脚本信任你的 CA；
- 有请求体的接口（比如添加客户端、保存设置），字段结构较复杂，建议先在面板"API 文档"里对照示例，或者先用 `GET` 取回现有对象，再按它的结构修改后提交；
- 面板更新 Xray 配置模板这类接口的行为，见 [3x-ui的Xray配置模板在哪改](https://vpsjq.com/2026/10/04/3x-ui-xray-config-template/) 里"点保存会发生什么"，通过接口保存和在界面点保存走的是同一条逻辑（`POST /panel/api/xray/update`）。

## 常见用法

- **监控**：建一个 monitor 令牌，定时拉 `/server/status` 和 Xray 观测数据，接到自己的告警上；
- **批量管理用户**：用 Clients 组的批量接口（批量创建、批量启用或停用、批量调整到期和流量）；
- **定时备份**：Server 组有下载数据库备份的接口（`getDb`），备份和迁移的完整做法见 [3x-ui面板迁移与备份教程](https://vpsjq.com/2026/08/27/3x-ui-backup-migrate/)；
- **用户管理参考**：界面上怎么管多用户，见 [3x-ui多用户管理](https://vpsjq.com/2026/08/27/3x-ui-multi-user/)。

## 安全上要注意

- **默认令牌是 admin 权限**，等同管理员，别写进公开仓库、别贴到聊天里；
- **按用途建令牌**：监控用 monitor，不要为了省事一个 admin 令牌到处用；
- **设过期时间**：临时用途的令牌填 `expiresAt`，不要永不过期；
- **走 HTTPS**：令牌在请求头里明文传输，面板必须配 TLS，或放在反向代理后面，见 [3x-ui用Nginx反向代理隐藏面板](https://vpsjq.com/2026/09/28/3x-ui-nginx-reverse-proxy/)；
- **泄露后立刻删除或停用令牌**，并检查日志；
- 面板本身的加固清单见 [3x-ui面板设置怎么设](https://vpsjq.com/2026/10/07/3x-ui-panel-settings/)；官方入口见 [3x-ui是什么](https://vpsjq.com/2026/10/04/3x-ui-what-is-github-docs/)。

## 小结

- 认证有两种：cookie 会话（浏览器）和 Bearer 令牌（脚本），Bearer 请求不需要 CSRF 令牌；
- 令牌在面板设置的安全设定里管理，明文只显示一次，库里只存哈希；
- 三种权限：`admin` 全部接口，`monitor` 只读且白名单很短，`node-sync` 只限多面板同步；
- 接口地址要带上面板的 URI 路径；认证失败，有令牌返回 401，没带凭据返回 404；
- 本文依据 3.x 的源码和规范，接口示例没有实际调用，上线前先在测试环境验证。
