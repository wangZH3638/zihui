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

PADDING = 50
CARD_RADIUS = 16
CONTENT_WIDTH = WIDTH - 2 * PADDING

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

def create_page_header(draw, y, date, title, subtitle, color, padding=PADDING):
    # Date - small, gray
    date_font = get_font(20)
    draw.text((padding, y), date, fill=TEXT_GRAY, font=date_font)
    y += 45

    # Main title - largest, dark black, bold feel
    title_font = get_font(52)
    draw.text((padding, y), title, fill=TEXT_DARK, font=title_font)
    y += 65

    # Subtitle - medium, colored accent
    en_font = get_font(20)
    draw.text((padding, y), subtitle, fill=color, font=en_font)
    y += 45
    return y

def create_summary_box(draw, y, items, width, accent_color=ACCENT_ORANGE):
    """Create a summary box with dynamic height based on content"""
    sum_title_font = get_font(20)
    sum_font = get_font(18)
    line_height = 32

    # Calculate dynamic height
    title_height = 60  # title + padding
    content_height = 0
    for item in items:
        # Count lines for this item
        chars_per_line = int((width - 85) / (sum_font.size * 1.2))
        if chars_per_line < 8:
            chars_per_line = 8
        lines = textwrap.wrap(item, width=chars_per_line)
        content_height += len(lines) * line_height

    summary_h = title_height + content_height + 25  # extra padding at bottom
    if summary_h < 120:
        summary_h = 120

    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+summary_h+4], radius=12, fill=(0,0,0,20))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+summary_h], radius=12, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+10, y+summary_h], radius=5, fill=accent_color)

    sx = PADDING + 35
    sy = y + 18

    draw.text((sx, sy), "编辑点评", fill=TEXT_DARK, font=sum_title_font)
    sy += 40

    for item in items:
        chars_per_line = int((width - 85) / (sum_font.size * 1.2))
        if chars_per_line < 8:
            chars_per_line = 8
        lines = textwrap.wrap(item, width=chars_per_line)
        for line in lines:
            draw.text((sx, sy), line, fill=TEXT_GRAY, font=sum_font)
            sy += line_height

    return y + summary_h + 20

