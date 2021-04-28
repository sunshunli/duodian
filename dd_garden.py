import requests
import time
import os
from datetime import datetime, timedelta
import threading
from urllib.parse import urlencode
from urllib.parse import urlparse


# 多点果园自动脚本
###################################################
# 每日早上7点执行领取水滴奖励任务
# 每日8-9点 12-14点 18-21点领每日三餐福袋

# 生成虚拟环境依赖包requirements.txt,用于项目发布。这样即使新的环境没有安装pipenv也可以直接安装依赖包。
# 方法1：pipenv run pip freeze > requirements.txt
# 方法2：pipenv lock -r --dev > requirements.txt

# 虚拟环境中导入requirements.txt
# pipenv install -r requirements.txt
###################################################
# 对应方案2: 下载到本地,需要此处填写
cookies1 = "tempid=C957C764BD50000210E4171010C91D36; updateTime=1619429326000; device=HUAWEI%20HUAWEI%20YAL-AL00%20LMY47I; sysVersion=Android-5.1.1; screen=1280*720; apiVersion=5.0.4; dSource=; oaid=; tdc=; utmId=; androidId=70c1430d8f180e33; channelId=dm010000000001; currentTime=1619534618614; abFlag=1-1-B; lastInstallTime=1619534455218; version=5.0.4; tpc=; firstInstallTime=1619534455218; networkType=1; deliveryLng=116.410277; deliveryLat=39.916501; cid=160a3797c8a8315f5aa; sessionId=876d9892c72244c8854ef2ca349f1c25; User-Agent=dmall/5.0.4%20Dalvik/2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20YAL-AL00%20Build/LMY47I%29; xyz=ac; appName=com.wm.dmall; smartLoading=1; utmSource=; wifiState=1; gatewayCache=; isOpenNotification=1; inited=true; console_mode=0; uuid=70c1430d8f180e33; store_id=150; storeId=150; vender_id=1; venderId=1; businessCode=1681; appMode=online; storeGroupKey=6d6728171e7121fa5c838248af04be9b@MS0xNTAtMQ; platformStoreGroupKey=43913b6f8c3125d3f87b46aaec7616d4@MjAzMi04MDA4Mg; originBusinessFormat=1-2-4-8; appVersion=5.0.4; platform=ANDROID; dmall-locale=zh_CN; token=ca23a209-c415-4e64-bbd3-5d03730b67e9; ticketName=A514D41153123DCAE3DB465DAFE0FE1F4D4116123140B978113F668820EA821CDE306E5BA281687C853D43129DE1AC99FBBB3E48022897B31562185781D4EA342116FCDA4BA78559A415AF31A5FD26DB3BFA99EE0B382DA8733E1163A56D07A4860FC9A0B4716491E41E4FD157963152272396876117C4A3AA157C9E9C3A7EC9; userId=395388955; lat=39.916501; lng=116.410277; addr=%E5%8C%97%E4%BA%AC%E5%B8%82%E4%B8%9C%E5%9F%8E%E5%8C%BA%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; community=%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; areaId=110101; session_id=876d9892c72244c8854ef2ca349f1c25; env=app; first_session_time=1619534530736; session_count=2; recommend=1; dmTenantId=1; risk=1"
cookies2 = ""

cookiesList = [cookies1, ]   # 多账号准备

# 通知服务
BARK = ''                   # bark服务,自行搜索; secrets可填;形如jfjqxDx3xxxxxxxxSaK的字符串
SCKEY = ''                  # Server酱的SCKEY; secrets可填
TG_BOT_TOKEN = ''           # telegram bot token 自行申请
TG_USER_ID = ''             # telegram 用户ID

###################################################
# 对应方案1:  GitHub action自动运行,此处无需填写;
if "DD_GARDEN_COOKIE" in os.environ:
    """
    判断是否运行自GitHub action,"DD_GARDEN_COOKIE" 该参数与 repo里的Secrets的名称保持一致
    """
    print("执行自GitHub action")
    dd_garden_cookie = os.environ["DD_GARDEN_COOKIE"]
    cookiesList = []  # 重置cookiesList
    for line in dd_garden_cookie.split('\n'):
        if not line:
            continue
        cookiesList.append(line)
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
# 可选项
UserAgent = "Mozilla/5.0 (Linux; Android 5.1.1; LYA-AL10 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 Dmall/5.0.4"
ts = datetime.now() - timedelta(hours=1)
previous_time_stamp = int(time.mktime(ts.timetuple()) * 1000)


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


