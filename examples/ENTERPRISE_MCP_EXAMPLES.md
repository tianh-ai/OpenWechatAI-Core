# 企业通信MCP使用示例

## 📋 目录

1. [企业微信示例](#企业微信示例)
2. [飞书示例](#飞书示例)
3. [钉钉示例](#钉钉示例)
4. [进阶用法](#进阶用法)
5. [实际场景](#实际场景)

---

## 企业微信示例

### 1. 群机器人推送通知

```python
#!/usr/bin/env python3
"""企业微信群机器人推送示例"""

import requests

# 配置
API_BASE = "http://localhost:8000"
WEWORK_CONFIG = {
    'enabled': True,
    'type': 'webhook',
    'webhook_url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY'
}

# 1. 配置企业微信
response = requests.post(
    f"{API_BASE}/api/config/wework",
    json=WEWORK_CONFIG
)
print(f"配置结果: {response.json()}")

# 2. 发送简单文本
response = requests.post(
    f"{API_BASE}/api/send/wework",
    json={'content': '📢 系统通知：服务器已成功重启'}
)
print(f"发送结果: {response.json()}")

# 3. 发送每日报表
daily_report = """
📊 每日数据报表 (2025-12-17)

✅ 订单量: 156单
💰 销售额: ¥128,900
👥 新用户: 23人
⭐ 好评率: 98.5%

🎯 明日目标: 订单量突破200单
"""

response = requests.post(
    f"{API_BASE}/api/send/wework",
    json={'content': daily_report}
)
print(f"报表发送: {response.json()}")
```

### 2. 企业应用自动回复

```python
#!/usr/bin/env python3
"""企业微信应用机器人示例"""

# 配置企业应用
WEWORK_APP_CONFIG = {
    'enabled': True,
    'type': 'app',
    'corp_id': 'ww1234567890abcdef',
    'corp_secret': 'YOUR_SECRET',
    'agent_id': '1000001',
    'token': 'YOUR_TOKEN',
    'encoding_aes_key': 'YOUR_AES_KEY'
}

# 更新配置
response = requests.post(
    f"{API_BASE}/api/config/wework",
    json=WEWORK_APP_CONFIG
)

# 配置自动回复规则
rules = """
rules:
  - name: "上班打卡提醒"
    condition:
      type: keyword
      keywords: ["打卡", "签到"]
    reply: "已收到打卡请求，正在为您处理..."
  
  - name: "报销审批"
    condition:
      type: regex
      pattern: "报销.*([0-9]+)元"
    reply: "您的报销申请已提交，预计3个工作日内审批完成"
"""

with open('config/reply_rules.yaml', 'w') as f:
    f.write(rules)

print("✓ 企业微信应用配置完成")
```

---

## 飞书示例

### 1. 群机器人卡片消息

```python
#!/usr/bin/env python3
"""飞书群机器人示例"""

from enterprise_comm_mcp.feishu_bot import FeishuWebhookBot

# 初始化
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
secret = "YOUR_SECRET"  # 如果启用了签名验证
bot = FeishuWebhookBot(webhook_url, secret)

# 1. 发送文本消息
bot.send_text("👋 大家好，这是一条测试消息")

# 2. 发送富文本消息
bot.send_rich_text(
    title="📊 项目进度更新",
    content="""
    项目已完成60%
    
    ✅ 已完成:
    - 需求分析
    - 原型设计
    - 前端开发
    
    🚧 进行中:
    - 后端开发
    - 测试用例编写
    
    📅 预计交付: 2025-12-30
    """
)

# 3. 发送卡片消息
bot.send_card(
    title="⚠️ 服务器告警",
    content="服务器CPU使用率超过90%，请立即检查"
)

print("✓ 飞书消息发送完成")
```

### 2. 飞书应用定时推送

```python
#!/usr/bin/env python3
"""飞书应用定时推送示例"""

from enterprise_comm_mcp.feishu_bot import FeishuAppBot
import schedule
import time

# 初始化应用机器人
bot = FeishuAppBot(
    app_id='cli_xxx',
    app_secret='YOUR_SECRET'
)

def send_morning_report():
    """发送早报"""
    message = {
        "text": "☀️ 早上好！\n\n今日天气: 晴 18-25℃\n今日任务: 3个会议，5个待办事项"
    }
    bot.send_message('open_id_xxx', 'text', message)
    print("✓ 早报已发送")

def send_evening_summary():
    """发送晚报"""
    message = {
        "text": "🌙 今日总结\n\n完成任务: 8个\n待处理: 2个\n明日重点: 产品评审"
    }
    bot.send_message('open_id_xxx', 'text', message)
    print("✓ 晚报已发送")

# 定时任务
schedule.every().day.at("09:00").do(send_morning_report)
schedule.every().day.at("18:00").do(send_evening_summary)

print("📅 定时推送已启动...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 钉钉示例

### 1. 群机器人@指定成员

```python
#!/usr/bin/env python3
"""钉钉群机器人示例"""

from enterprise_comm_mcp.dingtalk_bot import DingTalkWebhookBot

# 初始化
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
secret = "YOUR_SECRET"
bot = DingTalkWebhookBot(webhook_url, secret)

# 1. 普通文本消息
bot.send_text("测试消息")

# 2. @指定成员
bot.send_text(
    "紧急任务：请立即处理线上Bug",
    at_mobiles=["13800138000", "13900139000"]
)

# 3. @所有人
bot.send_text(
    "🎉 系统升级完成，欢迎大家体验新功能！",
    is_at_all=True
)

# 4. Markdown消息
bot.send_markdown(
    title="周报汇总",
    text="""
    ### 本周工作总结
    
    #### 完成事项
    - 完成用户模块开发
    - 优化数据库性能
    - 修复3个严重Bug
    
    #### 下周计划
    - 开发订单模块
    - 编写API文档
    - 进行压力测试
    
    > 工作进度: 80%
    """
)

# 5. 链接消息
bot.send_link(
    title="查看详细报告",
    text="点击查看本周详细工作报告",
    message_url="https://example.com/report/weekly",
    pic_url="https://example.com/images/report-cover.jpg"
)

print("✓ 钉钉消息发送完成")
```

### 2. ActionCard交互式消息

```python
#!/usr/bin/env python3
"""钉钉ActionCard示例"""

from enterprise_comm_mcp.dingtalk_bot import DingTalkWebhookBot

bot = DingTalkWebhookBot(
    webhook_url="https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN",
    secret="YOUR_SECRET"
)

# 发送带按钮的卡片
bot.send_action_card(
    title="项目审批",
    text="""
    ### 新项目申请
    
    **项目名称**: AI智能客服系统
    **预算**: ¥500,000
    **周期**: 3个月
    **负责人**: 张三
    
    请尽快审批
    """,
    btns=[
        {
            "title": "✅ 同意",
            "actionURL": "https://example.com/approve?id=123"
        },
        {
            "title": "❌ 拒绝",
            "actionURL": "https://example.com/reject?id=123"
        }
    ]
)

print("✓ ActionCard发送完成")
```

---

## 进阶用法

### 1. 多平台同时推送

```python
#!/usr/bin/env python3
"""同时向三个平台推送消息"""

import requests
from concurrent.futures import ThreadPoolExecutor

API_BASE = "http://localhost:8000"

def send_to_platform(platform, message):
    """发送到指定平台"""
    response = requests.post(
        f"{API_BASE}/api/send/{platform}",
        json={'content': message}
    )
    return platform, response.json()

# 消息内容
urgent_message = """
🚨 紧急通知

服务器磁盘使用率超过95%
请运维人员立即处理！

时间: 2025-12-17 15:30
"""

# 并发推送到三个平台
platforms = ['wework', 'feishu', 'dingtalk']
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [
        executor.submit(send_to_platform, platform, urgent_message)
        for platform in platforms
    ]
    
    for future in futures:
        platform, result = future.result()
        print(f"{platform}: {result}")

print("✓ 多平台推送完成")
```

### 2. 智能路由转发

```python
#!/usr/bin/env python3
"""根据消息类型智能路由到不同平台"""

import requests

API_BASE = "http://localhost:8000"

def smart_routing(msg_type, content):
    """智能路由"""
    routing_rules = {
        'urgent': 'wework',      # 紧急消息发企业微信
        'daily': 'feishu',       # 日常消息发飞书
        'notification': 'dingtalk'  # 通知发钉钉
    }
    
    platform = routing_rules.get(msg_type, 'wework')
    
    response = requests.post(
        f"{API_BASE}/api/send/{platform}",
        json={'content': content}
    )
    
    return response.json()

# 使用示例
smart_routing('urgent', '🚨 线上故障，立即处理')
smart_routing('daily', '📊 今日数据报表已生成')
smart_routing('notification', '🎉 新版本已发布')
```

### 3. 消息队列批量处理

```python
#!/usr/bin/env python3
"""批量处理消息队列"""

import requests
import time
from queue import Queue
from threading import Thread

API_BASE = "http://localhost:8000"
message_queue = Queue()

def worker():
    """消息发送工作线程"""
    while True:
        platform, message = message_queue.get()
        if message is None:
            break
        
        try:
            response = requests.post(
                f"{API_BASE}/api/send/{platform}",
                json={'content': message}
            )
            print(f"✓ {platform}: {response.json()}")
        except Exception as e:
            print(f"❌ {platform} 发送失败: {e}")
        
        message_queue.task_done()
        time.sleep(1)  # 避免频繁请求

# 启动工作线程
num_workers = 3
threads = []
for i in range(num_workers):
    t = Thread(target=worker)
    t.start()
    threads.append(t)

# 添加消息到队列
messages = [
    ('wework', '消息1'),
    ('feishu', '消息2'),
    ('dingtalk', '消息3'),
    ('wework', '消息4'),
    ('feishu', '消息5'),
]

for platform, message in messages:
    message_queue.put((platform, message))

# 等待所有消息处理完成
message_queue.join()

# 停止工作线程
for i in range(num_workers):
    message_queue.put((None, None))

for t in threads:
    t.join()

print("✓ 批量处理完成")
```

---

## 实际场景

### 场景1: CI/CD构建通知

```python
#!/usr/bin/env python3
"""CI/CD构建结果通知"""

import requests
import sys

API_BASE = "http://localhost:8000"

def notify_build_result(status, branch, commit, author):
    """通知构建结果"""
    
    emoji = "✅" if status == "success" else "❌"
    
    message = f"""
    {emoji} 构建{status}
    
    分支: {branch}
    提交: {commit[:7]}
    作者: {author}
    时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    # 成功发飞书，失败发企业微信
    platform = 'feishu' if status == 'success' else 'wework'
    
    response = requests.post(
        f"{API_BASE}/api/send/{platform}",
        json={'content': message}
    )
    
    return response.json()

# 在CI/CD脚本中调用
if __name__ == "__main__":
    import os
    notify_build_result(
        status=os.getenv('BUILD_STATUS', 'success'),
        branch=os.getenv('GIT_BRANCH', 'main'),
        commit=os.getenv('GIT_COMMIT', 'abc123'),
        author=os.getenv('GIT_AUTHOR', 'Developer')
    )
```

### 场景2: 监控告警

```python
#!/usr/bin/env python3
"""系统监控告警"""

import requests
import psutil

API_BASE = "http://localhost:8000"

def check_system_health():
    """检查系统健康状态"""
    
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    alerts = []
    
    if cpu_percent > 90:
        alerts.append(f"⚠️ CPU使用率: {cpu_percent}%")
    
    if memory.percent > 90:
        alerts.append(f"⚠️ 内存使用率: {memory.percent}%")
    
    if disk.percent > 90:
        alerts.append(f"⚠️ 磁盘使用率: {disk.percent}%")
    
    if alerts:
        message = "🚨 系统告警\n\n" + "\n".join(alerts)
        
        # 发送到企业微信（紧急告警）
        response = requests.post(
            f"{API_BASE}/api/send/wework",
            json={'content': message}
        )
        
        print(f"告警已发送: {response.json()}")

# 定时检查
import schedule
schedule.every(5).minutes.do(check_system_health)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 场景3: 客户服务工单

```python
#!/usr/bin/env python3
"""客户服务工单处理"""

import requests

API_BASE = "http://localhost:8000"

def create_ticket(customer, issue, priority):
    """创建客服工单"""
    
    priority_emoji = {
        'low': '🟢',
        'medium': '🟡',
        'high': '🔴'
    }
    
    message = f"""
    {priority_emoji[priority]} 新工单
    
    客户: {customer}
    问题: {issue}
    优先级: {priority.upper()}
    创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
    
    请及时处理
    """
    
    # 高优先级发企业微信，其他发钉钉
    platform = 'wework' if priority == 'high' else 'dingtalk'
    
    response = requests.post(
        f"{API_BASE}/api/send/{platform}",
        json={'content': message}
    )
    
    return response.json()

# 示例使用
create_ticket(
    customer="张三",
    issue="无法登录系统",
    priority="high"
)
```

---

## 🎯 最佳实践

1. **错误处理**: 总是添加try-except处理网络异常
2. **重试机制**: 对失败的请求实现指数退避重试
3. **日志记录**: 记录所有API调用和响应
4. **频率限制**: 注意各平台的API调用频率限制
5. **安全性**: 不要在代码中硬编码密钥，使用环境变量

## 📚 更多资源

- [企业通信MCP完整指南](ENTERPRISE_COMM_MCP_GUIDE.md)
- [API文档](enterprise_comm_mcp/README.md)
- [配置说明](enterprise_comm_mcp/config.yaml.example)
