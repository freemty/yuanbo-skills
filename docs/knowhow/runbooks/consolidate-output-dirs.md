# 统一 skill 输出目录到 ~/outputs/

> 把散落在 ~ 下的 skill 产出物目录收拢到 ~/outputs/，用 symlink 保持旧路径兼容。

## Problem

多个 skill 把输出写到 `~/` 下的独立目录（`~/no-more-fomo`、`~/unbox-output`、`~/weekly-report` 等），缺乏统一结构。

## Solution

```bash
# 1. 创建统一目录
mkdir -p ~/outputs

# 2. 移入
mv ~/no-more-fomo ~/outputs/no-more-fomo
mv ~/unbox-output ~/outputs/unbox
mv ~/weekly-report ~/outputs/weekly-report
# ...其他目录同理

# 3. 创建 symlink 兼容旧路径（skill 代码不用改）
ln -s ~/outputs/no-more-fomo ~/no-more-fomo
ln -s ~/outputs/unbox ~/unbox-output
ln -s ~/outputs/weekly-report ~/weekly-report
```

## Notes
- Date: 2026-04-22
- 详细约定见 `docs/outputs-convention.md`
- 不改 skill 代码中的路径引用，全靠 symlink 兼容
- `~/selfOS/` 不属于 outputs，不移入
