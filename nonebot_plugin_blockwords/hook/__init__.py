from typing import Any, List, Type

from nonebot.log import logger
from nonebot.adapters import Event as BaseEvent

from ..config import plugin_config
from ..check import blockword_exists, blockword_replace
from ..exception import StopSendMessage, PauseSendMessage, FinishSendMessage
from ..typings import Message, BaseMessage, BotSendFilter, BaseMessageSegment

_bot_send_hooks: List[BotSendFilter] = []


def on_bot_send(func: BotSendFilter) -> BotSendFilter:
    """注册一个 bot send hook

    ```python
    @on_bot_send
    async def _(event: Event, message: Message) -> Message:
        # do something
        return message
    ```
    """
    _bot_send_hooks.append(func)
    return func


def clear_send_hook() -> None:
    """清空所有 bot send hook"""
    _bot_send_hooks.clear()


async def send_hook(
    send,
    event: BaseEvent,
    message: Message,
    **kwargs: Any,
):
    if not plugin_config.blockwords_bot:
        return await send(event, message, **kwargs)
    for hook in _bot_send_hooks:
        try:
            message = await hook(event, message, **kwargs)
        except FinishSendMessage as err:
            return await send(event, err.message, **kwargs)
        except PauseSendMessage as err:
            await send(event, err.message, **kwargs)
        except StopSendMessage:
            break
        except Exception as err:
            logger.opt(colors=True, exception=err).error(
                "<r><bg #f8bbd0>Error in bot send hook</bg #f8bbd0></r>"
            )
            raise err
    else:
        return await send(event, message, **kwargs)


@on_bot_send
async def _blockwords_replace(
    _: BaseEvent,
    message: Message,
) -> Message:
    """屏蔽词过滤器"""
    if plugin_config.blockwords_replace is not None:
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
        raise FinishSendMessage(message)
    return message


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
