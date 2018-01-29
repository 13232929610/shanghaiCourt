#! C:\Python36\python.exe
# coding:utf-8

import gevent.monkey
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

gevent.monkey.patch_all()  # 协成自动切换

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true', '--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']  # 配置文件


# 获取当前页面的table表格信息
def getTable(url, start, end, file):
    driver = webdriver.PhantomJS(r'E:\phantomjs-2.1.1-windows\bin\phantomjs.exe', service_args=SERVICE_ARGS)  # 无界面浏览器
    driver.set_window_size(1400, 900)  # 设置窗口大小
    wait = WebDriverWait(driver, 10)  # 显示等待
    try:
        driver.get(url)
        time.sleep(10)
        driver.switch_to.frame('search_re')  # 转移到iframe中
        for i in range(start, end + 1):
            js = 'javascript:goPage(' + str(i) + ')'
            driver.execute_script(js)
            print("正在跳转到第%d页..." % (i))
            # 补抓tbody的具体位置
            table = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                'body > form > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td > table > tbody'))
            )
            print(table.text)  # 返回table文本
            file.write(table.text)
            print('第%d页写入完成' % (i))
            time.sleep(10)
    except Exception as e:
        print("出现错误：",e)

    driver.quit()


if __name__ == "__main__":
    url = 'http://www.hshfy.sh.cn/shfy/gweb2017/search_zh.jsp'
    file = open('info.txt', 'w', encoding='utf-8')
    # getTable(url,1,6,file)
    # 创建三个协成,分别加入协成队列中
    gevent.joinall([
        gevent.spawn(getTable, url, 1, 6, file),
        gevent.spawn(getTable, url, 7, 12, file),
        gevent.spawn(getTable, url, 13, 18, file),
    ])
    file.close()
    print('------文档存入完成------')
