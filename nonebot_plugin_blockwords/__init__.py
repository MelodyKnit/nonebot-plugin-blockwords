from functools import partial

from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot.internal.matcher import Matcher
from nonebot.adapters import Bot, Event, Message
from nonebot.params import CommandArg, CommandStart, EventPlainText

from .hook import send_hook
from .check import find_blockword
from .config import Config, driver, plugin_config
from .matcher import blockwords_status, blockwords_matcher


@blockwords_matcher.handle()
async def _(
    matcher: Matcher,
    state: T_State,
    event: Event,
    text: str = EventPlainText(),
):
    if plugin_config.blockwords_user and (blockwords := find_blockword(text)):
        state["_blockwords"] = blockwords
        user_id = event.get_user_id()
        logger.warning(f"[{user_id}] 用户触发屏蔽词: {text}")
        if plugin_config.blockwords_stop_propagation:
            matcher.stop_propagation()
    else:
        await matcher.finish()


@blockwords_status.handle()
async def _(matcher: Matcher, msg: Message = CommandArg(), start: str = CommandStart()):
    txt = msg.extract_plain_text().strip()
    if (status := txt == "开启" if txt in ["开启", "关闭"] else None) is not None:
        if start.startswith("用户"):
            plugin_config.blockwords_user = status
            await matcher.finish(f"用户屏蔽词{txt}")
        else:
            plugin_config.blockwords_bot = status
            await matcher.finish(f"机器人屏蔽词{txt}")


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
