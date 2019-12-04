# 界面文件为 ShowWindow.py
from PyQt5.Qt import *
import sys

from PyQt5.QtWidgets import QTableWidgetItem

from mysql.mysql_class import MysqlConnect

from QT import ShowWindow
# 继承至界面文件的主窗口类
from QT.ShowWindow import Ui_MainWindow
import pymysql

#用于连接数据库
config = {
    "host": "47.102.223.103",
    "port": 3306,
    'database': 'course_design',
    "charset": "utf8",
    "user": "root",
    "password": "aliyun"
}


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.model = QStandardItemModel()
        self.SearchRes_Tab.setModel(self.model)

        self.mysql = MysqlConnect('course_design')
        self.con, self.cur = self.mysql.connect_and_cursor

        # 触发函数确定按钮，重置按钮
        self.Ok_But.clicked.connect(self.search_sql)
        self.Reset_But.clicked.connect(self.on_Reset_But_click)

    '''
    函数还存在错误
    添加查询报错相应机制
    TODOOOOOOOOOOOOO设置窗口关闭时断开数据库连接
    '''
     # 数据库查询函数
    def search_sql(self):
        # 获取自然语言询问文本框的输入
        wquery = self.InQ_Text.toPlainText()
        sqlquery = self.InSql_Text.toPlainText()
        # print(wquery)
        # print(sqlquery)
        self.cur.execute(sqlquery)
        col_name = [t[0] for t in self.cur.description]
        results = self.cur.fetchall()
        col_num = len(col_name)
        row_num = len(results)
        for i in range(col_num):
            self.model.setHorizontalHeaderItem(i, QStandardItem(col_name[i]))
        for i in range(row_num):
            for j in range(col_num):
                t = QStandardItem(str(results[i][j]))
                self.model.setItem(i, j, t)

    #重置按钮响应事件
    def on_Reset_But_click(self):
        # 清空输入框
        self.InSql_Text.clear()
        self.InQ_Text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())