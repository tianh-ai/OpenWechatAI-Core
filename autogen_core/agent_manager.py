from autogen_agentchat.agents import UserProxyAgent, AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat


class AgentManager:
    """
    AutoGen 多智能体调度器：
    - 统一管理 Planner / Logic / Doc / Reply / Memory / Image Agents
    - 根据微信群聊/私聊消息分配任务
    - 执行多轮对话直到生成最佳回复
    """

    def __init__(self):
        # ---- 载入模型配置 ----
        self.llm_config_deepseek = {
            "config_list": [{
                "model": "deepseek-reasoner",
                "api_key": "your-deepseek-api-key"  # 需要从配置中获取
            }],
            "temperature": 0.3,
        }

        self.llm_config_qwen = {
            "config_list": [{
                "model": "qwen2.5-72b-instruct",
                "api_key": "your-qwen-api-key"  # 需要从配置中获取
            }],
            "temperature": 0.3,
        }

        # ---- 初始化 Agents ----
        self.planner = AssistantAgent(
            name="planner",
            llm_config=self.llm_config_deepseek,
            system_message="你是一个规划代理，负责制定任务计划。"
        )
        
        self.logic_agent = AssistantAgent(
            name="logic_agent",
            llm_config=self.llm_config_qwen,
            system_message="你是一个逻辑代理，负责处理逻辑推理任务。"
        )
        
        self.doc_agent = AssistantAgent(
            name="doc_agent",
            llm_config=self.llm_config_qwen,
            system_message="你是一个文档代理，负责处理文档相关任务。"
        )
        
        self.reply_agent = AssistantAgent(
            name="reply_agent",
            llm_config=self.llm_config_deepseek,
            system_message="你是一个回复代理，负责生成最终回复。"
        )
        
        self.memory_agent = AssistantAgent(
            name="memory_agent",
            llm_config=self.llm_config_deepseek,
            system_message="你是一个记忆代理，负责管理对话历史。"
        )
        
        self.image_agent = AssistantAgent(
            name="image_agent",
            llm_config=self.llm_config_qwen,
            system_message="你是一个图像代理，负责处理图像相关任务。"
        )

        # 用于用户输入
        self.user_proxy = UserProxyAgent(
            name="user",
            code_execution_config=False
        )

        # ---- 构建 GroupChat ----
        # 使用RoundRobinGroupChat作为替代
        self.group_chat = RoundRobinGroupChat(
            [self.user_proxy, self.planner, self.logic_agent, self.doc_agent, 
             self.reply_agent, self.memory_agent, self.image_agent],
            max_turns=12
        )

    # 主调用入口
    def chat(self, user_message: str):
        """
        微信消息 → 多智能体 → 自动回复内容
        """
        # 在新版本中，我们直接调用group_chat.run()
        result = self.group_chat.run(user_message)
        return result

# 简单测试
if __name__ == "__main__":
    print("AgentManager class defined successfully")