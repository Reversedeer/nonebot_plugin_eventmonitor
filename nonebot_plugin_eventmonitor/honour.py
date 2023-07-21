from .utils import superusers


async def monitor_rongyu(honor_type, user_id, bot_qq):  
    rely = ""

    if honor_type == "emotion":
        if user_id == bot_qq:
            pass
        elif user_id in superusers:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获快乐源泉🤣标识喵~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获快乐源泉🤣标识喵~"
    elif honor_type == "performer":
        if user_id == bot_qq:
            pass
        elif user_id in superusers:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获群聊之火🔥标识喵~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获群聊之火🔥标识喵~"

    elif honor_type == "talkative":
        if user_id == bot_qq:
            rely = "你们又不行了，本喵喜提龙王🐲~"
        elif user_id in superusers:
            rely = f"[CQ:at,qq={user_id}]恭喜主人荣获龙王🐲标识喵~"
        else:
            rely = f"恭喜[CQ:at,qq={user_id}]荣获龙王🐲标识喵~"

    return rely
