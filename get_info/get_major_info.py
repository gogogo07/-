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
        i += 1
        message = driver.find_element_by_class_name('search-table')
        pattern = re.compile(r'(.*)\n+')
        message1 = pattern.findall(message.text + '\n')
        data = [tuple(message1[i].split()) for i in range(1, len(message1))]
        print(year, i, data[0][0])
        cur.executemany(sql, data)
        con.commit()
        mes = driver.find_element_by_class_name("fypages")
        mes.find_elements_by_tag_name('li')[9].click()
        if i == pages:
            print('爬取成功')
            break


if __name__ == '__main__':
    url1 = r'https://gkcx.eol.cn/linespecialty?schoolyear=2018'
    sql1 = 'insert into major_info2018 values(%s, %s, %s, %s, %s, %s, %s, %s)'
    url2 = r'https://gkcx.eol.cn/linespecialty?schoolyear=2017'
    sql2 = 'insert into major_info2017 values(%s, %s, %s, %s, %s, %s, %s, %s)'
    url3 = r'https://gkcx.eol.cn/linespecialty?schoolyear=2016'
    sql3 = 'insert into major_info2016 values(%s, %s, %s, %s, %s, %s, %s, %s)'
    with ProcessPoolExecutor(3) as pool:
        pool.submit(get_info_major, url1, sql1, 25977, 2018)
        pool.submit(get_info_major, url2, sql2, 26375, 2017)
        pool.submit(get_info_major, url3, sql3, 22134, 2016)