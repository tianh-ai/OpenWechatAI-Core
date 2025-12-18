#!/usr/bin/env python3
"""
钉钉群机器人Webhook示例

功能:
- 发送文本消息
- 发送Markdown消息
- 发送链接消息
- 发送ActionCard消息
"""

import requests
import json
import hashlib
import hmac
import base64
import time
from datetime import datetime
from urllib.parse import quote_plus


class DingTalkWebhookExample:
    """钉钉Webhook示例"""
    
    def __init__(self, webhook_url: str, secret: str = None):
        """
        初始化
        
        Args:
            webhook_url: 钉钉群机器人Webhook地址
            secret: 加签密钥（如果启用了加签）
        """
        self.webhook_url = webhook_url
        self.secret = secret
    
    def _get_signed_url(self) -> str:
        """获取加签后的URL"""
        if not self.secret:
            return self.webhook_url
        
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        
        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256
        ).digest()
        
        sign = quote_plus(base64.b64encode(hmac_code))
        
        return f"{self.webhook_url}&timestamp={timestamp}&sign={sign}"
    
    def send_text(self, content: str, at_mobiles: list = None, is_at_all: bool = False):
        """发送文本消息"""
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": is_at_all
            }
        }
        
        url = self._get_signed_url()
        response = requests.post(url, json=data)
        return response.json()
    
    def send_markdown(self, title: str, text: str, at_mobiles: list = None, is_at_all: bool = False):
        """发送Markdown消息"""
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            },
            "at": {
                "atMobiles": at_mobiles or [],
                "isAtAll": is_at_all
            }
        }
        
        url = self._get_signed_url()
        response = requests.post(url, json=data)
        return response.json()
    
    def send_link(self, title: str, text: str, message_url: str, pic_url: str = ""):
        """发送链接消息"""
        data = {
            "msgtype": "link",
            "link": {
                "title": title,
                "text": text,
                "messageUrl": message_url,
                "picUrl": pic_url
            }
        }
        
        url = self._get_signed_url()
        response = requests.post(url, json=data)
        return response.json()
    
    def send_action_card(self, title: str, text: str, btns: list):
        """发送ActionCard消息"""
        data = {
            "msgtype": "actionCard",
            "actionCard": {
                "title": title,
                "text": text,
                "btnOrientation": "0",
                "btns": btns
            }
        }
        
        url = self._get_signed_url()
        response = requests.post(url, json=data)
        return response.json()


def example_daily_briefing():
    """示例1: 每日简报"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    secret = "YOUR_SECRET"  # 如果启用了加签
    bot = DingTalkWebhookExample(webhook_url, secret)
    
    title = "每日简报"
    text = f"""
### 📰 每日简报
> {datetime.now().strftime('%Y年%m月%d日')}

#### 📊 数据概览
- 今日订单: **156单** ⬆️ 12%
- 销售额: **¥128,900** ⬆️ 8%
- 活跃用户: **2,345人** ⬆️ 5%

#### 🎯 重点关注
1. 新用户转化率下降，需优化引导流程
2. 客服响应时间增加，建议增加人手
3. 服务器负载偏高，建议扩容

#### 📅 今日重要事项
- 10:00 产品评审会
- 14:00 技术分享会
- 16:00 周会

