---
title: Termux安装zsh和oh-my-zsh提升命令行体验
date: 2026-08-29 16:00:00
tags:
  - Termux
categories:
  - vps技巧
description: 在Termux里安装zsh和oh-my-zsh的完整步骤，包括自动补全、命令历史这些让命令行操作更高效的功能配置。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "Termux安装zsh和oh-my-zsh提升命令行体验",
      "description": "在Termux里安装zsh和oh-my-zsh的完整步骤，包括自动补全、命令历史这些让命令行操作更高效的功能配置。",
      "datePublished": "2026-08-29T16:00:00+08:00",
      "dateModified": "2026-08-29T16:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/29/termux-zsh/",
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
      "name": "Termux安装zsh和oh-my-zsh",
      "step": [
        {
          "@type": "HowToStep",
          "name": "安装zsh",
          "text": "执行pkg install zsh安装zsh。"
        },
        {
          "@type": "HowToStep",
          "name": "安装oh-my-zsh",
          "text": "运行官方安装脚本sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"，安装过程会自动切换默认shell为zsh，没自动切换的话手动执行chsh -s zsh。"
        },
        {
          "@type": "HowToStep",
          "name": "迁移原有配置",
          "text": "如果之前在bash里配置过别名或环境变量，需要把这些配置从~/.bashrc复制到~/.zshrc，否则在zsh里不会生效。"
        },
        {
          "@type": "HowToStep",
          "name": "按需启用插件",
          "text": "配置文件在~/.zshrc里可以启用更多插件或换主题，常用的比如git（显示当前分支状态）、z（快速跳转常用目录），插件不是装越多越好，装太多会拖慢启动速度。"
        }
      ]
    }
  ]
}
</script>

Termux 默认用的是 bash，够用但体验一般。换成 zsh 加上 oh-my-zsh 之后，自动补全和命令历史这两个功能会明显改善日常操作效率——敲命令的时候 Tab 补全更智能，之前跑过的命令用方向键就能翻出来，不需要重新手打，在手机小键盘上操作 VPS 的时候这两点体验提升很明显。

先安装 zsh：

\`\`\`bash
pkg install zsh
\`\`\`

装完之后安装 oh-my-zsh，这是一个 zsh 的配置框架，内置了大量实用插件和主题：

\`\`\`bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
\`\`\`

安装过程中会自动把默认 shell 切换成 zsh，安装完重启 Termux 就能看到效果。如果没有自动切换，手动设置一下：

\`\`\`bash
chsh -s zsh
\`\`\`

切换成 zsh 之后，最直接能感受到的是 Tab 自动补全变得更智能——输入命令的前几个字母按 Tab，zsh 会列出所有匹配的选项，用方向键选择，不需要完整手打命令名。命令历史同样更好用，按上方向键可以翻出之前跑过的命令，也可以输入部分命令再按上键，只在历史里搜索包含这几个字的命令，在手机键盘上操作的时候省事很多。

oh-my-zsh 安装完之后默认会启用一些插件，如果想进一步自定义，配置文件在 `~/.zshrc`，可以在里面启用更多插件或者换主题。常用的几个插件比如 `git`（显示当前 git 分支状态）、`z`（快速跳转到常用目录）都可以在配置文件里加上。不过插件不是装越多越好，装太多启动速度会变慢，挑几个真正用得上的就行。

如果之前在 bash 里配置过一些别名或者环境变量，切换到 zsh 之后需要把这些配置从 `~/.bashrc` 复制到 `~/.zshrc`，否则这些配置在 zsh 里不会生效。

用 Termux 管理 VPS 的时候，zsh 的自动补全对 SSH 命令特别有用，服务器地址和用户名都可以补全，不需要每次手打完整命令。关于用 Termux 连接和管理 VPS 的完整流程可以参考[Termux手机管理VPS教程](https://vpsjq.com/2026/08/02/termux-vps-remote-manage/)，如果遇到 SSH 断线问题可以看[Termux SSH连接VPS断线怎么办](https://vpsjq.com/2026/08/03/termux-ssh-disconnect/)。
