#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
多点自动获取答题share code脚本
每日早上0点执行领取水滴奖励任务
"""
import json
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
        response = requests.post('https://sign-in.dmall.com/generateInviteCode', headers=headers, data=data,
                                 verify=False)
    except Exception as e:
        print(e)
        return
    response = response.text.lstrip('(').rstrip(')').replace("'", '"')
    data = json.loads(response)
    print(data)

    assist_code += data.get('data') + '&'
    # print(assist_code)


def get_all_signcode():
    print(f"开始获取签到助力share code执行脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        get_own_sharecode(v)

    # 将获取每人的sharecode统一写入配置文件
    # conf.add_section("signCode")
    # conf.set("signCode", "code", str(assist_code))
    # 写入配置文件
    # with open(cfgpath, "w+") as f:
    #     conf.write(f)
    return assist_code


if __name__ == "__main__":
    get_all_signcode()