# 网站SEO与内容维护工作总结（截至2026-09-12）

本文档涵盖两个站点：`surveypayoutwatch.com`（本地路径 `~/paidsurvey`）和 `vpsjq.com`（本地路径 `~/myhexo`，Hexo博客）。所有改动均已通过 `git commit` + `git push` 提交，可用 `git log` 查看完整历史。

---

## 一、surveypayoutwatch.com 已完成的改动

### 1. 全站技术修复
- **www/非www域名规范化**：Vercel已设置www→非www的301跳转；`generate_sitemap.py`脚本的`BASE_URL`常量已修正为非www；全站149个HTML文件的canonical/schema/og标签批量替换为非www格式
- **`vercel.json`重定向修复**：`best-sweepstakes-sites.html`的301目标路径从错误的`/dispute-log.html`改为`/dispute-log/index.html`，字段统一为`permanent: true`
- **robots.txt**：已确认屏蔽两个backup目录（`dispute-log/backup-template-upgrade/`、`backup-template-upgrade-2/`），不影响索引

### 2. 内容语义缺口修复（基于GSC查询词+keywordtool.io核实）
- **Canada页面**：标题补充"cash"语义（原漏掉这个词导致CTR低）
- **UK页面**：标题拓宽覆盖头部词、补H2结构、FAQ schema与正文同步、平台从6扩到11个（新增PrizeRebel/PaidViewpoint/Qmee/Five Surveys/Askable）
- **Australia页面**：平台从6扩到11个（新增PaidViewpoint/YSense/Earnably/Qmee/Five Surveys）；新增税务FAQ（基于ATO官方指导，明确非税务建议）
- **Swagbucks系列**：
  - `swagbucks-account-suspended-banned.html`：新增"suspended vs deactivated"说明、年龄门槛FAQ（13岁注册门槛 vs PayPal提现18岁门槛的区分）
  - `swagbucks-registration-error.html`：新增"account already exists"措辞覆盖、403 Forbidden错误排查小节
  - `swagbucks-no-verification-email.html`：新增phone verification小节
  - 新建`swagbucks-sb-to-dollars.html`（SB转美元换算指南，100SB≈$1，诚实标注非官方固定汇率）
  - 新建`swagbucks-browser-extension.html`（SwagButton插件指南）
- **Robux系列**：
  - `earn-1000-robux-from-surveys.html`：补充400 Robux参考点（官方最小面额$4.99）；新增Roblox钓鱼骗局警示（"survey.roblox.com"类仿冒问卷，基于安全研究机构记录）
- **MyPoints系列**（5篇孤儿页）：修复metadata污染（og:url/图片路径/FAQ schema错误引用"母版"文章内容）；全部加入`dispute-log/index.html`目录；两篇真孤儿页补充编辑性内链

### 3. 编辑事故修复（与SEO无关的纯质量问题）
- `no-minimum.html`：清除SurveyLama重复内容（正文段落+表格行各一处）
- `payout-ledger.html`：清除H2标题重复
- `surveys-for-teens.html`：修复整段内容缺失（引用了不存在的平台列表），新增4个平台
- `dispute-log/five-surveys-vs-prime-opinion.html`：修复title标签内混入HTML标签的语法错误
- `dispute-log/mypoints-account-suspended-swagbucks.html`：新增分诊引导句，把纯Swagbucks封号流量导向通用指南
- `swagbucks-account-suspended-banned.html`←→其分诊对象已建立双向链接
- `surveys-for-moms.html`：新增Ask Mom平台（垂直定位匹配）

