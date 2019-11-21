import requests
import os

from sql_server.sql_server_class import SqlServer


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
}
items = ['school_id', 'name', 'f985', 'f211', 'dual_class_name']


def get_university_logo(s_id):
    url = 'https://static-data.eol.cn/upload/logo/{}.jpg'.format(s_id)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open(os.path.dirname(os.getcwd()) + '\\university_logo\\' + str(s_id) + '.jpg', 'bw') as f:
            f.write(res.content)


def get_university_info():
    sql_server = SqlServer('course_design')
    url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_dual_class=&keyword=&page={}&province_id=&request_type=1&school_type=&signsafe=&size=20&sort=view_total&type=&uri=apigkcx/api/school/hotlists'
    sql = 'insert into schools values(%s, %s, %s, %s, %s)'
    con, cur = sql_server.connect_and_cursor
    for i in range(1, 143):
        tmp_url = url.format(i)
        res = requests.get(tmp_url, headers=headers)
        data = res.json()['data']['item']
        tmp_data = []
        for d in data:
            d[items[4]] = 1 if d[items[4]] == '双一流' else 2
            get_university_logo(d[items[0]])
            tmp = []
            for item in items:
                tmp.append(d[item])
            tmp_data.append(tuple(tmp))
        cur.executemany(sql, tmp_data)
        con.commit()
        print(i, tmp_data[0][0])


if __name__ == '__main__':
    get_university_info()
