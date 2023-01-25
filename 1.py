# Задача: Создать информационную систему позволяющую работать с сотрудниками некой компании \ студентами вуза \ учениками школы

from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QDialog, QTableView, QHeaderView, QGridLayout,
                             QLineEdit, QMessageBox, QLabel, QMenu, QMenuBar, QAction, QComboBox)
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtCore import Qt

import sqlite3, os

class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.setMinimumSize(700, 500)
        self.setWindowTitle('ООО "Рога и Копыта')

        maket = QGridLayout()
        maket.addWidget(self.create_menu(), 0, 0, 1, 1)
        maket.addWidget(self.table(), 1, 0, 1, 1,)
        self.setLayout(maket)

    def create_menu(self):
        menu_bar = QMenuBar(self)
        self.file_menu = QMenu("Меню", self)
        menu_bar.addMenu(self.file_menu)
        self.close = QAction("Закрыть")
        self.close.triggered.connect(self.close_app)
        self.file_menu.addAction(self.close)

        self.edit_menu = menu_bar.addMenu("Правка")
        self.add_user = QAction("Добавить сотрудника")
        self.add_user.triggered.connect(self.win_add_new_contact)
        self.transfer_user = QAction("Перевод сотрудника")
        self.transfer_user.triggered.connect(self.win_transf_contact)
        self.del_user = QAction("Удалить сотрудника")
        self.del_user.triggered.connect(self.win_del_contact)
        self.edit_menu.addAction(self.add_user)
        self.edit_menu.addAction(self.transfer_user)
        self.edit_menu.addAction(self.del_user)
        
        self.view_menu = menu_bar.addMenu("Просмотр")
        self.dep = self.view_menu.addMenu("Отделы")
        self.sale_dep = QAction("Отдел продаж")
        self.sale_dep.triggered.connect(self.func_view_user)
        self.accounting = QAction("Бухгалтерия")
        self.accounting.triggered.connect(self.func_view_user)
        self.hr_dep = QAction("Отдел кадров")
        self.hr_dep.triggered.connect(self.func_view_user)
        self.guide = QAction("Руководство")
        self.guide.triggered.connect(self.func_view_user)
        self.dep.addAction(self.sale_dep)
        self.dep.addAction(self.hr_dep)
        self.dep.addAction(self.accounting)
        self.dep.addAction(self.guide)
    
        self. help_menu = menu_bar.addMenu("Помощь")
        return menu_bar

    def model_table(self, name):
        self.model = QSqlTableModel()
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setTable(name)
        self.model.select()
        self.model.setHeaderData(1, Qt.Horizontal, "Имя")
        self.model.setHeaderData(2, Qt.Horizontal, "Фамилия")
        self.model.setHeaderData(3, Qt.Horizontal, "Номер")
        self.model.setHeaderData(4, Qt.Horizontal, "Должность")

        return self.model

    def table(self):
        self.tableView = QTableView(self)
        self.tableView.hide()
        self.tableView.setMinimumSize(300, 200)
        self.tableView.installEventFilter(self)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return self.tableView

    def win_add_new_contact(self):
        self.add_new_user = QDialog(self)
        self.add_new_user.setWindowTitle("Добавить в...")
        self.add_new_user.setMinimumSize(300, 250)
        self.le_dep_add_user = QComboBox()
        self.le_dep_add_user.setMinimumSize(100, 40)
        self.le_dep_add_user.addItems(['Отдел продаж', 'Отдел кадров', 'Бухгалтерия', 'Руководство'])
        self.le_name_add_user = QLineEdit()
        self.le_name_add_user.setMinimumSize(100, 40)
        self.le_name_add_user.setPlaceholderText("Укажите имя")
        self.le_surname_add_user = QLineEdit()
        self.le_surname_add_user.setMinimumSize(100, 40)
        self.le_surname_add_user.setPlaceholderText("Укажите фамилию")
        self.le_call_num_add_user = QLineEdit()
        self.le_call_num_add_user.setMinimumSize(100, 40)
        self.le_call_num_add_user.setPlaceholderText("Укажите номер телефона")
        self.le_other_add_user = QLineEdit()
        self.le_other_add_user.setMinimumSize(100, 40)
        self.le_other_add_user.setPlaceholderText("Примечание")

        b_add = QPushButton("Добавить")
        b_add.clicked.connect(self.func_add_new_user)
        b_cancel = QPushButton("Отмена")
        b_cancel.clicked.connect(self.func_close_add_new_user)

        maket = QGridLayout()
        maket.addWidget(self.le_dep_add_user, 0, 0, 1, 2)
        maket.addWidget(self.le_name_add_user, 1, 0, 1, 2)
        maket.addWidget(self.le_surname_add_user, 2, 0, 1, 2)
        maket.addWidget(self.le_call_num_add_user, 3, 0, 1, 2)
        maket.addWidget(self.le_other_add_user, 4, 0, 1, 2)
        maket.addWidget(b_add, 5, 0)
        maket.addWidget(b_cancel, 5, 1)

        self.add_new_user.setLayout(maket)
        self.add_new_user.show()

    def win_transf_contact(self):
        self.w_transf_user = QDialog(self)
        self.w_transf_user.setWindowTitle("Перместить из...")
        self.w_transf_user.setMinimumSize(200, 100)
        self.le_dep_transf_user = QComboBox()
        self.le_dep_transf_user.setMinimumSize(100, 40)
        self.le_dep_transf_user.addItems(['Отдел продаж', 'Отдел кадров', 'Бухгалтерия', 'Руководство'])
        self.le_name_transf_user = QLineEdit()
        self.le_name_transf_user.setMinimumSize(100, 40)
        self.le_name_transf_user.setPlaceholderText("Укажите имя")
        self.le_surname_transf_user = QLineEdit()
        self.le_surname_transf_user.setMinimumSize(100, 40)
        self.le_surname_transf_user.setPlaceholderText("Укажите фамилию")
        self.l_transf_target = QLabel("Выберите, куда переместить сотрудника:")
        self.le_dep_transf_target = QComboBox()
        self.le_dep_transf_target.setMinimumSize(100, 40)
        self.le_dep_transf_target.addItems(['Отдел продаж', 'Отдел кадров', 'Бухгалтерия', 'Руководство'])

        b_transf = QPushButton("Переместить")
        b_transf.clicked.connect(self.func_transf_user)
        b_cancel = QPushButton("Отмена")
        b_cancel.clicked.connect(self.func_close_transf_contact)

        maket = QGridLayout()
        maket.addWidget(self.le_dep_transf_user, 0, 0, 1, 2)
        maket.addWidget(self.le_name_transf_user, 1, 0, 1, 2)
        maket.addWidget(self.le_surname_transf_user, 2, 0, 1, 2)
        maket.addWidget(self.l_transf_target, 3, 0, 1, 2)
        maket.addWidget(self.le_dep_transf_target, 4, 0, 1, 2)
        maket.addWidget(b_transf, 5, 0)
        maket.addWidget(b_cancel, 5, 1)

        self.w_transf_user.setLayout(maket)
        self.w_transf_user.show()
    def win_del_contact(self):
        self.w_del_user = QDialog(self)
        self.w_del_user.setWindowTitle("Удалить из...")
        self.w_del_user.setMinimumSize(200, 100)
        self.le_dep_del_user = QComboBox()
        self.le_dep_del_user.setMinimumSize(100, 40)
        self.le_dep_del_user.addItems(['Отдел продаж', 'Отдел кадров', 'Бухгалтерия', 'Руководство'])
        self.le_name_del_user = QLineEdit()
        self.le_name_del_user.setMinimumSize(100, 40)
        self.le_name_del_user.setPlaceholderText("Укажите имя")
        self.le_surname_del_user = QLineEdit()
        self.le_surname_del_user.setMinimumSize(100, 40)
        self.le_surname_del_user.setPlaceholderText("Укажите фамилию")

        b_del = QPushButton("Удалить")
        b_del.clicked.connect(self.func_del_user)
        b_cancel = QPushButton("Отмена")
        b_cancel.clicked.connect(self.func_close_del_user)

        maket = QGridLayout()
        maket.addWidget(self.le_dep_del_user, 0, 0, 1, 2)
        maket.addWidget(self.le_name_del_user, 1, 0, 1, 2)
        maket.addWidget(self.le_surname_del_user, 2, 0, 1, 2)
        maket.addWidget(b_del, 5, 0)
        maket.addWidget(b_cancel, 5, 1)

        self.w_del_user.setLayout(maket)
        self.w_del_user.show()
    #фронт ↑↑↑

    #бэк ↓↓↓
    def func_message_attention(self, title, message, button):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setStandardButtons(button)
        msgBox.exec_()
    def func_view_user(self):
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('config/Departments.db')
        self.db.open()
        if self.sender() is self.sale_dep:
            self.tableView.show()
            self.tableView.setModel(self.model_table("Sales_dep"))
        if self.sender() is self.hr_dep:
            self.tableView.show()
            self.tableView.setModel(self.model_table("HR_dep"))
        if self.sender() is self.accounting:
            self.tableView.show()
            self.tableView.setModel(self.model_table("Accounting"))
        if self.sender() is self.guide:
            self.tableView.show()
            self.tableView.setModel(self.model_table("Guide"))
        self.tableView.hideColumn(0)
        self.db.close()

    def func_add_new_user(self):
        self.base_line_edit = [self.le_name_add_user, self.le_surname_add_user, self.le_call_num_add_user]
        for line_edit in self.base_line_edit:
            if len(line_edit.text()) == 0:
                self.func_message_attention('Внимание!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы не заполнили поля</b></center></FONT>',
                                           QMessageBox.Ok)
                return
        else:
            if os.access('config/Departments.db', os.F_OK) == False:
                self.func_message_attention('Внимание!',
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">системная ошибка [0x000001]</b></center></FONT>'
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">свяжитесь с тех. поддержкой</b></center></FONT>',
                                           QMessageBox.Ok)
            else:
                if self.le_dep_add_user.currentText() == "Отдел кадров":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO HR_dep (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)
                    cur.close()
                    con.close()
                if self.le_dep_add_user.currentText() == "Отдел продаж":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO Sales_dep (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)

                    cur.close()
                    con.close()
                if self.le_dep_add_user.currentText() == "Бухгалтерия":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO Accounting (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)

                    cur.close()
                    con.close()
                if self.le_dep_add_user.currentText() == "Руководство":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO Guide (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)

                    cur.close()
                    con.close()

                self.add_new_user.close()
                self.func_model_updadter()

    def func_add_new_user(self):
        self.base_line_edit = [self.le_name_add_user, self.le_surname_add_user, self.le_call_num_add_user]
        for line_edit in self.base_line_edit:
            if len(line_edit.text()) == 0:
                self.func_message_attention('Внимание!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы не заполнили поля</b></center></FONT>',
                                           QMessageBox.Ok)
                return
        else:
            if os.access('config/Departments.db', os.F_OK) == False:
                self.func_message_attention('Внимание!',
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">системная ошибка [0x000001]</b></center></FONT>'
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">свяжитесь с тех. поддержкой</b></center></FONT>',
                                           QMessageBox.Ok)
            else:
                if self.le_dep_add_user.currentText() == "Отдел кадров":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(f"INSERT INTO HR_dep (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)
                    cur.close()
                    con.close()
                if self.le_dep_add_user.currentText() == "Отдел продаж":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO Sales_dep (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)

                    cur.close()
                    con.close()
                if self.le_dep_add_user.currentText() == "Бухгалтерия":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO Accounting (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)

                    cur.close()
                    con.close()
                if self.le_dep_add_user.currentText() == "Руководство":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO Guide (name, surname, number, other) VALUES ('{self.le_name_add_user.text().strip()}','{self.le_surname_add_user.text().strip()}','{self.le_call_num_add_user.text().strip()}','{self.le_other_add_user.text().strip()}')")
                    con.commit()
                    self.func_message_attention('Поздравляю!',
                                               '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Новый контакт добавлен!</b></center></FONT>',
                                               QMessageBox.Ok)

                    cur.close()
                    con.close()

                self.add_new_user.close()
                self.func_model_updadter()
    def func_transf_user(self):
        self.base_line_edit = [self.le_name_transf_user, self.le_surname_transf_user]
        for line_edit in self.base_line_edit:
            if len(line_edit.text()) == 0:
                self.func_message_attention('Внимание!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы не заполнили поля</b></center></FONT>',
                                           QMessageBox.Ok)
                return
        else:
            if os.access('config/Departments.db', os.F_OK) == False:
                self.func_message_attention('Внимание!',
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">системная ошибка [0x000001]</b></center></FONT>'
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">свяжитесь с тех. поддержкой</b></center></FONT>',
                                           QMessageBox.Ok)
            else:
                if self.le_dep_transf_target.currentText() == "Отдел кадров":
                    self.name_where = "HR_dep"
                if self.le_dep_transf_target.currentText() == "Отдел продаж":
                    self.name_where = "Sales_dep"
                if self.le_dep_transf_target.currentText() == "Бухгалтерия":
                    self.name_where = "Accounting"
                if self.le_dep_transf_target.currentText() == "Руководство":
                    self.name_where = "Guide"

                if self.le_dep_transf_user.currentText() == "Отдел кадров":
                    self.name_from = "HR_dep"
                if self.le_dep_transf_user.currentText() == "Отдел продаж":
                    self.name_from = "Sales_dep"
                if self.le_dep_transf_user.currentText() == "Бухгалтерия":
                    self.name_from = "Accounting"
                if self.le_dep_transf_user.currentText() == "Руководство":
                    self.name_from = "Guide"

                con = sqlite3.connect('config/Departments.db')
                cur = con.cursor()
                cur.execute(f"INSERT INTO {self.name_where} SELECT NULL, name, surname, number, other FROM {self.name_from} WHERE name=('{self.le_name_transf_user.text().strip()}') and surname=('{self.le_surname_transf_user.text().strip()}');")
                cur.execute(f"DELETE FROM {self.name_from} WHERE name=('{self.le_name_transf_user.text().strip()}') and surname=('{self.le_surname_transf_user.text().strip()}');")
                con.commit()
                self.func_message_attention('Поздравляю!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Сотрудник успешно переведен:</b></center></FONT>'
                                          f'<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">из {self.name_from} в {self.name_where}</b></center></FONT>',
                                           QMessageBox.Ok)
                cur.close()
                con.close()

                self.w_transf_user.close()
                self.func_model_updadter()

    def func_del_user(self):
        self.base_line_edit = [self.le_name_del_user, self.le_surname_del_user]
        for line_edit in self.base_line_edit:
            if len(line_edit.text()) == 0:
                self.func_message_attention('Внимание!',
                                           '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы не заполнили поля</b></center></FONT>',
                                           QMessageBox.Ok)
                return
        else:
            if os.access('config/Departments.db', os.F_OK) == False:
                self.func_message_attention('Внимание!',
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">системная ошибка [0x000001]</b></center></FONT>'
                                           '<center><b style=font-size:8pt><FONT FACE="Century Gothic">свяжитесь с тех. поддержкой</b></center></FONT>',
                                           QMessageBox.Ok)
            else:
                if self.le_dep_del_user.currentText() == "Отдел кадров":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    message = QMessageBox()
                    message.setWindowTitle('Внимание!')
                    message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы хотите удалить'
                                    f'<br> контакт: {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} ?</b></center></FONT>')
                    message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    but_yes = message.button(QMessageBox.Ok)
                    but_yes.setText("Да")
                    but_no = message.button(QMessageBox.Cancel)
                    but_no.setText("Нет")
                    close_message = message.exec_()
                    if close_message == QMessageBox.StandardButton.Ok:
                        cur.execute(f"DELETE FROM HR_dep WHERE name=('{self.le_name_del_user.text().strip()}') and surname=('{self.le_surname_del_user.text().strip()}')")
                        con.commit()
                        self.func_message_attention('Поздравляю!',
                                                   '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Удаление контакта:</b></center></FONT>'
                                                   f'<br> {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} успешно выполнено!</b></center></FONT>',
                                                   QMessageBox.Ok)
                    cur.close()
                    con.close()
                if self.le_dep_del_user.currentText() == "Отдел продаж":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    message = QMessageBox()
                    message.setWindowTitle('Внимание!')
                    message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы хотите удалить'
                                    f'<br> контакт: {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} ?</b></center></FONT>')
                    message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    but_yes = message.button(QMessageBox.Ok)
                    but_yes.setText("Да")
                    but_no = message.button(QMessageBox.Cancel)
                    but_no.setText("Нет")
                    close_message = message.exec_()
                    if close_message == QMessageBox.StandardButton.Ok:
                        cur.execute(
                            f"DELETE FROM Sales_dep WHERE name=('{self.le_name_del_user.text().strip()}') and surname=('{self.le_surname_del_user.text().strip()}')")
                        con.commit()
                        self.func_message_attention('Поздравляю!',
                                                   '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Удаление контакта:</b></center></FONT>'
                                                   f'<br> {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} успешно выполнено!</b></center></FONT>',
                                                   QMessageBox.Ok)
                    cur.close()
                    con.close()
                if self.le_dep_del_user.currentText() == "Руководство":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    message = QMessageBox()
                    message.setWindowTitle('Внимание!')
                    message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы хотите удалить'
                                    f'<br> контакт: {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} ?</b></center></FONT>')
                    message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    but_yes = message.button(QMessageBox.Ok)
                    but_yes.setText("Да")
                    but_no = message.button(QMessageBox.Cancel)
                    but_no.setText("Нет")
                    close_message = message.exec_()
                    if close_message == QMessageBox.StandardButton.Ok:
                        cur.execute(
                            f"DELETE FROM Guide WHERE name=('{self.le_name_del_user.text().strip()}') and surname=('{self.le_surname_del_user.text().strip()}')")
                        con.commit()
                        self.func_message_attention('Поздравляю!',
                                                   '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Удаление контакта:</b></center></FONT>'
                                                   f'<br> {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} успешно выполнено!</b></center></FONT>',
                                                   QMessageBox.Ok)
                    cur.close()
                    con.close()
                if self.le_dep_del_user.currentText() == "Бухгалтерия":
                    con = sqlite3.connect('config/Departments.db')
                    cur = con.cursor()
                    message = QMessageBox()
                    message.setWindowTitle('Внимание!')
                    message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы хотите удалить'
                                    f'<br> контакт: {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} ?</b></center></FONT>')
                    message.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                    but_yes = message.button(QMessageBox.Ok)
                    but_yes.setText("Да")
                    but_no = message.button(QMessageBox.Cancel)
                    but_no.setText("Нет")
                    close_message = message.exec_()
                    if close_message == QMessageBox.StandardButton.Ok:
                        cur.execute(f"DELETE FROM Accounting WHERE name=('{self.le_name_del_user.text().strip()}') and surname=('{self.le_surname_del_user.text().strip()}')")
                        con.commit()
                        self.func_message_attention('Поздравляю!',
                                                   '<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Удаление контакта:</b></center></FONT>'
                                                   f'<br> {self.le_name_del_user.text().strip()} {self.le_surname_del_user.text().strip()} успешно выполнено!</b></center></FONT>',
                                                   QMessageBox.Ok)
                    cur.close()
                    con.close()

                self.w_del_user.close()
                self.func_model_updadter()

    def func_close_add_new_user(self):
        self.add_new_user.close()

    def func_close_del_user(self):
        self.w_del_user.close()

    def func_close_transf_contact(self):
        self.w_transf_user.close()

    def func_model_updadter(self):
        self.db.open()
        self.model.select()
        self.db.close()

    def close_app(self):
        message = QMessageBox()
        message.setWindowTitle('Внимание!')
        message.setText('<center><br/><b style=font-size:8pt><FONT FACE="Century Gothic">Вы уверены, что хотите выйти?</b></center></FONT>')
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        but_yes = message.button(QMessageBox.Ok)
        but_yes.setText("Да")
        but_no = message.button(QMessageBox.Cancel)
        but_no.setText("Нет")
        close_message = message.exec_()
        if close_message == QMessageBox.StandardButton.Ok:
            Main.close(self)

if __name__ == ('__main__'):
    import sys
    App = QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(App.exec_())