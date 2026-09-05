# 本机安装迁移清单 — 2026-09-05（迁移前快照）

后续用户已授权推送、合并和实装；实际执行状态见
[发布与实装记录](2026-09-05-skill-rollout.md)。下文保留迁移前观察，
其中“未授权/未执行”描述不代表后续执行状态。

本轮没有执行以下迁移。隔离分支修改不会改变指向主 checkout 的全局链接，
也不会同步到 `/Users/sum_young/selfOS`。先备份、明确选择，再迁移并验证；
可用性不确定时回滚原链接/目录，不能用删除代替诊断。

## 已核实

| 项目 | 当前状态 | 后续迁移动作 |
| --- | --- | --- |
| LabMate | Codex registry 中 0.10.0 已安装且启用；另有 11 个 `~/.agents/skills` 链接指向 main 的 LabMate | 选择插件路径；先安装/验证新版，再备份并移除确认重复的链接 |
| 其他自有插件 | 全局链接：Papermate 6、Unbox 3、Meta Audit 2、Paper Review 2；本次 Codex registry 未列为已安装插件 | 不能按“已经是插件”直接 prune；先决定安装插件还是暂保留 legacy |
| web-fetcher | `/Users/sum_young/.agents/skills/web-fetcher` 是旧真实目录；Claude 同名项链接 main | prune 不会也不应删除真实目录；对旧目录做带日期备份后再决定替换，保留回滚副本 |
| paper-style | Codex 全局是真实目录；Claude 链接 main | 核对本地定制并备份；不能盲目覆写 |
| research-slides / beamer-style | Codex/Claude 都指向 main checkout | 本轮隔离修改不影响现有 SD 默认；未来只在明确迁移时改变来源 |
| selfOS skills | 多数有效链接指向独立 `/Users/sum_young/selfOS/.claude/skills` | 只迁移已审查的 skill 变更；不要合并/覆盖用户 wiki 与 raw |
| 失效链接 | `defuddle, json-canvas, obsidian-bases, obsidian-cli, obsidian-markdown, project-skill, selfos, selfos-completion` | 先记录原目标，决定替代入口；本轮保留未删 |
| 工作区 caveman | 主 checkout 有忽略的入口，另有全局真实目录；Claude 又链接全局 | 审查重复发现与模式范围，未经授权不改文件/注册 |

LabMate 11 个重复候选名：
`analyze-experiment, commit-changelog, init-project, monitor, new-experiment,
read-paper, survey-literature, update-docs, update-knowhow, update-project-skill,
visualize`。全局 `todo` 指向 selfOS，不可误当 LabMate 重复项移除。

## 供应商 / 旧框架冲突

这里只记录当前目录/发现信息与已读到的冲突；未修改供应商或系统文件，
也未声称逐个完成第三方运行验证。

- `agent-reach` 同时出现在 `~/.agents/skills` 与 `~/.codex/skills`
  （后者指向 .cc-switch）；`find-skills` 也有两处发现路径。
- 旧 `writing-skills` 真实目录带强制测试/子 agent/部署工作流与缺失依赖，
  与本轮风险分级、无自动 push 的范围冲突。
- 旧 `web-fetcher` 真实目录仍有“任何 URL / 禁用原生读取”的规则，
  所以仅修改仓库文件不能证明当前会话已采用新版。
- `claude-code-best-practices` 与 `cc-navigator` 的发现范围重叠；
  `frontend-slides` 与 research-slides、`humanizer` 系列与 de-ai/个人写作
  存在任务选择重叠。这是路由审查项，不等于必须卸载。
- `proactive-agent, notion-lifeos, scholar-agent, cmux, daily-summary` 等
  第三方真实目录保持不变。OpenAI 系统/官方插件由宿主管理，不在本仓库重写。

## 可回滚迁移顺序（待授权）

1. 保存当前 registry 的非敏感清单、版本及每个链接目标；对真实目录做独立备份，
   不搬动 HOME/skills 根目录。确认需要保留的本地定制。
2. 先完成分支评审与所需发布；本轮没有 push 或合并，主 checkout 仍是旧版。
3. 选择插件与 legacy 的唯一来源。安装所有计划替代的插件并验证，再处理链接。
   不把“插件文件已缓存”当作“已启用且 hook 已信任”。
4. 在**以后已获准更新的主 checkout**运行下面命令前先审阅其影响范围：

   ```bash
   bash /Users/sum_young/code/projects/yuanbo-skills/install.sh --target codex --prune-plugin-skill-links
   ```

   该选项针对该 checkout 的所有 plugin-skill 链接，不只 LabMate。
   当前隔离工作树下的同名选项不会清除指向 main 的链接。
   暂未采用插件的其他 skills 必须先保留可用路径。
5. 旧真实 web-fetcher/paper-style 目录单独备份后替换；prune 不处理它们。
   不自动修改 Claude 安装、供应商副本或 live selfOS。
6. 重启两个宿主，核对发现次数、实际读取的版本、hook 信任、无 named-agent
   路径以及 SD profile。失败则恢复已记录的原链接/真实目录，再诊断。

临时 HOME/CODEX_HOME 安装测试和本机迁移是两件事；前者已通过，
后者仍未授权执行。
