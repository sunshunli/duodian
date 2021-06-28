#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点自动获取答题share code脚本
每日早上0点执行领取水滴奖励任务
"""

import sys
import requests
import time
import configparser
import os

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
assist_code = ''


def get_own_sharecode(cookies):
    # 获取分享code
    global assist_code
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
        'code': '698d1912',
        'assistCode': ''
    }
    try:
        response = requests.get(
            'https://mario-api.dmall.com/activity/info', headers=headers, params=params, cookies=cookies,
            verify=False)
    except:
        print("网络请求异常,get_questions")
        return
    data = response.json()
    assist_code += data.get('data').get('userCode') + '&'
    print(assist_code)


def run():
    print(f"开始获取答题share code执行脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        get_own_sharecode(cookies)

    # 将获取每人的sharecode统一写入配置文件
    # conf.add_section("AssistCode")
    conf.set("AssistCode", "code", str(assist_code))
    # 写入配置文件
    with open(cfgpath, "w+") as f:
        conf.write(f)


if __name__ == "__main__":
    run()