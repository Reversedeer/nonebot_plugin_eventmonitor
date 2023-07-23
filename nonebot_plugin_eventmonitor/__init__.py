import contextlib

from .utils import *



#初始化配置配置文件
@driver.on_bot_connect
async def _():
    await init(g_temp)
    await config_check()


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
            "version": "0.1.8",
            "priority": 50,
        },
    )