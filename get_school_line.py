import pymssql
from selenium import webdriver
import time
import re
from concurrent.futures import ProcessPoolExecutor


def conn():
    connect = pymssql.connect(host='localhost', user='sa', password='5656', database='course_design',
                              charset='utf8')
    if connect:
        print("连接成功!")
    return connect, connect.cursor()


def get_info(url, sql, pages, year):
    driver = webdriver.Firefox()
    driver.get(url)  # 打开网页
    time.sleep(2)
    m = driver.find_elements_by_class_name('more-search')[1]
    m.find_element_by_tag_name('span').click()
    i = 0
    con, cur = conn()
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
            con.close()
            cur.close()
            print('爬取成功')
            break


if __name__ == '__main__':
    url1 = r'https://gkcx.eol.cn/lineschool?province=&schoolyear=2018'
    url2 = r'https://gkcx.eol.cn/lineschool?province=&schoolyear=2017'
    url3 = r'https://gkcx.eol.cn/lineschool?province=&schoolyear=2016'
    sql1 = 'insert into info2018 values(%s, %s, %s, %s, %s, %s, %s, %s)'
    sql2 = 'insert into info2017 values(%s, %s, %s, %s, %s, %s, %s, %s)'
    sql3 = 'insert into info2016 values(%s, %s, %s, %s, %s, %s, %s, %s)'
    with ProcessPoolExecutor(3) as pool:
        pool.submit(get_info, url1, sql1, 3400, 2018)
        pool.submit(get_info, url2, sql2, 3610, 2017)
        pool.submit(get_info, url3, sql3, 2427, 2016)
    """3400 3610 2427"""