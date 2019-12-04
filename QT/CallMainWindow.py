# 界面文件为 ShowWindow.py
import pymysql
from PyQt5.Qt import *
import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QMainWindow, QApplication
from pymssql import DataError, ProgrammingError

from QT import ShowWindow
# 继承至界面文件的主窗口类
from QT.ShowWindow import Ui_MainWindow

# 用于连接数据库
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
        # 为表格显示做准备
        self.model = QStandardItemModel()

    '''
    函数还存在错误
    添加查询报错相应机制
    未来优化可以加个翻页切换
    TODOOOOOOOOOOOOO设置窗口关闭时断开数据库连接
    '''
    # 查找数据库数据
    def search(self, sql):
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            return results
        except Exception:
            return -1

    # 获取列名
    def get_colname(self):
        try:
            colname = [tup[0] for tup in self.cur.description]  # 获得列名
            return colname
        except Exception:
            return -1

    # 获取输入的自然语言和SQL语句
    def get_input(self):
        self.wquery = self.InQ_Text.toPlainText()      # 获取输入的自然语言
        self.sqlquery = self.InSql_Text.toPlainText()  # 获取sql语句

    # 输入参数清空/重置
    def init_input(self):
        self.wquery = ""    # 清空输入的自然语言
        self.Sqlquer = ""   # 清空输入的SQL语句
        self.model.clear()  # 清空上一次查询的结果

    # 根据输入的SQL语言对比数据库查询函数
    def search_sql(self):

        # 如果输入为空，报错处理
        if (len(self.wquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的自然语言", QMessageBox.Yes, QMessageBox.Yes))
            return
        if(len(self.sqlquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的SQL语句", QMessageBox.Yes, QMessageBox.Yes))
            return

        # 执行对应的查询命令
        data = self.search(self.sqlquery)
        # 查询异常
        if(data == -1):
            print(QMessageBox.information(self, "提醒", "数据库查询出错！", QMessageBox.Yes, QMessageBox.Yes))
            return
        self.rowsum = len(data)  # 总行数
        # 查询无结果
        if (self.rowsum == 0):
            print(QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes))
            return

        self.colsum = len(data[0])  # 总列数
        # 获得列名
        colname = self.get_colname()
        # 获取列名失败
        if(colname == -1):
            print(QMessageBox.information(self, "提醒", "查询无记录", QMessageBox.Yes, QMessageBox.Yes))
            return
        self.model.setHorizontalHeaderLabels(colname)       # 设置列名
        for i in range(self.rowsum):
            for j in range(self.colsum):
                tempdata = data[i][j]
                finaldata = QStandardItem(str(tempdata))
                self.model.setItem(i, j, finaldata)
        self.SearchRes_Tab.setModel(self.model)             # 结果插入表


    #查询按钮响应事件
    def on_Ok_But_click(self):
        self.init_input()  # 重置
        self.search_sql()

    # 重置按钮响应事件
    def on_Reset_But_click(self):
        # 清空输入框
        self.InSql_Text.clear()
        self.InQ_Text.clear()
        # 重置输入参数
        self.init_input()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())