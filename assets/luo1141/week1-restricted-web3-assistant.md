# Week 1 - 受限 Web3 助手设计：测试网 Token Swap 工作流

> 作者: Voss (luo1141) | 日期: 2026-06-10
> 背景: AI + Web3 | 方向: Dev Tooling & Automation

---

## 一、问题描述

### 核心问题
AI Agent 需要与 DeFi 协议（如 Uniswap、SwapRouter）交互，但 DeFi 交互涉及真实资产流动、无限授权风险和智能合约漏洞。如果 Agent 拥有完全自主权，可能造成：

1. **资产损失**: Agent 误判价格或路径，执行不利交易
2. **权限滥用**: Agent 获取无限 Token 授权，可随时转走用户资产
3. **合约风险**: Agent 与未审计合约交互，遭遇三明治攻击或 Rug Pull
4. **Gas 浪费**: Agent 在高 Gas 时段执行非必要交易

### 设计目标
构建一个**受约束的测试网 Token Swap 助手**，实现：
- Agent 可以自主执行 Token Swap 操作
- 所有操作被严格限制在测试网环境
- 设置明确的预算上限和操作白名单
- 关键操作必须经过人工确认
- 所有操作可追溯和验证

---

## 二、工作流架构

```
用户指令 → 预算检查 → 协议白名单验证 → 人工确认(关键操作) → 交易执行 → 结果验证 → 日志记录
```

### 系统组件
1. **预算管理器**: 跟踪每日/每次操作的 Gas 和 Token 消耗
2. **协议白名单**: 只允许与预审过的测试网合约交互
3. **人工确认网关**: 超出阈值或首次操作时触发确认
4. **操作日志**: 全部交易记录上链 + 本地日志
5. **回滚机制**: 交易失败时的补偿逻辑

---

## 三、输入/输出示例

### 示例 1：标准 Swap（无需人工确认）
```
[输入]
用户: "用 0.01 ETH 在 Sepolia 测试网换 USDC"

[处理流程]
1. 检查预算：0.01 ETH < 每日上限 0.1 ETH ✅
2. 检查白名单：Sepolia Uniswap Router 在白名单内 ✅
3. 无需人工确认：金额在自动执行阈值内 ✅
4. 执行 Swap

[输出]
✅ Swap 已执行
- 输入: 0.01 ETH
- 输出: ~18.5 USDC
- 交易哈希: 0xabc123...
- Gas 消耗: 0.0003 ETH
- 剩余今日预算: 0.0997 ETH
```

### 示例 2：大额 Swap（需人工确认）
```
[输入]
用户: "用 0.05 ETH 在 Sepolia 换 DAI"

[处理流程]
1. 检查预算：0.05 ETH < 每日上限 0.1 ETH ✅
2. 检查白名单：Sepolia SwapRouter 在白名单内 ✅
3. 需要人工确认：金额 > 自动执行阈值(0.03 ETH) ⚠️

[输出]
⚠️ 需要人工确认
- 操作: 0.05 ETH → DAI (Sepolia)
- 预估输出: ~92 DAI
- 预估 Gas: 0.0005 ETH
- 今日已用预算: 0.02 ETH
请确认执行? (回复 "确认" 或 "取消")
```

### 示例 3：被拒绝的操作（超预算）
```
[输入]
用户: "用 0.2 ETH 在 Sepolia 换 USDC"

[输出]
❌ 操作被拒绝
- 原因: 超出每日预算上限 (0.1 ETH)
- 已用预算: 0.08 ETH
- 剩余预算: 0.02 ETH
- 建议: 明日再试，或联系管理员提高预算
```

---

## 四、人工确认点（≥3）

### 确认点 1：首次协议交互
- **触发条件**: Agent 第一次与某个 DEX/协议交互
- **确认内容**: 确认合约地址正确、理解交互逻辑、接受潜在风险
- **确认方式**: 详细弹窗展示合约信息 + 用户签名确认

### 确认点 2：超额交易
- **触发条件**: 单次交易金额超过自动执行阈值（如 0.03 ETH）
- **确认内容**: 确认交易对、预估输出、Gas 消耗
- **确认方式**: 展示预估结果 + 用户确认

