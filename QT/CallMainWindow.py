# 界面文件为 ShowWindow.py
from PyQt5.Qt import *
import sys
from QT import ShowWindow
# 继承至界面文件的主窗口类
from QT.ShowWindow import Ui_MainWindow





class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())