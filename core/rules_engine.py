"""
规则引擎 - 解析和执行YAML规则
"""
import yaml
import re
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, time
from loguru import logger
from models import Rule, RuleLog, get_db_context
import json


class RuleCondition:
    """规则条件"""
    
    def __init__(self, config: Dict[str, Any]):
        self.platform = config.get("platform")
        self.sender = config.get("sender")
        self.content_contains = config.get("content_contains")
        self.content_regex = config.get("content_regex")
        self.time_range = config.get("time_range")
    
    def matches(self, message: Dict[str, Any]) -> bool:
        """检查消息是否匹配条件"""
        # 平台匹配
        if self.platform and message.get("platform") != self.platform:
            return False
        
        # 发送者匹配（支持正则）
        if self.sender:
            sender = message.get("sender", "")
            if not re.match(self.sender, sender):
                return False
        
        # 内容包含
        if self.content_contains:
            content = message.get("content", "")
            if self.content_contains not in content:
                return False
        
        # 内容正则匹配
        if self.content_regex:
            content = message.get("content", "")
            if not re.search(self.content_regex, content):
                return False
        
        # 时间范围匹配
        if self.time_range:
            if not self._check_time_range(self.time_range):
                return False
        
        return True
    
    def _check_time_range(self, time_range: str) -> bool:
        """检查当前时间是否在指定范围内"""
        try:
            start_str, end_str = time_range.split("-")
            start_time = datetime.strptime(start_str.strip(), "%H:%M").time()
            end_time = datetime.strptime(end_str.strip(), "%H:%M").time()
            current_time = datetime.now().time()
            
            if start_time <= end_time:
                return start_time <= current_time <= end_time
            else:  # 跨越午夜
                return current_time >= start_time or current_time <= end_time
        except Exception as e:
            logger.error(f"时间范围解析失败: {e}")
            return False


class RuleAction:
    """规则动作"""
    
    def __init__(self, config: Dict[str, Any]):
        self.action_type = config.get("action", "auto_reply")
        self.message = config.get("message")
        self.message_template = config.get("message_template")
        self.skill = config.get("skill")
        self.use_ai = config.get("use_ai", False)
        self.ai_model = config.get("ai_model", "gpt-4")
        self.ai_prompt = config.get("ai_prompt")
        self.target = config.get("target")
        self.notify_channels = config.get("notify_channels", [])
    
    def execute(self, message: Dict[str, Any], platform) -> Dict[str, Any]:
        """执行动作"""
        if self.action_type == "auto_reply":
            return self._auto_reply(message, platform)
        elif self.action_type == "forward":
            return self._forward(message, platform)
        elif self.action_type == "notify":
            return self._notify(message, platform)
        else:
            logger.warning(f"未知的动作类型: {self.action_type}")
            return {"status": "error", "message": "Unknown action type"}
    
    def _auto_reply(self, message: Dict[str, Any], platform) -> Dict[str, Any]:
        """自动回复"""
        sender = message.get("sender")
        
        # 确定回复内容
        if self.message:
            reply_content = self.message
        elif self.message_template:
            reply_content = self.message_template.format(**message)
        elif self.use_ai:
            # AI回复（待实现AI集成）
            reply_content = f"[AI回复] 收到您的消息: {message.get('content', '')[:50]}"
        else:
            reply_content = "收到您的消息"
        
        # 发送回复
        try:
            platform.send_message(sender, reply_content)
            logger.info(f"自动回复成功: {sender}")
            return {"status": "success", "action": "auto_reply"}
        except Exception as e:
            logger.error(f"自动回复失败: {e}")
            return {"status": "error", "message": str(e)}
    
    def _forward(self, message: Dict[str, Any], platform) -> Dict[str, Any]:
        """转发消息"""
        if not self.target:
            return {"status": "error", "message": "No target specified"}
        
        forward_content = self.message_template.format(**message) if self.message_template else message.get("content")
        
        try:
            platform.send_message(self.target, forward_content)
            logger.info(f"消息已转发到: {self.target}")
            return {"status": "success", "action": "forward"}
        except Exception as e:
            logger.error(f"转发失败: {e}")
            return {"status": "error", "message": str(e)}
    
    def _notify(self, message: Dict[str, Any], platform) -> Dict[str, Any]:
        """发送通知"""
        logger.info(f"发送通知: {self.notify_channels}")
        # 通知功能待实现
        return {"status": "success", "action": "notify"}