### 确认点 3：非白名单协议交互
- **触发条件**: Agent 尝试与不在白名单中的合约交互
- **确认内容**: 展示合约审计状态、社区评分、潜在风险
- **确认方式**: 强制人工审查 + 管理员审批

### 确认点 4：授权操作（Approve）
- **触发条件**: Agent 需要对 Token 进行 Approve 操作
- **确认内容**: 授权额度、授权对象、有效期限
- **确认方式**: 详细展示授权细节 + 人工确认（建议设置为强制确认）

### 确认点 5：异常模式检测
- **触发条件**: Agent 短时间内执行多次 Swap 或交易金额异常
- **确认内容**: 操作频率、累计金额、是否符合用户意图
- **确认方式**: 暂停执行 + 人工审查

---

## 五、风险与限制（≥3）

### 风险 1：测试网与主网行为差异
- **描述**: 测试网的 Gas 价格、流动性深度与主网差异巨大，测试网成功的策略在主网可能失败
- **缓解**: 明确标注环境差异；在切换主网前强制人工审核所有参数

### 风险 2：预算绕过
- **描述**: Agent 可能通过多次小额交易累积超过预算上限
- **缓解**: 实现全局预算追踪（不仅检查单次，也检查累计）；设置操作频率限制

### 风险 3：白名单合约被攻击
- **描述**: 即使是审计过的合约，也可能被升级或发现新漏洞
- **缓解**: 定期审查白名单；监控合约事件；设置紧急暂停机制

### 风险 4：人工确认疲劳
- **描述**: 频繁的人工确认会导致用户习惯性批准，降低安全意识
- **缓解**: 使用渐进式信任机制（交易历史好则逐步降低确认频率）；关键操作始终确认

### 风险 5：链上数据延迟
- **描述**: RPC 节点数据可能延迟，导致 Agent 基于过期数据决策
- **缓解**: 使用多个 RPC 源验证；设置数据新鲜度阈值

---

## 六、验证方法

### 1. 单元测试
- 预算检查逻辑验证（边界值测试）
- 白名单过滤逻辑验证
- 人工确认触发条件验证

### 2. 集成测试
- 完整 Swap 流程在 Sepolia 测试网执行
- 确认点拦截验证（模拟超预算、非白名单等场景）
- 日志记录完整性验证

### 3. 安全审计
- 代码审计（重点检查预算绕过路径）
- 权限检查（Agent 无法修改白名单或预算上限）
- 紧急暂停机制验证

### 4. 端到端测试
- 模拟用户日常使用场景
- 异常场景恢复测试
- 性能测试（高频率操作下的预算追踪准确性）

---

## 七、技术实现要点

```python
# 核心约束检查伪代码
class RestrictedSwapAssistant:
    def __init__(self):
        self.daily_budget = 0.1  # ETH
        self.auto_exec_threshold = 0.03  # ETH
        self.allowed_contracts = load_whitelist()
        self.daily_used = 0.0
    
    def check_constraints(self, amount_eth: str, contract: str) -> dict:
        """检查所有约束条件"""
        amount = float(amount_eth)
        return {
            "budget_ok": (self.daily_used + amount) <= self.daily_budget,
            "contract_ok": contract in self.allowed_contracts,
            "needs_confirmation": amount > self.auto_exec_threshold,
        }
    
    def execute_swap(self, user_input: str) -> str:
        """执行受限 Swap"""
        params = parse_swap_input(user_input)
        checks = self.check_constraints(params.amount, params.contract)
        
        if not checks["budget_ok"]:
            return "❌ 超出预算限制"
        if not checks["contract_ok"]:
            return "❌ 协议不在白名单中"
        if checks["needs_confirmation"]:
            return f"⚠️ 需要人工确认: {params}"
        
        # 执行 Swap...
        result = execute_on_chain(params)
        self.daily_used += params.amount
        return format_result(result)
```

---

## 八、总结

这个受限 Web3 助手设计体现了 **"最小权限原则"** 和 **"人在回路中"** 的安全理念。通过多层约束（预算、白名单、人工确认），在给予 Agent 自主操作能力的同时，确保所有操作在安全边界内。这是 Agent + Web3 融合的关键基础设施之一。
