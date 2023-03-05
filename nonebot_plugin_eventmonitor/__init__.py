from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.plugin import on_notice

from nonebot.adapters.onebot.v11 import (
    Bot, Event, Message,
    PokeNotifyEvent,
    HonorNotifyEvent,
    GroupMessageEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupAdminNoticeEvent,
    LuckyKingNotifyEvent
)

from .stamp import *
from .honour import *
from .admin import *


try:
    cd_time = nonebot.get_driver().config.cd_time       # 从配置文件中读取cd_time
except:
    cd_time = 0      		# cd默认值

chuo_cd_dir = {}

# 获取戳一戳状态
async def _is_poke(event: Event, state: T_State) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()


# 获取群荣誉变更
async def _is_rongyu(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, HonorNotifyEvent)


# 获取文件上传
async def _is_checker(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupUploadNoticeEvent)


# 群成员减少
async def _is_del_user(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupDecreaseNoticeEvent)


# 群成员增加
async def _is_add_user(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)


# 管理员变动
async def _is_admin_change(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupAdminNoticeEvent)


# 红包运气王
async def _is_red_packet(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, LuckyKingNotifyEvent)


# 戳一戳
chuo = on_notice(Rule(_is_poke), priority=50, block=True)
# 群荣誉
qrongyu = on_notice(Rule(_is_rongyu), priority=50, block=True)
# 群文件
files = on_notice(Rule(_is_checker), priority=50, block=True)
# 群员减少
del_user = on_notice(Rule(_is_del_user), priority=50, block=True)
# 群员增加
add_user = on_notice(Rule(_is_add_user), priority=50, block=True)
# 群管理
group_admin = on_notice(Rule(_is_admin_change), priority=50, block=True)
# 红包
red_packet = on_notice(Rule(_is_red_packet), priority=50, block=True)


@chuo.handle()
async def send_chuo(bot: Bot, event: Event, state: T_State):
    if bot_name == "寄":
        await chuo.finish("请先配置bot_name")
    uid = event.get_user_id()    # 获取用户id
    try:
        cd = event.time - chuo_cd_dir[uid]                             # 计算cd
    except KeyError:
        cd = cd_time + 1                                        # 没有记录则cd为cd_time+1
    if (
        cd > cd_time
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                     # 记录cd
        chuo_cd_dir.update({uid: event.time})
    rely_msg = chuo_send_msg()
    await chuo.finish(message=Message(rely_msg))


@qrongyu.handle()
async def send_rongyu(bot: Bot, event: HonorNotifyEvent, state: T_State):
    if bot_qq == "寄":
        await qrongyu.finish("请先配置bot_qq")
    if super_qq == "寄":
        await qrongyu.finish("请先配置SUPERUSERS")
    rely_msg = monitor_rongyu(event.honor_type, event.user_id)
    await qrongyu.finish(message=Message(rely_msg))


@files.handle()
async def handle_first_receive(bot: Bot, event: GroupUploadNoticeEvent, state: T_State):
    rely = f'[CQ:at,qq={event.user_id}]\n' \
           f'[CQ:image,file=https://q4.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=640]' \
           f'\n 上传了新文件，感谢你一直为群里做贡献喵~[CQ:face,id=175]'
    await files.finish(message=Message(rely))


@del_user.handle()
async def user_bye(bot: Bot, event: GroupDecreaseNoticeEvent, state: T_State):
    rely_msg = del_user_bye(event.time, event.group_id, event.user_id)
    await del_user.finish(message=Message(rely_msg))


@add_user.handle()
async def user_welcome(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    rely_msg = add_user_wecome(event.time, event.group_id, event.user_id)
    await add_user.finish(message=Message(rely_msg))


@group_admin.handle()
async def admin_chance(bot: Bot, event: GroupAdminNoticeEvent, state: T_State):
    rely_msg = admin_changer(event.sub_type, event.user_id)
    await group_admin.finish(message=Message(rely_msg))

@red_packet.handle()
async def hongbao(bot: Bot, event: LuckyKingNotifyEvent, state: T_State):
    rely_msg = f"[CQ:at,qq={event.user_id}]\n本次红包运气王为：[CQ:at,qq={event.target_id}]"
    await red_packet.finish(message=Message(rely_msg))
