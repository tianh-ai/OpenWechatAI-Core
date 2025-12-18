# 贡献指南

感谢您考虑为 OpenWechatAI-Core 做出贡献！

## 🌟 贡献方式

### 1. 报告Bug

如果发现Bug，请[创建Issue](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=bug_report.md)并提供：

- 清晰的问题描述
- 复现步骤
- 预期行为 vs 实际行为
- 环境信息（Python版本、操作系统等）
- 相关日志或截图

### 2. 提出新功能

有好的想法？[创建Feature Request](https://github.com/tianh-ai/OpenWechatAI-Core/issues/new?template=feature_request.md)并说明：

- 功能描述和使用场景
- 为什么需要这个功能
- 可能的实现方案

### 3. 提交代码

1. **Fork项目** - 点击右上角的Fork按钮

2. **克隆仓库**
   ```bash
   git clone https://github.com/YOUR_USERNAME/OpenWechatAI-Core.git
   cd OpenWechatAI-Core
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **设置开发环境**
   ```bash
   # 安装依赖
   pip install -r requirements.txt
   
   # 安装开发依赖
   pip install pytest flake8 black
   ```

5. **编写代码**
   - 遵循现有的代码风格
   - 添加必要的注释和文档字符串
   - 确保代码通过lint检查
   ```bash
   # 格式化代码
   black .
   
   # 检查代码风格
   flake8 .
   ```

6. **编写测试**
   ```bash
   # 运行测试
   pytest tests/
   
   # 查看测试覆盖率
   pytest --cov=. tests/
   ```

7. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加XXX功能"
   ```
   
   提交信息格式：
   - `feat:` - 新功能
   - `fix:` - Bug修复
   - `docs:` - 文档更新
   - `style:` - 代码格式调整
   - `refactor:` - 重构
   - `test:` - 测试相关
   - `chore:` - 构建/工具相关

8. **推送到Fork仓库**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **创建Pull Request**
   - 访问原仓库
   - 点击"New Pull Request"
   - 选择你的分支
   - 填写PR描述（使用模板）
   - 提交PR

## 📝 代码规范

### Python代码风格

遵循 [PEP 8](https://pep8.org/) 规范：

```python
# 好的示例
def send_message(content: str, platform: str = "wework") -> dict:
    """
    发送消息到指定平台
    
    Args:
        content: 消息内容
        platform: 平台名称（wework/feishu/dingtalk）
    
    Returns:
        发送结果字典
    """
    # 实现逻辑
    pass


# 不好的示例
def sendMsg(c,p="wework"):
    # 没有文档字符串，参数名不清晰
    pass
```

### 文档字符串

使用Google风格的文档字符串：

```python
def example_function(param1: str, param2: int) -> bool:
    """
    简短的功能描述（一行）
    
    详细的功能描述（如果需要）
    可以多行
    
    Args:
        param1: 参数1的说明
        param2: 参数2的说明
    
    Returns:
        返回值的说明
    
    Raises:
        ValueError: 什么情况下抛出
        TypeError: 什么情况下抛出
    
    Examples:
        >>> example_function("test", 123)
        True
    """
    pass
```

### 命名规范

- **模块名**: 小写字母+下划线，如 `wework_bot.py`
- **类名**: 大驼峰，如 `WeWorkBot`
- **函数名**: 小写字母+下划线，如 `send_message()`
- **常量**: 大写字母+下划线，如 `MAX_RETRIES`
- **变量**: 小写字母+下划线，如 `webhook_url`

### 类型注解

尽可能使用类型注解：

```python
from typing import List, Dict, Optional

def process_messages(
    messages: List[str],
    config: Dict[str, any],
    timeout: Optional[int] = None
) -> bool:
    """处理消息"""
    pass
```

## 🧪 测试要求

### 单元测试

为新功能编写单元测试：

```python
# tests/test_wework_bot.py
import pytest
from wework_bot import WeWorkBot


def test_send_text_success():
    """测试发送文本消息成功"""
    bot = WeWorkBot(webhook_url="http://test.com")
    result = bot.send_text("test message")
    assert result['errcode'] == 0


def test_send_text_with_empty_content():
    """测试发送空内容时抛出异常"""
    bot = WeWorkBot(webhook_url="http://test.com")
    with pytest.raises(ValueError):
        bot.send_text("")
```

### 测试覆盖率

目标：保持80%以上的测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html tests/

# 查看报告
open htmlcov/index.html
```

## 📚 文档要求

### README更新

如果添加了新功能，请更新README：

- 在"核心特性"中添加说明
- 在"快速开始"中添加使用示例
- 更新技术栈（如果需要）

### 示例代码

在`examples/`目录添加示例：

```python
#!/usr/bin/env python3
"""
新功能示例

说明新功能的用途和使用场景
"""

# 导入必要的模块
from your_module import YourClass

# 示例代码
def example_usage():
    """示例使用"""
    # 详细的注释
    obj = YourClass()
    result = obj.do_something()
    print(f"结果: {result}")


if __name__ == "__main__":
    example_usage()
```

### API文档

为新的API端点添加文档：

```markdown
### POST /api/new-endpoint

新端点的描述

**请求参数**:
- `param1` (string, required): 参数1说明
- `param2` (integer, optional): 参数2说明

**请求示例**:
\```bash
curl -X POST http://localhost:8000/api/new-endpoint \
  -H "Content-Type: application/json" \
  -d '{"param1": "value", "param2": 123}'
\```

**响应示例**:
\```json
{
  "code": 0,
  "message": "success",
  "data": {...}
}
\```
```

## 🔍 代码审查

Pull Request会经过以下审查：

1. **功能完整性** - 是否实现了预期功能
2. **代码质量** - 是否符合规范，是否有明显问题
3. **测试覆盖** - 是否有足够的测试
4. **文档完整** - 是否更新了相关文档
5. **向后兼容** - 是否破坏了现有功能

## 🎯 开发优先级

当前需要帮助的领域：

### 高优先级
- [ ] 提高单元测试覆盖率（当前约60%）
- [ ] 性能优化和压力测试
- [ ] 错误处理和异常捕获优化
- [ ] 日志系统完善

### 中优先级
- [ ] 支持更多企业通信平台（Slack、Teams等）
- [ ] Web界面功能增强
- [ ] 消息模板系统
- [ ] 定时任务调度

### 低优先级
- [ ] 多语言支持（国际化）
- [ ] Docker容器化部署
- [ ] Kubernetes部署方案
- [ ] 监控和告警集成

## 💡 开发技巧

### 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 使用Python调试器
import pdb; pdb.set_trace()

# 或使用IPython调试器
from IPython import embed; embed()
```

### 本地测试MCP服务器

```bash
# 启动测试服务器
python enterprise_comm_mcp/mcp_server.py

# 在另一个终端测试API
curl http://localhost:8000/health

# 运行自动化测试
python test_enterprise_mcp.py
```

### 测试Webhook

使用[webhook.site](https://webhook.site/)测试Webhook：

1. 访问 https://webhook.site/
2. 获取唯一URL
3. 配置为Webhook地址
4. 查看接收到的请求

## 🤝 社区行为准则

### 友好和尊重
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 专注于对社区最有利的事情

### 不可接受的行为
- 使用性别化语言或图像
- 恶意攻击、侮辱或贬损评论
- 骚扰，无论是公开还是私下

### 报告问题
如果遇到不当行为，请联系项目维护者。

## 📧 联系方式

- **Issues**: [GitHub Issues](https://github.com/tianh-ai/OpenWechatAI-Core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tianh-ai/OpenWechatAI-Core/discussions)
- **Email**: 项目维护者邮箱

## 🙏 致谢

感谢所有贡献者！

特别感谢：
- 提出宝贵建议的用户
- 提交Bug报告的用户
- 贡献代码的开发者
- 完善文档的贡献者

你的贡献让这个项目变得更好！❤️

---

再次感谢您的贡献！🎉
