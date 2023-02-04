from datetime import datetime

# 机器人QQ号
bot_qq = 2311406250
# 开发者QQ号
super_qq = [2782383376]
# 退群消息
del_user_msg = ""
# 入群消息
add_user_msg = ""


def admin_change(sub_type, user_id):
    admin_msg = ""
    if sub_type == "set":
        if user_id == bot_qq:
            admin_msg = f"芜湖，咱以后也是管理了~"
        else:
            admin_msg = f"恭喜[CQ:at,qq={user_id}]喜提本群管理~"
    elif sub_type == "unset":
        if user_id == bot_qq:
            admin_msg = f"呜呜，别下咱管理呀QwQ"
        else:
            admin_msg = f"[CQ:at,qq={user_id}]痛失本群管理~"
    return admin_msg


def del_user_bye(add_time, group_id, user_id):
    global groups_all, del_user_msg
    del_time = datetime.fromtimestamp(add_time)
    if user_id in super_qq:
        del_user_msg = f"<{del_time}>@{user_id}恭送主人离开~"
    else:
        del_user_msg = f"<{del_time}>QQ号为：{user_id}的小可爱退群咯，good bye呀，永别了这位朋友~" \
                       f"[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640]"
        return del_user_msg


def add_user_wecome(add_time, group_id, user_id):
    global groups_all, add_user_msg
    add_time = datetime.fromtimestamp(add_time)
    if user_id == bot_qq:
        add_user_msg = f"唔，很荣幸受邀进入贵群~\n" \
                       f"嘤嘤嘤呜呜呜"
    elif user_id in super_qq:
        add_user_msg = f"[CQ:at,qq={user_id}]欢迎主人进群[CQ:face,id=175]"
    else:
        add_user_msg = f"欢迎[CQ:at,qq={user_id}]的加入，加入时间：{add_time}，请在群内积极发言哦~" \
                       f"[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={user_id}&spec=640]"
    return add_user_msg
