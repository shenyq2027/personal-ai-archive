# AI-READONLY: 跨 AI 适配与同步配置

## 能力边界

Markdown 是通用内容格式，GitHub API 是读取/写入接口；这不代表所有 AI 网页客户端都能调用 API、常驻后台或自动修改仓库。需要浏览工具、GitHub 连接器、自定义 Action/MCP 或可执行 Git/HTTP 的 Agent。初始包提供协议与脚本，不伪造任何平台的同步开关。

| 平台 | 可行接入方式 | 任务结束写回条件 |
| --- | --- | --- |
| ChatGPT | 有 GitHub 应用/连接器时按其范围授权；或使用具备浏览能力的会话读取公开文件；或自定义 Action 对接 GitHub API | 普通只读连接不等于可写；必须另有授权写入工具 |
| Codex | 克隆仓库，在此目录启动；读取项目 AGENTS.md，并遵循入口加载档案 | Git/gh 已登录且获仓库写权限；分支、提交、PR |
| Claude | Claude Code 克隆仓库并读取 CLAUDE.md；网页端按实际可用 GitHub 集成连接 | 客户端需提供 Git/GitHub 写工具；不得假定网页具备写权限 |
| Gemini | Gemini CLI 项目读取 GEMINI.md；网页端用可用导入/浏览能力读取文件 | 需 Git/GitHub 写工具与明确授权 |
| Meta Muse / OpenAI Dots | 尚未核实准确产品名称、公开 API 与用户账号能力；不视为已支持 | 若实际 Agent 支持 HTTP/Git，执行下述平台中立协议，否则手工提供 Markdown |

各产品名称和能力会变化，以实际客户端、账号、权限与官方文档为准。未连接的平台不会因本仓库存在而自动同步。

## GitHub API 读取（无需令牌）

用实际仓库路径替换 `OWNER/personal-ai-archive`。公开 REST API 有匿名速率限制。

```sh
curl --fail --location \
  -H 'Accept: application/vnd.github.raw+json' \
  'https://api.github.com/repos/OWNER/personal-ai-archive/contents/START-HERE.md?ref=main'
```

先读取 `GET /repos/OWNER/personal-ai-archive/commits/main` 保存 SHA；再以该 SHA 作为 `ref` 读取入口、AGENTS、身份和偏好，确保同一版本。目录枚举使用 `GET /repos/OWNER/personal-ai-archive/contents/{directory}?ref={sha}`；UTF-8 Markdown 可直接消费，默认 JSON 返回的 `content` 则需按 `encoding` 解码。公开 raw 地址形如 `https://raw.githubusercontent.com/OWNER/personal-ai-archive/main/START-HERE.md`，客户端必须能跟随相对链接，或逐个读取文件。

## 通用启动提示词

> 请通过可用的 GitHub 工具读取 OWNER/personal-ai-archive 的 START-HERE.md、AGENTS.md、identity/profile.md、identity/goals.md、workflow/preferences.md、workflow/priorities.md。将 main 解析成固定 commit SHA 后读取同一版本。占位符与候选记录不是事实。仅加载与任务有关的资料。当前本人指令优先。完成任务后按 ai-integration.md 提出可公开的新记忆更新；有写工具时建 PR，无工具时给出补丁并说明尚未写回。禁止把隐私或内部资料上传到公开仓库。

## 自动更新协议

这是供已接入的 Agent 执行的任务结束钩子协议，不是已安装在各 AI 服务中的后台任务。

1. 刷新 main 与基准 SHA，检查是否已有同 ID/同含义的记忆。
2. 提炼长期有用的经验或明确偏好；检查来源和公开许可。新推断标记 candidate，身份变化须本人明确指令。
3. 追加 memory/inbox.md；已确认条目可归入 workflow、skills、memory/lessons.md 或 memory/decisions.md。归档时引用旧条目，避免丢失上下文。
4. 建立 `memory/<agent>-<timestamp>` 分支，修改对应 Markdown，执行 `python3 scripts/validate.py`，提交、推送、建 PR。
5. 读取 PR diff、等待 `archive-validation`；按既有授权审阅后合并。不能绕过 main 保护；冲突时重新合并并校验。
6. 回读 main 上的文件，报告 PR URL、最终 SHA 与新增条目。其他设备或 AI 在下一次任务启动时刷新；无常驻调度则不会实时推送。

API 等价路径：GET main ref → POST git/refs 创建分支 → GET contents 获取 blob SHA → PUT contents（分支名、Base64 内容、旧 SHA）→ POST pulls。HTTP 409/422 先刷新重试，禁止覆盖并发写入。多文件原子提交可用 Git tree/commit API。

## 权限配置

公开读取无需凭据。写入优先用限定到此仓库的 GitHub App 或 fine-grained PAT：Contents 读写、Pull requests 读写、Metadata 读。平台需要持久权限时由本人完成授权，凭据存平台 Secret；不要粘贴到对话。普通 Agent 不需要 Administration 或 Workflows 写权限；只有首次保护设置需要仓库管理权限。读取权限不自动扩大为写入权限。

## 官方参考

- [Codex 的 AGENTS.md 指令发现机制](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [GitHub 仓库内容 API](https://docs.github.com/en/rest/repos/contents)
- [GitHub 分支保护](https://docs.github.com/en/rest/branches/branch-protection)
- [GitHub Pull Requests API](https://docs.github.com/en/rest/pulls/pulls)
