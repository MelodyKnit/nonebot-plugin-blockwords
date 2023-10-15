from .typings import Message


class BaseException(Exception):
    ...


class FinishFilter(BaseException):
    """完成消息过滤，并发送当前消息"""

    def __init__(self, message: Message) -> None:
        """停止消息过滤并且发送消息

        Args:
            message (Message): 需要发送的消息
        """
        self.message: Message = message


class StopSendMessage(BaseException):
    """停止发送消息的异常"""


class SendMessage(BaseException):
    def __init__(self, message: Message) -> None:
        """停止消息过滤并且发送消息

        Args:
            message (Message): 需要发送的消息
        """
        self.message: Message = message
