from nonebot import get_driver
from nonebot.log import logger

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

if config.at_enable:
    logger.info("正在加载at模块")
    from .fuctions import at
if config.flash_enable:
    logger.info("正在加载flash模块")
    from .fuctions import flash_img
if config.recall_enable:
    logger.info("正在加载recall模块")
    from .fuctions import recall
