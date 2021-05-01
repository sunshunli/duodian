import os


def get_cookies():
    cookies1 = "tempid=C957C6D8F2D0000266C6F4E6E9AC7000; updateTime=1619429326000; device=OPPO%20OPPO%20PCRT00%20LMY47I; sysVersion=Android-5.1.1; screen=1920*1080; apiVersion=5.0.4; dSource=; oaid=; tdc=; utmId=; androidId=52b30fc7470e5be3; channelId=dm010000000001; currentTime=1619534107933; abFlag=1-1-B; lastInstallTime=1619533954362; version=5.0.4; tpc=; firstInstallTime=1619533954362; networkType=1; deliveryLng=116.410277; deliveryLat=39.916501; cid=18071adc03a741e5d6f; sessionId=0cc6e4732ecd40d7b285b8a69231d332; User-Agent=dmall/5.0.4%20Dalvik/2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20PCRT00%20Build/LMY47I%29; xyz=ac; appName=com.wm.dmall; smartLoading=1; utmSource=; wifiState=1; gatewayCache=; isOpenNotification=1; inited=true; console_mode=0; uuid=52b30fc7470e5be3; store_id=150; storeId=150; vender_id=1; venderId=1; businessCode=1681; appMode=online; storeGroupKey=6d6728171e7121fa5c838248af04be9b@MS0xNTAtMQ; platformStoreGroupKey=43913b6f8c3125d3f87b46aaec7616d4@MjAzMi04MDA4Mg; originBusinessFormat=1-2-4-8; appVersion=5.0.4; platform=ANDROID; dmall-locale=zh_CN; token=8bb39444-2884-44ef-ba73-15f8ee5fe389; ticketName=9C97E435377962F7854D77C984DAFAF826C9A2F2BD22CFAF22D1757D175D3E5CC50B5007C2DCDD0F9DDBE1F1A0FAF3B0E65CAC5C5063A07BF0CC4CFDC2FEB1F38CA50139B39629AE42FEA5248B9E53DA8FCF711C3A715DE6233904279DB7E31C58262110F339657E5A908245FC77F36C8F2CF0896F6B3B5EB241200FD77092E9; userId=29071278; lat=39.916501; lng=116.410277; addr=%E5%8C%97%E4%BA%AC%E5%B8%82%E4%B8%9C%E5%9F%8E%E5%8C%BA%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; community=%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; areaId=110101; session_id=0cc6e4732ecd40d7b285b8a69231d332; env=app; first_session_time=1619533967581; session_count=2; recommend=1; dmTenantId=1; risk=1"
    cookies2 = ""


    cookiesList = [cookies1, ]  # 多账号准备
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

    return cookiesList

