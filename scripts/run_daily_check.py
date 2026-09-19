#!/usr/bin/env python3
"""
run_daily_check.py —— 整合脚本，把3个健康检查一次跑完，生成一份汇总报告

用途：依次运行 check_dead_links.py / check_inbound_links.py /
      check_seo_health.py，把每个脚本自己的"摘要"区块抽出来，按问题严重
      程度（❌先 > ⚠️次 > ✅最后）重新排序，拼成一个总摘要放在报告最上面，
      下面再附上每个脚本的完整详细结果。

用法：
    python3 scripts/run_daily_check.py

配合 crontab 定时跑，把输出重定向到文件即可，比如：
    0 3 * * * cd /root/myhexo && python3 scripts/run_daily_check.py > ~/myhexo_report.txt 2>&1

不调用AI，纯Python脚本+规则判断，不消耗任何AI配额。
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent

CHECKS = [
    ("死链/坏图/外部链接检查", "check_dead_links.py"),
    ("内链孤儿页检查", "check_inbound_links.py"),
    ("SEO/结构健康检查", "check_seo_health.py"),
]

BOLD = "\033[1m"
RESET = "\033[0m"


def run_script(script_name):
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / script_name)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return result.stdout, result.returncode


def extract_summary_lines(output):
    """从脚本输出里抠出"摘要"区块的几行（不含标题和分隔线本身）"""
    lines = output.splitlines()
    in_summary = False
    summary_lines = []
    dash_count = 0
    for line in lines:
        if "📋 摘要" in line:
            in_summary = True
            continue
        if in_summary:
            if line.strip().startswith("---"):
                dash_count += 1
                if dash_count == 2:
                    break
                continue
            if line.strip():
                summary_lines.append(line)
    return summary_lines


def severity_rank(line):
    if "❌" in line:
        return 0
    if "⚠️" in line:
        return 1
    return 2


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{BOLD}vpsjq.com 每日健康检查报告 —— {now}{RESET}")
    print("=" * 60)

    all_summary = []  # (severity, 脚本名, 原始行文本)
    full_outputs = []
    any_fail = False

    for label, script in CHECKS:
        output, code = run_script(script)
        if code != 0:
            any_fail = True
        full_outputs.append((label, output))
        for line in extract_summary_lines(output):
            all_summary.append((severity_rank(line), label, line))

    all_summary.sort(key=lambda x: x[0])

    print(f"\n{BOLD}🔎 总摘要（按问题严重程度排序，❌ > ⚠️  > ✅）{RESET}")
    print("-" * 60)
    current_label = None
    for _, label, line in all_summary:
        if label != current_label:
            print(f"\n  [{label}]")
            current_label = label
        print(f"  {line.strip()}")
    print("\n" + "-" * 60)

    for label, output in full_outputs:
        print(f"\n\n{BOLD}{'#' * 60}{RESET}")
        print(f"{BOLD}# {label}{RESET}")
        print(f"{BOLD}{'#' * 60}{RESET}\n")
        print(output)

    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
