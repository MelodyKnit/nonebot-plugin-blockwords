from typing import Any, List

from nonebot.log import logger
from nonebot.adapters import Event as BaseEvent

from ..config import plugin_config
from ..typings import Message, BotSendFilter
from ..exception import StopSendMessage, PauseSendMessage, FinishSendMessage

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
