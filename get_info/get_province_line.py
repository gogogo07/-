import requests

from sql_server.sql_server_class import SqlServer


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
}
items = ['local_province_name', 'year', 'local_type_name', 'local_batch_name', 'average']
province = [11, 12, 13, 41, 37, 14, 61, 15, 21, 22, 23, 31, 32, 34, 36, 42,
            43, 50, 51, 52, 53, 44, 45, 35, 62, 64, 65, 54, 46, 33, 63]


def get_province_line():
    sql = 'insert into province_line_info values(%s, %s, %s, %s, %s)'
    url = 'https://api.eol.cn/gkcx/api/?access_token=&page=1&province_id={}' \
          '&signsafe=&size=20&uri=apidata/api/gk/score/proprovince&year={}'
    sql_server = SqlServer('course_design')
    con, cur = sql_server.connect_and_cursor
    for year in range(2016, 2019):
        for province_id in province:
            tmp_url = url.format(province_id, year)
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
            print(year, tmp_data[0][0])


if __name__ == '__main__':
    get_province_line()