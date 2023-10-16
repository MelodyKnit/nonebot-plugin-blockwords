from nonebot.permission import SUPERUSER
from nonebot import on_command, on_message

from .config import plugin_config

blockwords_matcher = on_message(block=False, priority=plugin_config.blockwords_priority)
blockwords_status = on_command(
    "屏蔽词",
    aliases={"用户屏蔽词", "机器人屏蔽词"},
    block=True,
    priority=plugin_config.blockwords_priority,
    permission=SUPERUSER,
)


__all__ = ["blockwords_matcher"]
