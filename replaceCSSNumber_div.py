import os
import re
import sys
from PyQt5 import QtWidgets

"""
replaceCSSNumber 替换数值脚本

使用方法:
python.exe py脚本 CSS文件路径 相除的数值 

example:
C:/Anaconda3/python.exe d:/Users/Administrator/Desktop/regx_num/replaceCSSNumber.py D:/Users/Administrator/Desktop/regx_num/replace.css 1.5

CSS文件路径 如果只输入文件名会自动在当前路劲下查找文件，找不到则返回错误信息
相除的数值没有填写默认会去 1.5 进行处理
"""
DIR = os.path.dirname(__file__)

class CSSReplaceWindow(QtWidgets.QWidget):
    def __init__(self):
        super(CSSReplaceWindow,self).__init__()
        self.setupUi()

        self.GetPath_BTN.clicked.connect(self.getFilePath)
        self.Output_BTN.clicked.connect(self.outputFile)
    
    def getFilePath(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, '获取文件')[0]
        self.Path_LE.setText(path)
    
    def outputFile(self):
        
        # NOTE 获取输入路径
        target_file = self.Path_LE.text()
        if not os.path.exists(target_file):
            QtWidgets.QMessageBox.warning(self,"警告","获取文件路径不存在")
            self.Path_LE.setText("")
            return

        # NOTE 获取输出数值
        divide_num = self.Number_SP.value()
        if not divide_num:
            QtWidgets.QMessageBox.warning(self,"警告","相除数值不能为零")
            return
        
        # regx = self.Regx_LE.text()
        # try:
        #     regx = re.compile(regx)
        # except:
        #     QtWidgets.QMessageBox.warning(self,"警告","正则表达式不合法")
        #     return

        _,ext = os.path.splitext(target_file)
        # NOTE 获取输出路径
        save_path = QtWidgets.QFileDialog.getSaveFileName(self,'输出文件路径')[0]
        if not save_path:
            return
        name,_ = os.path.splitext(save_path)
        save_path = name + ext

        # NOTE 读取文件
        with open(target_file, 'r', encoding="utf-8") as f:
            content = f.read()

        # NOTE 匹配数字以及点号
        regx = r"(?P<value>(?:\d|\.)*?)px"
        # NOTE 将匹配的数字除以数值

        def numberHandler(matched):
            value = float(matched.group('value'))
            return str(round(value / divide_num,2)) + "px"

        content = re.sub(regx, numberHandler, content)

        # NOTE 输出替换的文本
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(content)
            QtWidgets.QMessageBox.information(self, "输出成功", "%s\n输出成功"% save_path)

    def setupUi(self):
        self.setObjectName("window")
        self.resize(308, 300)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.GetPath_BTN = QtWidgets.QPushButton(self)
        self.GetPath_BTN.setObjectName("GetPath_BTN")
        self.gridLayout.addWidget(self.GetPath_BTN, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.Path_LE = QtWidgets.QLineEdit(self)
        self.Path_LE.setObjectName("Path_LE")
        self.gridLayout.addWidget(self.Path_LE, 0, 2, 1, 1)
        self.Number_SP = QtWidgets.QDoubleSpinBox(self)
        self.Number_SP.setValue(1.5)
        self.Number_SP.setObjectName("Number_SP")
        self.gridLayout.addWidget(self.Number_SP, 1, 2, 1, 1)
        self.Output_BTN = QtWidgets.QPushButton(self)
        self.Output_BTN.setObjectName("Output_BTN")
        self.gridLayout.addWidget(self.Output_BTN, 3, 0, 1, 3)
        self.setWindowTitle("CSS文件批量替换数值")
        self.GetPath_BTN.setText("获取文件路径")
        self.label.setText("相除数值")
        self.Output_BTN.setText("输出文件")

        # self.label_2 = QtWidgets.QLabel(self)
        # self.label_2.setObjectName("label_2")
        # self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        # self.Regx_LE = QtWidgets.QLineEdit(self)
        # self.Regx_LE.setObjectName("Regx_LE")
        # self.gridLayout.addWidget(self.Regx_LE, 2, 2, 1, 1)
        # self.label_2.setText("正则表达式")
        # self.Regx_LE.setText("(?P<value>(?:\\d|\\.)*?)px")

def replaceCSSNumber(file_name="",divide_num="1.5"):

    # NOTE 判断第一个参数是否合法
    if not os.path.exists(file_name):
        target_file = os.path.join(DIR, file_name)
        if not os.path.exists(target_file):
            print("请输入正确的文件的名称")
            return
    else:
        target_file = file_name
    
    # NOTE 判断第二个参数是否合法
    try:
        divide_num = float(divide_num)
    except:
        print("请输入正确的数字")
        return

    # NOTE 读取文件
    with open(target_file, 'r',encoding="utf-8") as f:
        content = f.read()

    # NOTE 匹配数字以及点号
    regx = r"(?P<value>(?:\d|\.)*?)px"
    # NOTE 将匹配的数字除以数值
    def numberHandler(matched):
        value = float(matched.group('value'))
        return str(round(value / divide_num,2)) + "px"
    
    content = re.sub(regx, numberHandler, content)

    # NOTE 输出替换的文本
    with open(target_file, 'w', encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = CSSReplaceWindow()
    window.show()
    app.exec_()
    # # NOTE 判断脚本获取的参数数量
    # if len(sys.argv) == 1:
    #     print ("请输入替换文件的名称")
    # elif len(sys.argv) == 2:
    #     replaceCSSNumber(sys.argv[1])
    # elif len(sys.argv) == 3:
    #     replaceCSSNumber(sys.argv[1],sys.argv[2])
