# AgentPay SDK

<p align="center">
  <strong>🤖 AI Agent Payment SDK — 让 AI Agent 自主支付</strong>
</p>

<p align="center">
  <a href="https://github.com/luo1141/AI-Web3-School/blob/main/assets/luo1141/">GitHub</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#架构设计">架构</a> •
  <a href="#演示">演示</a> •
  <a href="#api-文档">API</a> •
  <a href="#贡献指南">贡献</a>
</p>

---

## 📖 项目描述

**AgentPay SDK** 是一个专为 AI Agent 设计的支付 SDK，让 AI Agent 能够自主完成链上支付。

传统支付方式需要人工介入，无法满足 AI Agent 的自主决策需求。AgentPay SDK 通过整合 **x402 支付协议**、**Smart Account (ERC-4337)** 和 **Session Key** 技术，实现了:

- 🤖 **Agent 自主支付**: AI Agent 可以自动完成支付决策和执行
- 💰 **预算控制**: 通过 Session Key 设置支付预算上限
- 🔐 **安全隔离**: Smart Account 提供资金安全隔离
- ⚡ **即时结算**: 基于 L2 网络，支付秒级确认
- 📝 **链上可追溯**: 所有支付记录可在区块链上验证

### 为什么需要 AgentPay?

| 场景 | 传统方式 | AgentPay SDK |
|------|----------|--------------|
| Agent 购买 API | 需要人工登录、输入密码 | Agent 自动支付，无需干预 |
| Agent 购买数据 | 需要绑定信用卡 | 使用 USDC，无银行依赖 |
| Agent 订阅服务 | 需要定期人工续费 | Session Key 自动续期 |
| Agent 间交易 | 需要中间平台 | 点对点支付，无中间人 |

---

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      AI Agent Layer                         │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Data Agent │    │  API Agent  │    │  Service    │     │
│  │  (数据代理)  │    │  (API代理)  │    │  Agent      │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    AgentPay SDK Layer                       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  agentPay.pay(intent)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  x402       │    │  Smart      │    │  Session    │     │
│  │  Protocol   │    │  Account    │    │  Key        │     │
│  │  (支付协议)  │    │  (智能账户) │    │  (会话密钥) │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   Blockchain Layer                          │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Base       │    │  EntryPoint │    │  USDC       │     │
│  │  (L2 网络)  │    │  (入口点)   │    │  (稳定币)   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件

| 组件 | 职责 | 技术 |
|------|------|------|
| **x402 Protocol** | HTTP 原生支付协议 | Stripe/Coinbase 实现 |
| **Smart Account** | 资金管理和 Gas 代付 | ERC-4337 (Biconomy/ZeroDev) |
| **Session Key** | 权限和预算控制 | 合约级授权 |
| **AgentPay Core** | 统一支付接口 | TypeScript SDK |

---

## 🚀 快速开始

### 安装

```bash
npm install agentpay-sdk
# 或
yarn add agentpay-sdk
```

### 基础用法

```typescript
import { AgentPay } from 'agentpay-sdk';

// 1. 初始化 SDK
const agentPay = new AgentPay({
  network: 'base-sepolia',
  privateKey: '0x...',  // 部署者私钥
  rpcUrl: 'https://base-sepolia.g.alchemy.com/v2/YOUR_KEY',
});

// 2. 创建 Smart Account
const smartAccount = await agentPay.createSmartAccount({
  type: 'biconomy',
});

// 3. 创建 Session Key
const sessionKey = await agentPay.createSessionKey({
  budget: '1000000',  // 1 USDC (6 位小数)
  validity: 86400,    // 24 小时
  allowedRecipients: ['0x...'],  // 允许的收款地址
});

// 4. 发起支付
const result = await agentPay.pay({
  resource: 'https://api.example.com/data',
  amount: '10000',  // 0.01 USDC
  recipient: '0x...',
});

console.log('支付结果:', result);
```

### 高级用法: Agent 自动支付

```typescript
import { AgentPay, SessionKey } from 'agentpay-sdk';

// Agent 自动支付场景
async function agentAutoPayment(agent: AIAssistant) {
  const agentPay = new AgentPay({
    network: 'base-sepolia',
    smartAccount: smartAccount,
    sessionKey: sessionKey,
  });

  // Agent 发现需要付费的资源
  const needPayment = await agent.checkResourceAccess('https://api.premium.com/data');

  if (needPayment) {
    // Agent 自动发起支付
    const result = await agentPay.pay({
      resource: 'https://api.premium.com/data',
      amount: '50000',  // 0.05 USDC
      recipient: '0x...',
    });

    if (result.success) {
      // 支付成功，继续获取资源
      const data = await agent.fetchResource('https://api.premium.com/data');
      return data;
    }
  }
}
```

---

## 🎬 演示

### 演示场景: AI Agent 购买 API 访问权限

