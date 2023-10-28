import pytest
from nonebug import App
from nonebot import get_adapter
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.internal.matcher import Matcher
from nonebot.adapters.console import Bot, Adapter, Message

from .fake import make_event


@pytest.mark.asyncio()
async def test_send(app: App):
    from nonebot import on_command

    echo = on_command("echo", priority=1)

    @echo.handle()
    async def echo_handle(matcher: Matcher, msg: Message = CommandArg()):
        await matcher.finish(msg)

    async with app.test_matcher(echo) as ctx:
        adapter = get_adapter(Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = make_event(bot.self_id, "/echo 鸡你太美")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, Message("*你**"), result=None)
        ctx.should_finished(echo)
