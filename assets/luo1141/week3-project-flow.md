# AgentPay SDK — 项目流程图 (文本描述)

> **项目**: AgentPay SDK
> **作者**: Voss (luo1141)
> **日期**: Week 3
> **说明**: 本文档以文本形式描述 AgentPay SDK 的完整工作流程

---

## 1. 整体流程概览

```
┌─────────────────────────────────────────────────────────────────┐
│                      AgentPay SDK 工作流程                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  开发者   │───▶│  SDK     │───▶│  x402    │───▶│  区块链   │  │
│  │  配置    │    │  核心    │    │  协议    │    │  确认    │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │         │
│       ▼               ▼               ▼               ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  AI      │◀───│  收据    │◀───│  USDC    │◀───│  交易    │  │
│  │  Agent   │    │  返回    │    │  转账    │    │  广播    │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 详细流程步骤

### Step 1: 开发者安装 SDK

```
开发者
  │
  ├─▶ npm install agentpay-sdk
  │
  ├─▶ 或
  │
  └─▶ yarn add agentpay-sdk
```

**操作**: 开发者通过包管理器安装 AgentPay SDK
**输入**: npm/yarn 命令
**输出**: SDK 安装到项目依赖中

---

### Step 2: 配置 Smart Account + Session Key

```
开发者
  │
  ├─▶ 导入 SDK
  │   import { AgentPay } from 'agentpay-sdk';
  │
  ├─▶ 初始化 SDK
  │   const agentPay = new AgentPay({
  │     network: 'base-sepolia',
  │     privateKey: '0x...',        // 部署者私钥
  │     rpcUrl: 'https://...',      // RPC 节点
  │   });
  │
  ├─▶ 创建/连接 Smart Account
  │   const smartAccount = await agentPay.createSmartAccount({
  │     type: 'biconomy',           // 或 'zerodev'
  │     owner: '0x...',             // 所有者地址
  │   });
  │
  └─▶ 创建 Session Key
      const sessionKey = await agentPay.createSessionKey({
        smartAccount: smartAccount,
        spender: '0x...',           // Agent 地址
        budget: '1000000',          // 预算 (USDC 最小单位)
        validity: 86400,            // 有效期 (秒)
        allowedRecipients: ['0x...'], // 允许的收款地址
      });
```

**操作**: 配置 Smart Account 和 Session Key
**输入**: 网络配置、私钥、Session Key 参数
**输出**: Smart Account 实例和 Session Key 实例

---

### Step 3: Agent 调用 agentPay.pay(intent)

```
AI Agent
  │
  ├─▶ Agent 识别需要付费的资源
  │   "我需要获取天气数据，需要支付 0.01 USDC"
  │
  ├─▶ Agent 构造支付意图
  │   const intent = {
  │     resource: 'https://api.weather.com/data',
  │     amount: '10000',            // 0.01 USDC (6 位小数)
  │     currency: 'USDC',
  │     recipient: '0x...',         // API 提供商地址
  │     description: 'Weather data access',
  │   };
  │
  └─▶ Agent 调用支付方法
      const result = await agentPay.pay(intent);
```

**操作**: AI Agent 发起支付请求
**输入**: 支付意图 (resource, amount, recipient)
**输出**: 支付结果 (成功/失败)

---

### Step 4: SDK 构造 UserOperation

```
AgentPay SDK
  │
  ├─▶ 接收支付意图
  │
  ├─▶ 验证 Session Key
  │   - 检查预算是否足够
  │   - 检查收款地址是否在允许列表中
  │   - 检查 Session Key 是否过期
  │
  ├─▶ 构造 UserOperation
  │   const userOp = {
  │     sender: smartAccount.address,
  │     nonce: await smartAccount.getNonce(),
  │     callData: encodeFunctionData({
  │       function: 'execute',
  │       args: [
  │         recipient,               // 收款地址
  │         amount,                  // 支付金额
  │         data                     // 附加数据
  │       ]
  │     }),
  │     signature: await signUserOp(userOp, sessionKey),
  │   };
  │
  └─▶ 提交到 Bundler
      const txHash = await bundler.sendUserOp(userOp);
