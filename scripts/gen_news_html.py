#!/usr/bin/env python3
"""HTML信息图生成器 - 参考MiniMax优雅设计"""

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/news_infographic.html"

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>今日科技要闻 2026.04.03</title>
 <style>
 * {
 margin: 0;
 padding: 0;
 box-sizing: border-box;
 }

 body {
 font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
 background: linear-gradient(135deg, #faf9f7 0%, #f5f3f0 100%);
 min-height: 100vh;
 padding: 20px;
 }

 .container {
 max-width: 1200px;
 margin: 0 auto;
 background: #fffef9;
 border-radius: 20px;
 padding: 40px;
 box-shadow: 0 10px 40px rgba(0,0,0,0.08);
 position: relative;
 overflow: hidden;
 }

 /* 装饰性背景 */
 .bg-decoration {
 position: absolute;
 top: 0;
 left: 0;
 right: 0;
 bottom: 0;
 pointer-events: none;
 overflow: hidden;
 }

 .dot {
 position: absolute;
 width: 8px;
 height: 8px;
 border-radius: 50%;
 background: #e8e4dd;
 }

 .star {
 position: absolute;
 color: #d4a574;
 font-size: 20px;
 animation: twinkle 2s ease-in-out infinite;
 }

 @keyframes twinkle {
 0%, 100% { opacity: 0.6; transform: scale(1); }
 50% { opacity: 1; transform: scale(1.2); }
 }

 /* 标题区域 */
 .header {
 text-align: center;
 margin-bottom: 40px;
 position: relative;
 }

 .header h1 {
 font-size: 42px;
 font-weight: 700;
 color: #2c3e50;
 margin-bottom: 10px;
 position: relative;
 display: inline-block;
 }

 .header h1::after {
 content: '';
 position: absolute;
 bottom: -5px;
 left: 50%;
 transform: translateX(-50%);
 width: 120px;
 height: 4px;
 background: linear-gradient(90deg, transparent, #f0b860, transparent);
 border-radius: 2px;
 }

 .header .date {
 font-size: 18px;
 color: #7f8c8d;
 margin-top: 15px;
 }

 .header .subtitle {
 font-size: 16px;
 color: #95a5a6;
 margin-top: 5px;
 }

 /* 核心技术标签 */
 .tech-badge {
 display: inline-flex;
 align-items: center;
 gap: 8px;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 color: white;
 padding: 8px 20px;
 border-radius: 30px;
 font-size: 14px;
 font-weight: 500;
 margin-top: 15px;
 }

 /* 对比区域 */
 .comparison-section {
 display: grid;
 grid-template-columns: 1fr 1fr;
 gap: 30px;
 margin-bottom: 40px;
 }

 .news-card {
 background: #fff;
 border-radius: 16px;
 padding: 25px;
 border: 2px solid #f0ebe3;
 position: relative;
 transition: all 0.3s ease;
 }

 .news-card:hover {
 transform: translateY(-5px);
 box-shadow: 0 15px 30px rgba(0,0,0,0.1);
 }

 .news-card.card-left {
 border-left: 4px solid #3498db;
 }

 .news-card.card-right {
 border-left: 4px solid #e74c3c;
 }

 .card-header {
 display: flex;
 align-items: center;
 gap: 15px;
 margin-bottom: 20px;
 }

 .icon-circle {
 width: 60px;
 height: 60px;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 28px;
 flex-shrink: 0;
 }

 .card-left .icon-circle {
 background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
 }

 .card-right .icon-circle {
 background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
 }

 .card-title {
 flex: 1;
 }

 .card-title h3 {
 font-size: 20px;
 font-weight: 700;
 color: #2c3e50;
 margin-bottom: 5px;
 }

 .card-title .tag {
 display: inline-block;
 padding: 3px 10px;
 border-radius: 12px;
 font-size: 12px;
 font-weight: 500;
 }

 .card-left .tag {
 background: #e3f2fd;
 color: #1976d2;
 }

 .card-right .tag {
 background: #ffebee;
 color: #c62828;
 }

 .card-description {
 color: #5d6d7e;
 font-size: 14px;
 line-height: 1.8;
 margin-bottom: 20px;
 }

 .feature-list {
 list-style: none;
 }

 .feature-list li {
 display: flex;
 align-items: flex-start;
 gap: 10px;
 padding: 10px 0;
 border-bottom: 1px dashed #eee;
 font-size: 14px;
 color: #34495e;
 }

 .feature-list li:last-child {
 border-bottom: none;
 }

 .check-icon {
 width: 20px;
 height: 20px;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 12px;
 flex-shrink: 0;
 margin-top: 2px;
 }

 .card-left .check-icon {
 background: #3498db;
 color: white;
 }

 .card-right .check-icon {
 background: #e74c3c;
 color: white;
 }

 /* 重要数据区 */
 .data-section {
 background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
 border-radius: 16px;
 padding: 30px;
 margin-bottom: 40px;
 border: 2px solid #f0ebe3;
 }

 .data-section h3 {
 text-align: center;
 font-size: 24px;
 color: #2c3e50;
 margin-bottom: 25px;
 position: relative;
 }

 .data-section h3::before,
 .data-section h3::after {
 content: '✦';
 position: absolute;
 top: 50%;
 transform: translateY(-50%);
 color: #f0b860;
 }

 .data-section h3::before {
 left: calc(50% - 120px);
 }

 .data-section h3::after {
 right: calc(50% - 120px);
 }

 .data-grid {
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 20px;
 }

 .data-item {
 text-align: center;
 padding: 20px;
 background: white;
 border-radius: 12px;
 border: 2px solid #f0ebe3;
 transition: all 0.3s ease;
 }

 .data-item:hover {
 border-color: #f0b860;
 transform: scale(1.05);
 }

 .data-number {
 font-size: 32px;
 font-weight: 700;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 -webkit-background-clip: text;
 -webkit-text-fill-color: transparent;
 background-clip: text;
 margin-bottom: 8px;
 }

 .data-label {
 font-size: 13px;
 color: #7f8c8d;
 }

 .data-desc {
 font-size: 12px;
 color: #95a5a6;
 margin-top: 5px;
 }

 /* 热点新闻列表 */
 .news-list-section {
 margin-bottom: 40px;
 }

 .news-list-section h3 {
 text-align: center;
 font-size: 24px;
 color: #2c3e50;
 margin-bottom: 25px;
 }

 .news-grid {
 display: grid;
 grid-template-columns: repeat(3, 1fr);
 gap: 20px;
 }

 .news-item {
 background: white;
 border-radius: 12px;
 padding: 20px;
 border: 2px solid #f0ebe3;
 position: relative;
 transition: all 0.3s ease;
 }

 .news-item:hover {
 border-color: #667eea;
 transform: translateY(-3px);
 }

 .news-item::before {
 content: attr(data-index);
 position: absolute;
 top: -10px;
 left: 15px;
 width: 28px;
 height: 28px;
 background: linear-gradient(135deg, #f0b860 0%, #e67e22 100%);
 color: white;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 14px;
 font-weight: 700;
 }

 .news-item h4 {
 font-size: 15px;
 color: #2c3e50;
 margin-bottom: 10px;
 line-height: 1.5;
 padding-top: 5px;
 }

 .news-item p {
 font-size: 12px;
 color: #7f8c8d;
 line-height: 1.6;
 }

 .news-icon {
 font-size: 24px;
 margin-bottom: 10px;
 }

 /* 底部信息 */
 .footer {
 text-align: center;
 padding-top: 30px;
 border-top: 2px dashed #eee;
 }

 .footer p {
 color: #95a5a6;
 font-size: 14px;
 }

 .footer .source {
 margin-top: 10px;
 font-size: 12px;
 color: #bdc3c7;
 }

 /* 手绘风格装饰 */
 .sketch-line {
 position: absolute;
 height: 3px;
 background: repeating-linear-gradient(
 90deg,
 #d4a574 0px,
 #d4a574 8px,
 transparent 8px,
 transparent 12px
 );
 border-radius: 2px;
 }

 .arrow {
 position: absolute;
 font-size: 24px;
 color: #d4a574;
 }

 /* 响应式 */
 @media (max-width: 1024px) {
 .comparison-section {
 grid-template-columns: 1fr;
 }

 .data-grid {
 grid-template-columns: repeat(2, 1fr);
 }

 .news-grid {
 grid-template-columns: repeat(2, 1fr);
 }
 }

 @media (max-width: 768px) {
 .container {
 padding: 20px;
 }

 .header h1 {
 font-size: 28px;
 }

 .data-grid {
 grid-template-columns: 1fr;
 }

 .news-grid {
 grid-template-columns: 1fr;
 }
 }
 </style>
</head>
<body>
 <div class="container">
 <!-- 装饰性背景 -->
 <div class="bg-decoration">
 <div class="dot" style="top: 10%; left: 5%;"></div>
 <div class="dot" style="top: 20%; right: 8%;"></div>
 <div class="dot" style="bottom: 30%; left: 3%;"></div>
 <div class="dot" style="bottom: 15%; right: 5%;"></div>
 <div class="star" style="top: 15%; right: 15%;">✦</div>
 <div class="star" style="top: 40%; left: 8%;">✦</div>
 <div class="star" style="bottom: 25%; right: 12%;">✦</div>
 </div>

 <!-- 标题区域 -->
 <div class="header">
 <h1>📰 今日科技要闻</h1>
 <p class="date">2026年4月3日 · 星期五</p>
 <p class="subtitle">聚焦全球科技创新动态</p>
 <div class="tech-badge">
 <span>🤖</span>
 <span>AI · 航天 · 芯片 · 新能源</span>
 </div>
 </div>

 <!-- 对比卡片区域 -->
 <div class="comparison-section">
 <!-- 左侧卡片 - 太空算力 -->
 <div class="news-card card-left">
 <div class="card-header">
 <div class="icon-circle">🚀</div>
 <div class="card-title">
 <h3>太空算力产业大会</h3>
 <span class="tag">航天科技</span>
 </div>
 </div>
 <p class="card-description">
 2026太空算力产业大会今日在北京经开区通明湖会展中心盛大开幕，大会主题"智算无界天地协同"，汇聚全球航天算力领域顶尖专家与企业代表。
 </p>
 <ul class="feature-list">
 <li>
 <span class="check-icon">✓</span>
 <span>探讨太空数据中心与地面算力协同方案</span>
 </li>
 <li>
 <span class="check-icon">✓</span>
 <span>推动卫星互联网与AI算力融合发展</span>
 </li>
 <li>
 <span class="check-icon">✓</span>
 <span>构建天地一体化算力网络新生态</span>
 </li>
 </ul>
 </div>

 <!-- 右侧卡片 - 美国重返月球 -->
 <div class="news-card card-right">
 <div class="card-header">
 <div class="icon-circle">🌙</div>
 <div class="card-title">
 <h3>美国重返月球</h3>
 <span class="tag">航天历史</span>
 </div>
 </div>
 <p class="card-description">
 "阿耳忒弥斯2号"载人绕月任务于4月1日成功升空，这是美国自1972年阿波罗17号以来首次载人飞向月球，标志着人类重返月球的新篇章。
 </p>
 <ul class="feature-list">
 <li>
 <span class="check-icon">✓</span>
 <span>50多年来首次载人绕月飞行</span>
 </li>
 <li>
 <span class="check-icon">✓</span>
 <span>为2027年载人登月任务奠定基础</span>
 </li>
 <li>
 <span class="check-icon">✓</span>
 <span>开启月球南极探索与资源勘探</span>
 </li>
 </ul>
 </div>
 </div>

 <!-- 数据亮点区域 -->
 <div class="data-section">
 <h3>📊 今日数据亮点</h3>
 <div class="data-grid">
 <div class="data-item">
 <div class="data-number">460万+</div>
 <div class="data-label">A股3月新开户数</div>
 <div class="data-desc">环比增长82.38%</div>
 </div>
 <div class="data-item">
 <div class="data-number">1300亿</div>
 <div class="data-label">国家电网Q1投资</div>
 <div class="data-desc">同比增长37%</div>
 </div>
 <div class="data-item">
 <div class="data-number">+500元</div>
 <div class="data-label">安卓手机涨价</div>
 <div class="data-desc">存储成本高位持续</div>
 </div>
 <div class="data-item">
 <div class="data-number">12家</div>
 <div class="data-label">数字人民币新增</div>
 <div class="data-desc">运营机构扩容</div>
 </div>
 </div>
 </div>

 <!-- 热点新闻列表 -->
 <div class="news-list-section">
 <h3>🔥 科技热点速递</h3>
 <div class="news-grid">
 <div class="news-item" data-index="1">
 <div class="news-icon">🔬</div>
 <h4>量子点显示技术突破</h4>
 <p>福州大学团队研发AR/VR超高分辨率量子点显示技术，论文发表于《自然》杂志</p>
 </div>
 <div class="news-item" data-index="2">
 <div class="news-icon">🤖</div>
 <h4>强人工智能临近</h4>
 <p>Anthropic报告称"强人工智能"或在2026年下半年至2027年成为现实</p>
 </div>
 <div class="news-item" data-index="3">
 <div class="news-icon">🏥</div>
 <h4>AI医疗联合实验室</h4>
 <p>蚂蚁健康与上海交大共建AI4Healthcare联合实验室，聚焦医疗专科智能体</p>
 </div>
 <div class="news-item" data-index="4">
 <div class="news-icon">🔋</div>
 <h4>移动电源安全国标</h4>
 <p>首部移动电源安全国标出台，电芯须通过针刺测试不起火不爆炸</p>
 </div>
 <div class="news-item" data-index="5">
 <div class="news-icon">📱</div>
 <h4>微信初代测试机</h4>
 <p>微信开发首版测试用苹果iPod touch曝光，将捐赠给计算机博物馆</p>
 </div>
 <div class="news-item" data-index="6">
 <div class="news-icon">🚗</div>
 <h4>3月汽车销量飘红</h4>
 <p>比亚迪超30万辆、奇瑞超24万辆、吉利23.3万辆领跑新能源市场</p>
 </div>
 </div>
 </div>

 <!-- 底部信息 -->
 <div class="footer">
 <p>📡 科技要闻，每日更新</p>
 <p class="source">数据来源：东方财富、36氪、IT之家、新浪科技等 · 2026.04.03</p>
 </div>
 </div>
</body>
</html>'''

def generate_html():
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(HTML_TEMPLATE)
    print(f"✅ HTML信息图已生成: {OUTPUT_PATH}")
    return OUTPUT_PATH

if __name__ == "__main__":
    generate_html()
