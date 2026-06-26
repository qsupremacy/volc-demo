# same.log & diff.log 日志分析报告

**分析日期**: 2026-06-26
**测试工具**: agentkit invoke
**应用版本**: 已带主机名 + 全局计数器（simple_agent.py 改造后）

---

## 概览

| 日志文件 | 测试类型 | 请求数 | 成功率 | 总耗时 | 时间范围 |
|---------|---------|-------|-------|-------|---------|
| same.log | 顺序执行（相同 session_id） | 100 | 100% | 36 秒 | 11:31:05 - 11:31:41 |
| diff.log | 顺序执行（不同 session_id） | 100 | 100% | 14 秒 | 11:32:49 - 11:33:03 |

---

## 1. same.log - 相同 Session ID 测试

### 测试配置
- **Session ID**: `same-session-id`（所有请求共用）
- **执行方式**: 顺序执行
- **请求数**: 100

### 性能统计

| 指标 | 值 |
|-----|-----|
| **平均耗时** | 359.9 ms |
| **中位数 (P50)** | 110 ms |
| **P90** | 145 ms |
| **P95** | 239 ms |
| **P99** | 587 ms |
| **最大耗时** | 23279 ms（request 92） |
| **最小耗时** | 95 ms |

### 耗时分布

| 区间 | 次数 | 占比 |
|------|------|------|
| < 100 ms | 2 | 2% |
| 100-150 ms | 87 | 87% |
| 150-300 ms | 7 | 7% |
| 300-500 ms | 2 | 2% |
| 500-1000 ms | 1 | 1% |
| > 1000 ms | 1 | 1% |

### 多主机分布

| 主机 | 请求数 | 占比 | 备注 |
|------|-------|------|------|
| `tsy4t02h-4q8bua7bk6-5fc58bd544-cd2wx` | 50 | 50% | 主处理节点 |
| `vefaas-tsy4t02h-4q8bua7bk6-d8uura3m6c5ik6a1mdtg` | 41 | 41% | 第二节点 |
| `vefaas-tsy4t02h-4q8bua7bk6-d8uv519e95toqnjv5irg` | 9 | 9% | 新增节点（request 92 起） |

### 计数器信息
- **计数器范围**: 1-55（来自 3 台主机的请求计数累加）
- 由于多机/多进程独立计数，全局计数器在 3 台机器上分别从 #1 开始
- 同主机内 #1, #2, #3... 连续递增

### 异常请求
- **Request 92** (新主机首次处理): 23279 ms
  - 出现在 11:31:40，恰好是新节点 `d8uv519e95toqnjv5irg` 首次接收请求
  - 推测为新节点冷启动开销
  - 后续请求 93-100 在 106-239 ms 之间，恢复正常

### 典型日志示例

```
[2026-06-26 11:31:05] Starting request 1
"mock message from tsy4t02h-4q8bua7bk6-5fc58bd544-cd2wx (request #1)"[2026-06-26 11:31:05] Finished request 1 - elapsed: 131 ms
[2026-06-26 11:31:05] Starting request 2
"mock message from tsy4t02h-4q8bua7bk6-5fc58bd544-cd2wx (request #2)"[2026-06-26 11:31:06] Finished request 2 - elapsed: 127 ms
```

---

## 2. diff.log - 不同 Session ID 测试

### 测试配置
- **Session ID**: 每次请求使用不同的 UUID
- **执行方式**: 顺序执行
- **请求数**: 100

### 性能统计

| 指标 | 值 |
|-----|-----|
| **平均耗时** | 144.0 ms |
| **中位数 (P50)** | 113 ms |
| **P90** | 133 ms |
| **P95** | 148 ms |
| **P99** | 1141 ms |
| **最大耗时** | 1792 ms（request 68） |
| **最小耗时** | 95 ms |

### 耗时分布

| 区间 | 次数 | 占比 |
|------|------|------|
| < 100 ms | 3 | 3% |
| 100-150 ms | 92 | 92% |
| 150-300 ms | 3 | 3% |
| 300-1000 ms | 0 | 0% |
| > 1000 ms | 2 | 2% |

### 多主机分布

