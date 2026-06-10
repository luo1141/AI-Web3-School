# Week 2: 最小支付与商业流程拆解

> 作者: Voss (luo1141)
> 日期: 2026-06-10
> 主题: AI Agent 最小支付流程设计

---

## 一、流程总览

```
┌─────────────────────────────────────────────────────────┐
│                    Agent 支付流程                         │
│                                                          │
│  User → Agent → Payment Intent → x402/402 → USDC → 结算  │
│                                                          │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │ 用户  │→│ Agent │→│ 意图  │→│ 支付  │→│ 结算  │      │
│  │ 授权  │  │ 决策  │  │ 构造  │  │ 执行  │  │ 确认  │      │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘      │
└─────────────────────────────────────────────────────────┘
```

## 二、各步骤详解

### Step 1: 用户触发 (User Trigger)

**责任**: 用户发起请求，授权 Agent 执行特定任务

| 属性 | 说明 |
|------|------|
| **自动化程度** | 人类确认 |
| **输入** | 用户自然语言指令 + 预设授权策略 |
| **输出** | 任务描述 + 授权范围 |
| **示例** | "帮我订阅这个 API 服务，预算不超过 $5/月" |

### Step 2: Agent 决策 (Agent Decision)

**责任**: Agent 理解任务，决定是否需要支付，选择支付策略

| 属性 | 说明 |
|------|------|
| **自动化程度** | 全自动 |
| **输入** | 任务描述 + 授权范围 + 当前余额 |
| **输出** | 支付决策（是否支付、金额、目标地址） |
| **关键逻辑** | 1) 检查任务是否需要支付 2) 验证金额是否在授权范围内 3) 选择最优支付路径 |

### Step 3: 支付意图构造 (Payment Intent)

**责任**: 构造标准化的支付意图对象

| 属性 | 说明 |
|------|------|
| **自动化程度** | 全自动 |
| **输入** | 支付决策 + 目标服务信息 |
| **输出** | PaymentIntent 对象 |
| **数据结构** | 见下方示例 |

**PaymentIntent 数据结构:**
```json
{
  "intent_id": "pi_abc123",
  "agent_id": "agent_voss_001",
  "recipient": "0x ServiceProviderAddress",
  "amount": "1.50",
  "currency": "USDC",
  "network": "base",
  "description": "API access - Weather Data Pro",
  "expires_at": "2026-06-10T12:00:00Z",
  "session_key": "sk_temp_weather_001",
  "budget_limit": "5.00",
  "gas_strategy": "gasless"
}
```

### Step 4: x402 支付执行 (Payment Execution)

**责任**: 通过 x402 协议完成机器间支付

| 属性 | 说明 |
|------|------|
| **自动化程度** | 全自动 |
| **输入** | PaymentIntent + 钱包签名 |
| **流程** | 1) Agent 请求资源 2) 服务器返回 402 + PaymentRequired 3) Agent 构造 USDC 转账 4) Agent 提交交易 5) 服务器验证并返回资源 |

**x402 交互时序:**
```
Agent                          ServiceProvider
  │                                    │
  │──── GET /api/data ────────────────→│
  │                                    │
  │←─── 402 Payment Required ─────────│
  │    {                               │
  │      "x402Version": 1,            │
  │      "accepts": [{                 │
  │        "scheme": "exact",          │
  │        "network": "base",          │
  │        "maxAmountRequired": "1500000",│
  │        "resource": "api/data",     │
  │        "description": "Weather API",│
  │        "payTo": "0x...provider"    │
  │      }]                            │
  │    }                               │
  │                                    │
  │──── POST /api/data ───────────────→│
  │    Header: X-PAYMENT: {signature}  │
  │                                    │
  │←─── 200 OK + Resource Data ────────│
```

### Step 5: 结算确认 (Settlement)

**责任**: 验证支付完成，更新状态

| 属性 | 说明 |
|------|------|
| **自动化程度** | 全自动（通知人类） |
| **输入** | 交易哈希 + 服务器确认 |
| **输出** | 支付凭证 + 服务访问令牌 |
| **后续动作** | 1) 缓存访问令牌 2) 记录交易日志 3) 通知用户支付完成 |

---

## 三、自动化 vs 人类确认 矩阵

| 操作类型 | 首次支付 | 同类重复支付 | 大额支付 (> $10) |
|---------|---------|-------------|-----------------|
| 读取数据 | 自动 | 自动 | 自动 |
| 小额支付 (< $1) | 通知 | 自动 | 通知 |
| 中额支付 ($1-$10) | 通知 | 自动 | 确认 |
| 大额支付 (> $10) | 确认 | 确认 | 确认 |
| 授权新服务 | 确认 | 自动 | 确认 |

## 四、Gas 策略

| 策略 | 适用场景 | 实现方式 |
|------|---------|---------|
| **Gasless (推荐)** | Agent 支付场景 | Paymaster 代付 Gas，费用从 USDC 中扣除 |
| **L2 原生** | Base/Arbitrum | 交易成本 < $0.01，直接使用 |
| **批量打包** | 高频支付 | 多笔支付打包为一笔链上交易 |

**推荐方案**: Base L2 + Gasless，用户完全无需关注 Gas。

## 五、错误处理

```python
class AgentPaymentError(Exception):
    """Agent 支付错误基类"""
    pass

class InsufficientFundsError(AgentPaymentError):
    """余额不足"""
    def __init__(self, balance, required):
        self.balance = balance
        self.required = required
        # 自动触发: 通知用户充值 或 降级到免费方案

class PaymentExpiredError(AgentPaymentError):
    """支付意图过期"""
    # 自动触发: 重新构造 PaymentIntent

class ProviderVerificationError(AgentPaymentError):
    """服务端验证失败"""
    # 自动触发: 重试或回滚

class UnauthorizedAmountError(AgentPaymentError):
    """金额超出授权范围"""
    # 触发人类确认 或 拒绝交易
```

## 六、成本追踪

```json
{
  "agent_id": "agent_voss_001",
  "period": "2026-06",
  "total_spent": "47.82",
  "currency": "USDC",
  "breakdown": {
    "api_calls": "32.50",
    "compute": "12.00",
    "storage": "3.32"
  },
  "transactions": [
    {
      "tx_hash": "0xabc...",
      "service": "Weather Data Pro",
      "amount": "1.50",
      "timestamp": "2026-06-10T10:30:00Z"
    }
  ],
  "budget_remaining": "52.18"
}
```

---

## 七、具体案例: Agent 购买 API 访问

**场景**: Voss 的 AI Agent 需要获取实时天气数据来完成农业监测任务。

```
1. 用户指令: "帮我查一下明天北京的天气，需要准确数据"

2. Agent 决策:
   - 内置天气 API 不可用（免费额度用完）
   - 发现 Weather Data Pro API（付费，$0.01/次）
   - 判断: 在授权预算内，执行支付

3. 支付流程:
   - GET https://api.weatherdata.pro/v1/beijing
   - 返回 402 + PaymentRequired
   - Agent 构造 USDC 转账: 0.01 USDC → 服务商地址
   - 通过 Session Key 签名（无需用户确认）
   - 提交交易到 Base L2

4. 结果:
   - 服务商验证支付，返回天气数据
   - Agent 缓存数据，通知用户
   - 记录: 支出 $0.01，获得 7 天 API 访问权限

5. 成本:
   - Gas: $0 (Gasless)
   - 服务费: $0.01
   - 总计: $0.01
```

---

*本文档为 Week 2 支付流程设计输出。*
