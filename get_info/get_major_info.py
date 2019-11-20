import requests

from concurrent.futures import ProcessPoolExecutor
from sql_server.sql_server_class import SqlServer


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
}
items = ['name', 'spname', 'local_province_name',
         'local_type_name', 'year', 'local_batch_name', 'average', 'min']


def get_info_major(start, url, sql, pages, year):
    sql = sql.format(year)
    sql_server = SqlServer('course_design')
    con, cur = sql_server.connect_and_cursor
    for i in range(start, pages + 1):
        tmp_url = url.format(i, year)
        res = requests.get(tmp_url, headers=headers)
        data = res.json()['data']['item']
        tmp_data = []
        for d in data:
            tmp = []
            for item in items:
                tmp.append(d[item])
            tmp_data.append(tuple(tmp))
        cur.executemany(sql, tmp_data)
        con.commit()
        print(year, i, tmp_data[0][0])


if __name__ == '__main__':
    # 11340
    sql = 'insert into major_info{} values(%s, %s, %s, %s, %s, %s, %s, %s)'
    url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_dual_class=&keyword=&local_batch_id=&local_type_id=&page={}&province_id=&school_type=&signsafe=&size=20&type=&uri=apidata/api/gk/score/special&year={}'
    get_info_major(17215, url, sql, 25977, 2018)