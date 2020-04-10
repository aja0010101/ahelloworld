#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QAbstractItemView, QFileDialog, QTableWidgetItem
import pandas as pd
import numpy as np

class SysTablewidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(6)
        self.setRowCount(6)
        self.verticalHeader().setVisible(False)
#        self.setEditTriggers(QAbstractItemView_EditTrigger=None)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

class GuiMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle('网页填写小助手V1.0  福州海关技术中心.机电检测部')
        self.resize(500, 300)
        self.vertical_horizontal_box_layout()

    def vertical_horizontal_box_layout(self):
        self.MyTablewidget = SysTablewidget()
        button_open = QPushButton('打开文件')
        button_open.setFixedSize(100, 28)
        button_open.clicked.connect(self.openfile)
        button_ok = QPushButton('填写网页')
        button_ok.clicked.connect(self.write_web)
        button_ok.setFixedSize(100, 28)
        button_exit = QPushButton('退 出')
        button_exit.setFixedSize(100, 28)
        button_exit.clicked.connect(self.close)
        hbox_1 = QHBoxLayout()
        hbox_2 = QHBoxLayout()
        hbox_1.addWidget(self.MyTablewidget)
        hbox_2.addWidget(button_open)
        hbox_2.addWidget(button_ok)
        hbox_2.addWidget(button_exit)
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_1)
        vbox.addLayout(hbox_2)
        layout_widget = QWidget()
        layout_widget.setLayout(vbox)
        self.setCentralWidget(layout_widget)

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        if openfile_name[0]:
            input_table = pd.read_excel(openfile_name[0])
            input_table_rows = len(input_table.index)
            input_table_columns = len(input_table.columns)
            input_table_header = input_table.columns.values.tolist()
            self.MyTablewidget.setRowCount(input_table_rows)
            self.MyTablewidget.setColumnCount(input_table_columns)
            self.MyTablewidget.setHorizontalHeaderLabels(input_table_header)
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_columns):
                    input_table_items_list = input_table_rows_values_list[j]
                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    self.MyTablewidget.setItem(i, j, newItem)
                    self.MyTablewidget.setCurrentItem(None)

    def write_web(self):
#        row_index = self.MyTablewidget.currentIndex().row()
#        print('you have clicked row number:', row_index)
#        current_row_name = self.MyTablewidget.item(row_index).text()
#        print(current_row_name)
#        d_content = self.MyTablewidget.currentRow()
        if self.MyTablewidget.selectedItems():
#            items = self.MyTablewidget.selectedItems()
#            row_number = items[0].row()
            row_number = self.MyTablewidget.currentRow()
            print(row_number)
#            print(items[0].text())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GuiMain()
    gui.show()
    sys.exit(app.exec_())