import sys
import os
import cv2 as cv
from gluoncv import data, utils
from mxnet import gluon
import mxnet as mx
import time
import multiprocessing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtWidgets import QMessageBox
from ui5_3 import Ui_MainWindow

import os
my_dir = os.getcwd()


class Result():
    def __init__(self):
        pass

    def struct(self, label, score, left, top, right, bottom):
        self.label = label
        self.score = score
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


def my_sort(a_list, attr):
    a_list_new = [(getattr(x, attr), i, x) for i, x in enumerate(a_list)]
    a_list_new.sort()
    return [x[-1] for x in a_list_new]


def solve(picture_file, ctx):
    classes = ['hat', 'person']
    img = cv.imread(picture_file)
    minn = min(img.shape[0], img.shape[1])
    x, img = data.transforms.presets.yolo.load_test(picture_file, short=minn)
    x = x.as_in_context(ctx)
    net = gluon.SymbolBlock.imports(symbol_file=my_dir + '/conf/mobilenet0.25-symbol.json', input_names=["data"],
                                    param_file=my_dir + '/conf/mobilenet0.25-0000.params')
    box_ids, scores, bboxes = net(x)

    ax = utils.viz.cv_plot_bbox(img, bboxes[0], scores[0], box_ids[0], class_names=classes, thresh=0.3)

    bboxes_np = bboxes.asnumpy()
    scores_np = scores.asnumpy()
    box_ids_np = box_ids.asnumpy()

    ans = []
    for i in range(len(scores[0])):
        if scores[0][i] < 0.3:
            break
        ans.append(Result())
        ans[i].label = classes[int(box_ids_np[0, i])]
        ans[i].score = scores_np[0, i, 0]
        ans[i].left = int(bboxes_np[0][i][0])
        ans[i].top = int(bboxes_np[0][i][1])
        ans[i].right = int(bboxes_np[0][i][2])
        ans[i].bottom = int(bboxes_np[0][i][3])

    ans = my_sort(ans, 'left')
    for i in ans:
        print(i.label, i.score, i.left, i.top, i.right, i.bottom)
    # cv.imshow('image', img[..., ::-1])

    # cv.imwrite(picture_file.split('.')[0] + '_result.jpg', img[..., ::-1])

    return img[..., ::-1], ans


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    _signal = QtCore.pyqtSignal(str)
    _signal_1 = QtCore.pyqtSignal(str)
    _signal_camera = QtCore.pyqtSignal(str)
    _signal_detection = QtCore.pyqtSignal(str)
    ctx = mx.cpu()
    filename = ""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.camera = cv.VideoCapture(0)
        self.is_camera_opened = False
        # 摄像头是否打开

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(30)

        self.timer_camera = QTimer(self)
        self.timer_detection = QTimer(self)

        self._signal.connect(self.ImageFrame)
        self._signal_1.connect(self.ImageFrame)
        self._signal_camera.connect(self.ImageFrame)
        self._signal_detection.connect(self.ImageFrame)

        # 动态显示时间在label上
        self._timer1 = QtCore.QTimer(self)
        self._timer1.timeout.connect(self.showtime)
        self._timer1.start()

    def showtime(self):
        datetime = QDateTime.currentDateTime()
        text = datetime.toString()
        year = text[-4:-1] + '0'
        month = text[3:4]
        day = text[6:8]
        out_text = year + "/" + month + "/" + day + " " + text[9:-8]
        # text = text[2:4] + " " +text[4:8] + " 日 " + text[9:-8]
        self.labeltime.setText(out_text)
        self.labeltime.setStyleSheet(
            "QLabel{color:rgb(255,255,255);font-size:24px;font-weight:bold;font-family:Microsoft YaHei;}"
        )

    def btnBack_Clicked(self):
        self.is_camera_opened = False
        self.btnOpenCamera.setText("打开摄像头")

        self.timer_camera.stop()
        self._timer.stop()
        self.timer_detection.stop()

        self.labelCamera.setPixmap(QPixmap(my_dir + "/image/shot.png"))
        self.labelCapture.setPixmap(QPixmap(my_dir + "/image/shot.png"))
        self.labelResult.setText("")

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''

        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.btnOpenCamera.setText("关闭摄像头")
            self._timer.start()
        else:
            self.btnOpenCamera.setText("打开摄像头")
            self._timer.stop()
            self.timer_detection.stop()

            self.labelCamera.setPixmap(QPixmap(my_dir + "/image/shot.png"))
            self.labelCapture.setPixmap(QPixmap(my_dir + "/image/shot.png"))

    def btnshoot_Clicked(self):
        if not self.is_camera_opened:
            QMessageBox().information(None, "提示", "您没有打开摄像头，不能进行此操作！", QMessageBox.Yes)
            return
        self.labelCamera.setText("")
        self.captured = self.frame
        # 后面这几行代码几乎都一样，可以尝试封装成一个函数
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.labelCapture.setScaledContents(True)

        # self.filename, _ = QFileDialog.getSaveFileName(self, "文件保存", "C:/Users/hs/Desktop/ph",
        #                                                "(*.jpg);;(*.png);;All Files (*)")

        self.filename = my_dir + "/temp/_temp.jpg"

        QImg.save(self.filename, "JPG", 80)
        self._signal_camera.emit(self.filename)

    def btnDetection_Clicked(self):
        if not self.is_camera_opened:
            QMessageBox().information(None, "提示", "您没有打开摄像头，不能进行此操作！", QMessageBox.Yes)
            return

        self.timer_detection.timeout.connect(self.detection)
        self.timer_detection.start(300)

    def detection(self):
        self.labelCamera.setText("")
        self.captured = self.frame
        # 后面这几行代码几乎都一样，可以尝试封装成一个函数
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        # Qt显示图片时，需要先转换成QImgage类型
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.labelCapture.setScaledContents(True)
        if os.path.exists(self.filename):
            os.remove(self.filename)

        self.filename = my_dir + "/temp/_temp.jpg"
        print(self.filename)

        QImg.save(self.filename, "JPG", 80)
        self._signal_detection.emit(self.filename)

    def btnLoadVideo_Clicked(self):
        """ Slot function to start the progamme
            """
        if self.is_camera_opened:
            QMessageBox().information(None, "提示", "请先关闭摄像头！", QMessageBox.Yes)
            return
        videoName, _ = QFileDialog.getOpenFileName(self, "Open", "", "*.mp4;;*.avi;;All Files(*)")
        self.turn = 0
        if videoName != "":  # “”为用户取消
            self.cap = cv.VideoCapture(videoName)
            self.timer_camera.start(400)
            self.timer_camera.timeout.connect(self.openFrame)

    def openFrame(self):
        """ Slot function to capture frame and process it
            """
        if (self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            if ret:
                print(self.filename)
                if os.path.exists(self.filename):
                    os.remove(self.filename)
                img_rows, img_cols, channels = self.frame.shape
                bytesPerLine = channels * img_cols

                cv.cvtColor(self.frame, cv.COLOR_BGR2RGB, self.frame)
                QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
                self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
                    self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

                self.turn += 1
                self.filename = my_dir + "/temp/" + str(self.turn) + '_temp.jpg'
                QImg.save(self.filename, "JPG", 80);
                self._signal_1.emit(self.filename)

            else:
                self.cap.release()
                self.timer_camera.stop()  # 停止计时器

    def btnLoadImage_Clicked(self):
        '''
        从本地读取图片
        '''
        # 打开文件选取对话框
        if self.is_camera_opened:
            QMessageBox().information(None, "提示", "请先关闭摄像头！", QMessageBox.Yes)
            return
        all_filenames, _ = QFileDialog.getOpenFileNames(self, '导入图片')
        # self.filename, _ = QFileDialog.getOpenFileNames(self, '导入图片')
        for file in all_filenames:
            self.filename = file
            if self.filename:
                self.captured = cv.imread(str(self.filename))
            # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
                self.captured = cv.cvtColor(self.captured, cv.COLOR_BGR2RGB)
                rows, cols, channels = self.captured.shape
                bytesPerLine = channels * cols
                QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)

                self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
                    self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                # self.labelCamera.setPixmap(QPixmap.fromImage(QImg))
                # self.labelCamera.setScaledContents(True)
                self._signal.emit(self.filename)

    def ImageFrame(self):
        print(self.filename)
        result, ans = solve(self.filename, self.ctx)
        self.captured = result
        # self.captured = self.frame
        # OpenCV图像以BGR通道存储，显示时需要从BGR转到RGB
        self.captured = cv.cvtColor(self.captured, cv.COLOR_BGR2RGB)
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # time.sleep(3)
        # self.labelCapture.setScaledContents(True)

        person_sum = 0;
        hat_sum = 0
        for i in ans:
            if i.label == 'hat' or i.label == 'person':
                person_sum += 1
            if i.label == 'hat':
                hat_sum += 1
        slogan = ["作业时戴安全帽,流汗总比流血好。", "安全帽是护身宝,上班之前要戴好。"]
        output_ans = "\n\n经检测，画面中一共有 " + str(person_sum) + " 人。其中 " + str(
            hat_sum) + " 人佩戴了安全帽， " + str(person_sum - hat_sum) + " 人未佩戴安全帽。"

        self.labelResult.setText(output_ans)

    def btnShow_Clicked(self):
        self.labelCamera.setPixmap(QPixmap(my_dir + "/image/datashow.jpg"))
        self.labelCapture.setPixmap(
            QPixmap(my_dir + "/image/datashow_3.jpg"))

    def btnclose_Clicked(self):  # 关闭
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.camera.release()
        self.close()

    def btnmax_Clicked(self):
        self.showMaximized()

    def btnmini_Clicked(self):
        self.showMinimized()

    @QtCore.pyqtSlot()
    def _queryFrame(self):  # 原始图像 右下角标签
        '''
        循环捕获图片
        '''
        ret, self.frame = self.camera.read()

        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols
        cv.cvtColor(self.frame, cv.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
