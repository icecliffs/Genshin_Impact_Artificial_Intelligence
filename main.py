# -*- coding:utf-8 -*-
# @Time     : 2023/10/15
# @Author   : IceCliffs
# @Github   : https://github.com/icecliffs
# @Software : PyCharm
# @File     : main.py
from typing import Any
from dataclasses import dataclass
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QIcon
import sys

from PyQt6.QtWidgets import QInputDialog, QMessageBox


@dataclass
class Rules:
    x: set
    y: int
class MyForm(QtWidgets.QWidget):
    def processRules(self) -> tuple[list[Any] | list[str], list[Rules], list[Any] | list[str]]:
        dataSets = []
        dataRules = []
        peopleData = []
        with open('data/condition.txt', mode='r', encoding='gbk') as file:
            for line in file:
                dataSets = line.split()
            file.close()
        with open('data/datasets.txt', mode='r', encoding='gbk') as file:
            for line in file:
                tmp = line.split()
                conditions = set(tmp[:-1])
                conclusion = str(tmp[-1])
                dataRules.append(Rules(x=conditions, y=conclusion))
            file.close()
        with open('data/people.txt', mode='r', encoding='gbk') as file:
            for line in file:
                peopleData = line.split()
            file.close()
        return dataSets, dataRules, peopleData
    def __init__(self):
        # 初始化界面
        super().__init__()
        self.setWindowTitle('《原神，提瓦特》人工智能产生式系统')
        self.setWindowIcon(QIcon('./assets/favicon.ico'))
        self.resize(890, 600)
        self.setUpdatesEnabled(True)
        self.ui()
        self.rules = []
        self.rulesReverse = ""
        self.useRules = []
        self.useRulesReverse = []
        self.dynamicRules = ""
        self.dynamicRulesReverse = ""
        self.finalPerson = ""
    def ui(self):
        a,b,c = self.processRules()
        self.label = QtWidgets.QLabel(self)
        self.label.move(30, 30)
        self.label.setText('正向推理数据集')
        self.label.setStyleSheet('font-size:20px; color:#00c')
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.addItems(a)
        self.listWidget.setGeometry(30, 60, 150, 300)
        self.label = QtWidgets.QLabel(self)
        self.label.move(210, 30)
        self.label.setText('反向推理数据集')
        self.label.setStyleSheet('font-size:20px; color:#00c')
        self.listWidget1 = QtWidgets.QListWidget(self)
        self.listWidget1.addItems(c)
        self.listWidget1.setGeometry(210, 60, 150, 300)
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText("添加条件")
        self.btn.setGeometry(30, 365, 150, 45)
        self.btn.clicked.connect(self.addToSelected)
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setText("添加反向条件")
        self.btn1.setGeometry(210, 365, 150, 45)
        self.btn1.clicked.connect(self.addToSelectedReverse)
        self.label = QtWidgets.QLabel(self)
        self.label.move(30, 415)
        self.label.setText('输入的条件')
        self.label.setStyleSheet('font-size:20px; color:#00c')
        self.listWidgetSelected = QtWidgets.QListWidget(self)
        self.listWidgetSelected.setGeometry(30, 450, 150, 100)
        self.label = QtWidgets.QLabel(self)
        self.label.move(380, 30)
        self.label.setText('推理过程')
        self.label.setStyleSheet('font-size:20px; color:#00c')
        self.listWidgetRules = QtWidgets.QListWidget(self)
        self.listWidgetRules.setGeometry(380, 60, 200, 300)
        self.label = QtWidgets.QLabel(self)
        self.label.move(210, 415)
        self.label.setText('最终推理的结果')
        self.label.setStyleSheet('font-size:20px; color:#00c')
        self.listWidgetFinal = QtWidgets.QListWidget(self)
        self.listWidgetFinal.setGeometry(210, 450, 250, 100)
        self.label = QtWidgets.QLabel(self)
        self.label.move(615, 65)
        self.label.setText('人物图片')
        self.label.setStyleSheet('font-size:20px; color:#00c')
        self.img = QtWidgets.QGraphicsView(self)
        self.img.setGeometry(615, 100, 250, 250)
        self.img.setStyleSheet("background: linear-gradient(180deg,#865A2E 0%,#B2732B 100%);")
        self.autoConsider = QtWidgets.QPushButton(self)
        self.autoConsider.setText("自动推理")
        self.autoConsider.setGeometry(520, 410, 150, 45)
        self.autoConsider.clicked.connect(self.clickToConsider)
        self.addRules = QtWidgets.QPushButton(self)
        self.addRules.setText('添加规则')
        self.addRules.setGeometry(680, 410, 150, 45)
        self.addRules.clicked.connect(self.addRulesForm)
        self.addRulesReverse = QtWidgets.QPushButton(self)
        self.addRulesReverse.setText('反向推理')
        self.addRulesReverse.setGeometry(680, 470, 150, 45)
        self.addRulesReverse.clicked.connect(self.clickToConsiderReverse)
        self.clearBtn = QtWidgets.QPushButton(self)
        self.clearBtn.setText("清空")
        self.clearBtn.setGeometry(520, 470, 150, 45)
        self.clearBtn.clicked.connect(self.clearToClear)
    def addRulesForm(self):
        text, ok = QInputDialog.getText(self, '请输入规则', '格式：a,b,c->d\ne.g：枫丹,单手剑,水属性->龙王')
        # print(text, ok)
        if ok:
            self.addRulesToDataSets(text)
    def addToSelected(self):
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            self.rules.append(item.text())
            self.listWidgetSelected.addItem(item.text())
    def addToSelectedReverse(self):
        selected_items = self.listWidget1.selectedItems()
        for item in selected_items:
            self.rulesReverse = (item.text())
        self.listWidgetSelected.addItem(self.rulesReverse)
    def clearToClear(self):
        self.rules = []
        self.useRules = []
        self.useRulesReverse = []
        self.dynamicRulesReverse = []
        self.dynamicRules = ""
        self.listWidgetRules.clear()
        self.listWidgetFinal.clear()
        self.listWidgetSelected.clear()
        self.finalPerson = ""
        self.rulesReverse = ""
        return
    def clickToConsider(self):
        self.forward(self.rules)
        for useRule in self.useRules:
            self.listWidgetRules.addItem(useRule)
        self.listWidgetFinal.addItem(self.dynamicRules)
        self.label1 = QtWidgets.QLabel(self)
        self.label1.move(10, 10)
        self.label1.setText(self.finalPerson)
        self.label1.setStyleSheet('font-size:100px; color:#00c')
        scene = QtWidgets.QGraphicsScene()
        img = QtGui.QPixmap('./assets/{0}.png'.format(self.finalPerson))
        scene.addPixmap(img)
        self.img.setScene(scene)
    def clickToConsiderReverse(self):
        self.reverse(self.rulesReverse)
        for useRule in self.useRulesReverse:
            self.listWidgetRules.addItem(useRule)
        self.listWidgetFinal.addItem(self.dynamicRulesReverse)
    def addRulesToDataSets(self, text):
        print(text)
        import re
        if (re.match('^\s*[\w\s,]+->[\w\s,]+\s*$', text)):
            tmp = str(text).replace(',', ' ').replace('->', ' ')
            with open('./data/datasets.txt', mode='a', encoding='gbk') as file:
                file.writelines('\n' + tmp)
            file.close()
        else:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("格式错误")
            msg_box.setText("输入的格式不符合要求。请使用正确的格式：a,b,c->d")
            msg_box.exec()
    def reverse(self, person):
        dataSets, dataRules, peopleData = self.processRules()
        tmpRule = []
        for pre, last in enumerate(dataRules):
            if person in last.y:
                tmpRule = list(last.x)
        for last in dataRules:
            for rule in tmpRule:
                if rule in last.y and len(last.x) == 1:
                    self.useRulesReverse.append(f"{person}->{rule}->{list(last.x)[0]}")
        self.dynamicRulesReverse = f"{person}->{str(','.join(tmpRule))}"
    def forward(self, rules):
        dataSets, dataRules, peopleData = self.processRules()
        middles = [rule.y for rule in dataRules]
        epoch = 0
        while epoch < len(dataRules):
            cnt = 0
            dataProcess = dataRules[epoch]
            for rule in rules:
                if rule in list(dataProcess.x) or rule == dataProcess.y:
                    cnt += 1
            if cnt == len(dataProcess.x):
                self.useRules.append(str(list(dataProcess.x)[0]))
                if middles[epoch] not in peopleData:
                    conclusion = middles.pop(epoch)
                    if conclusion not in rules:
                        condition = self.forward(rules + [conclusion])
                    else:
                        condition = self.forward(rules)
                    if condition == 1:
                        return 1
                    else:
                        return 0
                else:
                    process = dataRules.pop(epoch)
                    self.dynamicRules = str(','.join(process.x)) + "->" + str(process.y)
                    self.finalPerson = str(process.y)
                    return 1
            else:
                epoch += 1
        return 0
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.show()
    sys.exit(app.exec())