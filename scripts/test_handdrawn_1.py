#!/usr/bin/env python3
"""Test hand-drawn style icons"""
from PIL import Image, ImageDraw, ImageFont
import random
import math

WIDTH = 800
HEIGHT = 600
BG_COLOR = (255, 255, 255)
ACCENT = (232, 93, 4)
TEXT_DARK = (45, 45, 45)

def draw_handdrawn_circle(draw, cx, cy, radius, color, width=3):
    """Draw a hand-drawn style circle (not perfect)"""
    points = []
    num_points = 36
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        # Add slight randomness to make it look hand-drawn
        r = radius + random.randint(-2, 2)
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        points.append((x, y))
    
    # Draw as a series of short line segments with varying thickness
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        # Vary the line width slightly
        w = width + random.randint(-1, 1)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=max(1, w))

def draw_handdrawn_rect(draw, x, y, w, h, color, width=3):
    """Draw a hand-drawn style rectangle"""
    # Top line
    for i in range(w):
        offset = random.randint(-1, 1)
        draw.line([(x + i, y + offset), (x + i + 1, y + offset)], fill=color, width=width)
    # Right line
    for i in range(h):
        offset = random.randint(-1, 1)
        draw.line([(x + w + offset, y + i), (x + w + offset, y + i + 1)], fill=color, width=width)
    # Bottom line
    for i in range(w):
        offset = random.randint(-1, 1)
        draw.line([(x + i, y + h + offset), (x + i + 1, y + h + offset)], fill=color, width=width)
    # Left line
    for i in range(h):
        offset = random.randint(-1, 1)
        draw.line([(x + offset, y + i), (x + offset, y + i + 1)], fill=color, width=width)

def draw_simple_mountain(draw, cx, cy, size, color):
    """Draw a simple mountain shape"""
    # Triangle for mountain
    points = [
        (cx, cy - size),
        (cx - size, cy + size),
        (cx + size, cy + size)
    ]
    # Add some wobble
    wobbled = [(x + random.randint(-2, 2), y + random.randint(-2, 2)) for x, y in points]
    draw.polygon(wobbled, fill=color)

def draw_simple_chart(draw, x, y, width, height, color):
    """Draw a simple bar chart icon"""
    bar_width = width // 4
    gap = 4
    heights = [0.6, 0.9, 0.5, 0.8]
    
    for i, h in enumerate(heights):
        bx = x + i * (bar_width + gap)
        by = y + height - int(height * h)
        bh = int(height * h)
        # Add slight wobble to bars
        for j in range(bar_width):
            offset = random.randint(-1, 1)
            draw.line([(bx + j, by + offset), (bx + j, by + bh)], fill=color, width=2)

def draw_simple_rocket(draw, cx, cy, size, color):
    """Draw a simple rocket icon"""
    # Body
    body_points = [
        (cx, cy - size),  # nose
        (cx - size//2, cy + size//2),
        (cx + size//2, cy + size//2)
    ]
    wobbled = [(x + random.randint(-1, 1), y + random.randint(-1, 1)) for x, y in body_points]
    draw.polygon(wobbled, fill=color)
    
    # Flames
    flame_y = cy + size//2 + 5
    for i in range(3):
        fx = cx + random.randint(-5, 5)
        draw.line([(cx, flame_y), (fx, flame_y + 10 + random.randint(0, 5))], fill=(255, 100, 0), width=3)

def draw_simple_globe(draw, cx, cy, radius, color):
    """Draw a simple globe/world icon"""
    draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], outline=color, width=3)
    # Horizontal line
    draw.line([(cx-radius, cy), (cx+radius, cy)], fill=color, width=2)
    # Vertical ellipse
    draw.ellipse([cx-radius//2, cy-radius, cx+radius//2, cy+radius], outline=color, width=2)

def draw_simple_money(draw, cx, cy, size, color):
    """Draw a simple dollar/money icon"""
    # Circle
    draw.ellipse([cx-size, cy-size, cx+size, cy+size], outline=color, width=3)
    # Dollar sign
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    draw.text((cx - size//3, cy - size//2), "$", fill=color, font=font)

def test_handdrawn():
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Test icons at different positions
    icons = [
        ("Circle", draw_handdrawn_circle, (100, 150, 40)),
        ("Rectangle", draw_handdrawn_rect, (250, 110, 80, 80)),
        ("Mountain", draw_simple_mountain, (400, 150, 40)),
        ("Chart", draw_simple_chart, (550, 100, 80, 80)),
        ("Rocket", draw_simple_rocket, (100, 350, 30)),
        ("Globe", draw_simple_globe, (250, 350, 40)),
        ("Money", draw_simple_money, (400, 350, 35)),
    ]
    
    for name, func, args in icons:
        func(draw, *args, ACCENT)
        draw.text((args[0] - 20, args[1] + args[2] + 10 if len(args) > 2 else args[1] + 50), name, fill=TEXT_DARK)
    
    # Add title
    font = ImageFont.truetype("/home/node/.openclaw/fonts/NotoSansSC.otf", 32)
    draw.text((50, 50), "手绘风格图标测试", fill=TEXT_DARK, font=font)
    
    img.save("/home/node/.openclaw/workspace/handdrawn_test.png", "PNG")
    print("Saved: handdrawn_test.png")

test_handdrawn()
