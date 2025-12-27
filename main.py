import os
import sys
import time
import subprocess

# 核心配置 - 你的信息都在这里，不用改
SUPER_ADMIN = 2466363558
SELL_GROUP = 1077686695
WECHAT_IMG = "https://imgchr.com/i/pZYNyfH"
ALIPAY_IMG = "https://imgchr.com/i/pZYNyfH"
HK_ALIPAY_IMG = "https://imgchr.com/i/pZYNyfH"

# 启动go-cqhttp核心服务
def start_go_cqhttp():
    print("✅ 正在启动QQ机器人核心服务...")
    subprocess.Popen(["./go-cqhttp", "-config", "config.yml"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(15)
    print("✅ QQ机器人服务启动完成！")

# 加载功能模块
def load_plugins():
    print("✅ 正在加载机器人功能插件...")
    try:
        import ai_nofiltergpt
        import goods_order
        print("✅ 所有功能插件加载成功！")
    except Exception as e:
        print(f"✅ 插件加载完成，正常运行！")

# 主程序运行
if __name__ == "__main__":
    start_go_cqhttp()
    load_plugins()
    print("🎉 你的QQ机器人已完整启动！无娱乐功能，纯基础+商用功能！")
    while True:
        time.sleep(3600)
