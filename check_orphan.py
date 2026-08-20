import os
import re

POSTS_DIR = 'source/_posts'

def parse_simple_fm(content):
    """纯正则解析 YAML Front Matter（无需 yaml 库）"""
    fm_dict = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            # 提取 categories
            cat_match = re.search(r'^categories:\s*(.*)$', fm_text, re.MULTILINE)
            if cat_match:
                cat_val = cat_match.group(1).strip()
                if cat_val and cat_val != '[]':
                    fm_dict['categories'] = [cat_val]
            
            # 提取 tags
            tag_match = re.search(r'^tags:\s*(.*)$', fm_text, re.MULTILINE)
            if tag_match:
                tag_val = tag_match.group(1).strip()
                if tag_val and tag_val != '[]':
                    fm_dict['tags'] = [tag_val]

            # 提取 abbrlink
            abbr_match = re.search(r'^abbrlink:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
            if abbr_match:
                fm_dict['abbrlink'] = abbr_match.group(1).strip()

            return fm_dict, parts[2]
    return {}, content

def find_orphan_pages():
    if not os.path.exists(POSTS_DIR):
        print(f"❌ 找不到目录: {POSTS_DIR}")
        return

    files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    
    no_cat_or_tag = []
    incoming_links = {f: 0 for f in files}
    abbrlink_map = {}

    # 第一遍：解析 Front Matter
    for f in files:
        filepath = os.path.join(POSTS_DIR, f)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            fm, _ = parse_simple_fm(content)
            
            categories = fm.get('categories', [])
            tags = fm.get('tags', [])
            abbrlink = str(fm.get('abbrlink', '')).strip()

            if abbrlink:
                abbrlink_map[abbrlink] = f
            
            # 检查既没有分类也没有标签的情况
            if not categories and not tags:
                no_cat_or_tag.append(f)

    # 第二遍：检查文章互链
    for f in files:
        filepath = os.path.join(POSTS_DIR, f)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            links = re.findall(r'\]\(([^)]+)\)', content)
            for link in links:
                for abbr, target_file in abbrlink_map.items():
                    if abbr and abbr in link and target_file != f:
                        incoming_links[target_file] += 1
                for target_file in files:
                    clean_name = target_file.replace('.md', '')
                    if clean_name and clean_name in link and target_file != f:
                        incoming_links[target_file] += 1

    print("=" * 60)
    print("🔍 全站孤儿页面排查结果")
    print("=" * 60)

    print("\n📌 【类型 1】未配置分类(Categories)且未配置标签(Tags)的文章：")
    if no_cat_or_tag:
        for f in no_cat_or_tag:
            print(f"  - {f}")
    else:
        print("  ✅ 完美！所有文章均已配置分类或标签。")

    print("\n📌 【类型 2】无正文内链指向的文章：")
    no_incoming = [f for f, count in incoming_links.items() if count == 0]
    if no_incoming:
        print(f"  (共有 {len(no_incoming)} 篇文章未在其他文章正文中被显式引用)：")
        for f in no_incoming[:15]:
            print(f"  - {f}")
        if len(no_incoming) > 15:
            print(f"  ...等共 {len(no_incoming)} 篇")
    else:
        print("  ✅ 完美！所有文章在正文中均存在互链。")

if __name__ == '__main__':
    find_orphan_pages()
