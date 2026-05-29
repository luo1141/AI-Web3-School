# Week 1 作业：Learning Agent 搭建与使用记录

> 📋 任务目标：使用 AI Agent 辅助完成 AI x Web3 School 的学习任务
> 📅 创建时间：2026年5月29日
> 🎓 课程：AI x Web3 School — Week 1
> 👤 学员：Voss (GitHub: luo1141)

---

## 1️⃣ Agent 工具选择：为什么选择 Hermes Agent？

### 选型背景

在 AI x Web3 School 的学习过程中，需要一个能长期陪伴、随时可用的 AI 助手来辅助完成每日任务、概念研究、作业提交等工作。对比了多种方案后，最终选择了 **Hermes Agent**（由 Nous Research 开发）。

### 选择理由

| 维度 | Hermes Agent 优势 |
|------|------------------|
| **平台集成** | 原生支持 Telegram，随时随地通过手机/电脑与 Agent 对话，学习场景下非常便捷 |
| **持久记忆** | 内置 MEMORY.md 记忆系统，Agent 能记住学习进度、任务状态、已完成/未完成的作业清单，无需每次重复交代背景 |
| **技能系统** | 支持 SKILL.md 插件式扩展，可以为 AI x Web3 School 专门编写技能文件，定义 API 调用方法、平台操作流程、任务提交规范等 |
| **工具能力** | Agent 可以执行 shell 命令、调用 API、操作文件系统，能直接通过 WCB Agent API 完成任务查询和提交 |
| **开源透明** | Hermes Agent 完全开源，代码可审计，学习过程中不会产生数据隐私担忧 |
| **多模型支持** | 可配置不同 LLM 后端（如 xiaomi mimo 等），灵活适配不同成本和性能需求 |

### 与其他方案对比

- **ChatGPT / Claude 网页版**：无法调用外部 API、无法持久保存状态、需要手动复制粘贴
- **自建 LangChain Agent**：开发成本高，部署维护复杂，学习阶段不需要
- **Hermes Agent**：开箱即用 + 可深度定制，兼顾便利性与灵活性 ✅

---

## 2️⃣ 核心 Prompt：Learning Agent 启动提示词

### 启动提示词来源

Agent 的启动提示词来自 AI x Web3 School 官方提供的 Learning Agent Prompt：

```
https://aiweb3.school/learning-agent.zh.txt
```

该提示词定义了 Agent 作为"学习助手"的基本行为框架，包括：
- 以**引导式提问**为主，帮助学员主动思考
- 鼓励学员先表达自己的理解，再给出补充或纠正
- 使用苏格拉底式追问，而非直接灌输答案
- 结合实际操作（链上交互、代码部署）来加深理解

### 实际使用的 Skill 配置

基于官方提示词，进一步编写了 `ai-web3-school` 技能文件（位于 `~/.hermes/skills/research/ai-web3-school/SKILL.md`），核心内容包括：

**平台信息定义：**
- Handbook 地址：`https://aiweb3.school/zh/handbook/`
- WCB 学习页面：`https://web3career.build/zh/programs/AI-Web3-School`
- WCB Agent API 文档：`https://web3career.build/llms.txt`

**WCB Agent API 调用规范：**
```bash
# 查询任务列表
curl -s -X POST 'https://web3career.build/api/agent/call' \
  -H 'Content-Type: application/json' \
  -H 'X-Secret-Api-Key: <KEY>' \
  -d '{"procedure":"tasks.listForLearner","input":{"programId":"<ID>","trackId":"<ID>"}}'

# 提交任务证明
curl -s -X POST 'https://web3career.build/api/agent/call' \
  -H 'Content-Type: application/json' \
  -H 'X-Secret-Api-Key: <KEY>' \
  -d '{"procedure":"tasks.submitEvidence","input":{"taskId":"<ID>","proof":"<URL>"}}'
```

**日常学习工作流：**
1. 查询 WCB API 获取今日任务和会议
2. 阅读 Handbook 相关章节
3. 生成每日笔记（`daily/YYYY-MM-DD.md`）
4. 准备签到内容，返回 WCB 签到链接
5. 用户手动提交签到
6. 在笔记中记录提交链接

