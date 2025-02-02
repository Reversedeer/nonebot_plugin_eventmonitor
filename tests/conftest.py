import pytest
from nonebot.adapters.onebot.v11 import Adapter
from nonebot import get_driver, load_plugins


@pytest.fixture(scope="session", autouse=True)
def load_plugin():
    # 加载插件
    load_plugins("nonebot_plugin_eventmonitor")

    # 注册适配器
    driver = get_driver()
    driver.register_adapter(Adapter)


@pytest.fixture
def app():
    from nonebug import App

    return App()
