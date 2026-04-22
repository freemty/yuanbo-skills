# selfOS worktree → standalone repo 转换

> 把 git worktree 转为独立 repo，避免主 repo 删除后 worktree 失效。

## Problem

`~/selfOS/`（主 repo）+ `~/selfOS-private/`（worktree）结构过于复杂。worktree 的 `.git` 是指向主 repo 的指针文件，删主 repo 就断裂。

## Cause

最初 selfOS 有公开模板（main 分支）和私有数据（private 分支），用 worktree 同时 checkout 两个分支。后来发现公开模板没有独立存在的价值。

## Solution

```bash
# 1. 确认 worktree 有没有未推送的 commit
git -C ~/selfOS log --oneline origin/private..private

# 2. 从主 repo 移除 worktree 注册（会删除 worktree 目录）
git -C ~/selfOS worktree remove --force ~/selfOS-private

# 3. 重新 clone 为独立 repo
git clone --branch private <remote-url> ~/selfOS-private

# 4. 如果有未推送的 commit，从旧 repo fetch 过来
git -C ~/selfOS-private remote add old-selfos ~/selfOS
git -C ~/selfOS-private fetch old-selfos private
git -C ~/selfOS-private merge old-selfos/private --ff-only
git -C ~/selfOS-private remote remove old-selfos

# 5. 推送未推送的 commit
git -C ~/selfOS-private push origin private

# 6. 删除旧主 repo
rm -rf ~/selfOS
```

## CRITICAL: gitignored 文件会永久丢失

`worktree remove --force` 删除整个工作目录，包括 **gitignored 的 untracked 文件**。selfOS 的 `.gitignore` 排除了含 PII 的源数据：

```
raw/notion-notes/
raw/claude-conversations/
raw/gemini-conversations/
raw/twitter-bookmarks/
```

这些文件从未被 git 追踪，worktree 删除后无法恢复。**执行前必须手动备份 gitignored 目录。**

正确步骤应该是：
```bash
# 0. 先备份 gitignored 数据！
cp -r ~/selfOS-private/raw/notion-notes /tmp/notion-notes-backup
cp -r ~/selfOS-private/raw/claude-conversations /tmp/claude-backup
cp -r ~/selfOS-private/raw/gemini-conversations /tmp/gemini-backup
cp -r ~/selfOS-private/raw/twitter-bookmarks /tmp/twitter-backup

# 然后再执行 worktree remove...
# clone 完成后恢复：
cp -r /tmp/notion-notes-backup ~/selfOS/raw/notion-notes
# ...
```

恢复方式（如果已经丢失）：
- Notion: Settings → Export all workspace content
- Claude: claude.ai Settings → Export data
- Gemini: 用 `~/outputs/gemini-exporter/` 重新导出
- Twitter bookmarks: 重新导出

## Notes
- Date: 2026-04-22
- 最终结果：`~/selfOS-private` 改名为 `~/selfOS`（去掉 -private 后缀）
- 转换后 yuanbo-skills/selfos 子模块不受影响（它指向 remote）
