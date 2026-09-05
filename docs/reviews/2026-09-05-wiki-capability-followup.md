# LabMate / selfOS wiki 补充改造 — 2026-09-05

承接用户追加的“LabMate 和 selfOS wiki skills 也需要这样改”。
基线为外层 `5495953`，LabMate `ccc1261`，selfOS `38f69d4`。
继续原隔离改革分支，不改主 checkout、live selfOS、全局安装或已有 wiki/raw。

## 实际遗漏与处置

| 范围 | 原问题 | 本次处置 |
| --- | --- | --- |
| LabMate update-docs / update-knowhow + archival contract | “只归档已验证事实”与保存未解决调查/用户观点的意图不够区分；alias 依赖另一 skill | 分离观察、用户表述、决策、假设和已验证解决；alias 可直接完成；项目文档和个人 wiki 不自动双写 |
| LabMate read-paper | 保存条件可能被理解为读完后必须再收到一次请求 | 继承本任务已有保存意图；按明确目的地保存 packet/定位信息，保留现有论文验收格式 |
| wiki 入口 / 初始化模板 | 根发现只认 AGENTS，但 init 模板只写 CLAUDE；模板仍泛化全库写入 | 默认中立 AGENTS；保留已有文件，按需 Claude 入口；明确只读/写入边界及不存在脚本的回退 |
| wiki ingest / 新 evidence-acquisition 参考 | 未统一多模态覆盖、partial 重试、源身份与模型分析边界 | 按能力获取；保留页/段/时间定位；字幕不证明画面，摘要不冒充全文；已有 source 可直接编译图谱而不重复归档 |
| wiki query / 搜索脚本 | 指定 wiki root 后仍查询全局 qmd collection | 辅助脚本只查指定目录，rg/grep 路径均可；原生检索或已核对范围的索引仍可直接使用 |
| wiki lint | 默认写 log；修复指令连带 stub 和 commit | 默认全程只读；授权修复按已有范围推进，不补空节点凑图谱、不自动 commit |
| interview / modes / workflow | 固定 ft 列表上限、固定问答轮数、无变化也更新时间消提醒 | 按可用书签/记录选择；保留一次一个问题；只清理已解决/明确略过项，不伪造 updated |
| thought / note / todo / transcribe | 目标默认跟安装位置；thought 自动推荐追问；转写输出位置容易混同 wiki | 显式目标优先且错误目标不回退个人库；note helper 显式 root；转写保存遵从请求位置；取消自动跨流程推荐 |
| digest | 今日无记录自动扩大到三天；周报只读当月任务归档 | 保持请求日期范围，跨月读所有涉及的归档；未提交变更不冒充今天完成 |
| wiki-help / selfOS AGENTS / CLAUDE | 固定 slash 表和重叠旧规则、自动安装假设 | 按宿主输出帮助；压缩重复目录/宣传，保留 schema、来源和分支规则 |
| 测试 | selfOS 契约只搜入口字样，未走 references；未接入统一回归 | 递归检查可达参考；保留源字段检查；19 个 selfOS 检查纳入统一入口；字数只作审查提示 |

note 原话块、thought 用户文字、conversation/audio evidence_scope、JSONL 状态、
Notion checkpoint 和 paper packet 数据格式未替换。本次没有改写历史研究、
wiki 页面、raw、模板/私有分支历史、供应商或系统 skill。
既有 wiki sync/synthesize 的上一轮改造保留；本次没有重做它们。

## 可复现验证与界限

隔离外层运行 `bash tests/test-capability-refactor.sh`：通过。
其中 selfOS 可单独运行：

```bash
cd projects/selfos
python3 -B -m unittest tests.test_selfos_skill_contracts tests.test_validate_wiki_evidence tests.test_note_mode tests.test_wiki_search
```

- 19 个 selfOS 检查通过：8 个入口/可达参考/临时安装契约，4 个来源验证，
  2 个 note 生命周期，5 个搜索行为用例。
- 搜索旧实现实际复现 2 个失败：目标库被全局 qmd 结果替代、以选项字符
  开头的查询同样被送入错误索引。修复后隔离目录、中文/空格文件名、
  grep 回退、无匹配、无效目标/空查询、读取失败状态检查通过。
- 补跑旧 selfOS 契约最初有 4 个失败（入口字样未跟随已迁出的参考）；
  修复测试的可达资源检查，并保持用户原话/转写字段断言，没有关闭来源验证。
- LabMate 全文/摘要和公式锚点拒收、平台 policy、版本、四 handler、
  确定性接口，以及外层格式、引用、安装回归通过。LabMate 本轮仍是尚未发布的
  0.11.0，未覆盖当前安装缓存。
- 原生视频观察、模型实际 init/lint/ingest 行为、Claude 调用和 Light/Medium
  对照尚未做 live 验证。上述静态契约和脚本用例不是模型端到端通过证明。
- 主 checkout HEAD 仍为 `b6aee12`；全局 wiki/interview 链接仍指向
  live selfOS，update-docs 仍指向主 checkout。只在临时 HOME 测试安装。

## 提交与清单

内层提交：LabMate `bb663af`；selfOS `e4b3162`。
外层后续提交包含两个 gitlink、回归入口、计划补充和本记录；不 push、不建 PR。

本次按 skill-creator 的能力/范围原则、writing-skills 的实际用例验证思想和
meta-audit 的分层方法执行；旧的强制部署/固定测试流程按用户已批准计划覆盖。
update-docs 用于留下这份可复查记录，不触发个人 wiki 归档。

[逐入口/资源清单](2026-09-05-skill-capability-audit.md)及 JSON 哈希已刷新。
该机器清单聚焦 skill/执行参考；本次额外修改的 selfOS AGENTS/CLAUDE 和
两个 tests 文件，以及 LabMate tests/test-read-paper.sh，由上述内层提交完整记录。
安装迁移仍按[独立清单](2026-09-05-installation-migration.md)后续授权执行。
