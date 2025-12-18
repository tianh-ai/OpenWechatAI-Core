#!/usr/bin/env python3
"""
飞书群机器人Webhook示例

功能:
- 发送文本消息
- 发送富文本消息
- 发送卡片消息
- 发送图片消息
"""

import requests
import json
import hashlib
import hmac
import base64
import time
from datetime import datetime


class FeishuWebhookExample:
    """飞书Webhook示例"""
    
    def __init__(self, webhook_url: str, secret: str = None):
        """
        初始化
        
        Args:
            webhook_url: 飞书群机器人Webhook地址
            secret: 签名密钥（如果启用了签名验证）
        """
        self.webhook_url = webhook_url
        self.secret = secret
    
    def _gen_sign(self, timestamp: int) -> str:
        """生成签名"""
        if not self.secret:
            return ""
        
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(
            string_to_sign.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign
    
    def send_text(self, text: str):
        """发送文本消息"""
        timestamp = int(time.time())
        data = {
            "timestamp": str(timestamp),
            "sign": self._gen_sign(timestamp),
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def send_rich_text(self, title: str, content: str):
        """发送富文本消息"""
        timestamp = int(time.time())
        data = {
            "timestamp": str(timestamp),
            "sign": self._gen_sign(timestamp),
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": [
                            [{"tag": "text", "text": content}]
                        ]
                    }
                }
            }
        }
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def send_card(self, title: str, content: str):
        """发送卡片消息"""
        timestamp = int(time.time())
        data = {
            "timestamp": str(timestamp),
            "sign": self._gen_sign(timestamp),
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "plain_text",
                            "content": content
                        }
                    }
                ]
            }
        }
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()


def example_daily_standup():
    """示例1: 每日站会提醒"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    secret = "YOUR_SECRET"  # 如果启用了签名验证
    bot = FeishuWebhookExample(webhook_url, secret)
    
    content = """🎯 每日站会 - 10分钟后开始

📅 时间: 今天 10:00 AM
📍 地点: 会议室A / 飞书会议
👥 参与: 全体开发团队

议程:
1. 昨日完成事项分享
2. 今日工作计划
3. 遇到的问题讨论

请大家准时参加！"""
    
    result = bot.send_text(content)
    print(f"站会提醒结果: {result}")


def example_task_assignment():
    """示例2: 任务分配通知"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    title = "📋 新任务分配"
    content = """任务名称: 用户反馈功能开发
负责人: @张三
优先级: 高
截止日期: 2025-12-25

任务描述:
开发用户反馈功能，包括前端表单、后端API、数据库设计

要求:
- 支持文字、图片反馈
- 管理员可查看和处理反馈
- 邮件通知处理结果

请及时查看任务详情并开始工作！"""
    
    result = bot.send_card(title, content)
    print(f"任务分配结果: {result}")


def example_deployment_notification():
    """示例3: 部署通知"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    title = "🚀 生产环境部署通知"
    content = """项目: OpenWechatAI-Core
版本: v1.0.0
环境: Production

部署内容:
✅ 企业通信MCP模块
✅ 飞书机器人集成
✅ 钉钉机器人集成
✅ Web配置界面

部署时间: 2025-12-17 22:00
预计影响: 服务中断5分钟

请相关人员做好准备！"""
    
    result = bot.send_card(title, content)
    print(f"部署通知结果: {result}")


def example_code_review_reminder():
    """示例4: Code Review提醒"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    content = """👀 待Review的Pull Request

PR #123: 添加企业通信MCP功能
提交人: 张三
提交时间: 2小时前
文件变更: +3306 / -0
状态: 等待Review

描述:
完整实现企业微信、飞书、钉钉三大平台的机器人集成，
包括Webhook和应用模式，提供统一的MCP服务器。

@李四 @王五 请帮忙Review一下，谢谢！

查看详情: https://github.com/xxx/pull/123"""
    
    result = bot.send_text(content)
    print(f"Code Review提醒结果: {result}")


def example_sprint_summary():
    """示例5: Sprint总结"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    title = "🏁 Sprint 12 总结"
    content = """时间: 2025-12-03 ~ 2025-12-17 (2周)

📊 统计数据:
- 计划Story: 15个
- 完成Story: 13个
- 完成率: 87%
- 代码提交: 156次
- Bug修复: 23个

✅ 主要成果:
1. 企业通信MCP开发完成
2. 三大平台机器人集成
3. Web配置界面上线
4. 完整文档编写

⚠️ 遗留问题:
1. 单元测试覆盖率不足（当前65%）
2. 性能优化未完成

📅 下个Sprint:
- 提高测试覆盖率到85%
- 完成性能优化
- 准备v1.0正式发布

