# AGENTS.md

本文件给在这个仓库里工作的 AI 代理（Claude Code 等）看。

## 通用规则

- **语言**：所有回复、提交信息、文章内容一律使用简体中文（代码、命令、路径、专有名词保持原样）。
- **开工前先拉取**：每次开始工作前，先 `git pull origin main`（或 `git fetch origin main` 后确认本地不落后），再动手改文件。仓库有 GitHub Actions 和手机端（Termux）提交，远端经常比本地新。
- **提交身份**：提交邮箱用 `freedomdengyong@outlook.com`，用户名 `ziyouhua`（与仓库历史一致）。提交前确认 `git config user.email` 是这个值。
- **不用会丢改动的命令**：禁止 `git reset --hard`、`git checkout -- .` / `git restore .`（对未提交改动）、`git clean -fd`、`git push --force`、`git stash drop`、`rm -rf` 目录等。需要回退时用 `git revert`，需要整理时先问用户。覆盖或删除文件前先看一眼目标内容。
- 只在用户明确要求时才提交、推送、建 PR；推送到 `main` 会触发线上部署。

## 仓库是什么

Hexo 7 静态博客，站点 **https://vpsjq.com**（VPS 技巧与 Linux 运维笔记），GitHub 仓库 `libertydengyong/myhexo`，只有 `main` 一个分支。

## 目录结构

| 路径 | 说明 |
| --- | --- |
| `_config.yml` | Hexo 主配置：`url: https://vpsjq.com`、`language: zh-CN`、`theme: next`、永久链接 `:year/:month/:day/:title/` |
| `_config.next.yml` | NexT 主题的覆盖配置（Gemini 方案、本地搜索等） |
| `themes/next`、`themes/landscape` | 主题；实际使用 `next` |
| `source/_posts/` | 全部文章（约 200 篇 `.md`） |
| `source/_data/` | NexT 的自定义数据（如 `header.njk`） |
| `source/CNAME` | 域名 `vpsjq.com` |
| `source/robots.txt`、`source/images/`、`about/`、`archives/`、`categories/`、`tags/` | 静态资源与页面 |
| `source/vpsjqindexnowkey*.txt` | IndexNow 校验密钥文件，不要删 |
| `scaffolds/` | 新文章/页面/草稿模板 |
| `scripts/auto_excerpt.js` | Hexo 脚本：构建时自动在文章首段后插入 `<!-- more -->` |
| `scripts/indexnow.js` | Hexo 脚本：构建时向 IndexNow 提交 URL |
| `scripts/check_*.py`、`run_daily_check.py` | 死链 / 站内链接 / SEO 健康检查，`python3 scripts/run_daily_check.py` 汇总运行 |
| `patch-search.js` | `npm install` 的 postinstall，给 `hexo-generator-searchdb` 打补丁 |
| `merge_categories.sh`、`print_urls.py`、`realm.sh` 等 | 一次性/辅助脚本，不属于站点构建 |
| `vercel.json` | Vercel 配置：`cleanUrls`、`trailingSlash`、旧链接 301 重定向、缓存头 |
| `vercel.json.bak*`、`rebuild.txt`、`*.txt`（根目录） | 备份/临时文件，勿当作配置使用 |

`.gitignore` 已忽略 `node_modules/`、`public/`、`db.json`、`.deploy_git/` 等，不要提交构建产物。

## 构建与本地预览

```bash
npm install              # 会自动执行 patch-search.js
npx hexo generate        # 等同 npm run build，输出到 public/
npx hexo server          # 本地预览，默认 http://localhost:4000
```

## 部署方式

- 部署平台是 **Vercel**：推送到 `main` 后 Vercel 自动构建（`hexo generate`）并发布到 vpsjq.com。仓库内没有 Vercel 项目 ID 之类的文件，部署设置在 Vercel 后台。
- `.github/workflows/indexnow.yml`：推送到 `main` 后，等待 90 秒（让 Vercel 部署生效），再在 Actions 里 `npm install && npx hexo generate`，由 `scripts/indexnow.js` 向 IndexNow 提交新链接。

## 写文章约定

- 文章放 `source/_posts/`，文件名多为英文 slug 或 `YYYY-MM-DD-NNN.md`。
- Front-matter 参考 `scaffolds/post.md` 和现有文章：`title`、`date`、`categories`、`tags`、`description`（现有文章常带 `abbrlink`，不要随意改动，它决定链接）。
- 修改已发布文章的标题/日期/永久链接会改变 URL；如必须改，同步在 `vercel.json` 的 `redirects` 里加 301。
- 近期文章的提交风格：`新增文章：<主题>，依据<来源>，未实测部分均注明`。内容要写明依据来源，未实测/未核对的部分如实标注，不要编造命令输出。
- 分类请用现有分类（可看 `source/_posts` 里已有的 `categories`），避免新增近义分类。

## 提交前自查

1. `git pull` 后工作区干净、无冲突。
2. `npx hexo generate` 能通过（有改文章或配置时）。
3. 没有把 `public/`、`node_modules/`、密钥或 `credentials.json` / `token.json` 加进提交。
4. 提交信息为简体中文，邮箱正确。
