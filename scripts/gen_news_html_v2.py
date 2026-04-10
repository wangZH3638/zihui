#!/usr/bin/env python3
"""HTML信息图生成器 v2 - 美观完整版"""

OUTPUT_PATH = "/home/node/.openclaw/workspace/minimax-output/今日科技要闻_20260403.html"

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>今日科技要闻 2026.04.03</title>
 <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
 <style>
 * {
 margin: 0;
 padding: 0;
 box-sizing: border-box;
 }

 body {
 font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
 background: linear-gradient(135deg, #faf9f7 0%, #f5f3f0 100%);
 min-height: 100vh;
 padding: 30px;
 }

 .container {
 max-width: 1200px;
 margin: 0 auto;
 background: #fffef9;
 border-radius: 24px;
 padding: 45px;
 box-shadow: 0 12px 50px rgba(0,0,0,0.1);
 position: relative;
 overflow: hidden;
 }

 /* 装饰背景 */
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
 width: 10px;
 height: 10px;
 border-radius: 50%;
 background: #e8e4dd;
 }

 .star {
 position: absolute;
 font-size: 18px;
 color: #d4a574;
 animation: twinkle 2.5s ease-in-out infinite;
 }

 @keyframes twinkle {
 0%, 100% { opacity: 0.5; transform: scale(1); }
 50% { opacity: 1; transform: scale(1.3); }
 }

 /* 标题区 */
 .header {
 text-align: center;
 margin-bottom: 45px;
 position: relative;
 }

 .header h1 {
 font-size: 48px;
 font-weight: 700;
 color: #2c3e50;
 margin-bottom: 12px;
 position: relative;
 display: inline-block;
 }

 .header h1::after {
 content: '';
 position: absolute;
 bottom: -8px;
 left: 50%;
 transform: translateX(-50%);
 width: 140px;
 height: 5px;
 background: linear-gradient(90deg, transparent, #f0b860, transparent);
 border-radius: 3px;
 }

 .header .date {
 font-size: 20px;
 color: #7f8c8d;
 margin-top: 20px;
 }

 .header .subtitle {
 font-size: 17px;
 color: #95a5a6;
 margin-top: 6px;
 }

 .tech-badge {
 display: inline-flex;
 align-items: center;
 gap: 10px;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 color: white;
 padding: 10px 28px;
 border-radius: 35px;
 font-size: 15px;
 font-weight: 500;
 margin-top: 18px;
 box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35);
 }

 /* 对比卡片区 */
 .comparison-section {
 display: grid;
 grid-template-columns: 1fr 1fr;
 gap: 35px;
 margin-bottom: 45px;
 }

 .news-card {
 background: #fff;
 border-radius: 20px;
 padding: 28px;
 border: 2px solid #f0ebe3;
 position: relative;
 transition: all 0.35s ease;
 }

 .news-card:hover {
 transform: translateY(-6px);
 box-shadow: 0 18px 35px rgba(0,0,0,0.12);
 }

 .news-card.card-left {
 border-left: 5px solid #3498db;
 }

 .news-card.card-right {
 border-left: 5px solid #e74c3c;
 }

 .card-header {
 display: flex;
 align-items: center;
 gap: 18px;
 margin-bottom: 22px;
 }

 .icon-circle {
 width: 65px;
 height: 65px;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 32px;
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
 font-size: 22px;
 font-weight: 700;
 color: #2c3e50;
 margin-bottom: 6px;
 }

 .card-title .tag {
 display: inline-block;
 padding: 4px 14px;
 border-radius: 15px;
 font-size: 13px;
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
 font-size: 15px;
 line-height: 1.9;
 margin-bottom: 22px;
 }

 .feature-list {
 list-style: none;
 }

 .feature-list li {
 display: flex;
 align-items: flex-start;
 gap: 12px;
 padding: 12px 0;
 border-bottom: 1px dashed #eee;
 font-size: 15px;
 color: #34495e;
 }

 .feature-list li:last-child {
 border-bottom: none;
 }

 .check-icon {
 width: 22px;
 height: 22px;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 13px;
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

 /* 数据区 */
 .data-section {
 background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
 border-radius: 20px;
 padding: 35px;
 margin-bottom: 45px;
 border: 2px solid #f0ebe3;
 }

 .data-section h3 {
 text-align: center;
 font-size: 26px;
 color: #2c3e50;
 margin-bottom: 30px;
 position: relative;
 }

 .data-section h3::before,
 .data-section h3::after {
 content: '✦';
 position: absolute;
 top: 50%;
 transform: translateY(-50%);
 color: #f0b860;
 font-size: 18px;
 }

 .data-section h3::before {
 left: calc(50% - 140px);
 }

 .data-section h3::after {
 right: calc(50% - 140px);
 }

 .data-grid {
 display: grid;
 grid-template-columns: repeat(4, 1fr);
 gap: 22px;
 }

 .data-item {
 text-align: center;
 padding: 25px 15px;
 background: white;
 border-radius: 14px;
 border: 2px solid #f0ebe3;
 transition: all 0.3s ease;
 }

 .data-item:hover {
 border-color: #f0b860;
 transform: translateY(-4px) scale(1.02);
 box-shadow: 0 8px 25px rgba(240, 184, 96, 0.2);
 }

 .data-number {
 font-size: 36px;
 font-weight: 700;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 -webkit-background-clip: text;
 -webkit-text-fill-color: transparent;
 background-clip: text;
 margin-bottom: 10px;
 }

 .data-label {
 font-size: 14px;
 color: #7f8c8d;
 margin-bottom: 6px;
 }

 .data-desc {
 font-size: 13px;
 color: #95a5a6;
 }

 /* 热点新闻 */
 .news-list-section {
 margin-bottom: 45px;
 }

 .news-list-section h3 {
 text-align: center;
 font-size: 26px;
 color: #2c3e50;
 margin-bottom: 30px;
 }

 .news-grid {
 display: grid;
 grid-template-columns: repeat(3, 1fr);
 gap: 22px;
 }

 .news-item {
 background: white;
 border-radius: 14px;
 padding: 22px;
 border: 2px solid #f0ebe3;
 position: relative;
 transition: all 0.3s ease;
 }

 .news-item:hover {
 border-color: #667eea;
 transform: translateY(-4px);
 box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
 }

 .news-item::before {
 content: attr(data-index);
 position: absolute;
 top: -12px;
 left: 18px;
 width: 30px;
 height: 30px;
 background: linear-gradient(135deg, #f0b860 0%, #e67e22 100%);
 color: white;
 border-radius: 50%;
 display: flex;
 align-items: center;
 justify-content: center;
 font-size: 15px;
 font-weight: 700;
 }

 .news-icon {
 font-size: 28px;
 margin-bottom: 12px;
 }

 .news-item h4 {
 font-size: 16px;
 color: #2c3e50;
 margin-bottom: 10px;
 line-height: 1.5;
 padding-top: 5px;
 }

 .news-item p {
 font-size: 13px;
 color: #7f8c8d;
 line-height: 1.7;
 }

 /* 底部 */
 .footer {
 text-align: center;
 padding-top: 35px;
 border-top: 2px dashed #eee;
 }

 .footer p {
 color: #95a5a6;
 font-size: 15px;
 }

 .footer .source {
 margin-top: 12px;
 font-size: 13px;
 color: #bdc3c7;
 }

 /* 响应式 */
 @media (max-width: 1024px) {
 .comparison-section { grid-template-columns: 1fr; }
 .data-grid { grid-template-columns: repeat(2, 1fr); }
 .news-grid { grid-template-columns: repeat(2, 1fr); }
 }

 @media (max-width: 768px) {
 .container { padding: 25px; }
 .header h1 { font-size: 32px; }
 .data-grid { grid-template-columns: 1fr; }
 .news-grid { grid-template-columns: 1fr; }
 }
 </style>
</head>
<body>
 <div class="container">
 <!-- 装饰 -->
 <div class="bg-decoration">
 <div class="dot" style="top: 12%; left: 6%;"></div>
 <div class="dot" style="top: 22%; right: 10%;"></div>
 <div class="dot" style="bottom: 28%; left: 4%;"></div>
 <div class="dot" style="bottom: 18%; right: 7%;"></div>
 <div class="dot" style="top: 50%; left: 3%;"></div>
 <div class="dot" style="top: 65%; right: 5%;"></div>
 <div class="star" style="top: 18%; right: 18%;">✦</div>
 <div class="star" style="top: 45%; left: 9%; animation-delay: 0.5s;">✦</div>
 <div class="star" style="bottom: 30%; right: 14%; animation-delay: 1s;">✦</div>
 <div class="star" style="bottom: 12%; left: 15%; animation-delay: 1.5s;">✦</div>
 </div>

 <!-- 标题 -->
 <div class="header">
 <h1>📰 今日科技要闻</h1>
 <p class="date">2026年4月3日 · 星期五</p>
 <p class="subtitle">聚焦全球科技创新动态</p>
 <div class="tech-badge">
 <span>🤖</span>
 <span>AI · 航天 · 芯片 · 新能源</span>
 </div>
 </div>

 <!-- 对比卡片 -->
 <div class="comparison-section">
 <!-- 左侧 -->
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
 <li><span class="check-icon">✓</span><span>探讨太空数据中心与地面算力协同方案</span></li>
 <li><span class="check-icon">✓</span><span>推动卫星互联网与AI算力融合发展</span></li>
 <li><span class="check-icon">✓</span><span>构建天地一体化算力网络新生态</span></li>
 </ul>
 </div>

 <!-- 右侧 -->
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
 <li><span class="check-icon">✓</span><span>50多年来首次载人绕月飞行</span></li>
 <li><span class="check-icon">✓</span><span>为2027年载人登月任务奠定基础</span></li>
 <li><span class="check-icon">✓</span><span>开启月球南极探索与资源勘探</span></li>
 </ul>
 </div>
 </div>

 <!-- 数据亮点 -->
 <div class="data-section">
 <h3>📊 今日数据亮点</h3>
 <div class="data-grid">
 <div class="data-item">
 <div class="data-number">460万+</div>
 <div class="data-label">A股3月新开户</div>
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
 <div class="data-desc">存储成本高位</div>
 </div>
 <div class="data-item">
 <div class="data-number">12家</div>
 <div class="data-label">数字人民币新增</div>
 <div class="data-desc">运营机构扩容</div>
 </div>
 </div>
 </div>

 <!-- 热点新闻 -->
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
 <p>比亚迪30万辆、奇瑞24万辆、吉利23.3万辆领跑新能源市场</p>
 </div>
 </div>
 </div>

 <!-- 底部 -->
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
