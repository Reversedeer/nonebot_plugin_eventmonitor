import nonebot


try:
    bot_qq = nonebot.get_driver().config.bot_qq
except:
    bot_qq = "寄"

try:
    super_qq = nonebot.get_driver().config.superusers
except:
    super_qq = "寄"



def monitor_rongyu(honor_type, user_id):
    rely = ""

    if honor_type == "talkative":
        if user_id == bot_qq:
            rely = f"你们又不行了，本喵喜提龙王~"
        elif user_id == super_qq:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获龙王标识喵~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获龙王标识喵~"

    elif honor_type == "performer":
        if user_id == bot_qq:
            pass
        elif user_id == super_qq:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获群聊之火标识喵~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获群聊之火标识喵~"

    elif honor_type == "emotion":
        if user_id == bot_qq:
            pass
        elif user_id == super_qq:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获快乐源泉标识喵~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获快乐源泉标识喵~"
    return rely