```

**操作**: SDK 构造并提交 UserOperation
**输入**: 支付意图、Session Key
**输出**: 交易哈希 (txHash)

---

### Step 5: x402 支付请求

```
AgentPay SDK
  │
  ├─▶ 向目标服务器发送 HTTP 请求
  │   GET /premium-data HTTP/1.1
  │   Host: api.weather.com
  │   X-PAYMENT: <base64-encoded-payment>
  │
  ├─▶ 服务器返回 402 Payment Required
  │   HTTP/1.1 402 Payment Required
  │   {
  │     "x402Version": 1,
  │     "accepts": [{
  │       "scheme": "exact",
  │       "maxAmountRequired": "10000",
  │       "payTo": "0x...",
  │       "network": "base-sepolia"
  │     }]
  │   }
  │
  ├─▶ SDK 构造支付交易
  │   const paymentTx = {
  │     to: recipient,
  │     value: amount,
  │     data: '0x...',              // USDC transfer calldata
  │   };
  │
  └─▶ 通过 Smart Account 签名并发送
      const txHash = await smartAccount.execute(paymentTx);
```

**操作**: SDK 处理 x402 协议交互
**输入**: HTTP 请求、402 响应
**输出**: 支付交易哈希

---

### Step 6: USDC 转账

```
区块链 (Base Sepolia)
  │
  ├─▶ Bundler 接收 UserOperation
  │
  ├─▶ Entry Point 验证并执行
  │   - 验证签名
  │   - 验证 nonce
  │   - 执行合约调用
  │
  ├─▶ USDC 合约转账
  │   - 从 Smart Account 转出 USDC
  │   - 转入收款地址
  │   - 更新余额
  │
  └─▶ 交易确认
      - 交易被打包进区块
      - 等待确认 (通常几秒)
```

**操作**: 区块链执行 USDC 转账
**输入**: 签名的 UserOperation
**输出**: 已确认的交易

---

### Step 7: 收据返回

```
AgentPay SDK
  │
  ├─▶ 监听交易确认
  │   const receipt = await provider.waitForTransaction(txHash);
  │
  ├─▶ 构造支付收据
  │   const paymentReceipt = {
  │     txHash: '0x...',
  │     blockNumber: 12345678,
  │     amount: '10000',
  │     currency: 'USDC',
  │     recipient: '0x...',
  │     payer: smartAccount.address,
  │     timestamp: Date.now(),
  │     status: 'confirmed',
  │   };
  │
  └─▶ 返回收据给 Agent
      return {
        success: true,
        receipt: paymentReceipt,
        resource: await fetchResource(resourceUrl),
      };
```

**操作**: SDK 返回支付收据
**输入**: 交易哈希
**输出**: 支付收据和资源数据

---

### Step 8: Agent 继续任务

```
AI Agent
  │
  ├─▶ 收到支付成功结果
  │
  ├─▶ 获取资源数据
  │   const weatherData = result.resource;
  │
  ├─▶ 继续执行任务
  │   "已获取天气数据：北京，晴，25°C"
  │
  └─▶ 返回最终结果给用户
      "根据天气数据，建议您今天穿短袖出门"
```

**操作**: Agent 使用获取的数据继续任务
**输入**: 支付收据和资源数据
**输出**: 最终任务结果

---

## 3. 错误路径

### 3.1 错误路径 1: Session Key 预算不足

```
Agent 调用 agentPay.pay(intent)
  │
  ├─▶ SDK 验证 Session Key
  │   - 检查剩余预算
  │   - 发现: 剩余预算 < 请求金额
  │
  └─▶ 返回错误
      {
        success: false,
        error: 'INSUFFICIENT_BUDGET',
        message: 'Session Key 预算不足',
        remaining: '5000',
        required: '10000'
      }
```

**处理方式**:
- Agent 可以请求用户增加预算
- Agent 可以选择更便宜的替代资源
- Agent 可以创建新的 Session Key

---

### 3.2 错误路径 2: Session Key 过期

```
Agent 调用 agentPay.pay(intent)
  │
  ├─▶ SDK 验证 Session Key
  │   - 检查过期时间
  │   - 发现: 当前时间 > 过期时间
  │
  └─▶ 返回错误
      {
        success: false,
        error: 'SESSION_EXPIRED',
        message: 'Session Key 已过期',
        expiredAt: '2025-01-01T00:00:00Z'
      }
```

**处理方式**:
- Agent 需要请求用户重新创建 Session Key
- 或者使用备用支付方式

---

### 3.3 错误路径 3: 收款地址不允许

```
Agent 调用 agentPay.pay(intent)
  │
  ├─▶ SDK 验证 Session Key
  │   - 检查收款地址是否在允许列表
  │   - 发现: 收款地址不在允许列表
  │
  └─▶ 返回错误
      {
        success: false,
        error: 'RECIPIENT_NOT_ALLOWED',
        message: '收款地址未在允许列表中',
        recipient: '0x...',
        allowedRecipients: ['0x1234...', '0x5678...']
      }
