# 击剑升学系列 — Skill

> 项目工具与方法论 · 2026-04-09 整理（完整版）

---

## 工具清单

### HTML 卡片生成
- **模板路径**：`minimax-output/kcard-*.html`
- **截图脚本**：`/home/node/.openclaw/workspace/scripts/html_screenshot.py`
- **Chromium**：`~/.cache/ms-playwright/chromium-1208/chrome-linux/chrome`

### 截图命令
```bash
cd /home/node/.openclaw/workspace
python3 scripts/html_screenshot.py minimax-output/kcard-xxx.html minimax-output/kcard-xxx.png
```

### 截图参数（已确认）
- viewport：**800×1067**
- device_scale_factor：**2**
- 输出：**1600×2134px PNG**
- 截图后自动裁剪顶部/底部各2px白边

### 发送流程
1. 先发文字消息激活通道
2. 再发图片
3. 成功率更高

---

## 卡片类型与结构

### 钩子页（比例 45%/37%/18%）
- 大标题 75-85px
- 场景/问题描述
- 底部金句
- 留白多，制造悬念

### 内容页（比例 32%/52%/16%）
- 栏目标题（大号）
- 三栏内容（认知/边界/行动 或其他维度）
- 底部金句引言

---

## 文件命名规范

| 类型 | 命名格式 |
|------|----------|
| 钩子A | `kcard-hook-A.html` |
| 钩子B | `kcard-hook-B.html` |
| 路径总览 | `kcard-fencing-pathway.html` |
| 教育系统详解 | `kcard-article-03-education.html` |
| 体育系统详解 | `kcard-article-04-athletics.html` |
| 行动指南 | `kcard-action-guide.html` |

---

## 内容生成流程

1. 用户提供参考文档/链接
2. 分析内容结构，提取知识点
3. 设计钩子（金句/数据/场景）
4. 生成HTML → 截图 → 发送
5. 用户反馈 → 迭代调整

---

## 数据来源

### 教育系统 — 特长生
- 比赛：西安市中小学生击剑比赛
- 主办：西安市教育局 + 西安市体育局
- 资格：市级比赛前6名
- 用途：小升初/初升高，降分录取（普高线60%）

### 体育系统 — 运动员等级
- 比赛：陕西省青少年击剑冠军赛、陕西省青少年击剑锦标赛
- 主办：陕西省体育局
- 证书：一级/二级运动员等级证书
- 用途：高考体育单招（一级文化线可降30分）

---

## 相关文档路径

- 截图脚本：`/home/node/.openclaw/workspace/scripts/html_screenshot.py`
- 输出目录：`/home/node/.openclaw/workspace/minimax-output/`
- 设计规范索引：`memory/design-specs-index.md`
- 内容策略文档：`memory/fencing-knowledge-cards-series.md`
