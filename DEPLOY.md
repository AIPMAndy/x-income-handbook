# 发布到 GitHub Pages

**仓库拟用名：** `AIPMAndy/x-income-handbook`。本包由本地构建，**截至本次交付尚未创建这个远程仓库**。

1. 登录 [github.com/new](https://github.com/new)，Owner 选择 `AIPMAndy`；Repository name 写 `x-income-handbook`；Visibility 选 Public；创建仓库。
2. 解压 `x-income-handbook.zip`，将 `x-income-handbook/` **内部所有文件和隐藏目录（含 `.github`）** 上传到新仓库根目录，提交到 `main`。
3. 打开 `Settings → Pages`，选择 `Source: GitHub Actions`。
4. GitHub Actions 应运行 `Validate handbook` 与 `Deploy GitHub Pages`；检查均成功后，再访问拟定地址：`https://aipmandy.github.io/x-income-handbook/`。
5. 手动核验：手机、搜索、章节阅读、20 套模板、30 天进度、业务计算器、一键复制微信及官方来源链接。
6. GitHub 仓库 Social preview 不会随提交自动设置：到 `Settings → General → Social preview` 上传 `assets/social-preview.png`。

### 如果仓库被重命名

需修改 `index.html` 的 canonical/og:url、`robots.txt`、`sitemap.xml`、`404.html` 的站点路径与 README 中的仓库链接。

### 安全边界

此站无后端、无账户、不上传读者输入；30 天打卡保存在浏览器本地。商业咨询需另行确认服务条款，不通过 Github Issues 收集敏感身份证明。
