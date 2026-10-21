# AI-READONLY: 仓库搭建交付报告

- 检查日期：2026-10-21（Asia/Shanghai）
- 目标仓库名：personal-ai-archive
- 仓库地址：尚未创建或验证；等待 GitHub 账号登录后生成真实地址，不填猜测地址。
- 远端保护：尚未开启或验证。
- 历史资料导入：未执行。飞书、ima 未连接；未读取两年 Codex 聊天。

## 已生成的交付内容

- 五个核心目录与身份、目标、工作偏好、工具、任务优先级、候选记忆、经验、决策、技能、学习计划和项目归档模板。
- 所有 Markdown 首行带 AI-READONLY 或 AI-WRITABLE 标签；明确 {{占位符}} 不代表事实。
- START-HERE、AGENTS、CLAUDE、GEMINI 入口与跨 AI GitHub API 读取、PR 写回协议。
- 自动结构/标签/链接/明显敏感模式校验；公开内容仍需实际审阅。
- 发布脚本创建公开仓库、推送提交、设置并核验 main 分支保护。
- 手动 Actions 内容恢复 PR 与本地完整历史快照恢复脚本。

## 快速使用

本人先填写 identity/profile.md、identity/goals.md 与 workflow/preferences.md，并标为 confirmed。AI 启动时先读取 START-HERE.md 与 AGENTS.md，再按任务加载。详细路径、启动提示词与 API 示例见 [接入指南](../ai-integration.md)。新经验先追加 [候选箱](../memory/inbox.md)；通过 PR 校验与审阅再进入 main。

## 发布前置条件

需要已登录且具备本人仓库管理权限的 GitHub CLI。执行 `python3 scripts/validate.py` 后，将已审阅文件提交到独立 Git 仓库，再执行 `python3 scripts/publish.py`。若 gh 未在 PATH 中，可用 PERSONAL_ARCHIVE_GH 指定官方 CLI 可执行文件绝对路径。发布脚本报错时可能已有部分远端步骤完成，须查询实际状态；不能据文件存在就判断远端生效。

## 尚未完成的外部连接

ChatGPT、Claude、Gemini 需要各平台可用连接器/工具与授权；本包未替用户创建这些连接。Meta Muse、OpenAI Dots 的准确产品与可用接口未核实，未配置自动同步。GitHub 登录也不会授权飞书或 ima。完整私有资料不适合直接发布到公开仓库，见 [历史资料导入方法](import-guide.md)。

## 验收记录

本地验收已实际执行并通过：

- `python3 scripts/validate.py`：目录、AI 标签、UTF-8、相对链接与明显敏感模式检查通过。
- 三个 Python 脚本编译检查通过。
- `python3 tests/verify.py` 临时独立 Git 仓库测试：完整快照树相等；新增文件被移除、删除文件被恢复；main 保持原提交；非法 SHA 被拒绝；与被忽略的本地私密文件冲突时拒绝恢复而不覆盖。
- 五目录恢复测试通过；错误标签、断链、模拟令牌与符号链接反例均被校验器拒绝。
- GitHub 工作流仅完成本地语法核验；未在远端 Actions 实际运行。

远端 API、保护设置、CI 状态与跨平台实际读取仍待 GitHub 登录及平台连接后核验。本报告不把尚未完成的远端操作标为成功。
