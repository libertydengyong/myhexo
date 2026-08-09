#!/data/data/com.termux/files/usr/bin/bash
# Hexo 分类精确合并脚本（基于 vpsjq.com 实际分类数据定制）
# 用法：把本文件放到 myhexo 目录下，然后：
#   chmod +x merge_categories.sh
#   ./merge_categories.sh --dry-run   # 先预览，不修改文件
#   ./merge_categories.sh             # 确认无误后正式执行

set -e

POSTS_DIR="source/_posts"
DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
  DRY_RUN=true
fi

if [ ! -d "$POSTS_DIR" ]; then
  echo "找不到 $POSTS_DIR，请确认在 myhexo 目录下运行本脚本"
  exit 1
fi

echo "===== 合并前统计 ====="
grep -A 2 "^categories:" "$POSTS_DIR"/*.md | grep "  - " | sed 's/.*- //' | sort | uniq -c | sort -rn

if [ "$DRY_RUN" = true ]; then
  echo ""
  echo "===== 以下是将要执行的替换规则（预览，未修改文件） ====="
  echo "工具 / x-ui / 一键安装 OpenLiteSpeed        -> vps工具"
  echo "vps优化 / vps一键优化 / vps中转 / S-UI / S-UI中转 -> vps技巧"
  echo "wordpress主题与插件 / 免费wordpress主题 / wp优化 / wp主题 / wp / wordpress主题 -> WordPress"
  echo "IPv6家宽 / IPv6-only / IPv6 only / VPS IPv6 / (多余空格)IPv6 -> IPv6"
  echo ""
  echo "确认无误后运行: ./merge_categories.sh"
  exit 0
fi

echo ""
echo "===== 开始合并，正在修改 $POSTS_DIR 下的 .md 文件 ====="

find "$POSTS_DIR" -name "*.md" -print0 | xargs -0 sed -i -E \
  -e 's/^( *- *)工具 *$/\1vps工具/' \
  -e 's/^( *- *)x-ui *$/\1vps工具/' \
  -e 's/^( *- *)一键安装 OpenLiteSpeed *$/\1vps工具/' \
  -e 's/^( *- *)vps优化 *$/\1vps技巧/' \
  -e 's/^( *- *)vps一键优化 *$/\1vps技巧/' \
  -e 's/^( *- *)vps中转 *$/\1vps技巧/' \
  -e 's/^( *- *)S-UI中转 *$/\1vps技巧/' \
  -e 's/^( *- *)S-UI *$/\1vps技巧/' \
  -e 's/^( *- *)wordpress主题与插件 *$/\1WordPress/' \
  -e 's/^( *- *)免费wordpress主题 *$/\1WordPress/' \
  -e 's/^( *- *)wp优化 *$/\1WordPress/' \
  -e 's/^( *- *)wp主题 *$/\1WordPress/' \
  -e 's/^( *- *)wordpress主题 *$/\1WordPress/' \
  -e 's/^( *- *)wp *$/\1WordPress/' \
  -e 's/^( *- *)IPv6家宽 *$/\1IPv6/' \
  -e 's/^( *- *)IPv6-only *$/\1IPv6/' \
  -e 's/^( *- *)IPv6 only *$/\1IPv6/' \
  -e 's/^( *- *)VPS IPv6 *$/\1IPv6/' \
  -e 's/^( *- *) +IPv6 *$/\1IPv6/'

echo ""
echo "===== 合并后统计 ====="
grep -A 2 "^categories:" "$POSTS_DIR"/*.md | grep "  - " | sed 's/.*- //' | sort | uniq -c | sort -rn

echo ""
echo "合并完成。请检查上方统计结果是否符合预期。"
echo "确认无误后执行："
echo "  npx hexo clean && npx hexo generate"
echo "  git add . && git commit -m '合并分类' && git push"
