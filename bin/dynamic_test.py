import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def run():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    curpath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # driver_path = os.path.join(curpath, 'utils', 'chromedriver_win32_2', 'chromedriver.exe')
    driver_path = os.path.join(curpath, 'utils', 'phantomjs-2.1.1-windows', 'bin', 'phantomjs.exe')

    sys.path.append(driver_path)
    # driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver = webdriver.PhantomJS(executable_path=driver_path)

    driver.get('https://a.dmall.com/act/mhwQ23zOk8t70N.html?nopos=0&tpc=a_201242')
    # print(driver.page_source)
    print("Title: {0}".format(driver.title))
    driver.execute_script('console.log(window.DmallTracker.getDTrackData())')
    print(driver.get_log('browser'))
    time.sleep(2)
    driver.quit()





if __name__ == "__main__":
    run()