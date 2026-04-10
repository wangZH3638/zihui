#!/usr/bin/env python3
"""信息图生成器 v3 - 融合MiniMax优雅设计"""

from PIL import Image, ImageDraw, ImageFont
import random
import os

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/news_card_v3.jpg"

# MiniMax风格配色
COLORS = {
    "bg_light": "#faf9f7",        # 柔和浅底
    "bg_gradient_end": "#f5f3f0", # 渐变结束
    "white": "#ffffff",
    "text_dark": "#2c3e50",       # 深色文字
    "text_gray": "#5d6d7e",        # 灰色文字
    "text_light": "#7f8c8d",       # 浅灰文字
    
    # 渐变强调色（蓝紫渐变）
    "gradient_start": "#667eea",  # 渐变起点
    "gradient_end": "#764ba2",    # 渐变终点
    
    # 卡片强调色
    "accent_blue": "#3498db",
    "accent_red": "#e74c3c",
    "accent_green": "#27ae60",
    "accent_orange": "#f0b860",
    "accent_gold": "#d4a574",
    
    # 边框
    "border_light": "#f0ebe3",
    "border_medium": "#e8e4dd",
}

def create_gradient_background(width, height):
    """创建柔和渐变背景"""
    img = Image.new('RGB', (width, height), COLORS["bg_light"])
    draw = ImageDraw.Draw(img)
    
    # 垂直渐变
    for y in range(height):
        ratio = y / height
        r = int(250 - ratio * 5)
        g = int(249 - ratio * 6)
        b = int(247 - ratio * 7)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return img

def add_decorative_elements(draw, width, height):
    """添加装饰性圆点和星星"""
    random.seed(42)
    
    # 圆点装饰
    for _ in range(20):
        x = random.randint(20, width - 20)
        y = random.randint(100, height - 100)
        r = random.randint(3, 6)
        alpha = random.randint(80, 150)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(220, 215, 205))
    
    # 星星装饰（简化五角星）
    star_positions = [(width-120, 80), (100, height-200), (width-80, height-300)]
    for sx, sy in star_positions:
        draw_star(draw, sx, sy, 12, COLORS["accent_gold"])