def create_footer(draw, page_num, total_pages, category, source):
    footer_y = HEIGHT - 75
    draw.line([PADDING, footer_y - 12, WIDTH - PADDING, footer_y - 12], fill=(200, 200, 200), width=1)

    small_font = get_font(15)
    draw.text((PADDING, footer_y), category, fill=TEXT_GRAY, font=small_font)

    page_text = f"{page_num:02d}/{total_pages:02d}"
    pw = 60
    draw.text((WIDTH - PADDING - pw, footer_y), page_text, fill=TEXT_GRAY, font=small_font)

    sw = 180
    draw.text(((WIDTH - sw) // 2, footer_y), source, fill=TEXT_GRAY, font=small_font)

def create_political_page():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    PADDING = 50
    CARD_RADIUS = 16
    CONTENT_WIDTH = WIDTH - 2 * PADDING

    y = PADDING
    y = create_page_header(draw, y, "2026年4月3日", "全球政治与地缘局势", "GEOPOLITICAL UPDATE", RED)

    # === MAIN NEWS CARD ===
    main_h = 260
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+main_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+main_h], radius=CARD_RADIUS, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+12, y+main_h], radius=6, fill=RED)

    cx = PADDING + 45
    card_content_width = CONTENT_WIDTH - 80
    cy = y + 25

    # Label - small colored tag
    label_font = get_font(16)
    draw.text((cx, cy), "地缘政治", fill=RED, font=label_font)
    cy += 32

    # Headline 1 - large, dark, bold
    h1_font = get_font(32)
    draw.text((cx, cy), "特朗普称美伊战争有望2-3周内结束", fill=TEXT_DARK, font=h1_font)
    cy += 52

    # Headline 2 - medium, dark
    h2_font = get_font(24)
    draw.text((cx, cy), "美伊局势出现转圜信号", fill=TEXT_GRAY, font=h2_font)
    cy += 45

    # Description - smaller, gray, wrapped
    desc_font = get_font(19)
    desc_height = draw_wrapped_text(draw, "特朗普表示无论是否达成和平协议，美国都可能在2-3周内结束对伊朗的军事打击，市场信心提振", cx, cy, card_content_width, desc_font, TEXT_GRAY)
    cy += desc_height + 10

    # Key fact - accent color highlight
    key_font = get_font(18)
    draw.text((cx, cy), "伊朗方面称未参与任何谈判，态度仍强硬", fill=RED, font=key_font)

    y += main_h + 28

    # === SECONDARY NEWS (2 cards) ===
    card2_h = 220
    col_w = (CONTENT_WIDTH - 25) // 2

    news2 = [
        {
            "label": "中东局势",
            "conclusion": "霍尔木兹海峡持续紧张",
            "detail": "伊朗严密控制霍尔木兹海峡，全球液化天然气供应受阻，已连续数周无运输船通过",
            "color": LIGHT_PURPLE
        },
        {
            "label": "国际斡旋",
            "conclusion": "特朗普暗示与伊谈判进展顺利",
            "detail": "特朗普称与伊朗的谈判正在非常顺利地进行，但伊朗方面否认正在进行实质性谈判",
            "color": LIGHT_BLUE
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

    # === MORE NEWS ===
    more_h = 115
    more_news = [
        ("北药拉格", "北约秘书长下周访美与特朗普会面", "讨论美国是否留在北约联盟问题", LIGHT_GREEN),
        ("国际关系", "美国解除部分对委内瑞拉制裁", "或反映中东政策调整动向", TEAL),
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

    # === SUMMARY ===
    y += 10
    summary_items = [
        "1. 特朗普释放撤军信号，但伊朗拒绝谈判，地缘风险仍存",
        "2. 霍尔木兹海峡封锁持续，全球能源供应面临压力",
        "3. 北约峰会临近，美国盟友关系走向受关注",
    ]
    y = create_summary_box(draw, y, summary_items, CONTENT_WIDTH)

    # === FOOTER ===
    create_footer(draw, 1, 3, "政治与地缘局势", "来源: Reuters/Economist/NPR")

    output_path = "/home/node/.openclaw/workspace/political_card_20260403.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")
    return output_path

def create_economy_page():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    PADDING = 50
    CARD_RADIUS = 16
    CONTENT_WIDTH = WIDTH - 2 * PADDING

    y = PADDING
    y = create_page_header(draw, y, "2026年4月3日", "全球经济与市场动态", "GLOBAL ECONOMY UPDATE", LIGHT_GREEN)

    # === MAIN NEWS CARD ===
    main_h = 260
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+main_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+main_h], radius=CARD_RADIUS, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+12, y+main_h], radius=6, fill=LIGHT_GREEN)

    cx = PADDING + 45
    card_content_width = CONTENT_WIDTH - 80
    cy = y + 25

    # Label - small colored tag
    label_font = get_font(16)
    draw.text((cx, cy), "市场动态", fill=LIGHT_GREEN, font=label_font)
    cy += 32

    # Headline 1 - large, dark
    h1_font = get_font(32)
    draw.text((cx, cy), "美伊局势缓和信号推升全球股市", fill=TEXT_DARK, font=h1_font)
    cy += 52

    # Headline 2 - medium, gray
    h2_font = get_font(24)
    draw.text((cx, cy), "科技股领涨，纳指大涨250点", fill=TEXT_GRAY, font=h2_font)
    cy += 45

    # Description - smaller, gray, wrapped
    desc_font = get_font(19)
    desc_height = draw_wrapped_text(draw, "特朗普暗示可能很快结束伊朗军事行动，全球市场情绪改善，亚洲和欧洲股市普遍上涨", cx, cy, card_content_width, desc_font, TEXT_GRAY)
    cy += desc_height + 10

    # Key fact - accent
    key_font = get_font(18)
    draw.text((cx, cy), "油价回落至100美元附近，投资级债券反弹", fill=LIGHT_GREEN, font=key_font)

    y += main_h + 28

    # === SECONDARY NEWS (2 cards) ===
    card2_h = 220
    col_w = (CONTENT_WIDTH - 25) // 2

    news2 = [
        {
            "label": "风险警示",
            "conclusion": "摩根大通警告油价飙升风险",
            "detail": "摩根大通策略师警告，若油价持续维持在90美元，标普500可能下跌10-15%，消费支出将受冲击",
            "color": RED
        },
        {
            "label": "经济数据",
            "conclusion": " Polymarket预测69.5%概率避免衰退",
            "detail": "预测市场显示美国经济软着陆概率较高，Q4 2025年GDP增长0.7%，通胀稳定在2.4%",
            "color": LIGHT_BLUE
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

    # === MORE NEWS ===
    more_h = 115
    more_news = [
        ("关税影响", "特朗普关税政策实施一周年", "分析称关税尚未达到预期效果，全球贸易格局生变", ACCENT_ORANGE),
        ("央行政策", "美联储维持利率3.5-3.75%不变", "2026年仅计划降息一次，货币政策保持审慎", TEAL),
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

    # === SUMMARY ===
    y += 10

    sum_title_font = get_font(20)
    sum_item_font = get_font(18)
    line_height = 32
    label_width = 50  # fixed width for numbers like "1. "

    # Calculate dynamic height based on content
    items = [
        "1. 美伊局势转圜短期提振市场，但根本矛盾未解",
        "2. 经济衰退风险有所缓解，但油价高企仍是潜在威胁",
        "3. 美联储按兵不动，货币政策空间留有余地",
    ]

    max_lines = 0
    for item in items:
        chars_per_line = int((CONTENT_WIDTH - 85) / (sum_item_font.size * 1.2))
        lines = textwrap.wrap(item, width=chars_per_line)
        if len(lines) > max_lines:
            max_lines = len(lines)

    summary_h = 60 + max_lines * line_height + 25
    if summary_h < 150:
        summary_h = 150

    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+summary_h+4], radius=12, fill=(0,0,0,20))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+summary_h], radius=12, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+10, y+summary_h], radius=5, fill=ACCENT_ORANGE)

    sx = PADDING + 35
    sy = y + 18

    draw.text((sx, sy), "编辑点评", fill=TEXT_DARK, font=sum_title_font)
    sy += 40

    for item in items:
        chars_per_line = int((CONTENT_WIDTH - 85) / (sum_item_font.size * 1.2))
        lines = textwrap.wrap(item, width=chars_per_line)
        for line in lines:
            draw.text((sx, sy), line, fill=TEXT_GRAY, font=sum_item_font)
            sy += line_height

    y = y + summary_h + 20

    # === FOOTER ===
    create_footer(draw, 2, 3, "经济与市场", "来源: Reuters/Bloomberg/Yahoo Finance")

    output_path = "/home/node/.openclaw/workspace/economy_card_20260403.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")
    return output_path

