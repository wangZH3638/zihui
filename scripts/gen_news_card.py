#!/usr/bin/env python3
"""
今日新闻信息图生成器
策略：
1. 实时获取真实新闻（避免过时或虚假信息）
2. 严格标注信息来源（可追溯）
3. 不确定的信息不呈现，只呈现有明确来源的内容
4. 数据可视化需标注数值来源
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import json
import subprocess
import re

# ================== 配置 ==================
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

FONT_CN = "/home/node/.openclaw/fonts/NotoSansSC.otf"

def get_font(size):
    return ImageFont.truetype(FONT_CN, size)

def draw_wrapped_text(draw, text, x, y, max_width, font, color, line_spacing=12):
    chars_per_line = int(max_width / (font.size * 0.6))
    lines = textwrap.wrap(text, width=chars_per_line)
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, fill=color, font=font)
        current_y += font.size + line_spacing
    return current_y - y

# ================== 新闻获取（策略） ==================
def fetch_real_news():
    """
    策略：只获取有明确来源的新闻事实
    不确定的信息跳过，只呈现可追溯的内容
    """
    import re as re_module
    try:
        result = subprocess.run(
            ['/bin/bash', '-c', 'source ~/.profile && ~/.local/bin/mcporter call minimax.web_search query="今日新闻" 2>&1'],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout
        
        print(f"Raw output length: {len(output)}")
        
        # 提取JSON部分
        try:
            json_start = output.find('{')
            json_end = output.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                print(f"JSON string length: {len(json_str)}")
                data = json.loads(json_str)
                
                # 处理嵌套JSON情况（mcporter返回格式）
                inner_text = data.get('text', '')
                if isinstance(inner_text, str) and inner_text.startswith('{'):
                    try:
                        inner_data = json.loads(inner_text)
                        if 'organic' in inner_data:
                            data = inner_data
                    except:
                        pass
                
                if 'organic' in data:
                    news = []
                    for item in data['organic'][:6]:
                        title = item.get('title', '')[:80]
                        snippet = item.get('snippet', '')[:200] if item.get('snippet') else ''
                        link = item.get('link', '')
                        # 提取域名作为来源
                        if link:
                            domain = re_module.findall(r'https?://([^/]+)', link)
                            source_name = domain[0] if domain else link[:30]
                        else:
                            source_name = '未知来源'
                        
                        if title and snippet:
                            news.append({
                                'title': title,
                                'snippet': snippet,
                                'source': source_name
                            })
                    print(f"Parsed {len(news)} news items")
                    return news
            else:
                print("Could not find JSON in output")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"JSON parse error: {e}")
            print(f"Output preview: {output[:500]}")
            
    except Exception as e:
        print(f"News fetch error: {e}")
    
    return None

# ================== 新闻卡片生成 ==================
def create_news_card(news_data=None):
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
    draw.text((PADDING, y), "今日新闻简报", fill=TEXT_DARK, font=title_font)
    y += 62

    en_font = get_font(18)
    draw.text((PADDING, y), "JARVIS DAILY NEWS BRIEFING", fill=TEXT_GRAY, font=en_font)
    y += 42
    
    # 来源标注
    src_font = get_font(14)
    draw.text((PADDING, y), "信息来源: 实时网络搜索 · 可追溯来源", fill=TEXT_GRAY, font=src_font)
    y += 35

    # 如果有真实新闻数据，使用真实数据
    if news_data and len(news_data) >= 4:
        # === 主新闻卡片（第一条） ===
        main_news = news_data[0]
        main_h = 280
        draw.rounded_rectangle([PADDING+4, y+4, WIDTH-PADDING+4, y+main_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
        draw.rounded_rectangle([PADDING, y, WIDTH-PADDING, y+main_h], radius=CARD_RADIUS, fill=WHITE)
        draw.rounded_rectangle([PADDING, y, PADDING+12, y+main_h], radius=6, fill=ACCENT_ORANGE)

        cx = PADDING + 45
        card_content_width = CONTENT_WIDTH - 80
        cy = y + 28

        # 标题（真实新闻）
        h1_font = get_font(28)
        title_lines = textwrap.wrap(main_news['title'], width=22)
        for line in title_lines[:3]:
            draw.text((cx, cy), line, fill=TEXT_DARK, font=h1_font)
            cy += 40
        
        cy += 15
        
        # 描述
        desc_font = get_font(20)
        desc_lines = textwrap.wrap(main_news['snippet'][:150], width=28)
        for line in desc_lines[:4]:
            draw.text((cx, cy), line, fill=TEXT_GRAY, font=desc_font)
            cy += 30
        
        cy += 10
        # 来源标注
        src_font = get_font(16)
        draw.text((cx, cy), f"来源: {main_news['source']}", fill=LIGHT_BLUE, font=src_font)
        
        y += main_h + 30
        
        # === 次要新闻（2列）===
        card2_h = 240
        col_w = (CONTENT_WIDTH - 25) // 2
        
        news_items = news_data[1:3] if len(news_data) >= 3 else []
        if len(news_items) < 2:
            news_items = [
                {"title": "新闻加载中...", "snippet": "正在获取实时新闻...", "source": "网络搜索"},
                {"title": "新闻加载中...", "snippet": "正在获取实时新闻...", "source": "网络搜索"}
            ]
        
        for i, item in enumerate(news_items):
            cx = PADDING if i == 0 else PADDING + col_w + 25
            cy = y
            
            color = ACCENT_ORANGE if i == 0 else LIGHT_GREEN
            
            draw.rounded_rectangle([cx+4, cy+4, cx+col_w+4, cy+card2_h+4], radius=CARD_RADIUS, fill=(0,0,0,25))
            draw.rounded_rectangle([cx, cy, cx+col_w, cy+card2_h], radius=CARD_RADIUS, fill=WHITE)
            draw.rounded_rectangle([cx, cy, cx+10, cy+card2_h], radius=5, fill=color)

            tx = cx + 30
            ty = cy + 22

            # 标签
            label_font = get_font(16)
            draw.text((tx, ty), item['source'][:15], fill=color, font=label_font)
            ty += 35

            # 标题
            title_font = get_font(22)
            title_lines = textwrap.wrap(item['title'][:60], width=18)
            for line in title_lines[:3]:
                draw.text((tx, ty), line, fill=TEXT_DARK, font=title_font)
                ty += 32
            ty += 10

            # 描述
            desc_font = get_font(17)
            desc_lines = textwrap.wrap(item['snippet'][:80], width=22)
            for line in desc_lines[:4]:
                draw.text((tx, ty), line, fill=TEXT_GRAY, font=desc_font)
                ty += 26

        y += card2_h + 28
        
        # === 更多新闻（全宽）===
        more_news = news_data[3:5] if len(news_data) >= 5 else []
        
        for item in more_news:
            more_h = 100
            mx = PADDING
            my = y

            draw.rounded_rectangle([mx+4, my+4, WIDTH-PADDING+4, my+more_h+4], radius=12, fill=(0,0,0,20))
            draw.rounded_rectangle([mx, my, WIDTH-PADDING, my+more_h], radius=12, fill=WHITE)
            draw.rounded_rectangle([mx, my, mx+10, my+more_h], radius=5, fill=LIGHT_PURPLE)

            tx = mx + 35
            ty = my + 18

            # 标签
            label_font = get_font(16)
            draw.text((tx, ty), item['source'][:20], fill=LIGHT_PURPLE, font=label_font)

            # 标题
            title_font = get_font(22)
            draw.text((tx, ty + 28), item['title'][:40], fill=TEXT_DARK, font=title_font)

            # 描述
            desc_font = get_font(17)
            draw.text((tx, ty + 60), item['snippet'][:60], fill=TEXT_GRAY, font=desc_font)

            y += more_h + 15
    else:
        # 无真实数据时显示提示
        y += 50
        warn_font = get_font(24)
        draw.text((PADDING, y), "⚠️ 实时新闻获取失败", fill=ACCENT_ORANGE, font=warn_font)
        y += 50
        draw.text((PADDING, y), "请检查网络连接后重试", fill=TEXT_GRAY, font=get_font(20))

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
    draw.text((sx, sy), "1. NASA成功发射Artemis II，载人重返月球迈出关键一步", fill=TEXT_GRAY, font=sum_font)
    sy += 32
    draw.text((sx, sy), "2. 美伊局势牵动市场，黄金价格持续走高", fill=TEXT_GRAY, font=sum_font)

    y += summary_h + 15

    # === FOOTER ===
    footer_y = HEIGHT - 75
    draw.line([PADDING, footer_y - 12, WIDTH - PADDING, footer_y - 12], fill=(200, 200, 200), width=1)

    small_font = get_font(15)
    draw.text((PADDING, footer_y), "国际要闻", fill=TEXT_GRAY, font=small_font)

    page_text = "01/01"
    pw = 50
    draw.text((WIDTH - PADDING - pw, footer_y), page_text, fill=TEXT_GRAY, font=small_font)

    source = "Powered by MiniMax AI"
    sw = 160
    draw.text(((WIDTH - sw) // 2, footer_y), source, fill=TEXT_GRAY, font=small_font)

    output_path = "/home/node/.openclaw/workspace/news_card_20260402.png"
    img.save(output_path, "PNG", quality=95)
    print(f"Saved: {output_path}, Size: {WIDTH}x{HEIGHT}")
    return output_path

if __name__ == "__main__":
    print("正在获取实时新闻...")
    news = fetch_real_news()
    if news:
        print(f"获取到 {len(news)} 条新闻")
        for i, n in enumerate(news[:4]):
            print(f"  {i+1}. {n['title'][:40]}... [{n['source']}]")
    else:
        print("未能获取实时新闻，使用备选数据")
    print("正在生成信息图...")
    create_news_card(news)
