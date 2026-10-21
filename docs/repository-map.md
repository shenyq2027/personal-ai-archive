# AI-READONLY: 个人 AI 档案仓库结构图

[返回仓库首页](../README.md) · [查看交付报告](setup-report.md) · [AI 接入指南](../ai-integration.md)

五个核心目录分别回答：**我是谁、怎样协作、过去学到了什么、我会什么、什么已经结束**。其余文件负责 AI 接入、使用说明和版本维护。

## 完整文件树

下面列出截至 2026-10-21 本次更新的全部 35 个受 Git 管理的文件，包含本说明文档。树状图使用纯文本，普通 Markdown 阅读器即可显示。

```text
personal-ai-archive/
├── identity/  # 我是谁：身份、职业、目标与原则
│   ├── README.md  # 身份目录的填写与确认规则
│   ├── goals.md  # 人生目标、价值观和核心决策原则
│   └── profile.md  # 称呼、职业背景、核心标签、语言等
├── workflow/  # 如何与我协作：工作方式与执行规则
│   ├── README.md  # 工作方式目录说明
│   ├── preferences.md  # 沟通风格、回答长度、输出格式和反馈偏好
│   ├── priorities.md  # 任务优先级、自主执行边界与完成标准
│   └── tools.md  # 常用工具、用途与实际接入状态
├── memory/  # 从经历中沉淀：新记忆、经验和决策
│   ├── README.md  # 记忆目录说明
│   ├── decisions.md  # 重要决策、依据及后续复查记录
│   ├── inbox.md  # 新经验与偏好的候选收件箱
│   └── lessons.md  # 可复用的经验与复盘结论
├── skills/  # 我会什么、准备学什么
│   ├── README.md  # 技能目录说明
│   ├── inventory.md  # 已掌握技能、熟练度与成果证据
│   └── learning-plan.md  # 学习计划、练习项目与待提升能力
├── archive/  # 已经结束的项目和历史资料
│   ├── README.md  # 归档目录说明
│   └── project-template.md  # 历史项目与完成任务的归档模板
├── docs/  # 仓库的使用、运维与交付说明
│   ├── superpowers/  # 搭建过程文档
│   │   └── plans/  # 实施计划存档
│   │       └── 2026-10-21-personal-ai-archive.md  # 本次初始化的实施计划
│   ├── import-guide.md  # 飞书、Codex、ima 等历史资料的脱敏导入流程
│   ├── recovery.md  # 历史版本恢复与恢复 PR 的操作方法
│   ├── repository-map.md  # 本文件：完整结构树与存放指引
│   └── setup-report.md  # 搭建交付报告、接入提示词和验证记录
├── .github/  # GitHub 自动化配置
│   └── workflows/  # Actions 工作流
│       ├── restore.yml  # 手动触发，生成历史内容恢复 PR
│       └── validate.yml  # 提交与 PR 的自动校验
├── scripts/  # 发布、校验与恢复工具
│   ├── publish.py  # 创建公开仓库并设置、核验保护规则
│   ├── restore.py  # 从历史提交创建恢复分支及 PR
│   └── validate.py  # 校验目录、AI 标签、链接和明显敏感模式
├── tests/  # 工具的验证用例
│   └── verify.py  # 在临时 Git 仓库中验证恢复与拦截行为
├── README.md  # 仓库首页：用途、目录和常用入口
├── START-HERE.md  # 所有 AI 首先阅读的档案入口
├── AGENTS.md  # Agent 的读取、写回与提交规则
├── CLAUDE.md  # Claude 项目入口，指向统一规则
├── GEMINI.md  # Gemini 项目入口，指向统一规则
├── ai-integration.md  # 跨 AI 读取、GitHub API 和 PR 写回协议
├── SECURITY.md  # 公开内容边界、权限与版本保护说明
└── .gitignore  # 忽略本地临时文件、私有导入目录和凭据文件
```

`.git/` 是本地 Git 历史与配置目录，不作为仓库内容上传；临时文件、缓存和被 `.gitignore` 排除的内容也未列入上图。此结构树是当前快照，增删文件后需同步更新。

## 新内容应该放哪里

| 想记录的内容 | 存放位置 |
| --- | --- |
| 我的职业、身份与核心标签 | [identity/profile.md](../identity/profile.md) |
| 我的人生目标、价值观与决策原则 | [identity/goals.md](../identity/goals.md) |
| 希望 AI 如何回答、如何交付 | [workflow/preferences.md](../workflow/preferences.md) |
| 常用工具或任务执行规则 | [workflow/tools.md](../workflow/tools.md)、[workflow/priorities.md](../workflow/priorities.md) |
| 刚产生、还没归类的新经验或偏好 | [memory/inbox.md](../memory/inbox.md) |
| 可以重复使用的经验与复盘 | [memory/lessons.md](../memory/lessons.md) |
| 做了一个重要选择及其原因 | [memory/decisions.md](../memory/decisions.md) |
| 已掌握的技能或下一阶段学习计划 | [skills/inventory.md](../skills/inventory.md)、[skills/learning-plan.md](../skills/learning-plan.md) |
| 已结束的项目和任务总结 | 在 archive/ 中复制 [project-template.md](../archive/project-template.md)，填写后用具体项目名命名 |

## AI 如何使用这些文件

**读取顺序：** `START-HERE.md` → `AGENTS.md` → 身份与工作偏好 → 按任务读取记忆、技能或历史项目。

**更新路径：** 任务完成 → 提炼可公开的新信息 → 写入候选箱或对应文档 → 创建 PR → 自动校验与审阅 → 合并到 main。新设备或另一个 AI 在下次读取时获取最新版本；实时同步仍需平台接入和授权。

`AI-READONLY` 表示 AI 不应擅自改写，`AI-WRITABLE` 表示可按协议提出修改；真正的访问控制由 GitHub 权限和分支保护执行。`{{占位符}}` 不是个人事实，初始模板也不代表已导入历史资料。公开仓库只存放允许公开的内容。
