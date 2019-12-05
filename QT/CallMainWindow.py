# 界面文件为 ShowWindow.py
import pymysql
from PyQt5.Qt import *
import sys
#coding=utf-8
import re
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QMainWindow, QApplication
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

    """
    构造函数初始化
    Attributes:
        self.db: 连接数据库
        self.cur：与数据库建立的连接关系
        self.model:表格模型，与UI界面的表格绑定，用于显示信息
    """
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
    
    执行SQL语句在数据库中获得结果
    Args:
        sql:要执行的SQL语句
    Returns:
        results:查询的结果
        -1：当执行出错时返回标识符-1
    Raises:
        EXception:以防万一，一旦出现任何错就报错。
    '''
    def search(self, sql):
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            return results
        except Exception:
            return -1

    '''
    获取列名
    Returns:
        colname:列名列表
        -1：出错标识符-1
    Raises:
        Exception:以防万一，出现任何错都报错 
    '''
    def get_colname(self):
        try:
            colname = [tup[0] for tup in self.cur.description]  # 获得列名
            return colname
        except Exception:
            return -1

    '''
    获取输入的自然语言和SQL语句
    Attributes:
        self.wquery:输入的自然语言
        self.sqlquery:输入的SQL语句
    '''
    def get_input(self):
        self.wquery = self.InQ_Text.toPlainText()      # 获取输入的自然语言
        self.sqlquery = self.InSql_Text.toPlainText()  # 获取sql语句

    '''
        获取输入的自然语言和SQL语句
        Returns:
            sqlkey:根据空格切割的字符串列表
        '''
    def findwkey(self):
        pattern = re.compile(r"(.*?)")
        wkey = pattern.findall(self.wquery)
        print(wkey)
        return wkey

    '''
    获取输入的自然语言和SQL语句
    Returns:
        sqlkey:根据空格切割的字符串列表
    '''
    def findsqlkey(self):
        # 匹配查找‘关键词’
        pattern = re.compile(r"'(.*?)'")
        sqlkey = pattern.findall(self.sqlquery)
        print("-----------------------")
        print(sqlkey)
        # 匹配查找"关键词"
        pattern = re.compile(r"\"(.*?)\"")
        temp1 = pattern.findall(self.sqlquery)
        print("-----------------------")
        print(temp1)
        sqlkey = sqlkey + temp1
        # 匹配查找 数字关键词
        pattern = re.compile(r"[0-9]+")
        temp1 = pattern.findall(self.sqlquery)
        print("-----------------------")
        print(temp1)
        sqlkey = sqlkey + temp1
        # 匹配查找 年份关键词
        pattern = re.compile(r" .+\d+")
        temp1 = pattern.findall(self.sqlquery)
        print("-----------------------")
        print(temp1)
        sqlkey = sqlkey + temp1

        print(sqlkey)
        return sqlkey

    '''
    输入参数清空/重置
    '''
    def init_input(self):
        self.wquery = ""    # 清空输入的自然语言
        self.Sqlquer = ""   # 清空输入的SQL语句
        self.model.clear()  # 清空上一次查询的结果

    '''
    根据输入的SQL语言对比数据库查询函数
    并把结果显示到表格
    Attributes:
        self.rowsum:结果集（表格显示）总行数
        self.colsum:结果集（表格显示）总列数
    '''
    def search_sql(self):
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

    '''
    查询按钮响应事件
    Attributes:
        self.rowsum:结果集（表格显示）总行数
        self.colsum:结果集（表格显示）总列数
    '''
    def on_Ok_But_click(self):
        self.init_input()  # 重置
        self.get_input()   # 获取输入的自然语言和SQL语句

        # 如果输入为空，报错处理
        if (len(self.wquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的自然语言", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (len(self.sqlquery) == 0):
            print(QMessageBox.information(self, "提醒", "未输入要查询的SQL语句", QMessageBox.Yes, QMessageBox.Yes))
            return

        self.findsqlkey()  # 分析SQL中的关键词
        # self.search_sql()  # 执行查询并显示到表格

    '''
    重置按钮响应事件，清空输入参数和输入显示框
    '''
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