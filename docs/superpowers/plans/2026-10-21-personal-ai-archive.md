# AI-READONLY: Personal AI Archive Implementation Plan

**Goal:** 建立公开、纯 Markdown、跨 AI 可读的个人档案，使用 PR、检查与 Git 历史保护写入。
**Architecture:** 五类档案与统一索引；Agent 在任务结束后提交候选记忆；GitHub 主分支通过 PR 更新。
**Tech Stack:** Markdown、Python 3 标准库、Git、GitHub CLI、GitHub Actions。
**Spec:** 用户 2026-10-21 请求：personal-ai-archive 公开仓库、五目录、模板、集成、保护与交付报告。

## 约束

不从未连接的飞书、ima 或历史聊天推断个人事实；不把私密资料发布到公开仓库。不声称所有 AI 产品支持自动同步。无凭据时明确报告远端未创建。

## 执行步骤

- [x] 创建 identity、workflow、memory、skills、archive 模板，每个 Markdown 首行包含 AI 标签与清晰占位符。
- [x] 编写 README、START-HERE、AGENTS、CLAUDE、GEMINI 与 ai-integration；注明能力和信任边界。
- [x] 添加 validate.py（结构、标签、敏感模式、相对链接检查）、publish.py（创建公开仓库、首次推送、设置分支保护）、restore.py（按历史提交创建恢复 PR）。
- [x] 添加 PR 校验与手动内容恢复工作流；任务结束记忆通过 PR 同步。
- [x] 使用真实文件校验与临时 Git 仓库测试回退；通过后初始化并提交本地 Git 历史。
- [ ] GitHub 授权可用时执行 publish.py；查询仓库、保护和 Actions 状态验证，写入交付报告。缺少授权则保留可执行交付包与准确的未完成项。

所有步骤在当前会话内执行，无需另行选择实施方式。
