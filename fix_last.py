import os, re

filepath = "source/_posts/ssh-remote-host-identification-changed.md"
new_title = "解决 SSH 远程主机身份验证更改报错"

if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"^title:\s*.*$", f'title: {new_title}', content, flags=re.MULTILINE)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已修正: {new_title}")