def draw_star(draw, cx, cy, size, color):
    """绘制简化五角星"""
    points = []
    for i in range(10):
        angle = (i * 36 - 90) * 3.14159 / 180
        r = size if i % 2 == 0 else size * 0.4
        points.append((cx + r, cy + r))  # 简化
    # 简化：用椭圆代替
    draw.ellipse([cx-size//2, cy-size//2, cx+size//2, cy+size//2], fill=color)

def draw_rounded_rect(draw, x1, y1, x2, y2, radius, fill, outline=None, width=3):
    """绘制圆角矩形"""
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    draw.ellipse([x1, y1, x1+radius*2, y1+radius*2], fill=fill)
    draw.ellipse([x2-radius*2, y1, x2, y1+radius*2], fill=fill)
    draw.ellipse([x1, y2-radius*2, x1+radius*2, y2], fill=fill)
    draw.ellipse([x2-radius*2, y2-radius*2, x2, y2], fill=fill)
    
    if outline:
        draw.line([(x1+radius, y1), (x2-radius, y1)], fill=outline, width=width)
        draw.line([(x1+radius, y2), (x2-radius, y2)], fill=outline, width=width)
        draw.line([(x1, y1+radius), (x1, y2-radius)], fill=outline, width=width)
        draw.line([(x2, y1+radius), (x2, y2-radius)], fill=outline, width=width)

def draw_gradient_text(draw, x, y, text, font, gradient_colors=None):
    """绘制渐变效果文字（通过叠加实现）"""
    if gradient_colors is None:
        gradient_colors = [COLORS["gradient_start"], COLORS["gradient_end"]]
    # 先绘制深色底层
    draw.text((x, y), text, font=font, fill=(100, 80, 130))
    # 再绘制主文字
    draw.text((x, y), text, font=font, fill=COLORS["gradient_start"])

def draw_icon_circle(draw, x, y, emoji, bg_gradient=False):
    """绘制emoji圆形图标"""
    size = 50
    # 圆形背景
    if bg_gradient:
        draw.ellipse([x, y, x+size, y+size], fill=COLORS["accent_blue"])
    else:
        draw.ellipse([x, y, x+size, y+size], fill=COLORS["border_light"])
    
    # 简单边框
    draw.ellipse([x, y, x+size, y+size], outline=COLORS["border_medium"], width=2)
    
    # 绘制emoji（用文字代替）
    try:
        emoji_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        emoji_font = ImageFont.load_default(size=24)
    
    # 计算emoji居中位置
    bbox = draw.textbbox((0, 0), emoji, font=emoji_font)
    ew = bbox[2] - bbox[0]
    eh = bbox[3] - bbox[1]
    draw.text((x + (size - ew)//2 - 2, y + (size - eh)//2 - 2), emoji, font=emoji_font, fill=(60, 60, 60))

def draw_check_badge(draw, x, y, color):
    """绘制圆形勾选徽章"""
    size = 22
    draw.ellipse([x, y, x+size, y+size], fill=color)
    draw.text((x+5, y+3), "✓", font=ImageFont.load_default(size=14), fill=COLORS["white"])

def draw_news_badge(draw, x, y, number, color):
    """绘制数字角标"""
    size = 28
    draw.ellipse([x, y, x+size, y+size], fill=color)
    draw.text((x+7, y+5), str(number), font=ImageFont.load_default(size=14), fill=COLORS["white"])

def create_infographic():
    width, height = 1080, 1440
    margin = 40
    content_w = width - margin * 2
    
    # 创建背景
    img = create_gradient_background(width, height)
    draw = ImageDraw.Draw(img)
    
    # 添加装饰
    add_decorative_elements(draw, width, height)
    
    # 字体
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        font_title = ImageFont.load_default()
        font_header = font_title
        font_subtitle = font_title
        font_body = font_title
        font_small = font_title
        font_caption = font_title
    
    # === 标题区域 ===
    header_y = 30
    
    # 主标题
    draw.text((margin, header_y), "📰 今日科技要闻", font=font_title, fill=COLORS["text_dark"])
    
    # 标题下划线装饰
    line_width = 180
    line_x = margin + 60
    draw.line([(line_x, header_y + 48), (line_x + line_width, header_y + 48)], 
              fill=COLORS["accent_orange"], width=4)
    
    # 日期和副标题
    draw.text((margin, header_y + 65), "2026年4月3日 · 星期五", font=font_small, fill=COLORS["text_gray"])
    draw.text((margin, header_y + 90), "聚焦全球科技创新动态", font=font_caption, fill=COLORS["text_light"])
    
    # 技术标签
    tech_tag_y = header_y + 120
    draw_rounded_rect(draw, margin, tech_tag_y, margin + 220, tech_tag_y + 32, 16, 
                     fill=(100, 100, 180))
    draw.text((margin + 15, tech_tag_y + 7), "🤖 AI · 航天 · 芯片", font=font_caption, fill=COLORS["white"])
    
    # === 对比卡片区域 ===
    card_y = header_y + 175
    card_h = 200
    card_w = (content_w - 20) // 2
    
    # 左侧卡片 - 太空算力
    left_card_x = margin
    draw_rounded_rect(draw, left_card_x, card_y, left_card_x + card_w, card_y + card_h, 12,
                     COLORS["white"], COLORS["border_light"], 2)
    # 左侧色条
    draw.rectangle([left_card_x, card_y + 10, left_card_x + 4, card_y + card_h - 10], fill=COLORS["accent_blue"])
    
    # 左侧图标
    draw_icon_circle(draw, left_card_x + 20, card_y + 20, "🚀", bg_gradient=True)
    
    # 左侧标题
    draw.text((left_card_x + 85, card_y + 25), "太空算力产业大会", font=font_subtitle, fill=COLORS["text_dark"])
    draw_rounded_rect(draw, left_card_x + 85, card_y + 55, left_card_x + 145, card_y + 75, 8, 
                     fill=(220, 235, 250))
    draw.text((left_card_x + 92, card_y + 58), "航天科技", font=font_caption, fill=(25, 118, 210))
    
    # 左侧内容
    content_y = card_y + 90
    draw.text((left_card_x + 20, content_y), "大会在北京经开区开幕", font=font_body, fill=COLORS["text_gray"])
    
    points_left = [
        "太空数据中心与地面算力协同",
        "卫星互联网与AI融合发展",
        "天地一体化算力网络"
    ]
    py = content_y + 25
    for pt in points_left:
        draw_check_badge(draw, left_card_x + 20, py, COLORS["accent_blue"])
        draw.text((left_card_x + 50, py + 3), pt, font=font_small, fill=COLORS["text_gray"])
        py += 26
    
    # 右侧卡片 - 美国重返月球
    right_card_x = margin + card_w + 20
    draw_rounded_rect(draw, right_card_x, card_y, right_card_x + card_w, card_y + card_h, 12,
                     COLORS["white"], COLORS["border_light"], 2)
    # 右侧色条
    draw.rectangle([right_card_x, card_y + 10, right_card_x + 4, card_y + card_h - 10], fill=COLORS["accent_red"])
    
    # 右侧图标
    draw_icon_circle(draw, right_card_x + 20, card_y + 20, "🌙", bg_gradient=True)
    
    # 右侧标题
    draw.text((right_card_x + 85, card_y + 25), "美国重返月球", font=font_subtitle, fill=COLORS["text_dark"])
    draw_rounded_rect(draw, right_card_x + 85, card_y + 55, right_card_x + 145, card_y + 75, 8, 
                     fill=(255, 235, 235))
    draw.text((right_card_x + 92, card_y + 58), "航天历史", font=font_caption, fill=(198, 40, 40))
    
    # 右侧内容
    draw.text((right_card_x + 20, content_y), "阿耳忒弥斯2号成功升空", font=font_body, fill=COLORS["text_gray"])
    
    points_right = [
        "50多年来首次载人绕月飞行",
        "为2027年载人登月奠定基础",
        "月球南极探索与资源勘探"
    ]
    py = content_y + 25
    for pt in points_right:
        draw_check_badge(draw, right_card_x + 20, py, COLORS["accent_red"])
        draw.text((right_card_x + 50, py + 3), pt, font=font_small, fill=COLORS["text_gray"])
        py += 26
    
    # === 数据亮点区域 ===
    data_y = card_y + card_h + 30
    data_h = 140
    
    draw_rounded_rect(draw, margin, data_y, width - margin, data_y + data_h, 12,
                     COLORS["white"], COLORS["border_light"], 2)
    
    # 标题
    data_title = "📊 今日数据亮点"
    dt_bbox = draw.textbbox((0, 0), data_title, font=font_header)
    dt_width = dt_bbox[2] - dt_bbox[0]
    draw.text(((width - dt_width)//2, data_y + 15), data_title, font=font_header, fill=COLORS["text_dark"])
    
    # 数据网格
    data_items = [
        ("460万+", "A股3月新开户", "环比+82%"),
        ("1300亿", "国家电网Q1投资", "同比+37%"),
        ("+500元", "安卓手机涨价", "存储成本高位"),
        ("12家", "数字人民币新增", "运营机构扩容"),
    ]
    
    item_w = (content_w - 30) // 4
    item_y = data_y + 55
    
    for i, (num, label, desc) in enumerate(data_items):
        ix = margin + 10 + i * (item_w + 10)
        
        # 数据卡片
        draw_rounded_rect(draw, ix, item_y, ix + item_w, item_y + 70, 8,
                        COLORS["bg_light"], COLORS["border_light"], 1)
        
        # 数字（用蓝色）
        num_font = ImageFont.load_default(size=26)
        draw.text((ix + 10, item_y + 8), num, font=num_font, fill=COLORS["gradient_start"])
        
        # 标签
        draw.text((ix + 10, item_y + 38), label, font=font_caption, fill=COLORS["text_dark"])
        
        # 描述
        draw.text((ix + 10, item_y + 54), desc, font=font_caption, fill=COLORS["text_light"])
    
    # === 热点新闻网格 ===
    news_y = data_y + data_h + 30
    news_h = 300
    
    # 标题
    news_title = "🔥 科技热点速递"
    nt_bbox = draw.textbbox((0, 0), news_title, font=font_header)
    nt_width = nt_bbox[2] - nt_bbox[0]
    draw.text(((width - nt_width)//2, news_y), news_title, font=font_header, fill=COLORS["text_dark"])
    
    # 新闻网格 (3列2行)
    news_items = [
        ("🔬", "量子点显示技术突破", "福州大学团队研发AR/VR超高分辨率量子点显示技术，论文发表于《自然》杂志"),
        ("🤖", "强人工智能临近", "Anthropic报告称'强人工智能'或在2026年下半年至2027年成为现实"),
        ("🏥", "AI医疗联合实验室", "蚂蚁健康与上海交大共建AI4Healthcare联合实验室，聚焦医疗专科智能体"),
        ("🔋", "移动电源安全国标", "首部移动电源安全国标出台，电芯须通过针刺测试不起火不爆炸"),
        ("📱", "微信初代测试机", "微信开发首版测试用苹果iPod touch曝光，将捐赠给计算机博物馆"),
        ("🚗", "3月汽车销量飘红", "比亚迪30万辆、奇瑞24万辆、吉利23.3万辆领跑新能源市场"),
    ]
    
    grid_y = news_y + 40
    col_w = (content_w - 20) // 3
    row_h = 115
    
    for idx, (icon, title, desc) in enumerate(news_items):
        col = idx % 3
        row = idx // 3
        
        nx = margin + col * (col_w + 10)
        ny = grid_y + row * (row_h + 10)
        
        # 新闻卡片
        draw_rounded_rect(draw, nx, ny, nx + col_w, ny + row_h, 10,
                         COLORS["white"], COLORS["border_light"], 2)
        
        # 数字角标
        draw_news_badge(draw, nx + col_w - 35, ny - 10, idx + 1, COLORS["accent_orange"])
        
        # emoji图标
        try:
            icon_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            icon_font = ImageFont.load_default()
        draw.text((nx + 12, ny + 12), icon, font=icon_font, fill=(60, 60, 60))
        
        # 标题
        draw.text((nx + 12, ny + 42), title, font=font_small, fill=COLORS["text_dark"])
        
        # 描述
        draw.text((nx + 12, ny + 65), desc[:25] + "..." if len(desc) > 25 else desc, 
                 font=font_caption, fill=COLORS["text_light"])
    
    # === 底部信息 ===
    footer_y = grid_y + row_h * 2 + 40
    
    # 分隔线
    draw.line([(margin, footer_y), (width - margin, footer_y)], 
              fill=COLORS["border_medium"], width=2)
    
    # 底部文字
    draw.text((margin, footer_y + 15), "📡 科技要闻，每日更新", font=font_body, fill=COLORS["text_gray"])
    
    source = "数据来源：东方财富、36氪、IT之家、新浪科技等 · 2026.04.03"
    source_bbox = draw.textbbox((0, 0), source, font=font_caption)
    source_width = source_bbox[2] - source_bbox[0]
    draw.text(((width - source_width)//2, footer_y + 40), source, font=font_caption, fill=COLORS["text_light"])
    
    # 角落装饰
    draw.polygon([(margin, 15), (margin+30, 15), (margin, 45)], fill=COLORS["accent_gold"])
    draw.polygon([(width-margin, 15), (width-margin-30, 15), (width-margin, 45)], fill=COLORS["accent_gold"])
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img = img.convert('RGB')
    img.save(OUTPUT_PATH, 'JPEG', quality=95)
    print(f"✅ 已保存: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_infographic()