### 4. 本次发现并大幅重写的两篇低质量文章
（这两篇是站外/另一会话产生、本地此前未同步的历史提交，本次会话核实后发现问题）
- **`highest-paying-survey-apps-australia.html`**：原文16个H2小节全是空泛方法论、零具体App推荐。已重写为6个真实核实的平台数据（Swagbucks 4.19★/Qmee 4.3-4.6★/Toluna 4.47★/MyPoints 3.6-4.3★/YSense App Store仅1条评价/Five Surveys 4.5-4.64★），并核实说明**Prolific没有独立App**（官方确认web-only）。同步更新FAQ schema。
- **`surveys-for-cash-australia.html`**：核实后发现内容本身尚可（"site-card"式的比较框架有明确内链指路，不算空心），仅3处"Searches for X, Y, Z"关键词堆砌句式需要改写为自然表达，已修正。**注意**：已排除Cash App相关内容（核实澳洲不支持Cash App，跟Canada同类风险）。

### 5. 全站扫描发现的其他问题
- Blogger编辑器残留链接损坏问题：已确认为孤例，不是系统性问题
- 死链检查：`paid-surveys-australia.html`所有站内链接均正常

### 6. 变现渠道拓展（进行中，未完全跑通）
- **广告联盟**：
  - MyLead：已通过发布者审核（两个网站流量源均获批），但多个具体调查类campaign因"新发布者"限制被拒（Surveys2Cash、Unlock Surveys等），已申请Sweeps Survey/Finance Survey/Profit Survey/Finance Survey Mill这几个低门槛项目，结果未知
  - MaxBounty：注册流程中，已提交身份证件审核
  - Infolinks：已用`surveypayoutwatch.com`重新提交申请（此前用旧博客goodxyz.xyz被拒）
  - 已排除的网络：SpyRevenue（信誉证据不足）、BidVertiser（口碑极差，弹窗恶意广告投诉多）、AdBRT（域名新注册+服务器位于高风险地区）、CrakRevenue/Paysale/GiddyUp/DMS（信誉高但垂直领域不匹配，成人/约会/保险/金融类）
- **推广链接统一**：全站已确认并统一Swagbucks/Qmee/MyPoints/InboxDollars/PaidViewpoint/YSense/Earnably/Five Surveys/PrizeRebel/Freecash/Prime Opinion的推广链接（部分平台如Prolific/Survey Junkie/YouGov/LifePoints/Toluna/AttaPoll/Octopus Group/Pureprofile确认目前无推广计划，维持官网链接）
- **邮件订阅列表**：已注册Kit（免费版，最多1万订阅者），newsletter定位"骗局预警+平台状态更新"（A+B方向）。已在3篇高流量文章（`qmee-no-surveys-shadow-ban.html`、`swagbucks-account-suspended-banned.html`、`paid-surveys-australia.html`）末尾插入Inline订阅表单，配色调整为浅蓝色（`#EFF6FF`）系统统一。**这是方案B（先小范围测试），尚未推广到全站，需要1-2周后查看Kit后台是否有转化再决定。**
- **轮播Banner**：设计完成（Swagbucks/Qmee/InboxDollars/MyPoints/Freecash五平台轮播，7秒间隔，标注"Advertisement"），**但从未真正执行批量插入到全站180个文件这一步，目前只是设计稿，未部署**。

---

## 二、vpsjq.com 已完成的改动

### 1. 内容加固
- `S-UI-中转落地搭建教程.md`：从1166字扩充到1724字，补充端口占用/防火墙排查、访问路径记错场景、访问路径重置说明，新增4条内链
- `专为alpine定制的xray一键脚本.md`：从不到200字扩充到1146字，补充脚本安全预览步骤、Alpine系统OpenRC说明、apk装bash提示（明确排除了无法核实的开机自启命令，未编造内容）
- `2026-04-30-011.md`（3x-ui安装教程）：从820字扩充到1321字，新增访问路径输错场景、4条内链
- `linux-time-wait-port-exhaustion.md`：内容本身已扎实（4069字），仅补充了1条来自`linux-tcp-ip-和-bbr-参数智能优化脚本.md`的反向内链（此前零内链孤立状态）
- `termux-zsh.md`：补充chsh权限报错排查（来自Termux官方GitHub issue）、autosuggestions/syntax-highlighting插件、powerlevel10k主题说明

