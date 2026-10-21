# AI-READONLY: 回退到历史版本

## 网页恢复个人档案（一次手动运行）

仓库发布且 Actions 可运行后：Actions → Restore archive → Run workflow → 输入历史完整 commit SHA。工作流校验 SHA 属于 main 历史，将 identity、workflow、memory、skills、archive 恢复为该版本，并创建 PR。审阅并通过检查后合并，保留完整回退记录。

GitHub 可能对 bot 创建的 PR 标记 `action_required`，此时由具备权限的维护者批准该工作流运行；不要关闭保护。首次真实演练已验证批准后校验正常通过。

这是“运行一次生成恢复 PR”，不宣称点击后立即覆盖 main。默认分支工作流版本必须存在。发布脚本会尝试允许 Actions 创建 PR；组织若禁止此设置，须由组织管理员处理或使用下面的本地命令。恢复工作流显式触发校验，因为默认 GITHUB_TOKEN 创建的 PR 通常不会自动触发 pull_request 检查。

## 任意完整历史快照恢复（本地）

在干净克隆、GitHub CLI 已登录且有推送权限的环境：

```sh
python3 scripts/restore.py FULL_COMMIT_SHA
```

脚本要求该提交是 origin/main 的祖先，在新恢复分支重建该提交的完整受跟踪文件树，创建提交和 PR；不 force push、不重写 main。不允许恢复目标引入 symlink；脚本不会执行历史版本中的脚本。若目标修改 .github/workflows，凭据可能还需 workflow 权限，不能静默扩大授权。

恢复完整快照可能撤销当前安全配置与校验脚本，合并前必须审阅。旧版本若不符合当前检查会阻止合并；不要关闭保护，先按需要修正恢复分支。远端保护设置不在 Git 历史中，本脚本不会更改。

## 其他路径

单个已合并 PR 误改可使用 GitHub 的 Revert 创建反向 PR。回退到旧版本不等于清除敏感信息历史。仓库删除或账号丢失需要独立备份；本包不提供已启用的异地备份。
