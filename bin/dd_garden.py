#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点果园自动脚本
每日早上7点执行领取水滴奖励任务
每日8-9点 12-14点 18-21点领每日三餐福袋
"""

import sys
import requests
import json
import time
import configparser
import os
from datetime import datetime, timedelta
import threading
from urllib.parse import urlencode, urlparse


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
ts = datetime.now() - timedelta(hours=1)
previous_time_stamp = int(time.mktime(ts.timetuple()) * 1000)
cur_time = int(round(time.time() * 1000))

###################################################
# 果树信息
tree_level = 0  # 果树等级
tree_id = 0  # 果树id
fruit_name = ''  # 种植的水果名称
water_count = 0  # 剩余水滴数量
progress_percentage = 0  # 浇水进度百分比
total_reward = 0  # 获取水滴总数

summary_table = {}  # 多账号果树信息及收获信息汇总
###################################################


def get_time():
    mins = int(time.time())
    date_stamp = (mins-57600) % 86400
    utc_dt = datetime.utcnow()  # UTC时间
    bj_dt = utc_dt+timedelta(hours=8)  # 北京时间
    _datatime = bj_dt.strftime("%Y%m%d", )
    notify_time = bj_dt.strftime("%H %M")
    print(f"\n当前时间戳: {mins}")
    print(f"北京时间: {bj_dt}\n\n")
    return mins, date_stamp, _datatime, notify_time


def fun_timer(sec, fn, args):
    # print('定时器执行时间:', time.strftime('%Y-%m-%d %H:%M:%S'))
    timer = threading.Timer(sec, fn, args)
    timer.start()


def get_url_query(url):
    # 获取url地址中的参数
    query_array = urlparse(url).query.split('&')

    query_dict = {}
    for v in query_array:
        _temp = str(v).split('=')
        query_dict[_temp[0]] = _temp[1]

    return query_dict


def touch_tree_drop(cookies):
    # 点击果树，有机会掉落水滴
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'platformCode': '1',
        'vendorId': '1',
        'storeId': cookies['storeId'],
        'treeId': tree_id,
        'treeLevel': tree_level,
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
    }
    try:
        response = requests.get('https://farm.dmall.com/gardenTree/dropGood', headers=headers, params=params, cookies=cookies, verify=False)
    except:
        print("网络请求异常,touch_tree_drop")
        return
    data = response.json()['data']
    # data = json.loads(data)
    print('果树掉落', response.json())
    if json.loads(data.get('config')).get('awardType', -1) == 1:
        print(f"点击果树掉落{json.loads(data.get('config')).get('awardNums')}水滴")
        # 拾取掉落的水滴
        receive_tree_drop(cookies, str(data.get('id')))
    elif json.loads(data.get('config')).get('awardType', -1) == 3:
        print(f"点击果树掉落{json.loads(data.get('config')).get('awardName')}")
        # 拾取掉落的优惠券
        receive_tree_drop(cookies, str(data.get('id')))


def receive_tree_drop(cookies, activityid):
    # 拾取果树掉落的水滴
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'vendorId': '1',
        'storeId': cookies['storeId'],
        'descRewardId': activityid,
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
    }
    try:
        response = requests.get('https://farm.dmall.com/gardenTree/receiveGood', headers=headers, params=params,
                                cookies=cookies, verify=False)
    except:
        print("网络请求异常,touch_tree_drop")
        return
    data = response.json()['data']['config']
    data = json.loads(data)
    if data.get('awardType', -1) == 1:
        print(f"拾取果树掉落{data['awardNums']}水滴")

    if response.json()['code'] == '0000':  # 成功获取奖励
        global total_reward
        reward_num = get_target_value('awardNums', data, [])[0]
        total_reward = total_reward + int(reward_num)
    print('receive_tree_drop', response.json())


def daily_sign(cookies):
    # 每日签到领水滴
    print('执行每日签到任务')
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': '40',
        'taskType': '4',
        'taskStatus': '1',
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://farm.dmall.com/garden/home/finishTask', headers=headers, params=params, cookies=cookies, verify=False)
    except:
        print("网络请求异常,daily_sign")
        return
    data = response.json()

    print(f'执行每日签到任务，{data["message"]}')
    if data['code'] == '0000':  # 成功获取奖励
        global total_reward
        reward_num = get_target_value('prizeNumber', data, [])[0]
        total_reward = total_reward + int(reward_num)
    print('daily_sign', data)


def daily_seven_clock(cookies):
    # 每日签到领水滴
    print('执行每日7点钟领水滴任务')
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': '11',
        'taskType': '7',
        'taskStatus': '2',
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://farm.dmall.com/garden/home/finishTask', headers=headers, params=params,
                                cookies=cookies, verify=False)
    except:
        print("网络请求异常,daily_seven_clock")
        return
    data = response.json()

    print(f'执行每日7点领水滴任务，{data["message"]}')
    if data['code'] == '0000':  # 成功获取奖励
        global total_reward
        reward_num = get_target_value('prizeNumber', data, [])[0]
        total_reward = total_reward + int(reward_num)
    print('daily_seven_clock', data)


def water_tree(cookies):
    # 浇水
    headers = {
        'Host': 'farm.dmall.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7,ru;q=0.6,it;q=0.5,nl;q=0.4,fr;q=0.3,de;q=0.2,ko;q=0.1,ja;q=0.1',
        'Referer': 'https://act.dmall.com/',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = {
        'newCustomer': 'false',
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get(
            'https://farm.dmall.com/garden/home/watering', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,water_tree")
        return
    data = response.json()["data"]

    print('water_tree', data)
    if data is not None:
        global progress_percentage
        global water_count
        water_count = data.get('gardenUserResponse').get('userDropBalance')
        progress_percentage = data.get('treeInfo').get('progressPercentage')

    if int(water_count) > 120:
        time.sleep(3)
        water_tree(cookies)


def get_task_list(cookies, msg):
    # 获取领水滴任务列表
    print(msg)
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'newCustomer': 'false',
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://farm.dmall.com/garden/home/taskList', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = response.json()["data"] and response.json()["data"]["gardenTaskResponseList"]
    print('获取任务列表', response.json())
    if data:
        for index, task in enumerate(data):
            # 任务未完成状态才执行任务
            if task['taskStatus'] == 1:  # 1 任务未执行 2 任务执行完，可以领取奖励 0 任务不可执行
                if task['taskId'] == 37:
                    finish_browser_task(cookies, task)
                else:
                    do_task(cookies, task)
            elif task['taskStatus'] == 2:
                get_daily_reward(cookies, task)
            else:
                if msg == '获取任务列表':
                    print(f"{task['taskName']}任务已完成")


def do_task(cookies, task):
    # 做任务集水滴
    # print(f"开始执行{task['taskName']} - {task['taskDesc']}")
    # 判断任务的类型，决定如何完成任务
    switch = {'1': do_task_type1,  # 注意此处不要加括号
              '2': do_task_type2,
              '5': do_task_type5,
              '6': do_task_type6,
              '9': do_task_type2
              }
    choice = task['taskType']
    print('do_task', choice)
    switch.get(str(choice), do_task_type_default)(cookies, task)


def get_daily_reward(cookies, task):
    # 每日免费领水滴
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': task['taskId'],
        'taskType': task['taskType'],
        'taskStatus': task['taskStatus'],
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://farm.dmall.com/garden/home/finishTask', headers=headers, params=params, cookies=cookies, verify=False)
    except Exception as e:
        print(e)
        return
    data = response.json()
    if data['code'] == 'USER_3008':
        print(data['message'], '开始执行次浇水任务')
        water_tree(cookies)
        get_daily_reward(cookies, task)
    else:
        if 'haveTimeInterval' in data:
            # 需要定时器
            time_interval = get_target_value('timeInterval', data, [])[0]
            print('时间间隔-------------', time_interval)
            fun_timer(int(time_interval), get_daily_reward, [cookies, task])
    if data['code'] == '0000':  # 成功获取奖励
        global total_reward
        reward_num = get_target_value('prizeNumber', data, [])[0]
        total_reward = total_reward + int(reward_num)


def do_task_type1(cookies, task):
    # 执行任务列表中类型为1的任务
    # 判断任务是否可执行 1 可执行； 0 不可执行
    print(f"开始执行{task['taskName']}")
    if task['taskStatus'] == 1:
        get_daily_reward(cookies, task)


def do_task_type2(cookies, task):
    print(f"开始执行{task['taskName']}")
    print(task)
    if task['taskType'] == 2:
        url = task['gardenBrowseTaskExtResponse']['taskLoadLink']
    elif task['taskType'] == 9:
        url = task['gardenSearchTaskExtResponse']['taskLoadLink']

    url_dict = get_url_query(url)

    _pageTaskSource = url_dict.get('pageTaskSource')
    _pageTaskId = url_dict.get('pageTaskId')
    _pageTaskType = url_dict.get('pageTaskType')
    # 浏览页面任务
    # 进入页面调用接口
    headers = {
        'dmTenantId': '1',
        'device': 'HUAWEI HUAWEI LYA-AL10 LMY47I',
        'sysVersion': 'Android-5.1.1',
        'screen': '1280*720',
        'recommend': '1',
        'userId': cookies['userId'],
        'token': cookies['token'],
        'uuid': cookies['uuid'],
        'apiVersion': '5.0.4',
        'env': 'app',
        'androidId': '8543f3d27daa44ad',
        'originBusinessFormat': '1-2-4-8',
        'channelId': cookies['channelId'],
        'areaId': cookies['areaId'],
        'currentTime': str(cur_time),
        'lastInstallTime': '1619536070832',
        'firstInstallTime': '1619536070832',
        'storeId': cookies['storeId'],
        'sessionId': cookies['sessionId'],
        'User-Agent': UserAgent,
        'platform': 'ANDROID',
        'ticketName': cookies['ticketName'],
        'venderId': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'appapi.dmall.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    _payload = f"""{{'source': {_pageTaskSource}, 'taskId': {_pageTaskId}, 'taskType': {_pageTaskType}}}"""
    data = {
        'param': _payload
    }
    try:
        response = requests.post('https://appapi.dmall.com/app/farm/queryTask', headers=headers, data=urlencode(data), verify=False)
    except:
        print("网络请求异常,do_task_type2")
        return
    result = response.json()
    if result:
        # 写死创建新线程，等待15s后执行浏览确认任务
        fun_timer(15, finish_browser_page, [cookies, task])


def finish_browser_page(cookies, task):
    print(f"开始执行{task['taskName']}")
    if task['taskType'] == 2:
        url = task['gardenBrowseTaskExtResponse']['taskLoadLink']
    elif task['taskType'] == 9:
        url = task['gardenSearchTaskExtResponse']['taskLoadLink']
    url_dict = get_url_query(url)

    _pageTaskSource = url_dict.get('pageTaskSource')
    _pageTaskId = url_dict.get('pageTaskId')
    _pageTaskType = url_dict.get('pageTaskType')

    # 浏览时间到后调用接口
    finally_headers = {
        'dmTenantId': '1',
        'recommend': '1',
        'userId': cookies['userId'],
        'token': cookies['token'],
        'uuid': cookies['uuid'],
        'env': 'app',
        'currentTime': str(cur_time),
        'lastInstallTime': '1619415312747',
        'firstInstallTime': '1619415312747',
        'storeId': cookies['storeId'],
        'sessionId': cookies['sessionId'],
        'User-Agent': UserAgent,
        'platform': 'ANDROID',
        'ticketName': cookies['ticketName'],
        'venderId': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'appapi.dmall.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    _payload = f"""{{'source': {_pageTaskSource}, 'taskId': {_pageTaskId}, 'taskType': {_pageTaskType}, 'taskStatus': '1'}}"""
    finally_data = {
        'param': _payload
    }
    try:
        response = requests.post('https://appapi.dmall.com/app/farm/dofinishTask', headers=finally_headers, data=urlencode(finally_data), verify=False)
    except:
        print("网络请求异常,finish_browser_page")
        return
    result = response.json()['data']
    print(response.json())
    if result is not None:
        if task['taskType'] == 2:
            browse_reward_amount = get_target_value('browseRewardAmount', result, [])[0]
        elif task['taskType'] == 9:
            browse_reward_amount = get_target_value('prizeNumber', result, [])[0]
        print(f"执行完成{task['taskName']}任务，获得{browse_reward_amount}")


def finish_browser_task(cookies, task):
    # print(f"开始执行{task['taskName']}")
    # 浏览商品
    print('执行浏览商品任务')
    headers = {
        'Host': 'farm.dmall.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'User-Agent': UserAgent,
        'Accept': '*/*',
        'Referer': 'https://act.dmall.com/dac/fruitgarden/index.html?tpc=garden_37&dmfrom=wx&dmTransStatusBar=true&dmShowTitleBar=false&bounces=false&dmNeedLogin=true&dmNeedCloseLoading=false',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wm.dmall'
    }
    params = {
        'taskId': task['taskId'],
        'taskType': task['taskType'],
        'taskStatus': task['taskStatus'],
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get('https://farm.dmall.com/garden/home/finishTask', headers=headers, params=params,
                                cookies=cookies, verify=False)
    except:
        print("网络请求异常,daily_sign")
        return
    data = response.json()
    # print('浏览任务1', data)


def do_task_type5(cookies, task):
    print(f"开始执行{task['taskName']}")
    get_daily_reward(cookies, task)


def do_task_type6(cookies, task):
    print(f"开始执行{task['taskName']}")
    # 执行浇水10次
    # total_water_count = task['canFinishCount']
    # need_water_count = task['finishCount']
    # print(f"执行每日浇水任务，需要完成{total_water_count}次, 目前已完成{need_water_count}次")

    # i = need_water_count
    # while i < total_water_count:
    #     time.sleep(5)  # 延迟5秒执行
    #     water_tree(cookies)
    #     i = i + 1

    water_tree(cookies)


def do_task_type_default(cookies, task):
    print('default')


def get_tree_info(cookies):
    headers = {
        'Host': 'farm.dmall.com',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': UserAgent,
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,es;q=0.7,ru;q=0.6,it;q=0.5,nl;q=0.4,fr;q=0.3,de;q=0.2,ko;q=0.1,ja;q=0.1',
        'Referer': 'https://act.dmall.com/',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    params = {
        'newCustomer': 'false',
        'platformCode': '1',
        'token': cookies['token'],
        'ticketName': cookies['ticketName'],
        'vendorId': '1',
        'storeId': cookies['storeId']
    }
    try:
        response = requests.get(
            'https://farm.dmall.com/garden/home/gardenHome', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,water_tree")
        return
    data = response.json()
    global tree_level
    global fruit_name
    global tree_id
    global water_count
    global progress_percentage
    progress_percentage = get_target_value('progressPercentage', data, [])[0]
    water_count = get_target_value('userDropBalance', data, [])[0]
    tree_level = get_target_value('level', data, [])[0]
    fruit_name = get_target_value('fruitName', data, [])[0]
    tree_id = get_target_value('gardenItemId', data, [])[0]


def summary_info():
    global summary_table
    print(summary_table)

    serverJ("⏰ 多点果园", json.dumps(summary_table, ensure_ascii=False))


def run():
    print(f"开始运行多点果园自动执行脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    global tree_level
    global water_count
    global progress_percentage
    global total_reward
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        # 获取果树初始化信息
        get_tree_info(cookies)
        # 点击10次果树，间隔5s，拾取随机掉落的水滴
        for i in range(10):
            time.sleep(5)
            touch_tree_drop(cookies)

        # 每日签到任务
        daily_sign(cookies)

        # 每日7点领水滴
        daily_seven_clock(cookies)

        # 获取任务列表
        get_task_list(cookies, '获取任务列表')

        time.sleep(30)

        # 获取任务列表, 执行领取奖励
        get_task_list(cookies, '获取任务奖励')

        # global summary_table
        summary_table[f"账号{k+1}"] = {
            '果树等级': tree_level,
            '剩余水滴': water_count,
            '已完成': str(progress_percentage) + '%',
            '获取水滴': total_reward
        }
        # 初始化全局变量

        tree_level = ''
        water_count = ''
        progress_percentage = ''
        total_reward = ''
    summary_info()


if __name__ == "__main__":
    run()












