# zarazhangrui (Zara Zhang)

- **Source:** [github.com/zarazhangrui](https://github.com/zarazhangrui)
- **Type:** 个人开发者工具集
- **Tags:** skill, content-pipeline, podcast, feishu, slides, education

## 概述

Zara Zhang，AI builder / content creator。12 个公开 repo，围绕 "内容消费 → 转化 → 输出" 这条主线。工具风格：Claude Code skill 优先，个人效率导向，重视 "不需要新 app" 的理念（输出到 podcast app / email / 飞书等已有渠道）。

## 工具全景

### Tier 1: 值得深入研究

| Repo | What | Why Interesting |
|------|------|-----------------|
| [personalized-podcast](https://github.com/zarazhangrui/personalized-podcast) | 任意内容 → 双主持人 AI podcast（Fish Audio TTS），输出 MP3 + RSS feed | NotebookLM 的开源替代，可定制 prompt/voices/hosts。"听自己的简历被两个人讨论" 这个 use case 很有想象力。PROMPT.md 控制脚本风格 |
| [follow-builders](https://github.com/zarazhangrui/follow-builders) | AI builder 日报：25 个 X 账号 + 6 podcast + 公司 blog → digest 推送 | 和 no-more-fomo 定位高度重叠。区别：follow-builders 偏向人（builder）而非话题（AI news），有 Telegram/Discord/WhatsApp 推送，source list 中心化维护自动更新 |
| [frontend-slides](https://github.com/zarazhangrui/frontend-slides) | Claude Code skill：从零或从 PPT 创建动画 HTML 演示 | Anti-AI-slop 设计哲学，视觉风格发现流程（生成预览 → 选择 → 生成），PPT 转 web。和 beamer-style 的理念不同但互补 |
| [feishu-claudecode-bridge](https://github.com/zarazhangrui/feishu-claudecode-bridge) | 飞书里直接和本机 Claude Code 对话，WebSocket 长连接 + 流式卡片 | 复用 Claude Max/Pro 订阅，零额外成本。手机上 code review/debug。群聊支持，每群独立 session。Fork of joewongjc/feishu-claude-code |

### Tier 2: 有参考价值

| Repo | What | Why Interesting |
|------|------|-----------------|
| [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) | 任意代码库 → 交互式 HTML 课程（单文件，含动画/quiz/代码翻译） | "Build first, understand later" 教学理念。code ↔ 白话翻译、scroll-based modules、quiz 测应用不测背诵。对 learn skill 有参考价值 |
| [youtube-to-ebook](https://github.com/zarazhangrui/youtube-to-ebook) | YouTube 频道 → EPUB 电子书，Claude 改写为杂志风格文章 | 完整 pipeline：频道 → 转录 → Claude 改写 → EPUB → email。Streamlit dashboard + launchctl 自动化 |
| [lark-minutes-tasks](https://github.com/zarazhangrui/lark-minutes-tasks) | 飞书会议纪要 → 提取 action items → agent 自动执行 | Wake Word 机制：会议中说 "hey agent" 触发指令，会后 agent 从转录中提取执行。不只是 todo list，agent 真的去做（发消息/建日历/查文档） |
| [call-me-skill](https://github.com/zarazhangrui/call-me-skill) | Agent 打电话给你，对话后转化为推文/LinkedIn 帖子等 | Voice-first 内容创作。不是你打给 AI，是 AI 打给你 |
| [longcut](https://github.com/zarazhangrui/longcut) | 长视频 → 结构化学习空间（highlight reels + AI Q&A + 笔记） | Next.js 15 + xAI Grok 4 + Supabase。highlight 自动生成 + 按主题重新生成。技术栈较重但功能完整 |

### Tier 3: 小工具

| Repo | What |
|------|------|
| [tab-out](https://github.com/zarazhangrui/tab-out) | Chrome 新标签页替换为 tab 管理面板，domain 分组 + 关闭动效 |
| [podcast-feed](https://github.com/zarazhangrui/podcast-feed) | 个人 podcast RSS feed |
| [vibe-coding-jam-presentation](https://github.com/zarazhangrui/vibe-coding-jam-presentation) | 演示 slides |

## Key Takeaways

1. **内容 pipeline 思维：** 几乎所有工具都是 "X 格式 → AI 处理 → Y 格式" 的管道。YouTube→EPUB, 会议→tasks, 代码→课程, 任意内容→podcast
2. **"不需要新 app" 原则：** 输出到已有渠道（podcast app/email/飞书/Chrome），降低用户切换成本
3. **personalized-podcast 的 self-reflection use case：** 让 AI 以第三人称讨论你自己的内容（简历/日记/浏览记录），"genuinely illuminating"
4. **Wake Word 机制：** 会议中对 agent 说话，会后自动提取执行。这个交互模式值得借鉴
5. **Anti-AI-slop 设计意识：** frontend-slides 明确拒绝 "purple gradient on white" 的 AI 美学

## Relevance

- **follow-builders vs no-more-fomo：** 高度重叠，follow-builders 按人而非话题策展，source list 中心化自动更新（no-more-fomo 是本地配置）。推送渠道更丰富。值得对比学习
- **personalized-podcast：** 可以做一个 `/podcast` skill 把论文/实验报告/周报转成 podcast episode，通勤时听
- **feishu-claudecode-bridge：** 如果团队用飞书，这是手机端 Claude Code 的最佳方案
- **codebase-to-course：** 对 onboarding 新人到 fars-autotrain 等复杂项目有直接价值
- **lark-minutes-tasks 的 Wake Word：** 可以借鉴到 labmate 的会议 → action items 流程
