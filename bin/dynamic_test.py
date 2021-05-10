import os
import sys
import time
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

curpath = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_path)
from utils.dd_cookies import get_cookies
from utils.tools import get_target_value, str2dict, serverJ
cookiesList = get_cookies()

# 读取配置文件
cfgpath = os.path.join(curpath, '../conf', 'config.ini')
# 创建管理对象
conf = configparser.ConfigParser()
# 读ini文件
conf.read(cfgpath, encoding="utf-8")
# 读取配置文件中的User Agent
UserAgent = conf['user_agent']['garden_ua']
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     'Mozilla/5.0 (Linux; Android 5.1.1; PCRT00 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 Dmall/5.0.6',
# )
#
# dcap["phantomjs.page.customHeaders.User-Agent"] = (
#     'Mozilla/5.0 (Linux; Android 5.1.1; PCRT00 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 Dmall/5.0.6',
# )
#
# dcap["phantomjs.page.settings.loadImages"] = False #禁止加载图片

# headers = {
#     'Host': 'a.dmall.com',
#     'Connection': 'keep-alive',
#     'Pragma': 'no-cache',
#     'Cache-Control': 'no-cache',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; PCRT00 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 Dmall/5.0.6',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,en-US;q=0.8',
#     'Cookie': 'tempid=C957C6D8F2D0000266C6F4E6E9AC7000; _utm_id=257568882; web_session_count=10; updateTime=1620014350994; device=OPPO%20OPPO%20PCRT00%20LMY47I; sysVersion=Android-5.1.1; screen=1920*1080; apiVersion=5.0.6; dSource=; oaid=; tdc=; utmId=; androidId=52b30fc7470e5be3; channelId=dm010000002006; currentTime=1620443354931; abFlag=1-1-B; lastInstallTime=1620090005685; version=5.0.6; tpc=a_201242; firstInstallTime=1619533954362; networkType=1; deliveryLng=116.410543; deliveryLat=39.916615; cid=18071adc03a741e5d6f; sessionId=ee2adaa57f62447eb846f1d58eaef430; User-Agent=dmall/5.0.6%20Dalvik/2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20PCRT00%20Build/LMY47I%29; xyz=ac; appName=com.wm.dmall; smartLoading=1; utmSource=; wifiState=1; gatewayCache=; sysVersionInt=22; isOpenNotification=1; inited=true; console_mode=0; uuid=52b30fc7470e5be3; store_id=150; storeId=150; vender_id=1; venderId=1; businessCode=9682; appMode=online; storeGroupKey=6d6728171e7121fa5c838248af04be9b@MS0xNTAtMQ; platformStoreGroupKey=344871979a54416f66662534d7eb7a42@MjAzMi04MDA4Mg; originBusinessFormat=1-2-4-8; appVersion=5.0.6; platform=ANDROID; dmall-locale=zh_CN; token=8bb39444-2884-44ef-ba73-15f8ee5fe389; ticketName=9C97E435377962F7854D77C984DAFAF826C9A2F2BD22CFAF22D1757D175D3E5CC50B5007C2DCDD0F9DDBE1F1A0FAF3B0E65CAC5C5063A07BF0CC4CFDC2FEB1F38CA50139B39629AE42FEA5248B9E53DA8FCF711C3A715DE6233904279DB7E31C58262110F339657E5A908245FC77F36C8F2CF0896F6B3B5EB241200FD77092E9; userId=29071278; lat=39.916615; lng=116.410543; addr=%E5%8C%97%E4%BA%AC%E5%B8%82%E4%B8%9C%E5%9F%8E%E5%8C%BA%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; community=%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; areaId=110101; session_id=ee2adaa57f62447eb846f1d58eaef430; env=app; first_session_time=1620353191610; session_count=3; recommend=1; dmTenantId=1; risk=1',
#     'X-Requested-With': 'com.wm.dmall'
#
# }
#
# for key in headers:
#     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]


def run():
    for k, v in enumerate(cookiesList):
        print(f">>>>>>>【账号开始{k+1}】\n")
        cookies = str2dict(v)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 以最高权限运行
        chrome_options.add_argument('--no-sandbox')
        # 不加载图片, 提升速度
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_argument('User-Agent=Mozilla/5.0 (Linux; Android 5.1.1; PCRT00 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Safari/537.36 Dmall/5.0.6')

        chrome_options.add_argument('lang=zh_CN.UTF-8')




        project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        driver_path = os.path.join(project_path, 'utils', 'chromedriver_win32_2', 'chromedriver.exe')
        driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
        # driver = webdriver.Chrome(executable_path=driver_path, desired_capabilities=dcap)
        # script = "var page = this; page.clearCookies();"
        # driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
        # driver.execute('executePhantomScript', {'script': script, 'args': []})
        # expiration = datetime.datetime.now() + datetime.timedelta(days=30)
        driver.get('https://a.dmall.com/act/mhwQ23zOk8t70N.html?nopos=0&tpc=a_201242')
        driver.delete_all_cookies()
        driver.execute_script('localStorage.clear();')
        for k, v in cookies.items():
            cookie = {
                'name': k,
                'value': v,
                'domain': '.dmall.com',
                'path': '/'
            }
            driver.add_cookie(cookie)


        # driver.get('https://a.dmall.com/act/mhwQ23zOk8t70N.html?nopos=0&tpc=a_201242')
        # driver.refresh()
        # user_agent = driver.execute_script("return navigator.userAgent;")
        # print(user_agent)
        # 获取请求头信息
         # 查看请求头是否更改。
        # driver.implicitly_wait(10) # seconds
        d_track_data = driver.execute_script('return window.DmallTracker.getDTrackData()')
        env = driver.execute_script('return window.DmallTracker.getBaseConfigStatistics()')
        print('d_track_data', d_track_data)
        print('env', env)

        driver.quit()

#         try:
#     # 页面一直循环，直到 id="myDynamicElement" 出现
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "myDynamicElement"))
#     )
# finally:
# driver.quit()



if __name__ == "__main__":
    run()