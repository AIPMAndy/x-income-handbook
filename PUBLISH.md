# 发布开源仓库（macOS）

目标公开仓库：`https://github.com/AIPMAndy/x-income-handbook`。

## 方式 A：命令行一键发布

准备：安装 GitHub CLI（macOS 可运行 `brew install gh`），然后运行 `gh auth login` 选择 GitHub.com、HTTPS、通过浏览器登录，并确保连接的是 `AIPMAndy`。

解压本项目 ZIP，在终端进入解压后的 `x-income-handbook` 目录，执行：

```bash
bash publish.sh
```

脚本先运行内容检查、41 项 Python 测试和 JS 烟测，再建立**新的**公开仓库、上传源码、尝试启用 GitHub Pages。遇到已存在的仓库会退出，绝不强制覆盖。

## 方式 B：网页创建 + 上传

1. 打开 `https://github.com/new`，使用 `AIPMAndy` 创建 `x-income-handbook` 公开仓库。
2. 将此目录下的**所有文件**（包括隐藏的 `.github` 目录）上传到仓库**根目录**，确保 `index.html` 位于根目录而不是二级目录。
3. `Settings → Pages → Build and deployment → Source` 选择 `GitHub Actions`。
4. `Actions` 中检查 `Validate handbook` 和 `Deploy GitHub Pages` 都成功。
5. 打开 `https://aipmandy.github.io/x-income-handbook/` 验证页面、搜索、资格自检、收益计算器及手机端。
6. `Settings → General → Social preview` 手动上传 `assets/social-preview.png`。

**提醒：** 两种方式都必须由你在已授权的 GitHub 登录环境运行；本文档不代表网站已经上线。
