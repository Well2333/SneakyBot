import contextlib

from nonebot import on_message
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.adapters.onebot.v11.message import Message

from ..utils import get_info_header, send_msg, get_image_link


async def _checker(bot: Bot, event: Event) -> bool:
    msg = str(event.get_message())
    return "type=flash" in msg and "CQ:image" in msg


flashimg = on_message(rule=_checker, block=False)


@flashimg.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    msg = str(event.get_message()).replace(",type=flash", "")

    await send_msg(
        bot,
        [
            Message(await get_info_header(bot, "闪照", event.user_id, event.group_id)),
            Message(msg),
            Message(await get_image_link(bot, event)),
        ],
    )


@flashimg.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    msg = str(event.get_message()).replace(",type=flash", "")

    await send_msg(
        bot,
        [
            Message(await get_info_header(bot, "闪照", event.user_id)),
            Message(msg),
            Message(await get_image_link(bot, event)),
        ],
    )
