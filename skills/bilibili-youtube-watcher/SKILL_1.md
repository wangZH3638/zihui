---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 304502207ed8cd8ac69854d177f3131b04bb320db795ace22f7aa1a1636a8e9d24fcdf6202210084e481b8346ae6548fdcdcbde3e462314769a0bf3903479ba48d2bfd9fe22b0f
    ReservedCode2: 304502207c5cabfd88f966f76d9f697e56984e67eb5b95ace25db40d7bda2f046bf91b33022100a6a7de1ea78472e05156a1c255d5ed0e7793c2d57706a77d975789ed42c313d4
author: adapted from youtube-watcher
description: Fetch and read transcripts from YouTube and Bilibili videos. Use when you need to summarize a video, answer questions about its content, or extract information from it.
metadata:
    clawdbot:
        emoji: "\U0001F4FA"
        install:
            - bins:
                - yt-dlp
              formula: yt-dlp
              id: brew
              kind: brew
              label: Install yt-dlp (brew)
            - bins:
                - yt-dlp
              id: pip
              kind: pip
              label: Install yt-dlp (pip)
              package: yt-dlp
        requires:
            bins:
                - yt-dlp
name: video-watcher
triggers:
    - watch video
    - summarize video
    - video transcript
    - youtube summary
    - bilibili summary
    - analyze video
version: 1.1.0
---

# Video Watcher

Fetch transcripts from **YouTube** and **Bilibili** videos to enable summarization, QA, and content extraction.

## Supported Platforms

- ✅ **YouTube** (youtube.com, youtu.be)
- ✅ **Bilibili** (bilibili.com, b23.tv)

## Usage

### Get Transcript (Auto-detect Platform)

```bash
python3 {baseDir}/scripts/get_transcript.py "VIDEO_URL"
```

### Specify Language

```bash
python3 {baseDir}/scripts/get_transcript.py "VIDEO_URL" --lang zh-CN
```

## Examples

### YouTube Video
```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Bilibili Video
```bash
python3 {baseDir}/scripts/get_transcript.py "https://www.bilibili.com/video/BV1xx411c7mD"
```

### With Custom Language
```bash
# Get English subtitles for a Bilibili video
python3 {baseDir}/scripts/get_transcript.py "https://bilibili.com/video/..." --lang en

# Get Chinese subtitles for a YouTube video
python3 {baseDir}/scripts/get_transcript.py "https://youtube.com/watch?v=..." --lang zh-CN
```

## Default Languages

| Platform | Default Language |
|----------|-----------------|
| YouTube  | `en` (English)  |
| Bilibili | `zh-CN` (Chinese) |

## Common Language Codes

- `en` - English
- `zh-CN` - Simplified Chinese (简体中文)
- `zh-TW` - Traditional Chinese (繁體中文)
- `ja` - Japanese
- `ko` - Korean
- `es` - Spanish
- `fr` - French
- `de` - German

## Notes

- Requires `yt-dlp` to be installed and available in PATH
- Works with videos that have closed captions (CC) or auto-generated subtitles
- Automatically detects platform from URL
- If no subtitles available, the script will fail with an error message
- yt-dlp natively supports both YouTube and Bilibili
