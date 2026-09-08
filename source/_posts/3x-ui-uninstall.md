---
title: 3x-ui卸载方法和数据清理
date: 2026-08-30 14:00:00
tags:
  - 3x-ui
categories:
  - vps工具
description: 3x-ui面板完整卸载步骤，包括卸载命令、手动清理残留数据库文件和卸载前备份建议。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "3x-ui卸载方法和数据清理",
      "description": "3x-ui面板完整卸载步骤，包括卸载命令、手动清理残留数据库文件和卸载前备份建议。",
      "datePublished": "2026-08-30T14:00:00+08:00",
      "dateModified": "2026-08-30T14:00:00+08:00",
      "url": "https://vpsjq.com/2026/08/30/3x-ui-uninstall/",
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
      "name": "3x-ui完整卸载与数据清理",
      "step": [
        {
          "@type": "HowToStep",
          "name": "视情况先备份数据库",
          "text": "如果节点配置还有用或打算迁移到其他服务器，先执行cp /etc/x-ui/x-ui.db /root/x-ui-backup.db备份，数据完全不需要的话可以跳过这步。"
        },
        {
          "@type": "HowToStep",
          "name": "执行卸载命令",
          "text": "执行x-ui uninstall，这会停止面板服务并卸载程序本身，但不会自动删除数据库文件。"
        },
        {
          "@type": "HowToStep",
          "name": "手动清理残留数据",
          "text": "执行rm -rf /etc/x-ui/删除数据库文件和相关配置，删掉之后所有入站节点、用户数据、面板设置都会彻底清除，无法恢复。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "卸载后想重新安装怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "直接跑安装脚本即可，重新安装会生成全新的面板配置，之前的数据不会自动恢复，如果之前有备份数据库文件，可以参考3x-ui面板迁移与备份教程导入恢复。"
          }
        }
      ]
    }
  ]
}
</script>

卸载 3x-ui 只需要一条命令：

\`\`\`bash
x-ui uninstall
\`\`\`

这条命令会停止面板服务并卸载程序本身，但**不会自动删除数据库文件**，配置数据还会留在服务器上。如果想彻底清干净，卸载完之后手动删除数据库文件：

\`\`\`bash
rm -rf /etc/x-ui/
\`\`\`

这个目录里存的是 3x-ui 的数据库文件（x-ui.db）和相关配置，删掉之后所有入站节点、用户数据、面板设置都会彻底清除，无法恢复。

卸载之前要不要备份取决于你的情况。如果这台服务器上的节点配置还有用，或者打算迁移到另一台服务器继续用，建议先备份数据库文件：

\`\`\`bash
cp /etc/x-ui/x-ui.db /root/x-ui-backup.db
\`\`\`

备份完之后再卸载，以后需要恢复的时候参考[3x-ui面板迁移与备份教程](https://vpsjq.com/2026/08/27/3x-ui-backup-migrate/)，把备份文件导入新服务器就行。如果这台服务器上的数据完全不需要了，直接卸载不备份也没问题。

卸载完如果想重新安装，直接跑安装脚本就行，参考[3x-ui安装：MHSanaei版官方脚本与面板配置](https://vpsjq.com/2026/04/30/2026-04-30-011/)，重新安装会生成全新的面板配置，之前的数据不会自动恢复。
