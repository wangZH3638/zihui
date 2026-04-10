# OpenClaw × Claw Code 优化实施报告

**日期：** 2026-04-07  
**基于：** Claw Code 架构分析 + OpenClaw 源码调研

---

## 📊 调研结论

| Claw Code 特性 | OpenClaw 等效方案 | 状态 |
|---------------|-----------------|------|
| `is_error` + `return_code` | exec 已返回 `code` 字段 | ✅ 已有 |
| `maxTurns=8` 限制 | `tools.loopDetection` | ✅ 可配置 |
| `autoDream` 记忆整合 | `memoryFlush` + 自定义脚本 | 🟡 需补充 |
| `compact_after_turns=12` | `compaction.memoryFlush` | ✅ 已有 |
| 沙箱隔离 | `tools.exec.host=sandbox` | ✅ 已有 |

---

## ✅ 已实施优化

### 1. exec 结果结构化认知（已记录）

**发现：** OpenClaw 的 `exec` 工具底层 `runCommandWithTimeout` 已返回完整结构：
```javascript
{
  pid, stdout, stderr,
  code: 0,           // 0=成功，非0=失败
  signal, killed, termination, noOutputTimedOut
}
```

**问题：** 结果传回模型时可能变成纯文本。  
**方案：** 创建 skill `exec-structured/SKILL.md`，规范结果解读方式。

**使用规范：**
- `code !== 0` → 明确告知用户命令失败
- `killed === true` → 告知用户被终止（超时/信号）
- `stderr` 有内容 → 即使 code=0 也显示错误信息

---

### 2. Loop Detection（防止循环烧 Token）

**原理：** Claw Code 的 `maxTurns=8` 是硬限制。OpenClaw 的 `loopDetection` 更智能——基于模式检测而非简单计数。

**已配置优化值：**
```json
{
  "tools": {
    "loopDetection": {
      "enabled": true,
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

**效果：**
- 同一工具调用 6 次 → 警告
- 12 次 → 阻止调用
- 20 次 → 全局熔断

---

### 3. autoDream 记忆自动整理（新建脚本）

**差距：** Claw Code 的 `autoDream` 在 idle 时后台自动整理记忆。OpenClaw 只有 `memoryFlush`（压缩前触发），缺少定期主动整理。

**解决方案：** 创建 `scripts/auto_dream.sh`

**功能：**
- 扫描 `memory/` 目录下过去 7-30 天的日志
- 提取 `[决策]` `[教训]` `[偏好]` `[待办]` 标签内容
- 追加结构化摘要到 `MEMORY.md`
- 自动归档 60 天前的旧日志

**安装方式：**
```bash
# 每周一 09:00 自动运行
0 9 * * 1 bash /home/node/.openclaw/workspace/scripts/auto_dream.sh
```

**标签规范（建议在日志中使用）：**
```
[决策] 使用 MiniMax T2A v2 做 TTS
[教训] exec 不要返回空内容给模型
[偏好] 信息图来源统一用 Bleacher Report
[待办] 配置飞书机器人语音气泡
```

---

## 📁 新增文件

| 文件 | 说明 |
|------|------|
| `scripts/auto_dream.sh` | autoDream 记忆整理脚本 |
| `scripts/openclaw_optimizations.md` | 优化配置文档 |
| `skills/exec-structured/SKILL.md` | exec 结果结构化规范 |

---

## 🔧 推荐配置命令

```bash
# 1. 启用 loopDetection（立即生效）
openclaw config set tools.loopDetection.enabled true
openclaw config set tools.loopDetection.warningThreshold 6
openclaw config set tools.loopDetection.criticalThreshold 12

# 2. Session 维护加强
openclaw config set session.maintenance.mode enforce
openclaw config set session.maintenance.pruneAfter 30d

# 3. Compaction 调优
openclaw config set agents.defaults.compaction.memoryFlush.enabled true
```

---

## 📈 预期效果

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| Agent 循环风险 | 中 | 低（loopDetection 拦截） |
| 记忆可用性 | 依赖手动整理 | 自动每周整理 |
| Session 膨胀 | 30天后开始 | 自动清理 |
| exec 误判 | 可能 | 减少（明确标注错误） |

---

## ⚠️ 限制说明

1. **is_error 显式字段**：OpenClaw exec 底层返回 `code`，但上层可能丢失类型信息。这是框架层限制，建议向 OpenClaw 提 Feature Request。

2. **autoDream vs memoryFlush**：Claw Code 的 autoDream 是真正的 idle-time 后台进程。OpenClaw 方案是 cron 触发的定时任务，实时性稍差但更稳定。

3. **maxTurns 硬限制**：OpenClaw 没有 `maxTurns` 硬限制选项，只有 loopDetection 软保护。对于大多数场景足够，极端情况可用 `/stop` 中断。

---

*报告生成时间：2026-04-07 12:10 UTC*

---

## 执行记录 (2026-04-07 12:13 UTC)

### ✅ 已执行并生效

| 配置 | 命令 | 状态 |
|------|------|------|
| loopDetection.enabled | `openclaw config set tools.loopDetection.enabled true` | ✅ 已写入 openclaw.json |
| loopDetection.warningThreshold=6 | `openclaw config set tools.loopDetection.warningThreshold 6` | ✅ 已写入 |
| loopDetection.criticalThreshold=12 | `openclaw config set tools.loopDetection.criticalThreshold 12` | ✅ 已写入 |
| session.maintenance.mode=enforce | `openclaw config set session.maintenance.mode enforce` | ✅ 已写入 |
| compaction.memoryFlush.enabled | `openclaw config set agents.defaults.compaction.memoryFlush.enabled true` | ✅ 已写入 |
| compaction.memoryFlush.softThresholdTokens=3000 | `openclaw config set agents.defaults.compaction.memoryFlush.softThresholdTokens 3000` | ✅ 已写入 |
| auto_dream.sh 试运行 | `bash scripts/auto_dream.sh` | ✅ 已执行（正常） |

### ⚠️ 需要宿主机配合（容器内无 cron）

autoDream cron 任务需要在 **T2S 宿主机** 上配置：

```bash
# 在 T2S 上执行（不是容器内）
crontab -e
# 添加：
0 9 * * 1 bash /home/node/.openclaw/workspace/scripts/auto_dream.sh >> /home/node/.openclaw/workspace/memory/auto_dream.log 2>&1
```

### 🔄 需要重启 Gateway 生效

修改的配置需要重启 Gateway：
```bash
openclaw gateway restart
```

### 📊 auto_dream.sh 首次运行结果

```
[2026-04-07 12:13:06] === autoDream started ===
[2026-04-07 12:13:06] No significant content found to summarize
[2026-04-07 12:13:06] === autoDream completed ===
```

原因：现有 memory 文件中没有 `[决策]` `[教训]` `[偏好]` 等标签格式内容。
脚本已就绪，等标签内容积累后下次会自动提取。

