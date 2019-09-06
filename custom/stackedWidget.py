from custom.tableWidget import *


class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.page = GrayingTableWidget(parent=parent)
        self.addWidget(self.page)
        self.page_2 = FilterTabledWidget(parent=parent)
        self.addWidget(self.page_2)
        self.page_3 = MorphTabledWidget(parent=parent)
        self.addWidget(self.page_3)
        self.page_4 = GradTabledWidget(parent=parent)
        self.addWidget(self.page_4)
        self.page_5 = ThresholdTableWidget(parent=parent)
        self.addWidget(self.page_5)
        self.page_6 = EdgeTableWidget(parent=parent)
        self.addWidget(self.page_6)
        self.page_7 = ContourTableWidget(parent=parent)
        self.addWidget(self.page_7)
        self.setMinimumWidth(200)
