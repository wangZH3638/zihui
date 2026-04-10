# 信息图系列 — Skill

> 项目工具与方法论 · 2026-04-09 整理（完整版）

---

## 工具清单

### HTML 信息图生成
- **模板**：`minimax-output/*-2026.html`
- **截图脚本**：`/home/node/.openclaw/workspace/scripts/html_screenshot.py`
- **必须使用全页截图模式**（full_page=True，不能用固定viewport）

### 数据获取

| 频道 | 获取方式 |
|------|----------|
| GitHub Trending | `curl github.com/trending` + json解析 |
| Reddit | `curl -s "https://www.reddit.com/r/popular.json?limit=10" -H "User-Agent: agent-reach/1.0"` |
| NBA | Bleacher Report（首选）+ nba.com + ESPN |
| NFL/MLB | Bleacher Report |
| 全球热点 | CBS News / AP News |
| 其他 | Tavily搜索 / Exa搜索 / web_search |

### 快捷命令

```bash
# Reddit热门
curl -s "https://www.reddit.com/r/popular.json?limit=10" -H "User-Agent: agent-reach/1.0"

# Tavily搜索
tavily_search(query, max_results=5)

# Exa搜索
mcporter call 'exa.web_search_exa(query: "query", numResults: 5)'
```

---

## 生成流程

1. 确认日期范围（哪个时间段的数据）
2. 获取数据源
3. 核实关键数据（球员/比分/排名）
4. 设计模块布局
5. 生成HTML → 全页截图 → 发送
6. 二次验证关键数据

---

## 8模块结构（最终版）

1. Hero/头条模块
2. 次头条模块
3. 热点A
4. 热点B
5. 数据统计/观点
6. 详细报道A
7. 详细报道B
8. **Jarvis分析评估（固定）** — 紫色[AI]主题，宏观/外交/内政/亮点 + 高/中/低评分

---

## 文件命名规范

`{内容类型}-2026.html`

示例：`nba-hot-topics-2026.html`、`github-trending-2026.html`、`global-news-2026.html`

---

## 相关文档

- `memory/infographic-strategy.md` — 信息图生成标准流程（2026-04-05确立）
- 截图脚本：`/home/node/.openclaw/workspace/scripts/html_screenshot.py`
