# Skills 第二轮发布与实装 — 2026-09-05

用户在改革验收后明确要求推送、合并并实装，替代此前的“不 push、不改安装”边界。
按 update-docs 的归档契约记录观察、完成状态和未验证项，不把安装等同于运行验证。

## 发布

13 个修改的子仓库已先行推送改革分支 `codex/skill-capability-20260905`，
并无强推地快进远端默认分支。外层保留 `codex/context-engineering-20260731`
作为完整改革记录，再快进 main；不删除分支。

| 子仓库 | 发布提交 | 默认分支 |
| --- | --- | --- |
| LabMate | bb663af | main |
| Meta Audit | 8dc1926 | main |
| Paper Review | 95314e7 | main |
| PaperMate | 5afa715 | main |
| Unbox | 83bf080 | main |
| selfOS | 64d9e88 | private（仅 selfos-private 私有远端） |
| Beamer Style | 9c750a6 | main |
| CC Navigator | 605e13b | main |
| FlipRadio | de3d875 | main |
| No More FOMO | b695b2e | main |
| Paper Storyteller | a77c7f1 | main |
| Paper Style | 2c7431d | main |
| Writing Agents | 8e21413 | main |

selfOS 先合并当前私有主线 150299d 的 14 个新提交；相对该主线，
改造只触及技能、入口说明与测试，wiki/raw/docs 内容完全相同。
不将私有历史推到 public selfOS，不使用模板覆盖个人知识库。

发布前修正 Meta Audit 的 Claude 组件相对路径，并为 Paper Review 补齐
Claude manifest；两者均由当前 Claude CLI 验证通过。外层 Claude 本地
marketplace 现在与 Codex 一样暴露 5 个自有插件，发布检查阻止缺少 `./`
前缀的 Claude 组件路径。

## 实装策略与状态

目标插件：LabMate 0.11.0、Meta Audit 1.1.0、Paper Review 1.1.0、
PaperMate 0.2.0、Unbox 1.1.0。Codex 使用已有 `yuanbo-skills`
本地 marketplace；Claude 使用已有 `yuanbo-skills-local`。

先备份配置及链接，验证插件替代来源后再移出重复链接。保留第三方技能和
失效旧链接，不执行覆盖全部目录的 installer。独立技能指向 main；11 个
selfOS 全局技能继续指向 live selfOS。两个 transcribe 入口选择 selfOS
作为唯一全局来源。旧真实 web-fetcher、paper-style、Claude swiss-knife-design
整体保存后换为链接，paper-style 旧 Git 状态一并保留。

私密备份：`/Users/sum_young/.codex/backups/skills-rollout-20260905-__xlct_p/`。
其中 `before.json` 保存链接、提交与 selfOS 未提交文件哈希；配置副本不入 Git。
后续 `actions.json` 记录每个替换项及其可恢复副本。回滚应按目标逐项恢复，
不把旧整份配置覆盖到含新用户变更的配置上。

外层合并、本机版本和链接切换的最终结果在执行后补记。

## 验证与边界

- 发布前 `bash tests/test-capability-refactor.sh` 全部通过：51 个公开入口、
  版本/策略、内容审查、获取适配、LabMate hooks/接口、19 个 selfOS 行为用例、
  临时目录安装回归。254 项资源清单已刷新合并后的内容哈希。
- Claude 验证 5 个插件 manifest 和本地 marketplace 均通过；根目录 CLAUDE.md
  的开发说明不是插件自动加载指令，这一提示不作为校验失败。
- 原生媒体、真实模型质量对照仍沿用[验证记录](2026-09-05-skill-capability-validation.md)
  中的未完成状态。注册成功、缓存存在不能证明 hooks 已信任或本任务热加载了新版。
- 必须在新任务/会话中检查实际发现和 hook 信任；不通过手工伪造信任哈希绕过宿主审核。
