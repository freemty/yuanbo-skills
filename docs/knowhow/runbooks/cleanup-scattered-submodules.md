# 清理散落的子模块副本

> 删除 ~/code/projects/ 下与 yuanbo-skills 子模块重复的独立 clone。

## Problem

开发过程中在 `~/code/projects/` 下 clone 了多个 repo（labmate、meta-audit、no-more-fomo 等），后来这些 repo 也作为 submodule 加入了 yuanbo-skills。两份副本容易混淆。

## Solution

```bash
# 1. 对比散落副本和子模块，确认指向同一个 remote
for dir in flipradio-write-skill labmate meta-audit no-more-fomo paper-storyteller paper-style unbox-skills; do
  echo "$dir:"
  git -C ~/code/projects/$dir remote get-url origin
  git -C ~/code/projects/yuanbo-skills/$dir remote get-url origin
done

# 2. 检查散落副本有没有未提交/未推送的改动
for dir in ...; do
  git -C ~/code/projects/$dir status --porcelain | wc -l
  git -C ~/code/projects/$dir log --oneline origin/main..HEAD | wc -l
done

# 3. 确认安全后删除
rm -rf ~/code/projects/{flipradio-write-skill,labmate,meta-audit,...}
```

## Notes
- Date: 2026-04-22
- 删除前务必检查 dirty files 和 unpushed commits
- 常见的 dirty files 是 IDE 配置（`.DS_Store`、`.superpowers/`），可以安全忽略