[查看详细数据](https://dashboard.example.com)
    """
    
    result = bot.send_markdown(title, text)
    print(f"每日简报结果: {result}")


def example_urgent_alert():
    """示例2: 紧急告警"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    content = """🚨🚨🚨 紧急告警 🚨🚨🚨

【告警时间】2025-12-17 15:30:00
【告警级别】严重
【告警主机】web-server-01
【告警内容】服务器磁盘使用率超过95%

请运维人员立即处理！"""
    
    # @指定运维人员（手机号）
    result = bot.send_text(
        content,
        at_mobiles=["13800138000", "13900139000"]
    )
    print(f"紧急告警结果: {result}")


def example_approval_request():
    """示例3: 审批请求"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    title = "报销审批"
    text = """
### 💰 报销申请
> 申请人: 张三

#### 报销信息
- **报销金额**: ¥5,280
- **报销类型**: 差旅费
- **发生时间**: 2025-12-15 ~ 2025-12-17
- **出差地点**: 上海

#### 明细
1. 高铁票: ¥800 (往返)
2. 住宿费: ¥1,200 (2晚 × ¥600)
3. 餐饮费: ¥480
4. 打车费: ¥280
5. 其他: ¥2,520

#### 说明
参加上海客户产品演示会议

请审批!
    """
    
    btns = [
        {
            "title": "✅ 同意",
            "actionURL": "https://oa.example.com/approve?id=123"
        },
        {
            "title": "❌ 拒绝",
            "actionURL": "https://oa.example.com/reject?id=123"
        },
        {
            "title": "📋 查看详情",
            "actionURL": "https://oa.example.com/detail?id=123"
        }
    ]
    
    result = bot.send_action_card(title, text, btns)
    print(f"审批请求结果: {result}")


def example_version_release():
    """示例4: 版本发布通知"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    title = "版本发布"
    text = """
### 🚀 v1.0.0 正式发布！

#### 🎉 主要特性
- ✅ 企业通信MCP统一服务
- ✅ 支持企业微信/飞书/钉钉
- ✅ Web可视化配置界面
- ✅ 完整的API文档
- ✅ 自动回复规则引擎

#### 📦 技术栈
- Flask 3.0+ REST API
- Python 3.12+
- YAML配置管理

#### 🔧 改进
- 优化消息发送性能
- 增强错误处理机制
- 完善文档和示例

#### 📚 文档
- [快速开始](https://github.com/xxx/README.md)
- [API文档](https://github.com/xxx/API.md)
- [使用指南](https://github.com/xxx/GUIDE.md)

感谢所有贡献者的辛勤付出！🎊
    """
    
    result = bot.send_markdown(title, text, is_at_all=True)
    print(f"版本发布结果: {result}")


def example_build_status():
    """示例5: 构建状态通知"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    # 模拟构建失败
    title = "构建失败"
    text = """
### ❌ 构建失败

#### 基本信息
- **项目**: OpenWechatAI-Core
- **分支**: main
- **提交**: abc123d
- **作者**: 张三
- **时间**: 2025-12-17 16:00:00

#### 错误信息
```
pytest tests/test_feishu.py FAILED
AssertionError: assert False
```

#### 失败原因
单元测试未通过

#### 建议
请检查代码并重新提交
    """
    
    btns = [
        {
            "title": "查看日志",
            "actionURL": "https://ci.example.com/build/123/log"
        },
        {
            "title": "重新构建",
            "actionURL": "https://ci.example.com/build/123/rebuild"
        }
    ]
    
    result = bot.send_action_card(title, text, btns)
    print(f"构建状态结果: {result}")


def example_customer_inquiry():
    """示例6: 客户咨询"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    title = "新的客户咨询"
    text = """
### 💬 新客户咨询

#### 客户信息
- **公司**: 某某科技有限公司
- **联系人**: 李经理
- **电话**: 138****8888
- **邮箱**: li@example.com

#### 咨询内容
希望了解企业通信MCP的定制开发服务，
需要集成企业内部系统，预算充足。

#### 优先级
<font color=#ff0000>高</font>

#### 状态
待跟进

请销售团队尽快联系！
    """
    
    result = bot.send_markdown(title, text, at_mobiles=["13800138000"])
    print(f"客户咨询结果: {result}")


def example_training_notification():
    """示例7: 培训通知"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    result = bot.send_link(
        title="📚 技术分享：企业通信MCP架构设计",
        text="本周五下午2点，技术总监将分享企业通信MCP的架构设计思路和实现细节，欢迎大家参加！",
        message_url="https://meeting.dingtalk.com/j/xxx",
        pic_url="https://example.com/images/training.jpg"
    )
    print(f"培训通知结果: {result}")


def example_holiday_greeting():
    """示例8: 节日祝福"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    content = """🎄🎅 圣诞快乐！🎁🎉

亲爱的小伙伴们：

圣诞节到了，祝大家节日快乐！

愿你：
🌟 工作顺利，心想事成
💰 财源滚滚，钱途无量  
❤️ 身心健康，笑口常开
🎁 幸福美满，阖家欢乐

公司为大家准备了圣诞礼物，
请到行政部领取哦~

祝大家圣诞节快乐！🎊"""
    
    result = bot.send_text(content, is_at_all=True)
    print(f"节日祝福结果: {result}")


def example_performance_dashboard():
    """示例9: 性能监控面板"""
    
    import schedule
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    def send_performance_report():
        """发送性能报告"""
        title = "系统性能监控"
        text = f"""
### 📊 系统性能监控
> 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#### 服务器状态
- **CPU使用率**: 45% 🟢
- **内存使用率**: 68% 🟢
- **磁盘使用率**: 72% 🟡
- **网络流量**: 120MB/s 🟢

#### 应用状态
- **QPS**: 1,250 req/s 🟢
- **平均响应时间**: 85ms 🟢
- **错误率**: 0.02% 🟢
- **在线用户**: 2,345人 🟢

#### 数据库状态
- **连接数**: 45/200 🟢
- **慢查询**: 0 🟢
- **复制延迟**: 0.2s 🟢

所有指标正常！✅
        """
        
        result = bot.send_markdown(title, text)
        print(f"性能报告已发送: {result}")
    
    # 每小时发送一次
    schedule.every().hour.do(send_performance_report)
    
    print("性能监控定时任务已启动...")
    while True:
        schedule.run_pending()
        time.sleep(60)


def example_on_duty_handover():
    """示例10: 值班交接"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=YOUR_TOKEN"
    bot = DingTalkWebhookExample(webhook_url)
    
    title = "值班交接"
    text = """
### 🔄 值班交接通知

#### 值班信息
- **交班人**: 张三
- **接班人**: 李四  
- **交接时间**: 2025-12-17 18:00

#### 值班总结
1. 处理告警: 3次（已解决）
2. 用户咨询: 12个（已回复）
3. 系统巡检: 正常
4. 数据备份: 完成

#### 待处理事项
1. ⚠️ web-server-02 CPU偏高，需持续关注
2. 📋 明天凌晨有系统升级计划
3. 🔧 数据库慢查询优化进行中

#### 紧急联系
- 运维主管: 138****8888
- 值班手机: 139****9999

@李四 请接班！
    """
    
    result = bot.send_markdown(
        title, text,
        at_mobiles=["13900139999"]  # 接班人手机号
    )
    print(f"值班交接结果: {result}")


if __name__ == "__main__":
    print("钉钉Webhook示例")
    print("=" * 50)
    
    # 运行示例（需要替换为实际的Webhook URL）
    print("\n1. 每日简报")
    # example_daily_briefing()
    
    print("\n2. 紧急告警")
    # example_urgent_alert()
    
    print("\n3. 审批请求")
    # example_approval_request()
    
    print("\n4. 版本发布")
    # example_version_release()
    
    print("\n5. 构建状态")
    # example_build_status()
    
    print("\n6. 客户咨询")
    # example_customer_inquiry()
    
    print("\n7. 培训通知")
    # example_training_notification()
    
    print("\n8. 节日祝福")
    # example_holiday_greeting()
    
    print("\n9. 性能监控（长期运行）")
    # example_performance_dashboard()
    
    print("\n10. 值班交接")
    # example_on_duty_handover()
    
    print("\n提示: 请取消注释相应函数并替换Webhook URL后运行")
