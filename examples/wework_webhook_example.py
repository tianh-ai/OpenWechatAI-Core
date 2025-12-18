#!/usr/bin/env python3
"""
企业微信群机器人Webhook示例

功能:
- 发送文本消息
- 发送Markdown消息
- 发送图片消息
- 发送文件消息
"""

import requests
import json
from datetime import datetime


class WeWorkWebhookExample:
    """企业微信Webhook示例"""
    
    def __init__(self, webhook_url: str):
        """
        初始化
        
        Args:
            webhook_url: 企业微信群机器人Webhook地址
        """
        self.webhook_url = webhook_url
    
    def send_text(self, content: str, mentioned_list: list = None):
        """
        发送文本消息
        
        Args:
            content: 消息内容
            mentioned_list: @的成员列表（userid）
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        if mentioned_list:
            data["text"]["mentioned_list"] = mentioned_list
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def send_markdown(self, content: str):
        """
        发送Markdown消息
        
        Args:
            content: Markdown格式内容
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def send_image(self, base64_content: str, md5: str):
        """
        发送图片消息
        
        Args:
            base64_content: 图片的base64编码
            md5: 图片的MD5值
        """
        data = {
            "msgtype": "image",
            "image": {
                "base64": base64_content,
                "md5": md5
            }
        }
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()
    
    def send_news(self, articles: list):
        """
        发送图文消息
        
        Args:
            articles: 图文列表，每项包含title、description、url、picurl
        """
        data = {
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        }
        
        response = requests.post(self.webhook_url, json=data)
        return response.json()


def example_daily_report():
    """示例1: 每日数据报表"""
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    # 发送Markdown格式的日报
    content = f"""
    ## 📊 每日数据报表
    > 日期: {datetime.now().strftime('%Y-%m-%d')}
    
    ### 核心指标
    - **订单量**: 156单 <font color="info">↑12%</font>
    - **销售额**: ¥128,900 <font color="info">↑8%</font>
    - **新用户**: 23人 <font color="warning">↓5%</font>
    - **好评率**: 98.5% <font color="info">↑0.3%</font>
    
    ### 异常告警
    <font color="warning">暂无异常</font>
    
    ### 明日目标
    1. 订单量突破200单
    2. 销售额突破150,000元
    3. 新用户注册30人
    
    ---
    [查看详细报表](https://example.com/report/daily)
    """
    
    result = bot.send_markdown(content)
    print(f"日报发送结果: {result}")


def example_alert_notification():
    """示例2: 系统告警通知"""
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    # 发送告警消息并@运维人员
    content = """🚨 系统告警

[告警级别] 严重
[告警时间] 2025-12-17 15:30:00
[告警主机] web-server-01
[告警内容] CPU使用率持续超过90%

请运维人员立即处理！"""
    
    # @指定成员（需要替换为实际的userid）
    result = bot.send_text(content, mentioned_list=["zhangsan", "lisi"])
    print(f"告警发送结果: {result}")


def example_news_feed():
    """示例3: 资讯推送"""
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    # 发送图文消息
    articles = [
        {
            "title": "企业微信3.0正式发布",
            "description": "全新的设计，更强大的功能",
            "url": "https://work.weixin.qq.com/news/1",
            "picurl": "https://work.weixin.qq.com/images/news1.jpg"
        },
        {
            "title": "如何提高团队协作效率",
            "description": "10个实用技巧分享",
            "url": "https://work.weixin.qq.com/news/2",
            "picurl": "https://work.weixin.qq.com/images/news2.jpg"
        }
    ]
    
    result = bot.send_news(articles)
    print(f"资讯发送结果: {result}")


def example_weekly_summary():
    """示例4: 周报汇总"""
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    content = """
    ## 🗓️ 本周工作总结
    > 时间: 2025-12-16 ~ 2025-12-22
    
    ### ✅ 完成事项
    1. 完成用户模块开发（100%）
    2. 优化数据库查询性能（提升40%）
    3. 修复3个严重Bug
    4. 编写API文档（80%）
    
    ### 🚧 进行中
    - 订单模块开发（60%）
    - 单元测试编写（50%）
    
    ### 📅 下周计划
    1. 完成订单模块开发
    2. 进行压力测试
    3. 准备上线部署
    
    ### 📊 数据统计
    - 代码提交: 45次
    - 代码行数: +3200 / -800
    - 工作时长: 48小时
    
    ---
    **工作进度**: <font color="info">83%</font>
    **项目状态**: <font color="info">正常</font>
    """
    
    result = bot.send_markdown(content)
    print(f"周报发送结果: {result}")


def example_build_notification():
    """示例5: CI/CD构建通知"""
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    # 模拟构建成功
    content = """
    ## ✅ 构建成功
    
    **项目**: OpenWechatAI-Core
    **分支**: main
    **提交**: abc123d
    **作者**: 张三
    **时间**: 2025-12-17 16:00:00
    
    **变更文件**: 5个
    **测试覆盖**: 85%
    **构建时长**: 3分28秒
    
    [查看详情](https://ci.example.com/build/123)
    """
    
    result = bot.send_markdown(content)
    print(f"构建通知结果: {result}")


def example_customer_feedback():
    """示例6: 客户反馈通知"""
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    content = """
    ## 💬 新的客户反馈
    
    **客户**: 某某科技有限公司
    **联系人**: 李经理
    **满意度**: ⭐⭐⭐⭐⭐
    
    ### 反馈内容
    产品功能强大，操作简单，客服响应及时，非常满意！希望能增加更多定制化功能。
    
    ### 建议
    1. 增加批量导入功能
    2. 优化移动端体验
    3. 支持更多第三方集成
    
    **优先级**: <font color="warning">中</font>
    **处理状态**: <font color="comment">待处理</font>
    
    [查看详情](https://crm.example.com/feedback/456)
    """
    
    result = bot.send_markdown(content)
    print(f"反馈通知结果: {result}")


def example_scheduled_reminder():
    """示例7: 定时提醒"""
    
    import schedule
    import time
    
    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
    bot = WeWorkWebhookExample(webhook_url)
    
    def morning_reminder():
        """早上提醒"""
        content = "☀️ 早上好！新的一天开始了，今天也要加油哦！"
        bot.send_text(content)
        print("早上提醒已发送")
    
    def afternoon_reminder():
        """下午提醒"""
        content = "☕ 下午茶时间到了，休息一下，补充能量！"
        bot.send_text(content)
        print("下午提醒已发送")
    
    def evening_reminder():
        """晚上提醒"""
        content = "🌙 下班时间到了，记得整理工作日志，明天见！"
        bot.send_text(content)
        print("晚上提醒已发送")
    
    # 设置定时任务
    schedule.every().day.at("09:00").do(morning_reminder)
    schedule.every().day.at("15:00").do(afternoon_reminder)
    schedule.every().day.at("18:00").do(evening_reminder)
    
    print("定时提醒已启动...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    print("企业微信Webhook示例")
    print("=" * 50)
    
    # 运行示例（需要替换为实际的Webhook URL）
    print("\n1. 每日数据报表")
    # example_daily_report()
    
    print("\n2. 系统告警通知")
    # example_alert_notification()
    
    print("\n3. 资讯推送")
    # example_news_feed()
    
    print("\n4. 周报汇总")
    # example_weekly_summary()
    
    print("\n5. CI/CD构建通知")
    # example_build_notification()
    
    print("\n6. 客户反馈通知")
    # example_customer_feedback()
    
    print("\n7. 定时提醒（长期运行）")
    # example_scheduled_reminder()
    
    print("\n提示: 请取消注释相应函数并替换Webhook URL后运行")
