#!/usr/bin/env python3
"""
check_dead_links.py —— 全站死链/坏图检查工具（vpsjq.com / Hexo博客）

用途：
    1. 站内链接（内链）——确认每一条链接指向的文章真实存在，兼容3种写法：
       标准Markdown `[text](url)`、HTML `<a href="...">`、Hexo自带的
       `{% post_link 文件名 %}` 标签。
    2. 站外链接（外链）——实际发一次HTTP请求，确认外部网站没有变成404/
       host not found，超时或5xx也计入问题（但5xx额外标注，因为有可能是
       对方临时抖动，不一定是真的坏链，见下方"历史教训"）。
    3. 图片——正文里 `![alt](/images/xxx.webp)` 引用的文件是否真实存在于
       source/images/ 目录下。

不调用AI，纯规则+HTTP请求，可以放心设成每天定时跑。

用法：在仓库根目录下执行
    python3 scripts/check_dead_links.py

======================== 历史教训，务必读完再改这个脚本 ========================
2026年9月的人工排查里踩过这些坑，写脚本时已经避开，以后改动时不要漏掉：

1. 【日期/大小写手滑】文章的URL由 `permalink: :year/:month/:day/:title/`
   规则决定，即 front matter 的 date 字段（年月日部分）+ 文件名拼出来。
   人工写内链时很容易把日期抄错1-2天、或者大小写打错（比如该用
   "S-UI-中转落地" 却写成 "s-ui中转落地"），这类链接肉眼很难看出来，
   必须靠程序精确比对文件名和真实permalink，不能只看"看起来像不像"。

2. 【24:00:00非法时间】少数文章 date 字段被手滑写成 `2026-08-28 24:00:00`
   这种非法时间，Hexo会把它进位到次日00:00:00再生成真实URL。计算permalink
   时必须处理这个进位，否则会把这类文章自己的真实URL都算错，产生连锁误判。

3. 【查询参数/锚点】内链有时会带 `?highlight=xxx` 这种查询参数，比对前
   必须先去掉查询参数和#锚点，否则会把明明存在的链接误判成死链。

4. 【5xx/403/429不等于真死链】外部网站偶尔会有几秒到几分钟的临时性抖动，
   返回500不代表链接真的坏了（人工验证过ping0.cc就出现过这种情况，几分钟
   后自己恢复了）。另外接码/短信验证类网站(smspool.net等)对机房/VPS IP
   经常有反爬拦截，返回403是在防自动化请求，不是页面真的没了（同样是
   实测踩过的坑）。5xx、403、429这几种状态码统一归到"需要关注"而不是
   直接判定为死链，避免每天跑cron都对着同一个其实没坏的外部网站瞎报警。
================================================================================
"""
import glob
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timedelta

POSTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source", "_posts")
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "source", "images")
DOMAIN = "vpsjq.com"

RED = "\033[1;31m"
YELLOW = "\033[1;33m"
GREEN = "\033[1;32m"
BOLD = "\033[1m"
RESET = "\033[0m"


def load_posts():
    """返回 {url_path: filename}，同时处理date字段非法时间(>=24点)进位的情况"""
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
        posts[f"{dt.year}/{dt.month:02d}/{dt.day:02d}/{slug}/"] = fn
    return posts


def normalize_url(link):
    link = link.strip()
    if link.startswith(f"https://{DOMAIN}/"):
        link = link[len(f"https://{DOMAIN}/"):]
    elif link.startswith(f"http://{DOMAIN}/"):
        link = link[len(f"http://{DOMAIN}/"):]
    elif link.startswith("/"):
        link = link[1:]
    else:
        return None
    link = link.split("?")[0].split("#")[0]
    try:
        link = urllib.parse.unquote(link)
    except Exception:
        pass
    if not link.endswith("/"):
        link += "/"
    return link


def check_internal_links(posts):
    """检查每篇文章里的站内链接是否都指向真实存在的文章"""
    broken = []  # (来源文件, 原始链接文本)
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        body = re.sub(r"<script.*?</script>", "", content, flags=re.S)

        links = re.findall(r"\]\(([^)]+)\)", body)
        links += re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\']', body)

        for link in links:
            if DOMAIN not in link and not re.match(r"^/\d{4}/", link):
                continue  # 不是本站链接，跳过（外链另外单独检查）
            norm = normalize_url(link)
            if norm and norm not in posts:
                broken.append((fn, link))

        for slug in re.findall(r"\{%\s*post_link\s+(\S+)", body):
            target = f"{slug}.md"
            if not os.path.isfile(os.path.join(POSTS_DIR, target)):
                broken.append((fn, f"{{%% post_link {slug} %%}}"))

    return broken


