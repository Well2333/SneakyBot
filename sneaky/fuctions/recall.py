from nonebot.adapters.onebot.v11 import (
    Bot,
    FriendRecallNoticeEvent,
    GroupRecallNoticeEvent,
)
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import on_notice

from .. import config
from ..utils import get_info_header, send_msg


def check_msg(msg: str):
    # 如果是闪照, 则不发送
    if "CQ:image" in msg and "type=flash" in msg:
        return False
    # 如果开启 image_only, 则不包含 CQ:image 的消息不发送
    return "CQ:image" in msg if config.recall_image_only else False


recall = on_notice(block=False)


@recall.handle()
async def _(bot: Bot, event: GroupRecallNoticeEvent):
    msg = (await bot.get_msg(message_id=event.message_id))["message"]
    if check_msg(str(msg)):
        await send_msg(
            bot,
            [
                Message(
                    await get_info_header(bot, "撤回", event.user_id, event.group_id)
                ),
                Message(msg),
            ],
        )


@recall.handle()
async def _(bot: Bot, event: FriendRecallNoticeEvent):
    msg = (await bot.get_msg(message_id=event.message_id))["message"]
    if check_msg(str(msg)):
        await send_msg(
            bot,
            [Message(await get_info_header(bot, "撤回", event.user_id)), Message(msg)],
        )
