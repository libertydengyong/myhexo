import os, re

post_dir = "source/_posts"

# 优化后的精准标题映射表
title_updates = {
    "68.md": "x-ui甬哥版默认解锁ChatGPT配置指南",
    "一行代码部署极简、开源的网页版-ssh-管理.md": "一行代码部署极简开源网页版 SSH 管理工具",
    "dd命令大集合.md": "Linux dd 命令实用指南：磁盘镜像、DD重装与性能测试",
    "一键优化tcp.md": "Linux VPS 一键优化 TCP 网络性能与 BBR 加速脚本",
    "linux-ulimit-not-working.md": "ulimit 已设上限仍报 Too many open files 错误排查",
    "ssh-remote-host-identification-changed.md": "SSH 报错 REMOTE HOST IDENTIFICATION HAS CHANGED 解决方案"
}

for filename, new_title in title_updates.items():
    filepath = os.path.join(post_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 替换 title 字段
        content = re.sub(r"^title:\s*.*$", f'title: "{new_title}"', content, flags=re.MULTILINE)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已成功更新标题: {filename} -> {new_title}")
    else:
        print(f"❌ 未找到文件: {filename}")

