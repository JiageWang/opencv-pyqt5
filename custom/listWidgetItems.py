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

    def get_params(self):
        protected = [v for v in dir(self) if v.startswith('_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '')] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)


class GrayingItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 灰度化 ', parent=parent)

    def __call__(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


class FilterItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('平滑操作', parent=parent)
        self._ksize = 3
        self._kind = MEAN_FILTER
        self._sigmax = 0

    def __call__(self, img):
        if self._kind == MEAN_FILTER:
            img = cv2.blur(img, (self._ksize, self._ksize))
        elif self._kind == GAUSSIAN_FILTER:
            img = cv2.GaussianBlur(img, (self._ksize, self._ksize), self._sigmax)
        elif self._kind == MEDIAN_FILTER:
            img = cv2.medianBlur(img, self._ksize)
        return img


class MorphItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('形态操作', parent=parent)
        self._ksize = 3
        self._kind = ERODE_MORPH
        self._kshape = RECT_MORPH_SHAPE

    def __call__(self, img):
        kernal = cv2.getStructuringElement(self._kshape, (self._ksize, self._ksize))
        img = cv2.morphologyEx(img, self._kind, kernal)
        return img


class GradItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('梯度操作', parent=parent)
        self._kind = SOBEL_GRAD
        self._ksize = 3
        self._dx = 1
        self._dy = 0

    def __call__(self, img):
        if self._dx == 0 and self._dy == 0 and self._kind != LAPLACIAN_GRAD:
            self.setBackground(QColor(255, 0, 0))
            self.setText('梯度操作 （无效: dx与dy不同时为0）')
            return img
        else:
            self.setBackground(QColor(200, 200, 200))
            self.setText('梯度操作')
        if self._kind == SOBEL_GRAD:
            return cv2.Sobel(img, -1, self._dx, self._dy, self._ksize)
        elif self._kind == SCHARR_GRAD:
            return cv2.Scharr(img, -1, self._dx, self._dy)
        elif self._kind == LAPLACIAN_GRAD:
            return cv2.Laplacian(img, -1)


class ThresholdItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('阈值操作', parent=parent)
        self._thresh = 127
        self._maxval = 255
        self._type = BINARY_THRESH

    def __call__(self, img):
        print(self._type)
        return cv2.threshold(img, self._thresh, self._thresh, self._type)[1]


class EdgeItem(MyItem):
    def __init__(self, parent=None):
        super(EdgeItem, self).__init__('边缘检测', parent=parent)
        self._thresh1 = 20
        self._thresh2 = 100

    def __call__(self, img):
        return cv2.Canny(img, threshold1=self._thresh1, threshold2=self._thresh2)
