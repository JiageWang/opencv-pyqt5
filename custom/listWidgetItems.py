import cv2
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QApplication
from flags import *


class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super().__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))
        self.setBackground(QColor(200, 200, 200))  # color
        self.setSizeHint(QSize(60, 60))  # size


class GrayingItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 灰度化 ', parent=parent)

    def __call__(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_params(self):
        return None

    def update_params(self, param):
        pass


class FilterItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('平滑操作', parent=parent)
        self.__ksize = 3
        self.__kind = MEAN_FILTER
        self.__sigmax = 0

    def get_params(self):
        return {
            'kind': self.__kind,
            'ksize': self.__ksize,
        }

    def update_params(self, param):
        self.__ksize = param['ksize']
        self.__kind = param['kind']

    def __call__(self, img):
        if self.__kind == MEAN_FILTER:
            img = cv2.blur(img, (self.__ksize, self.__ksize))
        elif self.__kind == GAUSSIAN_FILTER:
            img = cv2.GaussianBlur(img, (self.__ksize, self.__ksize), self.__sigmax)
        elif self.__kind == MEDIAN_FILTER:
            img = cv2.medianBlur(img, self.__ksize)
        return img


class MorphItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('形态操作', parent=parent)
        self.__ksize = 3
        self.__kind = ERODE_MORPH
        self.__kshape = RECT_MORPH_SHAPE

    def get_params(self):
        return {
            'kind': self.__kind,
            'ksize': self.__ksize,
            'kshape': self.__kshape
        }

    def update_params(self, param):
        self.__ksize = param['ksize']
        self.__kind = param['kind']
        self.__kshape = param['kshape']

    def __call__(self, img):
        if self.__kind == ERODE_MORPH:
            op = cv2.MORPH_ERODE
        elif self.__kind == DILATE_MORPH:
            op = cv2.MORPH_DILATE
        elif self.__kind == OPEN_MORPH:
            op = cv2.MORPH_OPEN
        elif self.__kind == CLOSE_MORPH:
            op = cv2.MORPH_CLOSE

        if self.__kshape == RECT_MORPH_SHAPE:
            shape = cv2.MORPH_RECT
        elif self.__kshape == ELLIPSE_MORPH_SHAPE:
            shape = cv2.MORPH_ELLIPSE
        elif self.__kshape == CROSS_MORPH_SHAPE:
            shape = cv2.MORPH_CROSS

        kernal = cv2.getStructuringElement(shape, (self.__ksize, self.__ksize))
        img = cv2.morphologyEx(img, op, kernal)
        return img


class GradItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('梯度操作', parent=parent)
        self.__kind = SOBEL_GRAD
        self.__ksize = 3
        self.__dx = 1
        self.__dy = 0

    def get_params(self):
        return {
            'kind': self.__kind,
            'ksize': self.__ksize,
            'dx': self.__dx,
            'dy': self.__dy,
        }

    def update_params(self, param):
        self.__kind = param['kind']
        self.__ksize = param['ksize']
        self.__dx = param['dx']
        self.__dy = param['dy']

    def __call__(self, img):
        if self.__kind == SOBEL_GRAD:
            return cv2.Sobel(img, -1, self.__dx, self.__dy, self.__ksize)
        elif self.__kind == SCHARR_GRAD:
            return cv2.Scharr(img, -1, self.__dx, self.__dy)
        elif self.__kind == LAPLACIAN_GRAD:
            return cv2.Laplacian(img, -1)


