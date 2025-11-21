#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Agent Manager for OpenWechatAI
管理AI代理的创建、配置和协调
"""

import json
import os
from typing import Dict, Any, Optional


class AgentManager:
    """AI代理管理器"""
    
    def __init__(self, config_path: str = "config/agents.json"):
        """
        初始化代理管理器
        
        Args:
            config_path: 代理配置文件路径
        """
        self.config_path = config_path
        self.agents: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """加载代理配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.agents = json.load(f)
            else:
                # 默认配置
                self.agents = {
                    "daily_report_agent": {
                        "name": "日报生成代理",
                        "model": "deepseek-chat",
                        "prompt_template": "请为以下员工生成今日工作日报总结：\n员工姓名：{name}\n今日聊天记录：\n{messages}",
                        "enabled": True
                    },
                    "task_analysis_agent": {
                        "name": "任务分析代理",
                        "model": "deepseek-chat",
                        "prompt_template": "请分析以下任务信息并提供优化建议：\n{task_info}",
                        "enabled": True
                    }
                }
                self.save_config()
        except Exception as e:
            print(f"加载配置时出错: {e}")
            self.agents = {}
    
    def save_config(self) -> None:
        """保存代理配置"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.agents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置时出错: {e}")
    
    def create_agent(self, agent_id: str, config: Dict[str, Any]) -> None:
        """
        创建新的AI代理
        
        Args:
            agent_id: 代理ID
            config: 代理配置
        """
        self.agents[agent_id] = config
        self.save_config()
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        获取代理配置
        
        Args:
            agent_id: 代理ID
            
        Returns:
            代理配置或None
        """
        return self.agents.get(agent_id)
    
    def update_agent(self, agent_id: str, config: Dict[str, Any]) -> bool:
        """
        更新代理配置
        
        Args:
            agent_id: 代理ID
            config: 新的配置
            
        Returns:
            更新是否成功
        """
        if agent_id in self.agents:
            self.agents[agent_id].update(config)
            self.save_config()
            return True
        return False
    
    def delete_agent(self, agent_id: str) -> bool:
        """
        删除代理
        
        Args:
            agent_id: 代理ID
            
        Returns:
            删除是否成功
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.save_config()
            return True
        return False
    
    def list_agents(self) -> Dict[str, Any]:
        """
        列出所有代理
        
        Returns:
            所有代理配置
        """
        return self.agents.copy()


# 示例使用
if __name__ == "__main__":
    # 创建代理管理器实例
    manager = AgentManager()
    
    # 显示所有代理
    print("当前代理列表:")
    for agent_id, config in manager.list_agents().items():
        print(f"- {agent_id}: {config['name']}")