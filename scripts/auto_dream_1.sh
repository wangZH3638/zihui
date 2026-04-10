#!/bin/bash
#===============================================================================
# auto_dream.sh - Claw Code-inspired idle memory consolidation
# 
# Based on Claw Code's autoDream机制: idle-time memory analysis that:
#   1. Reads recent daily memory logs (7-30 days)
#   2. Extracts key decisions, lessons, and pending work
#   3. Updates MEMORY.md with distilled insights
#   4. Archives old daily logs
#
# Usage: Run via cron (weekly recommended) or manually
#   cron: 0 9 * * 1 bash /home/node/.openclaw/workspace/scripts/auto_dream.sh
#===============================================================================

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE}/memory"
MEMORY_FILE="${WORKSPACE}/MEMORY.md"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="${MEMORY_DIR}/auto_dream.log"

# Config
DAYS_TO_PROCESS=30      # How many days back to analyze
ARCHIVE_AFTER_DAYS=60   # Archive logs older than this
PRESERVE_RECENT_DAYS=7  # Keep these days intact

# Ensure memory dir exists
mkdir -p "${MEMORY_DIR}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "${LOG_FILE}"
}

log "=== autoDream started ==="

# Check if memory directory has any files
if [[ ! -d "${MEMORY_DIR}" ]] || [[ -z "$(ls -A "${MEMORY_DIR}" 2>/dev/null)" ]]; then
    log "No memory files found, nothing to process"
    exit 0
fi

# Get list of memory files from last 30 days, sorted oldest first
cd "${MEMORY_DIR}"
MEMORY_FILES=$(find . -maxdepth 1 -name "????-??-??.md" -type f | \
    sed 's|^\./||' | \
    while read f; do 
        stat -c "%Y %f %n" "$f" 2>/dev/null || stat -f "%Sm %f %N" "$f"
    done | \
    sort -t' ' -k1 -n | \
    awk '{print $NF}' | \
    head -n "${DAYS_TO_PROCESS}" || true)

if [[ -z "${MEMORY_FILES}" ]]; then
    log "No memory files in range, nothing to process"
    exit 0
fi

# Build consolidated content for analysis
CONSOLIDATED=""
for file in ${MEMORY_FILES}; do
    if [[ -f "$file" ]]; then
        # Skip recent files
        file_date=$(echo "$file" | sed 's|\.md$||')
        days_diff=$(echo $(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$file_date" +%s 2>/dev/null || date --date="$file_date" +%s 2>/dev/null || echo 0)) / 86400 ))) 2>/dev/null || days_diff=999
        if [[ "${days_diff}" -lt "${PRESERVE_RECENT_DAYS}" ]]; then
            continue
        fi
        CONSOLIDATED="${CONSOLIDATED}\n\n--- ${file} ---\n$(cat "$file")"
    fi
done

if [[ -z "${CONSOLIDATED}" || "${#CONSOLIDATED}" -lt 50 ]]; then
    log "Insufficient content to process"
    exit 0
fi

# Extract key elements using simple pattern matching
# This mimics autoDream's idle-time analysis

KEY_DECISIONS=$(echo -e "${CONSOLIDATED}" | grep -iE "\[决策\]|\[决定\]|decided|决定|决策" | head -10 || true)
LESSONS=$(echo -e "${CONSOLIDATED}" | grep -iE "\[教训\]|\[lesson\]|mistake|教训|错误|from.*error" | head -10 || true)
PREFERENCES=$(echo -e "${CONSOLIDATED}" | grep -iE "\[偏好\]|\[preference\]|prefer|喜欢|偏好" | head -10 || true)
PENDING=$(echo -e "${CONSOLIDATED}" | grep -iE "\[待办\]|\[pending\]|\[todo\]|todo|待办|pending" | head -10 || true)
PEOPLE=$(echo -e "${CONSOLIDATED}" | grep -iE "\[人\]|person|name|人名|姓名" | head -10 || true)

# Generate summary for MEMORY.md
SUMMARY_DATE=$(date +%Y-%m-%d)
SUMMARY="\n\n## ${SUMMARY_DATE} 自动记忆摘要\n"

if [[ -n "${KEY_DECISIONS}" ]]; then
    SUMMARY="${SUMMARY}\n### 关键决策\n"
    echo -e "${KEY_DECISIONS}" | while read line; do
        [[ -n "${line}" ]] && SUMMARY="${SUMMARY}- ${line}\n"
    done
fi

if [[ -n "${LESSONS}" ]]; then
    SUMMARY="${SUMMARY}\n### 教训与错误\n"
    echo -e "${LESSONS}" | while read line; do
        [[ -n "${line}" ]] && SUMMARY="${SUMMARY}- ${line}\n"
    done
fi

if [[ -n "${PREFERENCES}" ]]; then
    SUMMARY="${SUMMARY}\n### 偏好与习惯\n"
    echo -e "${PREFERENCES}" | while read line; do
        [[ -n "${line}" ]] && SUMMARY="${SUMMARY}- ${line}\n"
    done
fi

if [[ -n "${PENDING}" ]]; then
    SUMMARY="${SUMMARY}\n### 待处理事项\n"
    echo -e "${PENDING}" | while read line; do
        [[ -n "${line}" ]] && SUMMARY="${SUMMARY}- ${line}\n"
    done
fi

# Append to MEMORY.md if we found anything significant
if [[ "${#SUMMARY}" -gt 100 ]]; then
    echo -e "${SUMMARY}" >> "${MEMORY_FILE}"
    log "Memory summary appended to MEMORY.md (${#SUMMARY} chars)"
else
    log "No significant content found to summarize"
fi

# Archive very old files (>60 days)
cd "${MEMORY_DIR}"
for file in $(find . -maxdepth 1 -name "????-??-??.md" -type f 2>/dev/null); do
    file_date=$(echo "$file" | sed 's|^\./||;s|\.md$||')
    file_ts=$(date -j -f "%Y-%m-%d" "$file_date" +%s 2>/dev/null || date --date="$file_date" +%s 2>/dev/null || echo 0)
    cutoff_ts=$(date -d "${ARCHIVE_AFTER_DAYS} days ago" +%s 2>/dev/null || echo 0)
    
    if [[ "${file_ts}" -lt "${cutoff_ts}" ]] && [[ "${file_ts}" -gt 0 ]]; then
        archive_dir="${MEMORY_DIR}/archive"
        mkdir -p "${archive_dir}"
        mv "$file" "${archive_dir}/"
        log "Archived: $file"
    fi
done

log "=== autoDream completed ==="
