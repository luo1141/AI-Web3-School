# Week 2: Agent 链上操作的权限策略设计

> 作者: Voss (luo1141)
> 日期: 2026-06-10
> 主题: Agent 权限分层模型与安全控制

---

## 一、权限策略总览

AI Agent 在链上操作时，需要一个精细的权限控制体系。核心原则是：**最小权限 + 渐进授权 + 可撤销**。

```
┌─────────────────────────────────────────────────────────┐
│                    权限分层模型                            │
│                                                          │
│  ┌─────────────────────────────────────────────┐        │
│  │ Tier 3: Full Write (完全写入)                │        │
│  │ - 大额转账、合约部署、参数修改               │        │
│  │ - 需要人类逐次确认                           │        │
│  └─────────────────────────────────────────────┘        │
│                                                          │
│  ┌─────────────────────────────────────────────┐        │
│  │ Tier 2: Limited Write (受限写入)             │        │
│  │ - 小额支付、订阅、授权操作                   │        │
│  │ - 通知用户，自动执行                         │        │
│  └─────────────────────────────────────────────┘        │
│                                                          │
│  ┌─────────────────────────────────────────────┐        │
│  │ Tier 1: Read-Only (只读)                     │        │
│  │ - 查询余额、读取数据、获取报价               │        │
│  │ - 完全自动，无需确认                         │        │
│  └─────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

---

## 二、分层权限详解

### Tier 1: 只读操作 (Read-Only)

**定义**: Agent 可以自由读取链上数据，无需任何确认。

**允许的操作:**
- 查询 USDC 余额
- 读取交易历史
- 获取 Gas 价格
- 查询资产报价
- 读取合约状态

**具体示例:**

```python
# 示例 1: Agent 查询余额
balance = await agent.get_balance("USDC")
# 结果: 48.50 USDC
# 确认: 无需确认 ✓

# 示例 2: Agent 获取 ETH/USDC 报价
price = await agent.get_price("ETH", "USDC")
# 结果: 3850.00
# 确认: 无需确认 ✓

# 示例 3: Agent 检查服务可用性
status = await agent.check_service("https://api.weatherdata.pro")
# 结果: {"available": true, "price": "0.01 USDC/call"}
# 确认: 无需确认 ✓
```

**Session Key 配置:**
```json
{
  "tier": "read-only",
  "functions": ["get_balance", "get_price", "check_service", "read_data"],
  "max_calls_per_hour": 1000,
  "expires_at": "2026-06-17T00:00:00Z"
}
```

---

### Tier 2: 受限写入 (Limited Write)

**定义**: Agent 可以执行低风险的写入操作，系统自动通知用户。

**允许的操作:**
- USDC 小额支付 (< $5)
- 订阅服务
- 授权新合约
- 更新自身配置

**限制条件:**
- 单笔金额上限: $5
- 日累计上限: $20
- 月累计上限: $100
- 仅限白名单地址

**具体示例:**

```python
# 示例 1: Agent 自动支付 API 费用
payment = await agent.pay(
    recipient="0xServiceProvider",
    amount="0.50",
    currency="USDC",
    reason="Weather API - 7天订阅"
)
# 确认: 自动执行 + 通知用户
# 通知: "已支付 $0.50 给 Weather Data Pro"

# 示例 2: Agent 授权新服务
approval = await agent.approve_token(
    spender="0xNewService",
    amount="2.00",
    currency="USDC"
)
# 确认: 自动执行 + 通知用户
# 通知: "已授权 NewService 使用最多 $2.00 USDC"

# 示例 3: Agent 更新自身配置
config = await agent.update_config(
    key="api_endpoint",
    value="https://new-api.example.com"
)
# 确认: 自动执行 + 通知用户
```

**Session Key 配置:**
```json
{
  "tier": "limited-write",
  "functions": ["pay", "approve_token", "update_config"],
  "max_amount_per_tx": "5.00",
  "daily_budget": "20.00",
  "monthly_budget": "100.00",
  "allowed_recipients": [
    "0xProvider1",
    "0xProvider2",
    "0xProvider3"
  ],
  "expires_at": "2026-06-17T00:00:00Z"
}
```

---

### Tier 3: 完全写入 (Full Write)

**定义**: Agent 执行高风险操作时，必须获得人类的逐次确认。

**允许的操作:**
- 大额转账 (≥ $5)
- 合约部署
- 参数修改
- 紧急操作

**确认流程:**
```
Agent → 请求确认 → 人类 → 批准/拒绝 → 执行/取消
```

**具体示例:**

```python
# 示例 1: Agent 请求大额转账
request = await agent.request_confirmation(
    action="transfer",
    params={
        "recipient": "0xPartner",
        "amount": "50.00",
        "currency": "USDC",
        "reason": "月度合作费用"
    },
    timeout=300  # 5分钟超时
)
# 确认: 人类必须确认
# 流程: Agent 发送确认请求 → 人类在 App 中确认 → Agent 执行

