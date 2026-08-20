import os, re

post_dir = "source/_posts"
target_files = [
    "2026-07-27-001.md",
    "vmesswebsocket搭建中转服务器.md",
    "定期自动清理vps.md"
]

for filename in target_files:
    filepath = os.path.join(post_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 提取 abbrlink、date、title
        abbr = re.search(r"^abbrlink:\s*[\"']?(.*?)[\"']?\s*$", content, re.M)
        date = re.search(r"^date:\s*(.*?)\s*$", content, re.M)
        
        abbr_val = abbr.group(1).strip() if abbr else None
        date_val = date.group(1).strip() if date else "YYYY-MM-DD"
        
        print(f"📄 文件: {filename}")
        if abbr_val:
            print(f"   🔗 对应的 URL (abbrlink): /post/{abbr_val}.html （或 /archives/{abbr_val}.html，取决于 hexo 插件配置）")
        else:
            clean_date = date_val.split(" ")[0].replace("-", "/")
            slug = filename.replace(".md", "")
            print(f"   🔗 默认按日期路径: /{clean_date}/{slug}/")
        print("-" * 50)
