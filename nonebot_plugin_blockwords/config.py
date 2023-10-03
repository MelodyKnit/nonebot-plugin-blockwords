from typing import List, Union, Optional

from nonebot import get_driver
from pydantic import Extra, BaseModel
from nonebot.plugin import PluginMetadata
from nonebot_plugin_localstore import get_data_dir

driver = get_driver()


class Config(BaseModel, extra=Extra.ignore):
    blockwords: List[str] = []  # env中自定义屏蔽词
    blockwords_file: Union[str, List[str]] = []  # 屏蔽词文件路径
    blockwords_priority = 0  # 屏蔽词检查优先级
    blockwords_replace: Optional[str] = None  # 屏蔽词替换字符，不填写时触发屏蔽词时机器人将会不发送消息
    blockwords_use_jieba: bool = True  # 使用jieba分词的方式检查是否触发屏蔽词
    blockwords_bot: bool = True  # 检查机器人发送的消息
    blockwords_user: bool = False  # 检查用户发送的消息
    blockwords_stop_propagation: bool = True  # 用户触发屏蔽词后是否向继续向下传递


__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_blockwords",
    description="接收的消息或机器人发送的消息进行屏蔽词检查",
    usage="屏蔽词开关：屏蔽词 开启/关闭\n",
    config=Config,
)

plugin_config = Config.parse_obj(driver.config.dict())
data_dir = get_data_dir(__plugin_meta__.name)
default_blockwords_dir = data_dir / "blockwords"
