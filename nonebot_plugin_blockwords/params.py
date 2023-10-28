from typing import List, Optional

from nonebot.typing import T_State
from nonebot.params import Depends, EventPlainText

from .check import find_blockword


async def _find_blockword(text: str = EventPlainText()) -> List[str]:
    return find_blockword(text)


FindBlockWords = Depends(_find_blockword)


async def _blockwords(state: T_State) -> Optional[List[str]]:
    """具体的屏蔽词内容"""
    return state.get("_blockwords")


BlockWords = Depends(_blockwords)
