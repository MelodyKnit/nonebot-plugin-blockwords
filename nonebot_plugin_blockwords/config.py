from typing import List, Union, Optional

from nonebot import get_driver
from pydantic import Extra, BaseModel

driver = get_driver()


class Config(BaseModel, extra=Extra.ignore):
    blockwords: List[str] = []  # env中自定义屏蔽词
    blockwords_file: Union[str, List[str]] = []  # 屏蔽词文件路径
    blockwords_priority = 0  # 屏蔽词检查优先级
    blockwords_replace: Optional[str] = None  # 屏蔽词替换字符，不填写时触发屏蔽词时机器人将会不发送消息
    blockwords_use_jieba: bool = False  # 使用jieba分词的方式检查是否触发屏蔽词
    blockwords_bot: bool = True  # 检查机器人发送的消息
    blockwords_user: bool = False  # 检查用户发送的消息
    blockwords_stop_propagation: bool = True  # 用户触发屏蔽词后是否向继续向下传递


plugin_config = Config.parse_obj(driver.config.dict())
