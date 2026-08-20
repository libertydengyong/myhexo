import os, re

# 1. 检查 _config.yml 中的 permalink 结构
config_file = "_config.yml"
permalink = "未找到 permalink"
if os.path.exists(config_file):
    with open(config_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("permalink:"):
                permalink = line.strip()
                break

print("=" * 60)
print(f"⚙️ 你的 Hexo permalink 配置为: {permalink}")
print("=" * 60)

# 2. 读取后两篇文章的真正 Front Matter
target_files = [
    "vmesswebsocket搭建中转服务器.md",
    "定期自动清理vps.md"
]

post_dir = "source/_posts"

for filename in target_files:
    filepath = os.path.join(post_dir, filename)
    print(f"\n📄 文件名: {filename}")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            fm = content.split("---")[1] if "---" in content else "无 Front Matter"
            print("--- Front Matter 内容 ---")
            print(fm.strip())
    else:
        print("❌ 文件不存在！请检查文件名。")
    print("-" * 50)

