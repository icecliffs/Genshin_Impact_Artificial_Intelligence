# encoding=utf-8
#
#  Created by IceCliffs
#  Date 2023/10/02 07:20
#  Description @IceCliffs (https://github.com/icecliffs)
#  Blog        @IceCliffs (https://iloli.moe)
#
from dataclasses import dataclass
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QLinearGradient, QColor, QImage, QPainter
import sys

from PyQt6.QtWidgets import QLabel


# 初始化生成式条件
@dataclass
class Rules:
    x: set
    y: int
def initRules():
    dataSets = {
        1: "位于东北部",2: "位于中部",3: "位于西北",4: "位于中东",5: "岛国",
        6: "位于提瓦特外",7: "远程武器",8: "近战武器",9: "很长",10: "水属性",11: "雷属性",12: "草属性",13: "风属性",14: "火属性",15: "岩属性",16: "魔神",17: "治疗",18: "特产探索",19: "自身附魔",20: "伤害提升",21: "单手剑",22: "长柄武器",23: "弓箭",24: "法器",25: "稻妻",26: "蒙德",27: "璃月",28: "须弥",29: "枫丹",30: "艾尔海森",31: "珊瑚宫心海",32: "雷电将军",33: "八重神子",34: "温迪",35: "班尼特",36: "可莉",37: "刻晴",38: "烟绯",39: "钟离",40: "纳西妲",41: "芙宁娜",42: "旅行者（你自己）",43: "带羽毛",44: "参加魔神战争"
    }
    # 规则:结论
    dataRules = [
        Rules(set([1]), 26),
        Rules(set([2]), 27),
        Rules(set([3]), 29),
        Rules(set([4]), 28),
        Rules(set([5]), 25),
        Rules(set([7]), 24),
        Rules(set([8]), 21),
        Rules(set([7, 43]), 23),
        Rules(set([44]), 16),
        Rules(set([6]), 42),
        Rules(set([8, 9]), 22),
        Rules(set([25, 24, 10, 17]), 31),
        Rules(set([25, 22, 11, 16]), 32),
        Rules(set([25, 24, 11, 20]), 33),
        Rules(set([26, 16, 23, 13]), 34),
        Rules(set([26, 17, 21, 14]), 35),
        Rules(set([26, 18, 24, 14]), 36),
        Rules(set([27, 19, 21, 11]), 37),
        Rules(set([27, 18, 24, 14]), 38),
        Rules(set([27, 16, 22, 15]), 39),
        Rules(set([28, 16, 24, 12]), 40),
        Rules(set([28, 21, 12]), 30),
        Rules(set([29, 16, 21, 10]), 41)
    ]
    # 存储人物
    personData = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43]
    return dataSets, dataRules, personData

# 添加规则
def addRules(rules):
    global dataSets, dataRules, personData
    dataSets, dataRules, personData = initRules()


