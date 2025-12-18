# 使用示例目录

本目录包含企业通信MCP和个人微信自动化的完整使用示例。

## 📂 目录结构

```
examples/
├── README.md                           # 本文件
├── ENTERPRISE_MCP_EXAMPLES.md          # 企业通信MCP详细示例文档
├── wework_webhook_example.py           # 企业微信Webhook示例
├── feishu_webhook_example.py           # 飞书Webhook示例
├── dingtalk_webhook_example.py         # 钉钉Webhook示例
└── personal_wechat_example.py          # 个人微信自动化示例（待添加）
```

## 🚀 企业通信MCP示例

### 1. 企业微信群机器人 (`wework_webhook_example.py`)

包含7个实用场景：
- ✅ 每日数据报表
- ✅ 系统告警通知
- ✅ 资讯推送
- ✅ 周报汇总
- ✅ CI/CD构建通知
- ✅ 客户反馈通知
- ✅ 定时提醒

**快速使用**:
```python
from wework_webhook_example import WeWorkWebhookExample

# 初始化
webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
bot = WeWorkWebhookExample(webhook_url)

# 发送Markdown消息
bot.send_markdown("📊 每日报表", "今日订单: 156单")
```

### 2. 飞书群机器人 (`feishu_webhook_example.py`)

包含10个实用场景：
- ✅ 每日站会提醒
- ✅ 任务分配通知
- ✅ 部署通知
- ✅ Code Review提醒
- ✅ Sprint总结
- ✅ 故障报告
- ✅ 生日祝福
- ✅ 周报提醒
- ✅ 会议纪要
- ✅ 绩效考评提醒

**快速使用**:
```python
from feishu_webhook_example import FeishuWebhookExample

# 初始化（带签名验证）
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
secret = "YOUR_SECRET"
bot = FeishuWebhookExample(webhook_url, secret)

# 发送卡片消息
bot.send_card("🚀 部署通知", "v1.0.0已成功部署到生产环境")
```

### 3. 钉钉群机器人 (`dingtalk_webhook_example.py`)

包含10个实用场景：
- ✅ 每日简报
- ✅ 紧急告警
- ✅ 审批请求
- ✅ 版本发布
- ✅ 构建状态
- ✅ 客户咨询
- ✅ 培训通知
- ✅ 节日祝福
- ✅ 性能监控
- ✅ 值班交接

**快速使用**:
```python
from dingtalk_webhook_example import DingTalkWebhookExample

# 初始化（带加签）
webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
secret = "YOUR_SECRET"
bot = DingTalkWebhookExample(webhook_url, secret)

# 发送ActionCard
bot.send_action_card(
    title="审批请求",
    text="请审批报销申请",
    btns=[
        {"title": "同意", "actionURL": "https://..."},
        {"title": "拒绝", "actionURL": "https://..."}
    ]
)
```

## 📖 详细示例文档

查看 [`ENTERPRISE_MCP_EXAMPLES.md`](ENTERPRISE_MCP_EXAMPLES.md) 获取：
- 完整的代码示例
- 进阶用法（多平台推送、智能路由、消息队列）
- 实际场景（CI/CD、监控告警、客服工单）
- 最佳实践

## 🎯 使用步骤

### 步骤1: 获取Webhook地址

**企业微信**:
1. 在群聊中添加"群机器人"
2. 获取Webhook地址: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx`

**飞书**:
1. 在群聊设置中添加"机器人"
2. 获取Webhook地址: `https://open.feishu.cn/open-apis/bot/v2/hook/xxx`
3. (可选) 启用签名验证并获取Secret

**钉钉**:
1. 在群聊设置中添加"自定义机器人"
2. 获取Webhook地址: `https://oapi.dingtalk.com/robot/send?access_token=xxx`
3. (可选) 启用加签并获取Secret

### 步骤2: 配置示例代码

```python
# 替换为实际的Webhook地址和Secret
webhook_url = "YOUR_WEBHOOK_URL"
secret = "YOUR_SECRET"  # 如果启用了签名验证
```

### 步骤3: 运行示例

```bash
# 运行企业微信示例
python examples/wework_webhook_example.py

# 运行飞书示例
python examples/feishu_webhook_example.py

# 运行钉钉示例
python examples/dingtalk_webhook_example.py
```

## 🔧 进阶用法

### 多平台同时推送

```python
import requests
from concurrent.futures import ThreadPoolExecutor

API_BASE = "http://localhost:8000"

def send_to_all_platforms(message):
    """同时发送到三个平台"""
    platforms = ['wework', 'feishu', 'dingtalk']
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(
                requests.post,
                f"{API_BASE}/api/send/{platform}",
                json={'content': message}
            )
            for platform in platforms
        ]
        
        for future in futures:
            print(future.result().json())

# 使用
send_to_all_platforms("🚨 重要通知：系统将在10分钟后维护")
```

### 定时任务

```python
import schedule
import time

def send_daily_report():
    """每天9点发送日报"""
    bot.send_text("📊 今日工作开始，加油！")

schedule.every().day.at("09:00").do(send_daily_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 错误处理

```python
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def send_with_retry(bot, message):
    """带重试机制的发送"""
    try:
        result = bot.send_text(message)
        if result.get('errcode') != 0:
            raise Exception(f"发送失败: {result}")
        return result
    except Exception as e:
        print(f"发送错误: {e}")
        raise
```

## 🌟 实际场景示例

### 场景1: CI/CD集成

在`.gitlab-ci.yml`或GitHub Actions中：

```yaml
deploy:
  script:
    - python examples/notify_deployment.py
    
# notify_deployment.py
import os
import requests

webhook_url = os.getenv('WEWORK_WEBHOOK_URL')
bot = WeWorkWebhookExample(webhook_url)

bot.send_markdown(
    f"✅ 部署成功\n\n"
    f"分支: {os.getenv('CI_COMMIT_BRANCH')}\n"
    f"提交: {os.getenv('CI_COMMIT_SHA')[:7]}\n"
    f"作者: {os.getenv('CI_COMMIT_AUTHOR')}"
)
```

### 场景2: 监控告警

```python
import psutil

def check_system():
    """系统健康检查"""
    cpu = psutil.cpu_percent(interval=1)
    
    if cpu > 90:
        bot.send_text(
            f"🚨 告警：CPU使用率{cpu}%",
            at_mobiles=["13800138000"]  # @运维人员
        )
```

### 场景3: 客服工单

```python
def new_ticket(customer, issue, priority):
    """新工单通知"""
    emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
    
    platform = 'wework' if priority == 'high' else 'dingtalk'
    
    requests.post(
        f"http://localhost:8000/api/send/{platform}",
        json={
            'content': f"{emoji[priority]} 新工单\n客户: {customer}\n问题: {issue}"
        }
    )
```

## 📚 更多资源

- [企业通信MCP完整指南](../ENTERPRISE_COMM_MCP_GUIDE.md)
- [MCP服务器API文档](../enterprise_comm_mcp/README.md)
- [配置文件示例](../enterprise_comm_mcp/config.yaml.example)
- [快速开始](../README.md#快速开始)

## 💡 提示

1. **安全性**: 不要在代码中硬编码Webhook URL和Secret，使用环境变量
2. **频率限制**: 注意各平台的API调用频率限制
3. **错误处理**: 总是添加try-except和重试机制
4. **日志记录**: 记录所有API调用和响应用于调试
5. **测试**: 先在测试群中验证，再部署到生产环境

## 🤝 贡献

欢迎提交更多实用示例！请参考 [贡献指南](../CONTRIBUTING.md)

## 📄 许可证

MIT License - 详见 [LICENSE](../LICENSE)
