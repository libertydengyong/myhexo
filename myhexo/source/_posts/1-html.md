---
title: css的方式一行代码给wordpress添加面包屑导航
tags:
  - 面包屑导航
id: '118'
categories:
  - - wordpress主题与插件
date: 2025-06-11 20:13:49
---

css的方式一行代码给wordpress添加面包屑导航: 给wordpress的head文件添加: <div class="my-custom-breadcrumbs"><a href="/" title="Home">首页</a> <?php the\_category(","); ?> <span class="current-post-title"><?php the\_title(); ?></span></div> 接下来，登录WordPress后台，导航到外观 > 习惯。点击额外CSS（附加CSS），在文本框中添加以下 CSS 代码： /\* \* 面包屑导航样式 \* 确保在手机上显示并统一颜色 \*/ /\* 定义一个变量来存储链接的蓝色，方便统一管理。 你可以通过检查你网站其他链接的颜色来找到这个蓝色值。 \*/ :root { --my-link-blue: #007bff; /\* 这是一个常见的蓝色，请根据你网站的实际链接颜色调整 \*/ } /\* 针对手机屏幕的媒体查询：确保面包屑显示 \*/ @media screen and (max-width: 768px) { /\* 768px 是一个常见的手机/平板断点，可根据需要调整 \*/ .my-custom-breadcrumbs { /\* 定位到我们的面包屑容器 \*/ display: block !important; /\* 强制显示为块级元素 \*/ visibility: visible !important; /\* 强制可见 \*/ /\* 以下是可选的样式调整，让它在手机上看起来更好： \*/   text-align: left; /\* 左对齐 \*/   padding: 10px 15px; /\* 添加内边距 \*/   font-size: 0.9em; /\* 调整字体大小，使其在小屏幕上更紧凑 \*/   overflow-x: auto; /\* 如果面包屑内容过长，允许水平滚动 \*/   white-space: nowrap; /\* 防止面包屑在小屏幕上换行，保持单行显示 \*/   }   /\* 确保内部元素在行内显示 \*/   .my-custom-breadcrumbs a,   .my-custom-breadcrumbs .current-post-title {   display: inline-block !important; /\* 或者 'inline' \*/   }   }       /\* 统一面包屑内所有文本（包括文章标题）的颜色为链接蓝色 \*/   .my-custom-breadcrumbs a, /\* 链接 \*/   .my-custom-breadcrumbs .current-post-title /\* 当前文章标题 \*/ {   color: var(--my-link-blue) !important; /\* 使用上面定义的蓝色变量，并强制覆盖 \*/   }     点击“发布”按钮保存更改。