class RuleDefinition:
    """规则定义"""
    
    def __init__(self, config: Dict[str, Any]):
        self.name = config.get("name", "unnamed_rule")
        self.description = config.get("description", "")
        self.priority = config.get("priority", 0)
        self.enabled = config.get("enabled", True)
        
        self.condition = RuleCondition(config.get("if", {}))
        self.action = RuleAction(config.get("then", {}))
    
    def matches(self, message: Dict[str, Any]) -> bool:
        """检查是否匹配"""
        if not self.enabled:
            return False
        return self.condition.matches(message)
    
    def execute(self, message: Dict[str, Any], platform) -> Dict[str, Any]:
        """执行规则"""
        return self.action.execute(message, platform)


class RulesEngine:
    """规则引擎"""
    
    def __init__(self, rules_dir: str = "rules"):
        self.rules_dir = Path(rules_dir)
        self.rules: List[RuleDefinition] = []
        self.load_rules()
    
    def load_rules(self):
        """从YAML文件加载规则"""
        self.rules.clear()
        
        if not self.rules_dir.exists():
            logger.warning(f"规则目录不存在: {self.rules_dir}")
            self.rules_dir.mkdir(parents=True, exist_ok=True)
            return
        
        for rule_file in self.rules_dir.glob("*.yaml"):
            try:
                with open(rule_file, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                
                if isinstance(config, list):
                    for rule_config in config:
                        self.rules.append(RuleDefinition(rule_config))
                else:
                    self.rules.append(RuleDefinition(config))
                
                logger.info(f"已加载规则文件: {rule_file.name}")
            except Exception as e:
                logger.error(f"加载规则文件失败 {rule_file}: {e}")
        
        # 按优先级排序（高优先级在前）
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        logger.success(f"共加载 {len(self.rules)} 条规则")
    
    def reload(self):
        """重新加载规则"""
        logger.info("重新加载规则...")
        self.load_rules()
    
    def find_matching_rules(self, message: Dict[str, Any]) -> List[RuleDefinition]:
        """查找匹配的规则"""
        matching_rules = []
        for rule in self.rules:
            try:
                if rule.matches(message):
                    matching_rules.append(rule)
                    logger.debug(f"规则匹配: {rule.name}")
            except Exception as e:
                logger.error(f"规则匹配检查失败 {rule.name}: {e}")
        
        return matching_rules
    
    def execute_rules(self, message: Dict[str, Any], platform) -> List[Dict[str, Any]]:
        """
        执行匹配的规则
        
        Args:
            message: 消息字典
            platform: 平台实例
            
        Returns:
            执行结果列表
        """
        matching_rules = self.find_matching_rules(message)
        
        if not matching_rules:
            logger.debug("没有匹配的规则")
            return []
        
        results = []
        for rule in matching_rules:
            try:
                logger.info(f"执行规则: {rule.name}")
                result = rule.execute(message, platform)
                result["rule_name"] = rule.name
                results.append(result)
                
                # 记录到数据库（可选）
                self._log_rule_execution(rule, message, result)
                
            except Exception as e:
                logger.error(f"规则执行失败 {rule.name}: {e}", exc_info=True)
                results.append({
                    "status": "error",
                    "rule_name": rule.name,
                    "message": str(e)
                })
        
        return results
    
    def _log_rule_execution(self, rule: RuleDefinition, message: Dict[str, Any], result: Dict[str, Any]):
        """记录规则执行日志到数据库"""
        try:
            with get_db_context() as db:
                # 查找或创建规则记录
                db_rule = db.query(Rule).filter_by(name=rule.name).first()
                if not db_rule:
                    db_rule = Rule(
                        name=rule.name,
                        description=rule.description,
                        priority=rule.priority,
                        enabled=rule.enabled,
                        conditions={},  # 简化
                        actions={}
                    )
                    db.add(db_rule)
                    db.flush()
                
                # 更新统计
                db_rule.trigger_count += 1
                if result.get("status") == "success":
                    db_rule.success_count += 1
                else:
                    db_rule.failure_count += 1
                db_rule.last_triggered_at = datetime.utcnow()
                
                # 创建日志
                log = RuleLog(
                    rule_id=db_rule.id,
                    message_content=message.get("content", "")[:500],
                    matched=True,
                    executed=True,
                    success=result.get("status") == "success",
                    execution_result=result,
                    error_message=result.get("message") if result.get("status") == "error" else None
                )
                db.add(log)
                
        except Exception as e:
            logger.error(f"规则日志记录失败: {e}")


# 全局规则引擎实例
rules_engine = RulesEngine()


def get_rules_engine() -> RulesEngine:
    """获取全局规则引擎实例"""
    return rules_engine
