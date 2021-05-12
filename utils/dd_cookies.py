import os


def get_cookies():
    cookies1 = "tempid=C957C8E6D7400002556F637036001D98; updateTime=1619536169500; device=OnePlus%20OnePlus%20GM1900%20LMY47I; sysVersion=Android-5.1.1; screen=1280*720; apiVersion=5.0.4; dSource=; oaid=; tdc=; utmId=; androidId=7f9abade877db4ed; channelId=dm010000000001; currentTime=1619536221543; abFlag=1-1-B; lastInstallTime=1619536070832; version=5.0.4; tpc=; firstInstallTime=1619536070832; networkType=1; deliveryLng=116.410277; deliveryLat=39.916501; cid=140fe1da9e0470a8adb; sessionId=2cb586b962464037807613239f0826b6; User-Agent=dmall/5.0.4%20Dalvik/2.1.0%20%28Linux%3B%20U%3B%20Android%205.1.1%3B%20GM1900%20Build/LMY47I%29; xyz=ac; appName=com.wm.dmall; smartLoading=1; utmSource=; wifiState=1; gatewayCache=; isOpenNotification=1; inited=true; console_mode=0; uuid=7f9abade877db4ed; store_id=150; storeId=150; vender_id=1; venderId=1; businessCode=1681; appMode=online; storeGroupKey=6d6728171e7121fa5c838248af04be9b@MS0xNTAtMQ; platformStoreGroupKey=43913b6f8c3125d3f87b46aaec7616d4@MjAzMi04MDA4Mg; originBusinessFormat=1-2-4-8; appVersion=5.0.4; platform=ANDROID; dmall-locale=zh_CN; token=10ecd5cb-ba78-49eb-9626-dc5ab9ade16e; ticketName=36F8BF9452B1277AA5F35317986E8E8599D779981D99549DA15FFC266542229131920167F613B1B49F5D218F70C85DA2209341C1D590F8A6F6E4427DB9B9011157FCCB7A267438CBE762AF67E07053E3F6A02CC44E18057C24298CDC9862FEA57833625FCAC4401CE1FD66367BB75250C10F81EAF8C1A8C0867A0096F4C6E5AA; userId=401656357; lat=39.916501; lng=116.410277; addr=%E5%8C%97%E4%BA%AC%E5%B8%82%E4%B8%9C%E5%9F%8E%E5%8C%BA%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; community=%E5%88%A9%E7%94%9F%E5%86%99%E5%AD%97%E6%A5%BC; areaId=110101; session_id=2cb586b962464037807613239f0826b6; env=app; first_session_time=1619536129591; session_count=2; recommend=1; dmTenantId=1; risk=1"
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

