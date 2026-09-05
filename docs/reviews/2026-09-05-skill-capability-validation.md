# Skills 第二轮验证记录 — 2026-09-05

## 范围与环境

后续 wiki 补改和新增 selfOS 回归见
[LabMate / selfOS 补充记录](2026-09-05-wiki-capability-followup.md)。
本文下方原始 live 执行与提交 SHA 保留为当时快照，不代表补改已在真实宿主安装运行。

- 主 checkout：`/Users/sum_young/code/projects/yuanbo-skills`，main 基线
  `b6aee12f8d23149d1ecfeed1ea1c60ed6c2adf0c`；保持不变。
- 隔离工作树：`/Users/sum_young/code/projects/yuanbo-skills-worktrees/context-engineering-20260731`。
- 外层分支 `codex/context-engineering-20260731`；所有修改过的子模块使用
  `codex/skill-capability-20260905`。内层先提交、外层后更新 gitlink。
- macOS；本次 Python 为 3.14.3，Codex CLI 0.153.4。CI 配置仍用 Python 3.11，
  尚未远程运行；本轮没有 push、PR、合并 main 或修改安装。
- LabMate 0.11.0，Papermate 0.2.0；Unbox、Paper Review、Meta Audit 1.1.0。

## 可复现离线检查

从隔离外层目录运行：

```bash
bash tests/test-capability-refactor.sh
python3 skills/research-slides/scripts/test_template.py
```

| 检查 | 结果 / 证明范围 |
| --- | --- |
| skill 格式与共享发现 | 51/51；包括 quoted/block descriptions、合法 host metadata、公开/工作区区分 |
| context audit fixtures | 4 个测试：递归断链、wiki skill 不被误当数据排除、无效 policy、目录参考、动态数量与安装发现一致 |
| web-fetcher | 7 个离线测试：合法短帖、root/作者回复/评论归属、错误/登录/导航页、HTML 视频类型、四类字幕时间戳、Markdown/JSON、缺 CLI 与 blocked |
| Unbox graph | 3 个临时数据测试：两个同名 profile 分离、手工数据保留、预览无写、重试幂等、坏输入不覆盖、未知关系不推断 |
| PaperMate | 3 个测试：Claude/Codex/Cursor 当前诊断、干净/无关命令静默、失败诊断 |
| Meta Audit collector | 1 个临时配置测试：真实层级计数、Claude-only 范围、未知能力不宣称已运行 |
| LabMate lifecycle | 9 个直接 handler 测试：四事件、环境优先级、双路径、null、TODO、真实 Git commit/失败/文档提交、session/transcript/date、换行/-C/workdir、旧坏状态 |
| LabMate 既有契约 | paper packet、全文/锚点不足拒收、十一 explicit policy、五 Claude agents、版本镜像、typed init/experiment/TODO/snapshot 均通过 |
| 实验 helper | dry-run 不启动任务；错误 experiment ID 被拒；零日志项与缺日志仍只报告 snapshot |
| 安装器 | 临时 HOME：默认跳 plugin、legacy 建链、prune 保留真实目录/standalone/非 skill plugin 路径、all 仅改变 Codex 分支 |
| research-slides | 默认 SD profile 与模板契约通过；未改 SD 样式/内容结构模板，未新建整套幻灯片 |
| diff | 外层和修改子模块的 diff whitespace 检查通过；人工核对本轮切片 |

已修复回归中发现的问题：临时目录在 macOS 的 /var 与 /private/var 解析不一致、
裸文件/目录引用漏审、安装发现排序改变同名优先级、视频 HTML 被误标为普通正文、
graph unknown relationship 被补成 collaborator、空日志 fixture 的错误断言。
这些是实际检查结果，不是模型评测分数。

## 真实执行（非 mock）

```bash
bash plugins/labmate/tests/test-codex-plugin-smoke.sh
python3 skills/web-fetcher/scripts/fetch.py https://x.com/victornunez/status/2095895077381972247 --format json
```

- 临时 HOME/CODEX_HOME 的真实 Codex 插件安装通过：0.11.0，安装且启用，
  12 个 skill 文件各一份，无 legacy skill 链接。此检查不证明模型实际调用或 hook 已被信任。
- Victor 来源读取于 2026-09-05T11:53:23Z；真实 xreach 后端返回
  `status=ok`、`content_kind=social_post`，分别包含 root、作者回复与其他账号。
  返回值明确声明 conversation 可能不完整，附带媒体没有视觉/听觉观察。
- 官方 GPT-6 指南经官方文档工具读取；来源解释与本仓库决定分开保存在设计文档。

## 尚未完成的 live 验证

下列项目**没有通过声明**，也没有用离线 fixture 替代：

1. 当前 Codex App 对新 hook 的真实信任与事件调用。当前 App 仍加载旧安装；
   为保持本机安装不变，本轮不切换注册/信任状态。现在出现的旧初始化/brainstorm
   提醒不是新四-handler 实现的输出。
2. Claude named-agent 实际调用及 read-paper 主线程追问/保存闭环。
3. 原生浏览器/CUA 视频连续动作、音频、播放器定位与视觉 QA 的实测覆盖。
4. 没有 named agent 的真实模型 read-paper、monitor、init-project 完成率。
   静态路由和 typed init 行为已验，不等于模型端到端通过。
5. 旧/新指令 × 宿主实际 Light/Medium 档位 × 四类任务的对照实验；
   当前没有可比质量、耗时或工具调用数据，不改变默认 reasoning。

## 下一次 live 对照协议

基线用上述 main SHA 与其子模块 SHA；新版用本分支交付提交。
每次只载入一套待测 skill，使用相同源版本、用户任务、可用工具与权限。
记录实际宿主/模型 ID、effort 原始标签，不能擅自把 UI 的 Light 当作某 API 枚举。

| 类别 | 任务与必须观察的验收点 |
| --- | --- |
| 短推文 | 读取一个合法短帖及 thread；正文、作者回复、评论、附带媒体不混写 |
| 视频演示 | 同一公开视频分别回答讲述、屏幕和连续动作问题；记录实际片段/声音/字幕/帧覆盖，缺失时正确降级 |
| 同名研究者 | 提供两个官方身份锚点；分开时间线与关系，冲突保留、增量恢复不混并 |
| 论文定位 | 同一完整 PDF 指定公式与图表；保留页码/内容锚点，摘要版本必须拒绝全文完成结论 |

每个 old/new × Light/Medium 单元至少一次配对运行，记录端到端秒数、
工具调用数、来源访问失败、覆盖评分、unsupported claim 和越权写入。
较高档位仅用于未达标的复杂案例，另列不可与基础单元混算。
质量门槛：可定位证据、身份隔离、覆盖诚实、数据一致性和授权边界均满足。
没有 live 结果前只交付协议，不提供“更快/更强”的结论。

## 提交定位

外层实现批次：
`b8e6ccb` 文档基线 → `2746946` 获取链 → `c401fd6` 研究消费 →
`9758ccf` 流程/hooks → `7e3cdad` 领域知识 → `a1d3c22` 验收/发布检查。
本文及清单在随后的文档交付提交中保存。

内层交付版本：
LabMate `ccc1261`；Meta Audit `74c1ff1`；Paper Review `20e1a7c`；
Papermate `5afa715`；Unbox `83bf080`；selfOS `38f69d4`。
其余 skill gitlink 可由外层提交复现。以上提交只在本地；未来发布须先使
各内层提交在对应 remote 可获取，再发布外层指针。
