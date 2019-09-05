from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from flags import *

from .listWidgetItems import FilterItem, MorphItem, GradItem, GrayingItem, MyItem


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent.parent()
        self.setDragEnabled(True)


class UsedListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setFlow(QListView.TopToBottom)  # 设置列表方向
        self.setDragDropMode(QListView.InternalMove)  # 设置拖放模式, 内部拖放
        self.setMovement(QListView.Snap)
        self.itemClicked.connect(self.show_stacked_widget)

    def contextMenuEvent(self, e):
        # 右键菜单事件
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return  # 判断是否是空白区域
        menu = QMenu()
        delete_action = QAction('删除', self)
        delete_action.triggered.connect(lambda: self.delete_item(item))  # 传递额外值
        menu.addAction(delete_action)
        menu.exec(QCursor.pos())

    def delete_item(self, item):
        self.takeItem(self.row(item))
        self.mainwindow.update_label()  # 更新frame
        self.mainwindow.stackedWidget.close()

    def show_stacked_widget(self):
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return
        param = item.get_params()
        if isinstance(item, MorphItem):
            self.mainwindow.stackedWidget.setCurrentIndex(MORPH_STACKED_WIDGET)
        elif isinstance(item, GradItem):
            self.mainwindow.stackedWidget.setCurrentIndex(GRAD_STACKED_WIDGET)
        elif isinstance(item, FilterItem):
            self.mainwindow.stackedWidget.setCurrentIndex(FILTER_STACKED_WIDGET)
        elif isinstance(item, GrayingItem):
            self.mainwindow.stackedWidget.setCurrentIndex(GRAYING_STACKED_WIDGET)
        self.mainwindow.stackedWidget.currentWidget().update_params(param)
        self.mainwindow.stackedWidget.show()


class FuncListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent.parent()
        self.setFixedHeight(64)
        self.setFlow(QListView.LeftToRight)  # 设置列表方向
        self.setViewMode(QListView.IconMode)  # 设置列表模式
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关掉滑动条
        self.setAcceptDrops(False)
        for itemType in [GrayingItem, FilterItem, MorphItem, GradItem]:
            self.addItem(itemType())
        self.itemClicked.connect(self.add_used_function)

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setCurrentRow(-1)  # 取消选中状态

    def add_used_function(self):
        func_item = self.currentItem()
        if isinstance(func_item, MorphItem):
            use_item = MorphItem()
        elif isinstance(func_item, FilterItem):
            use_item = FilterItem()
        elif isinstance(func_item, GradItem):
            use_item = GradItem()
        elif isinstance(func_item, GrayingItem):
            use_item = GrayingItem()
        self.mainwindow.useListWidget.addItem(use_item)
        self.mainwindow.update_label()
