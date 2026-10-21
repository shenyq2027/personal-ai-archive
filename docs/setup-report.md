# AI-READONLY: 仓库搭建交付报告

- 检查日期：2026-10-21（Asia/Shanghai）
- 目标仓库名：personal-ai-archive
- 仓库地址：[shenyq2027/personal-ai-archive](https://github.com/shenyq2027/personal-ai-archive)
- 可见性：public；默认分支 main；已通过 GitHub API 查询核验。
- 远端保护：已核验必须 PR、必须通过 archive-validation、与 main 同步、管理员受规则约束、禁止 force push 与删除 main。单人仓库不要求第二位审核者。
- GitHub Actions：默认只读；已允许恢复工作流创建 PR，只有恢复任务请求必要的写权限。
- 跨平台读取：匿名 GitHub API 已实际返回 HTTP 200 的原始 Markdown。
- 历史资料导入：未执行。飞书、ima 未连接；未读取两年 Codex 聊天。

## 已生成的交付内容

- 五个核心目录与身份、目标、工作偏好、工具、任务优先级、候选记忆、经验、决策、技能、学习计划和项目归档模板。
- 所有 Markdown 首行带 AI-READONLY 或 AI-WRITABLE 标签；明确 {{占位符}} 不代表事实。
- START-HERE、AGENTS、CLAUDE、GEMINI 入口与跨 AI GitHub API 读取、PR 写回协议。
- 自动结构/标签/链接/明显敏感模式校验；公开内容仍需实际审阅。
- 发布脚本创建公开仓库、推送提交、设置并核验 main 分支保护。
- 手动 Actions 内容恢复 PR 与本地完整历史快照恢复脚本。

## 各目录使用说明

| 目录 | 放什么 | 如何更新 |
| --- | --- | --- |
| [identity](../identity/README.md) | 称呼、职业、核心标签、目标、决策原则 | 仅本人明确确认后更新 |
| [workflow](../workflow/README.md) | 工作习惯、工具、沟通偏好与优先级 | 已确认的新规则通过 PR 更新 |
| [memory](../memory/README.md) | 新经验、候选偏好、复盘、重要决策 | 新条目先进 inbox，保留日期和来源 |
| [skills](../skills/README.md) | 技能证据、学习计划、能力缺口 | 以真实成果更新，不自称掌握 |
| [archive](../archive/README.md) | 完成项目、旧文档、结束任务 | 脱敏摘要归档，保留历史引用 |

## 快速使用

本人先填写 identity/profile.md、identity/goals.md 与 workflow/preferences.md，并标为 confirmed。AI 启动时先读取 START-HERE.md 与 AGENTS.md，再按任务加载。详细路径、启动提示词与 API 示例见 [接入指南](../ai-integration.md)。新经验先追加 [候选箱](../memory/inbox.md)；通过 PR 校验与审阅再进入 main。

可直接复制给有 GitHub 读取工具的 AI：

> 请读取 https://api.github.com/repos/shenyq2027/personal-ai-archive/contents/START-HERE.md?ref=main ，使用 Accept: application/vnd.github.raw+json 获取 Markdown。按入口读取 AGENTS.md 和所需身份、工作偏好档案。占位符不是事实，当前本人指令优先。完成任务后，将已确认可公开的新经验按 ai-integration.md 通过 PR 写回；没有写工具时输出补丁并说明尚未写回。

写回不是公开读取附带的权限，必须由该 AI 所在平台具备授权的 Git/GitHub 写工具。另一个设备只需克隆或通过 API 读取此仓库，无需转换格式；不会自动迁移各平台私有记忆库。

## 发布与维护前置条件

需要已登录且具备本人仓库管理权限的 GitHub CLI。执行 `python3 scripts/validate.py` 后，将已审阅文件提交到独立 Git 仓库，再执行 `python3 scripts/publish.py`。若 gh 未在 PATH 中，可用 PERSONAL_ARCHIVE_GH 指定官方 CLI 可执行文件绝对路径。发布脚本报错时可能已有部分远端步骤完成，须查询实际状态；不能据文件存在就判断远端生效。

## 尚未完成的外部连接

ChatGPT、Claude、Gemini 需要各平台可用连接器/工具与授权；本包未替用户创建这些连接。Meta Muse、OpenAI Dots 的准确产品与可用接口未核实，未配置自动同步。GitHub 登录也不会授权飞书或 ima。完整私有资料不适合直接发布到公开仓库，见 [历史资料导入方法](import-guide.md)。

## 验收记录

本地验收已实际执行并通过：

- `python3 scripts/validate.py`：目录、AI 标签、UTF-8、相对链接与明显敏感模式检查通过。
- 三个 Python 脚本编译检查通过。
- `python3 tests/verify.py` 临时独立 Git 仓库测试：完整快照树相等；新增文件被移除、删除文件被恢复；main 保持原提交；非法 SHA 被拒绝；与被忽略的本地私密文件冲突时拒绝恢复而不覆盖。
- 五目录恢复测试通过；错误标签、断链、模拟令牌与符号链接反例均被校验器拒绝。
- GitHub 首次校验工作流 [39558270429](https://github.com/shenyq2027/personal-ai-archive/actions/runs/39558270429)：completed / success，包含结构检查与临时 Git 仓库恢复测试。

- 真实恢复演练：[Restore archive 39558464054](https://github.com/shenyq2027/personal-ai-archive/actions/runs/39558464054) 成功，从初始提交自动创建 [恢复 PR #2](https://github.com/shenyq2027/personal-ai-archive/pull/2)。
- 恢复 PR 的 [archive-validation](https://github.com/shenyq2027/personal-ai-archive/actions/runs/39558487886) 通过，GitHub 返回 mergeStateStatus=CLEAN。演练 PR 已关闭且未合并，当前档案保留。
- GitHub 对 bot 创建的 PR 要求过一次工作流运行批准；批准后检查正常通过。未关闭分支保护或绕过校验。
- [首次交付 PR #1](https://github.com/shenyq2027/personal-ai-archive/pull/1) 已通过校验并合并；说明正常 PR 更新路径已实际验证。

远端仓库、保护、PR 更新、CI、匿名 API 读取和恢复 PR 创建流程已核验。各 AI 平台的实际账号连接与任务结束自动钩子尚未配置，Meta Muse/OpenAI Dots 接口未核实；飞书/ima/两年历史资料未导入。
