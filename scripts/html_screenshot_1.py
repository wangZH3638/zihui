#!/usr/bin/env python3
"""HTML文件转PNG图片 - 使用Playwright，支持全页截图"""

import asyncio
import sys
import os
from PIL import Image

async def screenshot_html(html_path, output_path):
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=os.path.expanduser("~/.cache/ms-playwright/chromium-1208/chrome-linux/chrome")
        )
        
        page = await browser.new_page(viewport={'width': 800, 'height': 1067}, device_scale_factor=2)
        
        file_url = f'file://{os.path.abspath(html_path)}'
        
        # 禁用字体加载避免超时
        await page.route("**/*.css", lambda route: route.abort() if "fonts.googleapis" in route.request.url else route.continue_())
        await page.route("**/fonts.gstatic.com/**", lambda route: route.abort())
        
        await page.goto(file_url, wait_until='networkidle')
        await asyncio.sleep(0.5)
        
        # 全页截图
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()
    
    # 后处理：裁剪掉顶部和底部各2px的白边
    if os.path.exists(output_path):
        try:
            img = Image.open(output_path)
            w, h = img.size
            # 裁剪顶部和底部各2px
            if h > 4:
                img_cropped = img.crop((0, 2, w, h - 2))
                img_cropped.save(output_path)
        except Exception as e:
            print(f"裁剪失败: {e}")
    
    print(f"✅ 截图已保存: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 html_screenshot.py <html文件> <输出图片>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(html_file):
        print(f"错误: 文件不存在 {html_file}")
        sys.exit(1)
    
    asyncio.run(screenshot_html(html_file, output_file))
