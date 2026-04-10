---
name: news-card-generator
description: 生成新闻信息图卡片。支持多页分类、全面内容、层级清晰、动态排版。
---

# 新闻信息图卡片生成

## 设计规范

### 画布设置
- 尺寸：1080x1440（3:4竖版）
- 背景色：#E8E6E3（浅灰米色）
- 内边距：50px

### 配色方案
- 背景：#E8E6E3
- 文字主色：#2D2D2D（深炭黑）
- 文字次级：#6B7280（中灰）
- 强调色：#E85D04（活力橙）
- 卡片背景：白色
- 辅助色：#3B82F6蓝 / #4CAF50绿 / #9C27B0紫 / #DC4345红 / #20C997青

### 字体层级（重要）
| 元素 | 字号 | 颜色 | 说明 |
|------|------|------|------|
| 主标题 | 52px | #2D2D2D | 最大，深色 |
| 副标题/标签 | 20px | 彩色 | 次级，彩色标签色 |
| 正文描述 | 19px | #6B7280 | 较小，灰色 |
| 关键信息 | 18px | 彩色 | 强调，彩色 |
| 日期/页脚 | 15-20px | #6B7280 | 最小，灰色 |

### 多页结构（按类目分页）
1. **政治/地缘局势页**
2. **经济/市场动态页**
3. **总结与展望页**
   - 核心要点（3条）
   - 未来展望（3条）
   - 关键数据一览

## 排版规则

### 动态格子高度
- 卡片高度根据内容行数**动态计算**
- 公式：`高度 = 标题区 + 内容行数 × 行高 + 间距`
- 使用 `draw_wrapped_text()` 自动换行

### 内容对齐规则
- **标签+内容同行**：标签（如"地缘政治："）和后续内容在同一行开始
- 不要换行导致错位
- 使用固定宽度估算确保对齐

### 动态高度计算示例
```python
def calc_summary_height(items, font_size, line_height):
    max_lines = max(len(wrap(item, width)) for item in items)
    return 60 + max_lines * line_height + 25
```

## 文案逻辑
- **总分结构**：结论先行，再展开详情
- 主新闻：先说结果/结论，再说过程/原因
- 卡片：先说核心结论，再说详细描述

## 内容总结与分析（必须）
每页底部必须有"编辑点评"区域：
- 2-3条核心要点
- 简短精炼，一句话一条
- 帮助读者快速把握重点

## 新闻真实性原则（必须）
- 所有数据必须来自可靠来源
- 生成前核实关键事实（比分、排名、球员所属球队等）
- 不确定的信息标注或跳过，不能编造

## 生成脚本
```bash
# 多页新闻版（政治+经济+总结）
python3 /home/node/.openclaw/workspace/scripts/gen_multi_news.py

# NBA版
python3 /home/node/.openclaw/workspace/scripts/gen_nba_card.py

# Polymarket预测市场版
python3 /home/node/.openclaw/workspace/scripts/gen_polymarket_card.py
```

## 输出路径
- 政治页：political_card_YYYYMMDD.png
- 经济页：economy_card_YYYYMMDD.png
- 总结页：summary_card_YYYYMMDD.png
- NBA页：nba_card_YYYYMMDD.png
- 预测市场：polymarket_card_YYYYMMDD.png

## 发送方式
1. 优先微信直接发送
2. 失败时上传到飞书文档
