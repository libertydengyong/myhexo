---
title: SSH 加快连接的几种方法
tags:
  - SSH 加快连接
id: '147'
categories:
  - vps技巧
description: SSH 加快连接的几种方法：使用SSH密钥认证，取消DNS反向解析，配置SSH客户端连接复用，优化连接超时设置，取消GSSAPI认证，使用Mosh。
abbrlink: 40921
date: 2025-07-14 12:26:57
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "SSH 加快连接的几种方法",
      "description": "SSH 加快连接的几种方法：使用SSH密钥认证，取消DNS反向解析，配置SSH客户端连接复用，优化连接超时设置，取消GSSAPI认证，使用Mosh。",
      "datePublished": "2025-07-14T12:26:57+08:00",
      "dateModified": "2025-07-14T12:26:57+08:00",
      "url": "https://vpsjq.com/2025/07/14/ssh-加快连接的几种方法/",
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
          "name": "为什么SSH连接总是很慢？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "常见原因是服务器默认开着DNS反向解析和GSSAPI认证，这两者在大多数场景下用不上却会拖慢连接，在sshd_config里关掉UseDNS和GSSAPIAuthentication通常能明显改善。"
          }
        },
        {
          "@type": "Question",
          "name": "ControlMaster连接复用是怎么加速的？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "第一次SSH连接建立后，后续的scp、sftp或再次ssh连接会直接复用已建立的通道，不用重新走一遍认证握手，在~/.ssh/config里配置Host * 加ControlMaster auto、ControlPath、ControlPersist即可开启。"
          }
        },
        {
          "@type": "Question",
          "name": "一键优化脚本执行前需要注意什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "脚本里的PasswordAuthentication no和PermitRootLogin no会关闭密码登录和root直接登录，执行前必须确认已经配置好密钥登录，不然可能把自己锁在门外连不上服务器。"
          }
        }
      ]
    }
  ]
}
</script>

SSH 加快连接的几种方法：

**方法一：使用SSH密钥认证（最推荐）**

原理：密钥认证比密码认证快，不需要在每次连接时传输密码。

**方法二：取消DNS反向解析（服务器端 sshd_config）**

原理：SSH服务器接收连接时，默认会尝试反向解析客户端的IP地址到域名，如果客户端IP没有对应的PTR记录，或者DNS解析慢，会拖慢连接速度。这个方法是在服务器端 `/etc/ssh/sshd_config` 中配置，但效果体现在客户端连接速度上：

```
sudo nano /etc/ssh/sshd_config
```

修改为 `UseDNS no`，如果前面有 `#`，把它删掉。

**方法三：配置SSH客户端连接复用（ControlMaster）**

原理：允许在同一个SSH会话上重复使用多个连接。第一次连接后，后续的连接（如scp、sftp或再次ssh）会直接通过已建立的通道，不用重新认证握手，速度极快。在本地电脑或Termux的 `~/.ssh/config` 文件（权限必须是600）中添加：

```
Host *
  ControlMaster auto
  ControlPath ~/.ssh/cm_socket/%r@%h:%p
  ControlPersist 600s
```

`ControlPersist 600s` 表示保持主连接活跃600秒。

**方法四：优化连接超时设置（客户端config）**

原理：减少SSH客户端等待服务器响应的时间。在 `~/.ssh/config` 中添加：

```
Host *
  ConnectTimeout 10
  ServerAliveInterval 60
  ServerAliveCountMax 3
```

`ConnectTimeout 10` 表示连接超时10秒；`ServerAliveInterval 60` 表示每60秒发送一次保活消息；`ServerAliveCountMax 3` 表示最多发送3次保活消息未响应则断开。

**方法五：指定认证方式优先级（客户端config）**

原理：强制SSH客户端优先尝试指定的认证方式，避免浪费时间尝试不适用的认证方式。在 `~/.ssh/config` 中添加（如果需要密码登录）：

```
Host *
  PreferredAuthentications publickey,keyboard-interactive,password
```

通常情况下，如果设置了密钥，SSH会优先尝试密钥认证。

**方法六：取消GSSAPI认证**

原理：GSSAPI认证（如Kerberos）在某些环境下会尝试很长时间，导致连接缓慢。在服务器端 `/etc/ssh/sshd_config` 中设置：

```
GSSAPIAuthentication no
```

保存并重启SSH服务。

**方法七：使用Mosh**

Mosh专门针对网络不稳定的场景设计，网络切换或者信号不好的时候比普通SSH更抗断线。

**一键优化脚本**

把上面几个服务器端配置项打包成一条命令，直接在服务器上跑：

```bash
sed -i '/^#UseDNS/d' /etc/ssh/sshd_config && echo 'UseDNS no' >> /etc/ssh/sshd_config && \
sed -i '/^#GSSAPIAuthentication/d' /etc/ssh/sshd_config && echo 'GSSAPIAuthentication no' >> /etc/ssh/sshd_config && \
sed -i '/^#PermitRootLogin/d' /etc/ssh/sshd_config && echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && \
sed -i '/^#PasswordAuthentication/d' /etc/ssh/sshd_config && echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config && \
sed -i '/^#ClientAliveInterval/d' /etc/ssh/sshd_config && echo 'ClientAliveInterval 300' >> /etc/ssh/sshd_config && \
sed -i '/^#ClientAliveCountMax/d' /etc/ssh/sshd_config && echo 'ClientAliveCountMax 2' >> /etc/ssh/sshd_config && \
sed -i '/^#TCPKeepAlive/d' /etc/ssh/sshd_config && echo 'TCPKeepAlive no' >> /etc/ssh/sshd_config && \
echo -e "\n✅ SSH配置已优化，重启服务即可生效：" && \
systemctl restart sshd
```

说明：`UseDNS no` 取消DNS反向解析，加快连接速度；`GSSAPIAuthentication no` 禁用GSSAPI，避免Kerberos卡顿；`PermitRootLogin no` 禁止root直接登录，提升安全性；`PasswordAuthentication no` 强制使用密钥登录；`ClientAliveInterval 300` 每5分钟检测一次连接；`ClientAliveCountMax 2` 超过约10分钟无响应自动断开；`TCPKeepAlive no` 关闭TCP层面的保活探测，不影响中间人攻击防护，这个选项和安全性无关，纯粹是连接层面的设置。

**注意：这条一键命令里 `PasswordAuthentication no` 和 `PermitRootLogin no` 会关闭密码登录和root直接登录，执行前请确认已经配置好密钥登录，不然可能把自己锁在门外连不上服务器。**

相关内容

[一行代码部署极简、开源的网页版 SSH 管理](https://vpsjq.com/2025/07/28/一行代码部署极简、开源的网页版-ssh-管理/)

[Linux 一键初始化 & SSH 加固脚本](https://vpsjq.com/2025/12/12/linux-一键初始化-ssh-加固脚本/)

[一键root加改密码脚本](https://vpsjq.com/2025/12/31/一键root加改密码脚本/)
