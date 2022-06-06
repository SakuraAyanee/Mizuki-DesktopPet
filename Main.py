# 部分代码灵感来自CSDN 原文链接：https://blog.csdn.net/dQCFKyQDXYm3F8rB0/article/details/114957009
# https://blog.csdn.net/hxxjxw/article/details/105923371
# 需要的第三方库：pyQt5系列库

import os
import sys
import random
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):  # 定义顶层函数，自触发以下初始函数，从而使得程序运行
        super(DesktopPet, self).__init__(parent)
        self.init()
        self.initPall()
        self.initPetImage()
        self.petAction()
        # self.RandomTalk()



# 对功能模块开始定义，为实现做基
    def init(self):  # 初始化一个透明的窗口，使得边框 背景为透明，为之后仅lable显示作铺垫
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
        self.repaint()

    def initPall(self):  # 对托盘上的菜单 功能以及图表进行封装与设置
        icons = os.path.join('icon.png')  # 导入预先准备的图标
        quit_action = QAction('Quit',self,triggered=self.quit)  # 添加选项 Quit，链接函数quit
        quit_action.setIcon(QIcon(icons))  # 设置图标
        show = QAction('Show',self,triggered=self.showwin)  # 添加选项 Show，链接函数showwin
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(show)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()

    def petAction(self):
        if self.click_condition == 0 or self.talk_condition == 0:  # 当点击参数和对话参数均为0时触发随机事件
            # print("normal now")
            self.timer = QTimer()
            self.timer.start(10000)
            self.timer.timeout.connect(self.randomAct)


    def initPetImage(self):
        # 定义初始的宠物样式
        #self.talk = QLabel(self)
        self.normal = QLabel(self)  # 用Qlabel来显示宠物
        self.modle = QMovie("gif/Normal/Normal2.gif")
        # 用QMovue的样式来存放（或者说是准备显示）宠物的gif图片
        self.modle.setSpeed(120)  # 设置宠物播放速度为120，使得动作更加自然
        self.modle.setScaledSize(QSize(150,192))
        self.normal.setMovie(self.modle)  # 在normal这一Qlabel中设定Qmovie的播放，播放来源modle
        self.modle.start()
        self.resize(1024,1024)
        self.randomPosition()  # 调用随机位置库，使宠物在随机位置出现
        self.show()
        self.pet1 = []
        for i in os.listdir("gif/waiting"):
            self.pet1.append("gif/waiting/" + i)
        self.normal2 = []
        for i in os.listdir("gif/Normal"):
            self.normal2.append("gif/Normal/" + i)
        self.click = []
        for i in os.listdir("gif/click"):
            self.click.append("gif/click/" + i)
        # print(self.pet1)
        # print(self.normal2)
        self.click_condition = 0
        #  读取waiting文件夹中的动画，以此加入到pet1中

    def randomAct(self):
        # print("s1")
        self.modle = QMovie(random.choice(self.pet1))  # 随机切换pet1中的动画库进行播放
        self.modle.setSpeed(120)
        self.modle.setCacheMode(QMovie.CacheAll)
        self.modle.setScaledSize(QSize(150,192))
        self.normal.setMovie(self.modle)  # 在normal这一Qlabel中设定Qmovie的播放，播放来源modle
        # print(self.modle.loopCount())
        self.modle.start()
        self.modle.finished.connect(self.normalact)

    # def RandomTalk(self):
    #     if self.talk_condition == 1:
    #         self.talkTimer = QTimer()
    #         self.talkTimer.timeout.connect(self.talk)
    #         self.talkTimer.start(3000)

    def normalact(self):
        self.modle = QMovie(random.choice(self.normal2))
        # 用QMovue的样式来存放（或者说是准备显示）宠物的gif图片
        self.modle.setSpeed(120)  # 设置宠物播放速度为120，使得动作更加自然
        self.modle.setScaledSize(QSize(150,192))
        self.normal.setMovie(self.modle)  # 在normal这一Qlabel中设定Qmovie的播放，播放来源modle
        self.modle.start()

    def quit(self):
        self.close()
        sys.exit()

    def showwin(self):
        self.setWindowOpacity(1) # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏

    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()  # 设置窗口的距离，由于之后随机生成，故不做设置，作默认
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()  # 随机生成一个高宽坐标
        self.move(width, height)  # 将窗口移动到随机生成的坐标

    def mousePressEvent(self, event): # 设置点击时的触发以及鼠标状态
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.click_condition = 1
            self.talk_condition = 1
            self.click_()
        self.mouse_pos = event.globalPos() - self.pos()  # event.globalPos()获取
        event.accept()
        self.setCursor(QCursor(Qt.OpenHandCursor))  # 拖动时鼠标图形设置为小手

    def click_(self):
        self.modle = QMovie(random.choice(self.click))
        # 用QMovue的样式来存放（或者说是准备显示）宠物的gif图片
        self.modle.setSpeed(120)  # 设置宠物播放速度为120，使得动作更加自然
        self.modle.setScaledSize(QSize(150, 192))
        self.normal.setMovie(self.modle)  # 在normal这一Qlabel中设定Qmovie的播放，播放来源modle
        self.modle.start()
        self.modle.finished.connect(self.normalact)
        self.modle.finished.connect(self.click_condition_switch_0)


    def click_condition_switch_0(self):
        self.click_condition = 0

    def talk_condition_switch_0(self):
        self.talk_condition = 0

    def talk_condition_switch_1(self):
        self.talk_condition = 1

    def mouseReleaseEvent(self, event):  # 设置非点击时鼠标状态 为普通箭头
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseMoveEvent(self, event):  # 设置点击拖动时的鼠标状态
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_pos)
        event.accept()

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quit = menu.addAction('Quit')
        hide = menu.addAction('Hide')
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal(
        # )方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        if action == quit:  # 点击按钮不同时 出现的功能不同
            qApp.quit()
        if action == hide:
            self.setWindowOpacity(0)

    # def talk(self):
    #     self.modle = QMovie('gif/talk/talk.gif')
    #     # 用QMovue的样式来存放（或者说是准备显示）宠物的gif图片
    #     self.modle.setSpeed(120)  # 设置宠物播放速度为120，使得动作更加自然
    #     self.modle.setScaledSize(QSize(150, 192))
    #     self.normal.setMovie(self.modle)  # 在normal这一Qlabel中设定Qmovie的播放，播放来源modle
    #     self.modle.start()
    #     self.modle.finished.connect(self.normalact)








if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    pet = DesktopPet()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())







