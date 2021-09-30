from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        # self.right_widget.setStyleSheet("background-color:grey;")
        # self.right_widget.setStyleSheet(
        #     "border-image: url(logo2.jpg);")

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_max = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_max.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        self.labellogo = QtWidgets.QLabel("")
        self.labellogo.setObjectName('right_lable')

        self.labeltitle = QtWidgets.QLabel("安全帽检测系统")
        self.labeltitle.setObjectName('right_lable')
        self.labeltitle.setStyleSheet(
            "border-image: url(source/None.png);color : #FFFFFF; ;font-size:60px;font-family : Microsoft Yahei,sans-serif;")
        self.labeltime = QtWidgets.QLabel("时间")
        self.labeltime.setObjectName('right_lable')

        self.labelCamera = QtWidgets.QLabel("")
        self.labelCamera.setObjectName('right_lable2')
        self.labelCapture = QtWidgets.QLabel("")
        self.labelCapture.setObjectName('right_lable3')
        self.labelResult = QtWidgets.QLabel("")
        self.labelResult.setObjectName('right_lable4')

        #pix = QPixmap('./logo3.jpg')
        # self.labellogo.setStyleSheet("border: 2px solid red")
        # self.labellogo.setGeometry(0, 0, 2, 2)
        #self.labellogo.setPixmap(pix)



        self.labelCamera.setScaledContents(True)
        self.labelCapture.setScaledContents(True)

        self.btnOpenCamera = QtWidgets.QPushButton(qtawesome.icon('fa.camera', color='white'), "打开摄像头")
        self.btnOpenCamera.setObjectName('left_button')
        self.btnshoot = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "拍照识别")
        self.btnshoot.setObjectName('left_button')
        self.btnLoadVideo = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'), "导入视频")
        self.btnLoadVideo.setObjectName('left_button')
        self.btnLoadImage = QtWidgets.QPushButton(qtawesome.icon('fa.photo', color='white'), "导入图片")
        self.btnLoadImage.setObjectName('left_button')

        self.btndetection = QtWidgets.QPushButton(qtawesome.icon('fa.user-circle', color='white'), "实时监测")
        self.btndetection.setObjectName('left_button')

        # self.btnback = QtWidgets.QPushButton(qtawesome.icon('fa.newspaper-o', color='white'), "数据统计")
        # self.btnback.setObjectName('left_button')

        self.btnback = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "返回初始界面")
        self.btnback.setObjectName('left_button')



        self.right_layout.addWidget(self.labellogo, 0, 0, 2, 4)
        self.right_layout.addWidget(self.labeltitle, 0, 7, 2, 7)
        self.right_layout.addWidget(self.labeltime, 0, 16, 2, 3)
        self.right_layout.addWidget(self.labelCamera, 4, 1, 4, 8)
        self.right_layout.addWidget(self.labelCapture, 4, 10, 4, 8)
        self.right_layout.addWidget(self.labelResult, 8, 0, 3, 19)

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_max, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)

        # self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)

        self.left_layout.addWidget(self.btnOpenCamera, 2, 0, 1, 3)
        self.left_layout.addWidget(self.btnshoot, 4, 0, 1, 3)
        self.left_layout.addWidget(self.btndetection, 6, 0, 1, 3)
        self.left_layout.addWidget(self.btnLoadImage, 8, 0, 1, 3)
        self.left_layout.addWidget(self.btnLoadVideo, 10, 0, 1, 3)
        self.left_layout.addWidget(self.btnback, 12, 0, 1, 3)


        self.btnOpenCamera.clicked.connect(MainWindow.btnOpenCamera_Clicked)
        self.btnLoadVideo.clicked.connect(MainWindow.btnLoadVideo_Clicked)
        self.btnLoadImage.clicked.connect(MainWindow.btnLoadImage_Clicked)
        # self.btnclose.clicked.connect(MainWindow.btnclose_Clicked)
        self.btnshoot.clicked.connect(MainWindow.btnshoot_Clicked)
        self.left_close.clicked.connect(MainWindow.btnclose_Clicked)
        self.left_max.clicked.connect(MainWindow.btnmax_Clicked)
        self.left_mini.clicked.connect(MainWindow.btnmini_Clicked)
        self.btndetection.clicked.connect(MainWindow.btnDetection_Clicked)
        self.btnback.clicked.connect(MainWindow.btnBack_Clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        pe = QPalette()
        MainWindow.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, QColor(119,136,153))  # 设置背景色
        MainWindow.setPalette(pe)
        self.labelResult.setAlignment(Qt.AlignCenter)
        self.labelResult.setStyleSheet(
            "border-image: url(source/None.png);color:rgb(255,255,255);font-size:26px;font-family:Microsoft YaHei;")
        self.left_mini.setStyleSheet("QPushButton{border-image: url(image/mini.png);border-radius:5px;}"
                                     "QPushButton:hover{border-image: url(image/mini2.png);border-radius:5px;}")
        self.left_close.setStyleSheet("QPushButton{border-image: url(image/close.png);border-radius:5px;}"
                                      "QPushButton:hover{border-image: url(image/close2.png);border-radius:5px;}")
        self.left_max.setStyleSheet("QPushButton{border-image: url(image/max.png);border-radius:5px;}"
                                      "QPushButton:hover{border-image: url(image/max2.png);border-radius:5px;}")
        self.left_widget.setStyleSheet('''
                    QPushButton{border:none;color:white;}
                    QPushButton#left_label{
                        border:none;
                        border-bottom:1px solid white;
                        font-size:18px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                    QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                ''')
        self.right_widget.setStyleSheet('''
                    QWidget#right_widget{
                        color:#232C51;
                        border-image: url(bc3.jpg);
                        background:white;
                        border-top:1px solid darkGray;
                        border-bottom:1px solid darkGray;
                        border-right:1px solid darkGray;
                        border-top-right-radius:10px;
                        border-bottom-right-radius:10px;
                    }
                    QLabel#right_lable{
                        border:none;
                        font-size:16px;
                        font-weight:700;
                        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                    }
                ''')
        #self.setWindowState(Qt.WindowMaximized)
        self.main_layout.setSpacing(0)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
