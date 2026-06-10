# Week 2: x402 Paywall + CAW Agent 自主支付循环

> 作者: Voss (luo1141)
> 日期: 2026-06-10
> 主题: x402 协议机制与 Agent 自主支付架构

---

## 一、x402 协议机制

### 1.1 什么是 x402

x402 是一个基于 HTTP 402 状态码的机器间 (M2M) 支付协议。它复用了 HTTP 协议中预留但长期未使用的 402 "Payment Required" 状态码，为 AI Agent 提供了标准化的自主支付能力。

**核心思想**: 当 Agent 访问付费资源时，服务器返回 402 + 支付要求，Agent 自动完成支付后重试请求，整个过程无需人类介入。

### 1.2 协议工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    x402 支付流程                              │
│                                                              │
│  Agent (买方)                    ServiceProvider (卖方)       │
│       │                                │                     │
│       │──── 1. GET /resource ────────→│                     │
│       │                                │                     │
│       │←─── 2. 402 Payment Required ──│                     │
│       │    + PaymentRequirements       │                     │
│       │                                │                     │
│       │  3. Agent 自动处理:            │                     │
│       │  - 解析支付要求                │                     │
│       │  - 构造 USDC 转账             │                     │
│       │  - 签名并提交交易              │                     │
│       │                                │                     │
│       │──── 4. GET /resource ─────────→│                     │
│       │    + X-PAYMENT header          │                     │
│       │                                │                     │
│       │←─── 5. 200 OK + Resource ─────│                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 1.3 x402 关键特性

- **机器原生**: 专为 M2M 设计，不需要人类点击确认
- **HTTP 标准**: 复用已有 HTTP 语义，实现简单
- **链上结算**: 支付在区块链上完成，可验证、可审计
- **多链支持**: 支持 Base、Ethereum 等多条链
- **USDC 计价**: 使用稳定币，避免价格波动

---

## 二、CAW (Crypto Agent Wallet) 概念

### 2.1 什么是 CAW

CAW 是一种为 AI Agent 设计的专用加密钱包架构，具有以下特征：

1. **自主性**: Agent 可以自主管理资金、发起支付
2. **权限受限**: 通过 Session Key 和权限策略限制 Agent 的操作范围
3. **可审计**: 所有操作在链上记录，可追溯
4. **可撤销**: 人类可以随时撤销 Agent 的权限

### 2.2 CAW 架构

```
┌─────────────────────────────────────────────────────┐
│                  CAW 架构                             │
│                                                      │
│  ┌──────────────┐     ┌──────────────┐              │
│  │  主钱包       │     │  Session Key │              │
│  │  (Master)    │←────│  (Temporary)  │              │
│  │              │     │              │              │
│  │  - 人类控制   │     │  - Agent 使用 │              │
│  │  - 存储资金   │     │  - 有限权限   │              │
│  │  - 管理策略   │     │  - 时间限制   │              │
│  └──────────────┘     └──────────────┘              │
│         │                    │                       │
│         │                    │                       │
│  ┌──────┴──────┐     ┌──────┴──────┐              │
│  │  权限策略    │     │  支付执行    │              │
│  │  (Policy)   │     │  (Executor)  │              │
│  │             │     │             │              │
│  │  - 金额上限  │     │  - x402 处理 │              │
│  │  - 时间窗口  │     │  - Gas 管理  │              │
│  │  - 函数白名单│     │  - 交易签名  │              │
│  └─────────────┘     └─────────────┘              │
└─────────────────────────────────────────────────────┘
```

---

## 三、Agent 自主支付循环设计

### 3.1 完整循环流程