class MyForm(QtWidgets.QWidget):
    def __init__(self):
        # 初始化界面
        super().__init__()
        self.setWindowTitle('《原神，提瓦特》角色识别')
        self.setWindowIcon(QIcon('./assets/favicon.ico'))
        self.resize(800, 600)
        self.setUpdatesEnabled(True)
        self.ui()
        # 存储放入的规则
        self.rules = []
        # 使用规则
        self.useRules = []
        # 动态数据库
        self.dynamicRules = ""
        # 存储结果
        self.finalPerson = ""
    # 对其进行反向推理
    # def reverseInference(self, rules ...):
    #
    # 对其进行正向推理
    def forwardInference(self, rules):
        # 存储匹配到的数据长度
        dataSets, dataRules, personData = initRules()
        # 存储中间结论
        middles = [rule.y for rule in dataRules]
        # 对规则库进行查找
        for epoch, dataProcess in enumerate(dataRules):
            num = 0
            for rule in rules:
                if rule in list(dataProcess.x) or rule == dataProcess.y:
                    num += 1
            # 如果规则库判断规则当中数值相同，则继续查询，看是否为最终结果
            if num == len(dataProcess.x):
                if middles[epoch] not in personData:
                    # 结果
                    result = middles.pop(epoch)
                    process = list(dataRules.pop(epoch).x)[0]
                    # 判断结果是否已经存储在过程中，如果存在重新查找，不存在的话加入过程
                    if result not in rules:
                        self.useRules.append(str(dataSets.get(process) + "->" + str(dataSets.get(result))))
                        condition = self.forwardInference(rules + [result])
                        if condition == 1:
                            return 1
                        else:
                            return 0
                    else:
                        condition = self.forwardInference(rules)
                        if condition == 1:
                            return 1
                        else:
                            return 0
                else:
                    process = dataRules.pop(epoch)
                    for t in process.x:
                        self.dynamicRules += (dataSets.get(t) + "->")
                    self.dynamicRules += dataSets.get(middles[epoch])
                    self.finalPerson = middles[epoch]
                    return 1
    def ui(self):
        # 设置文字
        self.label = QtWidgets.QLabel(self)
        self.label.move(10, 10)
        self.label.setText('原来，你也玩原神')
        self.label.setStyleSheet('font-size:30px; color:#00c')
        # 设置列表（前提条件）
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.addItems(
            ["位于东北部","位于中部","位于西北","位于中东","岛国","位于提瓦特外","远程武器","近战武器","很长","水属性","雷属性","草属性","风属性","火属性","岩属性","参加魔神战争","治疗","特产探索","自身附魔","伤害提升", "带羽毛"]
        )
        self.listWidget.setGeometry(30, 60, 150, 300)
        # 设置按钮（添加条件按钮）
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText("添加条件")
        self.btn.setGeometry(30, 365, 150, 45)
        self.btn.clicked.connect(self.addToSelected)
        # 设置列表（前提条件选中）
        self.listWidgetSelected = QtWidgets.QListWidget(self)
        self.listWidgetSelected.setGeometry(30, 420, 150, 100)
        # 设置列表（使用规则）
        self.listWidgetRules = QtWidgets.QListWidget(self)
        self.listWidgetRules.setGeometry(230, 60, 250, 300)
        # 设置列表（推导结果）
        self.listWidgetFinal = QtWidgets.QListWidget(self)
        self.listWidgetFinal.setGeometry(230, 380, 250, 140)
        # 设置图片（最后结论）
        self.img = QtWidgets.QGraphicsView(self)
        self.img.setGeometry(515, 100, 250, 250)
        self.img.setStyleSheet("background: linear-gradient(180deg,#865A2E 0%,#B2732B 100%);")
        # 设置按钮（自动推理）
        self.autoConsider = QtWidgets.QPushButton(self)
        self.autoConsider.setText("自动推理")
        self.autoConsider.setGeometry(520, 410, 150, 45)
        self.autoConsider.clicked.connect(self.clickToConsider)
        # 设置按钮（清空）
        self.clearBtn = QtWidgets.QPushButton(self)
        self.clearBtn.setText("清空")
        self.clearBtn.setGeometry(520, 470, 150, 45)
        self.clearBtn.clicked.connect(self.clearToClear)
    def clickToConsider(self):
        if self.rules == None:
            self.msgBox = QtWidgets.QMessageBox(self)
            self.msgBox.information(self, '警告', '你没有添加任何规则')
        dataSets, dataRules, personData = initRules()
        self.forwardInference(self.rules)
        for useRule in self.useRules:
            self.listWidgetRules.addItem(useRule)
        self.listWidgetFinal.addItem(self.dynamicRules)
        result = "推理结果：" + str(dataSets.get(self.finalPerson))
        # 设置标签（推理结果）
        self.label1 = QtWidgets.QLabel(self)
        self.label1.move(10, 10)
        self.label1.setText(result)
        self.label1.setStyleSheet('font-size:100px; color:#00c')
        scene = QtWidgets.QGraphicsScene()
        img = QtGui.QPixmap('./assets/{0}.png'.format(self.finalPerson))
        scene.addPixmap(img)
        self.img.setScene(scene)
    def clearToClear(self):
        self.rules = []
        self.useRules = []
        self.dynamicRules = []

        self.label1.setText('')
        self.listWidgetRules.clear()
        self.listWidgetFinal.clear()
        self.listWidgetSelected.clear()
        return
    def addToSelected(self):
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            self.listWidgetSelected.addItem(item.text())
            index = self.listWidget.row(item)
            print(index)
            if index == 20:
                self.rules.append(43)
            elif index == 15:
                self.rules.append(44)
            else:
                self.rules.append(index + 1)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyForm()
    Form.show()
    sys.exit(app.exec())