def str2dict(str_cookie):
    if type(str_cookie) == dict:
        return str_cookie
    tmp = str_cookie.split(";")
    dict_cookie = {}
    try:
        for i in tmp:
            j = i.split("=")
            if not j[0]:
                continue
            dict_cookie[j[0].strip()] = j[1].strip()
        assert dict_cookie["token"].split("&")[0]
        # regex = r"&\d\.\d\.\d+"
        # appid = "&1.0.12"
        # dict_cookie["1&_device"] = re.sub(
        #     regex, appid, dict_cookie["1&_device"], 0, re.MULTILINE)
        # print(dict_cookie["1&_device"])

    except (IndexError, KeyError):
        print("cookie填写出错 ❌,仔细查看说明")
        raise
    return dict_cookie


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
            'https://farm.dmall.com/garden/home/watering', headers=headers, params=params, cookies=cookies, verify=False)
    except:
        print("网络请求异常,water_tree")
        return
    data = response.json()["data"]


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
                print(f"{task['taskName']}任务已完成")


def do_task(cookies, task):
    # 做任务集水滴
    # print(f"开始执行{task['taskName']} - {task['taskDesc']}")
    # 判断任务的类型，决定如何完成任务
    switch = {'1': do_task_type1,  # 注意此处不要加括号
              '2': do_task_type2,
              '5': do_task_type5,
              '6': do_task_type6
              }
    choice = task['taskType']
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
        print(data['message'], '开始执行10次浇水任务')
        i = 0
        while i < 10:
            time.sleep(5)
            water_tree(cookies)
            i = i + 1
        get_daily_reward(cookies, task)
    else:
        if data['data']['haveTimeInterval'] is not None:
            # 需要定时器
            fun_timer(data['timeInterval'], get_daily_reward, [cookies, task])


def do_task_type1(cookies, task):
    # 执行任务列表中类型为1的任务
    # 判断任务是否可执行 1 可执行； 0 不可执行
    print(f"开始执行{task['taskName']}")
    if task['taskStatus'] == 1:
        get_daily_reward(cookies, task)


def do_task_type2(cookies, task):
    print(f"开始执行{task['taskName']}")
    url = task['gardenBrowseTaskExtResponse']['taskLoadLink']
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
        'channelId': 'dm010205000004',
        'areaId': '110108',
        'currentTime': int(round(time.time() * 1000)),
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
    url = task['gardenBrowseTaskExtResponse']['taskLoadLink']
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
        'currentTime': int(round(time.time() * 1000)),
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
    print('浏览完毕')
    try:
        response = requests.post('https://appapi.dmall.com/app/farm/dofinishTask', headers=finally_headers, data=urlencode(finally_data), verify=False)
    except:
        print("网络请求异常,finish_browser_page")
        return
    result = response.json()
    print('浏览任务1', result)


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

    print('浏览任务1', data)


def do_task_type5(cookies, task):
    print(f"开始执行{task['taskName']}")
    get_daily_reward(cookies, task)


def do_task_type6(cookies, task):
    print(f"开始执行{task['taskName']}")
    # 执行浇水10次
    total_water_count = task['canFinishCount']
    need_water_count = task['finishCount']
    print(f"执行每日浇水任务，需要完成{total_water_count}次, 目前已完成{need_water_count}次")

    i = need_water_count
    while i < total_water_count:
        time.sleep(5)  # 延迟5秒执行
        water_tree(cookies)
        i = i + 1


def do_task_type_default(cookies, task):
    print('default')


def fun_timer(sec, fn, args):
    # print('定时器执行时间:', time.strftime('%Y-%m-%d %H:%M:%S'))
    global timer
    timer = threading.Timer(sec, fn, args)
    timer.start()


def get_url_query(url):
    # 获取url地址中的参数
    query_array = urlparse(url).query.split('&')

    query_dict = {}
    for v in query_array:
        _temp = v.split('=')
        query_dict[_temp[0]] = _temp[1]

    return query_dict


def run():
    print(f"开始运行多点果园自动执行脚本", time.strftime('%Y-%m-%d %H:%M:%S'))
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)

        # 每日签到任务
        daily_sign(cookies)

        # 每日7点领水滴
        daily_seven_clock(cookies)

        # 获取任务列表
        get_task_list(cookies, '获取任务列表')

        time.sleep(30)

        # 获取任务列表, 执行领取奖励
        get_task_list(cookies, '获取任务奖励')


if __name__ == "__main__":
    run()















