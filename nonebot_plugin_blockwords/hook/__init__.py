from typing import Type

from nonebot.log import logger
from nonebot.adapters import Event as BaseEvent

from ..config import plugin_config
from ..check import blockword_exists, blockword_replace
from .bot import send_hook, on_bot_send, clear_send_hook
from ..exception import StopSendMessage, FinishSendMessage
from ..typings import Message, BaseMessage, BaseMessageSegment


@on_bot_send
async def _blockwords_replace(
    _: BaseEvent,
    message: Message,
) -> Message:
    """屏蔽词过滤器"""
    if plugin_config.blockwords_replace is None:
        return message  # 会将消息返回到下一个过滤器
    if isinstance(message, str):
        message = blockword_replace(message)
    elif isinstance(message, BaseMessage):
        new_message = message.copy()
        new_message.clear()
        for msg in message:
            if isinstance(msg, BaseMessageSegment) and msg.is_text():
                new_message += blockword_replace(
                    msg.get_message_class()(msg).extract_plain_text()
                )
            else:
                new_message += msg
        message = new_message
    elif isinstance(message, BaseMessageSegment) and message.is_text():
        message_class: Type[BaseMessage] = message.get_message_class()
        message = message_class(
            blockword_replace(message_class(message).extract_plain_text())
        )
    raise FinishSendMessage(message)    # 将过滤后的消息让机器人发送出去


@on_bot_send
async def _blockwords_stop(
    _: BaseEvent,
    message: Message,
) -> Message:
    """屏蔽词过滤器"""
    text = message
    if isinstance(message, BaseMessage):
        text = message.extract_plain_text()
    elif isinstance(message, BaseMessageSegment) and message.is_text():
        text = message.get_message_class()(message).extract_plain_text()

    if isinstance(text, str) and blockword_exists(text):
        logger.warning(f"屏蔽词触发停止发送消息: {text}")
        raise StopSendMessage
    return message


__all__ = [
    "send_hook",
    "on_bot_send",
    "clear_send_hook",
]
