# Week 2: AI×Web3 问题图谱与方向选择

> 作者: Voss (luo1141)
> 日期: 2026-06-10
> 主题: AI×Web3 方向研究与路线选择

---

## 一、全景问题图谱

AI Agent 正在从"对话工具"进化为"自主行动者"，而 Web3 提供了身份、支付、隐私等基础设施层。我们将整个栈分为五层，逐层分析痛点与机会。

### 1.1 身份层 (Identity Layer)

**核心技术**: ERC-8004, MCP (Model Context Protocol), DID

| 维度 | 内容 |
|------|------|
| **痛点** | Agent 没有统一的链上身份；不同平台的 Agent 无法互认；身份与钱包绑定导致隐私泄露 |
| **现有方案** | ERC-8004 为 AI Agent 提出标准化身份表示；MCP 提供工具发现与调用协议；ENS/DID 提供去中心化标识 |
| **机会** | 构建 Agent 原生身份标准，让 Agent 能跨平台、跨链证明身份；将身份与能力声明（capability）绑定 |

### 1.2 钱包/权限层 (Wallet/Permission Layer)

**核心技术**: Smart Account (ERC-4337), Session Key, Pact Protocol

| 维度 | 内容 |
|------|------|
| **痛点** | EOA 钱包无法满足 Agent 自主操作需求；权限粒度太粗；缺乏时间/金额/功能的多维限制 |
| **现有方案** | Smart Account 支持多签、Gas Sponsor、批量交易；Session Key 允许临时授权特定功能；Pact 提供意图声明机制 |
| **机会** | 设计 Agent 专用的权限分层模型，让 Agent 在受控范围内自主执行，同时保留人类的最终控制权 |

### 1.3 支付层 (Payment Layer)

**核心技术**: x402, USDC, Gasless (Bundler/Paymaster)

| 维度 | 内容 |
|------|------|
| **痛点** | Agent 无法自主发起支付；M2M (Machine-to-Machine) 支付缺乏标准；传统支付渠道延迟高、手续费贵 |
| **现有方案** | x402 协议复用 HTTP 402 状态码实现机器间微支付；USDC 提供稳定币计价；Gasless 方案让用户免 Gas |
| **机会** | x402 + Smart Account 组合可实现 Agent 自主支付闭环；USDC on Base/L2 降低摩擦成本 |

### 1.4 隐私层 (Privacy Layer)

**核心技术**: ZK (零知识证明), TEE (可信执行环境)

| 维度 | 内容 |
|------|------|
| **痛点** | Agent 交易记录完全公开；用户偏好和行为模式可被追踪；多 Agent 协作时数据泄露风险大 |
| **现有方案** | ZK-SNARKs 可验证计算结果而不暴露输入；TEE 提供硬件级隐私保护；Azimuth/Scroll 等 ZK-Rollup |
| **机会** | 隐私支付 + 可验证计算的组合，让 Agent 既能证明执行了任务，又不暴露敏感数据 |

### 1.5 开发工具层 (Dev Tooling Layer)

**核心技术**: Agent SDK, Framework, Testing

| 维度 | 内容 |
|------|------|
| **痛点** | 开发 Agent + Web3 应用需要理解多个协议，学习曲线陡峭；缺乏统一的支付 SDK；调试和监控工具不完善 |
| **现有方案** | LangChain/AutoGPT 提供 Agent 框架；Viem/Ethers 提供链上交互；Coinbase Toolkit 简化支付集成 |
| **机会** | 构建面向 Agent 开发者的全栈工具链，降低 Web3 集成门槛 |

---

## 二、方向选择分析

### 2.1 候选方向对比

| 方向 | 技术成熟度 | 市场需求 | 竞争强度 | 个人匹配度 | 综合评分 |
|------|-----------|---------|---------|-----------|---------|
| Agent Payment & Commerce | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **4.25** |
| Dev Tooling & Automation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 3.75 |
| Privacy Security & Sovereign AI | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 3.25 |

### 2.2 选定方向: Agent Payment & Commerce

**聚焦: x402 + Smart Account**

#### 选择理由

1. **基础设施成熟**: x402 协议已经定义了 M2M 支付标准，USDC 在 L2 上的交易成本极低（< $0.01），ERC-4337 Smart Account 已被主流钱包支持。

2. **需求真实且迫切**: AI Agent 正在从"聊天"走向"行动"，支付是最核心的行动能力之一。没有支付能力的 Agent 只是一个高级聊天机器人。

3. **技术匹配度高**: 我的 Python AI Tooling 背景可以直接用于构建支付 SDK；Agent Workflows 经验帮助设计自主支付循环；Product Strategy 能力用于产品化。

4. **市场窗口期**: Agent 支付仍处于早期，x402 刚刚获得关注，现在进入可以成为该领域的早期贡献者。

5. **差异化空间**: 现有方案（Cobo, Safe）主要面向人类用户，缺乏 Agent 专用的支付流程设计和权限模型。

### 2.3 核心假设

> **假设 1**: x402 协议会成为 Agent M2M 支付的事实标准
> **假设 2**: 开发者需要一个简单易用的 SDK 来集成 Agent 支付能力
> **假设 3**: Smart Account + Session Key 是 Agent 自主操作的最佳权限模型

---

## 三、下一步行动

- [ ] 深入研究 x402 协议规范与实现
- [ ] 分析 x402 在 Base/L2 上的性能和成本
- [ ] 设计最小可行的 Agent 支付 SDK 架构
- [ ] 与 Z.AI 生态对接，探索集成可能

---

*本文档为 Week 2 方向研究输出，后续将基于选定方向展开深入分析。*
