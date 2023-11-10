from pathlib import Path

import pytest
from nonebug import App


@pytest.mark.asyncio()
async def test_send(app: App):
    from nonebot_plugin_blockwords.utils import (
        read_filed,
        get_blockwords,
        read_blockwords,
    )

    # 测试屏蔽词从长倒短排序
    assert [len(i) for i in get_blockwords()] == [2, 2, 1, 1]

    # 测试屏蔽词读取

    test_path = Path.cwd()

    # 测试读取txt
    test_txt_path = test_path / "test_read.txt"
    test_txt_path.write_text("鸡\n坤\n太美\n丁真", encoding="utf-8")
    assert read_blockwords(test_txt_path) == ["鸡", "坤", "太美", "丁真"]

    # 测试读取json

    test_json_path = test_path / "test_read.json"
    test_json_path.write_text('["哪里","贵","79元","眉笔"]', encoding="utf-8")
    assert read_blockwords(test_json_path) == ["哪里", "贵", "79元", "眉笔"]

    # 测试读取重复文件
    assert read_blockwords(test_json_path) == []

    # 测试读取全部文件
    read_filed.clear()
    assert not bool(set(read_blockwords(test_path)).difference(
        {"哪里", "贵", "79元", "眉笔", "鸡", "坤", "太美", "丁真"}
    ))

    test_txt_path.unlink(missing_ok=True)
    test_json_path.unlink(missing_ok=True)