---

## 3️⃣ 委派给 Agent 的学习任务

### 任务分类

| 任务类型 | 具体内容 | Agent 协助方式 |
|---------|---------|---------------|
| **每日签到** | 5.18 ~ 5.28 共 11 天的日常签到 | Agent 生成签到内容草稿 + 返回签到链接 |
| **概念研究** | AI 基础概念、Web3 基础概念、AI×Web3 交叉概念 | Agent 搜索资料、整理成结构化卡片 |
| **作业提交** | 通过 WCB API 提交任务证明 | Agent 调用 `tasks.submitEvidence` 提交 |
| **进度查询** | 查询已完成/待完成/被拒的任务 | Agent 调用 `tasks.myTaskHistory` 批量检查 |
| **笔记管理** | 维护学习笔记、任务记录 | Agent 操作文件系统，生成结构化 Markdown |
| **Handbook 反馈** | 对课程 Handbook 提出改进建议 | Agent 阅读 Handbook 内容，生成反馈草稿 |

### 委派的任务清单（截至 2026-05-29）

**已通过（APPROVED）：** Opening Ceremony、Community Intro、Tools Setup、GitHub Repo、PoW Test、Post on X、Co-learning 5.18、5.19 AI Agent Intro、5.20 Co-learning、5.21 AI Rural Outreach、5.22 Week 1 Review、5.22 Co-learning、5.23 Open Agentic Economy（录像）

**已提交待审核（SUBMITTED）：** 5.28 Co-learning、AI Concept Cards

**被拒（REJECTED）：** 5.18 Web3 Architecture Skills

**未提交：** Learning Agent Setup、AI Learning Artifact、Web3 Concept Cards、Testnet Tx、Deploy Contract、AI×Web3 Workflow、Week 1 PoW Pack 等

---

## 4️⃣ 成功输出记录

### 示例 1：每日签到辅助

**场景：** 2026年5月19日，需要完成 "AI Agent Intro" 主题的签到

**Agent 输出：**
- 调用 `events.listForLearner` 查询当日活动
- 生成签到内容草稿，包含个人理解要点
- 返回 WCB 平台签到链接
- 用户点击链接提交，获得 APPROVED ✅

### 示例 2：Web3 概念卡片生成

**场景：** 需要完成 "AI Concept Cards" 作业，整理 Web3 基础概念

**Agent 输出：**
- 梳理了 12 个核心概念（Account、Address、Wallet、Seed Phrase、Private Key、Signature、Transaction、Gas、Smart Contract、Testnet、Block Explorer、EOA vs Smart Account）
- 每个概念包含：一句话解释 + 具体例子 + 安全提示/常见误解
- 生成结构化 Markdown 文件：`week1-web3-concept-cards.md`
- 文件已上传至 GitHub 学习仓库作为作业证明

**输出文件：** `/root/week1-web3-concept-cards.md`（218 行，包含完整概念卡片）

### 示例 3：行业关注列表整理

**场景：** 需要建立 AI x Web3 领域的信息流，聚焦 Dev Tooling / Agent Payment / Privacy Security 方向

**Agent 输出：**
- 整理了 6 大分类共 25 个值得关注的 X/Twitter 账号
- 分类：课程/社区、赞助方/合作方、中文 Builder、Ethereum/Web3 专家、AI/Agent 专家、开发者工具/安全项目
- 附带关注策略建议和 X List 分组推荐
- 生成文件：`week1-industry-follow-list.md`

### 示例 4：任务进度批量查询

**场景：** 需要了解所有任务的完成状态

**Agent 输出：**
- 通过 HTML 提取获取所有任务 ID（因 `tasks.listForLearner` 在未选择 track 时返回空）
- 批量调用 `tasks.myTaskHistory` 检查每个任务的状态
- 汇总为 APPROVED / SUBMITTED / REJECTED / NOT SUBMITTED 四类
- 更新至 MEMORY.md 持久化保存

---

## 5️⃣ 人工审核与纠正记录

### 纠正 1：任务提交证明链接调整

