import cv2
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from windows.main_window import Ui_MainWindow  # 由qtdesigner 生成的布局


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.src_img = None
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            """
            QLabel{
            background: #4B4B4B
            }
            """
        )
        self.stackedWidget.close()

    def update_label(self):
        if self.src_img is None:
            return
        img = self.src_img.copy()
        for i in range(self.useListWidget.count()):
            img = self.useListWidget.item(i)(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # bgr -> rgb
        h, w, c = img.shape  # 获取图片形状
        image = QImage(img, w, h, 3 * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)

        self.item = QGraphicsPixmapItem(pixmap)  # 创建像素图元
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.label.setScene(self.scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
