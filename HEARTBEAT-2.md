# HEARTBEAT.md

## 每日备份检查
- 每天凌晨 3:00 检查是否需要备份
- 备份目标: `/home/node/.openclaw/workspace/backups/backup_YYYY-MM-DD_HHMMSS.tar.gz`
- 保留最近30天备份
- 手动执行备份: `bash /home/node/.openclaw/workspace/scripts/backup.sh`