| 主机 | 请求数 | 占比 |
|------|-------|------|
| `tsy4t02h-4q8bua7bk6-5fc58bd544-ckskc` | 31 | 31% |
| `vefaas-tsy4t02h-4q8bua7bk6-d8uura3m6c5ik6a1mdtg` | 25 | 25% |
| `vefaas-tsy4t02h-4q8bua7bk6-d8uv519e95toqnjv5irg` | 25 | 25% |
| `tsy4t02h-4q8bua7bk6-5fc58bd544-cd2wx` | 19 | 19% |

### 计数器信息
- **计数器范围**: 1-80
- 4 台主机各自分别从 #1 开始计数
- 整体分布更均匀，反映多机负载均衡

### 异常请求
- **Request 68**: 1792 ms（`d8uura3m6c5ik6a1mdtg` 处理，request #66）
- **Request 82**: 1141 ms（`d8uura3m6c5ik6a1mdtg` 处理，request #69）
- 两台异常请求都来自同一台主机 `d8uura3m6c5ik6a1mdtg`，建议关注该节点健康状态

### 典型日志示例

```
[2026-06-26 11:32:49] Starting request 1
"mock message from tsy4t02h-4q8bua7bk6-5fc58bd544-ckskc (request #1)"[2026-06-26 11:32:49] Finished request 1 - elapsed: 113 ms
[2026-06-26 11:32:49] Starting request 2
"mock message from tsy4t02h-4q8bua7bk6-5fc58bd544-ckskc (request #2)"[2026-06-26 11:32:49] Finished request 2 - elapsed: 186 ms
```

---

## 对比分析

### 核心指标对比

| 指标 | same.log | diff.log | 差异 |
|------|----------|----------|------|
| 平均耗时 | 359.9 ms | 144.0 ms | same 慢 2.5x |
| 中位数 | 110 ms | 113 ms | 相当 |
| P90 | 145 ms | 133 ms | diff 略快 |
| P95 | 239 ms | 148 ms | same 受异常拖累 |
| 最大耗时 | 23279 ms | 1792 ms | same 高 13x |
| 最小耗时 | 95 ms | 95 ms | 相同 |
| 主机数 | 3 | 4 | diff 多 1 台 |
| 异常请求数 | 1 (>1s) | 2 (>1s) | diff 略多 |

### 关键发现

1. **中位数相近**（110ms vs 113ms）：说明稳态性能无明显差异
2. **same.log 极端异常**（23279ms）显著拉高平均值：因新节点冷启动
3. **diff.log 异常更分散**（1.7s、1.1s）：可能是随机网络抖动
4. **多机分布**：
   - same.log 集中在 2 台机器，新增第 3 台时出现冷启动延迟
   - diff.log 4 台机器分布更均匀
5. **计数器独立性**：每台主机/进程的计数器独立从 1 开始，符合 Python 全局变量的预期行为

### Session ID 影响
- 使用相同 vs 不同 session_id 对稳态性能影响极小
- 但**不同 session_id** 触发的请求更均匀地分布到多台后端节点
- **相同 session_id** 可能命中同一后端的缓存/会话状态，引入热点

---

## 结论

1. **功能正常**: 两个测试均 100% 成功
2. **多机负载**: 后端至少 3-4 个处理节点，多机间请求会动态分配
3. **新节点冷启动**: same.log 的 23279ms 异常来自新节点首次启动（23 秒），需关注实例池预热
4. **抖动监控**: diff.log 两次 ~1.7s 异常需要进一步定位根因（同一节点）
5. **性能稳定**: 去除异常值后，两个测试的 P95 都在 250ms 以内

---

## 建议

1. **预热机制**: 新节点加入时先做预热请求，避免冷启动影响用户
2. **异常告警**: 单次请求 > 1s 应触发告警，关注 `d8uura3m6c5ik6a1mdtg` 节点
3. **跨进程计数**: 当前 `_request_counter` 是进程级，多 worker 部署时各算各的。如需全局统计，建议接入 Redis
4. **响应字段**: 当前响应已包含 hostname 和 request #，便于定位后端实例

---

## 附录

### simple_agent.py 改造内容

```python
import socket
import threading

_counter_lock = threading.Lock()
_request_counter = 0
_hostname = socket.gethostname()

# 在入口函数中
global _request_counter
with _counter_lock:
    _request_counter += 1
    current_count = _request_counter
response = f"mock message from {_hostname} (request #{current_count})"
```