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
TEAL = (32, 201, 151)

FONT_CN = "/home/node/.openclaw/fonts/NotoSansSC.otf"

def get_font(size):
    return ImageFont.truetype(FONT_CN, size)

def draw_wrapped_text(draw, text, x, y, max_width, font, color, line_spacing=10):
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

def create_polymarket_card():
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
    draw.text((PADDING, y), "Polymarket 预测热点", fill=TEXT_DARK, font=title_font)
    y += 62

    en_font = get_font(18)
    draw.text((PADDING, y), "PREDICTION MARKET TRENDS", fill=TEXT_GRAY, font=en_font)
    y += 42

    # === MAIN PREDICTION CARD ===
    main_h = 240
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+main_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+main_h], radius=CARD_RADIUS, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+12, y+main_h], radius=6, fill=TEAL)

    cx = PADDING + 45
    card_content_width = CONTENT_WIDTH - 80
    cy = y + 25

    # Label
    label_font = get_font(16)
    draw.text((cx, cy), "经济预测", fill=TEAL, font=label_font)
    cy += 35

    # Headline
    h1_font = get_font(30)
    draw.text((cx, cy), "美国经济软着陆概率极高", fill=TEXT_DARK, font=h1_font)
    cy += 52

    # Subheadline
    h2_font = get_font(26)
    draw.text((cx, cy), "69.5% 概率2026年不衰退", fill=TEXT_DARK, font=h2_font)
    cy += 50

    # Description
    desc_font = get_font(19)
    desc_height = draw_wrapped_text(draw, "Q4 2025年GDP增长0.7%，2月通胀率稳定在2.4%，美联储维持利率3.5-3.75%", cx, cy, card_content_width, desc_font, TEXT_GRAY)
    cy += desc_height + 12

    # Key fact
    key_font = get_font(20)
    draw.text((cx, cy), "美联储仅计划2026年降息一次", fill=TEXT_GRAY, font=key_font)

    y += main_h + 28

    # === SECONDARY PREDICTIONS (2 cards) ===
    card2_h = 220
    col_w = (CONTENT_WIDTH - 25) // 2

    news2 = [
        {
            "label": "体育预测",
            "conclusion": "公羊领跑超级碗预测",
            "detail": "洛杉矶公羊以14%概率位居榜首，其次是海鹰、费城老鹰和丹佛野马",
            "color": LIGHT_BLUE
        },
        {
            "label": "电影预测",
            "conclusion": "蜘蛛侠新作有望夺年度票房",
            "detail": "《蜘蛛侠：全新开始》以32%概率成为2026年票房冠军预测领跑者",
            "color": LIGHT_PURPLE
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

        label_font = get_font(16)
        draw.text((tx, ty), item["label"], fill=item["color"], font=label_font)
        ty += 32

        title_font = get_font(22)
        ty += draw_wrapped_text(draw, item["conclusion"], tx, ty, col_w - 50, title_font, TEXT_DARK, line_spacing=6)
        ty += 12

        desc_font = get_font(17)
        ty += draw_wrapped_text(draw, item["detail"], tx, ty, col_w - 45, desc_font, TEXT_GRAY, line_spacing=6)

    y += card2_h + 25

    # === MORE PREDICTIONS (full width) ===
    more_h = 115
    more_news = [
        ("气候预测", "38%概率2026年成史上第四热年", "9%概率刷新历史最高温纪录", LIGHT_GREEN),
        ("中期选举", "共和党保住47席参议院概率如何？", "预测市场关注两院归属变化", ACCENT_ORANGE),
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

    # === SUMMARY SECTION ===
    y += 15
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
    draw.text((sx, sy), "1. 美国经济稳健，预测市场看好软着陆", fill=TEXT_GRAY, font=sum_font)
    sy += 32
    draw.text((sx, sy), "2. 体育娱乐预测活跃，公羊和蜘蛛侠领跑", fill=TEXT_GRAY, font=sum_font)

    y += summary_h + 15

    # === FOOTER ===
    footer_y = HEIGHT - 75
    draw.line([PADDING, footer_y - 12, WIDTH - PADDING, footer_y - 12], fill=(200, 200, 200), width=1)

    small_font = get_font(15)
    draw.text((PADDING, footer_y), "预测市场", fill=TEXT_GRAY, font=small_font)

    page_text = "01/06"
    pw = 50
    draw.text((WIDTH - PADDING - pw, footer_y), page_text, fill=TEXT_GRAY, font=small_font)

    source = "来源: Polymarket.com"
    sw = 160
    draw.text(((WIDTH - sw) // 2, footer_y), source, fill=TEXT_GRAY, font=small_font)

    output_path = "/home/node/.openclaw/workspace/polymarket_card_20260402.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}, Size: {WIDTH}x{HEIGHT}")

create_polymarket_card()
