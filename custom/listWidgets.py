from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from config import items


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent
        self.setDragEnabled(True)
        # 选中不显示虚线
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)


class UsedListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setFlow(QListView.TopToBottom)  # 设置列表方向
        self.setDefaultDropAction(Qt.MoveAction)  # 设置拖放为移动而不是复制一个
        self.setDragDropMode(QAbstractItemView.InternalMove)  # 设置拖放模式, 内部拖放
        self.itemClicked.connect(self.show_attr)
        self.setMinimumWidth(200)

        self.move_item = None

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
        # 删除操作
        self.takeItem(self.row(item))
        self.mainwindow.update_image()  # 更新frame
        self.mainwindow.dock_attr.close()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.mainwindow.update_image()

    def show_attr(self):
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return
        param = item.get_params()  # 获取当前item的属性
        if type(item) in items:
            index = items.index(type(item))  # 获取item对应的table索引
            self.mainwindow.stackedWidget.setCurrentIndex(index)
            self.mainwindow.stackedWidget.currentWidget().update_params(param)  # 更新对应的table
            self.mainwindow.dock_attr.show()


class FuncListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(64)
        self.setFlow(QListView.LeftToRight)  # 设置列表方向
        self.setViewMode(QListView.IconMode)  # 设置列表模式
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关掉滑动条
        self.setAcceptDrops(False)
        for itemType in items:
            self.addItem(itemType())
        self.itemClicked.connect(self.add_used_function)

    def add_used_function(self):
        func_item = self.currentItem()
        if type(func_item) in items:
            use_item = type(func_item)()
            self.mainwindow.useListWidget.addItem(use_item)
            self.mainwindow.update_image()

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setCurrentRow(-1)  # 取消选中状态
