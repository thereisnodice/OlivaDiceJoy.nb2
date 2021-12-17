# -*- encoding: utf-8 -*-
"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   main.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
"""

from typing import Optional, Tuple

import OlivaDiceCore.crossHook
from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.plugin import on
from OlivaDiceCore.middleware import PluginEvent, Proc

import OlivaDiceJoy.data
import OlivaDiceJoy.msgReply


async def pre_process(
    bot: Optional[Bot] = None, event: Optional[Event] = None
) -> Tuple[PluginEvent, Proc]:
    plugin_event = PluginEvent(bot, event)
    proc = Proc()

    return plugin_event, proc


@get_driver().on_bot_connect
async def init(bot: Bot):
    plugin_event, proc = await pre_process()
    OlivaDiceJoy.msgReply.unity_init(plugin_event, proc)
    OlivaDiceCore.crossHook.dictHookList["model"].append(
        ["OlivaDiceJoy", OlivaDiceJoy.data.OlivaDiceJoy_ver]
    )


@on("message").handle()
async def private_message(bot: Bot, event: PrivateMessageEvent):
    plugin_event, proc = await pre_process(bot, event)
    OlivaDiceJoy.msgReply.unity_reply(plugin_event, proc)


@on("message").handle()
async def group_message(bot: Bot, event: GroupMessageEvent):
    plugin_event, proc = await pre_process(bot, event)
    OlivaDiceJoy.msgReply.unity_reply(plugin_event, proc)
