---
title: LiteSpeed Cache插件配置教程：页面缓存、图片优化和CDN
date: 2026-08-30 12:00:00
tags:
  - LiteSpeed Cache
  - WordPress优化
categories:
  - WordPress
description: LiteSpeed Cache插件的页面缓存、图片优化和QUIC.cloud CDN配置方法，配合OpenLiteSpeed服务器使用效果最好。
---

LiteSpeed Cache 是专门为 LiteSpeed 和 OpenLiteSpeed 服务器设计的 WordPress 缓存插件，配合 OpenLiteSpeed 使用效果比其他缓存插件好很多，因为插件可以直接调用服务器层面的缓存机制，不只是 PHP 层面的缓存。安装完之后网站速度提升很明显，页面加载时间能缩短不少。

在 WordPress 后台直接安装，左侧菜单点**插件** -> **添加新插件**，搜索"LiteSpeed Cache"，找到之后安装并启用。如果你的服务器是用 OpenLiteSpeed 搭建的，可以参考[一键安装OpenLiteSpeed与WP](https://vpsjq.com/2026/07/22/一键安装-openlitespeed与wp/)，装好服务器环境之后再安装这个插件。

启用插件之后左侧菜单会多出一个 LiteSpeed Cache 的设置入口。第一步先开启页面缓存，进入**LiteSpeed Cache** -> **缓存**，把**启用缓存**打开，保存设置。开启之后访客请求页面的时候，服务器会直接返回缓存好的静态 HTML，不需要每次都重新执行 PHP 和查询数据库，速度提升最明显的就是这一步。

图片优化用的是 QUIC.cloud 的在线压缩服务。进入**LiteSpeed Cache** -> **图片优化**，点**请求优化积分**，插件会把网站上的图片上传到 QUIC.cloud 服务器进行压缩，压缩完之后替换掉原来的图片文件。QUIC.cloud 每个月有免费额度，图片不多的小站基本够用，超出额度之后需要付费或者等下个月额度刷新。压缩之后图片文件大小明显减小，但视觉质量基本看不出差别，对页面加载速度有直接帮助。

CDN 配置同样走 QUIC.cloud。进入**LiteSpeed Cache** -> **CDN**，把 QUIC.cloud CDN 打开，需要先在 QUIC.cloud 官网注册账号，然后在插件里填入域名，QUIC.cloud 会给你的网站分配 CDN 节点，静态资源（图片、CSS、JS 文件）通过 CDN 分发，访客从离自己最近的节点拉取资源，速度更快。QUIC.cloud CDN 同样有免费额度，小站够用。

开启缓存之后如果发现网站某些页面显示异常，或者登录后台但前台还是显示未登录状态，大概率是缓存没有正确排除登录用户的请求。在缓存设置里找到**不缓存**选项，确认登录用户、购物车、后台这些路径已经被排除在缓存之外。如果改了网站内容但前台还是显示旧内容，手动清一下缓存，在 WordPress 后台顶部工具栏找到 LiteSpeed Cache 的清除缓存按钮点一下就行。

LiteSpeed Cache 跟 OpenLiteSpeed 的组合是目前 WordPress 建站性价比比较高的方案，服务器资源占用低、缓存效果好，适合流量不大但对速度有要求的个人博客或者小型网站。
