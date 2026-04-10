#!/usr/bin/env python3
"""科技新闻信息图生成器"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# 输出路径
OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/tech_news_card.jpg"

# 配色方案 - 科技感深色主题
COLORS = {
    "bg_dark": "#0a0e27",        # 深蓝黑背景
    "bg_gradient_end": "#1a1f4e", # 渐变结束色
    "accent_blue": "#00d4ff",    # 科技蓝
    "accent_purple": "#7b2cbf",  # 紫色强调
    "text_white": "#ffffff",    # 白色文字
    "text_gray": "#94a3b8",      # 灰色次要文字
    "card_bg": "rgba(255,255,255,0.08)",  # 半透明卡片
    "highlight": "#ff6b35",     # 高亮橙色
}

def create_gradient_background(width, height):
    """创建科技感渐变背景"""
    img = Image.new('RGB', (width, height), COLORS["bg_dark"])
    draw = ImageDraw.Draw(img)
    
    # 垂直渐变
    for y in range(height):
        ratio = y / height
        r = int(10 + ratio * 16)  # 10 -> 26
        g = int(14 + ratio * 17)  # 14 -> 31
        b = int(39 + ratio * 35)  # 39 -> 74
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 绘制网格线
    draw = ImageDraw.Draw(img)
    grid_color = (0, 212, 255, 30)  # 半透明蓝
    
    # 垂直网格线
    for x in range(0, width, 60):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    
    # 水平网格线
    for y in range(0, height, 60):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
    
    # 绘制一些发光的圆点代表数据点
    import random
    random.seed(42)  # 固定种子保证一致性
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(2, 5)
        # 青色发光点
        for i in range(3):
            alpha = 80 - i * 25
            draw.ellipse([x-r-i*2, y-r-i*2, x+r+i*2, y+r+i*2], 
                        fill=(0, 212, 255, alpha))
    
    return img

def draw_text_with_shadow(draw, position, text, font, text_color, shadow_color=(0,0,0,180)):
    """带阴影的文字"""
    x, y = position
    # 阴影
    draw.text((x+2, y+2), text, font=font, fill=shadow_color)
    # 文字
    draw.text((x, y), text, font=font, fill=text_color)

def create_infographic():
    # 尺寸 1080x1440 (3:4竖版)
    width, height = 1080, 1440
    
    # 创建背景
    img = create_gradient_background(width, height)
    draw = ImageDraw.Draw(img)
    
    # 加载字体 (使用系统字体)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_caption = ImageFont.load_default()
    
    center_x = width // 2
    
    # === 顶部标题区 ===
    # 装饰线
    draw.line([(80, 60), (center_x-60, 60)], fill=COLORS["accent_blue"], width=3)
    draw.line([(center_x+60, 60), (width-80, 60)], fill=COLORS["accent_purple"], width=3)
    
    # 标题
    title = "科技前沿"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_width)//2, 30), title, font=font_title, fill=COLORS["text_white"])
    
    # 副标题
    date_text = "2026年4月3日"
    date_bbox = draw.textbbox((0, 0), date_text, font=font_small)
    date_width = date_bbox[2] - date_bbox[0]
    draw.text(((width - date_width)//2, 95), date_text, font=font_small, fill=COLORS["text_gray"])
    
    # === 新闻卡片1: 三星Galaxy S26 Ultra ===
    card1_y = 170
    card1_height = 320
    
    # 卡片背景
    card1 = Image.new('RGBA', (width-80, card1_height), (255,255,255,15))
    card1_draw = ImageDraw.Draw(card1)
    
    # 左边强调条
    card1_draw.line([(0, 20), (0, card1_height-20)], fill=COLORS["accent_blue"], width=4)
    
    # 标签
    card1_draw.text((30, 25), "📱 智能手机", font=font_caption, fill=COLORS["accent_blue"])
    
    # 标题
    card1_draw.text((30, 65), "三星Galaxy S26 Ultra", font=font_subtitle, fill=COLORS["text_white"])
    
    # 正文
    news1_text = "隐私显示技术存在取舍，用户视角度数降低"
    wrapped1 = textwrap.wrap(news1_text, width=32)
    y_pos = 115
    for line in wrapped1:
        card1_draw.text((30, y_pos), line, font=font_body, fill=COLORS["text_gray"])
        y_pos += 38
    
    # 数据亮点
    card1_draw.text((30, y_pos+15), "屏幕可视角度：", font=font_small, fill=COLORS["text_gray"])
    card1_draw.text((200, y_pos+15), "明显收窄", font=font_small, fill=COLORS["highlight"])
    
    card1_draw.text((30, y_pos+50), "技术评价：", font=font_small, fill=COLORS["text_gray"])
    card1_draw.text((155, y_pos+50), "待优化", font=font_small, fill=COLORS["highlight"])
    
    # 来源
    card1_draw.text((30, y_pos+90), "来源: SamMobile | 2026-03-28", font=font_caption, fill=(148,163,184,180))
    
    img.paste(card1, (40, card1_y), card1)
    
    # === 新闻卡片2: 香港科技创新展 ===
    card2_y = card1_y + card1_height + 30
    card2_height = 380
    
    card2 = Image.new('RGBA', (width-80, card2_height), (255,255,255,15))
    card2_draw = ImageDraw.Draw(card2)
    
    # 左边强调条
    card2_draw.line([(0, 20), (0, card2_height-20)], fill=COLORS["accent_purple"], width=4)
    
    # 标签
    card2_draw.text((30, 25), "🤖 科技创新", font=font_caption, fill=COLORS["accent_purple"])
    
    # 标题
    card2_draw.text((30, 65), "香港InnoEX电子展", font=font_subtitle, fill=COLORS["text_white"])
    
    # 时间地点
    card2_draw.text((30, 115), "📅 2026年4月13-16日", font=font_small, fill=COLORS["accent_blue"])
    card2_draw.text((30, 150), "📍 香港会展中心", font=font_small, fill=COLORS["text_gray"])
    
    # 展会亮点
    highlights = [
        "• AI人工智能",
        "• 机器人技术（100+机器人）",
        "• 低空经济",
        "• 智能家居",
        "• 健康科技"
    ]
    y_pos = 195
    for line in highlights:
        card2_draw.text((30, y_pos), line, font=font_body, fill=COLORS["text_gray"])
        y_pos += 38
    
    # 重点数据
    card2_draw.text((30, y_pos+10), "展商数量:", font=font_small, fill=COLORS["text_gray"])
    card2_draw.text((140, y_pos+10), "全球数百家", font=font_small, fill=COLORS["highlight"])
    
    # 来源
    card2_draw.text((30, y_pos+50), "来源: iTnews | 2026-03-30", font=font_caption, fill=(148,163,184,180))
    
    img.paste(card2, (40, card2_y), card2)
    
    # === 底部总结区 ===
    summary_y = card2_y + card2_height + 30
    
    # 分隔线
    draw.line([(80, summary_y), (width-80, summary_y)], fill=(0,212,255,80), width=1)
    
    # 总结标题
    summary_title = "📊 本周要点"
    draw.text((80, summary_y+20), summary_title, font=font_body, fill=COLORS["accent_blue"])
    
    # 要点列表
    points = [
        "1. 三星S26 Ultra隐私保护功能引关注",
        "2. 香港电子展聚焦AI与机器人",
        "3. 智能设备隐私与便利平衡成焦点"
    ]
    y_pos = summary_y + 60
    for point in points:
        draw.text((80, y_pos), point, font=font_small, fill=COLORS["text_gray"])
        y_pos += 35
    
    # 底部信息
    footer_y = height - 80
    draw.line([(80, footer_y), (width-80, footer_y)], fill=(0,212,255,80), width=1)
    
    footer_text = "贾维斯AI信息图 | 数据来源：公开新闻"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=font_caption)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width)//2, footer_y+15), footer_text, font=font_caption, fill=(148,163,184,150))
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img = img.convert('RGB')
    img.save(OUTPUT_PATH, 'JPEG', quality=95)
    print(f"✅ 信息图已保存: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_infographic()
