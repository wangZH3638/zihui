# 知识库 — Skill

> Obsidian维护工具与方法论 · 2026-04-09 整理（完整版）

---

## 核心工具

### Obsidian CLI
- 工具：`/home/node/.openclaw/workspace/skills/obsidian-cli/SKILL.md`
- 功能：读写笔记、搜索、管理

### GitHub双向同步
- 本地：`/home/node/.openclaw/workspace/obsidian/obsidian-vault/`
- GitHub：`wangZH3638/zihui`
- 同步方式：git push/pull

### 快捷操作

```bash
# 在obsidian目录下
git add .
git commit -m "更新描述"
git push

# 拉取
git pull origin main
```

---

## 文件结构（基于Karpathy LLM Wiki模式）

```
obsidian-vault/
├── CLAUDE.md     # 知识库说明书（schema）
├── log.md        # 操作日志（追加only）
├── index.md      # wiki总索引
├── wiki/         # AI整理的知识页面（完全由AI维护）
│   ├── fencing-two-pathways.md
│   ├── 运动员的底色.md
│   ├── 你也懂点心理学-项目笔记.md
│   ├── 西安中小学生击剑比赛.md
│   ├── 陕西省青少年击剑冠军赛.md
│   └── 陕西省青少年击剑锦标赛.md
├── ref/          # 参考文档（用户提供的原始资料）
│   ├── 你也懂点心理学-知识点参考文档-DSM5诊断标准.md
│   └── 你也懂点心理学-内容策划文档.md
├── raw/          # 原始素材（永远不修改）
├── smart-collect/  # 网页收藏
└── outputs/      # AI生成的研究报告
```

---

## 工作流

### Ingest（摄入新素材）
1. 把源文件放入 `raw/`
2. 告诉AI："帮我处理这个素材"
3. AI会：读取 → 提炼要点 → 更新wiki → 更新index → 追加log

### Query（查询知识库）
1. 直接问问题
2. AI先读index.md定位相关页面
3. 综合wiki内容给出回答
4. 好答案存入outputs/，有价值的结论移入wiki/

---

## 页面类型

### Wiki页面（`wiki/`）
- 概念、对比、实体描述
- 使用双链语法 `[[页面名]]`
- 顶部标注来源和日期
- 每个文件**必须以一段摘要开头**（50字内）

### 参考文档（`ref/`）
- 原始参考资料
- 用户提供的文档
- 策划文档

---

## 内容维护流程

1. **及时记录**：讨论中的重要决策、偏好、教训，当天记入 `memory/YYYY-MM-DD.md`
2. **定期蒸馏**：从memory/蒸馏到MEMORY.md和项目知识库
3. **双向链接**：相关内容互相链接，形成知识网络
4. **标注来源**：每条重要信息标注来源和日期

---

## 自动整理

### autoDream 脚本
- 路径：`/home/node/.openclaw/workspace/scripts/auto_dream.sh`
- 功能：扫描memory/目录，提取[决策]/[教训]/[偏好]/[待办]
- **注意**：需要在T2S宿主机配置cron（容器内无crontab）

### autoDream cron配置（待完成）
- 在T2S宿主机配置：
  ```
  0 9 * * 1 bash /home/node/.openclaw/workspace/scripts/auto_dream.sh
  ```

---

## 索引维护

每次重要更新后更新 `wiki/index.md`，记录：
- 所有wiki页面和描述
- 参考文档列表
- 最后更新时间
