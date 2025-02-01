"""入口文件"""

from nonebot import require, get_driver
from nonebot.plugin import PluginMetadata, on_notice, on_command
from nonebot.permission import SUPERUSER
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11.permission import (
    GROUP_ADMIN,
    GROUP_OWNER,
)

from .config import Config, utils
from .handle import eventmonitor

require('nonebot_plugin_localstore')
require('nonebot_plugin_apscheduler')


driver = get_driver()


@scheduler.scheduled_job('cron', hour=8, misfire_grace_time=600)
async def plugin_update() -> None:
    await eventmonitor.check_plugin()


@driver.on_bot_connect
async def _() -> None:
    await utils.init()
    await eventmonitor.check_plugin()


# 戳一戳
chuo = on_notice(
    rule=utils.poke,
    priority=10,
    block=False,
    handlers=[eventmonitor.chuo],
)
# 群荣誉
qrongyu = on_notice(
    rule=utils.rongyu,
    priority=50,
    block=False,
    handlers=[eventmonitor.qrongyu],
)
# 群文件
files = on_notice(
    rule=utils.checker,
    priority=50,
    block=False,
    handlers=[eventmonitor.files],
)
# 群员减少
del_user = on_notice(
    rule=utils.del_user,
    priority=50,
    block=False,
    handlers=[eventmonitor.del_user],
)
# 群员增加
add_user = on_notice(
    rule=utils.add_user,
    priority=50,
    block=False,
    handlers=[eventmonitor.add_user],
)
# 群管理
group_admin = on_notice(
    rule=utils.admin_change,
    priority=50,
    block=False,
    handlers=[eventmonitor.admin_chance],
)
# 红包
red_packet = on_notice(
    rule=utils.red_packet,
    priority=50,
    block=False,
    handlers=[eventmonitor.hongbao],
)

on_command(
    '开启',
    aliases={'关闭'},
    priority=10,
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    block=True,
    handlers=[eventmonitor.switch],
)

on_command(
    'eventstatus',
    aliases={'event配置'},
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=False,
    handlers=[eventmonitor.state],
)

on_command(
    '检查event更新',
    aliases={'checkeventupdate'},
    priority=1,
    permission=SUPERUSER,
    block=True,
    handlers=[eventmonitor.check_plugin],
)

on_command(
    'event帮助',
    aliases={'eventhelp'},
    priority=20,
    block=False,
    handlers=[eventmonitor.usage],
)


__plugin_meta__ = PluginMetadata(
    name='nonebot-plugin-eventmonitor',
    description='监控群事件的插件，支持戳一戳，成员变动，群荣誉变化等提示的插件',
    usage=utils.usage,
    type='application',
    config=Config,
    homepage='https://github.com/Reversedeer/nonebot_plugin_eventmonitor',
    supported_adapters={'~onebot.v11'},
    extra={
        'author': 'Reversedeer',
        'version': '0.4.1',
        'priority': 50,
        'email': 'ysjvillmark@gmail.com',
    },
)
