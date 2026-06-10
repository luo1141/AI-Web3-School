# Week 1 - AI×Web3 学习总结

> 作者: Voss (luo1141) | 日期: 2026-06-10
> GitHub: [luo1141](https://github.com/luo1141)
> 方向: Dev Tooling & Automation / Agent Payment & Commerce / Privacy Security & Sovereign AI

---

## 一、本周学习内容

### AI 基础知识

| 主题 | 核心内容 | 掌握程度 |
|------|---------|---------|
| **LLM（大语言模型）** | Transformer 架构、Token 化、推理机制、Prompt Engineering | ⭐⭐⭐⭐ |
| **Agent（AI 代理）** | Agent 循环、工具调用（Tool Use）、ReAct 模式、规划能力 | ⭐⭐⭐⭐ |
| **MCP（Model Context Protocol）** | Anthropic 的开放协议、Server-Client 架构、工具和资源定义 | ⭐⭐⭐ |

**关键理解**:
- LLM 是"大脑"，Agent 是"身体"，MCP 是"神经系统"
- Agent 的核心能力不是"聪明"，而是"可组合"——通过工具调用连接现实世界
- MCP 为 Agent 提供了标准化的工具接口，类似于 USB 之于外设

### Web3 基础知识

| 主题 | 核心内容 | 掌握程度 |
|------|---------|---------|
| **钱包** | EOA vs 智能账户、私钥管理、Account Abstraction | ⭐⭐⭐⭐ |
| **智能合约** | Solidity 基础、ERC 标准、合约部署与交互 | ⭐⭐⭐ |
| **测试网** | Sepolia/Goerli、水龙头获取测试 Token、链上交互 | ⭐⭐⭐⭐ |

**关键理解**:
- Web3 的核心价值不是"去中心化"本身，而是"无需许可的可编程性"
- 智能合约让"代码即法律"成为可能，但也意味着漏洞即损失
- 测试网是 Agent 开发的安全沙箱，必须养成先在测试网验证的习惯

---

## 二、AI×Web3 交叉领域的关键洞察

### 洞察 1：Agent 需要 Web3 的三个原因
1. **自主支付**: Agent 需要独立的金融身份来完成交易，Web3 钱包提供了这个能力
2. **无需许可**: Agent 需要 24/7 自动化操作，Web3 协议没有"营业时间"限制
3. **可验证性**: Agent 的决策和执行需要可审计，区块链提供了不可篡改的记录

### 洞察 2：Web3 需要 AI 的两个原因
1. **复杂性管理**: DeFi 协议日益复杂，AI 可以帮助用户理解和操作
2. **自动化策略**: 链上数据丰富但处理成本高，AI 可以实时分析并执行策略

### 洞察 3：融合的最大挑战
- **安全性**: Agent + 资产 = 高风险。需要严格的权限管理和人在回路中机制
- **延迟**: LLM 推理需要秒级时间，链上确认需要区块时间，实时交互困难
- **成本**: AI 推理 + Gas 费的双重成本，需要精心优化

---

## 三、工具环境搭建

### 已完成配置

| 工具 | 用途 | 状态 |
|------|------|------|
| **Hermes Agent** | AI Agent 运行环境，支持工具调用和自主决策 | ✅ 已配置 |
| **GitHub** | 代码管理、学习记录、PoW 提交 | ✅ 已使用 |
| **WCB (Web3 CB)** | Web3 学习社区和任务管理 | ✅ 已加入 |
| **MetaMask** | 测试网钱包，用于链上交互 | ✅ 已配置 |
| **Remix IDE** | 智能合约开发和部署 | ✅ 可用 |
| **Node.js / npm** | 开发环境基础 | ✅ 已安装 |

---

## 四、遇到的挑战

### 挑战 1：Agent 钱包交互的安全性
- **问题**: Agent 直接持有私钥存在安全风险
- **解决方向**: 研究 Session Key 和 Account Abstraction 方案，实现权限隔离

### 挑战 2：测试网环境的不稳定性
- **问题**: 测试网水龙头有时不可用，RPC 节点偶尔延迟
- **解决方向**: 配置多个 RPC 源，准备备用测试 Token 获取方式

### 挑战 3：AI 与 Web3 概念的融合理解
- **问题**: 初期容易将两个领域割裂看待，难以找到真正的交叉点
- **解决方向**: 通过项目分析（如 Phala、Ritual）理解融合的商业模式

### 挑战 4：学习节奏管理
- **问题**: AI 和 Web3 两个领域的知识量都很大，容易陷入"什么都学但什么都不精"
- **解决方向**: 聚焦自己的方向（Dev Tooling & Agent Payment），以项目驱动学习

---

## 五、未来目标

### 短期（Week 2-4）
- [ ] 完成 Agent + 测试网 Token Swap 的原型开发
- [ ] 实现 Hermes Agent 的 MCP Server 扩展
- [ ] 深入研究 Account Abstraction (ERC-4337) 的实现细节

### 中期（Month 2-3）
- [ ] 构建一个可工作的 AI Agent DeFi 助手原型
- [ ] 研究 TEE 在 AI Agent 安全中的应用
- [ ] 参与至少一个 AI×Web3 项目的社区贡献

### 长期（School 结束后）
- [ ] 发布一个开源的 Agent + Web3 工具库
- [ ] 探索 Agent 支付的商业模式
- [ ] 建立 AI×Web3 方向的技术影响力

---

## 六、提交作品链接

| 作品 | 链接 |
|------|------|
| AI 概念卡片 | [AI Concept Cards](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |
| 学习 Agent 搭建 | [Learning Agent Setup](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |
| AI 作品 | [AI Artifact](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |
| Web3 概念卡片 | [Web3 Concept Cards](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |
| AI×Web3 工作流 | [AI×Web3 Workflow](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |
| 行业关注清单 | [Industry Follow List](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |
| Week 1 PoW Pack | [Week 1 PoW Pack](https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/) |

---

## 七、总结

Week 1 的核心收获是理解了 **AI × Web3 融合的本质不是技术叠加，而是范式转变**。Agent 需要 Web3 提供的自主金融身份和无需许可的基础设施，Web3 需要 AI 提供的智能分析和自动化能力。这个交叉领域刚刚起步，充满机会。

作为有 AI + Web3 背景的开发者，我的优势在于能够同时理解两个领域，我的方向（Dev Tooling & Agent Payment）正好处于交叉点的核心。Week 2 将开始动手实践，将学习转化为可运行的原型。
