import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def run():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')



    project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    driver_path = os.path.join(project_path, 'utils', 'phantomjs-2.1.1-windows', 'bin', 'phantomjs.exe')

    driver = webdriver.PhantomJS(executable_path=driver_path)

    # script = "var page = this; page.clearCookies();"
    # driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
    # driver.execute('executePhantomScript', {'script': script, 'args': []})
    # expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    driver.get('https://a.dmall.com/act/mhwQ23zOk8t70N.html?nopos=0&tpc=a_201242')
    driver.delete_all_cookies()
    for k, v in cookies.items():
        cookie = {
            'name': k,
            'value': v,
            'domain': '.a.dmall.com',
            'path': '/'
        }
        driver.add_cookie(cookie)


    driver.get('https://a.dmall.com/act/mhwQ23zOk8t70N.html?nopos=0&tpc=a_201242')
    driver.refresh()
    print(driver.get_cookies())
    time.sleep(2)
    d_track_data = driver.execute_script('return window.DmallTracker.getDTrackData()')
    env = driver.execute_script('return window.DmallTracker.getBaseConfigStatistics()')
    print('d_track_data', d_track_data)
    print('env', env)

    driver.quit()





if __name__ == "__main__":
    run()