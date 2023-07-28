import contextlib
import nonebot

from nonebot.rule import Rule
from nonebot.matcher import Matcher
from nonebot.plugin import on_notice, on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import (
    Bot, Event, Message,
    PokeNotifyEvent,
    HonorNotifyEvent,
    GroupUploadNoticeEvent,
    GroupDecreaseNoticeEvent,
    GroupIncreaseNoticeEvent,
    GroupAdminNoticeEvent,
    LuckyKingNotifyEvent,
    MessageSegment,
    GroupMessageEvent
)

from .stamp import chuo_send_msg
from .honour import monitor_rongyu
from .admin import del_user_bye, add_user_wecome, admin_changer
from .utils import *

# 获取戳一戳状态
async def _is_poke(event: Event) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()
# 获取群荣誉变更
async def _is_rongyu(event: Event) -> bool:
    return isinstance(event, HonorNotifyEvent)
# 获取文件上传
async def _is_checker(event: Event) -> bool:
    return isinstance(event, GroupUploadNoticeEvent)
# 群成员减少
async def _is_del_user(event: Event) -> bool:
    return isinstance(event, GroupDecreaseNoticeEvent)
# 群成员增加
async def _is_add_user(event: Event) -> bool:
    return isinstance(event, GroupIncreaseNoticeEvent)
# 管理员变动
async def _is_admin_change(event: Event) -> bool:
    return isinstance(event, GroupAdminNoticeEvent)
# 红包运气王
async def _is_red_packet(event: Event) -> bool:
    return isinstance(event, LuckyKingNotifyEvent)

# 戳一戳
chuo = on_notice(
    Rule(_is_poke),
    priority=50,
    block=True
)
# 群荣誉
qrongyu = on_notice(
    Rule(_is_rongyu),
    priority=50,
    block=True
)
# 群文件
files = on_notice(
    Rule(_is_checker),
    priority=50,
    block=True
)
# 群员减少
del_user = on_notice(
    Rule(_is_del_user),
    priority=50,
    block=True
)
# 群员增加
add_user = on_notice(
    Rule(_is_add_user),
    priority=50,
    block=True
)
# 群管理
group_admin = on_notice(
    Rule(_is_admin_change),
    priority=50,
    block=True
)
# 红包
red_packet = on_notice(
    Rule(_is_red_packet),
    priority=50,
    block=True
)
# 功能开关
switch_command = on_command(
    "开启",
    aliases={"关闭"}, 
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True
)
#功能状态
state = on_command(
    "event配置",
    aliases={"event状态"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True
)

#初始化配置配置文件
@driver.on_bot_connect
async def _():
    await init(g_temp)
    await config_check()

@chuo.handle()
async def send_chuo(event: PokeNotifyEvent):
    if not (await check_chuo(g_temp, str(event.group_id))):
        await chuo.finish(notAllow, at_sender=True)
    # 获取用户id    
    uid = event.get_user_id()
    # 计算cd                                                       
    try:
        cd = event.time - chuo_CD_dir[uid]                                          
    except KeyError:
        # 没有记录则cd为cd_time+1
        cd = chuo_cd + 1                                                            
    if (
        cd > chuo_cd
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):# 记录cd                                                                                   
        chuo_CD_dir.update({uid: event.time})
    rely_msg = await chuo_send_msg()
    await chuo.finish(message=Message(rely_msg))

#群荣誉变化
@qrongyu.handle()                                                                       
async def send_rongyu(event: HonorNotifyEvent, bot: Bot):
    if not (await check_honor(g_temp, str(event.group_id))):
        return
    bot_qq = int(bot.self_id)
    rely_msg = await monitor_rongyu(event.honor_type, event.user_id, bot_qq)
    await qrongyu.finish(message=Message(rely_msg))

#上传群文件
@files.handle()                                                                         
async def handle_first_receive(event: GroupUploadNoticeEvent):
    if not (await check_file(g_temp, str(event.group_id))):
        return
    rely = MessageSegment.at(event.user_id) + '\n' + \
           MessageSegment.image(f'https://q4.qlogo.cn/headimg_dl?dst_uin={event.user_id}&spec=640') + \
           '\n 上传了新文件，感谢你一直为群里做贡献喵~' + MessageSegment.face(175)
    await files.finish(message=rely)

#退群事件
@del_user.handle()
async def user_bye(event: GroupDecreaseNoticeEvent):
    if not (await check_del_user(g_temp, str(event.group_id))):
        return
    rely_msg = await  del_user_bye(event.time, event.user_id)
    await del_user.finish(message=Message(rely_msg))

#入群事件
@add_user.handle()
async def user_welcome(event: GroupIncreaseNoticeEvent, bot: Bot):
    await config_check()
    if not (await check_add_user(g_temp, str(event.group_id))):
        return
    bot_qq = int(bot.self_id)
    rely_msg = await  add_user_wecome(event.time, event.user_id, bot_qq)
    await add_user.finish(message=Message(rely_msg))

#管理员变动
@group_admin.handle()
async def admin_chance(event: GroupAdminNoticeEvent, bot: Bot):
    if not (await check_admin(g_temp, str(event.group_id))):
        return
    bot_qq = int(bot.self_id)
    rely_msg = await admin_changer(event.sub_type, event.user_id, bot_qq)
    await group_admin.finish(message=Message(rely_msg))
    
#红包运气王
@red_packet.handle()
async def hongbao(event: LuckyKingNotifyEvent):
    if not (await check_red_package(g_temp, str(event.group_id))):
        return
    rely_msg = MessageSegment.at(event.user_id) + "\n" + "本次红包运气王为：" + MessageSegment.at(event.target_id)
    await red_packet.finish(message=rely_msg)

@switch_command.handle()
async def switch(event: GroupMessageEvent, matcher: Matcher):
    # 获取开关指令的参数，即用户输入的指令内容
    command = str(event.get_message()).strip()
    # 获取群组ID
    gid = str(event.group_id)
    # 判断指令是否包含"开启"或"关闭"关键字
    if "开启" in command or "开始" in command:
        if key := get_command_type(command):
            g_temp[gid][key] = True
            write_group_data(g_temp)
            name = get_function_name(key)
            await matcher.finish(f"{name}功能已开启喵")
    elif "禁止" in command or "关闭" in command:
        if key := get_command_type(command):
            g_temp[gid][key] = False
            write_group_data(g_temp)
            name = get_function_name(key)
            await matcher.finish(f"{name}功能已禁用喵")

@state.handle()
async def event_state(event:GroupMessageEvent, matcher: Matcher):
    gid = str(event.group_id)
    with open(address, "r", encoding="utf-8") as f:
        group_status = json.load(f)
    if gid not in group_status:
        await config_check()
    else:
        await matcher.finish(f"群{gid}的Event配置状态：\n" + "\n".join
        (
            [f"{path[func][0]}: {'开启' if group_status[gid][func] else '关闭'}" for func in
            path]
        )
    )


with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata

    __plugin_meta__ = PluginMetadata(
        name="eventmonitor",
        description="监控群事件的插件，支持戳一戳，成员变动，群荣誉变化等提示的插件",
        usage=utils.usage,
        type="application",
        homepage="https://github.com/Reversedeer/nonebot_plugin_eventmonitor",
        supported_adapters={"onebot.v11"},
        extra={
            "author": "Reversedeer",
            "version": "0.2.0",
            "priority": 50,
        },
    )