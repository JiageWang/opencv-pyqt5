
from PyQt5.QtWidgets import *


class TableWidget(QTableWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent=parent)
        self.mainwindow = parent
        # self.setupUi(self)
        self.setShowGrid(True)  # 显示网格
        # self.tableWidget.setAlternatingRowColors(True)  # 隔行显示颜色
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.tableWidget.setColumnCount(2)
        # self.tableWidget.setRowCount(2)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().sectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)

    def update_item(self):
        param = self.get_params()
        self.mainwindow.useListWidget.currentItem().update_params(param)
        self.mainwindow.update_label()

    def update_params(self, param=None):
        pass

    def get_params(self):
        return None


class GrayingTableWidget(TableWidget):
    def __init__(self, parent=None):
        super(GrayingTableWidget, self).__init__(parent=parent)


class FilterTabledWidget(TableWidget):
    def __init__(self, param={'kind': 0, 'ksize': 3}, parent=None):
        super(FilterTabledWidget, self).__init__(parent=parent)

        self.kind_comBox = QComboBox()
        self.kind_comBox.addItems(['均值滤波', '高斯滤波', '中值滤波'])

        self.ksize_spinBox = QSpinBox()
        self.ksize_spinBox.setMinimum(1)
        self.ksize_spinBox.setSingleStep(2)

        self.update_params(param)
        self.ksize_spinBox.valueChanged.connect(self.update_item)
        self.kind_comBox.currentIndexChanged.connect(self.update_item)

        self.setColumnCount(2)
        self.setRowCount(2)
        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.kind_comBox)
        self.setItem(1, 0, QTableWidgetItem('核大小'))
        self.setCellWidget(1, 1, self.ksize_spinBox)
        # self.show()

    def update_params(self, param=None):
        self.kind_comBox.setCurrentIndex(param['kind'])
        self.ksize_spinBox.setValue(param['ksize'])

    def get_params(self):
        return {
            'kind': self.kind_comBox.currentIndex(),
            'ksize': self.ksize_spinBox.value()
        }


class MorphTabledWidget(TableWidget):
    def __init__(self, param={'kind': 0, 'ksize': 3, 'kshape': 0}, parent=None):
        super(MorphTabledWidget, self).__init__(parent=parent)

        self.kind_comBox = QComboBox()
        self.kind_comBox.addItems(['腐蚀操作', '膨胀操作', '开操作', '闭操作'])

        self.ksize_spinBox = QSpinBox()
        self.ksize_spinBox.setMinimum(1)
        self.ksize_spinBox.setSingleStep(2)

        self.kshape_comBox = QComboBox()
        self.kshape_comBox.addItems(['方形', '十字形', '椭圆形'])

        self.update_params(param)
        self.kind_comBox.currentIndexChanged.connect(self.update_item)
        self.ksize_spinBox.valueChanged.connect(self.update_item)
        self.kshape_comBox.currentIndexChanged.connect(self.update_item)

        self.setColumnCount(2)
        self.setRowCount(3)
        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.kind_comBox)
        self.setItem(1, 0, QTableWidgetItem('核大小'))
        self.setCellWidget(1, 1, self.ksize_spinBox)
        self.setItem(2, 0, QTableWidgetItem('核形状'))
        self.setCellWidget(2, 1, self.kshape_comBox)
        # self.show()

    def update_params(self, param=None):
        self.kind_comBox.setCurrentIndex(param['kind'])
        self.ksize_spinBox.setValue(param['ksize'])
        self.kshape_comBox.setCurrentIndex(param['kshape'])

    def get_params(self):
        return {
            'kind': self.kind_comBox.currentIndex(),
            'ksize': self.ksize_spinBox.value(),
            'kshape': self.kshape_comBox.currentIndex()
        }


class GradTabledWidget(TableWidget):
    def __init__(self, param={'kind': 0, 'ksize': 3, 'dx': 1, 'dy': 0}, parent=None):
        super(GradTabledWidget, self).__init__(parent=parent)

        self.kind_comBox = QComboBox()
        self.kind_comBox.addItems(['Sobel算子', 'Scharr算子', 'Laplacian算子'])

        self.ksize_spinBox = QSpinBox()
        self.ksize_spinBox.setMinimum(1)
        self.ksize_spinBox.setSingleStep(2)

        self.dx_spinBox = QSpinBox()
        self.dx_spinBox.setMaximum(1)
        self.dx_spinBox.setMinimum(0)
        self.dx_spinBox.setSingleStep(1)

        self.dy_spinBox = QSpinBox()
        self.dy_spinBox.setMaximum(1)
        self.dy_spinBox.setMinimum(0)
        self.dy_spinBox.setSingleStep(1)

        self.update_params(param)
        self.kind_comBox.currentIndexChanged.connect(self.update_item)
        self.ksize_spinBox.valueChanged.connect(self.update_item)
        self.dx_spinBox.valueChanged.connect(self.update_item)
        self.dy_spinBox.valueChanged.connect(self.update_item)

        self.setColumnCount(2)
        self.setRowCount(4)

        self.setItem(0, 0, QTableWidgetItem('类型'))
        self.setCellWidget(0, 1, self.kind_comBox)
        self.setItem(1, 0, QTableWidgetItem('核大小'))
        self.setCellWidget(1, 1, self.ksize_spinBox)
        self.setItem(2, 0, QTableWidgetItem('x方向'))
        self.setCellWidget(2, 1, self.dx_spinBox)
        self.setItem(3, 0, QTableWidgetItem('y方向'))
        self.setCellWidget(3, 1, self.dy_spinBox)
        # self.show()

    def update_params(self, param=None):
        self.kind_comBox.setCurrentIndex(param['kind'])
        self.ksize_spinBox.setValue(param['ksize'])
        self.dx_spinBox.setValue(param['dx'])
        self.dy_spinBox.setValue(param['dy'])

    def get_params(self):
        return {
            'kind': self.kind_comBox.currentIndex(),
            'ksize': self.ksize_spinBox.value(),
            'dx': self.dx_spinBox.value(),
            'dy': self.dy_spinBox.value()
        }
