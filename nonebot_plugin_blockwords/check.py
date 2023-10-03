from typing import List, Union, Iterable

from jieba import cut

from .utils import get_blockword
from .config import plugin_config

blockwords = get_blockword()


def find_blockword(text: Union[str, Iterable[str]]) -> List[str]:
    """获取屏蔽词文本

    Args:
        text (str): 要检查的文本

    Returns:
        List[str]: 存在的屏蔽词
    """
    if isinstance(text, str):
        if not plugin_config.blockwords_use_jieba:
            return [i for i in blockwords if i in text]
        text = cut(text)
    return list(set(text) & set(blockwords))


def blockword_exists(text: str) -> bool:
    """是否存在屏蔽词

    Args:
        text (str): 要检查的文本

    Returns:
        bool: 是否存在
    """
    if plugin_config.blockwords_use_jieba:
        return bool(find_blockword(text))
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
    if plugin_config.blockwords_replace is None:
        raise ValueError("缺少`blockwords_replace`配置项")
    if plugin_config.blockwords_use_jieba:
        word_segmentation = list(cut(text))
        if word := find_blockword(word_segmentation):
            for i, w in enumerate(word_segmentation):
                if w in word:
                    word_segmentation[i] = plugin_config.blockwords_replace * len(w)
        return "".join(word_segmentation)
    else:
        for word in find_blockword(text):
            text = text.replace(word, plugin_config.blockwords_replace * len(word))
    return text
