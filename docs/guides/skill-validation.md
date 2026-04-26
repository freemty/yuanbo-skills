# Skill Validation

机器可验证的 SKILL.md 契约 + repo 卫生规范。`scripts/validate_skills.py` 在本地和 CI 里执行。

## Prerequisites

- Python 3.11+（纯 stdlib，无额外依赖）
- repo 根目录运行

## Checks

对 `skills/` 和 `plugins/` 下所有包含 `SKILL.md` 的目录执行：

| 检查项 | 规则 |
|-------|------|
| Frontmatter 存在 | `SKILL.md` 首行 `---`，以 `---` 闭合 |
| `name` 字段 | 非空，且等于所在目录名 |
| `description` 字段 | 非空，≥ 20 字符（保证有触发语义） |
| README.md | 仅 `skills/*` 和 `plugins/*` 的**直接子目录**强制，嵌套子 skill 不要求 |

YAML 解析器支持折叠/字面块标量（`>`, `|`, `>-`, `|-` 等），因此多行 description 能被正确拼接。

## Steps

### 本地运行

```bash
python3 scripts/validate_skills.py
```

输出每个 skill 一行 `PASS` / `FAIL`，FAIL 下列出具体错误。末尾汇总 `N/M skills passed`。非零退出码 = 至少一个 skill 失败。

### CI

`.github/workflows/validate.yml` 在 push 到 main 和所有 PR 上自动跑。checkout 时带 `submodules: recursive`，因为多数 plugin 是子模块。

## Troubleshooting

### `frontmatter missing \`name\``

`SKILL.md` 没有 YAML 头，或格式不标准。模板：

```markdown
---
name: my-skill
description: >
  Use when ... Triggers: ...
---

# My Skill
...
```

### `name \`X\` != directory \`Y\``

frontmatter 的 `name` 必须和目录名完全一致。要么改目录名，要么改 frontmatter。注意：改目录名后要检查 `~/.claude/skills/` 下的 symlink 是否失效。

### `description too short`

少于 20 字符的 description 几乎无法触发 skill。按 CSO 格式（Context-Situation-Outcome）重写，描述*何时*用而非*做什么*。参考 `skills/paper-style/SKILL.md`。

### `missing README.md (required for top-level skills/plugins)`

只有 `skills/<name>/` 和 `plugins/<name>/` 根目录强制 README——面向 GitHub repo 页。嵌套子 skill（如 `plugins/labmate/skills/monitor/`）不需要。

## Repo Hygiene

与 validator 配套的 `.gitignore` 策略：

- 所有 agent runtime 目录（`.claude/`, `.codex/`, `.agents/`, `.augment/` 等 30+ 个）在 `.gitignore` 里统一屏蔽。它们由 `install.sh` 或第三方工具生成，不应进仓库。
- 本地状态文件（`.labmate-hook-state.json`, `skills-lock.json`, `index.html*`）同样 ignored。
- 面向用户的安装文档放在 `docs/install-codex.md`，而非 runtime 目录内。

## 添加新 skill 的 checklist

1. 创建目录 `skills/<name>/` 或 `plugins/<plugin-name>/<name>/`。
2. 写 `SKILL.md`（frontmatter 必须含 `name` + `description`）。
3. 如果是 top-level，额外写 `README.md`（面向 GitHub）。
4. 本地跑 `python3 scripts/validate_skills.py` 确认 PASS。
5. 提交 PR，CI 会再跑一次。
