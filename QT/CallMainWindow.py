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
#encoding=utf-8
from QT.ShowWindow import Ui_MainWindow
import jieba
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
    连接数据库
    加载自定义词典库
    Attributes:
        self.db: 连接数据库
        self.cur：与数据库建立的连接关系
        self.model:表格模型，与UI界面的表格绑定，用于显示信息
        self.sqlkeys:字典类型，sql中提取的关键词列表。
                     关键词有学校school、科目类别subject、批次level、
                     年份year、数字关键词val、专业major、学校层次schoollevel
        self.wkeys:字典类型，自然语言中提取的关键词列表。
                   关键词有学校school、科目类别subject、批次level、
                   年份year、数字关键词val、专业major、学校层次schoollevel
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
        # 加载jieba自定义词典
        jieba.load_userdict("dictionary.txt")
        # 为表格显示做准备
        self.model = QStandardItemModel()
        # sql提取出来的关键词分类列表
        self.sqlkeys = dict()
        self.sqlkeys["school"] = []
        self.sqlkeys["subject"] = []
        self.sqlkeys["subject"] = []
        self.sqlkeys["major"] = []
        self.sqlkeys["level"] = []
        self.sqlkeys["year"] = []
        self.sqlkeys["val"] = []
        self.sqlkeys["schoollevel"] = []
        # 自然语言提取出来的关键词分类列表
        self.wkeys = dict()
        self.wkeys["school"] = []
        self.wkeys["subject"] = []
        self.wkeys["subject"] = []
        self.wkeys["major"] = []
        self.wkeys["level"] = []
        self.wkeys["year"] = []
        self.wkeys["val"] = []
        self.wkeys["schoollevel"] = []
    '''
    添加查询报错相应机制(详细报错)
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
    提取输入的自然语言的关键词
    '''
    def solvewkeys(self):
        wkey = jieba.lcut(self.wquery)  #  对输入的自然语言进行分词
        print(wkey)
        # 分词后再次进行数据筛选，分类的分类，冗余的过滤
        for i in wkey:
            if ("大学" in i) or ("学院" in i):
                self.wkeys["school"].append(i)
                continue
            elif '批' in i:
                self.wkeys["level"].append(i)
                continue
            elif ("文科" in i) or ("理科" in i) or ("综合" in i):
                self.wkeys["subject"].append(i)
                continue
            elif "年" in i:
                self.wkeys["year"].append(i)
                continue
            elif ("985" in i) or ("211" in i) or ("双一流" in i):
                self.wkeys["schoollevel"].append(i)
                continue
            elif "专业" in i:
                self.wkeys["major"].append(i)
                continue
            elif i.isdigit():
                self.wkeys["val"].append(i)  # 内容全是数字，是数字关键词（如分数）
                continue
            else:
                continue
        # 用来测试有没有成功关键词分类
        print("--------------")
        print(self.wkeys["school"])
        print("--------------")
        print(self.wkeys["level"])
        print("--------------")
        print(self.wkeys["subject"])
        print("--------------")
        print(self.wkeys["year"])
        print("--------------")
        print(self.wkeys["val"])
        print("--------------")
        print(self.wkeys["major"])
        print("--------------")
        print(self.wkeys["schoollevel"])

    '''
    获取输入的自然语言和SQL语句
    Returns:
        sqlkey:根据空格切割的字符串列表
    Attributes:
        self.wquery:输入的自然语言
        self.sqlquery:输入的SQL语句
    Tips:
        关键词可以分为下面几种：
        本身就在SQL语句‘’内的，作为值。
        年份关键词，结构是表名（英文+下划线）+四位数字
        纯数字关键词，如分数625，如
        学校属性关键词，一共三种情况：is_985,is_211,_is_yiliu
    '''
    def findsqlkey(self):
        # 匹配查找‘关键词’
        pattern = re.compile(r"'(.*?)'")
        sqlkey = pattern.findall(self.sqlquery)
        # 匹配查找"关键词"
        pattern = re.compile(r"\"(.*?)\"")
        temp1 = pattern.findall(self.sqlquery)
        sqlkey = sqlkey + temp1
        # 匹配查找 年份表  X_2016(结构是 英文字表名+可能有的下划线+四位数字(2016~2018))
        pattern = re.compile(r"\s(\w+\d\d\d\d)")
        temp1 = pattern.findall(self.sqlquery)
        sqlkey = sqlkey + temp1
        # 匹配查找 年份表/学校属性
        pattern = re.compile("is_\w\w\w")
        temp1 = pattern.findall(self.sqlquery)
        sqlkey = sqlkey + temp1
        # 匹配查找 纯数字关键词
        pattern = re.compile(r"\s(\d+)\s")
        temp1 = pattern.findall(self.sqlquery)
        sqlkey = sqlkey + temp1

        # print(sqlkey)
        return sqlkey

    '''
    把输入的SQL命令中提取出来的关键词进行分类
    Attributes:
        self.wquery:输入的自然语言
        self.sqlquery:输入的SQL语句
    '''
    def solvesqlkey(self):
        sqlkeys = self.findsqlkey()  # 从输入的SQL提取的关键词列表
        for i in sqlkeys:
            if ("大学" in i) or ("学院" in i):
                self.sqlkeys["school"].append(i)
                continue
            elif '批' in i:
                self.sqlkeys["level"].append(i)
                continue
            elif ("文科" in i) or ("理科" in i) or ("综合" in i):
                self.sqlkeys["subject"].append(i)
                continue
            elif ('2016' in i) or ('2017' in i) or ('2018' in i):
                self.sqlkeys["year"].append(i)
                continue
            elif ('is_985' in i) or ('is_211' in i) or ("is_yiliu" in i):
                self.sqlkeys["schoollevel"].append(i)
                continue
            else:
                # pattern = re.compile('[0-9]+')
                # match = pattern.findall(i)
                if str(i).isdigit():
                    self.sqlkeys["val"].append(i)    # 内容全是数字，是数字关键词（如分数）
                else:
                    self.sqlkeys["major"].append(i)  # 字符串包含非数字的字符，是专业
                continue

        # 用来测试有没有成功关键词分类
        print("--------------")
        print(self.sqlkeys["school"])
        print("--------------")
        print(self.sqlkeys["level"])
        print("--------------")
        print(self.sqlkeys["subject"])
        print("--------------")
        print(self.sqlkeys["year"])
        print("--------------")
        print(self.sqlkeys["val"])
        print("--------------")
        print(self.sqlkeys["major"])
        print("--------------")
        print(self.sqlkeys["schoollevel"])

    '''
    输入参数清空/重置
    '''
    def init_input(self):
        self.wquery = ""     # 清空输入的自然语言
        self.Sqlquer = ""    # 清空输入的SQL语句
        self.model.clear()   # 清空上一次查询的结果

        self.sqlkeys["school"].clear()    # 清空sql学校关键词列表
        self.sqlkeys["val"].clear()       # 清空sql数字关键词列表
        self.sqlkeys["year"].clear()      # 清空sql年份表关键词列表
        self.sqlkeys["level"].clear()     # 清空sql批次关键词列表
        self.sqlkeys["subject"].clear()   # 清空sql科目关键词列表
        self.sqlkeys["major"].clear()     # 清空sql专业关键词列表
        self.sqlkeys["schoollevel"].clear()  # 清空sql学校层次关键词列表

        self.wkeys["school"].clear()         # 清空自然语言关键词表
        self.wkeys["subject"].clear()
        self.wkeys["subject"].clear()
        self.wkeys["major"].clear()
        self.wkeys["level"].clear()
        self.wkeys["year"].clear()
        self.wkeys["val"].clear()
        self.wkeys["schoollevel"].clear()

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
        self.solvewkeys()
        self.solvesqlkey()  # 测试用
        self.search_sql()  # 执行查询并显示到表格

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