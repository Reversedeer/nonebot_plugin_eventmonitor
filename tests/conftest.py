import pytest
from nonebot import get_driver, load_plugins
from nonebug.app import App
from nonebot.adapters.onebot.v11 import Adapter


@pytest.fixture(scope='session', autouse=True)
def load_plugin() -> None:
    load_plugins('nonebot_plugin_eventmonitor')

    driver = get_driver()
    driver.register_adapter(Adapter)


@pytest.fixture
def app() -> App:
    from nonebug import App

    return App()
