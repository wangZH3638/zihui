# 信息图生成策略

> 2026-04-05 与王子辉共同确立，2026-04-07 确认最新版本

## 核心流程
需求 → 数据获取 → 布局设计 → HTML → 截图 → 发送

## 数据获取
| 频道 | 来源 |
|------|------|
| GitHub Trending | curl github.com/trending API / github-rank 镜像 |
| Reddit | reddit.com/r/popular API (curl json) |
| **NBA** | Bleacher Report **作为首选来源** + nba.com + ESPN + NBC Sports |
| **NFL** | Bleacher Report（补充来源）|
| **MLB** | Bleacher Report（补充来源）|
| 全球热点 | CBS News / AP News |

## 字号规范（已确定）
| 元素 | 字号 |
|------|------|
| 年份数字 | 88px |
| 主标题 | 48px |
| Hero 标题 | 40-45px |
| 正文（card-body） | 19px |
| 数字统计（stat） | 20px |
| Hero 统计（hero.stat） | 22px |

## 字体
- **统一字体**：Inter（英文，`/home/node/.fonts/custom/Inter-Regular.ttf` + `Inter-Bold.ttf`）
- **中文字符**：自动 fallback 到系统 Noto Sans SC（`/home/node/.fonts/NotoSansCJK.otf`）
- **字体声明**：`font-family: 'Inter', 'NotoSansSC', sans-serif`
- 实际效果：英文用 Inter（漂亮），中文 fallback 到 Noto Sans SC（正确显示）

## 配色系统
```css
:root {
  --black:  #0a0a0a;
  --white:  #fafafa;
  --accent: #ff3366;  /* 可随主题变化，如NBA用ff3366，紫色主题用#6366f1 */
  --cyan:   #00d4ff;
  --gold:   #ffd700;
  --purple: #9945ff;
}
```
标题渐变：`background: linear-gradient(135deg, var(--white) 0%, #9ca3af 100%);`

## 布局结构
- **最终模块数量**：8个模块，排版最自如
- **等宽布局**：6列网格，3列×2列交替，适合内容均等
- **创意不等宽**：h6/h4/h3/h2 混排，示例：6→3+3→3+3→4+2→3+3→6
- **重要：严禁留白！** 内容必须填满整个页面，不留任何空白区域
- **accent bar**：3px左侧渐变，glow 阴影

## 卡片结构
```
[accent bar] | [rank] [icon][title][sub]
             | [card body]
             | [stats]
             | [tags]
```
- accent bar：3px，左侧，glow 阴影
- rank：右上角，大号半透明 opacity 0.05
- icon：30px 圆角，符号代替 emoji
- tags：胶囊标签

## 背景装饰
```css
background:
  radial-gradient(ellipse at 15% 5%,  rgba(accent, 0.22) 0%, transparent 50%),
  radial-gradient(ellipse at 85% 95%, rgba(cyan,   0.14) 0%, transparent 50%);
```
噪点叠加：`opacity: 0.025`

## 第8模块：Jarvis 分析评估（固定）
- **主题**：紫色 [AI] 主题
- **配色**：`background: linear-gradient(135deg, rgba(153,69,255,0.12), rgba(0,212,255,0.08))`
- **内容四维度**：
  - 宏观：全局风险评估
  - 外交：国际关系/地缘政治
  - 内政：国内政治/社会动态
  - 亮点：特别值得关注的事件
- **评分标签**：每条附高/中/低风险标签
  - 高风险：红色背景 `rgba(255,51,102,0.2)` + `#ff3366`
  - 中风险：金色背景 `rgba(255,215,0,0.15)` + `#ffd700`
  - 低风险：青色背景 `rgba(0,212,255,0.15)` + `#00d4ff`

## 截图规范
| 比例 | 视口 | device_scale_factor | 说明 |
|------|------|---------------------|------|
| 竖屏3:4 | 900×1200 | 2 | 固定viewport，内容全页截图 |

**⚠️ 重要**：必须使用全页截图（full_page=True），不能用固定viewport截断内容

## 发送技巧
1. 先发文字消息激活通道，再发图片，成功率更高
2. 图片过长时确保内容全部截取（用全页截图）

## HTML模板关键点
- Inter + Noto Sans SC 字体声明
- viewport initial-scale=1.0 防止缩放
- min-height:1200px 防止内容被压缩
- overflow:hidden 要去掉（允许内容自然延伸）
- 6列 grid + gap:10px
- 卡片使用 grid-column:span 2/3/4/6 控制宽度
