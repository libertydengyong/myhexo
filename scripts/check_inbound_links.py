#!/usr/bin/env python3
"""
check_inbound_links.py —— 检测 vpsjq.com (Hexo博客) 全站文章的"孤儿页"问题

用法：
    python3 scripts/check_inbound_links.py

思路：
    遍历 source/_posts/*.md 全部文章源文件（不是生成后的HTML——public/是构建产物，
    没有提交进仓库），统计每篇文章被多少篇"其他"文章引用（自己链自己不算），
    找出内链数量为0或很少的孤儿文章。

站点结构说明（写这个脚本前先确认过的实际情况，见 ltjl.txt）：
    - permalink 规则是 :year/:month/:day/:title/，由 front matter 的 date 字段
      （年月日部分）+ 文件名（去掉.md）拼出来，abbrlink 字段虽然存在但未启用。
    - date 字段偶尔会出现 "24:00:00" 这种非法时间，Hexo会把它进位到第二天
      00:00:00 再生成URL，这里同样处理，避免误判成孤儿页。
    - 内链一共有3种写法都要认：标准Markdown `[text](url)`、HTML `<a href="...">`、
      以及Hexo自带的 `{% post_link 文件名 [标题] %}` 标签（按文件名而不是URL匹配）。
    - JSON-LD结构化数据(<script type="application/ld+json">块)里文章会自引用自己的
      url字段，这不是真正的"内链"，统计前要先剔除这部分内容，否则会产生噪音
      （不过因为已排除自引用，实际不影响结果，只是避免混入无意义的模式）。
"""

import glob
import re
import sys
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent.parent / "source" / "_posts"


def load_posts():
    """返回 {url_path: filename}，url_path形如 '2026/08/28/slug/'"""
    posts = {}
    skipped = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8", errors="ignore")
        if not content.startswith("---"):
            skipped.append(path.name)
            continue
        fm = content.split("---", 2)[1]
        m = re.search(
            r"^date:\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})", fm, re.M
        )
        if not m:
            skipped.append(path.name)
            continue
        y, mo, d, h, mi, s = m.groups()
        dt = datetime(int(y), int(mo), int(d))
        if int(h) >= 24:  # 非法时间进位到次日，跟Hexo实际行为保持一致
            dt += timedelta(days=1)
        slug = path.stem
        url_path = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/{slug}/"
        posts[url_path] = path.name
    return posts, skipped


def normalize_url(link):
    """把各种写法的链接归一化成 posts 字典里用的 key 形式，非本站链接返回 None"""
    link = link.strip()
    if link.startswith("https://vpsjq.com/"):
        link = link[len("https://vpsjq.com/"):]
    elif link.startswith("http://vpsjq.com/"):
        link = link[len("http://vpsjq.com/"):]
    elif link.startswith("/"):
        link = link[1:]
    else:
        return None
    link = link.split("?")[0].split("#")[0]  # 去掉查询参数和锚点
    try:
        link = urllib.parse.unquote(link)
    except Exception:
        pass
    if not link.endswith("/"):
        link += "/"
    return link


def extract_links(content):
    """从正文里提取所有候选内链目标：markdown链接 / <a href> / {% post_link %}"""
    # 排除JSON-LD结构化数据块，那里的url是自引用，不算真正的内链
    body = re.sub(r"<script.*?</script>", "", content, flags=re.S)

    urls = []
    for m in re.finditer(r"\]\(([^)]+)\)", body):
        urls.append(("url", m.group(1).strip()))
    for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\']', body):
        urls.append(("url", m.group(1).strip()))

    post_link_slugs = []
    for m in re.finditer(r"\{%\s*post_link\s+(\S+)", body):
        post_link_slugs.append(m.group(1).strip())

    return urls, post_link_slugs


def main():
    posts, skipped = load_posts()
    if skipped:
        print(f"警告：{len(skipped)} 个文件没能解析出date字段，已跳过: {skipped}\n")

    filename_to_url = {fn: url for url, fn in posts.items()}
    inbound = {fn: set() for fn in posts.values()}

    for path in sorted(POSTS_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8", errors="ignore")
        urls, post_link_slugs = extract_links(content)

        for _, link in urls:
            norm = normalize_url(link)
            if norm and norm in posts:
                target = posts[norm]
                if target != path.name:
                    inbound[target].add(path.name)

        for slug in post_link_slugs:
            target = f"{slug}.md"
            if target in filename_to_url and target != path.name:
                inbound[target].add(path.name)

    results = sorted(inbound.items(), key=lambda x: (len(x[1]), x[0]))
    zero = [f for f, s in results if len(s) == 0]
    one = [f for f, s in results if len(s) == 1]

    print(f"文章总数: {len(posts)}")
    print(f"0个站内回链（孤儿页）: {len(zero)}")
    print(f"1个站内回链: {len(one)}")
    print()
    print("--- 0个回链的文章列表 ---")
    for f in zero:
        print(" ", f)
    print()
    print("--- 只有1个回链的文章列表（附来源） ---")
    for f, s in results:
        if len(s) == 1:
            print(f"  {f}  <- {next(iter(s))}")


if __name__ == "__main__":
    sys.exit(main())