def check_images():
    """检查正文里引用的图片文件是否真实存在"""
    missing = []
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", content):
            ref = m.group(1).strip()
            if not ref.startswith("/images/"):
                continue
            local_path = os.path.join(os.path.dirname(IMAGES_DIR), ref.lstrip("/"))
            if not os.path.isfile(local_path):
                missing.append((fn, ref))
    return missing


def collect_external_links():
    """收集全站所有外部链接及其来源文件，去重（同一个外链多篇文章引用只测一次）"""
    ext_links = {}  # url -> [来源文件, ...]
    for path in sorted(glob.glob(os.path.join(POSTS_DIR, "*.md"))):
        fn = os.path.basename(path)
        content = open(path, encoding="utf-8", errors="ignore").read()
        body = re.sub(r"<script.*?</script>", "", content, flags=re.S)
        for m in re.finditer(r"\]\((https?://[^)]+)\)", body):
            url = m.group(1).strip()
            if DOMAIN in url:
                continue
            ext_links.setdefault(url, []).append(fn)
    return ext_links


UNCERTAIN_CODES = {403, 429}  # 反爬拦截/限流常见状态码，不代表链接真的死了


def check_external_links(ext_links, timeout=8):
    """逐个发HTTP请求确认外部链接是否还活着"""
    dead = []       # (url, 来源文件列表, 错误信息) —— 比较有把握的真死链
    uncertain = []  # 5xx/403/429，单独归类，不直接判死
    req_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }
    for url, sources in ext_links.items():
        try:
            req = urllib.request.Request(url, headers=req_headers, method="HEAD")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            dead.append((url, sources, str(e)))
            continue

        if code >= 500 or code in UNCERTAIN_CODES:
            uncertain.append((url, sources, code))
        elif code >= 400:
            dead.append((url, sources, f"HTTP {code}"))
    return dead, uncertain


def main():
    posts = load_posts()
    print(f"共扫描文章: {len(posts)} 篇\n")

    internal_broken = check_internal_links(posts)
    missing_images = check_images()
    ext_links = collect_external_links()
    ext_dead, ext_server_err = check_external_links(ext_links)

    # ---- 摘要 ----
    print(f"{BOLD}📋 摘要{RESET}")
    print("-" * 50)
    items = [
        ("站内死链", internal_broken, RED),
        ("坏图（引用但文件不存在）", missing_images, RED),
        ("外部链接失效(404/host not found/超时等)", ext_dead, RED),
        ("外部链接返回5xx/403/429(可能是反爬拦截或临时抖动，需关注但不一定是坏链)", ext_server_err, YELLOW),
    ]
    for name, data, color in items:
        if data:
            mark = "❌" if color == RED else "⚠️ "
            print(f"  {color}{mark} {name}: {len(data)} 处{RESET}")
        else:
            print(f"  {GREEN}✅ {name}: 0 处{RESET}")
    print("-" * 50 + "\n")

    # ---- 详情 ----
    print(f"{BOLD}📖 详细结果{RESET}")
    print("=" * 50)

    print(f"\n1. 站内死链（共检查 {len(posts)} 篇文章里的内链）")
    if internal_broken:
        print(f"   {RED}{len(internal_broken)} 处{RESET}")
        for fn, link in internal_broken:
            print(f"   - {fn}  ->  {link}")
    else:
        print(f"   {GREEN}✅ 全部正常{RESET}")

    print(f"\n2. 坏图")
    if missing_images:
        print(f"   {RED}{len(missing_images)} 处{RESET}")
        for fn, ref in missing_images:
            print(f"   - {fn}  ->  {ref}")
    else:
        print(f"   {GREEN}✅ 全部正常{RESET}")

    print(f"\n3. 外部链接（共 {len(ext_links)} 个不重复的外部URL）")
    if ext_dead:
        print(f"   {RED}失效 {len(ext_dead)} 个{RESET}")
        for url, sources, err in ext_dead:
            print(f"   - {url}  [{err}]")
            print(f"     来源: {', '.join(sources[:3])}{' 等' if len(sources) > 3 else ''}")
    else:
        print(f"   {GREEN}✅ 没有发现失效的外部链接{RESET}")
    if ext_server_err:
        print(f"   {YELLOW}5xx/403/429（需关注，可能是反爬拦截或临时抖动）{len(ext_server_err)} 个{RESET}")
        for url, sources, code in ext_server_err:
            print(f"   - {url}  [HTTP {code}]")

    print("\n" + "=" * 50)

    return 1 if (internal_broken or missing_images or ext_dead) else 0


if __name__ == "__main__":
    sys.exit(main())
