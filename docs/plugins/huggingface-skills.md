# huggingface-skills

- **Source:** [huggingface/skills](https://github.com/huggingface/skills)
- **Type:** Plugin
- **Category:** ml
- **Version:** 1.0.1
- **License:** Apache-2.0
- **Tags:** papers, datasets, training, gradio, transformers.js, eval

## 组成

11 skills + 1 MCP server + 3 Gradio apps + 构建脚本 + 跨平台适配

| # | Skill | Category | Function |
|---|-------|----------|----------|
| 1 | hf-cli | infra | Hub CLI：上传下载模型/数据集/Space、认证、Endpoints 部署 |
| 2 | huggingface-datasets | data | Dataset Viewer API：浏览/分页/搜索/过滤，SQL 查询 parquet |
| 3 | huggingface-llm-trainer | training | TRL/Unsloth 云 GPU 训练 LLM（SFT/DPO/GRPO），GGUF 转换 |
| 4 | huggingface-vision-trainer | training | 视觉模型训练：检测(D-FINE/DETR)、分类(timm)、分割(SAM2) |
| 5 | huggingface-community-evals | eval | 本地 GPU eval（inspect-ai/lighteval，vLLM/Transformers 后端） |
| 6 | huggingface-trackio | tracking | 训练 metrics logging + alert + dashboard，同步 HF Space |
| 7 | huggingface-papers | papers | 读取 HF Papers / arXiv，获取元数据和关联资源 |
| 8 | huggingface-paper-publisher | papers | 在 Hub 发布论文、关联模型/数据集、认领作者 |
| 9 | huggingface-gradio | app | Python 构建 Gradio Web UI / ML Demo |
| 10 | huggingface-tool-builder | tooling | 创建可复用脚本，链式调用 HF API |
| 11 | transformers-js | inference | 浏览器/Node.js 跑 ML 模型，WebGPU/WASM |

- **MCP Server**: `https://huggingface.co/mcp?login`（远程 HF Hub 工具调用）
- **Apps**: evals-leaderboard / hackers-leaderboard / quests（Gradio Space）

## Key Takeaways

- HF 生态全家桶，从论文搜索到模型训练到部署一条龙
- huggingface-papers 搜论文比直接搜 arxiv 方便，结果带社区 upvote
- huggingface-llm-trainer / vision-trainer 直接在 HF 上跑 fine-tuning

## 值得借鉴的工程实践

- `generate_agents.py` — 从 SKILL.md frontmatter 自动生成 AGENTS.md + 校验 marketplace.json 一致性 + 更新 README 表格，一个脚本保证四处同步
- `AGENTS_TEMPLATE.md` — Mustache 风格模板，skill 增删无需手改 AGENTS.md
- `generate_cursor_plugin.py` + `gemini-extension.json` — 一套 skill 适配三个平台（Claude Code / Cursor / Gemini CLI）
- `UV_RULES.md` — PEP 723 inline deps + `uv run` 统一执行，不依赖 venv
- `publish.sh` + `.github/` — CI/发布自动化

## Relevance

- no-more-fomo 的 HF Daily 数据源用的就是 HF papers API
- fars-autotrain 的 model 可以考虑用 HF trainer 做对比实验
- 我们有 15+ skill 但缺统一生成/校验脚本，AGENTS.md 手写容易漂移。可参考 `generate_agents.py` 做一个类似的 `scripts/sync.py`
