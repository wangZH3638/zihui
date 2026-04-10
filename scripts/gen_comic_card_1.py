#!/usr/bin/env python3
"""美式卡通漫画风信息图生成器"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/comic_card.jpg"

# 漫画风配色 - 经典四色
COLORS = {
    "bg_cream": "#FFF8E7",      # 奶油色背景
    "red": "#E53935",           # 漫画红
    "yellow": "#FFD600",       # 漫画黄
    "blue": "#1E88E5",          # 漫画蓝
    "black": "#1a1a1a",         # 粗黑线
    "shadow": "#4A4A4A",        # 阴影灰
    "white": "#FFFFFF",
    "skin": "#FFCC99",         # 肤色
    "caption": "#8B0000",       # 深红说明文字
}

def find_latest_image():
    """找最新的图片"""
    import glob
    files = glob.glob("/tmp/*.png") + glob.glob("/tmp/*.jpg") + \
            glob.glob("/home/node/.openclaw/workspace/minimax-output/*.png") + \
            glob.glob("/home/node/.openclaw/workspace/minimax-output/*.jpg")
    files.sort(key=os.path.getmtime, reverse=True)
    # 找最新的非comic图片作为背景
    for f in files:
        if "comic" not in f.lower():
            return f
    return files[0] if files else None

def add_halftone_dots(img, density=0.3):
    """添加本·戴网点效果"""
    width, height = img.size
    overlay = Image.new('RGB', (width, height), COLORS["bg_cream"])
    draw = ImageDraw.Draw(overlay)
    
    dot_spacing = 12
    for y in range(0, height, dot_spacing):
        for x in range(0, width, dot_spacing):
            offset_x = (y // dot_spacing) % 2 * (dot_spacing // 2)
            # 根据原图亮度决定网点大小
            px = min(x + offset_x, width - 1)
            py = min(y, height - 1)
            try:
                pixel = img.getpixel((px, py))
                brightness = (pixel[0] + pixel[1] + pixel[2]) / 3 / 255
                dot_size = int(3 * (1 - brightness * density))
                if dot_size > 0:
                    draw.ellipse([px-dot_size, py-dot_size, px+dot_size, py+dot_size], 
                               fill=COLORS["shadow"])
            except:
                pass
    
    return Image.blend(img, overlay, 0.15)

def add_radial_burst(draw, cx, cy, radius, color, num_rays=12):
    """添加放射状爆发效果"""
    for i in range(num_rays):
        angle = (360 / num_rays) * i * math.pi / 180
        x2 = cx + radius * math.cos(angle)
        y2 = cy + radius * math.sin(angle)
        draw.line([(cx, cy), (x2, y2)], fill=color, width=8)

def add_explosion_shape(draw, cx, cy, size, color):
    """添加爆炸形状"""
    points = []
    num_points = 16
    for i in range(num_points * 2):
        angle = (360 / (num_points * 2)) * i * math.pi / 180
        if i % 2 == 0:
            r = size
        else:
            r = size * 0.6
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    draw.polygon(points, fill=color, outline=COLORS["black"])

def draw_comic_bubble(draw, x, y, w, h, text, font, color, tail_x=None, tail_y=None):
    """绘制漫画对话气泡"""
    # 气泡主体（圆角矩形效果）
    margin = 8
    draw.ellipse([x-margin, y-margin, x+w+margin, y+h+margin], 
                fill=COLORS["white"], outline=COLORS["black"], width=4)
    
    # 气泡尾巴
    if tail_x is not None and tail_y is not None:
        points = [
            (x + w//2 - 15, y + h),
            (x + w//2 + 15, y + h),
            (tail_x, tail_y)
        ]
        draw.polygon(points, fill=COLORS["white"], outline=COLORS["black"], width=4)
        # 重新描边尾巴
        draw.line([(x + w//2 - 15, y + h), (tail_x, tail_y)], fill=COLORS["black"], width=4)
        draw.line([(x + w//2 + 15, y + h), (tail_x, tail_y)], fill=COLORS["black"], width=4)
    
    # 文字
    draw.text((x + 10, y + 10), text, font=font, fill=color)

def draw_thick_outline(img, thickness=6):
    """给图片加粗轮廓"""
    from PIL import ImageFilter
    # 转RGBA
    img = img.convert('RGBA')
    # 创建轮廓
    enhanced = img.copy()
    
    # 简单的轮廓效果通过叠加描边
    overlay = Image.new('RGBA', img.size, (0,0,0,0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    width, height = img.size
    pixels = img.load()
    
    # 简化：直接用绘图方式添加粗边框
    border = Image.new('RGBA', (width + thickness*2, height + thickness*2), COLORS["black"])
    border.paste(img, (thickness, thickness), img)
    
    return border

def create_infographic():
    width, height = 1080, 1440
    
    # 找背景图
    bg_path = find_latest_image()
    print(f"背景图: {bg_path}")
    
    if bg_path:
        bg = Image.open(bg_path).convert('RGB')
        # 裁剪为3:4
        bg_ratio = bg.width / bg.height
        target_ratio = width / height
        if bg_ratio > target_ratio:
            new_width = int(bg.height * target_ratio)
            offset = (bg.width - new_width) // 2
            bg = bg.crop((offset, 0, offset + new_width, bg.height))
        else:
            new_height = int(bg.width / target_ratio)
            offset = (bg.height - new_height) // 2
            bg = bg.crop((0, offset, bg.width, offset + new_height))
        bg = bg.resize((width, height), Image.Resampling.LANCZOS)
    else:
        bg = Image.new('RGB', (width, height), COLORS["bg_cream"])
    
    # 添加网点效果
    bg = add_halftone_dots(bg)
    
    img = bg.copy()
    draw = ImageDraw.Draw(img)
    
    # === 字体 ===
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        font_exclaim = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_caption = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_exclaim = font_title
        font_subtitle = font_title
        font_body = font_title
        font_caption = font_title
        font_small = font_title
    
    # === 顶部粗黑边框 ===
    draw.rectangle([0, 0, width-1, 25], fill=COLORS["black"])
    draw.rectangle([0, height-25, width-1, height-1], fill=COLORS["black"])
    draw.rectangle([0, 0, 25, height-1], fill=COLORS["black"])
    draw.rectangle([width-25, 0, width-1, height-1], fill=COLORS["black"])
    
    # === 主标题区域 - 漫画风格 ===
    title_y = 60
    
    # 黄色背景块
    draw.rectangle([40, title_y, width-40, title_y + 130], fill=COLORS["yellow"], outline=COLORS["black"], width=6)
    
    # 标题文字（黑边白字）
    title = "BOOM!"
    title_bbox = draw.textbbox((0, 0), title, font=font_exclaim)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    # 文字描边（粗黑边）
    for dx, dy in [(-6,-6), (6,-6), (-6,6), (6,6), (0,-6), (0,6), (-6,0), (6,0)]:
        draw.text((title_x + dx, title_y + 25 + dy), title, font=font_exclaim, fill=COLORS["black"])
    draw.text((title_x, title_y + 25), title, font=font_exclaim, fill=COLORS["white"])
    
    # === 漫画效果词1 ===
    boom_x, boom_y = width - 180, 50
    add_radial_burst(draw, boom_x + 50, boom_y + 60, 60, COLORS["yellow"])
    draw.text((boom_x, boom_y), "POW!", font=font_subtitle, fill=COLORS["red"])
    
    # === 新闻内容区 ===
    content_y = 230
    
    # 漫画气泡1 - 主新闻
    bubble1_h = 180
    bubble1 = Image.new('RGBA', (width - 100, bubble1_h), (255,255,255,0))
    bubble1_draw = ImageDraw.Draw(bubble1)
    bubble1_draw.ellipse([0, 0, width - 100 - 1, bubble1_h - 1], 
                         fill=COLORS["white"], outline=COLORS["black"], width=5)
    
    img.paste(bubble1, (50, content_y), bubble1)
    draw = ImageDraw.Draw(img)
    
    # 气泡1内容
    draw.text((75, content_y + 25), "📰 TOP STORY", font=font_body, fill=COLORS["red"])
    draw.text((75, content_y + 70), "科技巨头发布", font=font_caption, fill=COLORS["black"])
    draw.text((75, content_y + 105), "新一代AI芯片!", font=font_subtitle, fill=COLORS["blue"])
    draw.text((75, content_y + 160), "处理速度提升300%", font=font_small, fill=COLORS["shadow"])
    
    # 气泡1尾巴
    tail_points = [(width//2 - 30, content_y + bubble1_h), 
                   (width//2 + 30, content_y + bubble1_h),
                   (width//2, content_y + bubble1_h + 50)]
    draw.polygon(tail_points, fill=COLORS["white"], outline=COLORS["black"], width=5)
    
    # === 效果词 ZAP! ===
    zap_x, zap_y = 60, content_y + bubble1_h + 20
    draw.text((zap_x, zap_y), "ZAP!", font=font_title, fill=COLORS["yellow"])
    add_radial_burst(draw, zap_x + 80, zap_y + 50, 45, COLORS["blue"])
    
    # === 漫画分镜卡片 ===
    card_y = content_y + bubble1_h + 100
    card_h = 350
    card_w = (width - 140) // 2
    
    # 左侧卡片
    left_card = Image.new('RGBA', (card_w, card_h), COLORS["white"])
    left_draw = ImageDraw.Draw(left_card)
    left_draw.rectangle([0, 0, card_w-1, card_h-1], outline=COLORS["black"], width=5)
    left_draw.rectangle([0, 0, card_w-1, 50], fill=COLORS["red"])
    
    # 左卡片内容
    left_draw.text((15, 12), "FACT 1", font=font_body, fill=COLORS["white"])
    left_draw.text((15, 65), "AI芯片", font=font_subtitle, fill=COLORS["black"])
    left_draw.text((15, 120), "性能大幅提升", font=font_body, fill=COLORS["shadow"])
    left_draw.text((15, 160), "功耗降低50%", font=font_caption, fill=COLORS["blue"])
    
    # 图表区域（条形图）
    bar_y = 210
    left_draw.rectangle([15, bar_y, 200, bar_y + 30], fill=COLORS["yellow"], outline=COLORS["black"], width=3)
    left_draw.rectangle([15, bar_y, 150, bar_y + 30], fill=COLORS["red"], outline=COLORS["black"], width=3)
    left_draw.text((15, bar_y + 40), "速度对比", font=font_small, fill=COLORS["black"])
    
    img.paste(left_card, (50, card_y), left_card)
    
    # 右侧卡片
    right_card = Image.new('RGBA', (card_w, card_h), COLORS["white"])
    right_draw = ImageDraw.Draw(right_card)
    right_draw.rectangle([0, 0, card_w-1, card_h-1], outline=COLORS["black"], width=5)
    right_draw.rectangle([0, 0, card_w-1, 50], fill=COLORS["blue"])
    
    # 右卡片内容
    right_draw.text((15, 12), "FACT 2", font=font_body, fill=COLORS["white"])
    right_draw.text((15, 65), "智能设备", font=font_subtitle, fill=COLORS["black"])
    right_draw.text((15, 120), "隐私保护升级", font=font_body, fill=COLORS["shadow"])
    right_draw.text((15, 160), "新一代加密技术", font=font_caption, fill=COLORS["red"])
    
    # 饼图效果
    pie_x, pie_y = card_w//2 - 30, 250
    right_draw.ellipse([pie_x - 50, pie_y, pie_x + 50, pie_y + 100], 
                       fill=COLORS["yellow"], outline=COLORS["black"], width=3)
    right_draw.polygon([(pie_x, pie_y + 50), (pie_x - 50, pie_y + 50), (pie_x, pie_y)], 
                      fill=COLORS["red"], outline=COLORS["black"])
    right_draw.text((pie_x - 30, pie_y + 55), "75%", font=font_caption, fill=COLORS["black"])
    
    img.paste(right_card, (50 + card_w + 40, card_y), right_card)
    draw = ImageDraw.Draw(img)
    
    # === WHAM! 效果词 ===
    wham_x = 50 + card_w + 40 - 40
    wham_y = card_y + card_h + 10
    draw.text((wham_x, wham_y), "WHAM!", font=font_title, fill=COLORS["red"])
    
    # === 底部漫画气泡 ===
    bottom_y = wham_y + 130
    bottom_h = 200
    
    bottom_bubble = Image.new('RGBA', (width - 100, bottom_h), (255,255,255,0))
    bottom_draw = ImageDraw.Draw(bottom_bubble)
    bottom_draw.ellipse([0, 0, width - 100 - 1, bottom_h - 1], 
                        fill=COLORS["white"], outline=COLORS["black"], width=5)
    
    img.paste(bottom_bubble, (50, bottom_y), bottom_bubble)
    draw = ImageDraw.Draw(img)
    
    # 底部内容
    draw.text((75, bottom_y + 20), "💡 BOTTOM LINE", font=font_body, fill=COLORS["blue"])
    draw.text((75, bottom_y + 65), "科技创新持续改变生活", font=font_subtitle, fill=COLORS["black"])
    
    points = [
        "✓ AI技术突飞猛进",
        "✓ 智能设备更注重隐私", 
        "✓ 科技让未来更美好!"
    ]
    y_pos = bottom_y + 120
    for point in points:
        draw.text((75, y_pos), point, font=font_caption, fill=COLORS["shadow"])
        y_pos += 32
    
    # 底部气泡尾巴（向上）
    tail_points = [(width//2 - 30, bottom_y), 
                   (width//2 + 30, bottom_y),
                   (width//2, bottom_y - 40)]
    draw.polygon(tail_points, fill=COLORS["white"], outline=COLORS["black"], width=5)
    
    # === 底部来源栏 ===
    footer_y = height - 100
    draw.rectangle([30, footer_y, width-30, footer_y + 60], fill=COLORS["black"])
    draw.text((width//2 - 150, footer_y + 18), "SOURCE: NEWS REPORT  |  2026-04-03", 
              font=font_small, fill=COLORS["white"])
    
    # === 角落漫画装饰 ===
    # 左下角星爆
    star_cx, star_cy = 70, height - 150
    add_explosion_shape(draw, star_cx, star_cy, 30, COLORS["yellow"])
    
    # 右上角星爆
    star_cx2, star_cy2 = width - 70, 200
    add_explosion_shape(draw, star_cx2, star_cy2, 25, COLORS["yellow"])
    
    # === 漫画网点强调 ===
    dot_overlay = Image.new('RGB', (width, height), (0,0,0,0))
    dot_draw = ImageDraw.Draw(dot_overlay)
    for _ in range(50):
        import random
        x = random.randint(50, width-50)
        y = random.randint(250, height-150)
        r = random.randint(3, 8)
        dot_draw.ellipse([x-r, y-r, x+r, y+r], fill=(0,0,0,30))
    
    img = Image.blend(img, dot_overlay, 0.1)
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img = img.convert('RGB')
    img.save(OUTPUT_PATH, 'JPEG', quality=95)
    print(f"✅ 美式卡通漫画风信息图已保存: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_infographic()
