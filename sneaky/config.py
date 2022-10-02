from pathlib import Path
from typing import Sequence

from nonebot.log import logger
from pydantic import BaseSettings, validator


class Config(BaseSettings):
    foword_msg: bool = True
    at_enable: bool = False
    at_all: bool = False
    flash_enable: bool = False
    recall_enable: bool = False
    recall_image_only: bool = False
    send_private: Sequence[int]
    send_group: Sequence[int]
    save_path: Path = Path("sneakydata")

    @validator("send_private")
    def private_check(cls, v):
        if isinstance(v, Sequence):
            return v
        elif str(v).isdigit():
            return [int(v)]
        else:
            return []

    @validator("send_group")
    def group_check(cls, v, values):
        if str(v).isdigit():
            v = [int(v)]
        elif not isinstance(v, Sequence):
            v = []
        if values["send_private"] or v:
            return v
        else:
            raise ValueError("SEND_PRIVATE 和 SEND_GROUP 中至少应有一项不为空")

    @validator("save_path")
    def path_check(cls, v):
        if Path(v).is_absolute():
            logger.warning(f"检测到 SAVE_PATH 为绝对路径 -> {v}")
        Path(v, "log").mkdir(755, True, True)
        Path(v, "cache").mkdir(755, True, True)
        return Path(v)

    class Config:
        extra = "ignore"
