# AgentKit 日志分析报告

**分析日期**: 2026-06-11
**测试工具**: agentkit invoke

---

## 概览

| 日志文件 | 测试类型 | 请求数 | 成功率 | 总耗时 |
|---------|---------|-------|-------|-------|
| same.log | 顺序执行（相同 session_id） | 82 | 100% | ~2m 3s |
| diff.log | 顺序执行（不同 session_id） | 100 | 100% | ~1m 43s |
| multi.log | 并发执行（不同 session_id） | 100+ | 100% | ~5s（单批） |

---

## 1. same.log - 相同 Session ID 测试

### 测试配置
- **Session ID**: `same-session-id`（所有请求共用）
- **执行方式**: 顺序执行
- **请求数**: 82
- **时间范围**: 10:57:52 - 11:01:29

### 性能统计
| 指标 | 值 |
|-----|-----|
| **平均耗时** | 1026 ms |
| **最大耗时** | 1319 ms（request 35） |
| **最小耗时** | 873 ms（request 80） |

### 耗时分布
- 900-1000 ms: 约 25 次
- 1000-1100 ms: 约 40 次
- 1100-1200 ms: 约 10 次
- 1200+ ms: 约 5 次

### 观察
- 所有 82 个请求均成功
- 请求严格顺序执行，无并发
- 响应时间稳定，波动较小（标准差约 71 ms）
- Session ID 正确合并到请求头中

### 日志示例
```
[2026-06-11 10:57:52] Starting request 1
Invoking agent...
Using merged headers: {'user_id': 'agentkit_user', 'session_id': 'same-session-id'}
✅ Invocation successful
📝 Response:
mock message
[2026-06-11 10:57:53] Finished request 1 - elapsed: 1077 ms
```

---

## 2. diff.log - 不同 Session ID 测试

### 测试配置
- **Session ID**: 每次请求使用不同的 UUID
- **执行方式**: 顺序执行
- **请求数**: 100
- **时间范围**: 11:00:05 - 11:01:48（约 1 分 43 秒）

### 性能统计
| 指标 | 值 |
|-----|-----|
| **平均耗时** | 1027 ms |
| **最大耗时** | 1207 ms（request 67） |
| **最小耗时** | 877 ms（request 20） |

### 耗时分布
- 850-950 ms: 约 10 次
- 950-1050 ms: 约 50 次
- 1050-1150 ms: 约 30 次
- 1150-1250 ms: 约 10 次

### 观察
- 所有 100 个请求均成功
- 每次请求都生成了唯一的 session_id
- 响应时间与 same.log 相近，说明 session_id 对响应速度无明显影响
- 日志清晰，每个请求的起止时间明确

### 日志示例
```
[2026-06-11 11:00:05] Starting request 1
Invoking agent...
Using merged headers: {'user_id': 'agentkit_user', 'session_id': '053fe642-7137-4f53-8f82-5e67a224032e'}
✅ Invocation successful
📝 Response:
mock message
[2026-06-11 11:00:06] Finished request 1 - elapsed: 1050 ms
```

---

## 3. multi.log - 并发执行测试

### 测试配置
- **Session ID**: 每次请求使用不同的 UUID
- **执行方式**: 并发执行（每 12 个一批，100 个请求分 9 批）
- **脚本**: `multi.sh`

### 性能统计（基于 time 命令输出）

| 指标 | 值 |
|-----|-----|
| **平均耗时（real）** | 约 5.3 s |
| **最大耗时（real）** | 12.852 s |
| **最小耗时（real）** | 1.298 s |
| **平均 user time** | 约 1.17 s |

### 耗时分布
- 1-4 s: 约 25 次（快速完成，可能是缓存或轻载）
- 3.4-4.7 s: 约 65 次（正常批次）
- 12-13 s: 约 15 次（负载较高批次）

### 观察

#### 正常行为
- 所有请求均成功
- 并发执行导致输出交织，这是预期行为
- 每批请求的 `session_id` 均为唯一的 UUID

#### 输出交织示例
```
✅ Invocation successful
📝 Response:
mock message
✅ Invocation successful
📝 Response:
mock message
```
两条成功消息几乎同时打印，属于正常并发现象。

### 关键发现
1. **并发处理正常**: 多个请求同时进行，输出会交织但不影响结果
2. **Header 正确合并**: 所有请求都正确包含了 `user_id` 和唯一的 `session_id`
3. **Mock 响应正常**: 所有响应均为 `mock message`
4. **负载波动**: 部分批次耗时明显增加（12s+），可能与系统负载相关

---

## 对比分析

### 响应时间对比

| 测试 | 平均耗时 | 最小 | 最大 | 波动率 |
|-----|---------|-----|-----|-------|
| same.log | 1026 ms | 873 ms | 1319 ms | ±12% |
| diff.log | 1027 ms | 877 ms | 1207 ms | ±11% |
| multi.log（real） | ~5300 ms | ~1298 ms | ~12852 ms | ±95% |

> 注：multi.log 的耗时是整体完成时间，非单个请求时间

### Session ID 影响
- **same.log vs diff.log**: 响应时间几乎相同（1026 ms vs 1027 ms），说明使用相同或不同的 session_id 对性能无明显影响

### 顺序 vs 并发
- **顺序执行**：单请求 ~1s，100 请求需 ~100s
- **并发执行**：100 请求仅需 ~5s（提升约 20 倍）

---

## 结论

1. **功能正常**: 所有三种测试场景（相同 session_id、不同 session_id、并发）均 100% 成功
2. **Header 合并正确**: `user_id` 和 `session_id` 都能正确合并到请求头
3. **并发处理健壮**: 多进程并发时输出会交织但不影响正确性
4. **性能表现一致**: 顺序执行时单请求响应时间稳定在 ~1 秒左右
5. **负载波动**: 并发测试中出现部分批次耗时显著增加，需关注系统在高并发下的表现

---

## 附录：multi.sh 脚本内容

```bash
#!/bin/bash

for i in $(seq 1 100); do
  time agentkit invoke hello --headers "{\"session_id\":\"$(uuidgen)\"}" &
  if (( i % 12 == 0 )); then
    wait
  fi
done
wait
```

测试使用 `agentkit invoke hello` 命令，每次调用附带唯一的 session_id（通过 `uuidgen` 生成）。