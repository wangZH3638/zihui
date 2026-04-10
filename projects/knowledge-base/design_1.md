# 知识库 — 设计规范

> Obsidian结构标准 · 2026-04-09 整理（完整版）

---

## 知识库定位

基于 **Karpathy LLM Wiki模式** 构建的个人知识库，涵盖击剑教育、升学规划、心理学等领域的资料收集与整理。

---

## 文件夹结构

```
obsidian-vault/
├── CLAUDE.md            # 知识库说明书（schema）
├── log.md               # 操作日志（追加only）
├── index.md             # wiki总索引
├── wiki/                # AI整理的知识页面
│   ├── index.md         # 知识库总索引
│   ├── fencing-two-pathways.md
│   ├── 运动员的底色.md
│   ├── 你也懂点心理学-项目笔记.md
│   ├── 西安中小学生击剑比赛.md
│   ├── 陕西省青少年击剑冠军赛.md
│   └── 陕西省青少年击剑锦标赛.md
├── ref/                  # 参考文档（原始资料）
│   ├── 你也懂点心理学-知识点参考文档-DSM5诊断标准.md
│   └── 你也懂点心理学-内容策划文档.md
├── raw/                  # 原始素材（永远不修改）
├── smart-collect/        # 网页收藏
└── outputs/              # AI生成的研究报告
```

---

## 命名规范

- Wiki页面：kebab-case或描述性中文，如 `fencing-two-pathways.md`
- 参考文档：`{项目名}-{文档类型}.md`
- 避免特殊字符和空格
- 格式：`.md`

---

## Wiki页面模板

```markdown
# 页面标题

> 来源 · 日期
> 一段50字内的摘要

## 概述
...

## 详细内容
...

## 相关页面
- [[关联页面]]

---

标签：#标签1 #标签2
```

---

## frontmatter（可选）

```yaml
---
uid: xxx
created: YYYY-MM-DD
modified: YYYY-MM-DD
tags: [tag1, tag2]
---
```

---

## 双链语法

- 链接到其他wiki页面：`[[页面名]]`
- 链接到标题：`[[页面名#标题]]`
- 悬停预览：Obsidian自动支持

---

## 用户偏好

- **简洁扁平**：不要花哨插件
- **优先内容**：结构清晰，内容为王
- **双向链接**：相关页面互相链接，形成知识网络

---

## GitHub同步

- 本地仓库：跟随workspace
- GitHub仓库：wangZH3638/zihui
- 同步频率：重要更新后及时push
