# 无屏蔽AI插件 - 仅你的主号私聊可回复，群聊@机器人回复，内置你的密钥
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.rule import to_me
import requests

# 你的核心配置（已内置）
SUPER_ADMIN = 2466363558
SELL_GROUP = 1077686695
API_KEY = "sk-YkNPaTdURDh6Z1VsSFJJNkE4MWdJN01kZGtVMg"
API_URL = "https://api.nofiltergpt.com/v1/chat/completions"

# AI请求头配置
AI_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# 注册AI聊天事件
ai_chat = on_message(rule=to_me(), priority=5, block=True)

@ai_chat.handle()
async def ai_reply(bot: Bot, event: Event):
    # 获取用户ID和消息类型
    user_id = int(event.get_user_id())
    msg_type = event.get_event_name()
    user_msg = event.get_plaintext().strip()
    
    # 规则：其他人私聊机器人，无任何回应
    if msg_type == "message.private" and user_id != SUPER_ADMIN:
        return
    
    # 无消息内容时的回复
    if not user_msg:
        await ai_chat.finish(Message("你可以对我说点什么哦～"))
    
    # 调用无屏蔽AI接口
    try:
        ai_data = {
            "model": "nofiltergpt-4",
            "messages": [{"role": "user", "content": user_msg}],
            "temperature": 0.9,
            "max_tokens": 2000
        }
        res = requests.post(API_URL, headers=AI_HEADERS, json=ai_data, timeout=12)
        ai_answer = res.json()["choices"][0]["message"]["content"].strip()
        await ai_chat.finish(Message(ai_answer))
    except:
        await ai_chat.finish(Message("收到啦，再发一次试试～"))
