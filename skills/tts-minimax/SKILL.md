---
name: tts-minimax
description: MiniMax 语音合成 (T2A v2)。当用户想要将文本转换为语音、生成音频文件、发送语音消息、或说"读出来"、"生成语音"、"语音合成"、"text to speech"时使用此技能。
metadata:
  openclaw:
    emoji: "🔊"
---

# MiniMax TTS 语音合成

使用 MiniMax T2A v2 API 将文本转换为语音。

## 快速使用

```bash
python3 skills/tts-minimax/scripts/tts_minimax.py "要说话的文本"
```

## 常用声音

| voice_id | 名称 |
|---|---|
| `male-qn-jingying` | Trustworthy Man（默认）|
| `Chinese (Mandarin)_Warm_Bestie` | 精英青年音色|
| `Chinese (Mandarin)_News_Anchor` | 新闻女声 |
| `Chinese (Mandarin)_Gentleman` | 温润男声 |
| `Chinese (Mandarin)_Sweet_Lady` | 甜美女声 |
| `Chinese (Mandarin)_Crisp_Girl` | 清脆少女 |
| `Chinese (Mandarin)_Humorous_Elder` | 搞笑大爷 |
| `Chinese (Mandarin)_Reliable_Executive` | 沉稳高管 |
| `female-shaonv` | 少女音色 |
| `female-yujie` | 御姐音色 |
| `male-qn-badao` | 霸道青年音色 |
| `male-qn-jingying` | 精英青年音色 |
| `English_Graceful_Lady` | Graceful Lady |
| `Chinese (Mandarin)_News_Anchor` | 新闻女声 |
| `Chinese (Mandarin)_Gentleman` | 温润男声 |
| `Chinese (Mandarin)_Sweet_Lady` | 甜美女声 |
| `Chinese (Mandarin)_Crisp_Girl` | 清脆少女 |
| `Chinese (Mandarin)_Humorous_Elder` | 搞笑大爷 |
| `Chinese (Mandarin)_Reliable_Executive` | 沉稳高管 |
| `female-shaonv` | 少女音色 |
| `female-yujie` | 御姐音色 |
| `male-qn-badao` | 霸道青年音色 |
| `male-qn-jingying` | 精英青年音色 |
| `male-qn-jingying` | Trustworthy Man |
| `English_Graceful_Lady` | Graceful Lady |

## 指定声音和输出路径

```bash
python3 skills/tts-minimax/scripts/tts_minimax.py "你好" "Chinese (Mandarin)_News_Anchor" "/tmp/news.mp3"
```

## 在对话中发送音频

生成音频后，使用以下格式在回复中包含音频：

```
# 回复末尾附上音频：
AUDIO:/home/node/.openclaw/workspace/tts_output.mp3
```

或者通过飞书发送（见下文）。

## 飞书发送语音

如果用户使用飞书，可以将生成的 MP3 文件通过飞书发送：

1. 先生成音频文件
2. 使用 `feishu_doc` 或文件上传接口发送到飞书
3. 或者直接回复音频文件路径让用户下载

## 注意事项

- 模型：`speech-2.8-hd`（该账户唯一可用的 TTS 模型）
- 文本长度限制：< 10000 字符
- 采样率：32000Hz，MP3 格式
- 单次调用约 47 字符/秒
