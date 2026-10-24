# X 赚钱保姆级攻略 · 2026

> 从 0 开始经营 X（Twitter）：七条变现路径、26 章系统教程、24 套模板、30 天行动计划、互动业务收益/时间成本测算。

**作者**：AI 酋长 Andy｜官网 [metaver.vip](https://metaver.vip/)｜微信：`AIPMAndy`  
**政策核验日期**：2026-10-24｜**许可证**：MIT（代码与原创文字，见版权说明）

## 先看结论

X 的「曝光」不是「到账」。如果你擅长解决问题，优先验证**咨询/陪跑或数字产品**；有开发能力的可以验证 SaaS；能持续提供原创内容且符合全部资格时，再考虑**官方原创奖励与创作者订阅**。

**关键变更**：X 旧版 `Creator Revenue Sharing` 于 **2026-09-07** 停止；新版 `Original Content Rewards` 对最近 90 天内至少 **500,000 次来自认证用户的 Home Timeline 曝光（回复不计入门槛）**、**500 位认证粉丝**、付费套餐、年龄、地区、原创性、账号状态等有要求。提交申请也不保证批准。**中国大陆目前不在官方公布的新版奖励适用地区列表中**（列表列有香港和台湾）；以实际资格与最新名单为准。新版合格曝光定义更严格，不能拿个人主页的「总曝光」乘虚构单价。见 [X 原创奖励官方政策](https://help.x.com/en/using-x/original-content-rewards)。

## 包含什么

| 资源 | 数量 | 说明 |
|---|---:|---|
| 变现路线 | 7 | 咨询、数字产品、AI/SaaS、联盟、商单、订阅、原创奖励 |
| 系统教程 | 26 | 每章包含场景演练、逐步操作、完成标准、失败处理、交付物及来源 |
| 实操模板 | 24 | 英文帖子、Thread、服务卡、商单 Media Kit、合同检查、收益复盘、CSV 等 |
| 30 天计划 | 30 | 每天一个动作，进度仅保存在浏览器本地 |
| 计算器 | 1 | 业务收入的**假设模型**，不预测 X 平台奖励 |
| 官方参考 | 9 | X 帮助中心 / FTC，定期人工核验 |

## 零门槛使用

1. 打开 `index.html`，无需 Node.js 或数据库，网站核心交互离线可用。
2. 用搜索框找章节、点开阅读、勾选 30 天任务、在工具箱调整收入参数。
3. `chapters/` 是可单独阅读和引用的 Markdown 文档。
4. `templates/` 是可编辑的 `.md` / `.csv` 文件。
5. 微信号 `AIPMAndy` 和 [官网](https://metaver.vip/) 已在网站导航与服务区提供。

## 本地开发

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000
python3 scripts/check.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
node scripts/smoke_dom.cjs # 在无浏览器运行环境下验证 JS 初始化及核心输出
```

直接打开 `index.html` 也可以，因为章节数据在 `data/content.js` 中，未依赖外部 API。

## 验证边界与测试

- 内容同步检查、Python 单元测试和 JavaScript 无浏览器运行时检查已通过。
- `scripts/browser_smoke.py` 提供点击、弹窗、资格检查及视觉截图的真实浏览器验收脚本，但**本次执行环境的浏览器禁止访问本地地址和 file URL，未获得有效新版截图**。部署后需在能访问本地网页的环境里执行。
- 因未创建远程仓库，本次更新不会自动出现在 GitHub Pages；请先完成部署，再测手机端和分享预览。

## 一键开源发布

本项目新增 `publish.sh`：在已经安装并登录 GitHub CLI 的 macOS/Linux 电脑上，解压后进入项目根目录执行 `bash publish.sh`，会先验证代码，再创建公开仓库并推送。它不会覆盖已存在仓库。详见 [PUBLISH.md](PUBLISH.md)。

## GitHub Pages 部署

目标仓库名：`AIPMAndy/x-income-handbook`（请先实际创建；文档中的目标地址不代表已经上线）。

1. 在 GitHub 新建 **Public** 仓库 `x-income-handbook`（也可自行换名，换名后要同步 HTML canonical / sitemap 里的链接）。
2. 把**本压缩包中的文件和目录上传到仓库根目录**，推送到 `main`。
3. 进入仓库 `Settings → Pages → Build and deployment → Source`，选择 **GitHub Actions**。
4. 打开 `Actions` 查看 `Deploy GitHub Pages`，等运行成功。
5. 访问拟定地址 `https://aipmandy.github.io/x-income-handbook/`，验证手机版、章节弹窗与模板下载。
6. 如需在仓库右侧展示社交分享图：`Settings → General → Social preview` 手动上传 `assets/social-preview.png`。

**说明**：仓库创建、Pages 设置与外部网站是否上线，需要在 GitHub 实际操作和检查后才能确认。当前压缩包并不代表仓库已创建。

## 目录

```text
index.html                    交互网站
assets/style.css              流动玻璃 + 响应式样式
assets/app.js                 章节搜索、路线、计算器、打卡
assets/favicon.svg            网站标识
assets/social-preview.png     可手动上传到 GitHub 的社交预览图
data/content.json             唯一内容主数据（维护来源）
data/content.js               由 JSON 生成的静态脚本
data/templates.js            模板索引
chapters/01.md ... 26.md      26 篇 Markdown 手册
templates/                    24 套编辑模板
research/sources.md           官方规则与核验日期
research/red-team.md          对抗式审核与风险清单
scripts/check.py              结构/内容/链接基础校验
scripts/test_content.py       单元测试
.github/workflows/ci.yml      持续集成
.github/workflows/pages.yml   GitHub Pages 自动部署
LICENSE                       MIT
```

## 维护内容

编辑 `data/content.json` 后，运行：

```bash
python3 scripts/sync.py
python3 scripts/check.py
```

`sync.py` 会同步 `data/content.js` 与 26 篇章节文件，避免在线网站和 Markdown 内容不一致。

## V2 对抗式审核与升级

- 针对原版“讲概念多、操作证据少”：26 章新增具体场景、分步实操、验收标准和卡住后的调整方案。
- 原创奖励和 Subscriptions **严格分离**：另外附上两套申请资格对照表 `templates/22-policy-check-matrix.md`。
- 补充 14 天首单验证实验、双语示范、失败时的停/改策略；不以泛流量当商业结果。
- 网站增加本地原创奖励资格自检、零单概率、税前每小时贡献指标；不收集/上传用户输入。移动端增加快捷导航，章节全文搜索包含实操案例。
- 修正商单品类警告：金融、加密货币等属于 Paid Partnerships 明确禁止推广的品类。
- 详细问答与修复证据见 `research/adversarial-dialogue.md`。

## 原则和限制

- 不提供虚假地址、假身份、代实名、刷量、群发、绕开平台地区限制的操作。
- 不承诺涨粉或收入；工具中的数字是场景假设，并非业绩案例。
- 所有费用、资格、区域、支付方法都可能更新，优先查官方最新文档。
- 转载第三方图片、界面截图、他人内容须遵守相应版权；MIT 只适用本仓库拥有版权的原创作品，不覆盖引用资料、外部商标或 X 官方内容。
- 不构成税务、投资、法律或财务专业意见。

## 参与贡献

欢迎 Issue / Pull Request 修正文档。规则更新请附**原始官方链接、核验日期和变更前后差异**；案例必须附可核验证据且保护客户隐私；不要提交营销垃圾内容。

---

**作者**：AI 酋长 Andy｜[metaver.vip](https://metaver.vip/)｜微信：**AIPMAndy**
