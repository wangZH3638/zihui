/**
 * 飞书日历助手
 * Feishu Calendar Helper
 * 
 * 提供简单的日历管理接口
 */

const axios = require('axios');

// 飞书 API 配置
const API_BASE = 'https://open.feishu.cn/open-apis';

/**
 * 获取飞书 API Token
 */
async function getTenantAccessToken(appId, appSecret) {
  const response = await axios.post(`${API_BASE}/auth/v3/tenant_access_token/internal`, {
    app_id: appId,
    app_secret: appSecret
  });
  return response.data.tenant_access_token;
}

/**
 * 创建日程
 * @param {Object} options 日程选项
 */
async function createEvent(options) {
  const { appId, appSecret, title, startTime, endTime, reminder = 10, location = '', description = '' } = options;
  
  const token = await getTenantAccessToken(appId, appSecret);
  
  // 飞书 API 需要 UTC 时间戳字符串
  const formatTimestamp = (ts) => {
    const date = new Date(ts * 1000);
    const pad = (n) => n.toString().padStart(2, '0');
    const tz = '+08:00';
    return date.getFullYear() + '-' + pad(date.getMonth()+1) + '-' + pad(date.getDate()) + 'T' + pad(date.getHours()) + ':' + pad(date.getMinutes()) + ':' + pad(date.getSeconds()) + tz;
  };

  const event = {
    summary: title,
    description: description || '',
    start_time: {
      time_zone: 'Asia/Shanghai',
      timestamp: formatTimestamp(startTime)
    },
    end_time: {
      time_zone: 'Asia/Shanghai', 
      timestamp: formatTimestamp(endTime)
    }
  };

  if (location) event.location = location;
  if (reminder > 0) {
    event.reminder = {
      minutes_before_remind: reminder
    };
  }

  const response = await axios.post(
    `${API_BASE}/calendar/v4/calendars/feishu.cn_JjeTUlOAn6apYukhcVnqbh@group.calendar.feishu.cn/events`,
    event,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

  return response.data;
}

/**
 * 获取日程列表
 */
async function getEvents(options) {
  const { appId, appSecret, startTime, endTime } = options;
  
  const token = await getTenantAccessToken(appId, appSecret);
  
  const response = await axios.get(
    `${API_BASE}/calendar/v4/calendars/primary/events`,
    {
      params: {
        start_time: startTime,
        end_time: endTime
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

  return response.data;
}

/**
 * 删除日程
 */
async function deleteEvent(options) {
  const { appId, appSecret, eventId } = options;
  
  const token = await getTenantAccessToken(appId, appSecret);
  
  await axios.delete(
    `${API_BASE}/calendar/v4/calendars/primary/events/${eventId}`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );

  return { success: true };
}

/**
 * 解析自然语言时间
 */
function parseNaturalTime(text) {
  const now = new Date();
  const result = { start: null, end: null };
  
  // 今天
  if (text.includes('今天')) {
    const timeMatch = text.match(/(\d{1,2})[点时]/);
    if (timeMatch) {
      const hour = parseInt(timeMatch[1]);
      result.start = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour, 0, 0);
      result.end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hour + 1, 0, 0);
    } else {
      // 默认今天 9:00-18:00
      result.start = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 9, 0, 0);
      result.end = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 18, 0, 0);
    }
  }
  // 明天
  else if (text.includes('明天')) {
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const timeMatch = text.match(/(\d{1,2})[点时]/);
    if (timeMatch) {
      const hour = parseInt(timeMatch[1]);
      result.start = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), hour, 0, 0);
      result.end = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), hour + 1, 0, 0);
    } else {
      result.start = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 9, 0, 0);
      result.end = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate(), 18, 0, 0);
    }
  }
  // 下周X
  else if (text.includes('下周')) {
    const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    for (let i = 0; i < weekdays.length; i++) {
      if (text.includes(weekdays[i])) {
        const nextWeek = new Date(now);
        nextWeek.setDate(nextWeek.getDate() + 7 - now.getDay() + i);
        result.start = new Date(nextWeek.getFullYear(), nextWeek.getMonth(), nextWeek.getDate(), 9, 0, 0);
        result.end = new Date(nextWeek.getFullYear(), nextWeek.getMonth(), nextWeek.getDate(), 10, 0, 0);
        break;
      }
    }
  }
  
  return result;
}

module.exports = {
  createEvent,
  getEvents,
  deleteEvent,
  parseNaturalTime
};
