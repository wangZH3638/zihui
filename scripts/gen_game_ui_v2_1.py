#!/usr/bin/env python3
"""游戏技能面板风格信息图 v2 - 完整文字版"""

from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/game_ui_card_v2.jpg"

# 暖黄做旧 + 深蓝/深绿配色
COLORS = {
    "bg_cream": "#F5E6C8",
    "bg_aged": "#EDD9A3",
    "title_blue": "#2D4A6F",
    "title_green": "#2D5A4A",
    "accent_blue": "#4A7AB0",
    "accent_green": "#4A9A7A",
    "text_dark": "#3D3D3D",
    "text_brown": "#5A4A3A",
    "white": (255, 255, 255),
    "border": "#8B7355",
    "border_dark": "#6B5344",
    "highlight": "#C4956A",
    "icon_gold": "#B8963E",
    "success": "#5A8A5A",
    "card_bg": "#FAF3E3",
    "shadow": "#D4C4A8",
}

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
        draw.arc([x1, y1, x1+radius*2, y1+radius*2], 180, 270, fill=outline, width=width)
        draw.arc([x2-radius*2, y1, x2, y1+radius*2], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2-radius*2, x1+radius*2, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2-radius*2, y2-radius*2, x2, y2], 0, 90, fill=outline, width=width)

