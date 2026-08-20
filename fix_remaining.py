import os, re

post_dir = "source/_posts"

# 精简后的标题（不带多余双引号）
title_updates = {
    "2026-07-23-002.md": "DMIT VPS IPv6 连接失败与服务访问排查记录",
    "81.md": "Slim SEO 插件：自动添加 WordPress Meta 标签与描述",
    "linux-ulimit-not-working.md": "ulimit 设上限仍报 Too many open files 排查",
    "ssh-remote-host-identification-changed.md": "SSH 报错 REMOTE HOST IDENTIFICATION 解决办法"
}

for filename, new_title in title_updates.items():
    filepath = os.path.join(post_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 精准替换 title 字段（不留外部引号）
        content = re.sub(r"^title:\s*.*$", f'title: {new_title}', content, flags=re.MULTILINE)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已精简: {filename} -> {new_title}")

