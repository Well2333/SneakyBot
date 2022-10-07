from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import on_message
from nonebot.rule import to_me

from .. import config
from ..utils import get_info_header, send_msg, get_image_link

at_tome = on_message(rule=to_me(), block=False)


@at_tome.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await send_msg(
        bot,
        [
            Message(await get_info_header(bot, "at个人", event.user_id, event.group_id)),
            event.get_message(),
            *(await get_image_link(bot, event.get_message())),
        ],
    )


async def is_all(event: GroupMessageEvent):
    if not config.at_all:
        return False
    if "qq=all" in str(event.get_message()):
        return True


at_all = on_message(rule=is_all, block=False)


@at_all.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await send_msg(
        bot,
        [
            Message(await get_info_header(bot, "at全体", event.user_id, event.group_id)),
            event.get_message(),
            *(await get_image_link(bot, event.get_message())),
        ],
    )
