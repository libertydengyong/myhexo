import os, re
from collections import defaultdict

post_dir = "source/_posts"
titles = []

for root, _, files in os.walk(post_dir):
    for file in sorted(files):
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r"^title:\s*[\"']?(.*?)[\"']?\s*$", content, flags=re.MULTILINE)
            if match:
                t = match.group(1).strip()
                titles.append((file, t))

print("=== 1. 标题结尾异常字符/格式问题 ===")
for file, t in titles:
    if t.endswith(":") or t.endswith("：") or t.startswith("\\_") or t.startswith("_"):
        print(f"❌ [{file}]: {t}")

print("\n=== 2. 标题过短 (< 8个字) ===")
for file, t in titles:
    if len(t) < 8:
        print(f"⚠️ [{file}] ({len(t)}字): {t}")

print("\n=== 3. 标题过长 (> 35个字) ===")
for file, t in titles:
    if len(t) > 35:
        print(f"⚠️ [{file}] ({len(t)}字): {t}")

print("\n=== 4. 重复或极度相似标题检查 ===")
seen = defaultdict(list)
for file, t in titles:
    clean_t = re.sub(r"[^\w\a-zA-Z0-9\u4e00-\u9fa5]", "", t).lower()
    seen[clean_t].append((file, t))

for clean_t, group in seen.items():
    if len(group) > 1:
        print("🚨 发现潜在重复文章/标题:")
        for g in group:
            print(f"   - {g[0]}: {g[1]}")