# 示例 2: Agent 请求合约部署
request = await agent.request_confirmation(
    action="deploy_contract",
    params={
        "contract": "PaymentSplitter",
        "constructor_args": [...],
        "estimated_gas": "0.005 ETH"
    }
)
# 确认: 人类必须确认

# 示例 3: Agent 请求参数修改
request = await agent.request_confirmation(
    action="modify_parameter",
    params={
        "contract": "GovernanceContract",
        "function": "updateThreshold",
        "args": ["new_threshold_value"]
    }
)
# 确认: 人类必须确认
```

**Session Key 配置:**
```json
{
  "tier": "full-write",
  "functions": ["transfer", "deploy_contract", "modify_parameter", "emergency_action"],
  "require_confirmation": true,
  "timeout_seconds": 300,
  "expires_at": "2026-06-11T00:00:00Z"
}
```

---

## 三、Session Key 设计

### 3.1 Session Key 结构

```typescript
interface SessionKey {
  // 基本信息
  key_id: string;           // 唯一标识
  agent_id: string;         // 关联的 Agent
  created_at: timestamp;    // 创建时间
  expires_at: timestamp;    // 过期时间

  // 权限范围
  tier: "read-only" | "limited-write" | "full-write";
  allowed_functions: string[];  // 允许调用的函数

  // 限制条件
  max_amount_per_tx: string;    // 单笔上限
  daily_budget: string;         // 日预算
  monthly_budget: string;       // 月预算
  allowed_recipients: string[]; // 白名单地址

