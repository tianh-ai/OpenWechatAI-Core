"""
FastAPI服务入口
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models import get_db, Message, Rule, User
from models.message import MessageStatus
from core.logging_config import setup_logging

# 初始化日志
setup_logging()

# 创建FastAPI应用
app = FastAPI(
    title="OpenWechatAI API",
    description="微信自动化AI助手API",
    version="1.0.0"
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 数据模型
class MessageCreate(BaseModel):
    platform: str
    sender: str
    receiver: str
    content: str
    message_type: str = "text"


class MessageResponse(BaseModel):
    id: int
    platform: str
    sender: str
    content: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class RuleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    priority: int
    enabled: bool
    trigger_count: int
    
    class Config:
        from_attributes = True


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# 消息接口
@app.get("/api/messages", response_model=List[MessageResponse])
async def list_messages(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取消息列表"""
    query = db.query(Message)
    
    if status:
        query = query.filter(Message.status == status)
    
    messages = query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    return messages


@app.get("/api/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: Session = Depends(get_db)):
    """获取单条消息"""
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message


# 规则接口
@app.get("/api/rules", response_model=List[RuleResponse])
async def list_rules(db: Session = Depends(get_db)):
    """获取规则列表"""
    rules = db.query(Rule).order_by(Rule.priority.desc()).all()
    return rules


@app.patch("/api/rules/{rule_id}/toggle")
async def toggle_rule(rule_id: int, db: Session = Depends(get_db)):
    """切换规则启用状态"""
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    rule.enabled = not rule.enabled
    db.commit()
    
    return {"id": rule.id, "enabled": rule.enabled}


# 统计接口
@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """获取统计信息"""
    total_messages = db.query(Message).count()
    pending_messages = db.query(Message).filter(Message.status == MessageStatus.PENDING).count()
    total_users = db.query(User).count()
    total_rules = db.query(Rule).count()
    active_rules = db.query(Rule).filter(Rule.enabled == True).count()
    
    return {
        "total_messages": total_messages,
        "pending_messages": pending_messages,
        "total_users": total_users,
        "total_rules": total_rules,
        "active_rules": active_rules
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
