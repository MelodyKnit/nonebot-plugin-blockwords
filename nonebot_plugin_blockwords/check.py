from jieba import cut

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
    if plugin_config.blockword_use_jieba:
        word = set(cut(text, cut_all=True)) & set(blockwords)
        return bool(word)
    else:
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
    if plugin_config.blockword_replace is None:
        return text
    if plugin_config.blockword_use_jieba:
        word = list(cut(text, cut_all=True))
        blockword = set(word) & set(blockwords)
        if blockword:
            for i, w in enumerate(word):
                if w in blockword:
                    word[i] = plugin_config.blockword_replace * len(w)
        return "".join(word)
    else:
        if plugin_config.blockword_replace is not None:
            for word in blockwords:
                text = text.replace(word, plugin_config.blockword_replace * len(word))
    return text
