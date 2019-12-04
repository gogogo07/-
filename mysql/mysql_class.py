import pymysql
import json
import os


class MysqlConnect:
    """自定义一个连接MySql的类"""

    def __init__(self, database, is_close_auto=True):
        self._database = database
        self._connect = None
        self._cursor = None
        self._is_close_auto = is_close_auto
        self.connect_to_mysql()

    def connect_to_mysql(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\config.json', 'r') as f:
            config = json.load(f)
        self._connect = pymysql.connect(database=self._database, **config)
        if self._connect:
            self._cursor = self.connect.cursor()

    @property
    def connect(self):
        return self._connect

    @property
    def connect_and_cursor(self):
        return self._connect, self._cursor

    def creat_table(self, table):
        pass

    def insert(self, table, *args):
        pass

    def __del__(self):
        if self._is_close_auto:
            if self._cursor:
                print('cursor close')
                self._cursor.close()
            if self._connect:
                print('connect close')
                self._connect.close()


if __name__ == '__main__':
    mysql = MysqlConnect('course_design')
    con, cur = mysql.connect_and_cursor
    sql = 'select s_id "学校码", s_name "学校", ' \
          'is_985 "985", is_211 "211", is_yiliu "双一流" from schools limit 0, 20'
    cur.execute(sql)
    print(cur)
    print(cur.description)
