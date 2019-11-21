import requests
import json

from sql_server.sql_server_class import SqlServer


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
}


def get_majors_info():
    pass


if __name__ == '__main__':
    url = 'https://api.eol.cn/gkcx/api/?access_token=&keyword=&level1=&level2=&page=4&signsafe=&size=20&uri=apidata/api/gk/special/lists'
    res = requests.get(url, headers=headers)
    print(len(res.json()['data']['item']))
    for r in res.json()['data']['item']:
        print(r)