import cv2
import numpy as np

from PyQt5.QtWidgets import *


class FileSystemTreeView(QTreeView, QDockWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath('.')
        self.setModel(self.fileSystemModel)
        self.setAnimated(True)
        self.doubleClicked.connect(self.select_image)
        self.setMinimumWidth(200)
        # self.setStyleSheet(
        #     """
        #     QTreeView{
        #     show-decoration-selected: 1;
        #     }
        #     QTreeView::item {
        #     height: 30px;
        #     }
        #     QTreeView::branch:has-children:!has-siblings:closed,
        #     QTreeView::branch:closed:has-children:has-siblings {
        #     border-image: none;
        #     }
        #
        #     QTreeView::branch:open:has-children:!has-siblings,
        #     QTreeView::branch:open:has-children:has-siblings  {
        #     border-image: none;
        #     }
        #     """)
        # self.show()

    def select_image(self, file_index):
        file_name = self.fileSystemModel.filePath(file_index)
        if file_name.endswith(('.jpg', '.png', '.bmp')):
            src_img = cv2.imdecode(np.fromfile(file_name, dtype=np.uint8), -1)
            self.mainwindow.change_image(src_img)
