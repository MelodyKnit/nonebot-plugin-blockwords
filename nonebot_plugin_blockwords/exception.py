from .typings import Message


class BaseException(Exception):
    ...


class StopSendMessage(BaseException):
    """停止发送消息的异常"""


class FinishSendMessage(BaseException):
    """在此完成消息过滤并且发送消息"""

    def __init__(self, message: Message) -> None:
        """停止消息过滤并且发送消息

        Args:
            message (Message): 需要发送的消息
        """
        self.message: Message = message


class PauseSendMessage(BaseException):
    def __init__(self, message: Message) -> None:
        """停止消息过滤并且发送消息

        以下例子两条都会发送

        ```python
        @on_bot_send
        async def _(event: Event, message: Message) -> Message:
            # do something
            raise PauseSendMessage(message)

        @on_bot_send
        async def _(event: Event, message: Message) -> Message:
            # do something
            raise PauseSendMessage(message)
        ```

        Args:
            message (Message): 需要发送的消息
        """
        self.message: Message = message
