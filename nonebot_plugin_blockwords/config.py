from typing import List, Union, Optional

from nonebot import get_driver
from pydantic import Extra, BaseModel
from nonebot.plugin import PluginMetadata
from nonebot_plugin_localstore import get_data_dir

driver = get_driver()


class Config(BaseModel, extra=Extra.ignore):
    blockwords: List[str] = []
    blockwords_file: Union[str, List[str]] = []
    blockwords_status: bool = True
    blockwords_priority = 0
    blockword_replace: Optional[str] = None


__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_blockwords",
    description="接收的消息或机器人发送的消息进行屏蔽词检查",
    usage="",
    config=Config,
)

plugin_config = Config.parse_obj(driver.config.dict())
data_dir = get_data_dir(__plugin_meta__.name)
default_blockwords_dir = data_dir / "blockwords"
