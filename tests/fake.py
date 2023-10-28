from typing import Union
from datetime import datetime

from nonechat.info import User
from nonebot.adapters.console import Message, MessageEvent


def make_event(self_id: str, message: Union[str, Message]) -> MessageEvent:
    return MessageEvent(
        time=datetime.now(),
        self_id=self_id,
        user=User(id="111"),
        message=Message(message),
    )
