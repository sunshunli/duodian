import os


def get_cookies():
    cookies1 = ""
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

