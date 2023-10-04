import re
from typing import List, Union, Iterable

from jieba import cut

from .utils import get_blockword
from .config import plugin_config

blockwords = get_blockword()
pattern = "|".join(re.escape(w) for w in blockwords)
regex = re.compile(rf"(?:{pattern})")


def replace_text(text: str) -> str:
    if plugin_config.blockwords_replace is None:
        raise ValueError("缺少`blockwords_replace`配置项")
    return plugin_config.blockwords_replace * len(text)


def find_blockword(text: Union[str, Iterable[str]]) -> List[str]:
    """获取屏蔽词文本

    Args:
        text (str): 要检查的文本

    Returns:
        List[str]: 存在的屏蔽词
    """
    if isinstance(text, str):
        if not plugin_config.blockwords_use_jieba:
            return regex.findall(text)
        text = cut(text, cut_all=False)
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
    return bool(regex.search(text))


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
        word_segmentation = list(cut(text, cut_all=False))
        if word := find_blockword(word_segmentation):
            for i, w in enumerate(word_segmentation):  # 使用jieba分词后，替换屏蔽词
                if w in word:
                    word_segmentation[i] = replace_text(w)
        return "".join(word_segmentation)
    return regex.sub(lambda m: replace_text(m.group(0)), text)  # type: ignore
