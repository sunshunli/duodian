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
from datetime import datetime, timedelta
import threading
from urllib.parse import urlencode, urlparse

curpath = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_path)
from utils.dd_cookies import get_cookies

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




def run():
    pass


if __name__ == "__main__":
    run()