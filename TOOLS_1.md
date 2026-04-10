# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS (MiniMax)

- Skill: `minimax-multimodal` (scripts/tts/generate_voice.sh)
- API: MiniMax T2A v2 (`speech-2.8-hd` model)
- Default voice: `English_Trustworthy_Man` (贾维斯风格，用这个音色说中文)
- 飞书语音消息: MiniMax TTS → FFmpeg转opus → 飞书audio发送（原生语音气泡）
- Other voices: `Chinese (Mandarin)_Warm_Bestie` (温暖闺蜜), `male-qn-badao` (霸道青年), `male-qn-jingying` (精英青年), `female-shaonv` (少女), `Chinese (Mandarin)_News_Anchor` (新闻女声), `audiobook_male_1` (有声书男), `audiobook_female_1` (有声书女)
- Output: MP3 → opus conversion via ffmpeg for Feishu voice bubbles
```

### 新闻信息图生成
- Skill: news-card-generator
- 脚本: /home/node/.openclaw/workspace/scripts/gen_news_card.py
- 字体: /home/node/.openclaw/fonts/NotoSansSC.otf
- 输出: news_card_YYYYMMDD.png

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 🌐 Web Search APIs

优先使用顺序（按速度）：
1. **Exa** (最快, ~0.6s) — `56bd0b16-06b9-4033-9481-194072b15ac4`
2. **Tavily** (中等, ~5s) — `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`
3. **Brave** (较慢, ~14s) — `BSAQ2bYQGqpOQMccZU0v-Un2U2ETzTB`

### 飞书机器人
- Agent: jarvis (贾维斯)
  - App ID: cli_a91aaec79c789cd1
  - App Secret: 51GB1nOln1aSE1APF1RmvcMkwZBKHXHu
  - 绑定: jarvis → main
