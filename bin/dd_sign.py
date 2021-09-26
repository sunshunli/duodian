#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点签到自动脚本
每日0点执行领签到任务
"""

import sys
import requests
import json
import configparser
import os, stat
import time
from urllib.parse import urlencode, urlparse
from selenium import webdriver
# 加上这行代码即可，关闭安全请求警告
requests.packages.urllib3.disable_warnings()

curpath = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_path)
from utils.dd_cookies import get_cookies
from utils.tools import get_target_value, str2dict, serverJ

from dd_get_siginCode import get_all_signcode


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
# assistCode = conf['signCode']['code']
###################################################
assistCode = ''
currentMonthContinuousDays = ''
currentMonthAddUpDays = ''
hasCheckIn = ''
score = ''
summary_table = {}
d_track_data = ''
env = ''

def do_signin(cookies):
    # 签到有礼
    headers = {
        'Host': 'sign-in.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://appsign-in.dmall.com',
        'Referer': 'https://appsign-in.dmall.com/?dmNeedLogin=true&dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall',
        'Cookie': cookies
    }

    data = {
        'tenantId': '1',
        'platform': 'ANDROID',
        'vendorId': '1'
    }
    try:
        response = requests.post('https://sign-in.dmall.com/checkIn', headers=headers, data=data, verify=False)
    except Exception as e:
        print(e)
        return
    # data = json.loads(response)
    result = response.json()
    print('执行签到任务', result)


def get_signin_info(cookies):
    # 获取签到信息
    headers = {
        'Host': 'sign-in.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://appsign-in.dmall.com',
        'Referer': 'https://appsign-in.dmall.com/?dmNeedLogin=true&dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall',
        'Cookie': cookies
    }

    data = {
        'tenantId': '1',
        'platform': 'ANDROID',
        'vendorId': '1'
    }
    try:
        response = requests.post('https://sign-in.dmall.com/checkInQuery', headers=headers, data=data, verify=False)
    except Exception as e:
        print(e)
        return
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)
    print(data)

    # # 本月已连续签到天数
    # month_continuous_sign = data.get('result').get('data').get('currentMonthContinuousDays')
    # # 本月已累计签到天数
    # month_add_sign = data.get('result').get('data').get('currentMonthAddUpDays')
    # # 循环遍历连续签到状态，判断是否有可领取奖励
    # month_continuous_progress = data.get('result').get('data').get('currentMonthContinueProgress')
    # for rewardList in month_continuous_progress:
    #     # 首先判断奖励是否被领取, False表示未被领取
    #     if rewardList['rewardFinished'] == False:
    #         # 再判断是否满足领取要求
    #         print('连续签到奖励', rewardList['rewards'][0].get('rewardName'))
    #         if rewardList['requiredTimes'] == month_continuous_sign:
    #             print('领取连续签到奖励', rewardList['rewards'])
    #             receive_signin_reward(cookies, rewardList['taskId'])
    # # 循环遍历累计签到状态，判断是否有可领取奖励
    # month_add_progress = data.get('result').get('data').get('currentMonthAddProgress')
    # for rewardAddList in month_add_progress:
    #     # 首先判断奖励是否被领取, False表示未被领取
    #     if rewardAddList['rewardFinished'] == False:
    #         # 再判断是否满足领取要求
    #         print('累计签到奖励', rewardAddList['rewards'][0].get('rewardName'))
    #         if rewardAddList['requiredTimes'] == month_continuous_sign:
    #             print('领取累计签到奖励', rewardAddList['rewards'])
    #             receive_signin_reward(cookies, rewardAddList['taskId'])
    #
    # global currentMonthContinuousDays
    # global currentMonthAddUpDays
    # global hasCheckIn
    # global score
    #
    # currentMonthContinuousDays = data.get('result').get('data').get('currentMonthContinuousDays')
    # currentMonthAddUpDays = data.get('result').get('data').get('currentMonthAddUpDays')
    # hasCheckIn = data.get('result').get('data').get('hasCheckIn')
    # score = data.get('result').get('data').get('score')
    # print('本月已连续签到', data.get('result').get('data').get('currentMonthContinuousDays'))
    # print('本月已累计签到', data.get('result').get('data').get('currentMonthAddUpDays'))
    # print('今日签到状态', data.get('result').get('data').get('hasCheckIn'))
    # print('当前多点金币', data.get('result').get('data').get('score'))


def receive_signin_reward(cookies, task_id):
    headers = {
        'Host': 'sign-in.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://appsign-in.dmall.com',
        'Referer': 'https://appsign-in.dmall.com/?dmNeedLogin=true&dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall',
        'Cookie': cookies
    }

    data = {
        'actId': 201
    }
    try:
        response = requests.post('https://sign-in.dmall.com/generateInviteCode', headers=headers, data=data, verify=False)
    except Exception as e:
        print(e)
        return
    print(response)
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)
    print(data)


def summary_info():
    print(summary_table)

    serverJ("⏰ 多点签到", json.dumps(summary_table, ensure_ascii=False))


def get_invite_code(cookies):
    # 获取邀请code
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
        'actId': '52',
        'linkUrl': 'https%3A%2F%2Fi.dmall.com%2Fkayak-project%2Fmpactivities%2Fhtml%2Finvite%2Finvite.html'
    }
    try:
        response = requests.get('https://appapis.dmall.com/static/generateInviteCode.jsonp', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)
    print(data)
    # print('邀请码', data.get('result').get('data').get('inviteCode'))
    # print('token', data.get('result').get('data').get('token'))


def get_account_signin_reward(cookies):
    """
    通过使用firefox无头浏览器加载页面获取必要参数，然后请求接口获取累计签到获取水滴奖励
    """
    global d_track_data
    global env
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.add_argument('--disable-gpu')
    options.add_argument(f'user-agent={UserAgent}')

    project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    driver_path = os.path.join(project_path, 'utils', 'chromedriver_win32_2', 'geckodriver.exe')
    os.chmod(driver_path, stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
    driver = webdriver.Firefox(options=options, executable_path=driver_path)
    driver.get('https://a.dmall.com/act/L76rkBq0UhGOyuV.html?nopos=0&tpc=a_202662')
    driver.delete_all_cookies()
    for k, v in cookies.items():
        cookie = {
            'name': k,
            'value': v,
            'domain': '.dmall.com',
            'path': '/'
        }
        driver.add_cookie(cookie)
    time.sleep(20)

    try:
        d_track_data = driver.execute_script('return window.DmallTracker.getDTrackData()')
        env = driver.execute_script('return window.DmallTracker.getBaseConfigStatistics()')
    finally:
        driver.close()

    headers = {
        'Host': 'pandoragw.dmall.com',
        'Connection': 'keep-alive',
        'Content-Length': '2601',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': UserAgent,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://a.dmall.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://a.dmall.com/act/L76rkBq0UhGOyuV.html?nopos=0&tpc=a_202662',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7,ru;q=0.6,it;q=0.5,nl;q=0.4,fr;q=0.3,de;q=0.2,ko;q=0.1,ja;q=0.1',
    }
    data1 = {
        'taskId': 'C3gCeTSBdTZlR_KlIw',
        'rewardItemId': '86113',
        'env': env,
        'd_track_data': d_track_data
    }
    data2 = {
        'taskId': 'C359bxUMKKq4ffhgAw',
        'rewardItemId': '86114',
        'env': env,
        'd_track_data': d_track_data
    }
    data3 = {
        'taskId': 'C35_r_wQCCphCP4xTA',
        'rewardItemId': '86115',
        'env': env,
        'd_track_data': d_track_data
    }
    try:
        response1 = requests.post('https://pandoragw.dmall.com/alps/pickup', headers=headers, data=urlencode(data1), cookies=cookies, verify=False)
        response2 = requests.post('https://pandoragw.dmall.com/alps/pickup', headers=headers, data=urlencode(data2), cookies=cookies, verify=False)
        response3 = requests.post('https://pandoragw.dmall.com/alps/pickup', headers=headers, data=urlencode(data3), cookies=cookies, verify=False)
    except:
        print("网络请求异常,do_task_type2")
        return
    result1 = response1.json()
    result2 = response2.json()
    result3 = response2.json()
    print(result1)
    print(result2)
    print(result3)


def do_assistant(cookies, inviteCode):
    """
    签到助力
    """
    headers = {
        'Host': 'sign-in.dmall.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; LYA-AL00 Build/HUAWEILYA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3133 MMWEBSDK/20210601 Mobile Safari/537.36 MMWEBID/2069 MicroMessenger/8.0.11.1980(0x28000B59) Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 miniProgram',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'X-Requested-With': 'com.tencent.mm',
        'Cookie': cookies,
        'Origin': 'https://appsign-in.dmall.com',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'inviteCode': inviteCode
    }
    try:
        response = requests.post('https://sign-in.dmall.com/sendKey', headers=headers, data=data, verify=False)
    except:
        print("网络请求异常,get_own_sharecode")
        return


def get_assistant_status(cookies):
    """
    获取助力信息
    """
    headers = {
        'Host': 'sign-in.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://appsign-in.dmall.com',
        'Referer': 'https://appsign-in.dmall.com/?dmNeedLogin=true&dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall',
        'Cookie': cookies
    }

    data = {}
    try:
        response = requests.post('https://sign-in.dmall.com/queryInviteAct', headers=headers, data=data,
                                 verify=False)
    except Exception as e:
        print(e)
        return
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)
    print(data)


    # nPos = response.text.index('(') + 1
    # response = response.text[nPos:-1].replace("'", '"')
    # data = json.loads(response)
    # # key_count = data.get("data").get('inviteBox').get('keyCount')
    # key_count = 3
    invite_result_arr = data.get('data').get('inviteBox').get('boxes')
    for item in invite_result_arr:
        # 获取奖励
        get_assistant_reward(cookies, item.get('index'))


def get_assistant_reward(cookies, index):
    """
    获取助力奖励
    """
    headers = {
        'Host': 'sign-in.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://appsign-in.dmall.com',
        'Referer': 'https://appsign-in.dmall.com/?dmNeedLogin=true&dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall',
        'Cookie': cookies
    }

    data = {
        'index': index
    }
    try:
        response = requests.post('https://sign-in.dmall.com/openBox', headers=headers, data=data,
                                 verify=False)
    except Exception as e:
        print(e)
        return
    print(response)
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)
    print(data)


def run():
    print(f"开始运行多点果园签到脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    # 获取助力码
    global  assistCode
    assistCode = get_all_signcode()
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)

        # get_invite_code(v)
        do_signin(v)
        get_signin_info(v)

        # 助力
        for t in assistCode.rstrip('&').split('&'):
            time.sleep(2)
            do_assistant(v, t)

        # 获取连续签到7天和11天奖励
        # get_account_signin_reward(cookies)

        # summary_table[f"账号{k+1}"] = {
        #     '本月已连续签到': currentMonthContinuousDays,
        #     '本月已累计签到': currentMonthAddUpDays,
        #     '今日签到': hasCheckIn,
        #     '当前多点金币': score
        # }

    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        get_assistant_status(v)

    # summary_info()


if __name__ == "__main__":
    run()