**场景描述**:
- AI Agent 需要获取天气数据
- 天气 API 需要付费 (0.01 USDC)
- Agent 自动完成支付并获取数据

**演示流程**:

```
1. 用户: "帮我查一下北京的天气"
2. Agent: "我需要访问天气 API，需要支付 0.01 USDC"
3. Agent: 调用 agentPay.pay() → 自动支付
4. Agent: "支付成功！北京今天晴，25°C"
5. Agent: "建议您穿短袖出门 ☀️"
```

**演示代码**:

```typescript
// demo.ts
import { AgentPay } from 'agentpay-sdk';

async function demo() {
  console.log('🤖 AI Agent 天气查询演示\n');

  // 初始化
  const agentPay = new AgentPay({
    network: 'base-sepolia',
    privateKey: process.env.PRIVATE_KEY,
  });

  // Agent 查询天气
  console.log('1️⃣ Agent 检查天气 API...');
  const weatherAPI = {
    url: 'https://api.weather.com/beijing',
    price: '10000',  // 0.01 USDC
    recipient: '0x...',
  };

  // 自动支付
  console.log('2️⃣ Agent 自动支付...');
  const result = await agentPay.pay({
    resource: weatherAPI.url,
    amount: weatherAPI.price,
    recipient: weatherAPI.recipient,
  });

  if (result.success) {
    console.log('3️⃣ 支付成功! 获取天气数据...');
    console.log('   交易哈希:', result.receipt.txHash);
    console.log('   支付金额: 0.01 USDC');

    // 模拟天气数据
    const weather = {
      city: '北京',
      weather: '晴',
      temperature: 25,
      suggestion: '建议穿短袖出门',
    };

    console.log('\n🌤️ 天气结果:');
    console.log(`   城市: ${weather.city}`);
    console.log(`   天气: ${weather.weather}`);
    console.log(`   温度: ${weather.temperature}°C`);
    console.log(`   建议: ${weather.suggestion}`);
  }
}

demo();
```

---

## 📚 API 文档

### AgentPay

```typescript
class AgentPay {
  constructor(config: AgentPayConfig);

  // 创建 Smart Account
  createSmartAccount(options: SmartAccountOptions): Promise<SmartAccount>;

  // 创建 Session Key
  createSessionKey(options: SessionKeyOptions): Promise<SessionKey>;

  // 发起支付
  pay(intent: PaymentIntent): Promise<PaymentResult>;

  // 验证支付
  verify(txHash: string): Promise<PaymentReceipt>;
}
```

### PaymentIntent

```typescript
interface PaymentIntent {
  resource: string;        // 请求的资源 URL
  amount: string;          // 支付金额 (最小单位)
  currency: string;        // 支付代币 (USDC)
  recipient: string;       // 收款地址
  description?: string;    // 支付描述
}
```

### PaymentResult

```typescript
interface PaymentResult {
  success: boolean;
  receipt?: PaymentReceipt;
  error?: string;
  message?: string;
}
```

### SessionKeyOptions

```typescript
interface SessionKeyOptions {
  budget: string;              // 预算 (最小单位)
  validity: number;            // 有效期 (秒)
  allowedRecipients: string[]; // 允许的收款地址
  maxPerTransaction?: string;  // 单笔最大金额
}
```

---

## ⚠️ 限制

- **测试网**: 目前仅支持 Base Sepolia 测试网
- **代币**: 仅支持 USDC 支付
- **网络**: 仅支持 Base L2 网络
- **Gas**: 需要 Smart Account 中有 ETH 用于 Gas (或使用 Gasless)
- **确认时间**: L2 交易确认需要几秒

---

## 🔮 未来工作

- [ ] 支持更多 L2 网络 (Arbitrum, Optimism, Polygon)
- [ ] 支持更多支付代币 (USDT, DAI, ETH)
- [ ] 实现 Gasless 支付 (Paymaster)
- [ ] 添加支付历史记录功能
- [ ] 实现多签支付 (Multi-sig)
- [ ] 支持法币入金 (Fiat On-ramp)
- [ ] 添加支付分析仪表板
- [ ] 实现跨链支付

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/luo1141/AgentPay-SDK.git

# 安装依赖
npm install

# 运行测试
npm test

# 运行示例
npm run demo
```

### 代码规范

- 使用 TypeScript
- 遵循 ESLint 规则
- 编写单元测试
- 更新文档

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [Stripe](https://stripe.com/) - x402 协议实现
- [Coinbase](https://www.coinbase.com/) - Base 网络支持
- [Biconomy](https://biconomy.io/) - Smart Account SDK
- [ZeroDev](https://zerodev.app/) - Session Key 实现
- [Viem](https://viem.sh/) - 以太坊工具库

---

<p align="center">
  <strong>AgentPay SDK</strong> — 让 AI Agent 拥有钱包 🤖💰
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/luo1141">Voss (luo1141)</a>
</p>