  // 签名
  public_key: string;           // Session Key 公钥
  signature: string;            // 主钱包签名
}
```

### 3.2 时间限制

| 维度 | 默认值 | 说明 |
|------|--------|------|
| 单次会话 | 24 小时 | 最短有效期 |
| 周期会话 | 7 天 | 推荐有效期 |
| 长期会话 | 30 天 | 需要额外验证 |

### 3.3 预算限制

```python
budget_config = {
    "per_transaction": {
        "read-only": "unlimited",      # 无限制
        "limited-write": "5.00",       # $5
        "full-write": "unlimited"      # 需人类确认
    },
    "daily": {
        "read-only": "unlimited",
        "limited-write": "20.00",      # $20/天
        "full-write": "unlimited"
    },
    "monthly": {
        "read-only": "unlimited",
        "limited-write": "100.00",     # $100/月
        "full-write": "unlimited"
    }
}
```

### 3.4 功能限制

```python
function_whitelist = {
    "read-only": [
        "get_balance",
        "get_price",
        "read_data",
        "check_service"
    ],
    "limited-write": [
        "pay",
        "approve_token",
        "update_config",
        "subscribe"
    ],
    "full-write": [
        "transfer",
        "deploy_contract",
        "modify_parameter",
        "emergency_action"
    ]
}
```

---

## 四、Pact 协议: 意图声明

### 4.1 什么是 Pact

Pact 是一个 Agent 意图声明协议，允许 Agent 在执行操作前先声明意图，让人类了解即将发生什么。

### 4.2 意图声明示例

```json
{
  "pact_id": "pact_abc123",
  "agent_id": "agent_voss_001",
  "action": "payment",
  "description": "Agent 需要支付 $0.50 USDC 获取天气数据",
  "details": {
    "recipient": "0xWeatherDataProvider",
    "amount": "0.50",
    "currency": "USDC",
    "service": "Weather Data API - 7天订阅",
    "justification": "用户请求查询天气数据，免费 API 额度已用完"
  },
  "risk_assessment": {
    "tier": "limited-write",
    "requires_confirmation": false,
    "within_budget": true
  },
  "created_at": "2026-06-10T10:30:00Z",
  "expires_at": "2026-06-10T10:35:00Z"
}
```

---

## 五、MPC 阈值签名

### 5.1 什么是 MPC 阈值签名

MPC (Multi-Party Computation) 阈值签名是一种分布式密钥管理方案，将私钥分割成多个份额，需要一定数量的份额才能完成签名。

### 5.2 应用场景

```
┌─────────────────────────────────────────────────────┐
│              MPC 阈值签名架构                         │
│                                                      │
│  主钱包私钥 → 分割为 3 份                            │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ 份额 1   │  │ 份额 2   │  │ 份额 3   │          │
│  │ (人类)   │  │ (Agent)  │  │ (安全存储)│          │
│  └──────────┘  └──────────┘  └──────────┘          │
│                                                      │
│  阈值: 2/3 (需要任意 2 个份额才能签名)               │
│                                                      │
│  小额支付: Agent + 安全存储 = 2/3 ✓                 │
│  大额支付: 人类 + Agent = 2/3 ✓                     │
│  紧急情况: 人类 + 安全存储 = 2/3 ✓                  │
└─────────────────────────────────────────────────────┘
```

### 5.3 优势

- **去中心化**: 没有单点故障
- **灵活授权**: 根据场景选择不同的签名组合
- **安全增强**: 即使 Agent 被攻破，也无法单独完成高风险操作

---

## 六、紧急撤销机制

### 6.1 撤销触发条件

| 触发条件 | 响应时间 | 操作 |
|---------|---------|------|
| 检测到异常交易 | 实时 | 冻结 Session Key |
| 用户主动撤销 | 即时 | 立即失效 |
| Session Key 过期 | 自动 | 自动失效 |
| 预算耗尽 | 自动 | 降级为只读 |
| 安全事件 | 实时 | 冻结所有权限 |

### 6.2 撤销流程

```python
class RevocationManager:
    """紧急撤销管理器"""

    async def emergency_revoke(self, agent_id: str, reason: str):
        """紧急撤销 Agent 权限"""
        # 1. 立即冻结所有 Session Key
        await self.freeze_all_session_keys(agent_id)

        # 2. 撤销所有未完成的授权
        await self.revoke_pending_approvals(agent_id)

        # 3. 记录撤销事件
        await self.log_revocation(agent_id, reason)

        # 4. 通知用户
        await self.notify_user(
            f"紧急撤销: Agent {agent_id} 的所有权限已被冻结"
        )

        # 5. 启动调查
        await self.initiate_investigation(agent_id)
```

### 6.3 撤销后的恢复

```python
async def restore_permissions(self, agent_id: str, new_policy: PermissionPolicy):
    """恢复 Agent 权限"""
    # 1. 验证用户身份
    if not await self.verify_identity():
        raise UnauthorizedError()

    # 2. 创建新的 Session Key
    new_key = await self.create_session_key(
        agent_id=agent_id,
        policy=new_policy
    )

    # 3. 逐步恢复权限（从只读开始）
    await self.gradual_restore(agent_id, new_key)
```

---

## 七、完整示例: Agent 订阅工作流

### 场景

Agent 需要订阅三个数据服务来完成农业监测任务。

### 权限检查流程

```
1. Agent 查询服务价格
   - Tier: Read-Only
   - 确认: 无需确认 ✓

2. Agent 评估总成本
   - 天气数据: $0.50/周
   - 土壤数据: $1.00/周
   - 卫星数据: $2.00/周
   - 总计: $3.50/周 = $15.00/月
   - Tier: Limited-Write (月度 < $20)
   - 确认: 自动执行 + 通知 ✓

3. Agent 执行支付
   - 支付 1: $0.50 → Weather Service
   - 支付 2: $1.00 → Soil Service
   - 支付 3: $2.00 → Satellite Service
   - Tier: Limited-Write
   - 确认: 自动执行 + 通知 ✓

4. Agent 获取数据
   - Tier: Read-Only
   - 确认: 无需确认 ✓

5. 用户收到通知
   - "已自动订阅 3 个数据服务，本周支出 $3.50"
   - "月度预算剩余: $85.00"
```

---

*本文档为 Week 2 权限策略设计输出。*
