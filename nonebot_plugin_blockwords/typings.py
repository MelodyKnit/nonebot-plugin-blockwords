from typing_extensions import TypeAlias
from typing import Union, Callable, Awaitable

from nonebot.adapters import Event as BaseEvent
from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

Message: TypeAlias = Union[str, BaseMessage, BaseMessageSegment]
BotSendFilter: TypeAlias = Callable[[BaseEvent, Message], Awaitable[Message]]
