import contextlib
from datetime import date, datetime
from pathlib import Path
from typing import List, Union
import re

from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.log import logger

from . import config


async def _get_sender_info(bot: Bot, user_id: int, group_id: int = 0):
    """获取用户的昵称信息"""
    group_name = None
    user_name = None
    if group_id:
        try:
            group_name = (await bot.get_group_info(group_id=group_id))["group_name"]
            user_name = (
                await bot.get_group_member_info(group_id=group_id, user_id=user_id)
            )["nickname"]
        except ActionFailed as e:
            logger.exception(e)
            group_name = group_name or "群信息获取失败"
            user_name = user_name or "群成员获取失败"
    else:
        try:
            for user in await bot.get_friend_list():
                # https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E5%A5%BD%E5%8F%8B%E5%88%97%E8%A1%A8
                if user["user_id"] == user_id:
                    user_name = user["nickname"]
                    break
        except ActionFailed as e:
            logger.exception(e)
            user_name = "好友获取失败"
        group_name = "好友消息"
    return group_name, user_name


async def get_info_header(bot: Bot, infotype: str, user_id: int, group_id: int = 0):
    """构造消息头, 包含事件类型, 时间和发送者信息"""
    group_name, user_name = await _get_sender_info(bot, user_id, group_id)
    return f"{infotype} -- {datetime.now().strftime('%H:%M:%S')}\n{group_name}({group_id})\n{user_name}({user_id})"


async def get_image_link(bot: Bot, msg: Union[str,Message]):
    """获取图片链接"""
    imgs = []
    for file in re.findall("file=[^.]*.image", str(msg)):
        try:
            imgs.append((await bot.get_image(file=file[5:]))["url"])
        except ActionFailed as e:
            imgs.append(f"获取图片链接失败\n{e}")
    return imgs


async def _send_msg_msg(bot: Bot, msgs: List[Message]):
    """通过群聊和私聊直接发送消息"""
    for msg in msgs:
        for group_id in config.send_group:
            with contextlib.suppress(ActionFailed):
                await bot.send_group_msg(group_id=group_id, message=msg)
        for user_id in config.send_private:
            with contextlib.suppress(ActionFailed):
                await bot.send_private_msg(user_id=user_id, message=msg)


async def _send_foword_msg(bot: Bot, msgs: List[Message]):
    """通过群聊和私聊发送合并转发消息"""
    f_msg = [
        {
            "type": "node",
            "data": {"name": "sneaky-bot", "uin": bot.self_id, "content": msg},
        }
        for msg in msgs
    ]
    for user_id in config.send_private:
        with contextlib.suppress(ActionFailed):
            await bot.send_private_forward_msg(user_id=user_id, messages=f_msg)
    for user_id in config.send_group:
        with contextlib.suppress(ActionFailed):
            await bot.send_group_forward_msg(user_id=user_id, messages=f_msg)


async def _save_to_local(msgs: List[Message]):
    """将消息保存至本地"""
    with open(
        Path(config.save_path, f"log/{date.today()}.log"), mode="a", encoding="utf-8"
    ) as f:
        for m in msgs:
            f.write(str(m).rstrip("\n") + "\n")
        f.write("\n")


async def send_msg(bot: Bot, msgs: List[Message]):
    """将消息保存至本地并根据用户配置的渠道发送消息"""
    
    await _save_to_local(msgs)
    if config.foword_msg:
        await _send_foword_msg(bot, msgs)
    else:
        await _send_msg_msg(bot, msgs)
