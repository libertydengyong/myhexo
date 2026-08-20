import os, re

post_dir = "source/_posts"

title_updates = {
    "81.md": "WordPress 插件 Slim SEO 自动设置 Meta 标签",
    "ssh-remote-host-identification-changed.md": "解决 SSH 报错 Host Identification Changed"
}

for filename, new_title in title_updates.items():
    filepath = os.path.join(post_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"^title:\s*.*$", f'title: {new_title}', content, flags=re.MULTILINE)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已修正: {filename} -> {new_title}")

