# 📦 Repo Skeleton — AgentPay SDK

## 目录结构

```
agentpay-sdk/
├── src/                          # 核心 SDK 代码
│   ├── core/                     # 核心模块
│   │   ├── agent-pay.ts          # AgentPay 主入口
│   │   ├── types.ts              # 类型定义
│   │   └── constants.ts          # 常量配置
│   ├── providers/                # 支付提供方
│   │   ├── x402-provider.ts      # x402 协议提供方
│   │   ├── smart-account.ts      # Smart Account 封装
│   │   └── session-key.ts        # Session Key 管理
│   ├── utils/                    # 工具函数
│   │   ├── signer.ts             # 签名工具
│   │   ├── validation.ts         # 参数校验
│   │   └── formatting.ts         # 格式化工具
│   └── index.ts                  # SDK 导出入口
├── examples/                     # 示例代码
│   ├── basic-payment/            # 基础支付示例
│   │   └── basic.ts
│   ├── multi-agent/              # 多 Agent 协作示例
│   │   └── multi-agent.ts
│   └── escrow/                   # 托管支付示例
│       └── escrow.ts
├── docs/                         # 文档
│   ├── quickstart.md             # 快速开始指南
│   ├── api-reference.md          # API 参考文档
│   ├── architecture.md           # 架构设计文档
│   └── examples.md               # 示例说明
├── tests/                        # 测试文件
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   └── fixtures/                 # 测试数据
├── .github/                      # GitHub Actions CI
│   └── workflows/
│       ├── ci.yml                # CI 流水线
│       └── release.yml           # 发布流水线
├── package.json                  # 项目配置
├── tsconfig.json                 # TypeScript 配置
├── README.md                     # 项目 README
├── LICENSE                       # 开源协议
└── .gitignore                    # Git 忽略配置
```

---

## package.json 配置

```json
{
  "name": "agentpay-sdk",
  "version": "0.1.0",
  "description": "让 AI Agent 安全自主支付的开发者工具包",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/",
    "format": "prettier --write src/",
    "example:basic": "ts-node examples/basic-payment/basic.ts",
    "example:multi": "ts-node examples/multi-agent/multi-agent.ts",
    "example:escrow": "ts-node examples/escrow/escrow.ts"
  },
  "dependencies": {
    "viem": "^2.0.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "vitest": "^1.0.0",
    "@types/node": "^20.0.0"
  },
  "peerDependencies": {
    "viem": ">=2.0.0"
  }
}
```

---

## README 模板

```markdown
# AgentPay SDK 🔐

让 AI Agent 安全自主支付的开发者工具包。

## 安装

npm install agentpay-sdk

## 快速开始

import { AgentPay } from 'agentpay-sdk';

const agent = new AgentPay({
  privateKey: '0x...',
  rpcUrl: 'https://sepolia.infura.io/v3/YOUR_KEY'
});

// Agent 支付示例
const tx = await agent.pay({
  to: '0x...',
  amount: '1000000',  // 1 USDC (6 decimals)
  currency: 'USDC'
});

console.log('支付成功:', tx.hash);

## 文档

- [快速开始](./docs/quickstart.md)
- [API 参考](./docs/api-reference.md)
- [架构设计](./docs/architecture.md)

## 许可证

MIT
```

---

## GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - run: npm test
      - run: npm run lint
```

---

## 测试策略

| 测试类型 | 覆盖范围 | 工具 |
|----------|----------|------|
| 单元测试 | 工具函数、类型校验 | Vitest |
| 集成测试 | SDK 核心流程 | Vitest + Mock |
| E2E 测试 | 完整支付流程 | Vitest + 测试网 |

**测试目标：** 核心模块测试覆盖率 ≥ 80%

---

## 快速开始步骤

```bash
# 克隆仓库
git clone https://github.com/luo1141/agentpay-sdk.git

# 安装依赖
cd agentpay-sdk
npm install

# 开发模式
npm run dev

# 运行测试
npm test

# 构建
npm run build
```