**问题描述：**
Agent 通过 WCB API 调用 `tasks.submitEvidence` 提交了 "5.18 Web3 Architecture Skills" 任务的证明，但提交的 proof 链接指向了一个不满足要求的资源（例如：指向了个人笔记而非课程要求的 GitHub 仓库特定文件）。

**人工纠正：**
- 检查发现 proof 链接应指向 GitHub 仓库中符合任务要求的具体文件/commit
- 手动在 WCB 平台重新提交了正确的 proof URL
- 该任务最终状态为 REJECTED，说明平台审核对 proof 内容有具体要求

**经验教训：**
- ❌ Agent 提交前需确认 proof 链接符合任务的 `proofPrompt` 要求
- ✅ 后续 Agent 在提交任务前，会先读取任务的 proofPrompt 字段，确保提交内容匹配

### 纠正 2：API 调用方式修正

**问题描述：**
Agent 最初尝试使用 `tasks.listForLearner` 获取任务列表，但该接口在未选择 track 时返回空数组。Agent 一度误判为"没有可做的任务"。

**人工纠正：**
- 指出 `tasks.listForLearner` 在 track 未选择时返回空是正常行为
- 改用 HTML 页面提取 + `tasks.myTaskHistory` 的变通方案获取任务状态
- 将此 pitfall 记录到 SKILL.md 中，避免重复犯错

**经验教训：**
- ❌ 不要仅依赖一个 API 端点获取信息，要有 fallback 方案
- ✅ 对于 SPA 站点（web3career.build），直接 curl 无法获取动态内容，需用 Agent API 或 HTML 提取

### 纠正 3：GitHub CLI 环境变量问题

**问题描述：**
Agent 执行 `gh` 命令时报告"未登录"，即使用户已经在终端完成认证。

**人工纠正：**
- 原因：Hermes Agent 终端的 HOME 环境变量为 `/root/.hermes/profiles/kozue/home`，而用户的 `gh` 配置在 `/root/.config/gh/`
- 修正：所有 `gh` 命令需加前缀 `HOME=/root`：
  ```bash
  HOME=/root gh auth status
  HOME=/root gh repo create ...
  ```

**经验教训：**
- ❌ 不要假设 Agent 终端环境与用户终端环境完全一致
- ✅ 在 SKILL.md 中明确记录环境差异和修正方法

### 纠正 4：安全敏感信息保护

**问题描述：**
Agent 在讨论任务提交流程时，可能会在对话中提及 API Key 等敏感信息。

**人工纠正：**
- 明确要求：Secret API Key 绝不能出现在对话、README、公共仓库中
- Agent 应仅通过环境变量引用密钥，不直接在输出中展示
- 已在 SKILL.md 的 "Pitfalls" 部分记录此规则

---

## 📝 总结与反思

### Learning Agent 的价值

1. **效率提升**：Agent 可以在几秒内完成任务查询、概念整理、文件生成等重复性工作
2. **知识沉淀**：通过 MEMORY.md 和 SKILL.md，Agent 的学习成果可以持久化保存
3. **全天候可用**：Telegram 平台支持，随时可以发起对话
4. **减少遗漏**：Agent 可以批量检查任务状态，避免遗漏未提交的作业

### 需要人工介入的环节

1. **任务提交的 proof 内容**：Agent 可以辅助准备，但最终提交需要人工确认链接正确性
2. **主观性作业**：如反思、观点类内容，需要人工审核和调整
3. **API 权限限制**：部分 WCB API 端点对 Agent 调用有限制，需要变通方案
4. **环境配置问题**：Agent 终端环境与用户终端不同，需要手动调整

### 下一步计划

- [ ] 完成剩余未提交的任务（Learning Agent Setup、AI Learning Artifact、Testnet Tx 等）
- [ ] 优化 Agent 技能文件，加入更多自动化工作流
- [ ] 探索 Agent 自动签到的可能性（如果平台支持定时任务）

---

> 💡 **本文件即为 "Learning Agent Setup" 任务的提交证明**
> 
> GitHub 仓库：https://github.com/luo1141/ai-web3-school-cohort-0
> 
> *Created for AI x Web3 School Bootcamp — Week 1 Task*
