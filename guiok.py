#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# by 福州海关技术中心.机电产品检测部 张
# mail: 2050169410@qq.com
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QAbstractItemView, QFileDialog, QTableWidgetItem
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import numpy as np

class SysTablewidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(0)
        self.setRowCount(0)
        self.verticalHeader().setVisible(False)
#        self.setEditTriggers(QAbstractItemView_EditTrigger=None)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

class GuiMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle('网页填写小助手V1.0  福州海关技术中心.机电产品检测部')
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
        button_set = QPushButton('设 置')
        button_set.setFixedSize(100, 28)
        button_exit = QPushButton('退 出')
        button_exit.setFixedSize(100, 28)
        button_exit.clicked.connect(self.close)
        hbox_1 = QHBoxLayout()
        hbox_2 = QHBoxLayout()
        hbox_1.addWidget(self.MyTablewidget)
        hbox_2.addWidget(button_open)
        hbox_2.addWidget(button_ok)
        hbox_2.addWidget(button_set)
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
            input_table = input_table.fillna('!empty!')
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
        if self.MyTablewidget.selectedItems():
            row_number = self.MyTablewidget.currentRow()
            self.my_dict = dict()
            for col_cnumber in range(self.MyTablewidget.columnCount()):
                h_headertext = self.MyTablewidget.horizontalHeaderItem(col_cnumber).text()
                h_tablerowtext = self.MyTablewidget.item(row_number, col_cnumber).text()
                self.my_dict[h_headertext] = h_tablerowtext
#               print(self.my_dict)
            try:
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
                self.mydriver = webdriver.Chrome(chrome_driver, options=chrome_options)
                windows = self.mydriver.window_handles
                self.mydriver.switch_to.window(windows[-1])
                to_frame = self.mydriver.find_element_by_xpath('//iframe[@scrolling="auto"]')
                self.mydriver.switch_to.frame(to_frame)
                scrollbar_id = self.mydriver.find_element_by_xpath('//div[contains(@class,\'lr-form-wrap lr-scroll-wrap\')]/div[@class="lr-scroll-box"]').get_attribute('id')
#               print(scrollbar_id)
                js = 'document.getElementById("' + scrollbar_id + '").style.top="0px"'
                self.mydriver.execute_script(js)
                time.sleep(0.3)
                list_items = self.mydriver.find_elements_by_xpath('//div[@class="col-xs-12 lr-form-item"]')
#               print(len(list_items))
                for tin_item in list_items:
                    target_title = tin_item.find_element_by_xpath('div[@class="lr-form-item-title"]')
                    self.mydriver.execute_script("arguments[0].scrollIntoView(false);", target_title)
                    time.sleep(0.2)
#                   print(target_title.text, 'next')
                    if target_title.text in self.my_dict and self.my_dict[target_title.text] != '!empty!':
#                       print('有在，准备写入...')
                        tin_item.find_element_by_xpath('input[@id]').clear()
                        tin_item.find_element_by_xpath('input[@id]').send_keys(self.my_dict[target_title.text])
                    else:
                        pass
                self.mydriver.quit()
            except Exception:
                self.mydriver.quit()
                print('打开网页错误!请重来。')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GuiMain()
    gui.show()
    sys.exit(app.exec_())