感谢大家的辛勤付出！"""
    
    result = bot.send_card(title, content)
    print(f"Sprint总结结果: {result}")


def example_incident_report():
    """示例6: 故障报告"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    title = "🚨 线上故障报告"
    content = """故障级别: P1 (严重)
影响范围: 全部用户
故障时间: 2025-12-17 14:30 - 15:15 (45分钟)

故障现象:
用户无法登录系统，报500错误

根本原因:
数据库连接池耗尽，大量慢查询导致

解决方案:
1. 紧急重启数据库
2. 优化慢查询SQL
3. 增加连接池配置

预防措施:
- 添加数据库监控告警
- 定期SQL性能审查
- 增加降级方案

责任人: 运维团队
复盘时间: 明天14:00

详细报告: https://docs.example.com/incident/202512170001"""
    
    result = bot.send_card(title, content)
    print(f"故障报告结果: {result}")


def example_birthday_greeting():
    """示例7: 生日祝福"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    content = """🎂 生日快乐！

今天是 @张三 的生日
让我们一起祝TA生日快乐！🎉

愿你:
🌟 工作顺利，步步高升
💰 财源广进，钱途无量
❤️ 身体健康，笑口常开
🎁 天天开心，幸福美满

下午3点在茶水间有惊喜哦~"""
    
    result = bot.send_text(content)
    print(f"生日祝福结果: {result}")


def example_weekly_report():
    """示例8: 周报提醒"""
    
    import schedule
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    def send_weekly_reminder():
        """发送周报提醒"""
        content = """📝 周报提醒

本周五17:00前请提交周报

周报内容:
1. 本周工作总结
2. 遇到的问题和解决方案
3. 下周工作计划
4. 需要的支持

提交地址: https://report.example.com

温馨提示: 越早提交越早下班哦~"""
        
        result = bot.send_text(content)
        print(f"周报提醒已发送: {result}")
    
    # 每周五下午3点提醒
    schedule.every().friday.at("15:00").do(send_weekly_reminder)
    
    print("周报提醒定时任务已启动...")
    while True:
        schedule.run_pending()
        time.sleep(60)


def example_meeting_minutes():
    """示例9: 会议纪要"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    title = "📋 产品评审会议纪要"
    content = """会议时间: 2025-12-17 14:00-16:00
参会人员: 产品、开发、测试、设计
会议地点: 会议室B

讨论议题:
1. v1.0版本功能确认
2. UI/UX设计评审
3. 技术方案讨论
4. 上线时间排期

决议事项:
✅ 确认v1.0核心功能范围
✅ UI设计方案通过
✅ 采用微服务架构
✅ 计划12月30日上线

待办事项:
1. 开发团队: 12月20日前完成开发
2. 测试团队: 12月25日前完成测试
3. 运维团队: 准备生产环境

下次会议: 12月24日 14:00

完整纪要: https://docs.example.com/meeting/20251217"""
    
    result = bot.send_card(title, content)
    print(f"会议纪要结果: {result}")


def example_performance_review():
    """示例10: 绩效考评提醒"""
    
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
    bot = FeishuWebhookExample(webhook_url)
    
    content = """📊 Q4绩效考评通知

考评周期: 2025年10月-12月
截止时间: 2025-12-25 18:00

考评内容:
1. 自我评价
2. 工作成果展示
3. 项目贡献说明
4. 个人成长总结
5. 下季度目标

考评流程:
1. 填写自评表（12月20日前）
2. 主管评分（12月23日前）
3. 绩效面谈（12月24-25日）

考评系统: https://hr.example.com/performance

提示:
- 请认真填写，这关系到年终奖哦
- 准备好项目数据和成果展示
- 有问题随时找HR沟通

祝大家都能取得好成绩！💪"""
    
    result = bot.send_text(content)
    print(f"绩效考评提醒结果: {result}")


if __name__ == "__main__":
    print("飞书Webhook示例")
    print("=" * 50)
    
    # 运行示例（需要替换为实际的Webhook URL）
    print("\n1. 每日站会提醒")
    # example_daily_standup()
    
    print("\n2. 任务分配通知")
    # example_task_assignment()
    
    print("\n3. 部署通知")
    # example_deployment_notification()
    
    print("\n4. Code Review提醒")
    # example_code_review_reminder()
    
    print("\n5. Sprint总结")
    # example_sprint_summary()
    
    print("\n6. 故障报告")
    # example_incident_report()
    
    print("\n7. 生日祝福")
    # example_birthday_greeting()
    
    print("\n8. 周报提醒（长期运行）")
    # example_weekly_report()
    
    print("\n9. 会议纪要")
    # example_meeting_minutes()
    
    print("\n10. 绩效考评提醒")
    # example_performance_review()
    
    print("\n提示: 请取消注释相应函数并替换Webhook URL后运行")
