# 机器人QQ号
bot_qq = 2311406250
# 开发者QQ号
super_qq = 2782383376


def monitor_rongyu(honor_type, user_id):
    rely = ""
    # 龙王
    if honor_type == "talkative":
        if user_id == bot_qq:
            rely = f"你们又不行了，本喵喜提龙王~"
        elif user_id == super_qq:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获龙王标识~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获龙王标识~"
    # 群聊之火
    elif honor_type == "performer":
        if user_id == bot_qq:
            pass
        elif user_id == super_qq:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获群聊之火标识~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获群聊之火标识~"
    # 快乐源泉
    elif honor_type == "emotion":
        if user_id == bot_qq:
            pass
        elif user_id == super_qq:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获快乐源泉标识~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获快乐源泉标识~"
    return rely
