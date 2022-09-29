from nonebot.adapters.onebot.v11 import (
    Bot,
    FriendRecallNoticeEvent,
    GroupRecallNoticeEvent,
)
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import on_notice

from ..utils import get_info_header, send_msg

recall = on_notice(block=False)


@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    msg = (await bot.get_msg(message_id=event.message_id))["message"]
    if "type=flash" in msg and "CQ:image" in msg:
        return
    await send_msg(
        bot,
        [
            Message(await get_info_header(bot, "撤回", event.user_id, event.group_id)),
            Message(msg),
        ],
    )


@recall.handle()
async def _(bot: Bot, event: FriendRecallNoticeEvent):
    msg = (await bot.get_msg(message_id=event.message_id))["message"]
    if "type=flash" in msg and "CQ:image" in msg:
        return
    await send_msg(
        bot, [Message(await get_info_header(bot, "撤回", event.user_id)), Message(msg)]
    )
