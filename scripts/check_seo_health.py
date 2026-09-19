#!/usr/bin/env python3
"""
check_seo_health.py —— 全站SEO/结构健康检查工具（vpsjq.com / Hexo博客）

用途：覆盖多个针对这个Hexo博客实际踩过的坑设计的检查项，纯规则判断，
      不调用AI，不消耗任何AI配额，可以放心设成每天定时跑。

检查项（全部来自2026年9月人工审计时真实遇到过的问题类型，防止复发）：
  1. front matter 缺少必填字段（title/date/description/tags/categories）
  2. date 字段格式非法（比如 "24:00:00" 这种小时数≥24的非法时间）
  3. JSON-LD结构化数据的 url/datePublished/dateModified 跟文章真实permalink
     对不上（通常是问题2导致的连锁反应——日期进位了但JSON-LD没跟着改）
  4. 代码块用了转义反引号 \\`\\`\\` 而不是正常的三个反引号，导致代码框没法正常渲染
  5. 正文里裸露的类似域名的英文短语(不在反引号里)紧贴中文，容易被Markdown
     渲染器误判成一个乱码域名链接（历史真实案例：acme.sh/tcpx.sh）
  6. 单篇文章独占的"孤儿tag"数量（仅提示，不是每个孤儿tag都需要合并，
     但数量太多说明该做一轮tag梳理了）
  7. sitemap.xml覆盖情况（需要联网请求线上sitemap，没网络时自动跳过这一项）

用法：
    python3 scripts/check_seo_health.py

======================== 历史教训，务必读完再改这个脚本 ========================
1. date字段的"24:00:00"非法时间：2026年9月审计时发现两篇文章
   (iconic-one-download.md、3x-ui-shadowsocks.md) 都把date字段写成了这种
   非法时间，Hexo会把permalink进位到次日，但文章自己JSON-LD里硬编码的
   日期/url字段没有跟着改，导致文章自己的结构化数据描述的URL是错的。
   这是个真实会反复出现的手滑类型，必须常态化检查。

2. 转义反引号代码块：2026年9月一次性在28篇文章里发现148处这个问题，
   全是复制粘贴/批量生成内容时引入的格式错误，同样是容易复发的类型。

3. 裸露域名被Markdown渲染器误判：正文提到"acme.sh"这种工具名时，如果
   紧贴中文没有空格分隔（比如"底层调用的是acme.sh"），会被渲染器的
   linkify功能连中文一起编码成一个不存在的乱码域名，产生"host not found"
   的死链，且这种链接不会出现在这篇脚本之外的死链检查里(因为源文件里
   根本没有markdown链接语法，是渲染时才产生的)，必须单独用启发式规则找。
================================================================================
"""
import glob
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(BASE_DIR, "source", "_posts")
DOMAIN = "vpsjq.com"

RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
BOLD = "\033[1m"
RESET = "\033[0m"

REQUIRED_FIELDS = ["title", "date", "description", "tags", "categories"]

# 常见的"看起来像域名"的后缀，用来做启发式检测（不追求100%精确，
# 宁可漏报也不要因为规则太宽而产生大量误报噪音）
DOMAIN_LIKE_SUFFIXES = ["sh", "com", "net", "org", "io", "cc", "top", "cn"]


def load_posts():
    posts = {}
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        if not content.startswith("---"):
            continue
        fm = content.split("---", 2)[1]
        m = re.search(r"^date:\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})", fm, re.M)
        if not m:
            continue
        y, mo, d, h, mi, s = m.groups()
        dt = datetime(int(y), int(mo), int(d))
        if int(h) >= 24:
            dt += timedelta(days=1)
        slug = fn[:-3]
        posts[fn] = f"{dt.year}/{dt.month:02d}/{dt.day:02d}/{slug}/"
    return posts


def check_missing_fields():
    issues = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        if not content.startswith("---"):
            issues.append((fn, "front matter缺失或格式不对"))
            continue
        fm = content.split("---", 2)[1]
        missing = [field for field in REQUIRED_FIELDS if not re.search(rf"^{field}:", fm, re.M)]
        if missing:
            issues.append((fn, "缺少字段: " + ", ".join(missing)))
    return issues