```

**处理方式**:
- Agent 只能向允许的收款地址支付
- 需要用户更新 Session Key 的允许列表

---

### 3.4 错误路径 4: 区块链交易失败

```
SDK 提交 UserOperation
  │
  ├─▶ Bundler 接收交易
  │
  ├─▶ Entry Point 执行失败
  │   - Gas 不足
  │   - 合约调用失败
  │   - Nonce 错误
  │
  └─▶ 返回错误
      {
        success: false,
        error: 'TX_FAILED',
        message: '区块链交易失败',
        txHash: '0x...',
        reason: 'execution reverted: insufficient balance'
      }
```

**处理方式**:
- 检查 Smart Account 余额
- 检查 Gas 费用是否充足
- 检查合约状态是否正确

---

### 3.5 错误路径 5: x402 服务器拒绝

```
SDK 发送 x402 支付请求
  │
  ├─▶ 服务器返回错误
  │   HTTP/1.1 402 Payment Required
  │   {
  │     "error": "INVALID_PAYMENT",
  │     "message": "支付金额不足"
  │   }
  │
  └─▶ 返回错误
      {
        success: false,
        error: 'X402_REJECTED',
        message: '服务器拒绝支付',
        serverMessage: '支付金额不足'
      }
```

**处理方式**:
- 检查支付金额是否满足服务器要求
- 检查收款地址是否正确
- 检查网络是否正确

---

### 3.6 错误路径 6: 网络连接失败

```
SDK 尝试连接区块链
  │
  ├─▶ RPC 节点无响应
  │
  └─▶ 返回错误
      {
        success: false,
        error: 'NETWORK_ERROR',
        message: '无法连接到区块链网络',
        rpcUrl: 'https://...',
        retryable: true
      }
```

**处理方式**:
- 检查网络连接
- 尝试备用 RPC 节点
- 重试请求

---

## 4. 流程状态机

```
                    ┌──────────────┐
                    │   待支付     │
                    │  (Pending)   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ 预算不足  │ │ Session  │ │ 地址不允许│
        │ (Error)  │ │ 过期     │ │ (Error)  │
        └──────────┘ └──────────┘ └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   构造中     │
                    │ (Building)   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ 签名失败  │ │ 构造失败  │ │ 网络错误  │
        │ (Error)  │ │ (Error)  │ │ (Retry)  │
        └──────────┘ └──────────┘ └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   已提交     │
                    │ (Submitted)  │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ 交易失败  │ │ 等待确认  │ │ 超时     │
        │ (Error)  │ │ (Pending)│ │ (Retry)  │
        └──────────┘ └──────────┘ └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   已确认     │
                    │ (Confirmed)  │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   完成      │
                    │ (Completed)  │
                    └──────────────┘
```

---

## 5. 关键数据流

### 5.1 支付意图数据

```typescript
interface PaymentIntent {
  resource: string;        // 请求的资源 URL
  amount: string;          // 支付金额 (最小单位)
  currency: string;        // 支付代币 (USDC)
  recipient: string;       // 收款地址
  description?: string;    // 支付描述
  metadata?: Record<string, any>; // 附加数据
}
```

### 5.2 UserOperation 数据

```typescript
interface UserOperation {
  sender: string;          // Smart Account 地址
  nonce: bigint;           // Nonce
  callData: string;        // 合约调用数据
  callGasLimit: bigint;    // Gas 限制
  verificationGasLimit: bigint;
  preVerificationGas: bigint;
  maxFeePerGas: bigint;
  maxPriorityFeePerGas: bigint;
  paymasterAndData: string;
  signature: string;       // Session Key 签名
}
```

### 5.3 支付收据数据

```typescript
interface PaymentReceipt {
  txHash: string;          // 交易哈希
  blockNumber: number;     // 区块号
  amount: string;          // 实际支付金额
  currency: string;        // 支付代币
  recipient: string;       // 收款地址
  payer: string;           // 支付者 (Smart Account)
  timestamp: number;       // 时间戳
  status: 'confirmed' | 'pending' | 'failed';
}
```

---

*流程文档版本: v1.0*
*最后更新: Week 3*
