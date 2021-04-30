import os


def get_cookies():
    cookies1 = "tempid=C957C764BD50000210E4171010C91D36; updateTime=1619429326000; device=HUAWEI%20HUAWEI%20YAL-AL00%20LMY47I; sysVersion=Android-5.1.1; screen=1280*720; apiVersion=5.0.4; dSource=; oaid=; tdc=; utmId=; androidId=70c1430d8f180e33; channelId=dm010000000001; currentTime=1619534618614; abFlag=1-1-B; lastInstallTime=1619534455218; version=5.0.4; tpc=; firstInstallTime=1619534455218; networkType=1; deliveryLng=116.410277; deliveryLat=39.916501; cid=160a3797c8a8315f5aa; sessionId=876d9892c72244c8854ef2ca349f1c25; User-Agent=dmall/5.0.4%20Dalvik/2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20YAL-AL00%20Build/LMY47I%29; xyz=ac; appName=com.wm.dmall; smartLoading=1; utmSource=; wifiState=1; gatewayCache=; isOpenNotification=1; inited=true; console_mode=0; uuid=70c1430d8f180e33; store_id=150; storeId=150; vender_id=1; venderId=1; businessCode=1681; appMode=online; storeGroupKey=6d6728171e7121fa5c838248af04be9b@MS0xNTAtMQ; platformStoreGroupKey=43913b6f8c3125d3f87b46aaec7616d4@MjAzMi04MDA4Mg; originBusinessFormat=1-2-4-8; appVersion=5.0.4; platform=ANDROID; dmall-locale=zh_CN; token=ca23a209-c415-4e64-bbd3-5d03730b67e9; ticketName=A514D41153123DCAE3DB465DAFE0FE1F4D4116123140B978113F668820EA821CDE306E5BA281687C853D43129DE1AC99FBBB3E48022897B31562185781D4EA342116FCDA4BA78559A415AF31A5FD26DB3BFA99EE0B382DA8733E1163A56D07A4860FC9A0B4716491E41E4FD157963152272396876117C4A3AA157C9E9C3A7EC9; userId=395388955; lat=39.916501; lng=116.410277; addr=%E5%8C%97%E4%BA%AC%E5%B8%82%E4%B8%9C%E5%9F%8E%E5%8C%BA%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; community=%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; areaId=110101; session_id=876d9892c72244c8854ef2ca349f1c25; env=app; first_session_time=1619534530736; session_count=2; recommend=1; dmTenantId=1; risk=1"
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