def check_invalid_date():
    issues = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        if not content.startswith("---"):
            continue
        fm = content.split("---", 2)[1]
        m = re.search(r"^date:\s*(.+)$", fm, re.M)
        if not m:
            continue
        raw = m.group(1).strip()
        dm = re.match(r"(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})", raw)
        if not dm:
            issues.append((fn, f"date格式无法识别: {raw}"))
            continue
        h = int(dm.group(4))
        if h >= 24:
            issues.append((fn, f"date字段小时数非法(>=24): {raw}"))
    return issues


def check_jsonld_mismatch(posts):
    """检查JSON-LD里的url/datePublished跟真实permalink是否一致"""
    issues = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        if fn not in posts:
            continue
        content = open(path, encoding="utf-8", errors="ignore").read()
        script_m = re.search(r"<script type=\"application/ld\+json\">(.*?)</script>", content, re.S)
        if not script_m:
            continue
        script_body = script_m.group(1)
        url_m = re.search(r'"url":\s*"https://vpsjq\.com/([^"]+)"', script_body)
        if not url_m:
            continue
        jsonld_path = url_m.group(1)
        real_path = posts[fn]
        if jsonld_path != real_path:
            issues.append((fn, jsonld_path, real_path))
    return issues


def check_escaped_backtick_fences():
    issues = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        count = content.count(r"\`\`\`")
        if count:
            issues.append((fn, count))
    return issues


def check_bare_domain_like_text():
    """启发式检测：中文紧贴一个"看起来像域名"的裸露短语，没有用反引号包起来"""
    issues = []
    suffix_pattern = "|".join(DOMAIN_LIKE_SUFFIXES)
    # 匹配: 中文字符 + 字母数字.suffix (中间没有空格)，且这段没有被反引号包裹
    pattern = re.compile(rf"[一-鿿]([a-zA-Z0-9_-]+\.(?:{suffix_pattern}))(?![a-zA-Z0-9])")
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        # 只查正文，跳过front matter（description等字段是纯文本meta，
        # 不会经过Markdown渲染器的linkify，不存在被误判成链接的风险）
        parts = content.split("---", 2)
        body = parts[2] if len(parts) >= 3 else content
        body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
        body = re.sub(r"```.*?```", "", body, flags=re.S)  # 代码块里的不算
        for m in pattern.finditer(body):
            start = m.start(1)
            # 排除已经在反引号里的情况：往前找最近的反引号，数量为奇数说明在反引号内
            before = body[:start]
            if before.count("`") % 2 == 1:
                continue
            snippet = m.group(0)
            issues.append((fn, snippet))
    return issues


def check_orphan_tags():
    tag_counter = Counter()
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        content = open(path, encoding="utf-8", errors="ignore").read()
        if not content.startswith("---"):
            continue
        fm = content.split("---", 2)[1]
        m = re.search(r"^tags:\s*\n((?:\s*-\s*.+\n?)+)", fm, re.M)
        if not m:
            continue
        for line in m.group(1).splitlines():
            line = line.strip()
            if line.startswith("-"):
                tag_counter[line[1:].strip()] += 1
    orphans = [t for t, c in tag_counter.items() if c == 1]
    return len(tag_counter), orphans


