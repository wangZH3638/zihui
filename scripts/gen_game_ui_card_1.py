#!/usr/bin/env python3
"""游戏技能面板风格信息图 - 复古游戏UI"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/game_ui_card.jpg"

# 暖黄做旧 + 深蓝/深绿配色
COLORS = {
    "bg_cream": "#F5E6C8",        # 暖黄做旧底色
    "bg_aged": "#EDD9A3",         # 做旧黄
    "title_blue": "#2D4A6F",      # 深蓝标题栏
    "title_green": "#2D5A4A",     # 深绿标题栏  
    "accent_blue": "#4A7AB0",     # 亮蓝强调
    "accent_green": "#4A9A7A",   # 亮绿强调
    "text_dark": "#3D3D3D",       # 深色文字
    "text_brown": "#5A4A3A",      # 棕色文字
    "text_white": "#FFFFFF",      # 白色文字
    "border": "#8B7355",          # 边框棕色
    "border_dark": "#6B5344",     # 深棕边框
    "highlight": "#C4956A",       # 高亮暖色
    "icon_gold": "#B8963E",       # 金色图标
    "success": "#5A8A5A",         # 成功绿
    "warning": "#B8864A",         # 警告橙
    "card_bg": "#FAF3E3",         # 卡片背景
    "shadow": "#D4C4A8",          # 阴影色
}

def create_aged_paper_bg(width, height):
    """创建做旧纸张背景"""
    img = Image.new('RGB', (width, height), COLORS["bg_cream"])
    draw = ImageDraw.Draw(img)
    
    # 轻微的纹理效果
    import random
    random.seed(42)
    for _ in range(500):
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(1, 3)
        alpha = random.randint(10, 30)
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(180, 165, 140, alpha))
    
    return img

def draw_rounded_rect(draw, x1, y1, x2, y2, radius, fill, outline=None, width=3):
    """绘制圆角矩形"""
    # 主体
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    draw.ellipse([x1, y1, x1+radius*2, y1+radius*2], fill=fill)
    draw.ellipse([x2-radius*2, y1, x2, y1+radius*2], fill=fill)
    draw.ellipse([x1, y2-radius*2, x1+radius*2, y2], fill=fill)
    draw.ellipse([x2-radius*2, y2-radius*2, x2, y2], fill=fill)
    
    # 边框
    if outline:
        # 上边
        draw.line([(x1+radius, y1), (x2-radius, y1)], fill=outline, width=width)
        # 下边
        draw.line([(x1+radius, y2), (x2-radius, y2)], fill=outline, width=width)
        # 左边
        draw.line([(x1, y1+radius), (x1, y2-radius)], fill=outline, width=width)
        # 右边
        draw.line([(x2, y1+radius), (x2, y2-radius)], fill=outline, width=width)
        # 四角弧形
        draw.arc([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=outline, width=width)
        draw.arc([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=outline, width=width)

def draw_game_icon(draw, x, y, icon_type, size=32):
    """绘制游戏风格图标"""
    cx, cy = x + size//2, y + size//2
    
    if icon_type == "check":
        # 对勾图标
        draw.ellipse([x, y, x+size, y+size], fill=COLORS["success"])
        draw.line([(x+8, cy), (x+14, cy+8), (x+24, cy-8)], fill=(255,255,255), width=4)
    elif icon_type == "gear":
        # 齿轮图标
        draw.ellipse([x+4, y+4, x+size-4, y+size-4], fill=COLORS["icon_gold"], outline=COLORS["border_dark"], width=2)
        for i in range(8):
            angle = i * 45 * 3.14159 / 180
            rx = cx + 12 * (1 if i % 2 == 0 else 0.7) * (1 if i < 4 else -1) * abs(1 if i < 2 or i > 5 else -1 if 2 <= i < 4 or i > 6 else 0)
            # 简化齿轮
        draw.ellipse([x+10, y+10, x+size-10, y+size-10], fill=COLORS["bg_cream"])
    elif icon_type == "clock":
        # 时钟图标
        draw.ellipse([x, y, x+size, y+size], fill=COLORS["accent_blue"], outline=COLORS["border_dark"], width=2)
        draw.line([(cx, cy), (cx, y+8)], fill=(255,255,255), width=3)
        draw.line([(cx, cy), (cx+8, cy)], fill=(255,255,255), width=3)
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(255,255,255))
    elif icon_type == "arrow":
        # 箭头图标
        draw.polygon([(x, cy-6), (x+size-10, cy-6), (x+size-10, y), 
                     (x+size, cy), (x+size-10, y+size), (x+size-10, cy+6)], 
                     fill=COLORS["accent_green"], outline=COLORS["border_dark"], width=2)
    elif icon_type == "star":
        # 星星图标
        points = []
        for i in range(10):
            angle = (i * 36 - 90) * 3.14159 / 180
            r = size//2 if i % 2 == 0 else size//4
            points.append((cx + r * (1 if i < 5 else -1) * abs(1 if i < 3 or i > 7 else -1 if 3 <= i < 5 or i > 7 else 0) + r * (1 if i % 2 == 0 else 0.4) * (1 if i < 5 else -1) if True else cx, 
                         cy + r * (1 if i < 5 else -1) * abs(1 if i < 3 or i > 7 else -1 if 3 <= i < 5 or i > 7 else 0)))
        # 简化五角星
        star_pts = [(cx, y), (cx+8, cy-4), (cx+size, y+8), (cx+6, cy+8), (cx+4, cy+size)]
        draw.polygon(star_pts, fill=COLORS["icon_gold"], outline=COLORS["border_dark"])
    elif icon_type == "book":
        # 书本图标
        draw.rectangle([x+2, y+4, x+size-2, y+size-4], fill=COLORS["accent_blue"], outline=COLORS["border_dark"], width=2)
        draw.line([(cx, y+4), (cx, y+size-4)], fill=COLORS["border_dark"], width=2)
    elif icon_type == "lightbulb":
        # 灯泡图标
        draw.ellipse([x+4, y+2, x+size-4, y+size-8], fill=COLORS["icon_gold"])
        draw.rectangle([x+10, y+size-10, x+size-10, y+size-4], fill=COLORS["border_dark"])
        draw.line([(x+8, y+size-8), (x+size-8, y+size-8)], fill=COLORS["border_dark"], width=2)
    elif icon_type == "chat":
        # 对话框图标
        draw_rounded_rect(draw, x, y+2, x+size, y+size-2, 6, COLORS["card_bg"], COLORS["border_dark"], 2)
        draw.polygon([(x+6, y+size-2), (x+16, y+size-2), (x+6, y+size+6)], fill=COLORS["card_bg"], outline=COLORS["border_dark"], width=2)
        draw.line([(x+8, y+12), (x+size-8, y+12)], fill=COLORS["text_dark"], width=2)
        draw.line([(x+8, y+20), (x+size-16, y+20)], fill=COLORS["text_dark"], width=2)

def draw_progress_bar(draw, x, y, w, h, fill_ratio, fill_color, label=""):
    """绘制进度条"""
    # 背景槽
    draw_rounded_rect(draw, x, y, x+w, y+h, 6, COLORS["shadow"], COLORS["border_dark"], 2)
    # 填充
    if fill_ratio > 0:
        fill_w = int((w - 4) * fill_ratio)
        if fill_w > 0:
            draw_rounded_rect(draw, x+2, y+2, x+2+fill_w, y+h-2, 4, fill_color)
    # 标签
    if label:
        draw.text((x + w//2 - 30, y + h + 4), label, font=ImageFont.load_default(size=16), fill=COLORS["text_brown"])

def draw_info_panel(draw, x, y, w, h, title, title_color, content_func=None):
    """绘制信息面板"""
    # 标题栏
    draw_rounded_rect(draw, x, y, x+w, y+45, 8, title_color, COLORS["border_dark"], 3)
    draw.text((x+15, y+12), title, font=ImageFont.load_default(size=24), fill=(255,255,255))
    
    # 内容区
    draw_rounded_rect(draw, x, y+45, x+w, y+h, 8, COLORS["card_bg"], COLORS["border_dark"], 3)
    
    if content_func:
        content_func(draw, x, y)

def draw_divider(draw, x1, y, x2, line_count=3):
    """绘制分隔线（手绘风格）"""
    for i, offset in enumerate([-2, 0, 2]):
        draw.line([(x1, y+offset), (x2, y+offset)], fill=COLORS["border"], width=1)

def create_infographic():
    width, height = 1080, 1440
    
    # 创建做旧背景
    img = create_aged_paper_bg(width, height)
    draw = ImageDraw.Draw(img)
    
    # 字体
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_title = ImageFont.load_default(size=36)
        font_header = ImageFont.load_default(size=28)
        font_body = ImageFont.load_default(size=22)
        font_small = ImageFont.load_default(size=18)
        font_caption = ImageFont.load_default(size=16)
    
    margin = 40
    content_w = width - margin * 2
    
    # === 顶部主面板 ===
    panel_y = 30
    panel_h = 130
    
    # 主面板背景
    draw_rounded_rect(draw, margin, panel_y, width-margin, panel_y+panel_h, 12, 
                     COLORS["title_blue"], COLORS["border_dark"], 4)
    
    # 面板标题
    draw.text((margin + 20, panel_y + 20), "📜 今日要闻", font=font_title, fill=(255,255,255))
    
    # 副标题装饰线
    draw.line([(margin+20, panel_y+65), (width-margin-20, panel_y+65)], 
             fill=(255,255,255,80), width=2)
    
    # 日期显示
    draw.text((margin+20, panel_y+80), "2026年4月3日  科技资讯", font=font_small, fill=(220,220,200))
    
    # 角落装饰
    draw.text((width-margin-120, panel_y+80), "NEWS ◆", font=font_small, fill=(200,200,180))
    
    # === 主要信息卡片1 - AI芯片进展 ===
    card1_y = panel_y + panel_h + 25
    card1_h = 260
    
    # 卡片背景
    draw_rounded_rect(draw, margin, card1_y, width-margin, card1_y+card1_h, 10,
                     COLORS["card_bg"], COLORS["border"], 3)
    
    # 左侧标题栏
    draw_rounded_rect(draw, margin, card1_y, margin+180, card1_y+card1_h, 10,
                     COLORS["title_green"], COLORS["border_dark"], 3)
    draw.text((margin+15, card1_y+20), "主题", font=font_header, fill=(255,255,255))
    draw.text((margin+15, card1_y+55), "AI", font=font_title, fill=(255,255,255))
    draw.text((margin+15, card1_y+95), "芯片", font=font_title, fill=(255,255,255))
    
    # 右侧内容
    content_x = margin + 200
    content_y = card1_y + 25
    line_h = 32
    
    # 图标 + 文字
    draw_game_icon(draw, content_x, content_y, "star")
    draw.text((content_x+45, content_y+5), "新一代AI芯片发布", font=font_body, fill=COLORS["text_dark"])
    
    draw_game_icon(draw, content_x, content_y+line_h, "check")
    draw.text((content_x+45, content_y+line_h+5), "处理速度提升 300%", font=font_body, fill=COLORS["text_dark"])
    
    draw_game_icon(draw, content_x, content_y+line_h*2, "check")
    draw.text((content_x+45, content_y+line_h*2+5), "功耗降低 50%", font=font_body, fill=COLORS["text_dark"])
    
    draw_game_icon(draw, content_x, content_y+line_h*3, "gear")
    draw.text((content_x+45, content_y+line_h*3+5), "适用于下一代智能设备", font=font_small, fill=COLORS["text_brown"])
    
    # 进度条
    bar_y = content_y + line_h*4 + 10
    draw_progress_bar(draw, content_x, bar_y, content_w - 220, 18, 0.85, COLORS["success"], "性能评分")
    
    # === 主要信息卡片2 - 隐私保护 ===
    card2_y = card1_y + card1_h + 20
    card2_h = 220
    
    draw_rounded_rect(draw, margin, card2_y, width-margin, card2_y+card2_h, 10,
                     COLORS["card_bg"], COLORS["border"], 3)
    
    # 左侧标题栏
    draw_rounded_rect(draw, margin, card2_y, margin+180, card2_y+card2_h, 10,
                     COLORS["title_blue"], COLORS["border_dark"], 3)
    draw.text((margin+15, card2_y+20), "主题", font=font_header, fill=(255,255,255))
    draw.text((margin+15, card2_y+55), "隐私", font=font_title, fill=(255,255,255))
    draw.text((margin+15, card2_y+95), "保护", font=font_title, fill=(255,255,255))
    
    # 右侧内容
    content_x = margin + 200
    content_y = card2_y + 25
    
    draw_game_icon(draw, content_x, content_y, "chat")
    draw.text((content_x+45, content_y+5), "智能设备隐私功能升级", font=font_body, fill=COLORS["text_dark"])
    
    draw_game_icon(draw, content_x, content_y+line_h, "check")
    draw.text((content_x+45, content_y+line_h+5), "新一代加密技术采用", font=font_body, fill=COLORS["text_dark"])
    
    draw_game_icon(draw, content_x, content_y+line_h*2, "clock")
    draw.text((content_x+45, content_y+line_h*2+5), "安全响应速度提升 40%", font=font_body, fill=COLORS["text_dark"])
    
    draw_game_icon(draw, content_x, content_y+line_h*3, "arrow")
    draw.text((content_x+45, content_y+line_h*3+5), "预计年内大规模应用 →", font=font_small, fill=COLORS["accent_green"])
    
    # === 流程图区域 - 三步流程 ===
    flow_y = card2_y + card2_h + 25
    flow_h = 160
    
    # 背景
    draw_rounded_rect(draw, margin, flow_y, width-margin, flow_y+flow_h, 10,
                     COLORS["bg_aged"], COLORS["border"], 3)
    
    # 标题
    draw.text((margin+15, flow_y+12), "📋 发展路径", font=font_header, fill=COLORS["text_dark"])
    
    draw_divider(draw, margin+15, flow_y+50, width-margin-15)
    
    # 三个步骤
    step_w = (content_w - 60) // 3
    step_y = flow_y + 70
    
    steps = [
        ("STEP 1", "技术研发", "AI芯片迭代", COLORS["title_green"]),
        ("STEP 2", "产品落地", "设备搭载", COLORS["title_blue"]),
        ("STEP 3", "市场推广", "普及应用", COLORS["icon_gold"]),
    ]
    
    for i, (step, title, desc, color) in enumerate(steps):
        sx = margin + 15 + i * (step_w + 20)
        
        # 步骤框
        draw_rounded_rect(draw, sx, step_y, sx+step_w, step_y+75, 8, COLORS["card_bg"], color, 3)
        
        # 步骤标签
        draw_rounded_rect(draw, sx+5, step_y+5, sx+90, step_y+30, 5, color, color, 0)
        draw.text((sx+12, step_y+10), step, font=font_caption, fill=(255,255,255))
        
        # 标题
        draw.text((sx+10, step_y+38), title, font=font_small, fill=COLORS["text_dark"])
        draw.text((sx+10, step_y+55), desc, font=font_caption, fill=COLORS["text_brown"])
        
        # 箭头
        if i < 2:
            arrow_x = sx + step_w + 3
            arrow_y = step_y + 30
            draw.polygon([(arrow_x, arrow_y-8), (arrow_x+14, arrow_y), (arrow_x, arrow_y+8)], 
                        fill=COLORS["border"], outline=COLORS["border_dark"])
    
    # === 底部总结面板 ===
    summary_y = flow_y + flow_h + 25
    summary_h = 180
    
    draw_rounded_rect(draw, margin, summary_y, width-margin, summary_y+summary_h, 10,
                     COLORS["title_blue"], COLORS["border_dark"], 4)
    
    # 标题
    draw.text((margin+20, summary_y+15), "💡 核心要点", font=font_header, fill=(255,255,255))
    draw.line([(margin+20, summary_y+50), (width-margin-20, summary_y+50)], 
             fill=(255,255,255,60), width=2)
    
    # 要点列表
    points = [
        ("✓", "AI技术持续发展，重塑产业格局"),
        ("✓", "隐私保护成为智能设备核心竞争力"),
        ("✓", "技术落地改变日常生活方式"),
    ]
    
    py = summary_y + 65
    for check, text in points:
        draw.text((margin+25, py), check, font=font_body, fill=COLORS["icon_gold"])
        draw.text((margin+55, py+2), text, font=font_body, fill=(255,255,255))
        py += 35
    
    # === 底部规则栏 ===
    footer_y = height - 70
    
    draw_rounded_rect(draw, margin, footer_y, width-margin, height-15, 8,
                     COLORS["bg_aged"], COLORS["border"], 3)
    
    footer_text = "数据来源：公开新闻报道  |  生成时间：2026-04-03  |  贾维斯信息图"
    fw = draw.textbbox((0, 0), footer_text, font=font_caption)
    tw = fw[2] - fw[0]
    draw.text(((width - tw)//2, footer_y + 20), footer_text, font=font_caption, fill=COLORS["text_brown"])
    
    # === 角落装饰 ===
    # 左上角
    draw.polygon([(margin, 15), (margin+30, 15), (margin, 45)], fill=COLORS["icon_gold"])
    # 右上角
    draw.polygon([(width-margin, 15), (width-margin-30, 15), (width-margin, 45)], fill=COLORS["icon_gold"])
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img = img.convert('RGB')
    img.save(OUTPUT_PATH, 'JPEG', quality=95)
    print(f"✅ 游戏技能面板风格信息图已保存: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_infographic()
