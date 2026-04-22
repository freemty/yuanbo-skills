# Outputs Convention

Skill 产出物统一存放在 `~/outputs/`，旧路径通过 symlink 兼容。

## 目录结构

```
~/outputs/
├── no-more-fomo/      # 日报 HTML/MD（skill: no-more-fomo）
├── unbox/             # 人物 profiles + graph（skill: unbox/unbox-graph/unbox-to-wiki）
├── weekly-report/     # 周报（skill: weekly-report）
├── zhihu-articles/    # 知乎文章存档（raw source for selfOS）
├── gemini-exporter/   # Gemini 对话导出工具 + 数据
└── maqianzu-wiki/     # 马前卒视频 wiki
```

## Symlinks（向后兼容）

Skill 代码中大量引用旧路径（`~/no-more-fomo`、`~/unbox-output` 等），不逐一修改，用 symlink 保持兼容：

```
~/no-more-fomo    → ~/outputs/no-more-fomo
~/unbox-output    → ~/outputs/unbox
~/weekly-report   → ~/outputs/weekly-report
~/zhihu-articles  → ~/outputs/zhihu-articles
~/gemini-exporter → ~/outputs/gemini-exporter
~/maqianzu-wiki   → ~/outputs/maqianzu-wiki
```

## 不在 outputs 里的

| 路径 | 原因 |
|------|------|
| `~/selfOS/` | 独立知识库，不是 skill 产出物 |
| `~/selfOS/` | 分发模板 |
| `~/readloop/` | 独立 app 项目 |

## 新 skill 输出约定

新建 skill 如果需要持久化输出：

1. 输出目录: `~/outputs/<skill-name>/`
2. 目录名: 全小写，连字符分隔，与 skill name 一致
3. 兼容 symlink: 如果 skill 已经引用了 `~/<old-name>`，建 symlink 而不是改代码
4. 在本文档的目录结构里追加一行