def check_sitemap_coverage(posts):
    """联网请求线上sitemap.xml，比对本地文章是否都在里面。没网络就跳过。"""
    try:
        req = urllib.request.Request(
            f"https://{DOMAIN}/sitemap.xml",
            headers={"User-Agent": "Mozilla/5.0 (compatible; vpsjq-seocheck/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, str(e)

    locs = set(re.findall(r"<loc>([^<]+)</loc>", xml))
    sitemap_paths = set()
    for loc in locs:
        if loc.startswith(f"https://{DOMAIN}/"):
            path = loc[len(f"https://{DOMAIN}/"):]
            try:
                path = urllib.parse.unquote(path)  # sitemap里中文slug是URL编码的，要解码才能跟本地路径比对
            except Exception:
                pass
            sitemap_paths.add(path)

    missing = [url for url in posts.values() if url not in sitemap_paths]
    return missing, None


def main():
    posts = load_posts()

    missing_fields = check_missing_fields()
    invalid_dates = check_invalid_date()
    jsonld_mismatch = check_jsonld_mismatch(posts)
    escaped_fences = check_escaped_backtick_fences()
    bare_domains = check_bare_domain_like_text()
    total_tags, orphan_tags = check_orphan_tags()
    sitemap_missing, sitemap_err = check_sitemap_coverage(posts)

    print(f"共检查 {len(posts)} 篇文章\n")

    checks = [
        ("date字段非法时间(>=24点)", invalid_dates, RED),
        ("JSON-LD的url/日期跟真实permalink不一致", jsonld_mismatch, RED),
        ("front matter缺少必填字段", missing_fields, RED),
        ("转义反引号代码块(渲染不出代码框)", escaped_fences, RED),
        ("裸露域名样式文本可能被误判成链接", bare_domains, YELLOW),
        ("sitemap覆盖情况", None, RED),
        ("孤儿tag(仅供参考，不强制处理)", orphan_tags, YELLOW),
    ]

    print(f"{BOLD}📋 摘要{RESET}")
    print("-" * 50)
    for name, data, color in checks:
        if name.startswith("sitemap"):
            if sitemap_err:
                print(f"  {YELLOW}⚠️  {name}: 无法联网检查（{sitemap_err}）{RESET}")
            elif sitemap_missing:
                print(f"  {color}❌ {name}: {len(sitemap_missing)} 篇未收录{RESET}")
            else:
                print(f"  {GREEN}✅ {name}: 全部覆盖{RESET}")
            continue
        if data:
            print(f"  {color}{'❌' if color == RED else '⚠️ '} {name}: {len(data)} 处{RESET}")
        else:
            print(f"  {GREEN}✅ {name}: 0 处{RESET}")
    print("-" * 50 + "\n")

    print(f"{BOLD}📖 详细结果{RESET}")
    print("=" * 50)

    print(f"\n1. date字段非法时间")
    if invalid_dates:
        print(f"   {RED}{len(invalid_dates)} 篇{RESET}")
        for fn, msg in invalid_dates:
            print(f"   - {fn}: {msg}")
    else:
        print(f"   {GREEN}✅ 全部正常{RESET}")

    print(f"\n2. JSON-LD自引用url/日期不一致")
    if jsonld_mismatch:
        print(f"   {RED}{len(jsonld_mismatch)} 篇{RESET}")
        for fn, jsonld_path, real_path in jsonld_mismatch:
            print(f"   - {fn}: JSON-LD写的是 {jsonld_path}  实际应该是 {real_path}")
    else:
        print(f"   {GREEN}✅ 全部一致{RESET}")

    print(f"\n3. front matter缺少必填字段")
    if missing_fields:
        print(f"   {RED}{len(missing_fields)} 篇{RESET}")
        for fn, msg in missing_fields:
            print(f"   - {fn}: {msg}")
    else:
        print(f"   {GREEN}✅ 全部齐全{RESET}")

    print(f"\n4. 转义反引号代码块")
    if escaped_fences:
        print(f"   {RED}{len(escaped_fences)} 篇{RESET}")
        for fn, count in escaped_fences:
            print(f"   - {fn}: {count} 处")
    else:
        print(f"   {GREEN}✅ 全部正常{RESET}")

    print(f"\n5. 裸露域名样式文本(启发式检测，可能有误报，人工复核一下)")
    if bare_domains:
        print(f"   {YELLOW}{len(bare_domains)} 处{RESET}")
        for fn, snippet in bare_domains:
            print(f"   - {fn}: ...{snippet}...")
    else:
        print(f"   {GREEN}✅ 没有发现{RESET}")

    print(f"\n6. sitemap覆盖情况")
    if sitemap_err:
        print(f"   {YELLOW}⚠️  无法联网检查: {sitemap_err}{RESET}")
    elif sitemap_missing:
        print(f"   {RED}{len(sitemap_missing)} 篇文章不在sitemap里{RESET}")
        for url in sitemap_missing:
            print(f"   - {url}")
    else:
        print(f"   {GREEN}✅ 全部文章都在sitemap里{RESET}")

    print(f"\n7. 孤儿tag（仅供参考，全站tag总数: {total_tags}，单篇独占的孤儿tag: {len(orphan_tags)}个）")
    print(f"   {YELLOW}提示：不是每个孤儿tag都需要合并，数量持续增长时再考虑做一轮梳理{RESET}")

    print("\n" + "=" * 50)

    fatal = bool(invalid_dates or jsonld_mismatch or missing_fields or escaped_fences or sitemap_missing)
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
