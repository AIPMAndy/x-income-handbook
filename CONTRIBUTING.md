# 贡献指南

感谢帮助核查 X 平台规则。请创建 Issue 说明：**原规则引用、最新官方 URL、核验日期、对应章节编号、建议修改**。

接受：政策纠错、原创实操模板、可复现数据集、无个人隐私的案例。

不接受：刷量、批量群发、购买身份、误导性收入截图、搬运与未授权素材、平台风控规避内容。

提交 PR 前运行 `python3 scripts/check.py && python3 -m unittest discover -s scripts -p 'test_*.py' -v`。
