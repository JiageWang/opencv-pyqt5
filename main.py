import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from custom.stackedWidget import StackedWidget
from custom.treeView import FileSystemTreeView
from custom.listWidgets import FuncListWidget, UsedListWidget
from custom.graphicsView import GraphicsView


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.useListWidget = UsedListWidget(self)
        self.funcListWidget = FuncListWidget(self)
        self.stackedWidget = StackedWidget(self)
        self.fileSystemTreeView = FileSystemTreeView(self)
        self.graphicsView = GraphicsView(self)

        self.dock1 = QDockWidget(self)
        self.dock1.setWidget(self.fileSystemTreeView)
        self.dock1.setTitleBarWidget(QLabel('目录'))
        self.dock1.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock2 = QDockWidget(self)
        self.dock2.setWidget(self.funcListWidget)
        self.dock2.setTitleBarWidget(QLabel())
        self.dock2.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock3 = QDockWidget(self)
        self.dock3.setWidget(self.useListWidget)
        self.dock3.setTitleBarWidget(QLabel('已选操作'))
        self.dock3.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.dock4 = QDockWidget(self)
        self.dock4.setWidget(self.stackedWidget)
        self.dock4.setTitleBarWidget(QLabel('属性'))
        self.dock4.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock4.close()

        self.setCentralWidget(self.graphicsView)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock1)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock2)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock3)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock4)

        self.setWindowTitle('Opencv图像处理')
        self.setWindowIcon(QIcon('icons/main.png'))
        self.src_img = None

    def update_image(self):
        if self.src_img is None:
            return
        img = self.process_image()
        self.graphicsView.update_image(img)

    def change_image(self, img):
        self.src_img = img
        img = self.process_image()
        self.graphicsView.change_image(img)

    def process_image(self):
        img = self.src_img.copy()
        for i in range(self.useListWidget.count()):
            img = self.useListWidget.item(i)(img)
        return img


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
