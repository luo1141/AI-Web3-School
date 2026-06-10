# AgentPay SDK — 技术验证计划

> **项目**: AgentPay SDK
> **作者**: Voss (luo1141)
> **日期**: Week 3
> **目的**: 验证 AgentPay SDK 核心功能的可行性

---

## 总览

本文档列出了 4 个核心技术验证点，每个验证点包含测试方法、预期结果和通过/失败标准。

**验证环境**:
- 网络: Base Sepolia (测试网)
- 代币: USDC (Base Sepolia 版本)
- Smart Account: Biconomy / ZeroDev
- RPC: Alchemy / Infura (Base Sepolia)

---

## 验证 1: 连接 Sepolia Smart Account

### 验证目标
能否在 Base Sepolia 网络上成功创建和连接一个 Smart Account？

### 测试方法

**步骤 1: 安装依赖**
```bash
npm install @biconomy/account viem
# 或
npm install @zerodev/sdk viem
```

**步骤 2: 编写测试脚本**
```typescript
import { createSmartAccountClient, BiconomySmartAccountV2 } from '@biconomy/account';
import { createPublicClient, http } from 'viem';
import { baseSepolia } from 'viem/chains';

async function testSmartAccountConnection() {
  // 1. 创建 Public Client
  const publicClient = createPublicClient({
    chain: baseSepolia,
    transport: http('https://base-sepolia.g.alchemy.com/v2/YOUR_KEY'),
  });

  // 2. 创建 Smart Account
  const smartAccount = await createSmartAccountClient({
    signer: walletClient,  // 钱包客户端
    bundlerUrl: 'https://bundler.biconomy.io/api/v2/...',
    chainId: baseSepolia.id,
  });

  // 3. 获取 Smart Account 地址
  const address = await smartAccount.getAccountAddress();
  console.log('Smart Account 地址:', address);

  // 4. 验证地址格式
  if (!address.startsWith('0x') || address.length !== 42) {
    throw new Error('地址格式错误');
  }

  return { success: true, address };
}
```

**步骤 3: 运行测试**
```bash
npx ts-node test-smart-account.ts
```

### 预期结果
- Smart Account 地址成功生成
- 地址格式正确 (0x + 40 位十六进制)
- 可以通过 Public Client 查询 Smart Account 信息
- Smart Account 合约已部署 (通过 EntryPoint)

### 通过/失败标准

| 检查项 | 通过标准 | 失败标准 |
|--------|----------|----------|
| 地址生成 | 成功生成 42 位地址 | 无法生成或格式错误 |
| 合约部署 | 合约已存在 (getCode 返回非 0x) | 合约不存在 |
| 余额查询 | 可以查询 USDC 余额 | 查询失败 |
| 签名能力 | 可以用私钥签名 | 签名失败 |

**整体通过条件**: 所有检查项均通过

---

## 验证 2: 创建带预算限制的 Session Key

### 验证目标
能否为 Smart Account 创建一个带有预算限制的 Session Key？

### 测试方法

**步骤 1: 编写测试脚本**
```typescript
import { createSessionKeyManagerModule, createSessionKey } from '@biconomy/account';

async function testSessionKeyCreation() {
  // 1. 连接 Smart Account
  const smartAccount = await connectSmartAccount();

  // 2. 定义 Session Key 参数
  const sessionKeyData = {
    sessionPublicKey: '0x...',           // Agent 的公钥
    validAfter: Math.floor(Date.now() / 1000), // 生效时间
    validUntil: Math.floor(Date.now() / 1000) + 86400, // 过期时间 (24小时)
    permittedModule: '0x...',            // 允许的模块
    sessionData: {
      budget: BigInt('1000000'),         // 预算: 1 USDC (6 位小数)
      spent: BigInt(0),                  // 已花费
      allowedRecipients: ['0x...'],      // 允许的收款地址
      maxPerTransaction: BigInt('100000'), // 单笔最大: 0.1 USDC
    },
  };

  // 3. 创建 Session Key
  const sessionKeyModule = await createSessionKeyManagerModule({
    smartAccount,
    sessionKeys: [sessionKeyData],
  });

  // 4. 安装 Session Key 模块
  const tx = await sessionKeyModule.createSessionKey(sessionKeyData);
  console.log('Session Key 创建交易:', tx.transactionHash);

  // 5. 验证 Session Key
  const isActive = await sessionKeyModule.isSessionKeyActive(
    sessionKeyData.sessionPublicKey
  );
  console.log('Session Key 状态:', isActive ? '活跃' : '未激活');

  return { success: true, txHash: tx.transactionHash };
}
```

**步骤 2: 运行测试**
```bash
npx ts-node test-session-key.ts
```

### 预期结果
- Session Key 成功创建
- 预算限制生效 (1 USDC)
- 收款地址限制生效
- 单笔交易限制生效
- Session Key 状态为活跃

### 通过/失败标准

