def test_plugin_loaded():
    # 检测插件是否成功加载
    from nonebot import get_plugin

    assert get_plugin("nonebot_plugin_eventmonitor") is not None
