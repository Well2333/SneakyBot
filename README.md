# SneakyBot

将QQ内收到的若干种类信息(如闪照)保存并对特定对象提示, 用于划水的机器人, 基于 NoneBot2 开发

**偷偷摸摸用就好了, 别把保安招来**
**偷偷摸摸用就好了, 别把保安招来**
**偷偷摸摸用就好了, 别把保安招来**
**偷偷摸摸用就好了, 别把保安招来**
**偷偷摸摸用就好了, 别把保安招来**

## 机器人使用方法

1. 将仓库clone至本地 `git clone https://github.com/Well2333/SneakyBot.git` 。
2. 在文件夹内执行 `poetry install` 或 `pip install nonebot2 nonebot-adapter-onebot` 完成依赖的安装。
3. 在文件夹内新建文件 `.env`, 并按照 [配置项](docs/配置项.md) 中的介绍在本文件中填写配置项。
4. 下载并运行 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的**最新版**并按照配置项中设置的 `HOST` 及 `PORT` 配置其 `config.yml`, 可参考 [配置项](docs/配置项.md)。
5. **同时**启动 go-cqhttp 及 bot.py 以开启机器人（可使用screen等方式）。

## 插件使用方法

> 之后可能会传pypi，但是现在没传

1. 提取仓库中的 `sneaky` 文件夹。
2. 在 nonebot2 中加载插件，参考 <https://v2.nonebot.dev/docs/next/tutorial/plugin/load-plugin>。
3. 在 `.env.*` 中添加本插件的 [自定义配置项](docs/配置项.md#插件自定义配置项简介)。
4. 启动机器人即可运行。

## 特别感谢

- [NoneBot2](https://github.com/nonebot/nonebot2)：SneakBot 使用的开发框架。
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：稳定完善的 CQHTTP 实现。
- [haruka-bot](https://github.com/SK-415/HarukaBot): 插件结构和部分代码参考, 文档参考。
- [A60](https://github.com/djkcyl): 🙏阿门🙏