```
┌─────────────────────────────────────────────────────────────┐
│              Agent 自主支付循环 (Autonomous Payment Loop)     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Phase 1: 发现 (Discovery)                            │    │
│  │   Agent 访问资源 → 发现内容在 Paywall 后面            │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │ Phase 2: 评估 (Evaluation)                           │    │
│  │   检查: 1) 是否在授权范围 2) 余额是否充足              │    │
│  │   决策: 执行支付 / 通知用户 / 放弃                     │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │ Phase 3: 构造 (Construction)                         │    │
│  │   构造 PaymentIntent → 选择支付策略 → 准备签名         │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │ Phase 4: 执行 (Execution)                            │    │
│  │   1) 构造 USDC 转账                                  │    │
│  │   2) Session Key 签名                                │    │
│  │   3) 提交到 Base L2                                  │    │
│  │   4) 等待确认                                        │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │ Phase 5: 验证 (Verification)                         │    │
│  │   服务器验证支付 → 返回 Access Token                  │    │
│  └──────────────────────┬──────────────────────────────┘    │
│                         │                                    │
│  ┌──────────────────────▼──────────────────────────────┐    │
│  │ Phase 6: 缓存 (Caching)                              │    │
│  │   1) 缓存 Access Token（带过期时间）                   │    │
│  │   2) 缓存资源内容                                    │    │
│  │   3) 记录交易日志                                    │    │
│  │   4) 更新成本统计                                    │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              通知用户 (Notification)                  │    │
│  │   异步推送支付结果，不影响 Agent 工作流               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心代码结构

```python
class AgentPaymentLoop:
    """Agent 自主支付循环"""

    def __init__(self, wallet: CAW, policy: PaymentPolicy):
        self.wallet = wallet
        self.policy = policy
        self.cache = PaymentCache()
        self.logger = TransactionLogger()

    async def discover_and_pay(self, resource_url: str) -> Optional[Resource]:
        """发现资源并自主完成支付"""

        # Phase 1: 发现
        response = await self.fetch(resource_url)

        if response.status != 402:
            return response.data  # 免费资源，直接返回

        # Phase 2: 评估
        payment_req = response.parse_x402()
        evaluation = self.evaluate(payment_req)

        if not evaluation.approved:
            await self.notify_user(f"需要支付 {payment_req.amount} USDC")
            return None

        # Phase 3: 构造
        payment_intent = self.construct_intent(payment_req)

        # Phase 4: 执行
        tx_hash = await self.execute_payment(payment_intent)

        # Phase 5: 验证
        verified = await self.verify_payment(tx_hash, payment_req)

        if not verified:
            await self.rollback(tx_hash)
            return None

        # Phase 6: 缓存
        access_token = verified.access_token
        self.cache.store(resource_url, access_token, verified.expires_at)
        self.logger.record(tx_hash, payment_req)

        # 重新获取资源
        response = await self.fetch(resource_url, token=access_token)
        return response.data

    def evaluate(self, payment_req: PaymentRequirement) -> Evaluation:
        """评估支付请求是否在授权范围内"""
        return Evaluation(
            approved=(
                payment_req.amount <= self.policy.max_amount_per_tx
                and payment_req.amount + self.policy.period_spent <= self.policy.monthly_budget
                and payment_req.recipient in self.policy.allowed_recipients
            ),
            reason="符合授权策略" if ... else "超出授权范围"
        )
```

---

## 四、安全考虑

### 4.1 支付安全

| 威胁 | 缓解措施 |
|------|---------|
| **重放攻击** | PaymentIntent 包含 nonce + 过期时间 |
| **金额篡改** | 链上验证实际转账金额 |
| **地址伪造** | 白名单机制 + 域名验证 |
| **Gas 耗尽** | 预留 Gas 缓冲区 + 自动重试 |

### 4.2 会话安全

| 威胁 | 缓解措施 |
|------|---------|
| **Session Key 泄露** | 短有效期 + 功能限制 |
| **权限提升** | 严格的角色分离 + 策略引擎 |
| **中间人攻击** | HTTPS + 链上验证 |

### 4.3 回滚机制

```python
class RollbackManager:
    """支付回滚管理器"""

    async def rollback(self, tx_hash: str):
        """回滚失败的支付"""
        # 1. 记录回滚意图
        self.log_rollback_intent(tx_hash)

        # 2. 如果是 ERC-20 且支付未完成，等待自然过期
        # 3. 如果支付已完成但服务未提供，发起争议
        # 4. 更新状态为 "回滚中"
        # 5. 通知用户

    async def dispute(self, tx_hash: str, reason: str):
        """发起支付争议"""
        # 通过智能合约的争议机制
        # 提交证据（402 响应、服务端确认等）
        # 等待仲裁结果
```

---

## 五、实际案例

### 场景: Agent 自主订阅数据服务

```
1. Agent 执行数据分析任务时，发现需要实时股票数据

2. Discovery:
   - 尝试访问 https://api.stockdata.io/realtime/AAPL
   - 收到 402 + PaymentRequired: 0.005 USDC

3. Evaluation:
   - 检查策略: 允许的数据服务 ✓
   - 检查预算: 月度剩余 $48.50 ✓
   - 检查金额: $0.005 < 单笔上限 $1.00 ✓
   - 决策: 批准

4. Execution:
   - 构造 USDC 转账: 0.005 USDC → stockdata.io
   - Session Key 签名
   - 提交到 Base L2
   - 等待确认 (~2秒)

5. Verification:
   - 服务器验证链上支付
   - 返回 7 天访问令牌

6. Caching:
   - 缓存令牌（TTL: 7天）
   - 获取实时数据
   - 记录: 支出 $0.005

7. Notification:
   - "已自动订阅 StockData Pro，支出 $0.005，有效期 7 天"
```

---

*本文档为 Week 2 x402 + CAW 自主支付循环设计输出。*
