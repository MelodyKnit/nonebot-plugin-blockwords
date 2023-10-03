from .utils import get_blockword
from .config import plugin_config

blockwords = get_blockword()


def blockword_exists(text: str) -> bool:
    """是否存在屏蔽词

    Args:
        text (str): 要检查的文本

    Returns:
        bool: 是否存在
    """
    for word in blockwords:
        if word in text:
            return True
    return False


def blockword_replace(text: str) -> str:
    """屏蔽词替换

    Args:
        text (str): 要检查的文本

    Returns:
        str: 将屏蔽词替换为指定字符后的文本
    """
    if plugin_config.blockword_replace is not None:
        for word in blockwords:
            text = text.replace(word, plugin_config.blockword_replace * len(word))
    return text
