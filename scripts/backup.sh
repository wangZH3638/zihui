#!/bin/bash
# Jarvis 每日备份脚本
# 每天凌晨3点执行，备份关键数据并同步到 GitHub

BACKUP_DIR="/home/node/.openclaw/workspace/backups"
WORKSPACE="/home/node/.openclaw/workspace"
DATE=$(date +%Y-%m-%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${DATE}.tar.gz"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份 workspace 文件
tar -czf $BACKUP_FILE \
    $WORKSPACE/MEMORY.md \
    $WORKSPACE/AGENTS.md \
    $WORKSPACE/USER.md \
    $WORKSPACE/SOUL.md \
    $WORKSPACE/TOOLS.md \
    $WORKSPACE/HEARTBEAT.md \
    $WORKSPACE/memory/ \
    $WORKSPACE/obsidian/ \
    $WORKSPACE/config/ 2>/dev/null

# 保留最近30天的备份
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +30 -delete

echo "[$(date)] Backup completed: $BACKUP_FILE"

# 同步到 GitHub
cd $WORKSPACE
git config user.email "wangzh@example.com" 2>/dev/null
git config user.name "Jarvis" 2>/dev/null
git add backups/
git commit -m "每日备份 $(date +%Y-%m-%d_%H%M%S)" 2>/dev/null
git push origin master 2>/dev/null

echo "[$(date)] GitHub sync completed"
