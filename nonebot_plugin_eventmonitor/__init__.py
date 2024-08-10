"""入口文件"""
import os
import platform
import contextlib

from nonebot.params import ArgStr
from nonebot import get_driver, require
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_notice, on_command
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN

from .utils import utils
from .update import update
from .handle import eventmonitor

require("nonebot_plugin_apscheduler")

from  nonebot_plugin_apscheduler import scheduler

scheduler.add_job(update.auto_check_bot_update, 'cron', hour = 8, misfire_grace_time=600)


driver = get_driver()

@driver.on_bot_connect
async def _() -> None:
    await utils.init()
    await utils.config_check()
    await update.auto_check()

#戳一戳
chuo = on_notice(
    rule=utils._is_poke,
    priority=10,
    block=False,
    handlers=[eventmonitor.chuo]
)
# 群荣誉
qrongyu = on_notice(
    rule=utils._is_rongyu,
    priority=50,
    block=True,
    handlers=[eventmonitor.qrongyu]
)
# 群文件
files = on_notice(
    rule=utils._is_checker,
    priority=50,
    block=True,
    handlers=[eventmonitor.files]
)
# 群员减少
del_user = on_notice(
    rule=utils._is_del_user,
    priority=50,
    block=True,
    handlers=[eventmonitor.del_user]
)
# 群员增加
add_user = on_notice(
    rule=utils._is_add_user,
    priority=50,
    block=True,
    handlers=[eventmonitor.add_user]
)
# 群管理
group_admin = on_notice(
    rule=utils._is_admin_change,
    priority=50,
    block=True,
    handlers=[eventmonitor.admin_chance]
)
# 红包
red_packet = on_notice(
    rule=utils._is_red_packet,
    priority=50,
    block=True,
    handlers=[eventmonitor.hongbao]
)

on_command(
    "开启",
    aliases={"关闭"},
    priority=10,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    block=True,
    handlers=[eventmonitor.switch]
)

on_command(
    "eventstatus",
    aliases={"event配置"},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True,
    handlers=[eventmonitor.state]
)

on_command(
    "更新插件eventmonitor",
    priority=1,
    permission=SUPERUSER,
    block=False,
    handlers=[eventmonitor.check_bot]
)

on_command(
    "event指令帮助",
    aliases={"eventhelp"},
    priority=20,
    block=True,
    handlers=[eventmonitor.usage]
)

restart = on_command(
    "重启",
    aliases={"restart"},
    priority=1,
    permission=SUPERUSER,
    block=True
)

@restart.got(
        "flag",
        prompt="确定是否重启？确定请回复[是|好|确定]（重启失败咱们将失去联系，请谨慎！)")
async def _(flag: str = ArgStr("flag")) -> None:
    if flag.lower() in {"true", "是", "好", "确定"}:
        await restart.send("开始重启..请稍等...")
        open("data/eventmonitor/new_version", "w")
        if str(platform.system()).lower() == "windows":
            import sys
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            os.system("./restart.sh")
    else:
        await restart.send("已取消操作...")


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
            "version": "0.3.2",
            "priority": 50,
        },
    )