# AI-READONLY: Personal AI Archive

跨 AI、跨设备的个人记忆源。纯 Markdown、UTF-8、相对链接；GitHub 是唯一事实来源，AI 平台内的记忆是副本。

**公开仓库：禁止上传账号凭据、私人对话原文、公司内部资料、客户/候选人资料和第三方个人信息。** 初始版本只有模板，没有导入过去两年的私人档案。

## 从这里开始

1. AI 首先阅读 [START-HERE.md](START-HERE.md) 与 [AGENTS.md](AGENTS.md)。
2. 本人填写 [身份](identity/profile.md)、[目标](identity/goals.md) 和 [工作偏好](workflow/preferences.md)；`{{占位符}}` 不是事实。
3. 其他平台按 [AI 接入指南](ai-integration.md) 读取，每个会话先刷新，不假定自动长期记忆。
4. 任务完成后将可公开的新经验作为 PR 写入 [候选记忆](memory/inbox.md)。

## 目录

| 目录 | 内容 | 默认更新方式 |
| --- | --- | --- |
| [identity/](identity/README.md) | 身份、职业、标签、目标、原则 | 本人明确指示后通过 PR |
| [workflow/](workflow/README.md) | 工作习惯、工具、沟通、优先级 | 已确认偏好通过 PR |
| [memory/](memory/README.md) | 候选偏好、经验、决策 | 追加有来源的记录 |
| [skills/](skills/README.md) | 技能、学习、能力缺口 | 有证据的更新 |
| [archive/](archive/README.md) | 历史项目、旧材料、完成任务 | 归档；避免删除 |

## 运维

- [安全与版本保护](SECURITY.md)
- [历史信息导入方法](docs/import-guide.md)
- [恢复操作说明](docs/recovery.md)
- [搭建状态与交付报告](docs/setup-report.md)

本地校验：`python3 scripts/validate.py`。发布：`python3 scripts/publish.py`（需要已登录的 GitHub CLI）。

AI 标签是协作约定，不是访问控制；实际写保护依靠 GitHub 权限、主分支保护和 PR。仓库不提供永久无误的隐私过滤或不可删除备份。
