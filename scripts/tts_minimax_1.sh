#!/bin/bash
# MiniMax TTS 合成工具
# 用法: tts_minimax.sh "要合成的文本" [voice_id] [输出文件路径]

API_KEY="sk-cp-EN_b7oI9Yl0z7uoPmcjIF3LOk1XO4ds8SuX5cL4h3TlmPZofk84PHhbuCakm8xZ9XgdxW1Dyv1hm1GiiOSF50V4bv05GH8MhRxjYWGociJQj6JiEJkvT1YI"
TEXT="${1:-你好，这是语音合成测试}"
VOICE="${2:-Chinese (Mandarin)_Warm_Bestie}"
OUTPUT="${3:-/home/node/.openclaw/workspace/tts_output.mp3}"

curl -s -X POST "https://api.minimaxi.com/v1/t2a_v2" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"speech-2.8-hd\",
    \"text\": \"$TEXT\",
    \"stream\": false,
    \"voice_setting\": {
      \"voice_id\": \"$VOICE\",
      \"speed\": 1,
      \"vol\": 1,
      \"pitch\": 0,
      \"emotion\": \"happy\"
    },
    \"audio_setting\": {
      \"sample_rate\": 32000,
      \"bitrate\": 128000,
      \"format\": \"mp3\",
      \"channel\": 1
    }
  }" | python3 -c "
import json,sys,binascii
d=json.load(sys.stdin)
if d.get('data',{}).get('audio'):
    audio=binascii.unhexlify(d['data']['audio'])
    with open('$OUTPUT','wb') as f: f.write(audio)
    print('OK:', len(audio), 'bytes -> $OUTPUT')
else:
    print('ERROR:', d.get('base_resp',{}).get('status_msg','unknown'))
"