# MEMORY.md - 长期记忆

## 用户信息
- 姓名: 王子辉
- 飞书ID: ou_dd7de58278bf2895b6ef35a2720b7471

## 我的身份
- 名字: 贾维斯 (Jarvis)
- 服务于王子辉

## 系统配置

### Skills (18个)
- self-improving, proactive-agent, skill-vetter, find-skills
- feishu-bot-manager, obsidian-*, agent-reach, github-repo-search

### 硬件环境
- 宿主机: 极空间Zima T2S（ARM64 Linux NAS）
- OpenClaw运行在Docker容器里

### 语音输入配置（待生效）
- 容器内已安装 openai-whisper（mlx-whisper不支持ARM64，用替代方案）
- Whisper small中文模型已下载至 ~/.cache/whisper
- STT配置已写入 ~/.openclaw/openclaw.json → tools.media.audio
- 需要在T2S上执行 `docker restart <容器名/ID>` 重启容器后才能生效

### 关键路径
- Workspace: /home/node/.openclaw/workspace
- Obsidian同步: /home/node/.openclaw/workspace/obsidian → GitHub: wangZH3638/zihui
- 智能收藏: ~/Obsidian/shoucang/

## 语音配置
- TTS: tts-minimax 技能，MiniMax T2A v2，声音 English_Trustworthy_Man（贾维斯默认音色）
- 飞书语音消息：MiniMax TTS → FFmpeg转换opus → 飞书audio消息发送（原生语音气泡）
- 默认音色：English_Trustworthy_Man（英文音色说中文，有英式口音，习惯后很自然）

## 飞书语音气泡
- Skill: feishu-voice-bubble
- 使用 Edge TTS 生成 .opus 文件，通过飞书 audio 消息发送为原生语音气泡
- 免费、无需API key
- 路径: ~/.openclaw/workspace/skills/feishu-voice-bubble
- 如需更好音质，可调用 MiniMax TTS 生成音频，再用 ffmpeg 转换 为 .opus 格式发送

## 品牌标识
- 每张知识卡片右上角固定包含：
  - **2026** — 大号淡色数字（88px，极淡透明度）
  - **陕西杰森** — 金色文字（27px），位于2026下方

## 语音配置
- TTS声音: English_Trustworthy_Man (male-qn-jingying)
- 这是贾维斯的固定声音，以后所有TTS回复都用这个音色

## 用户偏好（重要）

### 设计类
- **视觉风格**：蓝灰分析风，浅色背景，不要太深太重
- **emoji**：一律用文字符号替代，不使用emoji
- **术语标注**：专业简称（BPD等）旁加小字备注
- **顶部比例**：紧凑，留白不要太多

### 内容术语
- "伴侣行为对照" → 改为"亲密关系对照"（更准确）

### 沟通风格
- 有不同意见直接提，不要随声附和，是讨论不是确认
- 用户不喜欢"好的没问题"这类敷衍回应

### 项目信息
- **你也懂点心理学**：心理学科普系列，作者笔名「辉常心理」
- 配色：浅蓝白背景 + 主色 #00b4dc
- 卡片结构：01开篇 → 02-04 A簇 → 05-08 B簇 → 09-11 C簇 → 12投票结尾

## 快捷指令
- 说"信息图" → 自动生成HTML + 截图 + 发PNG给用户
- 说"读出来" → 用 English_Trustworthy_Man 音色语音播报

## 信息图生成策略

### 流程
1. 生成HTML文件 → `minimax-output/xxx.html`
2. Playwright截图 → `minimax-output/xxx.png`
3. 直接发送到微信

### 风格
**浅色科技风（首选）**
- 白色/浅灰渐变背景
- 蓝紫渐变强调色 `#667eea → #764ba2`
- 圆角卡片 + 左侧彩色边框
- 卡片悬浮动画

### 图标方案（容器无emoji字体）
使用文字符号：
| 含义 | 符号 |
|------|------|
| 金钱 | [$] |
| 石油 | [OIL] |
| 芯片/英伟达 | [GPU] |
| 银行 | [BANK] |
| 购物 | [SHOP] |
| 房产 | [HOME] |
| 电力 | [PWR] |
| 百分比 | [%] |
| 增长 | [↑] |
| 下降 | [↓] |

### 内容结构
1. 标题区 - 主标题 + 日期 + 标签
2. 对比卡片 - 左右两栏（主题A vs 主题B）
3. 数据网格 - 4列关键数据
4. 新闻网格 - 3x2热点新闻
5. 底部来源 - 数据出处

### 截图脚本
`/home/node/.openclaw/workspace/scripts/html_screenshot.py`
Chromium路径：`~/.cache/ms-playwright/chromium-1208/chrome-linux/chrome`

## 新闻生成原则
- 所有新闻简报必须严格遵守真实性

## 信息图新闻来源
- **NBA/NFL/MLB 来源之一：** Bleacher Report (bleacherreport.com)

- 以后NBA信息图直接用Bleacher Report作为新闻来源
- 数据必须来自可靠来源并核实
- 不确定的信息要标注或跳过，不能编造
- 核实关键事实：比分、排名、球员所属球队等

## sherpa-onnx 备选方案

**定位：** 语音输入备选方案（目前用 OpenAI Whisper，够用）

**已调研：**
- 安装：`pip install sherpa-onnx sherpa-onnx-bin`，模型 SenseVoice int8（228MB，中英日韩粤）
- 优势：VAD 断句、说话人识别、本地离线、无需 API key
- 局限：语音唤醒需要**带麦克风的智能音箱**等硬件支持，T2S NAS 目前没有
- 触发条件：有智能音箱（支持语音唤醒）→ sherpa-onnx 接管本地 STT/TTS

**触发条件：**
- MiniMax API 频繁限流 → 可用本地 TTS 兜底
- 有新的硬件设备（如 USB 麦克风、语音唤醒模块）→ 可启用语音唤醒
- sherpa-onnx 发布重大更新 → 评估是否值得迁移

## 使用习惯
- 每天检查收藏回顾
- 用 self-improving 记录教训

## 教训汇总（持续更新）

### 截图相关
- **微信发图成功率低**，可能需要重试或换方案（2026-04-06）
- **字体加载超时会阻塞截图**，考虑预下载字体或跳过等待（2026-04-06）
- **viewport 和实际内容宽度不匹配会导致白边**，截图脚本 viewport 要和 HTML 卡片宽度一致（2026-04-07）
- **全页截图不能套用固定 viewport**，会截断内容：信息图用全页截图，知识卡片固定 800×1067（2026-04-07）

### exec 工具
- **exec 返回空内容会导致模型误判**，底层已返回 code 字段，但上层可能丢失类型；code !== 0 要明确告知用户失败（2026-04-07）

### 信息图生成
- **Bleacher Report 是 NBA/NFL/MLB 新闻来源之一**（2026-04-05确立，2026-04-07更正）
- **严禁留白**，内容必须填满整个页面（2026-04-05确立）

### 击剑升学系列
- **钩子页比例 45%/37%/18%**，其他页面 32%/52%/16%（2026-04-06确立）
- **引言金句要引发共鸣**，不要说教（2026-04-07）
