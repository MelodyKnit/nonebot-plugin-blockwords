from typing import List, Callable

from nonebot.params import Depends, EventPlainText

from .check import find_blockword


async def _find_blockword(text: str = EventPlainText()) -> List[str]:
    return find_blockword(text)


FIND_BLOCKWORD: Callable[..., List[str]] = Depends(_find_blockword)
