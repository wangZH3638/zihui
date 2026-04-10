#!/bin/bash
# HTML转图片脚本 - 在T2S上运行
# 需要先安装依赖: sudo apt-get install wkhtmltoimage

# 或者使用playwright（需要安装依赖）：
# sudo apt-get install libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libdbus-1-3 libcups2 libxkbcommon0 libasound2 libgbm1 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libatspi2.0-0

# 检查是否安装了wkhtmltoimage
if command -v wkhtmltoimage &> /dev/null; then
    echo "使用 wkhtmltoimage 截图..."
    wkhtmltoimage --quality 95 --width 1200 --disable-smart-width \
        --custom-header-propagation --enable-local-file-access \
        "$1" "$2"
    echo "完成: $2"
    exit 0
fi

# 检查是否有playwright
if command -v python3 &> /dev/null; then
    if python3 -c "import playwright" 2>/dev/null; then
        echo "使用 Playwright 截图..."
        python3 << 'PYEOF'
import asyncio
from playwright.async_api import async_playwright
import sys

async def screenshot(url, path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1200, 'height': 1600})
        await page.goto(f'file://{url}')
        await asyncio.sleep(2)  # 等待渲染
        await page.screenshot(path=path, full_page=True)
        await browser.close()
        print(f"截图已保存: {path}")

asyncio.run(screenshot(sys.argv[1], sys.argv[2]))
PYEOF
        exit 0
    fi
fi

echo "错误: 未找到截图工具"
echo "请先安装以下任一工具:"
echo ""
echo "方案1: wkhtmltoimage"
echo "  sudo apt-get install wkhtmltoimage"
echo ""
echo "方案2: Playwright + Chromium"
echo "  sudo apt-get install libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libdbus-1-3 libcups2 libxkbcommon0 libasound2 libgbm1 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libatspi2.0-0"
echo "  pip3 install playwright"
echo "  python3 -m playwright install chromium"
