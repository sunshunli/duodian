#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点庄园自动脚本
"""
import os
import sys
import time
import json
import requests
import configparser

# 加上这行代码即可，关闭安全请求警告
requests.packages.urllib3.disable_warnings()

curpath = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_path)
from utils.dd_cookies import get_cookies
from utils.tools import get_target_value, str2dict, serverJ

# 读取配置文件
cfgpath = os.path.join(curpath, '../conf', 'config.ini')
# 创建管理对象
conf = configparser.ConfigParser()
# 读ini文件
conf.read(cfgpath, encoding="utf-8")
# 读取配置文件中的User Agent
UserAgent = conf['user_agent']['garden_ua']
cookiesList = get_cookies()
###################################################
fertilizerAmount = 0  # 庄园目前持有肥料数量
totalRewardAmount = 0  # 当前执行任务获取的总肥料数量
steal_amount = 0  # 累计当天偷取次数
can_steal_list = []  # 累计获取可以偷取的对象
stealLimit = 0  # 可以偷取邻居次数
stealCount = 0  # 已偷取的次数
summary_table = {}


def get_manor_info(cookies):
    global fertilizerAmount
    global stealLimit
    global stealCount
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/user/login', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = json.loads(response.text)
    print('get_manor_info', data)
    fertilizerAmount = data.get('data').get('userInfo').get('fertilizerAmount')
    # 遍历登录奖励
    login_reward = data.get('data').get('taskShowList')
    for key, value in enumerate(login_reward):
        taskid = value.get('taskId')
        if value.get('receiveCount') == 0 and value.get('finishCount') == value.get('canFinishCount'):
            get_daily_reward(cookies, taskid)
    # 遍历每周登录奖励，对比领取数量为1的任务
    signin_reward_taskid = data.get('data').get('addLoginTaskInfoVo').get('taskId')
    signin_reward_tasklist = data.get('data').get('addLoginTaskInfoVo').get('addLoginAwardVoList')
    for key, value in enumerate(signin_reward_tasklist):
        # TODO 暂时判断条件，等领取完7天后，需要重新修改
        if value.get('receiveStatus') == 1:
            total_days = value.get('totalDays')
            get_signin_reward(cookies, signin_reward_taskid, total_days)

    # 遍历任务列表
    daily_reward_tasklist = data.get('data').get('taskListVo').get('taskInfoVoList')
    for key, value in enumerate(daily_reward_tasklist):
        task_id = value.get('taskId')
        # task_name = value.get('name')
        task_targetType = value.get('targetType')
        # task_url = value.get('propertiesUrl')
        if task_targetType == 2 and value.get('canFinishCount') != value.get('finishCount'):  # 浏览任务
            do_browser_task(cookies, task_id)
        elif value.get('receiveCount') == 0 and value.get('canFinishCount') == value.get('finishCount'):
            get_task_reward(cookies, task_id)

    stealLimit = data.get('data').get('rockLoginInfo').get('stealProgressVo').get('stealLimit')
    stealCount = data.get('data').get('rockLoginInfo').get('stealProgressVo').get('stealCount')


def get_signin_reward(cookies, taskid, total_days):
    """
    领取每日登陆奖励
    """
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'callback': 'jQuery35109564943156586088_1620826617402',
        'taskId': taskid,
        'totalDays': total_days,
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
        '_': '1620826617414'
    }
    try:
        response = requests.get('https://farm.dmall.com/task/receiveAddLogin', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    nPos = response.text.index('(') + 1
    response = response.text[nPos:-2]
    data = json.loads(response)
    print(data)
    # print(data.get('data').get('addLoginAwardVoList'))


def do_browser_task(cookies, taskid):
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': taskid,
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/task/doFinish', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    # data = json.loads(response.text)
    print('do_browser_task', response.text)


def get_task_reward(cookies, taskid):
    """
    领取任务列表中完成的奖励
    """
    global totalRewardAmount
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': taskid,
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/task/receive', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = json.loads(response.text)
    totalRewardAmount += int(data.get('data').get('prizeAmount'))
    print('get_task_reward', response.text)


def get_daily_reward(cookies, taskid):
    """
    领取登录奖励
    """
    global totalRewardAmount
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': taskid,
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/task/receive', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = json.loads(response.text)
    totalRewardAmount += int(data.get('data').get('prizeAmount'))
    print('get_task_reward', response.text)


def get_neighbor_list(cookies, left_steal_count):
    """
    获取可偷取邻居的信息
    """
    global can_steal_list
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/rock/neighbor/list', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = json.loads(response.text)
    print('get_neighbor_list', data)
    neighborList = data.get('data')
    for key, value in enumerate(neighborList):
        # print(value)
        if value.get('canSteal') == 1:
            print(value)
            can_steal_list.append(value)
    print('len', len(can_steal_list))
    # 判断可偷取列表中是否满足5个，否则重新获取
    if len(can_steal_list) < left_steal_count:
        get_neighbor_list(cookies, left_steal_count)
    else:
        for key, value in enumerate(can_steal_list):
            do_deal_neighbor(cookies, value)


def do_deal_neighbor(cookies, neighbor):
    """
    偷取邻居化肥
    """
    global totalRewardAmount
    global can_steal_list
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'neighborId': neighbor.get('userId'),
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/rock/stealFertilizer', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = json.loads(response.text)
    print(data)
    if data.get('data') != None:
        totalRewardAmount += int(data.get('data').get('stealFertilizerAmount'))


def do_fertilization(cookies):
    """
    偷取邻居化肥
    """
    global totalRewardAmount
    global can_steal_list
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/mygarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'landId': '1',
        'cropId': '143',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId'],
    }
    try:
        response = requests.get('https://farm.dmall.com/farm/fertilization', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = json.loads(response.text)
    print(data)
    if data.get('data') != None:
        time.sleep(5)
        do_fertilization(cookies)


def summary_info():
    global summary_table
    print(summary_table)

    serverJ("⏰ 多点庄园", json.dumps(summary_table, ensure_ascii=False))


def run():
    print(f"开始运行多点庄园自动执行脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    global totalRewardAmount
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        # 获取任务信息并执行任务
        get_manor_info(cookies)
        # 领取任务奖励
        get_manor_info(cookies)
        if stealCount < stealLimit:
            print(f'今日可偷取邻居化肥次数: {stealCount}/{stealLimit}, 开始执行偷取化肥任务!')
            can_steal_count = stealLimit - stealCount
            get_neighbor_list(cookies, can_steal_count)
        else:
            print(f'今日可偷取邻居化肥次数: {stealCount}/{stealLimit}, 已无机会偷取化肥!')
        # 施肥
        do_fertilization(cookies)

        # global summary_table
        summary_table[f"账号{k+1}"] = {
            '获取总化肥数:': totalRewardAmount
        }
        # 初始化全局变量
        totalRewardAmount = 0

    summary_info()


if __name__ == "__main__":
    run()