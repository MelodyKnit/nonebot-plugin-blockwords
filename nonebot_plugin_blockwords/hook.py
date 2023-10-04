from typing import Any, Type, Union

from nonebot.log import logger
from nonebot.adapters import Event, Message, MessageSegment

from .config import plugin_config
from .check import blockword_exists, blockword_replace


async def send_hook(
    send,
    event: "Event",
    message: Union[str, "Message", "MessageSegment"],
    **kwargs: Any,
):
    if not plugin_config.blockwords_bot:
        return await send(event, message, **kwargs)

    if plugin_config.blockwords_replace is not None:  # 是否带有替换字符
        if isinstance(message, str):
            message = blockword_replace(message)
        elif isinstance(message, Message):
            new_message = message.copy()
            new_message.clear()
            for msg in message:
                if isinstance(msg, MessageSegment) and msg.is_text():
                    new_message += blockword_replace(
                        msg.get_message_class()(msg).extract_plain_text()
                    )
                else:
                    new_message.append(msg)
            message = new_message
        elif isinstance(message, MessageSegment) and message.is_text():
            message_class: Type[Message] = message.get_message_class()
            message = message_class(
                blockword_replace(message_class(message).extract_plain_text())
            )
        await send(event, message, **kwargs)
    else:
        text = message
        if isinstance(message, Message):
            text = message.extract_plain_text()
        elif isinstance(message, MessageSegment) and message.is_text():
            text = message.get_message_class()(message).extract_plain_text()
        if isinstance(text, str) and blockword_exists(text):
            logger.warning(f"屏蔽词触发停止发送消息: {text}")
            return
        await send(event, message, **kwargs)
