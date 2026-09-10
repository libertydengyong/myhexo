---
title: Vmess+WebSocket搭建中转服务器
tags:
  - Vmess+WebSocket中转
id: '45'
categories:
  - vps技巧
abbrlink: 65243
date: 2025-05-09 14:13:18
description: 记录使用 Vmess + WebSocket 协议配置 VPS 中转服务器的完整实践流程与节点设置技巧。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Vmess+WebSocket搭建中转服务器",
      "description": "记录使用 Vmess + WebSocket 协议配置 VPS 中转服务器的完整实践流程与节点设置技巧。",
      "datePublished": "2025-05-09T14:13:18+08:00",
      "dateModified": "2025-05-09T14:13:18+08:00",
      "url": "https://vpsjq.com/2025/05/09/vmesswebsocket搭建中转服务器/",
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
      "name": "用Vmess+WebSocket搭建中转落地架构",
      "step": [
        {
          "@type": "HowToStep",
          "name": "落地机配置Vmess入站",
          "text": "在落地机3x-ui面板新建入站，协议选Vmess，添加用户时传输协议选WebSocket，输入6-8位随机路径字符，保存后把生成的链接导入V2RAY客户端测试速度确认配置成功。"
        },
        {
          "@type": "HowToStep",
          "name": "中转机配置dokodemo-door入站",
          "text": "登录中转机面板新建入站，协议选dokodemo-door（任意门），目标地址填落地机IP，目标端口填落地机的Vmess端口，保存完成配置。"
        },
        {
          "@type": "HowToStep",
          "name": "客户端指向中转机测试",
          "text": "编辑客户端的服务器配置，地址改成中转机IP，端口改成中转机端口，右键测速确认显示速度数据说明配置正常。"
        }
      ]
    }
  ]
}
</script>

文章来源:     https://www.laoliuceping.com/31450.html 比如一台德国机慢，一台日本机快，给两台服务器都安装3x-ui面板，配置德鸡，面板进入“新建入站”界面。

1.  选择协议为Vmess，默认端口为10391。
2.  添加用户时选择传输协议为WebSocket，并输入6-8位随机路径字符（如：`/abc123`）。
3.  确认后保存设置，将生成的链接导入到V2RAY客户端测试。若速度显示为数字，则表示配置成功。

#### 配置日本中转机入站规则

1.  登录中转机的3x-ui面板，进入“新建入站”界面。
2.  协议选择为dokodemo-door（中文名“任意门”），默认端口为35466。
3.  设置目标地址和端口：目标地址填写德国落地机的IP（如：95.169.x.x），目标端口为10391。
4.  保存设置，完成配置。

#### 修改V2RAY客户端设置

1.  编辑落地机的服务器配置，名称可随意设置。
2.  地址修改为中转机的IP（如：5.34.x.x），端口修改为中转机的端口35466。
3.  确认后右键测速，若显示速度数据则说明配置正常。


相关内容
[**S-UI面板搭建**](https://vpsjq.com/2025/11/17/s-ui面板搭建/)

[**S-UI 中转落地**](https://vpsjq.com/2025/05/09/vmesswebsocket搭建中转服务器//)