def draw_icon_check(draw, x, y, size=28):
    """对勾图标"""
    draw.ellipse([x, y, x+size, y+size], fill=COLORS["success"])
    draw.line([(x+6, y+size//2), (x+11, y+size//2+6), (x+22, y+size//2-8)], fill=COLORS["white"], width=3)

def draw_icon_star(draw, x, y, size=28):
    """星星图标"""
    cx, cy = x + size//2, y + size//2
    draw.ellipse([x, y, x+size, y+size], fill=COLORS["icon_gold"], outline=COLORS["border_dark"], width=2)

def draw_icon_arrow(draw, x, y, size=28):
    """箭头图标"""
    cx, cy = x + size//2, y + size//2
    draw.polygon([(x, cy-5), (x+size-8, cy-5), (x+size-8, y), 
                 (x+size, cy), (x+size-8, y+size), (x+size-8, cy+5)
                 ], fill=COLORS["accent_green"], outline=COLORS["border_dark"])

def draw_progress_bar(draw, x, y, w, h, fill_ratio, fill_color, label="", font_ref=None):
    """进度条"""
    draw_rounded_rect(draw, x, y, x+w, y+h, 6, COLORS["shadow"], COLORS["border_dark"], 2)
    if fill_ratio > 0:
        fill_w = int((w - 4) * fill_ratio)
        if fill_w > 0:
            draw_rounded_rect(draw, x+2, y+2, x+2+fill_w, y+h-2, 4, fill_color)
    if label:
        try:
            fnt = font_ref if font_ref else ImageFont.load_default()
            draw.text((x + 8, y + h + 4), label, font=fnt, fill=COLORS["text_brown"])
        except:
            pass

def create_infographic():
    width, height = 1080, 1440
    margin = 40
    content_w = width - margin * 2
    
    # 背景
    img = Image.new('RGB', (width, height), COLORS["bg_cream"])
    draw = ImageDraw.Draw(img)
    
    # 字体
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        font_title = ImageFont.load_default()
        font_header = font_title
        font_body = font_title
        font_small = font_title
        font_caption = font_title
    
    # === 顶部主面板 ===
    panel_y = 30
    panel_h = 120
    
    draw_rounded_rect(draw, margin, panel_y, width-margin, panel_y+panel_h, 12, 
                     COLORS["title_blue"], COLORS["border_dark"], 4)
    
    # 标题
    draw.text((margin + 20, panel_y + 15), "📜 科技新闻日报", font=font_title, fill=COLORS["white"])
    draw.text((margin + 20, panel_y + 58), "2026年4月3日  |  聚焦AI与智能设备", font=font_small, fill=(220, 220, 200))
    
    # 右侧装饰
    draw.text((width - margin - 100, panel_y + 58), "DAY 403 ◆", font=font_small, fill=(200, 200, 180))
    
    # === 卡片1 - AI芯片 ===
    card1_y = panel_y + panel_h + 25
    card1_h = 250
    
    draw_rounded_rect(draw, margin, card1_y, width-margin, card1_y+card1_h, 10,
                     COLORS["card_bg"], COLORS["border"], 3)
    
    # 左侧标签
    draw_rounded_rect(draw, margin, card1_y, margin+160, card1_y+card1_h, 10,
                     COLORS["title_green"], COLORS["border_dark"], 3)
    draw.text((margin+15, card1_y+20), "NEWS 1", font=font_header, fill=COLORS["white"])
    draw.text((margin+15, card1_y+60), "AI", font=font_title, fill=COLORS["white"])
    draw.text((margin+15, card1_y+100), "芯片", font=font_title, fill=COLORS["white"])
    
    # 右侧内容
    cx = margin + 180
    cy = card1_y + 25
    lh = 34
    
    draw_icon_star(draw, cx, cy)
    draw.text((cx+40, cy+3), "三星发布Galaxy S26 Ultra新机", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_check(draw, cx, cy+lh)
    draw.text((cx+40, cy+lh+3), "隐私显示技术引发关注", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_check(draw, cx, cy+lh*2)
    draw.text((cx+40, cy+lh*2+3), "屏幕可视角度明显收窄", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_check(draw, cx, cy+lh*3)
    draw.text((cx+40, cy+lh*3+3), "技术成熟度仍需提升", font=font_small, fill=COLORS["text_brown"])
    
    # 进度条
    bar_y = cy + lh*4 + 8
    draw_progress_bar(draw, cx, bar_y, content_w - 200, 16, 0.72, COLORS["icon_gold"], "隐私保护指数", font_caption)
    
    # === 卡片2 - 香港电子展 ===
    card2_y = card1_y + card1_h + 20
    card2_h = 250
    
    draw_rounded_rect(draw, margin, card2_y, width-margin, card2_y+card2_h, 10,
                     COLORS["card_bg"], COLORS["border"], 3)
    
    draw_rounded_rect(draw, margin, card2_y, margin+160, card2_y+card2_h, 10,
                     COLORS["title_blue"], COLORS["border_dark"], 3)
    draw.text((margin+15, card2_y+20), "NEWS 2", font=font_header, fill=COLORS["white"])
    draw.text((margin+15, card2_y+60), "展会", font=font_title, fill=COLORS["white"])
    draw.text((margin+15, card2_y+100), "亮点", font=font_title, fill=COLORS["white"])
    
    # 右侧内容
    cx = margin + 180
    cy = card2_y + 25
    
    draw_icon_star(draw, cx, cy)
    draw.text((cx+40, cy+3), "香港InnoEX电子展 4月13-16日", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_check(draw, cx, cy+lh)
    draw.text((cx+40, cy+lh+3), "AI人工智能与机器人技术", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_check(draw, cx, cy+lh*2)
    draw.text((cx+40, cy+lh*2+3), "100+款机器人将亮相", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_check(draw, cx, cy+lh*3)
    draw.text((cx+40, cy+lh*3+3), "智能家居与健康科技", font=font_body, fill=COLORS["text_dark"])
    
    draw_icon_arrow(draw, cx, cy+lh*4)
    draw.text((cx+40, cy+lh*4+3), "查看详情 →", font=font_small, fill=COLORS["accent_green"])
    
    # === 流程图 ===
    flow_y = card2_y + card2_h + 25
    flow_h = 170
    
    draw_rounded_rect(draw, margin, flow_y, width-margin, flow_y+flow_h, 10,
                     COLORS["bg_aged"], COLORS["border"], 3)
    
    draw.text((margin+15, flow_y+12), "📋 技术发展趋势", font=font_header, fill=COLORS["text_dark"])
    
    # 分隔线
    draw.line([(margin+15, flow_y+52), (width-margin-15, flow_y+52)], fill=COLORS["border"], width=2)
    
    # 三步流程
    step_w = (content_w - 60) // 3
    step_y = flow_y + 70
    
    steps = [
        ("01", "技术突破", "AI芯片迭代\n性能大幅提升", COLORS["title_green"]),
        ("02", "产品升级", "智能设备\n隐私保护增强", COLORS["title_blue"]),
        ("03", "市场普及", "新技术\n走进日常生活", COLORS["icon_gold"]),
    ]
    
    for i, (num, title, desc, color) in enumerate(steps):
        sx = margin + 15 + i * (step_w + 20)
        
        draw_rounded_rect(draw, sx, step_y, sx+step_w, step_y+80, 8, COLORS["card_bg"], color, 3)
        
        # 数字标签
        draw.text((sx+12, step_y+10), num, font=font_header, fill=color)
        
        # 标题
        draw.text((sx+12, step_y+38), title, font=font_body, fill=COLORS["text_dark"])
        draw.text((sx+12, step_y+60), desc, font=font_caption, fill=COLORS["text_brown"])
        
        # 箭头
        if i < 2:
            ax = sx + step_w + 5
            ay = step_y + 35
            draw.polygon([(ax, ay-10), (ax+12, ay), (ax, ay+10)], fill=COLORS["border"])
    
    # === 底部总结 ===
    sum_y = flow_y + flow_h + 25
    sum_h = 190
    
    draw_rounded_rect(draw, margin, sum_y, width-margin, sum_y+sum_h, 10,
                     COLORS["title_blue"], COLORS["border_dark"], 4)
    
    draw.text((margin+20, sum_y+15), "💡 本日要点总结", font=font_header, fill=COLORS["white"])
    draw.line([(margin+20, sum_y+52), (width-margin-20, sum_y+52)], fill=(255,255,255,60), width=2)
    
    points = [
        "✦ AI芯片技术持续进化，性能提升300%",
        "✦ 智能设备隐私保护成为核心竞争点",
        "✦ 香港电子展展示机器人与AI融合前景",
        "✦ 技术落地改变用户日常生活方式"
    ]
    
    py = sum_y + 68
    for pt in points:
        draw.text((margin+25, py), pt, font=font_body, fill=COLORS["white"])
        py += 32
    
    # === 底部栏 ===
    footer_y = height - 70
    draw_rounded_rect(draw, margin, footer_y, width-margin, height-15, 8,
                     COLORS["bg_aged"], COLORS["border"], 3)
    
    ft = "数据来源：SamMobile / iTnews  |  2026-04-03  |  贾维斯AI信息图"
    fw = draw.textbbox((0, 0), ft, font=font_caption)
    tw = fw[2] - fw[0]
    draw.text(((width - tw)//2, footer_y + 22), ft, font=font_caption, fill=COLORS["text_brown"])
    
    # 角落装饰
    draw.polygon([(margin, 15), (margin+35, 15), (margin, 50)], fill=COLORS["icon_gold"])
    draw.polygon([(width-margin, 15), (width-margin-35, 15), (width-margin, 50)], fill=COLORS["icon_gold"])
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img = img.convert('RGB')
    img.save(OUTPUT_PATH, 'JPEG', quality=95)
    print(f"✅ 已保存: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_infographic()
