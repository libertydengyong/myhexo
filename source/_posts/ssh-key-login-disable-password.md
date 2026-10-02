---
title: VPS怎么配置SSH密钥登录？关闭密码登录之前，先做这几步防锁死
date: 2026-10-02 16:00:00
tags:
  - SSH
  - 密钥登录
categories:
  - vps技巧
description: 给VPS配置SSH密钥登录并关闭密码登录，步骤不难，难的是不把自己锁在门外。这篇从生成密钥、上传公钥讲到修改sshd配置，重点是改完先用第二个窗口验证，以及sshd_config.d目录里的配置为什么会让你的修改不生效。
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "BlogPosting",
      "headline": "VPS怎么配置SSH密钥登录？关闭密码登录之前，先做这几步防锁死",
      "description": "给VPS配置SSH密钥登录并关闭密码登录，步骤不难，难的是不把自己锁在门外。这篇从生成密钥、上传公钥讲到修改sshd配置，重点是改完先用第二个窗口验证，以及sshd_config.d目录里的配置为什么会让你的修改不生效。",
      "datePublished": "2026-10-02T16:00:00+08:00",
      "dateModified": "2026-10-02T16:00:00+08:00",
      "url": "https://vpsjq.com/2026/10/02/ssh-key-login-disable-password/",
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
      "name": "配置VPS的SSH密钥登录并关闭密码登录",
      "step": [
        {
          "@type": "HowToStep",
          "name": "在本地生成密钥对",
          "text": "在自己的电脑或手机上执行ssh-keygen -t ed25519，得到私钥和以.pub结尾的公钥，私钥不要发给任何人，也不要上传到服务器。"
        },
        {
          "@type": "HowToStep",
          "name": "把公钥放到服务器上",
          "text": "用ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 端口 用户@服务器IP上传公钥，或者手动把公钥内容追加到服务器上的~/.ssh/authorized_keys。"
        },
        {
          "@type": "HowToStep",
          "name": "新开一个窗口验证密钥能登录",
          "text": "保持原来的SSH窗口不要关，另开一个终端用密钥登录，成功之后才继续下一步。"
        },
        {
          "@type": "HowToStep",
          "name": "修改sshd配置并检查语法",
          "text": "把PasswordAuthentication设为no，同时检查sshd_config.d目录里有没有覆盖它的配置，用sshd -t检查语法，再用sshd -T确认最终生效的值。"
        },
        {
          "@type": "HowToStep",
          "name": "重载服务并再开新窗口测试",
          "text": "执行systemctl reload ssh（部分系统服务名是sshd），再另开一个窗口确认密钥登录正常、密码登录被拒绝，确认之后才关闭原窗口。"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "关闭SSH密码登录之前必须做什么？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "先确认密钥登录已经在另一个窗口成功过，并且保留一个已经登录的原窗口作为后路。改完配置后用sshd -t检查语法、重载服务，再新开窗口测试，确认能登录之后才关掉原窗口。如果服务商有网页版控制台(VNC)，也先确认自己能进去，它是最后的救命通道。"
          }
        },
        {
          "@type": "Question",
          "name": "我把PasswordAuthentication改成了no，为什么还能用密码登录？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "常见原因有两个：一是配置没有重载；二是sshd对同一个选项取第一次出现的值，如果主配置文件里Include了sshd_config.d目录，而那里面的文件先设置了yes，你在后面写的no就不会生效。用sshd -T | grep -i passwordauthentication可以看到最终生效的值。"
          }
        },
        {
          "@type": "Question",
          "name": "ssh-copy-id不能用或者提示被拒绝怎么办？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "ssh-copy-id本质上是用密码登录后把公钥追加到服务器的authorized_keys，所以服务器必须还允许密码登录。如果已经关闭了密码登录，就需要通过服务商的网页控制台登录，手动把公钥内容追加到~/.ssh/authorized_keys，并注意目录和文件的权限。"
          }
        }
      ]
    }
  ]
}
</script>

