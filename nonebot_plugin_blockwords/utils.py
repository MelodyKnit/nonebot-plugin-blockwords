import json
from pathlib import Path
from typing import List, Union, Callable

from nonebot.log import logger
from nonebot.adapters import Message, MessageSegment

from .config import plugin_config, default_blockwords_dir


def message_liter(message: Union[str, "Message", "MessageSegment"]):
    def _(func: Callable[[str], str]):
        if isinstance(message, str):
            func(message)
        elif isinstance(message, Message):
            for msg in message:
                if isinstance(msg, MessageSegment) and msg.is_text():
                    func(msg.get_message_class()(msg).extract_plain_text())

    return _


def get_blockword() -> List[str]:
    """获取屏蔽词

    在配置文件中没有配置blockwords_file时，会读取默认的屏蔽词文件夹中的所有文件

    Returns:
        List[str]: 屏蔽词列表
    """
    words = plugin_config.blockwords.copy()
    if isinstance(plugin_config.blockwords_file, str):
        words.extend(read_words(Path(plugin_config.blockwords_file)))
        logger.success(f"读取屏蔽词文件 << {plugin_config.blockwords_file}")
    elif isinstance(plugin_config.blockwords_file, list):
        for file_path in plugin_config.blockwords_file:
            words.extend(read_words(Path(file_path)))
            logger.success(f"读取屏蔽词文件 << {file_path}")
    else:
        for file_path in default_blockwords_dir.iterdir():
            words.extend(read_words(file_path))
            logger.success(f"读取屏蔽词文件 << {file_path}")
    words = list(set(words))  # 去重
    words.sort(key=len, reverse=True)  # 按长度排序
    return words


def read_words(file_path: Path) -> List[str]:
    text = file_path.read_text(encoding="utf-8")
    try:
        words = json.loads(text)
        if isinstance(words, list):
            return words
        logger.error(f"{file_path} 屏蔽词文件格式并不是一个 list")
    except ValueError:
        return text.split("\n")
    return []
