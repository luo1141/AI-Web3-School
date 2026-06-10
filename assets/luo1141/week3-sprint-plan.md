# 🗓️ Week 4 Sprint Plan — AgentPay SDK

## 冲刺概览

| 字段 | 内容 |
|------|------|
| **项目** | AgentPay SDK |
| **冲刺周期** | Week 4（5天） |
| **目标** | 完成 MVP 开发并提交 Hackathon |
| **参赛形式** | Solo |

---

## 每日冲刺计划

### Day 1: Core SDK Scaffold + x402 Integration

**主题：** 搭建 SDK 骨架，集成 x402 协议

#### 任务清单
- [ ] 初始化 TypeScript 项目，配置 tsconfig.json
- [ ] 安装核心依赖（viem, typescript, vitest）
- [ ] 创建 src/core/ 目录结构
- [ ] 实现 types.ts — 定义核心类型（PaymentRequest, PaymentResult 等）
- [ ] 实现 constants.ts — 配置常量（网络、合约地址）
- [ ] 研究 x402 协议文档和 SDK
- [ ] 实现 x402-provider.ts — x402 协议封装

#### 交付物
- ✅ 可运行的 TypeScript 项目骨架
- ✅ 核心类型定义完成
- ✅ x402 基础集成代码
- ✅ 基础单元测试框架

#### 预计时间
- 上午（4h）：项目初始化 + 类型定义
- 下午（4h）：x402 集成 + 测试

---

### Day 2: Smart Account + Session Key Integration

**主题：** 集成 Smart Account 和 Session Key 机制

#### 任务清单
- [ ] 研究 Smart Account SDK（viem/account-abstraction）
- [ ] 实现 smart-account.ts — Smart Account 封装
- [ ] 研究 Session Key 权限模型
- [ ] 实现 session-key.ts — Session Key 管理
- [ ] 集成 Smart Account 到 AgentPay 主流程
- [ ] 编写集成测试

#### 交付物
- ✅ Smart Account 创建和管理功能
- ✅ Session Key 生成和权限控制
- ✅ 集成测试通过
- ✅ 示例代码（basic-payment）

#### 预计时间
- 上午（4h）：Smart Account 集成
- 下午（4h）：Session Key 实现 + 测试

---

### Day 3: Demo App — Agent Buying API Access

**主题：** 构建演示应用，展示完整支付流程

#### 任务清单
- [ ] 设计 Demo 场景：AI Agent 购买 API 访问权限
- [ ] 实现 Demo 前端界面（简单 HTML/JS）
- [ ] 连接 AgentPay SDK 到前端
- [ ] 模拟 Agent 发起支付请求
- [ ] 实现支付状态追踪
- [ ] 测试完整流程（从创建到支付）

#### 交付物
- ✅ 可运行的 Demo 应用
- ✅ 完整支付流程演示
- ✅ 交互式用户体验
- ✅ Demo 文档说明

#### 预计时间
- 上午（4h）：Demo 设计 + 前端开发
- 下午（4h）：SDK 集成 + 测试

---

### Day 4: Testing + Documentation

**主题：** 全面测试，完善文档

#### 任务清单
- [ ] 编写核心模块单元测试（覆盖率 ≥ 80%）
- [ ] 编写集成测试（支付流程）
- [ ] 完善 API 参考文档
- [ ] 编写 Quick Start 指南
- [ ] 编写架构设计文档
- [ ] 优化 README.md
- [ ] 代码审查和重构

#### 交付物
- ✅ 单元测试覆盖率 ≥ 80%
- ✅ 集成测试通过
- ✅ 完整 API 文档
- ✅ Quick Start 指南

#### 预计时间
- 上午（4h）：测试编写
- 下午（4h）：文档完善

---

### Day 5: Polish + Submission

**主题：** 最终优化，提交 Hackathon

#### 任务清单
- [ ] 代码最终审查和清理
- [ ] 性能优化
- [ ] 错误处理完善
- [ ] 准备提交材料
- [ ] 录制 Demo 视频
- [ ] 撰写项目描述
- [ ] 提交 Hackathon

#### 交付物
- ✅ 生产级代码
- ✅ 完整提交材料
- ✅ Demo 视频
- ✅ 项目描述文档
- ✅ Hackathon 提交完成

#### 预计时间
- 上午（4h）：代码优化 + 审查
- 下午（4h）：提交准备 + 提交

---

## 里程碑检查点

| 天数 | 检查点 | 状态 |
|------|--------|------|
| Day 1 | SDK 骨架 + x402 集成 | ⬜ |
| Day 2 | Smart Account + Session Key | ⬜ |
| Day 3 | Demo 应用完成 | ⬜ |
| Day 4 | 测试和文档 | ⬜ |
| Day 5 | 提交完成 | ⬜ |

---

## 风险预案

| 风险 | 应对策略 |
|------|----------|
| x402 集成困难 | 简化支付流程，使用 Mock |
| Smart Account SDK 问题 | 使用基础 EOA 钱包降级 |
| 时间不足 | 优先核心功能，砍掉非必要特性 |
| 测试覆盖率不足 | 聚焦核心模块测试 |

---

## 每日站会模板

```markdown
## Day X 站会

### 昨日完成
- [ ] ...

### 今日计划
- [ ] ...

### 阻塞问题
- ...
```
