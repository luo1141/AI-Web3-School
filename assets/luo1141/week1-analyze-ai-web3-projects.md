# Week 1 - AI×Web3 项目分析

> 作者: Voss (luo1141) | 日期: 2026-06-10
> 背景: AI + Web3 | 方向: 隐私安全与主权 AI

---

## 项目一：Phala Network — TEE + AI 计算

### 1. AI 部分

Phala Network 是一个去中心化的云计算网络，核心 AI 能力体现在：

- **隐私保护 AI 推理**: 借助 TEE（Trusted Execution Environment，Intel SGX/TDX）技术，在硬件隔离环境中执行 AI 模型推理，确保模型和数据在运行时不可被外部（包括节点运营者）窥探
- **Agent 执行环境**: Phala 提供了 Khala Runtime 作为 Agent 的可信执行环境，Agent 可以在 TEE 中运行 LLM 推理、工具调用等操作，保证 Agent 逻辑的机密性和完整性
- **AI Worker 节点**: 网络中的 Worker 节点可提供 GPU 算力，支持大规模 AI 模型的分布式推理和训练

**技术亮点**: TEE 将 AI 计算的信任基础从"信任软件"提升到"信任硬件"，这在当前 AI 模型知识产权保护和数据隐私场景中具有独特价值。

### 2. Web3 部分

- **去中心化计算市场**: 通过区块链经济激励，Worker 节点提供算力并获得 PHA 代币奖励
- **TEE 证明上链**: Worker 节点的 TEE Attestation（远程证明）记录在链上，任何人可以验证计算确实在 TEE 中执行
- **无需许可的计算网络**: 任何持有 GPU 的节点均可加入网络提供算力
- **与 Polkadot 生态集成**: 作为 Polkadot 平行链，共享整个波卡生态的安全性

### 3. 可验证材料

- 📄 官方文档: [https://docs.phala.network/](https://docs.phala.network/)
- 📄 白皮书: [https://github.com/Phala-Network/whitepaper](https://github.com/Phala-Network/whitepaper)
- 📄 GitHub: [https://github.com/Phala-Network](https://github.com/Phala-Network)
- 📄 Subscan (链上数据): [https://khala.subscan.io/](https://khala.subscan.io/)
- 📄 CoinGecko 市场数据: [https://www.coingecko.com/en/coins/phala](https://www.coingecko.com/en/coins/phala)

### 4. 个人判断与洞察

**优势分析**:
- TEE 技术是当前隐私 AI 计算最成熟的方案之一，无需复杂的密码学证明（如 ZKP），性能损失相对可控
- 已在波卡生态中运行多年，有一定的技术积累和社区基础
- AI + TEE 的组合对"可信 Agent"场景非常有意义——Agent 的推理过程可以被验证为在安全环境中执行

**潜在问题**:
- Intel SGX/TDX 本身存在已知攻击面（如侧信道攻击），TEE 不是万无一失的
- 市场竞争激烈，Akash Network、Render Network 等也在提供去中心化算力
- PHA 代币经济学的可持续性需要验证

**待研究问题**:
1. Phala 的 TEE 方案在面对 AI 模型规模增长（如 70B+ 参数）时，性能瓶颈在哪里？
2. TEE Attestation 的上链成本和延迟如何？是否适合高频 AI 推理场景？
3. 与 Oasis Network、Secret Network 等隐私计算项目的差异化在哪里？

---

## 项目二：Ritual — 链上 AI 推理

### 1. AI 部分

Ritual 致力于将 AI 推理能力直接嵌入区块链基础设施：

- **链上 AI 推理**: Ritual 的核心是构建一个去中心化的 AI 推理网络，任何智能合约都可以直接调用 AI 模型进行推理
- **模型注册与分发**: AI 模型可以在 Ritual 网络中注册，节点根据需求加载模型并执行推理
- **Infernet SDK**: 提供了开发者工具包，允许智能合约通过简单接口调用链下 AI 模型，实现"AI 原生"的智能合约
- **支持多种模型**: 不仅支持 LLM，还支持图像生成、音频处理等多模态 AI 任务

**技术亮点**: Ritual 将 AI 推理变成了一种链上可调用的"服务"，类似于 Chainlink 为预言机所做的事，但针对的是更复杂的 AI 计算。

### 2. Web3 部分

- **去中心化推理网络**: 节点运营者提供 GPU 算力执行 AI 推理，获得经济激励
- **链上验证**: 推理结果通过密码学证明（如 ZK 证明）确保计算正确性
- **智能合约集成**: 通过 Infernet，开发者可以让 Solidity 合约直接调用 AI 推理，实现 AI × DeFi 的原生组合
- **模块化架构**: 推理网络作为基础设施层，可服务于任意链、任意应用

### 3. 可验证材料

- 📄 官方网站: [https://ritual.net/](https://ritual.net/)
- 📄 博客: [https://ritual.net/blog](https://ritual.net/blog)
- 📄 GitHub (Infernet): [https://github.com/ritual-net/infernet](https://github.com/ritual-net/infernet)
- 📄 融资信息: Ritual 在 2024 年完成 1200 万美元融资，Archetype 领投（The Block 报道）
- 📄 技术文档: [https://docs.ritual.net/](https://docs.ritual.net/)

### 4. 个人判断与洞察

**优势分析**:
- 定位清晰：做 AI × Web3 的基础设施层，而非应用层。这种"卖铲子"策略在早期可能更有生命力
- Infernet SDK 的设计理念很好——让智能合约原生调用 AI，这是 DeFi × AI 的关键拼图
- 融资背景强，团队技术实力有保障

**潜在问题**:
- 链上 AI 推理的延迟和成本问题尚未完全解决。LLM 推理需要秒级延迟，但链上确认需要区块时间
- 如何保证推理结果的可信度？ZK 证明生成 AI 推理结果的计算开销巨大
- 与 Bittensor、Nosana 等项目的差异化需要更明确

**待研究问题**:
1. Ritual 的推理延迟目前能达到什么水平？对于实时 DeFi 策略是否可用？
2. ZK 证明验证 AI 推理结果的可行性如何？是否有更轻量级的验证方案？
3. Infernet 的实际开发者采用情况如何？是否有成功的 dApp 集成案例？

---

## 三、对比总结

| 维度 | Phala Network | Ritual |
|------|---------------|--------|
| **核心定位** | 隐私保护的去中心化计算 | 链上 AI 推理基础设施 |
| **AI 能力** | TEE 内执行 AI 推理 | 智能合约调用 AI 推理 |
| **隐私保护** | ✅ TEE 硬件隔离 | ⚠️ 依赖 ZK 证明（部分） |
| **开发者体验** | 中等（需理解 TEE 概念） | 较好（SDK 简化集成） |
| **成熟度** | 较高（已运行多年） | 较低（仍在早期） |
| **生态** | Polkadot | 多链 |
| **Agent 适用性** | ⭐⭐⭐⭐（可信执行环境） | ⭐⭐⭐⭐⭐（AI 原生合约） |

## 四、综合洞察

两个项目代表了 AI × Web3 融合的两种不同路径：

1. **Phala** = "在安全环境中运行 AI"（隐私优先）
2. **Ritual** = "让 AI 成为链上原生能力"（功能优先）

对于我的方向（隐私安全与主权 AI），Phala 的 TEE 方案更有参考价值。对于 Agent 自动化方向，Ritual 的 Infernet 提供了更直接的集成路径。两者都有可能成为未来 Agent 经济的基础设施。