def create_summary_page():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    PADDING = 50
    CARD_RADIUS = 16
    CONTENT_WIDTH = WIDTH - 2 * PADDING

    y = PADDING

    # === HEADER ===
    date_font = get_font(22)
    draw.text((PADDING, y), "2026年4月3日", fill=TEXT_GRAY, font=date_font)
    y += 50

    title_font = get_font(48)
    draw.text((PADDING, y), "本期总结与展望", fill=TEXT_DARK, font=title_font)
    y += 62

    en_font = get_font(18)
    draw.text((PADDING, y), "WEEKLY INSIGHTS & OUTLOOK", fill=TEXT_GRAY, font=en_font)
    y += 50

    # === MAIN SUMMARY CARD ===
    main_h = 280
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+main_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+main_h], radius=CARD_RADIUS, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+12, y+main_h], radius=6, fill=ACCENT_ORANGE)

    cx = PADDING + 45
    cy = y + 25

    sum_title_font = get_font(24)
    draw.text((cx, cy), "核心要点", fill=TEXT_DARK, font=sum_title_font)
    cy += 45

    sum_font = get_font(20)
    items = [
        ("地缘政治", "美伊战争出现缓和迹象，特朗普暗示2-3周内可能撤军，但伊朗拒绝谈判，根本矛盾仍存"),
        ("市场反应", "美伊局势缓和预期推动全球股市上涨、油价回落，但能源危机风险未解除"),
        ("经济前景", "衰退概率有所下降，但油价高企和关税政策仍是隐忧，复苏道路不确定"),
    ]

    for label, content in items:
        label_font = get_font(20)
        sum_font = get_font(20)
        line_height = 30

        # Calculate how many lines content will wrap to
        content_width = CONTENT_WIDTH - 80 - label_font.getlength(label + "：")
        chars_per_line = int(content_width / (sum_font.size * 1.2))
        if chars_per_line < 8:
            chars_per_line = 8
        wrapped_lines = textwrap.wrap(content, width=chars_per_line)

        # Draw label at current cy
        draw.text((cx, cy), label + "：", fill=ACCENT_ORANGE, font=label_font)

        # Draw first line of content at same y as label
        first_line_y = cy
        draw.text((cx + label_font.getlength(label + "："), first_line_y), wrapped_lines[0], fill=TEXT_GRAY, font=sum_font)

        # Draw remaining lines
        for i in range(1, len(wrapped_lines)):
            cy += line_height
            draw.text((cx, cy), wrapped_lines[i], fill=TEXT_GRAY, font=sum_font)

        cy += line_height + 10

    y += main_h + 30

    # === OUTLOOK SECTION ===
    outlook_h = 220
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+outlook_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+outlook_h], radius=CARD_RADIUS, fill=WHITE)
    draw.rounded_rectangle([PADDING, y, PADDING+12, y+outlook_h], radius=6, fill=LIGHT_BLUE)

    cx = PADDING + 45
    cy = y + 25

    outlook_title_font = get_font(24)
    draw.text((cx, cy), "未来展望", fill=TEXT_DARK, font=outlook_title_font)
    cy += 45

    outlook_items = [
        ("需关注", "4月6日是特朗普设定的伊朗开放海峡最后期限，届时局势可能有新进展"),
        ("投资建议", "短期内市场波动可能加剧，建议关注能源板块和防御性资产"),
        ("长期趋势", "地缘政治重构将持续，全球供应链和贸易格局面临长期调整"),
    ]

    for label, content in outlook_items:
        outlook_label_font = get_font(20)
        outlook_content_font = get_font(20)
        line_height = 30

        # Calculate wrapped lines
        content_width = CONTENT_WIDTH - 80 - outlook_label_font.getlength(label + "：")
        chars_per_line = int(content_width / (outlook_content_font.size * 1.2))
        if chars_per_line < 8:
            chars_per_line = 8
        wrapped_lines = textwrap.wrap(content, width=chars_per_line)

        # Draw label at current cy
        draw.text((cx, cy), label + "：", fill=LIGHT_BLUE, font=outlook_label_font)

        # Draw first line of content at same y as label
        draw.text((cx + outlook_label_font.getlength(label + "："), cy), wrapped_lines[0], fill=TEXT_GRAY, font=outlook_content_font)

        # Draw remaining lines
        for i in range(1, len(wrapped_lines)):
            cy += line_height
            draw.text((cx, cy), wrapped_lines[i], fill=TEXT_GRAY, font=outlook_content_font)

        cy += line_height + 10

    y += outlook_h + 30

    # === KEY METRICS ===
    metrics_h = 120
    draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+metrics_h+4], radius=12, fill=(0,0,0,20))
    draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+metrics_h], radius=12, fill=WHITE)

    cx = PADDING + 30
    cy = y + 20

    metrics_title_font = get_font(20)
    draw.text((cx, cy), "关键数据一览", fill=TEXT_DARK, font=metrics_title_font)
    cy += 38

    metrics = [
        ("标普500", "≈5200", LIGHT_GREEN),
        ("原油价格", "≈$100/桶", RED),
        ("美联储利率", "3.5-3.75%", LIGHT_BLUE),
        ("衰退概率", "30.5%", ACCENT_ORANGE),
    ]

    mw = (CONTENT_WIDTH - 60) // 4
    for i, (name, value, color) in enumerate(metrics):
        mx = PADDING + 30 + i * mw

        name_font = get_font(16)
        draw.text((mx, cy), name, fill=TEXT_GRAY, font=name_font)

        value_font = get_font(22)
        draw.text((mx, cy + 30), value, fill=color, font=value_font)

    y += metrics_h + 20

    # === FOOTER ===
    create_footer(draw, 3, 3, "总结与展望", "来源: Reuters/Economist/Bloomberg")

    output_path = "/home/node/.openclaw/workspace/summary_card_20260403.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}")
    return output_path

if __name__ == "__main__":
    p1 = create_political_page()
    p2 = create_economy_page()
    p3 = create_summary_page()
    print("All pages created successfully!")
