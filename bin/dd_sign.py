#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点签到自动脚本
每日0点执行领签到任务
"""

import sys
import requests
import json
import time
import configparser
import os
# from datetime import datetime, timedelta
# import threading
from urllib.parse import urlencode, urlparse
# 加上这行代码即可，关闭安全请求警告
requests.packages.urllib3.disable_warnings()

curpath = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_path)
from utils.dd_cookies import get_cookies
from utils.tools import get_target_value, str2dict, serverJ

###################################################
# GitHub action运行需要填写对应的secrets
if "BARK" in os.environ and os.environ["BARK"]:
    BARK = os.environ["BARK"]
    print("BARK 推送打开")
if "SCKEY" in os.environ and os.environ["SCKEY"]:
    BARK = os.environ["SCKEY"]
    print("serverJ 推送打开")
if "TG_BOT_TOKEN" in os.environ and os.environ["TG_BOT_TOKEN"] and "TG_USER_ID" in os.environ and os.environ["TG_USER_ID"]:
    TG_BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    TG_USER_ID = os.environ["TG_USER_ID"]
    print("Telegram 推送打开")
###################################################
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
currentMonthContinuousDays = ''
currentMonthAddUpDays = ''
hasCheckIn = ''
score = ''
summary_table = {}


def do_signin(cookies):
    # 签到有礼
    headers = {
        'Host': 'appapis.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/signIn/index.html?dmShowTitleBar=false&dmfrom=wx&bounces=false&dmTransStatusBar=true&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'isNew': '1',
        'apiVersion': '5.0.4',
        'platform': 'Android',
        'venderId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://appapis.dmall.com/static/signInProccess.jsonp', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    # data = json.loads(response)
    print('执行签到任务', response.text)


def get_signin_info(cookies):
    # 获取签到信息
    headers = {
        'Host': 'appapis.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/signIn/index.html?dmShowTitleBar=false&dmfrom=wx&bounces=false&dmTransStatusBar=true&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'isNew': '1',
        'apiVersion': '5.0.4',
        'platform': 'Android',
        'venderId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://appapis.dmall.com/static/queryUserCheckInfo.jsonp', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)

    # 本月已连续签到天数
    month_continuous_sign = data.get('result').get('data').get('currentMonthContinuousDays')
    # 本月已累计签到天数
    month_add_sign = data.get('result').get('data').get('currentMonthAddUpDays')
    # 循环遍历连续签到状态，判断是否有可领取奖励
    month_continuous_progress = data.get('result').get('data').get('currentMonthContinueProgress')
    for rewardList in month_continuous_progress:
        # 首先判断奖励是否被领取, False表示未被领取
        if rewardList['rewardFinished'] == False:
            # 再判断是否满足领取要求
            # print('领取连续签到奖励', rewardList['rewards'][0].get('rewardName'))
            if rewardList['requiredTimes'] == month_continuous_sign:
                # print('领取连续签到奖励', rewardList['rewards'])
                pass
    # 循环遍历累计签到状态，判断是否有可领取奖励
    month_add_progress = data.get('result').get('data').get('currentMonthAddProgress')
    for rewardAddList in month_add_progress:
        # 首先判断奖励是否被领取, False表示未被领取
        if rewardAddList['rewardFinished'] == False:
            # 再判断是否满足领取要求
            print('领取累计签到奖励', rewardAddList['rewards'][0].get('rewardName'))
            if rewardAddList['requiredTimes'] == month_continuous_sign:
                pass
                # print('领取连续签到奖励', rewardAddList['rewards'])

    global currentMonthContinuousDays
    global currentMonthAddUpDays
    global hasCheckIn
    global score

    currentMonthContinuousDays = data.get('result').get('data').get('currentMonthContinuousDays')
    currentMonthAddUpDays = data.get('result').get('data').get('currentMonthAddUpDays')
    hasCheckIn = data.get('result').get('data').get('hasCheckIn')
    score = data.get('result').get('data').get('score')
    print('本月已连续签到', data.get('result').get('data').get('currentMonthContinuousDays'))
    print('本月已累计签到', data.get('result').get('data').get('currentMonthAddUpDays'))
    print('今日签到状态', data.get('result').get('data').get('hasCheckIn'))
    print('当前多点金币', data.get('result').get('data').get('score'))


def receive_signin_reward(cookies):
    pass


def summary_info():
    print(summary_table)

    serverJ("⏰ 多点签到", json.dumps(summary_table, ensure_ascii=False))


def run():
    print(f"开始运行多点果园签到脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        do_signin(cookies)
        get_signin_info(cookies)

        summary_table[f"账号{k+1}"] = {
            '本月已连续签到': currentMonthContinuousDays,
            '本月已累计签到': currentMonthAddUpDays,
            '今日签到': hasCheckIn,
            '当前多点金币': score
        }

    summary_info()


if __name__ == "__main__":
    run()
