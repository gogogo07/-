import pymssql


class SqlServer():
    """封装的sql server类"""

    def __init__(self, database, host='localhost',
                 charset='utf8', user='sa', password='5656',
                 is_close_auto=True):
        self._host = host
        self._database = database
        self._charset = charset
        self._user = user
        self._password = password
        self._connect = None
        self._cursor = None
        self._is_close_auto = is_close_auto
        self.connect_to_sql_server()

    def connect_to_sql_server(self):
        self._connect = pymssql.connect(host=self._host, user=self._user,
                                        password=self._password, database=self._database,
                                        charset=self._charset)
        if self._connect:
            self._cursor = self._connect.cursor()

    @property
    def connect(self):
        return self._connect

    @property
    def connect_and_cursor(self):
        return self._connect, self._cursor

    def __del__(self):
        if self._is_close_auto:
            if self._cursor:
                print('cur')
                self._cursor.close()
            if self._connect:
                print('con')
                self._connect.close()


if __name__ == '__main__':
    sql_server = SqlServer('course_design')