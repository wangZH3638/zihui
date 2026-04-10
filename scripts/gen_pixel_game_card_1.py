#!/usr/bin/env python3
"""复古像素风游戏信息图生成器"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/pixel_game_card.jpg"

# 像素风配色
COLORS = {
    "bg_dark": "#1a0a2e",       # 深紫黑
    "bg_mid": "#2d1b4e",        # 中紫
    "accent_pink": "#ff6b9d",   # 霓虹粉
    "accent_cyan": "#00fff7",   # 霓虹青
    "accent_yellow": "#ffe66d", # 像素黄
    "accent_green": "#39ff14",  # 街机绿
    "text_white": "#ffffff",
    "text_gray": "#b8b8d1",
    "star": "#ffd700",
}

def find_latest_image():
    """找最新的图片"""
    import glob
    files = glob.glob("/tmp/*.png") + glob.glob("/tmp/*.jpg") + \
            glob.glob("/home/node/.openclaw/workspace/minimax-output/*.png") + \
            glob.glob("/home/node/.openclaw/workspace/minimax-output/*.jpg")
    files.sort(key=os.path.getmtime, reverse=True)
    for f in files:
        if "pixel" not in f.lower() and "game" not in f.lower():
            return f
    return files[0] if files else None

def add_pixel_border(img, border=8):
    """给图片加像素风格边框"""
    width, height = img.size
    new_img = Image.new('RGB', (width + border*2, height + border*2), COLORS["bg_dark"])
    draw = ImageDraw.Draw(new_img)
    
    # 像素风边框 - 粗线条
    border_color = COLORS["accent_pink"]
    # 上边框
    draw.rectangle([0, 0, width + border*2 - 1, 3], fill=COLORS["accent_cyan"])
    # 下边框  
    draw.rectangle([0, height + border*2 - 4, width + border*2 - 1, height + border*2 - 1], fill=COLORS["accent_cyan"])
    # 左边框
    draw.rectangle([0, 0, 3, height + border*2 - 1], fill=COLORS["accent_pink"])
    # 右边框
    draw.rectangle([width + border*2 - 4, 0, width + border*2 - 1, height + border*2 - 1], fill=COLORS["accent_pink"])
    
    new_img.paste(img, (border, border))
    return new_img

def add_scanlines(img, interval=3, alpha=30):
    """添加扫描线效果"""
    width, height = img.size
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for y in range(0, height, interval):
        draw.rectangle([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def create_pixel_text_img(text, font_size, color, stroke=False):
    """创建像素风格的文字图像"""
    # 使用默认位图字体模拟像素感
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # 创建临时图像测量文字宽度
    temp_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 创建文字图像
    padding = 10
    img = Image.new('RGBA', (text_width + padding*2, text_height + padding*2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    if stroke:
        # 描边效果
        for dx, dy in [(-2,0), (2,0), (0,-2), (0,2), (-2,-2), (2,-2), (-2,2), (2,2)]:
            draw.text((padding + dx, padding + dy), text, font=font, fill=(0, 0, 0, 200))
    
    draw.text((padding, padding), text, font=font, fill=color)
    return img

def add_glow_effect(draw, x, y, radius=20, color=(0, 255, 247, 50)):
    """添加发光效果"""
    for i in range(3):
        r = radius + i * 5
        alpha = 30 - i * 10
        draw.ellipse([x-r, y-r, x+r, y+r], fill=(color[0], color[1], color[2], alpha))

def create_infographic():
    # 找背景图
    bg_path = find_latest_image()
    print(f"背景图: {bg_path}")
    
    if bg_path:
        img = Image.open(bg_path).convert('RGB')
        # 调整大小
        target_w, target_h = 1080, 1440
        # 裁剪并缩放
        img_ratio = img.width / img.height
        target_ratio = target_w / target_h
        if img_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            offset = (img.width - new_width) // 2
            img = img.crop((offset, 0, offset + new_width, img.height))
        else:
            new_height = int(img.width / target_ratio)
            offset = (img.height - new_height) // 2
            img = img.crop((0, offset, img.width, offset + new_height))
        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (1080, 1440), COLORS["bg_dark"])
    
    # 调整背景亮度
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.7)  # 调暗一点
    
    # 添加彩色渐变叠加
    overlay = Image.new('RGB', (1080, 1440), (0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    for y in range(1440):
        alpha = int(100 * (1 - y / 1440))
        overlay_draw.line([(0, y), (1080, y)], fill=(26, 10, 46, alpha))
    
    img = Image.blend(img, overlay, 0.3)
    
    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)
    
    # === 加载像素风字体 ===
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 42)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        font_pixel = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = font_title
        font_body = font_title
        font_small = font_title
        font_pixel = font_title
    
    width, height = 1080, 1440
    
    # === 顶部装饰 - 像素风格标题栏 ===
    # 标题栏背景
    title_bar = Image.new('RGBA', (width, 120), (0, 0, 0, 180))
    title_bar_draw = ImageDraw.Draw(title_bar)
    
    # 像素风边框
    title_bar_draw.rectangle([0, 0, width-1, 4], fill=COLORS["accent_yellow"])
    title_bar_draw.rectangle([0, 115, width-1, 119], fill=COLORS["accent_yellow"])
    
    img.paste(title_bar, (0, 0), title_bar)
    draw = ImageDraw.Draw(img)
    
    # 主标题 - 像素风文字
    title = "GAME STATS"
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    # 文字描边
    for dx, dy in [(-3,0), (3,0), (0,-3), (0,3)]:
        draw.text(((width - title_width)//2 + dx, 30 + dy), title, font=font_title, fill=(0,0,0))
    draw.text(((width - title_width)//2, 30), title, font=font_title, fill=COLORS["accent_yellow"])
    
    # 副标题
    subtitle = "PRESS START ▼"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    sub_width = sub_bbox[2] - sub_bbox[0]
    draw.text(((width - sub_width)//2, 95), subtitle, font=font_small, fill=COLORS["accent_cyan"])
    
    # === 装饰像素图标 ===
    # 左上角像素心形
    pixel_heart_x, pixel_heart_y = 60, 50
    heart_positions = [
        (pixel_heart_x+4, pixel_heart_y), (pixel_heart_x+12, pixel_heart_y),
        (pixel_heart_x+20, pixel_heart_y), (pixel_heart_x+28, pixel_heart_y),
        (pixel_heart_x, pixel_heart_y+4), (pixel_heart_x+8, pixel_heart_y+4),
        (pixel_heart_x+16, pixel_heart_y+4), (pixel_heart_x+24, pixel_heart_y+4),
        (pixel_heart_x+32, pixel_heart_y+4),
        (pixel_heart_x, pixel_heart_y+8), (pixel_heart_x+8, pixel_heart_y+8),
        (pixel_heart_x+16, pixel_heart_y+8), (pixel_heart_x+24, pixel_heart_y+8), (pixel_heart_x+32, pixel_heart_y+8),
        (pixel_heart_x+4, pixel_heart_y+12), (pixel_heart_x+12, pixel_heart_y+12),
        (pixel_heart_x+20, pixel_heart_y+12), (pixel_heart_x+28, pixel_heart_y+12),
        (pixel_heart_x+8, pixel_heart_y+16), (pixel_heart_x+16, pixel_heart_y+16), (pixel_heart_x+24, pixel_heart_y+16),
        (pixel_heart_x+12, pixel_heart_y+20), (pixel_heart_x+20, pixel_heart_y+20),
    ]
    for px, py in heart_positions:
        draw.rectangle([px, py, px+4, py+4], fill=COLORS["accent_pink"])
    
    # 右上角像素星星
    star_x = width - 100
    star_y = 50
    star_positions = [
        (star_x+16, star_y), (star_x+20, star_y), (star_x+24, star_y),
        (star_x+12, star_y+4), (star_x+16, star_y+4), (star_x+20, star_y+4), (star_x+24, star_y+4), (star_x+28, star_y+4),
        (star_x+8, star_y+8), (star_x+12, star_y+8), (star_x+16, star_y+8), (star_x+20, star_y+8), (star_x+24, star_y+8), (star_x+28, star_y+8), (star_x+32, star_y+8),
        (star_x+4, star_y+12), (star_x+8, star_y+12), (star_x+12, star_y+12), (star_x+16, star_y+12), (star_x+20, star_y+12), (star_x+24, star_y+12), (star_x+28, star_y+12), (star_x+32, star_y+12), (star_x+36, star_y+12),
        (star_x, star_y+16), (star_x+4, star_y+16), (star_x+8, star_y+16), (star_x+12, star_y+16), (star_x+16, star_y+16), (star_x+20, star_y+16), (star_x+24, star_y+16), (star_x+28, star_y+16), (star_x+32, star_y+16), (star_x+36, star_y+16), (star_x+40, star_y+16),
        (star_x+8, star_y+20), (star_x+12, star_y+20), (star_x+16, star_y+20), (star_x+20, star_y+20), (star_x+24, star_y+20), (star_x+28, star_y+20), (star_x+32, star_y+20),
        (star_x+12, star_y+24), (star_x+16, star_y+24), (star_x+20, star_y+24), (star_x+24, star_y+24), (star_x+28, star_y+24),
        (star_x+16, star_y+28), (star_x+20, star_y+28), (star_x+24, star_y+28),
        (star_x+20, star_y+32),
    ]
    for px, py in star_positions:
        draw.rectangle([px, py, px+4, py+4], fill=COLORS["star"])
    
    # === 玩家数据卡片1 ===
    card1_y = 160
    card1 = Image.new('RGBA', (width-80, 200), (0, 0, 0, 150))
    card1_draw = ImageDraw.Draw(card1)
    
    # 像素边框
    card1_draw.rectangle([0, 0, 6, 199], fill=COLORS["accent_green"])
    card1_draw.rectangle([width-80-6, 0, width-80-1, 199], fill=COLORS["accent_green"])
    
    # 标签
    card1_draw.text((25, 15), "▶ PLAYER LV.99", font=font_pixel, fill=COLORS["accent_green"])
    
    # 数据
    card1_draw.text((25, 50), "HP", font=font_small, fill=COLORS["accent_pink"])
    card1_draw.rectangle([25, 78, 400, 90], fill=(50, 50, 50))
    card1_draw.rectangle([25, 78, 380, 90], fill=COLORS["accent_pink"])  # 95% HP
    card1_draw.text((410, 78), "3800/4000", font=font_small, fill=COLORS["text_white"])
    
    card1_draw.text((25, 105), "MP", font=font_small, fill=COLORS["accent_cyan"])
    card1_draw.rectangle([25, 133, 400, 145], fill=(50, 50, 50))
    card1_draw.rectangle([25, 133, 280, 145], fill=COLORS["accent_cyan"])  # 70% MP
    card1_draw.text((410, 133), "1400/2000", font=font_small, fill=COLORS["text_white"])
    
    card1_draw.text((25, 160), "EXP", font=font_small, fill=COLORS["accent_yellow"])
    card1_draw.rectangle([25, 185, 400, 195], fill=(50, 50, 50))
    card1_draw.rectangle([25, 185, 320, 195], fill=COLORS["accent_yellow"])  # 80%
    card1_draw.text((410, 185), "8000/10000", font=font_small, fill=COLORS["text_white"])
    
    img.paste(card1, (40, card1_y), card1)
    
    # === 游戏数据卡片2 ===
    card2_y = card1_y + 220
    card2 = Image.new('RGBA', (width-80, 280), (0, 0, 0, 150))
    card2_draw = ImageDraw.Draw(card2)
    
    card2_draw.rectangle([0, 0, 6, 279], fill=COLORS["accent_cyan"])
    card2_draw.rectangle([width-80-6, 0, width-80-1, 279], fill=COLORS["accent_cyan"])
    
    card2_draw.text((25, 15), "🎮 GAME RANKINGS", font=font_pixel, fill=COLORS["accent_cyan"])
    
    # 排行榜数据
    rankings = [
        ("1UP", "#1", COLORS["accent_yellow"]),
        ("MARIO", "999999", COLORS["accent_pink"]),
        ("SONIC", "888888", COLORS["accent_cyan"]),
        ("LINK", "777777", COLORS["accent_green"]),
        ("SAMUS", "666666", COLORS["accent_pink"]),
    ]
    
    y_pos = 55
    for name, score, color in rankings:
        card2_draw.text((25, y_pos), f"RANK", font=font_small, fill=COLORS["text_gray"])
        card2_draw.text((90, y_pos), name, font=font_body, fill=color)
        score_bbox = card2_draw.textbbox((0, 0), score, font=font_body)
        score_width = score_bbox[2]
        card2_draw.text((width-80 - 25 - score_width, y_pos), score, font=font_body, fill=COLORS["text_white"])
        y_pos += 42
    
    img.paste(card2, (40, card2_y), card2)
    
    # === 成就卡片3 ===
    card3_y = card2_y + 300
    card3 = Image.new('RGBA', (width-80, 220), (0, 0, 0, 150))
    card3_draw = ImageDraw.Draw(card3)
    
    card3_draw.rectangle([0, 0, 6, 219], fill=COLORS["accent_pink"])
    card3_draw.rectangle([width-80-6, 0, width-80-1, 219], fill=COLORS["accent_pink"])
    
    card3_draw.text((25, 15), "🏆 ACHIEVEMENTS", font=font_pixel, fill=COLORS["accent_pink"])
    
    achievements = [
        "◆ FIRST PLAY    [✓ UNLOCKED]",
        "◆ HIGH SCORE    [✓ UNLOCKED]",
        "◆ SPEED RUN     [✗ LOCKED]",
        "◆ PERFECT GAME  [✗ LOCKED]",
    ]
    y_pos = 55
    for ach in achievements:
        unlocked = "[✓" in ach
        color = COLORS["accent_yellow"] if unlocked else (100, 100, 100)
        card3_draw.text((25, y_pos), ach, font=font_small, fill=color)
        y_pos += 38
    
    img.paste(card3, (40, card3_y), card3)
    
    # === 关卡信息条 ===
    level_bar_y = card3_y + 240
    
    level_bar = Image.new('RGBA', (width, 80), (0, 0, 0, 200))
    level_bar_draw = ImageDraw.Draw(level_bar)
    
    # 关卡信息
    level_bar_draw.text((40, 25), "STAGE 1-1", font=font_body, fill=COLORS["accent_green"])
    level_bar_draw.text((40, 50), "▼ COIN × 127", font=font_small, fill=COLORS["accent_yellow"])
    
    level_bar_draw.text((width//2 - 50, 25), "TIME", font=font_small, fill=COLORS["text_gray"])
    level_bar_draw.text((width//2 - 30, 45), "03:42", font=font_subtitle, fill=COLORS["accent_cyan"])
    
    level_bar_draw.text((width - 200, 25), "WORLD", font=font_small, fill=COLORS["text_gray"])
    level_bar_draw.text((width - 180, 45), "1-1", font=font_subtitle, fill=COLORS["accent_pink"])
    
    img.paste(level_bar, (0, level_bar_y), level_bar)
    
    # === 底部提示 ===
    footer_y = height - 60
    draw.line([(40, footer_y), (width-40, footer_y)], fill=COLORS["accent_cyan"], width=2)
    
    tip = "INSERT COIN  ◆  PRESS START  ◆  CONTINUE?"
    tip_bbox = draw.textbbox((0, 0), tip, font=font_small)
    tip_width = tip_bbox[2] - tip_bbox[0]
    draw.text(((width - tip_width)//2, footer_y + 15), tip, font=font_small, fill=COLORS["accent_cyan"])
    
    # 角落装饰 - 像素方块
    for i in range(4):
        draw.rectangle([40 + i*15, height-45, 50 + i*15, height-35], fill=COLORS["accent_pink"] if i%2==0 else COLORS["accent_cyan"])
        draw.rectangle([width-90 + i*15, height-45, width-80 + i*15, height-35], fill=COLORS["accent_pink"] if i%2==0 else COLORS["accent_cyan"])
    
    # === 添加扫描线效果 ===
    scanline_overlay = Image.new('L', (width, height), 0)
    scanline_draw = ImageDraw.Draw(scanline_overlay)
    for y in range(0, height, 4):
        scanline_draw.rectangle([(0, y), (width, y+1)], fill=25)
    scanline_img = Image.merge('RGB', [scanline_overlay, scanline_overlay, scanline_overlay])
    img = Image.blend(img, scanline_img, 0.08)
    
    # 保存
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img = img.convert('RGB')
    img.save(OUTPUT_PATH, 'JPEG', quality=95)
    print(f"✅ 像素风游戏信息图已保存: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    create_infographic()
