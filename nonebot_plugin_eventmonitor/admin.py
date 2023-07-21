from datetime import datetime
from .utils import superusers


async def admin_changer(sub_type, user_id, bot_qq) : 
    admin_msg = ""

    if sub_type == "set":
        admin_msg = (
            "我也是管理啦，你们要小心喵~"
            if user_id == bot_qq
            else f"🚔 管理员变动\n恭喜[CQ:at,qq={user_id}]喜提本群管理喵~"
        )
    elif sub_type == "unset":
        admin_msg = (
            "呜呜，别下咱管理呀QwQ，喵呜~"
            if user_id == bot_qq
            else f"🚔 管理员变动\n[CQ:at,qq={user_id}]痛失本群管理喵~"
        )
    return admin_msg

async def del_user_bye(add_time, user_id):
    global del_user_msg
    del_time = datetime.fromtimestamp(add_time)
    if user_id in superusers:
        del_user_msg = f"⌈{del_time}⌋\n@{user_id}恭送主人离开喵~"
        print(superusers)
    else:
        del_user_msg = f"✈️ 成员变动⌈{del_time}⌋\nQQ号为：{user_id}的小可爱退群喵~" \
                       f"[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640]"
        return del_user_msg

async def add_user_wecome(add_time, user_id, bot_qq):
    global groups_all, add_user_msg
    add_time = datetime.fromtimestamp(add_time)
    if user_id == bot_qq:
        add_user_msg = f"本喵被邀进入贵群喵~\n" \
                       f"火速上个管理喵~"
    elif user_id in superusers:
        add_user_msg = f"✨ 成员变动 ✨\n@{user_id}[CQ:at,qq={user_id}]欢迎主人进群喵~[CQ:face,id=175]"
    else:
        add_user_msg = f"✨ 成员变动 ✨\n欢迎[CQ:at,qq={user_id}]的加入喵~\n加入时间：⌈{add_time}⌋，请在群内积极发言喵~" \
                       f"[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640]"
    return add_user_msg
