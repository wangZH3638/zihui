---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3045022043a4b583f5cedc556d7c21013b77b31c7f2f511e9d7ffe7f479e6cdb7bacd70e022100d953136ce647bf42b0360df8ba0f8cc1255dcbe922de63b73e0cfdd79980e4c1
    ReservedCode2: 30440220626ef1ca2b82b0fc4f1b87f46e66491e8842fe61dd1f9f231940445b329a323a02204412283bed914cb31b923d1a4ae92bf464d73604fd69d8d96cb97d7e12c40121
---

# Corrections Log — Template

> This file is created in `~/self-improving/corrections.md` when you first use the skill.
> Keeps the last 50 corrections. Older entries are evaluated for promotion or archived.

## Example Entries

```markdown
## 2026-02-19

### 14:32 — Code style
- **Correction:** "Use 2-space indentation, not 4"
- **Context:** Editing TypeScript file
- **Count:** 1 (first occurrence)

### 16:15 — Communication
- **Correction:** "Don't start responses with 'Great question!'"
- **Context:** Chat response
- **Count:** 3 → **PROMOTED to memory.md**

## 2026-02-18

### 09:00 — Project: website
- **Correction:** "For this project, always use Tailwind"
- **Context:** CSS discussion
- **Action:** Added to projects/website.md
```

## Log Format

Each entry includes:
- **Timestamp** — When the correction happened
- **Correction** — What the user said
- **Context** — What triggered it
- **Count** — How many times (for promotion tracking)
- **Action** — Where it was stored (if promoted)

## 2026-04-02

### 飞书语音消息方式偏好
CONTEXT: 飞书语音消息发送
USER_SAID: 用 feishu-voice-bubble并调用MiniMax TTS 发飞书语音
REFLECTION: 用户明确要求使用 MiniMax TTS 生成音频，但必须以 feishu-voice-bubble 方式（.opus 格式）发送为原生语音气泡
LESSON: 飞书语音消息 = MiniMax TTS 生成音频 → FFmpeg 转换 .opus → 飞书 audio 消息发送为语音气泡
PATTERN: 以后飞书语音消息必须用此流程（MiniMax TTS + ffmpeg转换 + 飞书audio消息）

## 2026-04-02

### 默认语音音色
CONTEXT: 语音音色选择
USER_SAID: 以后就用这个音色了但要说中文
REFLECTION: 用户确认使用 English_Trustworthy_Man 作为默认音色，但内容要说中文
LESSON: 默认音色 = English_Trustworthy_Man，说中文内容时也用此音色
PATTERN: 贾维斯默认语音音色为 English_Trustworthy_Man，说中文内容
