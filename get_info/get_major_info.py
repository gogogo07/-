import time
import re

from selenium import webdriver
from concurrent.futures import ProcessPoolExecutor
from sql_server.sql_server_class import SqlServer


def get_info_major(url, sql, pages, year):
    sql_server = SqlServer('course_design')
    driver = webdriver.Firefox()
    driver.get(url)  # 打开网页
    time.sleep(2)
    m = driver.find_elements_by_class_name('more-search')[1]
    m.find_element_by_tag_name('span').click()
    i = 0
    con, cur = sql_server.connect_and_cursor
    while True:
        class_name = 'search-table'
        message = driver.find_element_by_class_name(class_name)
        pattern = re.compile(r'(.*)\n+')
        message1 = pattern.findall(message.text + '\n')
        data = [tuple(message1[i].split()[:-1]) for i in range(1, len(message1))]
        print(year, i, data[0][0])
        cur.executemany(sql, data)
        con.commit()
        mes = driver.find_element_by_class_name("fypages")
        mes.find_elements_by_tag_name('li')[9].click()
        i += 1
        if i == pages:
            print('爬取成功')
            break


if __name__ == '__main__':
    url1 = r'https://gkcx.eol.cn/lineschool?province=&schoolyear=2018'
    sql1 = 'insert into test values(%s, %s, %s, %s, %s, %s, %s, %s)'
    get_info_major(url1, sql1, 7, 2018)
    with ProcessPoolExecutor(3) as pool:
        pass