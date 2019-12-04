# 界面文件为 ShowWindow.py
import pymysql
from PyQt5.Qt import *
import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QMainWindow, QApplication
from QT import ShowWindow
# 继承至界面文件的主窗口类
from QT.ShowWindow import Ui_MainWindow

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

        # 触发函数确定按钮，重置按钮
        self.Ok_But.clicked.connect(self.on_Ok_But_click)
        self.Reset_But.clicked.connect(self.on_Reset_But_click)
        # 连接数据库
        self.db = pymysql.connect(**config)
        self.cur = self.db.cursor()

    '''
    函数还存在错误
    添加查询报错相应机制
    未来优化可以加个翻页切换
    TODOOOOOOOOOOOOO设置窗口关闭时断开数据库连接
    '''
     # 数据库查询函数
    def search_sql(self):
        # 获取自然语言询问文本框的输入
        wquery = self.InQ_Text.toPlainText()
        sqlquery = self.InSql_Text.toPlainText()
        # 如果输入为空，报错处理
        if(len(sqlquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的自然语言", QMessageBox.Yes, QMessageBox.Yes))
            return
        if(len(wquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的SQL语句", QMessageBox.Yes, QMessageBox.Yes))
            return
        # self.querymode.setQuery(sqlquery)
        self.cur.execute(sqlquery)       # 执行对应的查询命令
        data = self.cur.fetchall()
        self.rowsum = len(data)  # 总行数
        print(data[0])
        self.colsum = len(data[0])  # 总列数
        print(self.rowsum)
        print(self.colsum)
        print("--------------------")
        if(self.rowsum == 0):
            print(QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes))
            return
        #self.SearchRes_Tab.setModel(self.querymode)
        colname = [tup[0] for tup in self.cur.description]  # 获得列名
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(colname)       # 设置列名
        for i in range(self.rowsum):
            for j in range(self.colsum):
                tempdata = data[i][j]
                finaldata = QStandardItem(str(tempdata))
                self.model.setItem(i, j, finaldata)
        self.SearchRes_Tab.setModel(self.model)             # 结果插入表


    #查询按钮响应事件
    def on_Ok_But_click(self):
        #resetquerymode = QSqlQueryModel()
        #self.SearchRes_Tab.setModel(resetquerymode)
        self.search_sql()




    # 重置按钮响应事件
    def on_Reset_But_click(self):
        # 清空输入框
        self.InSql_Text.clear()
        self.InQ_Text.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())