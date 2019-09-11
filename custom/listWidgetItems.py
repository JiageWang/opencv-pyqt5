import numpy as np
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QListWidgetItem, QPushButton
from flags import *


class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__(name, parent=parent)
        self.setIcon(QIcon('icons/color.png'))
        self.setSizeHint(QSize(60, 60))  # size

    def get_params(self):
        protected = [v for v in dir(self) if v.startswith('_') and not v.startswith('__')]
        param = {}
        for v in protected:
            param[v.replace('_', '', 1)] = self.__getattribute__(v)
        return param

    def update_params(self, param):
        for k, v in param.items():
            if '_' + k in dir(self):
                self.__setattr__('_' + k, v)


class GrayingItem(MyItem):
    def __init__(self, parent=None):
        super(GrayingItem, self).__init__(' 灰度化 ', parent=parent)
        self._mode = BGR2GRAY_COLOR

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class FilterItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('平滑处理', parent=parent)
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
        super().__init__(' 形态学 ', parent=parent)
        self._ksize = 3
        self._op = ERODE_MORPH_OP
        self._kshape = RECT_MORPH_SHAPE

    def __call__(self, img):
        op = MORPH_OP[self._op]
        kshape = MORPH_SHAPE[self._kshape]
        kernal = cv2.getStructuringElement(kshape, (self._ksize, self._ksize))
        img = cv2.morphologyEx(img, self._op, kernal)
        return img


class GradItem(MyItem):

    def __init__(self, parent=None):
        super().__init__('图像梯度', parent=parent)
        self._kind = SOBEL_GRAD
        self._ksize = 3
        self._dx = 1
        self._dy = 0

    def __call__(self, img):
        if self._dx == 0 and self._dy == 0 and self._kind != LAPLACIAN_GRAD:
            self.setBackground(QColor(255, 0, 0))
            self.setText('图像梯度 （无效: dx与dy不同时为0）')
        else:
            self.setBackground(QColor(200, 200, 200))
            self.setText('图像梯度')
            if self._kind == SOBEL_GRAD:
                img = cv2.Sobel(img, -1, self._dx, self._dy, self._ksize)
            elif self._kind == SCHARR_GRAD:
                img = cv2.Scharr(img, -1, self._dx, self._dy)
            elif self._kind == LAPLACIAN_GRAD:
                img = cv2.Laplacian(img, -1)
        return img


class ThresholdItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('阈值处理', parent=parent)
        self._thresh = 127
        self._maxval = 255
        self._method = BINARY_THRESH_METHOD

    def __call__(self, img):
        method = THRESH_METHOD[self._method]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.threshold(img, self._thresh, self._thresh, method)[1]
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class EdgeItem(MyItem):
    def __init__(self, parent=None):
        super(EdgeItem, self).__init__('边缘检测', parent=parent)
        self._thresh1 = 20
        self._thresh2 = 100

    def __call__(self, img):
        img = cv2.Canny(img, threshold1=self._thresh1, threshold2=self._thresh2)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img


class ContourItem(MyItem):
    def __init__(self, parent=None):
        super(ContourItem, self).__init__('轮廓检测', parent=parent)
        self._mode = TREE_CONTOUR_MODE
        self._method = SIMPLE_CONTOUR_METHOD
        self._bbox = NORMAL_CONTOUR

    def __call__(self, img):
        mode = CONTOUR_MODE[self._mode]
        method = CONTOUR_METHOD[self._method]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cnts, _ = cv2.findContours(img, mode, method)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if self._bbox == RECT_CONTOUR:
            bboxs = [cv2.boundingRect(cnt) for cnt in cnts]
            print(bboxs)
            for x, y, w, h in bboxs:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
        elif self._bbox == MINRECT_CONTOUR:
            bboxs = [np.int0(cv2.boxPoints(cv2.minAreaRect(cnt))) for cnt in cnts]
            img = cv2.drawContours(img, bboxs, -1, (255, 0, 0), thickness=2)
        elif self._bbox == MINCIRCLE_CONTOUR:
            circles = [cv2.minEnclosingCircle(cnt) for cnt in cnts]
            print(circles)
            for (x, y), r in circles:
                img = cv2.circle(img, (int(x), int(y)), int(r), (255, 0, 0), thickness=2)
        elif self._bbox == NORMAL_CONTOUR:
            img = cv2.drawContours(img, cnts, -1, (255, 0, 0), thickness=2)

        return img


class EqualizeItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(' 均衡化 ', parent=parent)
        self._blue = True
        self._green = True
        self._red = True

    def __call__(self, img):
        b, g, r = cv2.split(img)
        if self._blue:
            b = cv2.equalizeHist(b)
        if self._green:
            g = cv2.equalizeHist(g)
        if self._red:
            r = cv2.equalizeHist(r)
        return cv2.merge((b, g, r))


class HoughLineItem(MyItem):
    def __init__(self, parent=None):
        super(HoughLineItem, self).__init__('直线检测', parent=parent)
        self._rho = 1
        self._theta = np.pi / 180
        self._thresh = 10
        self._min_length = 20
        self._max_gap = 5

    def __call__(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLinesP(img, self._rho, self._theta, self._thresh, minLineLength=self._min_length,
                                maxLineGap=self._max_gap)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if lines is None: return img
        for line in lines:
            for x1, y1, x2, y2 in line:
                img = cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
        return img


class LightItem(MyItem):
    def __init__(self, parent=None):
        super(LightItem, self).__init__('亮度调节', parent=parent)
        self._alpha = 1
        self._beta = 0

    def __call__(self, img):
        blank = np.zeros(img.shape, img.dtype)
        img = cv2.addWeighted(img, self._alpha, blank, 1 - self._alpha, self._beta)
        return img


class GammaItem(MyItem):
    def __init__(self, parent=None):
        super(GammaItem, self).__init__('伽马校正', parent=parent)
        self._gamma = 1

    def __call__(self, img):
        gamma_table = [np.power(x / 255.0, self._gamma) * 255.0 for x in range(256)]
        gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
        return cv2.LUT(img, gamma_table)
