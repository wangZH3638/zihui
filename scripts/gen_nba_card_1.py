#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import textwrap

WIDTH = 1080
HEIGHT = 1440
BG_COLOR = (232, 230, 227)

TEXT_DARK = (45, 45, 45)
TEXT_GRAY = (107, 114, 128)
ACCENT_ORANGE = (232, 93, 4)
WHITE = (255, 255, 255)
LIGHT_BLUE = (59, 130, 246)
LIGHT_GREEN = (76, 175, 80)
LIGHT_PURPLE = (156, 39, 176)
RED = (220, 53, 69)

FONT_CN = "/home/node/.openclaw/fonts/NotoSansSC.otf"

def get_font(size):
    return ImageFont.truetype(FONT_CN, size)

def draw_wrapped_text(draw, text, x, y, max_width, font, color, line_spacing=10):
    # Use conservative estimate: Chinese chars are ~1.2x font size width
    avg_char_width = font.size * 1.2
    chars_per_line = int(max_width / avg_char_width)
    if chars_per_line < 8:
        chars_per_line = 8
    lines = textwrap.wrap(text, width=chars_per_line)
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, fill=color, font=font)
        current_y += font.size + line_spacing
    return current_y - y

def create_nba_card():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    PADDING = 50
    CARD_RADIUS = 16
    CONTENT_WIDTH = WIDTH - 2 * PADDING

    y = PADDING

    # === HEADER ===
    date_font = get_font(22)
    draw.text((PADDING, y), "2026年4月2日", fill=TEXT_GRAY, font=date_font)
    y += 50

    title_font = get_font(48)
    draw.text((PADDING, y), "NBA每日战报", fill=TEXT_DARK, font=title_font)
    y += 62

    en_font = get_font(18)
    draw.text((PADDING, y), "JARVIS NBA DAILY REPORT", fill=TEXT_GRAY, font=en_font)
    y += 42

    # === MAIN NEWS CARD (总分结构：结论先行) ===
    main_h = 260
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+main_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+main_h], radius=CARD_RADIUS, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+12, y+main_h], radius=6, fill=RED)

    cx = PADDING + 45
    card_content_width = CONTENT_WIDTH - 80
    cy = y + 25

    # 结论先行：大比分+核心结果
    h1_font = get_font(30)
    draw.text((cx, cy), "猛龙大胜国王 131-115", fill=TEXT_DARK, font=h1_font)
    cy += 52

    # 原因/过程
    h2_font = get_font(26)
    draw.text((cx, cy), "西亚卡姆砍全场最高分率队取胜", fill=TEXT_DARK, font=h2_font)
    cy += 48

    # 详细描述
    desc_font = get_font(19)
    desc_height = draw_wrapped_text(draw, "多伦多猛龙主场大胜萨克拉门托国王，西亚卡姆发挥出色带领球队取得关键胜利", cx, cy, card_content_width, desc_font, TEXT_GRAY)
    cy += desc_height + 12

    # 数据亮点
    key_font = get_font(20)
    draw.text((cx, cy), "西亚卡姆 ", fill=TEXT_GRAY, font=key_font)
    draw.text((cx + key_font.getlength("西亚卡姆 "), cy), "最高得分", fill=ACCENT_ORANGE, font=key_font)
    draw.text((cx + key_font.getlength("西亚卡姆 最高得分"), cy), " | 猛龙主场连胜", fill=TEXT_GRAY, font=key_font)

    y += main_h + 28

    # === SECONDARY NEWS (总分结构) ===
    card2_h = 230
    col_w = (CONTENT_WIDTH - 25) // 2

    news2 = [
        {
            "label": "球员动态",
            "conclusion": "公牛客场落败，河村勇辉3助攻",
            "detail": "芝加哥公牛102-118不敌步行者，河村勇辉替补出场贡献3次助攻，表现稳定",
            "color": LIGHT_BLUE
        },
        {
            "label": "比赛战报",
            "conclusion": "库里32分难救主，勇士负马刺",
            "detail": "金州勇士93-107不敌圣安东尼奥马刺，库里拿下全队最高32分但未能带领球队取胜",
            "color": LIGHT_GREEN
        }
    ]

    for i, item in enumerate(news2):
        cx = PADDING if i == 0 else PADDING + col_w + 25
        cy = y

        draw.rounded_rectangle([cx+4, cy+4, cx+col_w+4, cy+card2_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
        draw.rounded_rectangle([cx, cy, cx+col_w, cy+card2_h], radius=CARD_RADIUS, fill=WHITE)
        draw.rounded_rectangle([cx, cy, cx+10, cy+card2_h], radius=5, fill=item["color"])

        tx = cx + 28
        ty = cy + 20

        # 标签
        label_font = get_font(16)
        draw.text((tx, ty), item["label"], fill=item["color"], font=label_font)
        ty += 32

        # 结论先行
        title_font = get_font(22)
        ty += draw_wrapped_text(draw, item["conclusion"], tx, ty, col_w - 50, title_font, TEXT_DARK, line_spacing=6)
        ty += 12

        # 详细描述
        desc_font = get_font(17)
        ty += draw_wrapped_text(draw, item["detail"], tx, ty, col_w - 45, desc_font, TEXT_GRAY, line_spacing=6)

    y += card2_h + 25

    # === MORE NEWS (总分结构) ===
    more_h = 115
    more_news = [
        ("焦点对决", "奇才119-113胜76人", "八村垒砍27分7篮板表现亮眼", LIGHT_PURPLE),
        ("西部格局", "湖人紧追勇士", "季后赛席位之争进入白热化", ACCENT_ORANGE),
    ]

    for i, (label, conclusion, detail, color) in enumerate(more_news):
        mx = PADDING
        my = y

        draw.rounded_rectangle([mx+4, my+4, WIDTH-PADDING+4, my+more_h+4], radius=12, fill=(0,0,0,20))
        draw.rounded_rectangle([mx, my, WIDTH-PADDING, my+more_h], radius=12, fill=WHITE)
        draw.rounded_rectangle([mx, my, mx+10, my+more_h], radius=5, fill=color)

        tx = mx + 35
        ty = my + 18

        label_font = get_font(16)
        draw.text((tx, ty), label, fill=color, font=label_font)

        title_font = get_font(22)
        draw.text((tx, ty + 28), conclusion, fill=TEXT_DARK, font=title_font)

        desc_font = get_font(17)
        draw.text((tx, ty + 60), detail, fill=TEXT_GRAY, font=desc_font)

        y += more_h + 15

    # === STANDINGS SECTION ===
    y += 15
    section_font = get_font(22)
    draw.text((PADDING, y), "东西部排名", fill=TEXT_DARK, font=section_font)
    y += 50

    standings_data = [
        ("东部", "1 凯尔特人", "2 尼克斯", "3 雄鹿"),
        ("西部", "1 雷霆", "2 湖人", "3 勇士"),
    ]

    stand_w = (CONTENT_WIDTH - 20) // 2
    stand_h = 100
    for i, (conf, t1, t2, t3) in enumerate(standings_data):
        mx = PADDING if i == 0 else PADDING + stand_w + 20
        my = y

        draw.rounded_rectangle([mx, my, mx+stand_w, my+stand_h], radius=12, fill=WHITE)

        conf_font = get_font(18)
        draw.text((mx + 20, my + 15), conf, fill=RED if i == 0 else LIGHT_BLUE, font=conf_font)

        rank_font = get_font(17)
        draw.text((mx + 20, my + 45), t1, fill=TEXT_DARK, font=rank_font)
        draw.text((mx + 20, my + 68), t2, fill=TEXT_GRAY, font=rank_font)
        draw.text((mx + stand_w//2, my + 45), t3, fill=TEXT_GRAY, font=rank_font)

    y += stand_h + 20

    # === SUMMARY SECTION ===
    y += 10
    summary_h = 120
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+summary_h+4], radius=12, fill=(0,0,0,20))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+summary_h], radius=12, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+10, y+summary_h], radius=5, fill=ACCENT_ORANGE)

    sx = PADDING + 35
    sy = y + 18

    sum_title_font = get_font(20)
    draw.text((sx, sy), "本期要点", fill=TEXT_DARK, font=sum_title_font)
    sy += 38

    sum_font = get_font(18)
    draw.text((sx, sy), "1. 西亚卡姆爆发砍最高分，猛龙大胜国王巩固排名", fill=TEXT_GRAY, font=sum_font)
    sy += 32
    draw.text((sx, sy), "2. 库里独木难支，勇士爆冷负马刺排名下滑", fill=TEXT_GRAY, font=sum_font)

    y += summary_h + 15

    # === FOOTER ===
    footer_y = HEIGHT - 75
    draw.line([PADDING, footer_y - 12, WIDTH - PADDING, footer_y - 12], fill=(200, 200, 200), width=1)

    small_font = get_font(15)
    draw.text((PADDING, footer_y), "篮球赛事", fill=TEXT_GRAY, font=small_font)

    page_text = "01/06"
    pw = 50
    draw.text((WIDTH - PADDING - pw, footer_y), page_text, fill=TEXT_GRAY, font=small_font)

    source = "来源: TSP Sports / Yahoo Sports"
    sw = 220
    draw.text(((WIDTH - sw) // 2, footer_y), source, fill=TEXT_GRAY, font=small_font)

    output_path = "/home/node/.openclaw/workspace/nba_card_20260402.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}, Size: {WIDTH}x{HEIGHT}")

create_nba_card()
