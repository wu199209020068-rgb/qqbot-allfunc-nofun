from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.rule import to_me
import random

# 你的核心配置 全部内置 不用改
SUPER_ADMIN = 2466363558
SELL_GROUP = 1077686695
WECHAT_IMG = "https://imgchr.com/i/pZYNyfH"
ALIPAY_IMG = "https://imgchr.com/i/pZYNyfH"
HK_ALIPAY_IMG = "https://imgchr.com/i/pZYNyfH"
PAY_KEY = "YkNPaTdURDh6Z1VsSFJJNkE4MWdJN01kZGtVMg"

# 商品列表
goods_list = {
    "GTA5线上金币": 68,
    "游戏加速月卡": 198,
    "PS5游戏代购": 399
}

# 指令注册 - 商品查询
goods_cmd = on_command("商品", rule=to_me(), priority=5, block=True)
# 指令注册 - 下单
order_cmd = on_command("下单", rule=to_me(), priority=5, block=True)
# 指令注册 - 上传商品(仅你可用)
add_cmd = on_command("上传商品", rule=to_me(), priority=3, block=True)
# 自动识别收款码
pay_cmd = on_message(rule=to_me(), priority=6, block=True)

# 查看商品列表
@goods_cmd.handle()
async def show_goods(bot: Bot, event: Event):
    group_id = int(event.group_id) if hasattr(event, 'group_id') else 0
    if group_id != SELL_GROUP and group_id != 0:
        await goods_cmd.finish(Message("本群无商品服务"))
    msg = "🛒 商品列表 \n"
    for name, price in goods_list.items():
        msg += f"• {name} - ¥{price}\n"
    msg += "📌 下单格式：@机器人 下单 商品名 数量"
    await goods_cmd.finish(Message(msg))

# 下单功能
@order_cmd.handle()
async def create_order(bot: Bot, event: Event):
    group_id = int(event.group_id) if hasattr(event, 'group_id') else 0
    user_id = int(event.get_user_id())
    if group_id != SELL_GROUP:
        await order_cmd.finish(Message("本群无下单权限"))
    msg = event.get_plaintext().strip().split()
    if len(msg) < 2:
        await order_cmd.finish(Message("❌ 格式错误！正确：@机器人 下单 商品名 数量"))
    goods_name = msg[1]
    num = int(msg[2]) if len(msg)>=3 else 1
    if goods_name not in goods_list:
        await order_cmd.finish(Message(f"❌ 商品【{goods_name}】不存在！"))
    total = goods_list[goods_name] * num
    order_id = random.randint(100000,999999)
    # 群内回复
    await bot.send_group_msg(group_id=group_id, message=f"✅ 下单成功！\n订单号：{order_id}\n总价：¥{total}\n支付码已发私信！")
    # 私信买家收款码
    private_msg = f"📝 你的订单详情\n订单号：{order_id}\n商品：{goods_name} × {num}\n总价：¥{total}\n\n✅ 微信收款码：\n[CQ:image,file={WECHAT_IMG}]\n✅ 支付宝收款码：\n[CQ:image,file={ALIPAY_IMG}]\n✅ 港版支付宝收款码：\n[CQ:image,file={HK_ALIPAY_IMG}]"
    await bot.send_private_msg(user_id=user_id, message=private_msg)
    # 私信你（管理员）订单信息
    await bot.send_private_msg(user_id=SUPER_ADMIN, message=f"🔔 新订单提醒\n订单号：{order_id}\n买家ID：{user_id}\n商品：{goods_name} × {num}\n总价：¥{total}")

# 自动识别收款码请求
@pay_cmd.handle()
async def pay_recognize(bot: Bot, event: Event):
    user_msg = event.get_plaintext().strip()
    if "微信" in user_msg:
        await pay_cmd.finish(Message(f"✅ 微信收款码：\n[CQ:image,file={WECHAT_IMG}]"))
    elif "支付宝" in user_msg and "港版" not in user_msg:
        await pay_cmd.finish(Message(f"✅ 支付宝收款码：\n[CQ:image,file={ALIPAY_IMG}]"))
    elif "港版支付宝" in user_msg:
        await pay_cmd.finish(Message(f"✅ 港版支付宝收款码：\n[CQ:image,file={HK_ALIPAY_IMG}]"))

# 管理员专属：上传商品
@add_cmd.handle()
async def add_goods(bot: Bot, event: Event):
    user_id = int(event.get_user_id())
    if user_id != SUPER_ADMIN:
        await add_cmd.finish(Message("❌ 无操作权限！"))
    msg = event.get_plaintext().strip().split()
    if len(msg) < 3:
        await add_cmd.finish(Message("✅ 格式：@机器人 上传商品 商品名 价格"))
    goods_list[msg[1]] = int(msg[2])
    await add_cmd.finish(Message(f"✅ 商品【{msg[1]}】已添加，价格¥{msg[2]}"))