### 2. 修复的技术/格式错误
- `一键更换为xanmod内核.md`：修复损坏的Blogger编辑器残留链接（3处`wget`/`curl`命令的URL被替换成了`draft.blogger.com`内部编辑页面），同时修复了Markdown链接语法混入shell命令的语法错误，补充Debian/Ubuntu通用性说明。**全站排查确认此问题为孤例，非系统性。**
- `2026-05-08-001.md`（x-ui 2.9.4版）：补上缺失的代码块格式（该文章内容本身已妥善处理"已停更"事实，只是格式缺陷）

### 3. 域名规范化检查
- 已确认vpsjq.com canonical/sitemap全部使用非www格式，配置健康，无需修改（与paidsurveywatch形成对比：Hexo框架统一由`_config.yml`的`url`字段控制，不存在手写HTML导致的批量遗漏风险）

### 4. 命名规范问题（已定性，不回溯修改）
- 发现19篇日期序号命名（如`2026-07-23-003.md`）、十几篇纯数字命名（如`61.md`）的历史遗留文章，全部**不做改名处理**（避免URL变更带来的排名风险），仅作为以后新建文章的规范提醒：新建文章务必用`hexo new "英文slug"`直接指定语义化文件名

---

## 三、方法论与操作规范（供Claude Code参考）

### 长尾词分析流程
1. 从GSC查询词或keywordtool.io导出CSV
2. **先用`grep`核实现有文章是否已覆盖**（避免重复内容），注意同义措辞（如"suspended" vs "deactivated"、"stuck on loading" vs "not loading"）可能已被不同措辞覆盖
3. 需要写入新事实前，**必须web_search核实**，不能凭空断言。核实时注意排除：
   - 同名不同物的混淆（如"SwagBucks"加密货币 vs Swagbucks积分平台）
   - 山寨/仿冒App与官方App的混淆（如假的"Swagbucks" by Zae Tae Apps、埃及本地版"MyPoints"）
   - 基于错误认知的搜索需求（如"Cash App在加拿大/澳洲可用"、"SurveyMonkey能换Robux"均已证伪）
4. 样本量过小（个位数展示、单一变体）不构成独立成篇理由，倾向于补充进现有文章而非新建
5. 涉及未成年人的查询词（10-16岁精确年龄段），原则是**不主动扩大内容对更低龄读者的适配**，但在已有13-18岁框架内做精细化（如"15岁能否参与"这类FAQ）不违反此原则

### Git操作
- 两个仓库都会遇到远程有其他设备/会话产生的未同步提交，push被拒时**先`git pull`（会自动rebase），确认无冲突后再push**，不要强制覆盖
- 多行文本替换优先用Python而非sed（避免行号偏移导致的重复插入等问题），涉及JSON-LD schema必须用`json.loads()`校验格式，不能只看`grep`匹配到文字就当作成功

### 技术细节
- 命令包含markdown三反引号时，用`chr(96) * 3`动态生成，避免破坏聊天界面代码块渲染
- Termux不支持`/tmp`目录，临时文件用`~/tmp/`

---

## 四、下一步待办

1. **观察期**（进行中）：
   - 149文件canonical批量修复后的索引恢复情况（`paid-surveys-for-teens.html`等页面曾出现展示量下降，已排查确认非技术缺陷，可能是正常评估期波动）
   - Kit邮件订阅表单在3篇测试文章上的转化数据（1-2周后查看）
   - 广告联盟审核结果（MyLead低门槛项目、MaxBounty、Infolinks）

2. **待决策**：
   - 是否将Kit订阅表单推广到全站（取决于测试期数据）
   - 是否执行轮播Banner的全站批量插入（设计已完成，未部署）
   - 是否申请AdSense（已讨论，认为是当前阶段性价比最高的展示广告选择，尚未行动）

3. **未处理的低优先级项**：
   - vpsjq.com的19篇日期序号命名+十几篇纯数字命名文章（不改名，仅规范以后新建流程）
   - paidsurveywatch.com teens/14-year-olds页面的进一步流量优化（已确定"负责任优先"方向，不追求扩大适配）
