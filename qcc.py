#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/7 13:50
# @Author  : Barrett
# @Email   : 1198878568@qq.com
# @FileName: qcc.py
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.uic import *
from PyQt5.QtGui import QIcon, QPixmap
import os
import keyboard
import pyperclip
import json
from threading import Thread
import time
from tool import *


class MySignals(QObject):
    # 主线程提示信号
    info = pyqtSignal(str, str, int)
    text_print = pyqtSignal(str)


global_ms = MySignals()


class check:
    def __init__(self):
        self.ui = loadUi("./qcc.ui")
        self.ui.resize(1500, 1000)
        self.ui.setWindowTitle("     爬虫 for 企查查")
        self.setting = None
        self.company_list = None
        self.input_setting()
        self.headers = {'User-Agent': self.setting["agent"],
                        'cookie': self.setting["cookie"]}
        self.df_result = None

        # 更新配置信息
        self.ui.button_renew_user.clicked.connect(self.renew_user)
        self.ui.button_renew_setting.clicked.connect(self.renew_setting)

        # 链接其他
        self.ui.button_input_com.clicked.connect(self.input_coms)
        self.ui.button_one_search.clicked.connect(self.one_search_thread)  # 链接查询子线程
        self.ui.button_more_search.clicked.connect(self.more_search_thread)

        self.ui.button_output_csv.clicked.connect(self.output_csv)  # 导出数据
        self.ui.button_output_excel.clicked.connect(self.output_excel)

        # 自定义信号与槽的链接
        global_ms.info.connect(self.info)
        global_ms.text_print.connect(self.printToGui)

    def input_setting(self):
        """
        :return: 导入存储了上次使用的json格式数据
        """
        if not os.path.exists('./setting.json'):
            dic = {"account": "", "password": "",
                   "agent": "", "cookie": ""}
            json.dump(dic, open('./setting.json', 'w'), ensure_ascii=False, indent=4)
        data = json.load(open('./setting.json', 'r'))
        self.setting = data  # 将解析的配置 json 文件（dic）赋值给 self.setting
        self.ui.line_account.setText(self.setting["account"])  # 导入 user
        self.ui.line_pw.setText(self.setting["password"])
        self.ui.label_account.setText("账号：" + self.setting["account"])  # 导入 user 显示
        self.ui.label_pw.setText("密码：" + self.setting["password"])
        # 显示导入的代理与cookie
        # self.ui.plain_agent.setPlainText(self.setting["agent"])
        # self.ui.plain_cookie.setPlainText(self.setting["cookie"])
        self.ui.browser.setText("【系统代理】:\n" + "=" * 10 + "\n" + self.setting["agent"] + "\n\n\n【cookie】:\n" +
                                "=" * 10 + "\n" + self.setting["cookie"])

    def renew_user(self):
        # 更新 self.setting
        self.setting["account"] = self.ui.line_account.text()
        self.setting["password"] = self.ui.line_pw.text()
        # 将更新的内容保存至 json 配置文件
        json.dump(self.setting, open("./setting.json", "w"), ensure_ascii=False, indent=4)

        self.ui.label_account.setText("账号：" + self.setting["account"])  # 更新 user 显示
        self.ui.label_pw.setText("密码：" + self.setting["password"])
        QMessageBox.information(self.ui, "提示", "更新账号密码完成！")

    def renew_setting(self):
        self.setting["agent"] = self.ui.plain_agent.toPlainText()
        self.setting["cookie"] = self.ui.plain_cookie.toPlainText()
        json.dump(self.setting, open("./setting.json", "w"), ensure_ascii=False, indent=4)
        self.ui.browser.setText("【系统代理】:\n" + "=" * 10 + "\n" + self.setting["agent"] + "\n\n\n【cookie】:\n" +
                                "=" * 10 + "\n" + self.setting["cookie"])
        self.headers = {'User-Agent': self.setting["agent"],
                        'cookie': self.setting["cookie"]}
        QMessageBox.information(self.ui, "提示", "更新代理和cookie完成！")

    def input_coms(self):
        filepath = QFileDialog.getOpenFileName(self.ui, "请选择查询公司模板(.txt)")
        judge = filepath[0][-4:]
        if judge != ".txt":
            QMessageBox.critical(self.ui, "错误:", "请导入.txt格式的文件！")
            return
        print(filepath[0])
        with open(filepath[0], encoding="utf-8") as f:
            data = f.readlines()
        coms = [s[0:-1] for s in data]
        self.company_list = coms
        s = "当前查询公司为:\n" + "=" * 10 + "\n\n"
        for i in range(len(self.company_list)):
            s += str(i + 1) + "、" + self.company_list[i] + "\n"
        self.ui.browser_com.setText(s)
        QMessageBox.information(self.ui, "提示:", "导入查询公司模板成功！")

    def more_search_thread(self):
        thread_more = Thread(target=self.more_search
                             )
        thread_more.setDaemon(True)
        thread_more.start()

    def more_search(self):
        try:
            df_more = pd.DataFrame()
            if self.company_list is not None:
                global_ms.info.emit("提示", "即将查询左侧文本框中的公司！", 2)
                for com in self.company_list:
                    global_ms.text_print.emit(f"\n正在查询【{com}】，请稍后...")
                    ms = get_company_message(com, headers=self.headers)
                    df_sub = message_to_df(ms[0])
                    li = df_to_textli(df_sub)
                    for s in li:
                        global_ms.text_print.emit(s)
                    df_more = pd.concat([df_more, df_sub], axis=0, ignore_index=True)
                self.df_result = df_more
                global_ms.text_print.emit("\n\n所有公司查询完毕！请到数据页导出数据！")
            else:
                global_ms.info.emit("错误", "请先导入查询公司名单", 0)
        except:
            global_ms.info.emit("错误", "查询失败！", 0)

    def one_search_thread(self):
        thread = Thread(target=self.one_search
                        )
        thread.setDaemon(True)
        thread.start()

    def one_search(self):
        try:
            com = self.ui.line_com.text()
            if len(com) < 4:
                global_ms.info.emit("错误", "输入的公司名称过短，请检查后重新输入！", 0)
                return
            global_ms.info.emit("提示", "即将查询的公司为: " + com, 2)
            global_ms.text_print.emit(f"正在查询【{com}】！请稍后...")

            ms = get_company_message(com, headers=self.headers)
            print(ms[0])
            self.df_result = message_to_df(ms[0])
            global_ms.text_print.emit(com)
            li = df_to_textli(self.df_result)
            for s in li:
                global_ms.text_print.emit(s)
            global_ms.text_print.emit(f"\n\n查询【{com}】成功！请到数据页导出数据！\n")
        except:
            global_ms.info.emit("错误", "查询失败！", 0)

    # 导出数据
    def output_csv(self):
        if self.df_result is not None:
            filepath = QFileDialog.getSaveFileName()
            print(filepath)
            filepath = filepath[0] + ".csv"
            print(filepath)
            self.df_result.to_csv(filepath, index=False, encoding="utf-8_sig")
            QMessageBox.information(self.ui, "提示", "导出成功！")
        else:
            QMessageBox.critical(self.ui, "错误", "请先去查询页面生成数据再来！")

    def output_excel(self):
        if self.df_result is not None:
            filepath = QFileDialog.getSaveFileName()
            filepath = filepath[0] + ".xlsx"
            self.df_result.to_excel(filepath, index=False)
            QMessageBox.information(self.ui, "提示", "导出成功！")
        else:
            QMessageBox.critical(self.ui, "错误", "请先去查询页面生成数据再来！")

    # 自定义信号函数
    def info(self, str1, str2, info_type):  # 用 0, 1, 2 分别表示错误，警告，提示
        if info_type == 0:
            QMessageBox.critical(self.ui, str1, str2)
        elif info_type == 2:
            QMessageBox.information(self.ui, str1, str2)
        else:
            return

    def printToGui(self, text):
        self.ui.textBrowser.append(str(text))
        self.ui.textBrowser.ensureCursorVisible()


app = QApplication([])
app.setWindowIcon(QIcon("./rifn.png"))
check = check()
check.ui.show()
app.exec()
