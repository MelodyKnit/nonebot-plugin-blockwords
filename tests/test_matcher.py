from typing import List, Optional

import pytest
from nonebug import App
from nonebot import get_adapter
from nonebot.internal.matcher import Matcher
from nonebot.adapters.console import Bot, Adapter

from .fake import make_event


@pytest.mark.asyncio()
async def test_send(app: App):
    from nonebot_plugin_blockwords.params import BlockWords
    from nonebot_plugin_blockwords import blockwords_matcher

    @blockwords_matcher.handle()
    async def _(matcher: Matcher, blockwords: List[str] = BlockWords):
        await matcher.finish("不许说脏话[%s]" % ", ".join(blockwords))

    async with app.test_matcher(blockwords_matcher) as ctx:
        adapter = get_adapter(Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        # 测试发送屏蔽词
        event = make_event(bot.self_id, "鸡你太美")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "不许说脏话[*, **]", result=None)  # 被拦截

        # 测试发送非屏蔽词
        event = make_event(bot.self_id, "好的")
        ctx.receive_event(bot, event)

        ctx.should_finished(blockwords_matcher)