| 检查项 | 通过标准 | 失败标准 |
|--------|----------|----------|
| Session Key 创建 | 交易成功，返回 txHash | 交易失败 |
| 预算设置 | 预算为 1 USDC | 预算未设置或错误 |
| 收款限制 | 只能向指定地址支付 | 可以向任意地址支付 |
| 时间限制 | 24小时后自动过期 | 无时间限制 |
| 状态查询 | 返回 true (活跃) | 返回 false (未激活) |

**整体通过条件**: 所有检查项均通过

---

## 验证 3: 触发 x402 支付

### 验证目标
能否通过 x402 协议成功触发一笔支付？

### 测试方法

**步骤 1: 设置测试环境**
- 准备一个返回 402 的测试服务器
- 准备一个带有 USDC 余额的 Smart Account
- 准备一个 Session Key

**步骤 2: 编写测试脚本**
```typescript
import { AgentPay } from 'agentpay-sdk'; // 我们的 SDK

async function testX402Payment() {
  // 1. 初始化 SDK
  const agentPay = new AgentPay({
    network: 'base-sepolia',
    smartAccount: smartAccount,
    sessionKey: sessionKey,
  });

  // 2. 定义支付意图
  const intent = {
    resource: 'https://test-server.com/premium-data',
    amount: '10000',  // 0.01 USDC
    currency: 'USDC',
    recipient: '0x...', // 测试收款地址
    description: 'Test payment for premium data',
  };

  // 3. 发起支付
  console.log('发起支付...');
  const result = await agentPay.pay(intent);

  // 4. 检查结果
  if (result.success) {
    console.log('支付成功!');
    console.log('交易哈希:', result.receipt.txHash);
    console.log('支付金额:', result.receipt.amount);
    console.log('收款地址:', result.receipt.recipient);
  } else {
    console.log('支付失败:', result.error);
  }

  return result;
}
```

**步骤 3: 设置测试服务器**
```javascript
// test-server.js
import express from 'express';

const app = express();

app.get('/premium-data', (req, res) => {
  // 检查是否有支付证明
  const payment = req.headers['x-payment'];

  if (!payment) {
    // 返回 402
    return res.status(402).json({
      x402Version: 1,
      accepts: [{
        scheme: 'exact',
        network: 'base-sepolia',
        maxAmountRequired: '10000',
        resource: 'https://test-server.com/premium-data',
        description: 'Premium data access',
        payTo: '0x...',
        extra: {
          asset: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
        },
      }],
    });
  }

  // 验证支付证明 (简化版)
  // 实际应该在链上验证
  console.log('收到支付证明:', payment);

  // 返回资源
  res.json({
    data: 'This is premium data!',
    timestamp: Date.now(),
  });
});

app.listen(3000, () => {
  console.log('测试服务器运行在 http://localhost:3000');
});
```

**步骤 4: 运行测试**
```bash
# 终端 1: 启动测试服务器
node test-server.js

# 终端 2: 运行支付测试
npx ts-node test-x402-payment.ts
```

### 预期结果
- 收到 402 响应
- 正确解析支付需求
- 成功构造支付交易
- 交易被区块链确认
- 收到资源数据

### 通过/失败标准

| 检查项 | 通过标准 | 失败标准 |
|--------|----------|----------|
| 402 响应 | 正确收到并解析 | 解析失败或格式错误 |
| 交易构造 | 成功构造 UserOp | 构造失败 |
| 交易签名 | Session Key 签名成功 | 签名失败 |
| 交易提交 | 交易被 Bundler 接收 | 提交失败 |
| 交易确认 | 交易在链上确认 | 超时或失败 |
| 资源获取 | 成功获取资源数据 | 未获取或数据错误 |

**整体通过条件**: 所有检查项均通过

---

## 验证 4: 链上验证支付

### 验证目标
能否在区块链上验证一笔支付的真实性？

### 测试方法

