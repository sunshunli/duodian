#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点自动回答问题脚本
每日早上7点执行领取水滴奖励任务
"""

import sys
import requests
import json
import time
import configparser
import os
from datetime import datetime, timedelta
import threading
from urllib.parse import urlencode, urlparse, quote

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
assistCode = conf['AssistCode']['code']
###################################################
coin = 0
totalCoin = 0
summary_table = {}
activity_code = '5d8a4213'
activity_prizeId = '6315'
# https://mario-api.dmall.com/activity/info?code=5d8a4213&assistCode=&_=1627868775788 查看activity_code

def get_activity_code(cookies):
    """
    获取答题活动的id
    """
    global activity_code
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
        'callback': 'jQuery35109245784105782566_1625203096510',
        'lastUserMessageId': '',
        'lastSysMessageId': '',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://farm.dmall.com/user/login', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    nPos = response.text.index('(') + 1
    response = response.text[nPos:-2]
    data = json.loads(response)
    targetUrl = data.get('data').get('popAdInfo').get('targetUrl')
    for item in targetUrl.split('?')[1].split('&'):
        if item.startswith('code'):
            activity_code = item.split('=')[1]



def get_more_chance(cookies, code):
    # 助力好友答题，增加一次答题机会
    headers = {
        'Host': 'mario-api.dmall.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://act.dmall.com',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Referer': 'https://act.dmall.com/dac/mario_h5/index.html?dmShowShare=false&bounces=false&dmShowCart=false&dmfrom=wx&code=698d1912',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'com.wm.dmal'
    }
    params = {
        'code': activity_code,
        'assistCode': code
    }
    try:
        response = requests.get(
            'https://mario-api.dmall.com/activity/info', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,get_questions")
        return
    data = response.json()
    print('get_more_chance', data)


def get_questions(cookies):
    # 获取问题列表
    headers = {
        'Host': 'mario-api.dmall.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://act.dmall.com',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Referer': 'https://act.dmall.com/dac/mario_h5/index.html?dmShowShare=false&bounces=false&dmShowCart=false&dmfrom=wx&code=698d1912',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'com.wm.dmal'
    }
    params = {
        'code': activity_code
    }
    try:
        response = requests.get(
            'https://mario-api.dmall.com/game/play', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,get_questions")
        return
    data = response.json()
    print(data)
    if data.get('data') != None:
        token = data.get('data').get('token')
        _questions_list = data.get('data').get('questionList')
        print(data)
        print(_questions_list)
        answer_ids = []
        for k, v in enumerate(_questions_list):
            answer_ids.append(v.get('rkey'))
        answer_ids_str = ','.join(answer_ids)
        answer_questions(cookies, token, answer_ids_str)


def answer_questions(cookies, token, ids):
    global totalCoin
    # 回答问题
    headers = {
        'Host': 'mario-api.dmall.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://act.dmall.com',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Referer': 'https://act.dmall.com/dac/mario_h5/index.html?dmShowShare=false&bounces=false&dmShowCart=false&dmfrom=wx&code=698d1912',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'com.wm.dmal'
    }
    params = {
        'code': activity_code,
        'token': token,
        'answers': ids
    }
    try:
        response = requests.get(
            'https://mario-api.dmall.com/game/over', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,answer_questions")
        return
    data = response.json()
    totalCoin = data.get('data').get('totalCoin')
    time.sleep(10)
    print(answer_questions, data)


def get_reward_water(cookies):
    headers = {
        'Host': 'mario-api.dmall.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://act.dmall.com',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Referer': 'https://act.dmall.com/dac/mario_h5/index.html?dmShowShare=false&bounces=false&dmShowCart=false&dmfrom=wx&code=698d1912',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'com.wm.dmal'
    }
    params = {
        'code': activity_code,
        'activityPrizeId': activity_prizeId
    }
    try:
        response = requests.get(
            'https://mario-api.dmall.com/prize/exchange', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,get_questions")
        return
    data = response.json()
    print('get_reward_water', data)
    if data.get('code') == '0000':
        get_prize_list(cookies)


def get_prize_list(cookies):
    headers = {
        'Host': 'mario-api.dmall.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://act.dmall.com',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Referer': 'https://act.dmall.com/dac/mario_h5/index.html?dmShowShare=false&bounces=false&dmShowCart=false&dmfrom=wx&code=698d1912',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'com.wm.dmal'
    }
    params = {
        'code': activity_code
    }
    try:
        response = requests.get(
            'https://mario-api.dmall.com/prize/list', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,get_questions")
        return
    data = response.json()
    print('get_prize_list', data)
    if data.get('code') == '0000':
        if data.get('data').get('score') > 30:
            get_reward_water(cookies)


def summary_info():
    global summary_table
    print(summary_table)

    serverJ("⏰ 多点果园", json.dumps(summary_table, ensure_ascii=False))


def run():
    print(f"开始运行答题自动执行脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    global coin
    global totalCoin
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        # 前提条件，必须先执行获取答题活动code
        get_activity_code(cookies)

        # 获取答题机会
        for v in assistCode.rstrip('&').split('&'):
            get_more_chance(cookies, v)
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        get_questions(cookies)
        get_questions(cookies)

        global summary_table
        summary_table[f"账号{k+1}"] = {
            '答题获取金币': coin,
            '答题获取总金币': totalCoin
        }
        get_prize_list(cookies)
        # 初始化全局变量
        coin = 0
        totalCoin = 0

    summary_info()


if __name__ == "__main__":
    run()