import pytest
from nonebot import require, get_driver
from nonebug import NONEBOT_INIT_KWARGS
from nonebot.adapters.console import Adapter as ConsoleAdapter


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~none",
        "log_level": "DEBUG",
        "blockwords": ["鸡", "坤", "太美", "丁真"],
        "blockwords_user": True,
        "blockwords_replace": "*",
    }


@pytest.fixture(scope="session", autouse=True)
def load_bot():
    driver = get_driver()
    driver.register_adapter(ConsoleAdapter)

    require("nonebot_plugin_blockwords")
    return None
