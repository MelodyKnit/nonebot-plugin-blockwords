import json
from pathlib import Path
from typing import List, Optional

from genericpath import isdir
from nonebot.log import logger

from .config import plugin_config

global_words: Optional[List[str]] = None
read_filed: List[Path] = []


def get_blockwords() -> List[str]:
    """获取屏蔽词

    在配置文件中没有配置blockwords_file时，会读取默认的屏蔽词文件夹中的所有文件

    Returns:
        List[str]: 屏蔽词列表
    """
    global global_words
    if global_words is None:
        words = plugin_config.blockwords.copy()
        if isinstance(plugin_config.blockwords_file, str):
            words: List[str] = read_blockwords(
                Path(plugin_config.blockwords_file))
        elif isinstance(plugin_config.blockwords_file, list):
            for file_path in plugin_config.blockwords_file:
                words.extend(read_blockwords(Path(file_path)))
        global_words = sorted(set(words), key=len, reverse=True)
    return global_words


def read_file_blockwords(file_path: Path) -> List[str]:
    """读取文件屏蔽词

    如果文件是`.json`格式结尾就会进行`json`解析

    如果文件是`.txt`格式结尾就会按行读取

    Args:
        file_path (Path): 文件路径

    Returns:
        List[str]: 屏蔽词内容
    """
    if file_path not in read_filed:
        read_filed.append(file_path)
        text = file_path.read_text(encoding="utf-8")
        logger.success(f"读取屏蔽词文件 << {file_path}")
        try:
            if file_path.suffix == ".json":
                if isinstance(words := json.loads(text), list):
                    return words
                logger.error(f"{file_path} 屏蔽词文件格式并不是一个 list")
            else:
                return text.split("\n")
        except ValueError:
            logger.error(f"{file_path} 屏蔽词文件格式错误")
    else:
        logger.warning(f"{file_path} 屏蔽词文件已读取过")
    return []


def read_blockwords(file_path: Path) -> List[str]:
    """读取屏蔽词

    传入路径后回递归读取文件夹中的所有`.json`和`.txt`文件

    Args:
        file_path (Path): 文件或文件夹路径

    Returns:
        List[str]: 屏蔽词
    """
    if file_path.is_dir():
        bk = []
        for file in file_path.iterdir():
            bk.extend(read_blockwords(file))
        return bk
    elif file_path.suffix in [".json", ".txt"]:
        return read_file_blockwords(file_path)
    return []
