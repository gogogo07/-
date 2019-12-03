# 界面文件为 ShowWindow.py
from PyQt5.Qt import *
import sys

from PyQt5.QtWidgets import QTableWidgetItem

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
    # 连接数据库
    con = pymysql.connect(**config)
    cur = con.cursor()

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        # 触发函数确定按钮，重置按钮
        self.Ok_But.clicked.connect(self.on_Ok_But_click)
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
        MyMainWindow.cur.execute(sqlquery)
        rows = MyMainWindow.cur.fetchall()
        row = MyMainWindow.cur.rowcount   #取得记录个数，用于设置表格行数
        vol = len(rows[0])                #取得字段数，用于设置表格的列数
        self.SearchRes_Tab.setRowCount(row)
        self.SearchRes_Tab.setColumnCount(vol)
        for i in range(row):
            for j in range(vol):
                temp_data = rows[i][j]  #临时记录，不能直接插入表格
                data = QTableWidgetItem(str(temp_data))  #转换后可插入表格
                self.SearchRes_Tab.setItem(i, j, data)




    #查询按钮响应事件
    def on_Ok_But_click(self):
        MyMainWindow.search_sql(self)



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