**步骤 1: 编写测试脚本**
```typescript
import { createPublicClient, http, formatUnits } from 'viem';
import { baseSepolia } from 'viem/chains';
import { ERC20_ABI } from './abis/erc20';

async function testPaymentVerification() {
  // 1. 连接区块链
  const publicClient = createPublicClient({
    chain: baseSepolia,
    transport: http('https://base-sepolia.g.alchemy.com/v2/YOUR_KEY'),
  });

  // 2. 支付信息
  const txHash = '0x...'; // 测试交易哈希
  const expectedRecipient = '0x...'; // 预期收款地址
  const expectedAmount = BigInt('10000'); // 预期金额 (0.01 USDC)
  const usdcAddress = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'; // Base Sepolia USDC

  // 3. 获取交易详情
  const tx = await publicClient.getTransaction({ hash: txHash });
  console.log('交易详情:', tx);

  // 4. 获取交易收据
  const receipt = await publicClient.getTransactionReceipt({ hash: txHash });
  console.log('交易收据:', receipt);

  // 5. 验证交易状态
  if (receipt.status !== 'success') {
    throw new Error('交易失败');
  }

  // 6. 解析 USDC Transfer 事件
  const transferLogs = receipt.logs.filter(
    log => log.address.toLowerCase() === usdcAddress.toLowerCase()
  );

  if (transferLogs.length === 0) {
    throw new Error('未找到 USDC Transfer 事件');
  }

  // 7. 解析事件数据
  const transferLog = transferLogs[0];
  const decodedLog = decodeTransferLog(transferLog);

  // 8. 验证收款地址
  if (decodedLog.to.toLowerCase() !== expectedRecipient.toLowerCase()) {
    throw new Error('收款地址不匹配');
  }

  // 9. 验证金额
  if (decodedLog.amount < expectedAmount) {
    throw new Error('支付金额不足');
  }

  console.log('✅ 支付验证通过!');
  console.log('收款地址:', decodedLog.to);
  console.log('支付金额:', formatUnits(decodedLog.amount, 6), 'USDC');
  console.log('区块号:', receipt.blockNumber);

  return {
    success: true,
    verified: true,
    recipient: decodedLog.to,
    amount: decodedLog.amount,
    blockNumber: receipt.blockNumber,
  };
}

// 辅助函数: 解析 Transfer 事件
function decodeTransferLog(log: any) {
  // Transfer(address from, address to, uint256 value)
  const topics = log.topics;
  return {
    from: '0x' + topics[1].slice(26),
    to: '0x' + topics[2].slice(26),
    amount: BigInt(log.data),
  };
}
```

**步骤 2: 运行测试**
```bash
npx ts-node test-payment-verification.ts
```

### 预期结果
- 成功获取交易详情
- 交易状态为 success
- 找到 USDC Transfer 事件
- 收款地址正确
- 金额正确
- 区块号有效

### 通过/失败标准

| 检查项 | 通过标准 | 失败标准 |
|--------|----------|----------|
| 交易获取 | 成功获取交易详情 | 交易不存在 |
| 交易状态 | status = 'success' | status = 'reverted' |
| 事件解析 | 找到 Transfer 事件 | 未找到事件 |
| 收款验证 | 地址匹配 | 地址不匹配 |
| 金额验证 | 金额 >= 预期 | 金额不足 |
| 区块确认 | 区块号 > 0 | 区块号无效 |

**整体通过条件**: 所有检查项均通过

---

## 验证环境准备

### 1. 测试网络配置

```typescript
// networks.ts
export const TEST_NETWORK = {
  name: 'Base Sepolia',
  chainId: 84532,
  rpcUrl: 'https://base-sepolia.g.alchemy.com/v2/YOUR_KEY',
  blockExplorer: 'https://sepolia.basescan.org',
  usdcAddress: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  entryPointAddress: '0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789',
};
```

### 2. 测试钱包

```
部署者地址: 0x... (需要 ETH 用于 Gas)
Smart Account: 由 Biconomy/ZeroDev 部署
Session Key: 由 Smart Account 创建
```

### 3. 测试资金

```
- ETH (Base Sepolia): 用于 Gas 费用
- USDC (Base Sepolia): 用于支付测试
- 来源: Base Sepolia 水龙头
```

---

## 验证顺序

建议按以下顺序执行验证:

```
1. 验证 1: 连接 Smart Account
   ↓
2. 验证 2: 创建 Session Key
   ↓
3. 验证 3: 触发 x402 支付
   ↓
4. 验证 4: 链上验证支付
```

**原因**: 后续验证依赖于前面的验证结果

---

## 风险与缓解

### 风险 1: 网络不稳定
- **风险**: Base Sepolia 测试网可能出现不稳定
- **缓解**: 准备备用 RPC 节点 (Infura, Alchemy)

### 风险 2: Gas 费用波动
- **风险**: 测试网 Gas 费用可能波动
- **缓解**: 预留足够的 ETH 用于测试

### 风险 3: Smart Account 部署失败
- **风险**: 首次部署可能失败
- **缓解**: 检查 EntryPoint 地址是否正确，合约是否已部署

### 风险 4: Session Key 创建失败
- **风险**: 模块安装可能失败
- **缓解**: 检查模块地址是否正确，权限是否足够

---

## 验证结果记录模板

```
验证日期: ____
验证人员: ____

验证 1: 连接 Smart Account
- 状态: ✅ 通过 / ❌ 失败
- 备注: ____

验证 2: 创建 Session Key
- 状态: ✅ 通过 / ❌ 失败
- 备注: ____

验证 3: 触发 x402 支付
- 状态: ✅ 通过 / ❌ 失败
- 备注: ____

验证 4: 链上验证支付
- 状态: ✅ 通过 / ❌ 失败
- 备注: ____

总体结论: ____
```

---

*验证计划版本: v1.0*
*最后更新: Week 3*