很多教程会告诉你"VPS 装好之后第一件事是关掉密码登录，改用密钥"，这个建议没错，密钥登录确实能挡掉绝大部分暴力破解。但这个操作有个特点：**做对了没有任何感觉，做错了直接把自己锁在服务器外面**。所以这篇的重点不在命令本身，而在每一步怎么留后路。如果你想一次性做完加固，可以看[一键初始化和 SSH 加固脚本](https://vpsjq.com/2025/12/12/linux-一键初始化-ssh-加固脚本/)，不过关闭密码登录这一步，我建议还是手动做一遍，知道它改了什么。

## 第一步：在本地生成密钥

密钥要在**你自己的电脑或手机**上生成，不是在服务器上。Termux、Mac、Linux 和新版 Windows 自带的终端都可以：

```bash
ssh-keygen -t ed25519 -C "my-vps"
```

提示保存位置直接回车，默认会放在 `~/.ssh/id_ed25519`。接下来会问你要不要设置 passphrase（私钥口令），设置的话，私钥就算被人拿走也不能直接用，更安全；不设置就是空口令，用起来方便，这个按自己的习惯选。

生成后有两个文件：

- `id_ed25519`：**私钥**，不能发给任何人，不能上传到服务器。
- `id_ed25519.pub`：**公钥**，放到服务器上的就是它。

`ed25519` 是目前 OpenSSH 默认推荐的类型，生成的公钥比较短，兼容性也够用；个别很老的系统不支持的话，才需要换成 RSA。

## 第二步：把公钥放到服务器上

最省事的是 `ssh-copy-id`：

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub -p 22 root@你的服务器IP
```

端口要写你服务器实际的 SSH 端口，不是默认 22 的话一定要改。它会先用密码登录，再把公钥追加到服务器的 `~/.ssh/authorized_keys`，所以**这一步服务器必须还允许密码登录**，这也是为什么要先配密钥、后关密码。

没有 `ssh-copy-id`（比如 Windows）的话，手动做也一样：

```bash
# 在服务器上执行
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "这里粘贴 id_ed25519.pub 的整行内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

`authorized_keys` 里一行就是一把公钥，所以可以放多把，手机、电脑各一把。**用 `>>` 追加，不要用 `>`**，否则会把已有的公钥覆盖掉。

## 第三步：先新开一个窗口验证

这一步不能省：**保持当前这个已登录的 SSH 窗口不要关**，另外再开一个终端：

```bash
ssh -i ~/.ssh/id_ed25519 -p 22 root@你的服务器IP
```

如果没有要求输入服务器密码（设了 passphrase 的话会让你输入私钥口令，那是正常的），直接登录进去了，说明密钥已经好使。登不进去就先别往下走，回到上一步检查公钥有没有粘贴完整、权限是不是对的。

想确认是不是真的走了密钥，可以加 `-v` 看过程，里面会出现 `Authentication succeeded (publickey)`。

## 第四步：关闭密码登录

编辑 SSH 服务端配置：

```bash
nano /etc/ssh/sshd_config
```

把这一项改成：

```
PasswordAuthentication no
```

另外还有一项 `KbdInteractiveAuthentication`（旧版本叫 `ChallengeResponseAuthentication`），它是"键盘交互"认证方式，在启用了 PAM 的系统上，它有可能成为密码登录的另一个入口。想彻底只留密钥，也把它设成 `no`：

```
KbdInteractiveAuthentication no
```

### 坑：sshd_config.d 里的配置会让你的修改不生效

新一点的 Debian、Ubuntu 默认会在主配置文件开头写一行：

```
Include /etc/ssh/sshd_config.d/*.conf
```

意思是先读这个目录里的配置文件。而 sshd 有一条规则：**同一个选项出现多次时，取第一次出现的值**。所以如果这个目录里某个文件已经写了 `PasswordAuthentication yes`，你在主文件后面写的 `no` 就会被无视。云服务商的镜像里，常常会放这样一个文件来保证你能用密码登录。

我在本机用临时配置试了一下，这个行为是确定的：同样两行，`yes` 写在前面，最终生效的就是 `yes`；`Include` 的文件里写 `no`、主文件里写 `yes`，最终也是 `no`。

所以改完之后不要凭感觉，先看看有没有这类文件，再让 sshd 自己告诉你最终生效的值：

```bash
ls /etc/ssh/sshd_config.d/
grep -ri "PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/
sshd -T | grep -i "passwordauthentication\|kbdinteractiveauthentication"
```

`sshd -T` 打印的是 sshd 合并所有配置之后真正会用的值，以它为准。如果发现是目录里某个文件在覆盖，就去改那个文件，或者把那一行也改成 `no`。

## 第五步：检查语法、重载、再验证

先检查配置有没有写错，语法错误会让 sshd 重载时失败，甚至起不来：

```bash
sshd -t
```

没有任何输出就是没问题。然后重载服务：

```bash
systemctl reload ssh
```

Debian 和 Ubuntu 的服务名是 `ssh`，CentOS、Rocky 等系统通常是 `sshd`，报 `Unit not found` 就换另一个。`reload` 只是重新读配置，已经建立的连接不会断，这正是后路所在。

重载之后，**再新开一个窗口**测试两件事：

1. 密钥登录依然正常。
2. 强制用密码登录会被拒绝：

```bash
ssh -o PubkeyAuthentication=no -p 22 root@你的服务器IP
```

提示 `Permission denied (publickey)` 就说明密码登录已经关了。两个都符合预期，才可以关掉最开始那个窗口。

## 如果已经把自己锁在外面了

先别急着重装系统，按这个顺序试：

1. **原窗口还没关**：赶紧在里面把 `PasswordAuthentication` 改回 `yes`，`sshd -t` 后 reload。
2. **用服务商的网页控制台（VNC/Console）登录**：绝大多数 VPS 商家的后台都有，它不走 SSH，是最后的救命通道。进去之后改配置、重新放公钥就行。所以**关密码登录之前，先确认自己能进这个控制台**，部分服务商的控制台需要账户密码或者面板里单独设置的 root 密码。
3. **公钥放错、权限不对**：`~/.ssh` 目录应该是 700，`authorized_keys` 是 600，而且这两个都不能是别的用户的、对其他人可写的，否则 sshd 可能会拒绝使用它们。
4. **SSH 端口改过**：改了端口的话，检查防火墙和服务商安全组有没有放行新端口，参考[SSH 连接很慢](https://vpsjq.com/2026/08/15/ssh-connection-slow/)里的排查思路，以及[Termux SSH 断线](https://vpsjq.com/2026/08/03/termux-ssh-disconnect/)里手机端的注意事项。

## 补充两个常见疑问

**只关密码登录够不够安全？** 它挡的是暴力破解，对一般的扫描攻击足够有效，但不是万能的。私钥丢了或者泄露，别人一样能进，所以私钥不要乱传，换设备时用 passphrase 保护。想再加一层，可以搭配改端口、限制 root 直接登录、装 fail2ban，具体做法见[Linux 一键初始化和 SSH 加固脚本](https://vpsjq.com/2025/12/12/linux-一键初始化-ssh-加固脚本/)里的说明。

**主机指纹变了怎么办？** 换了服务器或者重装系统后，本地会提示"远程主机身份验证已更改"，那跟密钥登录无关，是本机记录的服务器指纹对不上，处理方法看[这篇](https://vpsjq.com/2026/08/15/ssh-remote-host-identification-changed/)。
