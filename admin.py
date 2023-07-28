from datetime import datetime
from .utils import superusers


async def admin_changer(sub_type, user_id, bot_qq) : 
    admin_msg = ""
    
    # 根据管理员变动类型选择不同的消息
    if sub_type == "set":
        # 如果用户ID等于机器人的QQ号，返回特定消息
        admin_msg = (
            "我也是管理啦，你们要小心喵~"
            if user_id == bot_qq
            else f"🚔 管理员变动\n恭喜@{user_id}喜提本群管理喵~"
        )
    elif sub_type == "unset":
        # 如果用户ID等于机器人的QQ号，返回特定消息
        admin_msg = (
            "呜呜，别下咱管理呀QwQ，喵呜~"
            if user_id == bot_qq
            else f"🚔 管理员变动\n@{user_id}痛失本群管理喵~"
        )
        
    return admin_msg


async def del_user_bye(add_time, user_id):
    global del_user_msg
    del_time = datetime.fromtimestamp(add_time)
    
    # 检查用户ID是否在超级用户列表superusers中
    if user_id in superusers:
        # 如果是超级用户，生成特定的离开消息
        del_user_msg = f"⌈{del_time}⌋\n@{user_id}恭送主人离开喵~"
    else:
        # 如果不是超级用户，生成通用的离开消息，包含用户的QQ号和头像图片
        del_user_msg = f"✈️ 成员变动 ✈️ \n时间: ⌈{del_time}⌋\nQQ号为：{user_id}的小可爱退群喵~" \
                       f"[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640]"
                       
        return del_user_msg


async def add_user_wecome(add_time, user_id, bot_qq):
    global groups_all, add_user_msg   
    # 将时间戳转换为datetime类型的时间add_time
    add_time = datetime.fromtimestamp(add_time) 
    # 判断用户ID是否等于机器人的QQ号
    if user_id == bot_qq:
        # 如果是机器人自己加入群组，生成特定的欢迎消息
        add_user_msg = f"本喵被邀进入贵群喵~\n" \
                       f"火速上个管理喵~"
    # 判断用户ID是否在超级用户列表superusers中
    elif user_id in superusers:
        # 如果是超级用户加入群组，生成特定的欢迎消息，包含用户ID和CQ表情
        add_user_msg = f"✨ 成员变动 ✨\n@{user_id}欢迎主人进群喵~[CQ:face,id=175]"
    else:
        # 如果是普通用户加入群组，生成通用的欢迎消息，包含用户ID、加入时间和用户头像图片的链接
        add_user_msg = f"✨ 成员变动 ✨\n欢迎@{user_id}的加入喵~\n加入时间：⌈{add_time}⌋，请在群内积极发言喵~" \
                       f"[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640]"
    return add_user_msg

