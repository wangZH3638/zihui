# 你也懂点心理学 — Skill

> 项目工具与方法论 · 2026-04-09 整理（完整版）

---

## 工具清单

### HTML 卡片生成
- **模板**：`minimax-output/psychology-card-*.html`
- **截图脚本**：`/home/node/.openclaw/workspace/scripts/html_screenshot.py`
- **Chromium**：`~/.cache/ms-playwright/chromium-1208/chrome-linux/chrome`

### 截图命令
```bash
cd /home/node/.openclaw/workspace
python3 scripts/html_screenshot.py minimax-output/psychology-card-01.html minimax-output/psychology-card-01.png
```

### 截图参数
- viewport：**800×1067**
- device_scale_factor：**2**
- 输出：**1600×2134px PNG**

---

## 卡片结构（12张）

### 开篇引流卡（01）
- 系列名徽章置顶
- 主标题钩子
- 3个核心信号卡片
- 系列介绍模块
- 三问承诺
- 系列info pills（12张/10种/A-B-C三簇）
- CTA互动框

### 人格障碍类型卡（02-11）
- 系列徽章 + 类型标注
- 主标题（类型名 + 简称旁注）
- 3个行为信号卡片（编号+标题+描述）
- 影视原型框
- 小提醒金句
- 互动CTA

### 投票结尾卡（12）
- 总结10种人格判断要点
- 投票互动引导
- 下期预告钩子（点赞最高类型出沟通指南）

---

## 每张独立accent色

| 类型 | accent色 | 备注 |
|------|----------|------|
| 偏执型 | `#e94560` 红 | 警示 |
| 分裂样 | `#888888` 灰 | 冷漠 |
| 分裂型 | `#9945ff` 紫 | 怪异 |
| 边缘型 BPD | `#ff6b35` 橙 | 情绪波动 |
| 自恋型 | `#ffd700` 金 | 自我神化 |
| 表演型 | `#ff69b4` 粉 | 夸张戏剧 |
| 反社会型 ASPD | `#1a1a1a` 黑 | 无道德底线 |
| 回避型 | `#4a9eff` 蓝 | 退缩 |
| 依赖型 | `#ff9966` 暖橙 | 依附 |
| 强迫型 OCPD | `#2d8a4e` 绿 | 控制 |

---

## 文件命名规范

| 类型 | 命名 |
|------|------|
| 开篇 | `psychology-card-01.html` |
| 偏执型 | `psychology-card-02.html` |
| 分裂样 | `psychology-card-03.html` |
| 分裂型 | `psychology-card-04.html` |
| 边缘型 | `psychology-card-05.html` |
| 自恋型 | `psychology-card-06.html` |
| 表演型 | `psychology-card-07.html` |
| 反社会型 | `psychology-card-08.html` |
| 回避型 | `psychology-card-09.html` |
| 依赖型 | `psychology-card-10.html` |
| 强迫型 | `psychology-card-11.html` |
| 投票结尾 | `psychology-card-12.html` |

---

## 内容来源

- DSM-5 10种人格障碍诊断标准（北京市卫生健康委员会权威解读）
- 每类3个行为信号，对应DSM-5核心症状
- 影视原型精准匹配（每部影视标注对应DSM-5症状）

---

## 参考文献

- `obsidian/ref/你也懂点心理学-知识点参考文档-DSM5诊断标准.md`
- `obsidian/ref/你也懂点心理学-内容策划文档.md`
