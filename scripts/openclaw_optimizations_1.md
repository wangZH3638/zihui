# OpenClaw 优化配置

基于 Claw Code 架构分析，为 OpenClaw 添加以下优化。

## 1. Loop Detection（防止 Agent 循环失控）

OpenClaw 内置了 `tools.loopDetection`，配置后效果类似 Claw Code 的 `maxTurns` 限制。

```bash
# 查看当前 loopDetection 配置
openclaw config get tools.loopDetection

# 启用并调优
openclaw config set tools.loopDetection.enabled true
openclaw config set tools.loopDetection.warningThreshold 6
openclaw config set tools.loopDetection.criticalThreshold 12
openclaw config set tools.loopDetection.globalCircuitBreakerThreshold 20
```

或直接编辑 `~/.openclaw/openclaw.json`：

```json
{
  "tools": {
    "loopDetection": {
      "enabled": true,
      "historySize": 30,
      "warningThreshold": 6,
      "criticalThreshold": 12,
      "globalCircuitBreakerThreshold": 20,
      "detectors": {
        "genericRepeat": true,
        "knownPollNoProgress": true,
        "pingPong": true
      }
    }
  }
}
```

**说明：**
- `warningThreshold=6`：同一工具调用6次后发出警告
- `criticalThreshold=12`：12次后阻止调用，防止 Token 浪费
- Claw Code 的 `maxTurns=8` 更严格，但 OpenClaw 的 loopDetection 更智能（基于模式检测而非简单计数）

---

## 2. autoDream 记忆整理 Cron

创建每周一上午9点自动运行的记忆整理：

```bash
# 编辑 crontab
crontab -e

# 添加这一行：
0 9 * * 1 bash /home/node/.openclaw/workspace/scripts/auto_dream.sh >> /home/node/.openclaw/workspace/memory/auto_dream.log 2>&1
```

auto_dream.sh 功能：
- 分析过去30天的 memory 日志
- 提取关键决策、教训、偏好
- 追加到 MEMORY.md
- 自动归档60天前的旧日志

---

## 3. Session 维护优化

加强 session 清理，防止无限膨胀：

```bash
openclaw config set session.maintenance.mode enforce
openclaw config set session.maintenance.pruneAfter 30d
openclaw config set session.maintenance.maxEntries 500
```

---

## 4. Compaction 调优

调整自动压缩策略，更积极地管理上下文窗口：

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "mode": "safeguard",
        "reserveTokensFloor": 15000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 3000
        }
      }
    }
  }
}
```

---

## 验证优化效果

```bash
# 检查 loopDetection 状态
openclaw status

# 查看 session 统计
openclaw sessions --json | jq 'length'

# 查看上下文使用
openclaw status | grep -i context
```
