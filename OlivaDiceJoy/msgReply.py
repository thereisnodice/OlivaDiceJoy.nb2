# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReply.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import hashlib
import time

import OlivaDiceCore.msgCustom
import OlivaDiceCore.msgReply
import OlivaDiceCore.userConfig
from nonebot.adapters.cqhttp import MessageSegment

import OlivaDiceJoy.msgCustomManager


def unity_init(plugin_event, Proc):
    data_init(plugin_event, Proc)

def data_init(plugin_event, Proc):
    OlivaDiceJoy.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])

def unity_reply(plugin_event, Proc):
    data_init(plugin_event, Proc)
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = plugin_event.data.sender['nickname']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)

    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    skipToRight = OlivaDiceCore.msgReply.skipToRight

    tmp_at_str = str(MessageSegment.at(plugin_event.base_info['self_id']))
    tmp_at_str_sub = None
    if "sub_self_id" in plugin_event.data.extend:
        if plugin_event.data.extend["sub_self_id"] != None:
            tmp_at_str_sub = str(MessageSegment.at(plugin_event.data.extend['sub_self_id']))
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
        if isMatchWordStart(tmp_reast_str, tmp_at_str):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_at_str):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        flag_force_reply = True
    if tmp_at_str_sub != None:
        if isMatchWordStart(tmp_reast_str, tmp_at_str_sub):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str_sub)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if getattr(plugin_event.data, 'to_me', False):
        flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_command_str_1):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_command_str_1)
        flag_is_command = True
    elif isMatchWordStart(tmp_reast_str, tmp_command_str_2):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_command_str_2)
        flag_is_command = True
    elif isMatchWordStart(tmp_reast_str, tmp_command_str_3):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_command_str_3)
        flag_is_command = True
    if flag_is_command:
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                flag_is_from_host = True
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = plugin_event.data.group_id,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = plugin_event.data.group_id,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = plugin_event.data.group_id,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
        if isMatchWordStart(tmp_reast_str, 'jrrp'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'jrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime())).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            tmp_reply_str = dictStrCustom['strJoyJrrp'].format(**dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'zrrp'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'zrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) - 24 * 60 * 60))).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            tmp_reply_str = dictStrCustom['strJoyZrrp'].format(**dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
        elif isMatchWordStart(tmp_reast_str, 'mrrp'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'mrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) + 24 * 60 * 60))).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            tmp_reply_str = dictStrCustom['strJoyMrrp'].format(**dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
            return
