from functools import partial
from typing import Any, Type, Union

from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message
from nonebot.internal.matcher import Matcher
from nonebot.adapters import Bot, Event, Message, MessageSegment
from nonebot.params import CommandArg, CommandStart, EventPlainText

from .config import Config, driver, plugin_config
from .check import blockword_exists, blockword_replace

blockwords_matcher = on_message(block=False, priority=plugin_config.blockwords_priority)
blockwords_status = on_command(
    "屏蔽词",
    aliases={"用户屏蔽词", "机器人屏蔽词"},
    block=True,
    priority=plugin_config.blockwords_priority,
    permission=SUPERUSER,
)


@blockwords_matcher.handle()
async def _(
    matcher: Matcher,
    event: Event,
    text: str = EventPlainText(),
):
    if plugin_config.blockwords_user and blockword_exists(text):
        user_id = event.get_user_id()
        logger.warning(f"[{user_id}] 用户触发屏蔽词: {text}")
        if plugin_config.blockwords_stop_propagation:
            matcher.stop_propagation()
    else:
        await matcher.finish()


@blockwords_status.handle()
async def _(matcher: Matcher, msg: Message = CommandArg(), start: str = CommandStart()):
    txt = msg.extract_plain_text()
    if start.startswith("用户"):
        if txt == "开启":
            plugin_config.blockwords_user = True
            await matcher.finish("用户屏蔽词开启")
        elif txt == "关闭":
            plugin_config.blockwords_user = False
            await matcher.finish("用户屏蔽词关闭")
        else:
            await matcher.finish("用户屏蔽词开关：屏蔽词 开启/关闭\n")
    else:
        if txt == "开启":
            plugin_config.blockwords_bot = True
            await matcher.finish("机器人屏蔽词开启")
        elif txt == "关闭":
            plugin_config.blockwords_bot = False
            await matcher.finish("机器人屏蔽词关闭")


async def send_hook(
    send,
    event: "Event",
    message: Union[str, "Message", "MessageSegment"],
    **kwargs: Any,
):
    if plugin_config.blockwords_bot:
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
    else:
        await send(event, message, **kwargs)


@driver.on_bot_connect
async def _(bot: Bot):
    bot.send = partial(send_hook, bot.send)


__plugin_meta__ = PluginMetadata(
    name="屏蔽词插件",
    description="接收的消息或机器人发送的消息进行屏蔽词检查",
    usage="屏蔽词开关：屏蔽词 开启/关闭\n",
    type="application",
    config=Config,
    homepage="https://github.com/MelodyKnit/nonebot-plugin-blockwords",
    supported_adapters=None,
)
