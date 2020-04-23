# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 19:33:32 2020

@authors: Sam, Marylyn, Max, Frank
"""
#!/usr/bin/env python3

import pymysql, sip, datetime, sys, hashlib
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QRadioButton,
    QDialog,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QLabel,
    qApp,
    QAction,
    QSplitter,
    QListView,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QTextEdit,
    QCheckBox
)

from PyQt5.QtCore import Qt

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.setModal(True) #prevents other windows from getting any input
        self.setWindowTitle("Login")
        self.username = QLineEdit()
        self.password = QLineEdit()

        form_group_box = QGroupBox("GT Food Truck")
        layout = QFormLayout()
        layout.addRow(QLabel("Username"), self.username)
        layout.addRow(QLabel("Password"), self.password)
        form_group_box.setLayout(layout)

        buttonlogin = QPushButton("Login", self) #can make icons for the buttons - QIcon
        buttonregister = QPushButton("Register", self)

        buttonlogin.clicked.connect(self.buttonloginclick)
        buttonregister.clicked.connect(self.buttonregisterclick)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(buttonlogin)
        hbox_layout.addWidget(buttonregister)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addLayout(hbox_layout)
        self.setLayout(vbox_layout)
        self.username.setFocus()

    def buttonloginclick(self):
        cursor = connection.cursor()
        cursor.execute("call login(\"" + str(self.username.text()) + "\",\"" + str(self.password.text()) + "\");")
        cursor.execute("SELECT COUNT(*) FROM login_result")
        data = cursor.fetchall()
        cursor.execute("call login(\"" + str(self.username.text()) + "\",\"" + str(self.password.text()) + "\");")
        cursor.execute("SELECT * FROM login_result")
        data2 = cursor.fetchall()

        if (data[0]['COUNT(*)'] == 1):
            logintype = data2[0]['userType']
            if logintype == 'Customer':
                home = HomeScreenCustomer(self.username.text(),logintype)
                self.close()
                home.exec()
            elif logintype == 'Staff':
                home = HomeScreenStaff(self.username.text(),logintype)
                self.close()
                home.exec ()
            elif logintype == 'Admin':
                home = HomeScreenAdmin(self.username.text(),logintype)
                self.close()
                home.exec()
            elif logintype == 'Manager':
                home = HomeScreenManager(self.username.text(),logintype)
                self.close()
                home.exec()
            elif logintype == 'Admin-Customer':
                home = HomeScreenCustomerAdmin(self.username.text(),logintype)
                self.close()
                home.exec()
            elif logintype == 'Staff-Customer':
                home = HomeScreenCustomer(self.username.text(),logintype)
                self.close()
                home.exec()
            elif logintype ==  'Manager-Customer':
                home = HomeScreenCustomerManager(self.username.text(),logintype)
                self.close()
                home.exec()

    def findrole(username, password):
        cursor = connection.cursor()

    def buttonregisterclick(self):
        self.close()
        reg = Register()
        reg.exec ()

class HomeScreenCustomer(QDialog):
    def __init__(self, username, loginrole):
        super(HomeScreenCustomer, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Customer Home")
        self.l1 = QLabel()
        self.l1.setText("Home")

        #checks if customer has a location available
        cursor = connection.cursor()
        cursor.execute('''select stationName from customer where username = "''' + self.username + '''";''')
        self.station = cursor.fetchall()[0]["stationName"]

        self.explore = QPushButton("Explore")
        #Screen 16
        self.explore.setEnabled(True)
        self.explore.clicked.connect(self.screen16)

        self.history = QPushButton("View Order History")
        #screen 19
        self.history.setEnabled(True)
        self.history.clicked.connect(self.screen19)

        self.currentinfo = QPushButton("View Current Information")
        self.currentinfo.setEnabled(True)
        self.currentinfo.clicked.connect(self.screen17)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.explore)
        vbox.addWidget(self.history)
        vbox.addWidget(self.currentinfo)
        self.setLayout(vbox)

    def screen16(self):
        screen16 = Explore16(self.username, self.loginrole)
        self.close()
        screen16.exec()

    def screen19(self):
        screen19 = OrderHistory19(self.username, self.loginrole)
        self.close()
        screen19.exec()

    def screen17(self):
        if self.station == None:

            screen17b = CurrentInfo17B(self.username, self.loginrole)
            self.close()
            screen17b.exec()
        else:

            screen17 = CurrentInfo17(self.username, self.loginrole)
            self.close()
            screen17.exec()

class HomeScreenManager(QDialog):
    def __init__(self, username, loginrole):
        super(HomeScreenManager, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Manager Home")
        self.l1 = QLabel()
        self.l1.setText("Home")

        self.managermanage = QPushButton("Manage Food Truck")

        self.managermanage.setEnabled(True)
        self.managermanage.clicked.connect(self.screen11)

        self.managersummary = QPushButton("View Food Truck Summary")

        self.managersummary.setEnabled(True)
        self.managersummary.clicked.connect(self.screen14)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.managermanage)
        vbox.addWidget(self.managersummary)
        self.setLayout(vbox)


    def screen11(self):
        screen11 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen11.exec()

    def screen14(self):
        screen14 = FoodTruckSummary14(self.username, self.loginrole)
        self.close()
        screen14.exec()

class HomeScreenAdmin(QDialog):
    def __init__(self, username, loginrole):
        super(HomeScreenAdmin, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Admin Home")
        self.l1 = QLabel()
        self.l1.setText("Home")

        self.adminmanage = QPushButton("Manage Building and Station")

        self.adminmanage.setEnabled(True)
        self.adminmanage.clicked.connect(self.screen4)

        self.newfood = QPushButton("Manage Food")

        self.newfood.setEnabled(True)
        self.newfood.clicked.connect(self.screen9)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.adminmanage)
        vbox.addWidget(self.newfood)
        self.setLayout(vbox)

    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

    def screen9(self):
        screen9 = ManageFood9(self.username, self.loginrole, "None")
        self.close()
        screen9.exec ()

class HomeScreenCustomerManager(QDialog):
    def __init__(self, username, loginrole):
        super(HomeScreenCustomerManager, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Customer Manager Home")
        self.l1 = QLabel()
        self.l1.setText("Home")

        cursor = connection.cursor()
        cursor.execute('''select stationName from customer where username = "''' + self.username + '''";''')
        self.station = cursor.fetchall()[0]["stationName"]

        self.explore = QPushButton("Explore")
        # Screen 16
        self.explore.setEnabled(True)
        self.explore.clicked.connect(self.screen16)

        self.history = QPushButton("View Order History")
        # screen 19
        self.history.setEnabled(True)
        self.history.clicked.connect(self.screen19)

        self.currentinfo = QPushButton("View Current Information")
        self.currentinfo.setEnabled(True)
        self.currentinfo.clicked.connect(self.screen17)

        self.managermanage = QPushButton("Manage Food Truck")

        self.managermanage.setEnabled(True)
        self.managermanage.clicked.connect(self.screen11)

        self.managersummary = QPushButton("View Food Truck Summary")

        self.managersummary.setEnabled(True)
        self.managersummary.clicked.connect(self.screen14)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.explore)
        vbox.addWidget(self.history)
        vbox.addWidget(self.currentinfo)
        vbox.addWidget(self.managermanage)
        vbox.addWidget(self.managersummary)
        self.setLayout(vbox)

    def screen16(self):
        screen16 = Explore16(self.username, self.loginrole)
        self.close()
        screen16.exec()

    def screen19(self):
        screen19 = OrderHistory19(self.username, self.loginrole)
        self.close()
        screen19.exec()

    def screen17(self):
        if self.station == None:
            screen17b = CurrentInfo17B(self.username, self.loginrole)
            self.close()
            screen17b.exec()
        else:
            screen17 = CurrentInfo17(self.username, self.loginrole)
            self.close()
            screen17.exec()

    def screen11(self):
        screen11 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen11.exec()

    def screen14(self):
        screen14 = FoodTruckSummary14(self.username, self.loginrole)
        self.close()
        screen14.exec()

class HomeScreenCustomerAdmin(QDialog):
    def __init__(self, username, loginrole):
        super(HomeScreenCustomerAdmin, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Customer Admin Home")
        self.l1 = QLabel()
        self.l1.setText("Home")
        cursor = connection.cursor()
        cursor.execute('''select stationName from customer where username = "''' + self.username + '''";''')
        self.station = cursor.fetchall()[0]["stationName"]

        self.explore = QPushButton("Explore")
        # Screen 16
        self.explore.setEnabled(True)
        self.explore.clicked.connect(self.screen16)

        self.history = QPushButton("View Order History")
        # screen 19
        self.history.setEnabled(True)
        self.history.clicked.connect(self.screen19)

        self.currentinfo = QPushButton("View Current Information")
        self.currentinfo.setEnabled(True)
        self.currentinfo.clicked.connect(self.screen17)

        self.adminmanage = QPushButton("Manage Building and Station")

        self.adminmanage.setEnabled(True)
        self.adminmanage.clicked.connect(self.screen4)

        self.newfood = QPushButton("Manage Food")

        self.newfood.setEnabled(True)
        self.newfood.clicked.connect(self.screen9)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.explore)
        vbox.addWidget(self.history)
        vbox.addWidget(self.currentinfo)
        vbox.addWidget(self.adminmanage)
        vbox.addWidget(self.newfood)
        self.setLayout(vbox)

    def screen16(self):
        screen16 = Explore16(self.username, self.loginrole)
        self.close()
        screen16.exec()

    def screen19(self):
        screen19 = OrderHistory19(self.username, self.loginrole)
        self.close()
        screen19.exec()

    def screen17(self):
        if self.station == None:
            screen17b = CurrentInfo17B(self.username, self.loginrole)
            self.close()
            screen17b.exec()
        else:
            screen17 = CurrentInfo17(self.username, self.loginrole)
            self.close()
            screen17.exec()

    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()


    def screen9(self):
        screen9 = ManageFood9(self.username, self.loginrole, "None")
        self.close()
        screen9.exec()

class HomeScreenStaff(QDialog):
    def __init__(self, username, loginrole):
        super(HomeScreenStaff, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Staff Home")
        self.l1 = QLabel()
        self.l1.setText("Home")



        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        self.setLayout(vbox)

class Register(QDialog):
    def __init__(self):
        super(Register, self).__init__()
        self.setWindowTitle("Register")
        self.title = QLabel("Register")
        self.username_label = QLabel("Username")
        self.email_label = QLabel("Email")
        self.first_name_label = QLabel("First Name")
        self.last_name_label = QLabel("Last Name")
        self.password_label = QLabel("Password")
        self.confirm_label = QLabel("Confirm Password")
        self.balance_label = QLabel("Balance")
        self.username = QLineEdit()
        self.email = QLineEdit()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.password = QLineEdit()
        self.confirm = QLineEdit()
        self.balance = QLineEdit()
        self.admin = QRadioButton("Admin")
        self.manager = QRadioButton("Manager")
        self.staff = QRadioButton("Staff")
        self.back = QPushButton("Back")
        self.register = QPushButton("Register")
        self.back.clicked.connect(self.BackHome)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.username_label)
        hbox.addWidget(self.username)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.first_name_label)
        hbox.addWidget(self.first_name)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.password_label)
        hbox.addWidget(self.password)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.balance_label)
        hbox.addWidget(self.balance)
        vbox.addLayout(hbox)
        vbox.addWidget(self.back)
        hbox_final = QHBoxLayout()
        hbox_final.addLayout(vbox)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.email_label)
        hbox.addWidget(self.email)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.last_name_label)
        hbox.addWidget(self.last_name)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.confirm_label)
        hbox.addWidget(self.confirm)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.admin)
        hbox.addWidget(self.manager)
        hbox.addWidget(self.staff)
        vbox.addLayout(hbox)
        vbox.addWidget(self.register)
        hbox_final.addLayout(vbox)

        self.setLayout(hbox_final)
        self.cursor = connection.cursor()

        self.register.clicked.connect(self.register_entry)

    def register_entry(self):
        test = False
        if self.username.text() and self.password.text() and self.first_name.text() and self.last_name.text() \
                and self.password.text() == self.confirm.text():
            if self.balance.text() and not self.email.text():
                self.cursor.execute(f"call register ('{self.username.text()}', null, '{self.first_name.text()}', \
                '{self.last_name.text()}', '{self.password.text()}', '{self.balance.text()}', null);")
                test = True
            elif self.balance.text() and self.email.text():
                if self.admin.isChecked():
                    self.cursor.execute(
                        f"call register ('{self.username.text()}', '{self.email.text()}', '{self.first_name.text()}', \
                    '{self.last_name.text()}', '{self.password.text()}', '{self.balance.text()}', 'Admin');")
                    test = True
                elif self.manager.isChecked():
                    self.cursor.execute(
                        f"call register ('{self.username.text()}', '{self.email.text()}', '{self.first_name.text()}', \
                    '{self.last_name.text()}', '{self.password.text()}', '{self.balance.text()}', 'Manager');")
                    test = True
                elif self.staff.isChecked():
                    self.cursor.execute(
                        f"call register ('{self.username.text()}', '{self.email.text()}', '{self.first_name.text()}', \
                    '{self.last_name.text()}', '{self.password.text()}', '{self.balance.text()}', 'Staff');")
                    test = True
            elif self.email.text():
                if self.admin.isChecked():
                    self.cursor.execute(
                        f"call register ('{self.username.text()}', '{self.email.text()}', '{self.first_name.text()}', \
                    '{self.last_name.text()}', '{self.password.text()}', null, 'Admin');")
                    test = True
                elif self.manager.isChecked():
                    self.cursor.execute(
                        f"call register ('{self.username.text()}', '{self.email.text()}', '{self.first_name.text()}', \
                    '{self.last_name.text()}', '{self.password.text()}', null, 'Manager');")
                    test = True
                elif self.staff.isChecked():
                    self.cursor.execute(
                        f"call register ('{self.username.text()}', '{self.email.text()}', '{self.first_name.text()}', \
                    '{self.last_name.text()}', '{self.password.text()}', null, 'Staff');")
                    test = True

        connection.commit()

        if test:
            self.close()
            log = LoginScreen()
            log.exec ()

    def BackHome(self):
        screenlogin = LoginScreen()
        self.close()
        screenlogin.exec()

class AdminManageBS4(QDialog):
    def __init__(self, username, loginrole, filtercriteria):
        super(AdminManageBS4, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.fbuilding = filtercriteria[0]
        self.ftag = filtercriteria[1]
        self.fstation = filtercriteria[2]
        self.fminc = filtercriteria[3]
        self.fmaxc = filtercriteria[4]
        self.tagstoupdate = []
        self.descriptiontoupdate = ""
        self.setModal(True)
        self.setWindowTitle("Admin Manage Building and Station")
        self.foodtruckindex = -1
        self.stationstartingindex = 0
        self.buildingstartingindex = 0
        #SQL QUERIES
        self.allbuildings = []
        self.allstations = []
        cursor = connection.cursor()
        cursor.execute("select stationName from station order by stationName ASC;")
        for i in cursor.fetchall():
            self.allstations.append(i["stationName"])

        connection.commit()

        cursor = connection.cursor()
        cursor.execute("select buildingname from building order by buildingname ASC;")
        for i in cursor.fetchall():
            self.allbuildings.append(i["buildingname"])

        connection.commit()

        #"select stationName from station order by stationName ASC;"

        cursor = connection.cursor()
        query = '''call ad_filter_building_station("''' + self.fbuilding + '''" ,"''' + self.ftag + '''", "''' + self.fstation +'''", ''' + self.fminc +", " + self.fmaxc +");"
        cursor.execute(query)
        connection.commit()

        cursor = connection.cursor()
        query = "select * from ad_filter_building_station_result;"
        cursor.execute(query)
        connection.commit()
        self.data = cursor.fetchall()

        self.l1 = QLabel()
        self.l1.setText("Manage Building and Station")

        self.l2 = QLabel()
        self.l2.setText("Building Name")
        self.buildingcb = QComboBox()
        self.buildingcb.addItem("")
        for i in range(0, len(self.allbuildings)):
            self.buildingcb.addItem(self.allbuildings[i])
            if self.allbuildings[i] == self.fbuilding:
                self.buildingstartingindex = i + 1
        self.buildingcb.setCurrentIndex(self.buildingstartingindex)
        self.l3 = QLabel()
        self.l3.setText("Building Tag (Contain)")
        self.tagcontains = QLineEdit()
        self.tagcontains.setText(self.ftag)

        self.l4 = QLabel()
        self.l4.setText("Station Name")
        self.stationcb = QComboBox()
        self.stationcb.addItem("")
        for i in range(0, len(self.allstations)):
            self.stationcb.addItem(self.allstations[i])
            if self.allstations[i] == self.fstation:
                self.stationstartingindex = i + 1

        self.stationcb.setCurrentIndex(self.stationstartingindex)

        self.l5 = QLabel()
        self.l5.setText("Capacity")
        self.l6 = QLabel()
        self.l6.setText("Through")
        self.minc = QLineEdit()
        if self.fminc == "Null":
            self.minc.setText("")
        else:
            self.minc.setText(self.fminc)
        self.minc.setValidator(QtGui.QIntValidator(1, 99999))

        self.maxc = QLineEdit()
        if self.fmaxc == "Null":
            self.maxc.setText("")
        else:
            self.maxc.setText(self.fmaxc)

        self.maxc.setValidator(QtGui.QIntValidator(1, 99999))

        self.FilterB = QPushButton("Filter")
        self.FilterB.setEnabled(True)
        self.FilterB.clicked.connect(self.filter)
        #table

        self.DeleteB = QPushButton("Delete Building")
        self.DeleteB.setEnabled(False)
        self.DeleteB.clicked.connect(self.DB)

        self.DeleteS = QPushButton("Delete Station")
        self.DeleteS.setEnabled(False)
        self.DeleteS.clicked.connect(self.DS)

        self.table = QtWidgets.QTableWidget()
        # make this based of length of SQL Query
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(5)
        columns = ["Building", "Tag(s)", "Station", "Capacity", "Food Truck(s)"]
        self.table.setHorizontalHeaderLabels(columns)

        # stretched_size = self.table.viewport().size().width() - self.table.horizontalHeader().sectionSize(0)
        # size = max(self.table.sizeHintForColumn(4), stretched_size)
        # self.table.horizontalHeader().resizeSection(4, size)
        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            rb = QtWidgets.QRadioButton(self.data[i]["buildingName"], parent=self.table)

            ##rb.setText(str("FOOD NAME"))
            rb.clicked.connect(self.onStateChanged)
            self.table.setCellWidget(i, 0, rb)
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.data[i]["tags"]))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.data[i]["stationName"]))
            if str(self.data[i]["capacity"]) == "None":
                self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(""))
            else:
                self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(self.data[i]["capacity"])))

            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(self.data[i]["foodTruckNames"]))
            # self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.data2[i]["Tagsss"]))
            # self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.data2[i]["Station Name"]))
            # self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(self.data2[i]["Cap"]))
            # self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(
            #     self.data2[i]["FoodTrucks, FoodTrucks, FoodTrucks, FoodTrucks, FoodTrucks, "]))

        self.CreateB = QPushButton("Create Building")
        self.CreateB.setEnabled(True)
        self.CreateB.clicked.connect(self.CB)

        self.UpdateB = QPushButton("Update Building")
        self.UpdateB.setEnabled(False)
        self.UpdateB.clicked.connect(self.UB)

        self.CreateS = QPushButton("Create Station")
        self.CreateS.setEnabled(True)
        self.CreateS.clicked.connect(self.CS)

        self.UpdateS = QPushButton("Update Station")
        self.UpdateS.setEnabled(False)
        self.UpdateS.clicked.connect(self.US)

        #creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)

        hboxb = QHBoxLayout()
        vboxa = QVBoxLayout()
        hboxa = QHBoxLayout()
        vbox = QVBoxLayout()
        vboxc = QVBoxLayout()
        vboxc.addWidget(self.l1)
        vbox.addLayout(vboxc)
        hboxa.addWidget(self.l2)
        hboxa.addWidget(self.buildingcb)
        vboxa.addLayout(hboxa)
        hboxa = QHBoxLayout()
        hboxa.addWidget(self.l4)
        hboxa.addWidget(self.stationcb)
        vboxa.addLayout(hboxa)
        hboxb.addLayout(vboxa)
        vboxa = QVBoxLayout()
        hboxa = QHBoxLayout()
        hboxa.addWidget(self.l3)
        hboxa.addWidget(self.tagcontains)
        vboxa.addLayout(hboxa)
        hboxa = QHBoxLayout()
        hboxa.addWidget(self.l5)
        hboxa.addWidget(self.minc)
        hboxa.addWidget(self.l6)
        hboxa.addWidget(self.maxc)
        vboxa.addLayout(hboxa)
        hboxb.addLayout(vboxa)
        vbox.addLayout(hboxb)
        vbox.addWidget(self.FilterB)
        vbox.addWidget(self.table)
        hboxd = QHBoxLayout()
        hboxd.addWidget(self.CreateB)
        hboxd.addWidget(self.UpdateB)
        hboxd.addWidget(self.DeleteB)
        vbox.addLayout(hboxd)
        hboxd = QHBoxLayout()
        hboxd.addWidget(self.CreateS)
        hboxd.addWidget(self.UpdateS)
        hboxd.addWidget(self.DeleteS)
        vbox.addLayout(hboxd)
        vbox.addWidget(self.GoHome)

        self.setLayout(vbox)

    def filter(self):
        if self.minc.text() == "":
            minctext = "Null"
        else:
            minctext = self.minc.text()
        if self.maxc.text() == "":
            maxctext = "Null"
        else:
            maxctext = self.maxc.text()
        #DEFAULT TUPLE = (self.username, self.loginrole, ["", "", "", "Null", "Null"])
        # self.loginrole = loginrole
        # self.fbuilding = filtercriteria[0]
        # self.ftag = filtercriteria[1]
        # self.fstation = filtercriteria[2]
        # self.fminc = filtercriteria[3]
        # self.fmaxc = filtercriteria[4]
        screen4 = AdminManageBS4(self.username, self.loginrole,[ self.buildingcb.currentText(), self.tagcontains.text(), self.stationcb.currentText(), minctext, maxctext])
        self.close()
        screen4.exec()

    def CB(self):
        screen5 = CreateBuilding5(self.username, self.loginrole, ["", "", []])
        self.close()
        screen5.exec()
    def UB(self):
        buildingtoupdate = self.table.cellWidget(self.foodtruckindex, 0).text()

        cursor = connection.cursor()
        query = '''call ad_view_building_tags("''' + buildingtoupdate + '''");'''
        cursor.execute(query)
        connection.commit()

        cursor = connection.cursor()
        query = '''select * from ad_view_building_tags_result'''
        cursor.execute(query)
        data1 = cursor.fetchall()
        connection.commit()

        cursor = connection.cursor()
        query = '''call ad_view_building_general("''' + buildingtoupdate + '''");'''
        cursor.execute(query)
        connection.commit()
        cursor = connection.cursor()
        query = '''select * from ad_view_building_general_result'''
        cursor.execute(query)
        data2 = cursor.fetchall()
        connection.commit()

        self.descriptiontoupdate = ""
        for i in data2:
            self.descriptiontoupdate = i["description"]

        for i in data1:
            self.tagstoupdate.append(i["tag"])

        screen6 = UpdateBuilding6(self.username, self.loginrole, buildingtoupdate, self.tagstoupdate, [buildingtoupdate, self.descriptiontoupdate, self.tagstoupdate])
        self.close()
        screen6.exec()

    def CS(self):
        screen7 = CreateStation7(self.username, self.loginrole)
        self.close()
        screen7.exec()

    def US(self):
        stationtoupdate = self.table.item(self.foodtruckindex, 2).text()
        screen8 = UpdateStation8(self.username, self.loginrole, stationtoupdate)
        self.close()
        screen8.exec()

    def DB(self):
        try :
            cursor = connection.cursor()
            query = '''call ad_delete_building("''' + self.table.cellWidget(self.foodtruckindex, 0).text() + '''");'''
            cursor.execute(query)
            connection.commit()

        except:
            dog = 0
        if self.minc.text() == "":
            minctext = "Null"
        else:
            minctext = self.minc.text()
        if self.maxc.text() == "":
            maxctext = "Null"
        else:
            maxctext = self.maxc.text()
        screen4 = AdminManageBS4(self.username, self.loginrole,
                                     [self.buildingcb.currentText(), self.tagcontains.text(),
                                      self.stationcb.currentText(), minctext, maxctext])
        self.close()
        screen4.exec()

    def DS(self):
        #self.table.cellWidget(self.foodtruckindex, 0).text()
        try:

            cursor = connection.cursor()
            query = '''call ad_delete_station("''' + self.table.item(self.foodtruckindex, 2).text() + '''");'''
            cursor.execute(query)
            connection.commit()
        except:
            dog = 0
        if self.minc.text() == "":
            minctext = "Null"
        else:
            minctext = self.minc.text()
        if self.maxc.text() == "":
            maxctext = "Null"
        else:
            maxctext = self.maxc.text()
        screen4 = AdminManageBS4(self.username, self.loginrole,
                                     [self.buildingcb.currentText(), self.tagcontains.text(),
                                      self.stationcb.currentText(), minctext, maxctext])
        self.close()
        screen4.exec()

    def onStateChanged(self):
        self.UpdateB.setEnabled(True)

        self.DeleteB.setEnabled(True)
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()

        if self.table.item(self.foodtruckindex, 2).text() == "":
            self.UpdateS.setEnabled(False)
            self.DeleteS.setEnabled(False)
        else:
            self.UpdateS.setEnabled(True)
            self.DeleteS.setEnabled(True)

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

class CreateBuilding5(QDialog):
    def __init__(self, username, loginrole, currenttags):
        super(CreateBuilding5, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.currentname = currenttags[0]
        self.currentdescription = currenttags[1]

        self.setModal(True)
        self.setWindowTitle("Create Building")
        self.l1 = QLabel()
        self.l1.setText("Create Building")

        self.l2 = QLabel()
        self.l2.setText("Name")
        self.newname = QLineEdit()

        self.l3 = QLabel()
        self.l3.setText("Description")
        self.currenttags = currenttags[2]

        self.description = QTextEdit()

        self.l4 = QLabel()
        self.l4.setText("Tags")
        self.table = QTableWidget()
        self.table.setRowCount(len(self.currenttags)+1)
        self.table.setColumnCount(2)
        columns = ["New Tag", "Tag Action"]
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.createbutton = QPushButton("Create")
        self.createbutton.setEnabled(False)
        self.createbutton.clicked.connect(self.create)
         ### MUST HAVE FOOD TRUCK SELECTED
        for i in range(0,len(self.currenttags)):
            self.createbutton.setEnabled(True)
            remove = QPushButton("Remove")
            remove.clicked.connect(self.onClickDelete)
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem((self.currenttags[i])))

            self.table.setCellWidget(i, 1,remove)
        addlast= QPushButton("Add")
        addlast.clicked.connect(self.onClickAdd)
        addlast.setEnabled(False)
        addedtag = QLineEdit()
        addedtag.textChanged.connect(self.newtagdetection)
        self.test = len(self.currenttags)
        self.table.setCellWidget(self.test, 0, addedtag)
        self.table.setCellWidget(self.test, 1, addlast)

        self.newname.setText(self.currentname)
        self.newname.textChanged.connect(self.checkname)

        self.description.textChanged.connect(self.checkdesc)
        self.description.setText(self.currentdescription)
        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen4)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l2)
        hbox.addWidget(self.newname)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addLayout(hbox)
        vbox.addWidget(self.l3)
        vbox.addWidget(self.description)
        vbox.addWidget(self.l4)
        vbox.addWidget(self.table)
        vbox.addWidget(self.createbutton)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def checkname(self):

        self.currentname = self.newname.text()
        if self.newname.text() == "" or self.description.toPlainText =="" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def checkdesc(self):
        self.currentdescription = self.description.toPlainText()
        if self.newname.text() == "" or self.description.toPlainText() == "" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def newtagdetection(self):
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        if rb.text() =="":
            pass
        else:
            pass
            self.table.cellWidget(self.test, 1).setEnabled(True)
        if self.newname.text() == "" or self.description.toPlainText =="" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def onClickDelete(self):
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()
        self.currenttags.remove(self.table.item(self.foodtruckindex, 0).text())
        screenreload = CreateBuilding5(self.username, self.loginrole,
                                       [self.currentname, self.currentdescription, self.currenttags])
        ### DEFAULT VALUE freshinstance = CreateBuilding5(self.username, self.loginrole, ["", "", []])
        self.close()
        screenreload.exec()



    def onClickAdd(self):
        self.currenttags.append(self.table.cellWidget(self.test, 0).text())

        screenreload = CreateBuilding5(self.username, self.loginrole, [self.currentname, self.currentdescription, self.currenttags])
        ### DEFAULT VALUE freshinstance = CreateBuilding5(self.username, self.loginrole, ["", "", []])
        self.close()
        screenreload.exec()

    def create(self):
        try:
            query = '''call ad_create_building("''' + self.currentname + '''", "''' + self.currentdescription + '''");'''
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

            for i in self.currenttags:
                try:
                    query = '''call ad_add_building_tag("''' + self.currentname +'''", "''' + i +'''");'''
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                except:
                    pass
        except:
            dog = 3

        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()
    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

class UpdateBuilding6(QDialog):
    def __init__(self, username, loginrole, oldbuilding, oldtags, currenttags):
        super(UpdateBuilding6, self).__init__()
        self.setbuildingname = oldbuilding
        self.settags = oldtags
        self.settags2 = sorted(oldtags)

        self.username = username
        self.loginrole = loginrole
        self.currentname = currenttags[0]
        self.currentdescription = currenttags[1]

        self.setModal(True)
        self.setWindowTitle("Update Building")
        self.l1 = QLabel()
        self.l1.setText("Update Building")

        self.l2 = QLabel()
        self.l2.setText("Name")
        self.newname = QLineEdit()

        self.l3 = QLabel()
        self.l3.setText("Description")
        self.currenttags = currenttags[2]
        self.description = QTextEdit()

        self.l4 = QLabel()
        self.l4.setText("Tags")
        self.table = QTableWidget()
        self.table.setRowCount(len(self.currenttags)+1)
        self.table.setColumnCount(2)
        columns = ["New Tag", "Tag Action"]
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.createbutton = QPushButton("Update")
        self.createbutton.setEnabled(False)
        self.createbutton.clicked.connect(self.create)
         ### MUST HAVE FOOD TRUCK SELECTED
        for i in range(0,len(self.currenttags)):
            self.createbutton.setEnabled(True)
            remove = QPushButton("Remove")
            remove.clicked.connect(self.onClickDelete)
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem((self.currenttags[i])))

            self.table.setCellWidget(i, 1,remove)
        addlast= QPushButton("Add")
        addlast.clicked.connect(self.onClickAdd)
        addlast.setEnabled(False)
        addedtag = QLineEdit()
        addedtag.textChanged.connect(self.newtagdetection)
        self.test = len(self.currenttags)
        self.table.setCellWidget(self.test, 0, addedtag)
        self.table.setCellWidget(self.test, 1, addlast)

        self.newname.setText(self.currentname)
        self.newname.textChanged.connect(self.checkname)

        self.description.textChanged.connect(self.checkdesc)
        self.description.setText(self.currentdescription)
        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen4)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l2)
        hbox.addWidget(self.newname)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addLayout(hbox)
        vbox.addWidget(self.l3)
        vbox.addWidget(self.description)
        vbox.addWidget(self.l4)
        vbox.addWidget(self.table)
        vbox.addWidget(self.createbutton)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def checkname(self):
        self.currentname = self.newname.text()
        if self.newname.text() == "" or self.description.toPlainText =="" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def checkdesc(self):
        self.currentdescription = self.description.toPlainText()
        if self.newname.text() == "" or self.description.toPlainText() == "" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def newtagdetection(self):
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        if rb.text() =="":
            pass
        else:
            pass
            self.table.cellWidget(self.test, 1).setEnabled(True)
        if self.newname.text() == "" or self.description.toPlainText =="" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def onClickDelete(self):
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()
        self.currenttags.remove(self.table.item(self.foodtruckindex, 0).text())
        screenreload = UpdateBuilding6(self.username, self.loginrole, self.setbuildingname, self.settags2,
                                       [self.currentname, self.currentdescription, self.currenttags])
        ### DEFAULT VALUE freshinstance = CreateBuilding5(self.username, self.loginrole, ["", "", []])
        self.close()
        screenreload.exec()

    def onClickAdd(self):
        self.currenttags.append(self.table.cellWidget(self.test, 0).text())

        screenreload = UpdateBuilding6(self.username, self.loginrole, self.setbuildingname, self.settags2, [self.currentname, self.currentdescription, self.currenttags])
        ### DEFAULT VALUE freshinstance = CreateBuilding5(self.username, self.loginrole, ["", "", []])
        self.close()
        screenreload.exec()

    def create(self):
        tagstoremove = []
        for i in self.settags:
            if i in self.currenttags:
                self.currenttags.remove(i)
            else:
                tagstoremove.append(i)

        try:
            # remove tags from old building
            for i in tagstoremove:
                query = '''call ad_remove_building_tag("''' + self.setbuildingname + '''", "''' + i +'''");'''
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()

            for i in self.currenttags:
                try:
                    #update current buildings tags
                    query = '''call ad_add_building_tag("''' + self.setbuildingname +'''", "''' + i +'''");'''
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                except:
                    pass
             #update old building name to new building name
            query = '''call ad_update_building("''' + self.setbuildingname + '''", "''' + self.currentname + '''", "''' + self.currentdescription + '''");'''
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

        except:
            dog = 3
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

class CreateStation7(QDialog):
    def __init__(self, username, loginrole):
        super(CreateStation7, self).__init__()
        self.username = username
        self.loginrole = loginrole

        self.setModal(True)
        self.setWindowTitle("Create Station")
        self.l1 = QLabel()
        self.l1.setText("Create Station")

        cursor = connection.cursor()
        query = "call ad_get_available_building"
        cursor.execute(query)
        connection.commit()

        cursor = connection.cursor()
        query = '''select * from ad_get_available_building_result'''
        cursor.execute(query)
        connection.commit()

        self.availablebuildings = cursor.fetchall()

        self.l2 = QLabel()
        self.l2.setText("Name")
        self.newstationname = QLineEdit()
        self.newstationname.textChanged.connect(self.onStateChanged)

        self.l3 = QLabel()
        self.l3.setText("Capacity")
        self.stationcapacity = QLineEdit()
        self.stationcapacity.setValidator(QtGui.QIntValidator(1, 99999))
        self.stationcapacity.textChanged.connect(self.onStateChanged)

        self.l4 = QLabel()
        self.l4.setText("Sponsored Building")
        self.buildingcb = QComboBox()

        self.CreateB = QPushButton("Create")
        self.CreateB.setEnabled(False)
        self.CreateB.clicked.connect(self.createstation)
        ### MUST HAVE FOOD TRUCK SELECTED
        for i in range(0, len(self.availablebuildings)):
            self.buildingcb.addItem(self.availablebuildings[i]["buildingName"])

        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen4)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l2)
        hbox.addWidget(self.newstationname)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l3)
        hbox.addWidget(self.stationcapacity)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l4)
        hbox.addWidget(self.buildingcb)
        vbox.addLayout(hbox)
        vbox.addWidget(self.CreateB)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def onStateChanged(self):
        if self.stationcapacity.text() == "" or self.newstationname == "":
            self.CreateB.setEnabled(False)
        else:
            self.CreateB.setEnabled(True)

    def createstation(self):
        cursor = connection.cursor()
        query = '''call ad_create_station("''' + self.newstationname.text() + '''", "''' + self.buildingcb.currentText() +'''", ''' + self.stationcapacity.text() +''');'''
        cursor.execute(query)
        connection.commit()
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

class UpdateStation8(QDialog):
    def __init__(self, username, loginrole, stationname):
        super(UpdateStation8, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.stationname=stationname

        self.setModal(True)
        self.setWindowTitle("Update Station")
        self.l1 = QLabel()
        self.l1.setText("Update Station")

        cursor = connection.cursor()
        query = "call ad_get_available_building"
        cursor.execute(query)
        connection.commit()

        cursor = connection.cursor()
        query = '''select * from ad_get_available_building_result'''
        cursor.execute(query)
        connection.commit()

        self.availablebuildings = cursor.fetchall()
        self.addedavailablebuildings = []
        for i in range(0, len(self.availablebuildings)):
            self.addedavailablebuildings.append(self.availablebuildings[i]["buildingName"])

        cursor = connection.cursor()
        query = '''select buildingName, capacity from station where stationName = "''' + self.stationname +'''";'''
        cursor.execute(query)
        self.currentinfo = cursor.fetchall()
        self.currentbuilding =  self.currentinfo[0]["buildingName"]
        self.currentcapacity = str(self.currentinfo[0]["capacity"])
        self.addedavailablebuildings.append(self.currentbuilding)
        self.finalbuildings = sorted(self.addedavailablebuildings)

        connection.commit()

        self.l2 = QLabel()
        self.l2.setText("Name")
        self.lstation = QLabel()
        self.lstation.setText(self.stationname)

        self.l3 = QLabel()
        self.l3.setText("Capacity")
        self.stationcapacity = QLineEdit()
        self.stationcapacity.setValidator(QtGui.QIntValidator(1, 99999))
        self.stationcapacity.setText(self.currentcapacity)

        self.stationcapacity.textChanged.connect(self.onStateChanged)

        self.l4 = QLabel()
        self.l4.setText("Sponsored Building")
        self.buildingcb = QComboBox()

        self.currentindex = 0
        self.CreateB = QPushButton("Update")
        self.CreateB.setEnabled(True)
        self.CreateB.clicked.connect(self.createstation)
        ### MUST HAVE FOOD TRUCK SELECTED
        for i in self.finalbuildings:
             self.buildingcb.addItem(i)
        k = 0
        for i in self.finalbuildings:
            if i == self.currentbuilding:
                self.currentindex = k
            else:
                k+=1
        self.buildingcb.setCurrentIndex(self.currentindex)
        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen4)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l2)
        hbox.addWidget(self.lstation)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l3)
        hbox.addWidget(self.stationcapacity)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l4)
        hbox.addWidget(self.buildingcb)
        vbox.addLayout(hbox)
        vbox.addWidget(self.CreateB)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def onStateChanged(self):
        if self.stationcapacity.text() =="":
            self.CreateB.setEnabled(False)
        else:
            self.CreateB.setEnabled(True)

    def createstation(self):
        query = '''call ad_update_station("''' + self.stationname + '''", ''' + self.stationcapacity.text() +''', "''' + self.buildingcb.currentText()  +'''");'''
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

    def screen4(self):
        screen4 = AdminManageBS4(self.username, self.loginrole, ["", "", "", "Null", "Null"])
        self.close()
        screen4.exec()

class ManageFood9(QDialog):
    def __init__(self, username, loginrole, filtercriteria):
        super(ManageFood9, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.filtercriteria = filtercriteria
        self.setModal(True)
        self.setWindowTitle("Admin Manage Food")
        self.l1 = QLabel()
        self.l1.setText("Manage Food")
        self.l2 = QLabel()
        self.l2.setText("Name")
        self.fooditems =[]
        self.foodtruckindex = -1
        cursor = connection.cursor()
        cursor.execute('''call ad_filter_food(Null, Null, Null);''')
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("select * from ad_filter_food_result;")
        self.data = cursor.fetchall()

        self.FilterButton = QPushButton("Filter")
        self.FilterButton.setEnabled(True)
        self.FilterButton.clicked.connect(self.Filter)

        self.CreateF = QPushButton("Create")
        self.CreateF.setEnabled(True)
        self.CreateF.clicked.connect(self.CF)
        self.filtercb = QComboBox()
        self.DeleteButton = QPushButton("Delete")
        self.DeleteButton.setEnabled(False)
        self.DeleteButton.clicked.connect(self.Delete)
        self.filtercb.addItem("None")

        self.table = QtWidgets.QTableWidget()
        # make this based of length of SQL Query
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(3)
        columns = ["Name", "Menu Count", "Purchase Count"]
        self.table.setHorizontalHeaderLabels(columns)
        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            self.fooditems.append(self.data[i]["foodName"])
            ##rb.setText(str("FOOD NAME"))

            if self.filtercriteria == "None":
                a = QtWidgets.QTableWidgetItem()

                rb = QtWidgets.QRadioButton("", parent=self.table)

                rb.setAccessibleName(self.data[i]["foodName"])
                a.setData(QtCore.Qt.EditRole , QtCore.QVariant(self.data[i]["foodName"]))
                self.table.setCellWidget(i, 0, rb)
                self.table.setItem(i, 0, QtWidgets.QTableWidgetItem("     "+ str(self.data[i]["foodName"])))

                b = QtWidgets.QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole , QtCore.QVariant(self.data[i]["menuCount"]))
                self.table.setItem(i, 1, b)

                c = QtWidgets.QTableWidgetItem()
                c.setData(QtCore.Qt.EditRole, QtCore.QVariant(self.data[i]["purchaseCount"]))
                self.table.setItem(i, 2, c)

                rb.clicked.connect(self.onStateChanged)

            elif self.data[i]["foodName"] == self.filtercriteria:
                a = QtWidgets.QTableWidgetItem()

                rb = QtWidgets.QRadioButton("", parent=self.table)

                rb.setAccessibleName(self.data[i]["foodName"])
                a.setData(QtCore.Qt.EditRole, QtCore.QVariant(self.data[i]["foodName"]))
                self.table.setCellWidget(0, 0, rb)
                self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("     " + str(self.data[i]["foodName"])))

                b = QtWidgets.QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(self.data[i]["menuCount"]))
                self.table.setItem(0, 1, b)

                c = QtWidgets.QTableWidgetItem()
                c.setData(QtCore.Qt.EditRole, QtCore.QVariant(self.data[i]["purchaseCount"]))
                self.table.setItem(0, 2, c)

                rb.clicked.connect(self.onStateChanged)

        self.filtercb.addItems(sorted(self.fooditems))
        vh = self.table.verticalHeader()
        vh.setVisible(False)
        self.table.setSortingEnabled(True)

        #creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)
        vbox = QVBoxLayout()

        vbox.addWidget(self.l1)
        vbox.addWidget(self.l2)
        vbox.addWidget(self.filtercb)
        vbox.addWidget(self.FilterButton)
        vbox.addWidget(self.table)
        vbox.addWidget(self.CreateF)
        vbox.addWidget(self.DeleteButton)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def onStateChanged(self):
        self.DeleteButton.setEnabled(True)
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()

    def Filter(self):
        screen9 = ManageFood9(self.username, self.loginrole, self.filtercb.currentText())
        self.close()
        screen9.exec()

    def Delete(self):
        try:
            cursor = connection.cursor()
            query = '''call ad_delete_food("''' + self.table.item(self.foodtruckindex, 0).text().strip() + '''");'''
            cursor.execute(query)
            connection.commit()
            screen9 = ManageFood9(self.username, self.loginrole, "None")
            self.close()
            screen9.exec()
        except:
            screen9 = ManageFood9(self.username, self.loginrole, "None")
            self.close()
            screen9.exec()
    def CF(self):
        screen10 = CreateFood10(self.username, self.loginrole)
        self.close()
        screen10.exec()

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class CreateFood10(QDialog):
    def __init__(self, username, loginrole):
        super(CreateFood10, self).__init__()
        self.username = username
        self.loginrole = loginrole

        self.setModal(True)
        self.setWindowTitle("Create Food")
        self.l1 = QLabel()
        self.l1.setText("Create Food")
        self.newFood = QLineEdit()

        self.createf = QPushButton("Create")
        self.createf.setEnabled(False)
        self.createf.clicked.connect(self.createfood)

        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen9)

        self.newFood.textChanged.connect(self.enablecreatebutton)

        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.newFood)
        vbox.addWidget(self.createf)

        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def screen9(self):
        screen9 = ManageFood9(self.username, self.loginrole, "None")
        self.close()
        screen9.exec()

    def createfood(self):
        cursor = connection.cursor()
        query = '''select * from food where foodname =''' + '''"''' + self.newFood.text() + '''"'''
        cursor.execute(query)
        data = cursor.fetchall()

        if len(data) == 0:
            cursor = connection.cursor()
            query = '''call ad_create_food('''+ '''"''' +  self.newFood.text() + '''")'''
            cursor.execute(query)

            connection.commit()
            self.newFood.setText('')

    def enablecreatebutton(self):
        if len(self.newFood.text()) == 0:
            self.createf.setEnabled(False)

        else:
            self.createf.setEnabled(True)

class ManageFoodTruck11(QDialog):
    def __init__(self, username, loginrole):
        super(ManageFoodTruck11, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.hasremainingcapacity = False
        self.var = 0

        # Fill Station dropdown with values
        cursor = connection.cursor()
        query = f"call mn_filter_foodTruck('{self.username}', null, null, null, null, False);"
        cursor.execute(query)

        cursor = connection.cursor()
        query = "select * from mn_filter_foodTruck_result;"
        cursor.execute(query)
        self.data = cursor.fetchall()

        self.setModal(True)
        self.setWindowTitle("Manager Manage Food Truck")
        self.l1 = QLabel()
        self.l1.setText("Manage Food Truck")

        self.l2 = QLabel()
        self.l2.setText("Food Truck Name (contain)")
        self.ftname = QLineEdit()

        self.l3 = QLabel()
        self.l3.setText("Station Name")
        self.station = QComboBox()
        self.station.addItem("None")

        cursor.execute("SELECT stationName from station")
        self.result = cursor.fetchall()

        for line in self.result:
            self.station.addItem(line["stationName"])

        self.l4 = QLabel()
        self.l4.setText("Staff Count")
        self.l5 = QLabel()
        self.l5.setText("Through")
        self.mins = QLineEdit()
        self.maxs = QLineEdit()

        self.remcapB = QtWidgets.QCheckBox()
        self.remcapB.setText("Has Remaining Capacity")
        self.remcapB.clicked.connect(self.hasremaining)

        self.FilterB = QPushButton("Filter")
        self.FilterB.setEnabled(True)
        self.FilterB.clicked.connect(self.filter)

        #CREATE TABLE
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(5)
        columns = ["FoodTruckName", "Station Name", "Remaining Capacity", "Staff(s)", "#Menu Item"]
        self.table.setHorizontalHeaderLabels(columns)

        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            rb = QtWidgets.QRadioButton(self.data[i]["foodTruckName"], parent=self.table)
            rb.clicked.connect(self.OnStateChange)
            self.table.setCellWidget(i, 0, rb)

            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.data[i]["stationName"]))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.data[i]["remainingCapacity"])))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(self.data[i]["staffCount"])))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(self.data[i]["menuItemCount"])))

        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)

        self.CreateFT = QPushButton("Create")
        self.CreateFT.setEnabled(True)
        self.CreateFT.clicked.connect(self.CFT)

        self.UpdateFT = QPushButton("Update")
        self.UpdateFT.setEnabled(True)
        self.UpdateFT.clicked.connect(self.UFT)

        self.DeleteFT = QPushButton("Delete")
        self.DeleteFT.setEnabled(False)
        self.DeleteFT.clicked.connect(self.DFT)

        #SET LAYOUT
        vbox1 = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.l2)
        hbox1.addWidget(self.ftname)
        hbox1.addWidget(self.l3)
        hbox1.addWidget(self.station)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.l4)
        hbox2.addWidget(self.mins)
        hbox2.addWidget(self.l5)
        hbox2.addWidget(self.maxs)
        hbox2.addWidget(self.remcapB)
        hbox2.addWidget(self.FilterB)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.table)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.GoHome)
        hbox3.addWidget(self.CreateFT)
        hbox3.addWidget(self.UpdateFT)
        hbox3.addWidget(self.DeleteFT)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(vbox1)
        self.vbox.addLayout(hbox1)
        self.vbox.addLayout(hbox2)
        self.vbox.addLayout(hbox3)
        self.vbox.addLayout(vbox2)

        self.setLayout(self.vbox)
        connection.commit()

    def screen11(self):
        screen11 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen11.exec()

    def hasremaining(self):
        if self.var == 0:
            self.hasremainingcapacity = True
            self.var = 1
        else:
            self.hasremainingcapacity = False
            self.var = 0

    def OnStateChange(self):
        self.UpdateFT.setEnabled(True)
        self.DeleteFT.setEnabled(True)
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()

    def filter(self):
        self.vbox.removeWidget(self.table)
        sip.delete(self.table)
        self.table = None

        if self.station.currentText() == "None":
            station = "null"
        else:
            station = f"'{self.station.currentText()}'"
        if (not self.ftname.text()):
            ftname = "null"
        else:
            ftname = f"'{self.ftname.text()}'"
        if self.mins.text() == "":
            mins = "Null"
        else:
            mins = self.mins.text()
        if self.maxs.text() == "":
            maxs = "Null"
        else:
            maxs = self.maxs.text()

        cursor = connection.cursor()
        query = f"call mn_filter_foodTruck('{self.username}', {ftname}, {station}, {mins}, {maxs}, {self.hasremainingcapacity});"
        cursor.execute(query)
        query = "select * from mn_filter_foodTruck_result;"
        cursor.execute(query)
        self.data = cursor.fetchall()

        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(5)
        columns = ["FoodTruckName", "Station Name", "Remaining Capacity", "Staff(s)", "#Menu Item"]
        self.table.setHorizontalHeaderLabels(columns)

        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            rb = QtWidgets.QRadioButton(self.data[i]["foodTruckName"], parent=self.table)
            rb.clicked.connect(self.OnStateChange)
            self.table.setCellWidget(i, 0, rb)

            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.data[i]["stationName"]))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.data[i]["remainingCapacity"])))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(self.data[i]["staffCount"])))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(self.data[i]["menuItemCount"])))

        self.vbox.addWidget(self.table)
        self.setLayout(self.vbox)

    def CFT(self):
        screen12 = CreateFoodTruck12(self.username, self.loginrole, ["", "", [],[]])
        self.close()
        screen12.exec()

    def UFT(self):
        cursor = connection.cursor()
        self.truckName = self.table.cellWidget(self.foodtruckindex, 0).text()
        query = f"SELECT DISTINCT staff.username AS staffusername, CONCAT(user.firstName, ' ', user.lastName) AS staffname FROM staff JOIN user USING(username) WHERE staff.foodTruckName = '{self.truckName}';"
        cursor.execute(query)
        self.staff = cursor.fetchall()

        query = f"SELECT stationName FROM foodtruck WHERE foodTruckName = '{self.truckName}';"
        cursor.execute(query)
        self.stationName = cursor.fetchall()

        alist = [self.truckName, self.stationName, self.staff, []]
        screen13 = UpdateFoodTruck13(self.username, self.loginrole, self.truckName, self.stationName[0]["stationName"], self.staff, alist)
        self.close()
        screen13.exec()

    def DFT(self):
        cursor = connection.cursor()
        query = "call mn_delete_foodTruck('" + self.table.cellWidget(self.foodtruckindex, 0).text() + "');"
        cursor.execute(query)
        connection.commit()
        screen4 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen4.exec()

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class CreateFoodTruck12(QDialog):
    def __init__(self, username, loginrole,currenttags):
        super(CreateFoodTruck12, self).__init__()
        self.username = username
        self.loginrole = loginrole
        #SQL HERE
        self.availablestaff =[]
        self.setfood =[]
        self.initialstaff = []
        self.currentname = currenttags[0]
        self.currentstation = currenttags[1]
        self.currentstaff =currenttags[2]
        self.newfoods = currenttags[3]

        self.setModal(True)
        self.setWindowTitle("Create Food Truck")
        self.l1 = QLabel()
        self.l1.setText("Create Food Truck")

        self.l2 = QLabel()
        self.l2.setText("Name")
        self.newname = QLineEdit()
        cursor = connection.cursor()
        query = '''SELECT DISTINCT staff.username, CONCAT(user.firstName, " ", user.lastName) as staffname FROM staff JOIN user using(username) WHERE staff.foodTruckName is null;'''
        cursor.execute(query)
        staffdata = cursor.fetchall()
        connection.commit()
        for i in staffdata:
            self.availablestaff.append({"staffusername": i["username"], "staffname": i["staffname"]})

        self.l3 = QLabel()
        self.l3.setText("Station")
        self.stationcb =QComboBox()

        query = " call mn_filter_foodTruck_hascapacity;"

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        query = "select stationname from mn_filter_foodTruck_remainingcapacity where capacity > 0;"
        cursor.execute(query)
        self.availablestations = cursor.fetchall()
        connection.commit()
        index = -1
        k = 0
        for i in range(0,len(self.availablestations)):
            self.stationcb.addItem(self.availablestations[i]["stationname"])
            if self.availablestations[i]["stationname"] == self.currentstation:
                index = k
            else:
                k+=1

        cursor = connection.cursor()
        query = "select * from food;"
        cursor.execute(query)
        connection.commit()

        self.datafood = cursor.fetchall()
        self.allfoods =[]
        for i in self.datafood:
            self.allfoods.append(i["foodName"])

        #CREATE THE STATION NAMES HERE
        if index == -1:
            pass
        else:
            self.stationcb.setCurrentIndex(index)

        self.l7 = QLabel()
        self.l7.setText("Assigned Staff")
        self.tablestaff =QTableWidget()
        self.tablestaff.setRowCount(len(self.currentstaff) + len(self.availablestaff))
        self.tablestaff.setColumnCount(1)
        self.tablestaff.horizontalHeader().hide()
        self.tablestaff.verticalHeader().hide()

        for i in range(0,len(self.initialstaff)):
            staff = QCheckBox(self.initialstaff[i]["staffname"])

            for k in self.currentstaff:
                if k["staffusername"] == self.initialstaff[i]["staffusername"]:
                    staff.setChecked(True)
            staff.stateChanged.connect(self.stafflist)
            self.tablestaff.setCellWidget(i, 0, staff)

        self.l4 = QLabel()
        self.l4.setText("MenuItem")
        self.table = QTableWidget()
        self.table.setRowCount(len(self.setfood)+len(self.newfoods)+1)
        self.table.setColumnCount(3)
        columns = ["Food", "Price", "Action"]
        self.table.setHorizontalHeaderLabels(columns)
        self.table.verticalHeader().hide()
        self.createbutton = QPushButton("Create")
        self.createbutton.setEnabled(True)
        self.createbutton.clicked.connect(self.create)
         ### MUST HAVE FOOD TRUCK SELECTED

        cat = len(self.initialstaff)
        # FILL ASSIGNED STAFF
        for i in range(0,len(self.availablestaff)):
            staff = QCheckBox(self.availablestaff[i]["staffname"])


            for k in self.currentstaff:
                if k["staffusername"] == self.availablestaff[i]["staffusername"]:
                    staff.setChecked(True)
            staff.stateChanged.connect(self.stafflist)
            self.tablestaff.setCellWidget(i + cat, 0, staff)

        #FILL MENUITEM
        dog = len(self.newfoods) + len(self.setfood)

        for i in range(0,len(self.setfood)):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem((self.setfood[i]["food"])))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem((self.setfood[i]["price"])))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem("None"))
            pass

        for i in range(0 , len(self.newfoods)):
            k = len(self.setfood)
            remove = QPushButton("Remove")
            remove.clicked.connect(self.onClickDelete)
            self.table.setItem(k+i, 0, QtWidgets.QTableWidgetItem((self.newfoods[i]["food"])))
            self.table.setItem(k + i, 1, QtWidgets.QTableWidgetItem((self.newfoods[i]["price"])))

            self.table.setCellWidget(k+i, 2, remove)

        self.addlast= QPushButton("Add")
        self.addlast.clicked.connect(self.onClickAdd)
        self.addlast.setEnabled(False)
        self.addedfood = QComboBox()
        self.addedfood.currentTextChanged.connect(self.newtagdetection)
        self.addedprice = QLineEdit()
        self.addedprice.textChanged.connect(self.newtagdetection)
        self.table.setCellWidget(dog, 0, self.addedfood)
        self.table.setCellWidget(dog, 1, self.addedprice)
        self.table.setCellWidget(dog, 2, self.addlast)

        self.addedfood.currentIndexChanged.connect(self.newtagdetection)

        for i in self.setfood:
            if i["food"] in self.allfoods:
                self.allfoods.remove(i["food"])
        for i in self.newfoods:
            if i["food"] in self.allfoods:
                self.allfoods.remove(i["food"])
        for i in self.allfoods:
            self.addedfood.addItem(i)

        self.stationcb.currentTextChanged.connect(self.checkname)

        self.newname.setText(self.currentname)
        self.newname.textChanged.connect(self.checkname)

        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen4)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l2)
        hbox.addWidget(self.newname)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.l3)
        hbox.addWidget(self.stationcb)

        vbox.addLayout(hbox)
        vbox.addWidget(self.l7)
        vbox.addWidget(self.tablestaff)
        vbox.addWidget(self.l4)
        vbox.addWidget(self.table)
        vbox.addWidget(self.createbutton)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def stafflist(self):
        rb = self.sender()
        ix = self.tablestaff.indexAt(rb.pos())
        self.staffindex = ix.row()
        name = self.tablestaff.cellWidget(self.staffindex,0).text()
        state = self.tablestaff.cellWidget(self.staffindex,0).checkState()

        if state == 2:
            for i in self.initialstaff:
                if i["staffname"] == name:
                    self.currentstaff.append(i)
            for i in self.availablestaff:
                if i["staffname"] == name:
                    self.currentstaff.append(i)
        if state== 0:
            for i in self.initialstaff:
                if i["staffname"] == name:
                    self.currentstaff.remove(i)
            for i in self.availablestaff:
                if i["staffname"] == name:
                    self.currentstaff.remove(i)

    def checkname(self):
        self.currentname = self.newname.text()
        if self.newname.text() == "" or self.stationcb.currentText() =="" or len(self.currentstaff) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def checkdesc(self):
        self.currentdescription = self.description.toPlainText()
        if self.newname.text() == "" or self.description.toPlainText() == "" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def newtagdetection(self):
         if self.addedprice.text() == "" or self.addedfood.currentText() == "":
             self.addlast.setEnabled(False)
         else:
             self.addlast.setEnabled(True)


    def onClickDelete(self):
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()
        for i in range(0, len(self.newfoods)):
            if self.newfoods[i]["food"] == self.table.item(self.foodtruckindex, 0).text():
                del self.newfoods[i]
                break
        screenreload = CreateFoodTruck12(self.username, self.loginrole, [self.newname.text(), self.stationcb.currentText(), self.currentstaff, self.newfoods])
        self.close()
        screenreload.exec()

    def onClickAdd(self):
        self.newfoods.append({"food":self.table.cellWidget(len(self.newfoods) + len(self.setfood), 0).currentText(), "price":self.table.cellWidget(len(self.newfoods) + len(self.setfood), 1).text()})
        screenreload = CreateFoodTruck12(self.username, self.loginrole, [self.currentname, self.currentstation, self.currentstaff, self.newfoods])
        self.close()
        screenreload.exec()

    def create(self):
        query = '''call mn_create_foodtruck_add_station("''' + self.newname.text() + '''", "''' + self.stationcb.currentText() + '''", "''' + self.username + '''");'''
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

        for i in self.newfoods:
            query = '''call mn_create_foodTruck_add_menu_item("''' + self.newname.text() + '''", ''' + i["price"] + ''', "''' + i["food"] + '''");'''
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

        for i in self.currentstaff:
            query = '''update staff set foodtruckname ="''' + self.newname.text() + '''" where username = "''' + i["staffusername"] + '''";'''
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        screen4 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen4.exec()

    def screen4(self):
        screen4 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen4.exec()

class UpdateFoodTruck13(QDialog):
    def __init__(self, username, loginrole,  oldftn, oldstation, initialstaff, currenttags):
        super(UpdateFoodTruck13, self).__init__()
        self.oldstation = oldstation

        self.oldftname = oldftn
        self.initialstaff = initialstaff.copy()
        self.username = username
        self.loginrole = loginrole
        #SQL HERE
        self.availablestaff =[]
        self.setfood =[]

        cursor = connection.cursor()
        query = '''select price, foodname from menuitem where foodtruckname ="''' + self.oldftname + '''";'''
        cursor.execute(query)
        self.menudata = cursor.fetchall()
        for i in self.menudata:
            self.setfood.append({"food": i["foodname"], "price": str(i["price"])})

        self.currentname = currenttags[0]
        self.currentstation = currenttags[1]
        self.currentstaff =currenttags[2]
        self.newfoods = currenttags[3]

        self.setModal(True)
        self.setWindowTitle("Update Food Truck")
        self.l1 = QLabel()
        self.l1.setText("Update Food Truck")

        self.l2 = QLabel()
        self.l2.setText("Name")
        self.newname = QLineEdit()
        cursor = connection.cursor()
        query = '''SELECT DISTINCT staff.username, CONCAT(user.firstName, " ", user.lastName) as staffname FROM staff JOIN user using(username) WHERE staff.foodTruckName is null;'''
        cursor.execute(query)
        staffdata = cursor.fetchall()
        connection.commit()
        for i in staffdata:
            self.availablestaff.append({"staffusername": i["username"], "staffname": i["staffname"]})

        self.l3 = QLabel()
        self.l3.setText("Station")
        self.stationcb = QComboBox()

        query = " call mn_filter_foodTruck_hascapacity;"

        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        query = "select stationname from mn_filter_foodTruck_remainingcapacity where capacity > 0;"
        cursor.execute(query)
        self.availablestations = cursor.fetchall()
        connection.commit()
        self.stationcb.addItem(self.oldstation)
        index = -1
        k = 1
        for i in range(0,len(self.availablestations)):
            self.stationcb.addItem(self.availablestations[i]["stationname"])
            if self.availablestations[i]["stationname"] == self.currentstation:
                index = k
            else:
                k+=1

        cursor = connection.cursor()
        query = "select * from food;"
        cursor.execute(query)
        connection.commit()


        self.datafood = cursor.fetchall()
        self.allfoods =[]
        for i in self.datafood:
            self.allfoods.append(i["foodName"])

        #CREATE THE STATION NAMES HERE
        if index == -1:
            pass
        else:
            self.stationcb.setCurrentIndex(index)

        self.l7 = QLabel()
        self.l7.setText("Assigned Staff")
        self.tablestaff =QTableWidget()
        self.tablestaff.setRowCount(len(self.currentstaff) + len(self.availablestaff))
        self.tablestaff.setColumnCount(1)
        header = self.tablestaff.horizontalHeader()
        vheader = self.tablestaff.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        self.tablestaff.horizontalHeader().hide()
        self.tablestaff.verticalHeader().hide()

        for i in range(0,len(self.initialstaff)):
            staff = QCheckBox(self.initialstaff[i]["staffname"])

            for k in self.currentstaff:
                if k["staffusername"] == self.initialstaff[i]["staffusername"]:
                    staff.setChecked(True)
            staff.stateChanged.connect(self.stafflist)
            self.tablestaff.setCellWidget(i, 0, staff)

        self.l4 = QLabel()
        self.l4.setText("MenuItem")
        self.table = QTableWidget()
        self.table.setRowCount(len(self.setfood)+len(self.newfoods)+1)
        self.table.setColumnCount(3)
        columns = ["Food", "Price", "Action"]
        self.table.setHorizontalHeaderLabels(columns)
        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().hide()
        self.createbutton = QPushButton("Update")
        self.createbutton.setEnabled(True)
        self.createbutton.clicked.connect(self.create)
         ### MUST HAVE FOOD TRUCK SELECTED

        cat = len(self.initialstaff)
        # FILL ASSIGNED STAFF
        for i in range(0,len(self.availablestaff)):
            staff = QCheckBox(self.availablestaff[i]["staffname"])
            for k in self.currentstaff:
                if k["staffusername"] == self.availablestaff[i]["staffusername"]:
                    staff.setChecked(True)
            staff.stateChanged.connect(self.stafflist)
            self.tablestaff.setCellWidget(i + cat, 0, staff)

        #FILL MENUITEM
        dog = len(self.newfoods) + len(self.setfood)

        for i in range(0,len(self.setfood)):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem((self.setfood[i]["food"])))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem((self.setfood[i]["price"])))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem("None"))
            pass

        for i in range(0 , len(self.newfoods)):
            k = len(self.setfood)
            remove = QPushButton("Remove")
            remove.clicked.connect(self.onClickDelete)
            self.table.setItem(k+i, 0, QtWidgets.QTableWidgetItem((self.newfoods[i]["food"])))
            self.table.setItem(k + i, 1, QtWidgets.QTableWidgetItem((self.newfoods[i]["price"])))

            self.table.setCellWidget(k+i, 2, remove)

        self.addlast= QPushButton("Add")
        self.addlast.clicked.connect(self.onClickAdd)
        self.addlast.setEnabled(False)
        self.addedfood = QComboBox()
        self.addedfood.currentTextChanged.connect(self.newtagdetection)
        self.addedprice = QLineEdit()
        self.addedprice.textChanged.connect(self.newtagdetection)
        self.table.setCellWidget(dog, 0, self.addedfood)
        self.table.setCellWidget(dog, 1, self.addedprice)
        self.table.setCellWidget(dog, 2, self.addlast)

        self.addedfood.currentIndexChanged.connect(self.newtagdetection)

        for i in self.setfood:
            if i["food"] in self.allfoods:
                self.allfoods.remove(i["food"])
        for i in self.newfoods:
            if i["food"] in self.allfoods:
                self.allfoods.remove(i["food"])
        for i in self.allfoods:
            self.addedfood.addItem(i)

        self.stationcb.currentTextChanged.connect(self.checkname)

        self.newname.setText(self.currentname)
        self.newname.textChanged.connect(self.checkname)

        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen4)
        hbox = QHBoxLayout()
        hbox.addWidget(self.l2)
        hbox.addWidget(self.newname)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.l3)
        hbox.addWidget(self.stationcb)

        vbox.addLayout(hbox)
        vbox.addWidget(self.l7)
        vbox.addWidget(self.tablestaff)
        vbox.addWidget(self.l4)
        vbox.addWidget(self.table)
        vbox.addWidget(self.createbutton)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def stafflist(self):

        rb = self.sender()
        ix = self.tablestaff.indexAt(rb.pos())
        self.staffindex = ix.row()
        name = self.tablestaff.cellWidget(self.staffindex,0).text()
        state = self.tablestaff.cellWidget(self.staffindex,0).checkState()
        if state == 2:
            for i in self.initialstaff:
                if i["staffname"] == name:
                    self.currentstaff.append(i)
            for i in self.availablestaff:
                if i["staffname"] == name:
                    self.currentstaff.append(i)
        if state== 0:
            for i in self.initialstaff:
                if i["staffname"] == name:
                    self.currentstaff.remove(i)
            for i in self.availablestaff:
                if i["staffname"] == name:
                    self.currentstaff.remove(i)

    def checkname(self):

        self.currentname = self.newname.text()
        if self.newname.text() == "" or self.stationcb.currentText() =="" or len(self.currentstaff) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def checkdesc(self):
        self.currentdescription = self.description.toPlainText()
        if self.newname.text() == "" or self.description.toPlainText() == "" or len(self.currenttags) == 0:
            self.createbutton.setEnabled(False)
        else:
            self.createbutton.setEnabled(True)

    def newtagdetection(self):
         if self.addedprice.text() == "" or self.addedfood.currentText() == "":
             self.addlast.setEnabled(False)
         else:
             self.addlast.setEnabled(True)

    def onClickDelete(self):
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()
        for i in range(0, len(self.newfoods)):
            if self.newfoods[i]["food"] == self.table.item(self.foodtruckindex, 0).text():
                del self.newfoods[i]
                break

        screenreload = UpdateFoodTruck13(self.username, self.loginrole, self.oldftname, self.oldstation, self.initialstaff,
                                       [self.newname.text(), self.stationcb.currentText(), self.currentstaff, self.newfoods])
        self.close()
        screenreload.exec()

    def onClickAdd(self):
        self.newfoods.append({"food":self.table.cellWidget(len(self.newfoods) + len(self.setfood), 0).currentText(), "price":self.table.cellWidget(len(self.newfoods) + len(self.setfood), 1).text()})
        screenreload = UpdateFoodTruck13(self.username, self.loginrole, self.oldftname, self.oldstation,
                                       self.initialstaff,
                                       [self.currentname, self.currentstation, self.currentstaff, self.newfoods])
        self.close()
        screenreload.exec()

    def create(self):
        for k in self.initialstaff:
            try:
                if k in self.currentstaff:
                    pass
                else:
                    cursor = connection.cursor()

                    query = '''update staff set foodtruckname = null where username = "''' + k["staffusername"] + '''";'''
                    cursor.execute(query)
                    connection.commit()
            except:
                pass

        for k in self.availablestaff:
            try:
                if k in self.currentstaff:
                    cursor = connection.cursor()

                    query = '''update staff set foodtruckname = "''' + self.oldftname+'''" where username = "''' + k["staffusername"] + '''";'''
                    cursor.execute(query)
                    connection.commit()

                else:
                    pass
            except:
                pass

        for i in self.newfoods:
            try:
                cursor = connection.cursor()

                query = '''insert into menuitem(price, foodTruckName, foodName) values(''' + i["price"] + ''', "''' + self.oldftname + '''", "''' + i["food"] + '''");'''
                cursor.execute(query)
                connection.commit()
            except:
                pass
        try:
            cursor = connection.cursor()

            query = '''Update foodtruck set stationname = "''' + self.stationcb.currentText() +'''" where foodtruckname ="''' + self.oldftname +'''";'''
            cursor.execute(query)
            connection.commit()
        except:
            query = self.currentstation

        try:
            cursor = connection.cursor()
            query = '''Update foodtruck set foodtruckname = "''' + self.currentname + '''" where foodtruckname ="''' + self.oldftname + '''";'''
            cursor.execute(query)
            connection.commit()
        except:
            pass
        screen11 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen11.exec()

    def screen4(self):
        screen11 = ManageFoodTruck11(self.username, self.loginrole)
        self.close()
        screen11.exec()

class FoodTruckSummary14(QDialog):
    def __init__(self, username, loginrole):
        super(FoodTruckSummary14, self).__init__()
        self.var = 0
        self.username = username
        self.cursor = connection.cursor()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Food Truck Summary")
        self.l1 = QLabel("Food Truck Summary")
        self.l1.setAlignment(Qt.AlignCenter)
        self.contains_label = QLabel("Food Truck Name (contains)")
        self.station_label = QLabel("Station Name")
        self.date_beg_label = QLabel("Date")
        self.date_dash_label = QLabel("——")

        self.contains = QLineEdit()
        self.station = QComboBox()
        self.station.addItem("None")

        self.cursor.execute("SELECT stationName from station")
        self.result = self.cursor.fetchall()

        for line in self.result:
            self.station.addItem(line["stationName"])

        self.date_beg = QLineEdit()
        self.date_end = QLineEdit()

        self.filter = QPushButton("Filter")
        self.filter.clicked.connect(self.filter_result)

        self.ViewD = QPushButton("View Detail")
        self.ViewD.clicked.connect(self.VD)

        #creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.clicked.connect(self.BackHome)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.l1)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.contains_label)
        self.hbox.addWidget(self.contains)
        self.hbox.addWidget(self.station_label)
        self.hbox.addWidget(self.station)
        self.vbox.addLayout(self.hbox)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.date_beg_label)
        self.hbox.addWidget(self.date_beg)
        self.hbox.addWidget(self.date_dash_label)
        self.hbox.addWidget(self.date_end)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.filter)
        self.vbox.addWidget(self.ViewD)
        self.vbox.addWidget(self.GoHome)

        query = f"CALL mn_filter_summary('{self.username}', null, null, null, null, null, null)"
        self.cursor.execute(query)
        self.cursor.execute(f"SELECT DISTINCT * FROM mn_filter_summary_result;")
        result = self.cursor.fetchall()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setRowCount(len(result))
        self.table_widget.setHorizontalHeaderLabels(["Food Truck Name", "# Total Order", "Total Revenue", "# Customer"])
        header = self.table_widget.horizontalHeader()
        vheader = self.table_widget.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setVisible(False)
        self.table_widget.setSortingEnabled(True)

        for i in range(len(result)):
            rb = QRadioButton("", parent=self.table_widget)
            self.table_widget.setCellWidget(i, 0, rb)
            self.table_widget.setItem(i, 0, QTableWidgetItem("     " + str(list(result[i].values())[0])))
            rb.clicked.connect(self.onStateChanged)
            for j in range(1, 4):
                b = QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(str(list(result[i].values())[j])))
                self.table_widget.setItem(i, j, b)

        self.vbox.addWidget(self.table_widget)
        self.setLayout(self.vbox)

    def filter_result(self):
        try:
            self.vbox.removeWidget(self.table_widget)
            sip.delete(self.table_widget)
            self.table_widget = None
        except:
            pass

        if self.station.currentText() == "None":
            station = "null"
        else:
            station = f"'{self.station.currentText()}'"

        if (not self.contains.text()):
            contains = "null"
        else:
            contains = f"'{self.contains.text()}'"

        if (not self.date_beg.text()):
            beg = "null"
        else:
            beg = f"'{self.date_beg.text()}'"

        if (not self.date_end.text()):
            end = "null"
        else:
            end = f"'{self.date_end.text()}'"

        query = f"CALL mn_filter_summary('{self.username}', {contains}, {station}, {beg}, {end}, null, null)"
        self.cursor.execute(query)
        self.cursor.execute(f"SELECT DISTINCT * FROM mn_filter_summary_result;")
        result = self.cursor.fetchall()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setRowCount(len(result))
        self.table_widget.setHorizontalHeaderLabels(["Food Truck Name", "# Total Order", "Total Revenue", "# Customer"])
        header = self.table_widget.horizontalHeader()
        vheader = self.table_widget.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setVisible(False)
        self.table_widget.setSortingEnabled(True)

        for i in range(len(result)):
            rb = QRadioButton("", parent=self.table_widget)
            self.table_widget.setCellWidget(i, 0, rb)
            self.table_widget.setItem(i, 0, QTableWidgetItem("     " + str(list(result[i].values())[0])))
            rb.clicked.connect(self.onStateChanged)
            for j in range(1, 4):
                b = QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(str(list(result[i].values())[j])))
                self.table_widget.setItem(i, j, b)

        self.vbox.addWidget(self.table_widget)
        self.setLayout(self.vbox)

    def onStateChanged(self):
        rb = self.sender()
        ix = self.table_widget.indexAt(rb.pos())
        self.foodtruckindex = ix.row()
        self.truck = self.table_widget.item(self.foodtruckindex, 0).text().strip()

    def VD(self):
        foodtruckname15 = self.truck
        screen15 = SummaryDetail15(self.username, self.loginrole, foodtruckname15)
        self.cursor.close()
        self.close()
        screen15.exec()

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class SummaryDetail15(QDialog):
    def __init__(self, username, loginrole, foodtruckname):
        super(SummaryDetail15, self).__init__()
        self.cursor = connection.cursor()
        self.username = username
        self.loginrole = loginrole
        self.foodtruckname = foodtruckname
        self.setModal(True)
        self.setWindowTitle("Summary Detail")
        self.l1 = QLabel("Summary Detail")
        self.l1.setAlignment(Qt.AlignCenter)
        self.name_label = QLabel("Food Truck Name")
        self.name = QLabel(self.foodtruckname)

        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen14)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        hbox = QHBoxLayout()
        hbox.addWidget(self.name_label)
        hbox.addWidget(self.name)
        vbox.addLayout(hbox)
        vbox.addWidget(self.GoHome)

        try:
            self.vbox.removeWidget(self.table_widget)
            sip.delete(self.table_widget)
            self.table_widget = None
        except:
            pass

        query = f"CALL mn_summary_detail('{self.username}', '{self.foodtruckname}')"
        self.cursor.execute(query)
        self.cursor.execute(f"SELECT DISTINCT * FROM mn_summary_detail_result;")
        result = self.cursor.fetchall()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setRowCount(len(result))
        self.table_widget.setHorizontalHeaderLabels(["Date", "Customer", "Total Purchase", "# Orders", "Food(s)"])
        header = self.table_widget.horizontalHeader()
        vheader = self.table_widget.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setVisible(False)
        self.table_widget.setSortingEnabled(True)

        for i in range(len(result)):
            for j in range(5):
                b = QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(str(list(result[i].values())[j])))
                self.table_widget.setItem(i, j, b)

        vbox.addWidget(self.table_widget)
        self.setLayout(vbox)

    def screen14(self):
        screen14 = FoodTruckSummary14(self.username, self.loginrole)
        self.cursor.close()
        self.close()
        screen14.exec()

class Explore16(QDialog):
    def __init__(self, username, loginrole):
        super(Explore16, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Explore")
        self.l1 = QLabel()
        self.l1.setText("Explore")
        self.cursor = connection.cursor()

        self.buildingtext = QLabel("Building Name")

        self.buildinglist = QComboBox()
        self.buildinglist.addItem("None")
        self.cursor.execute("SELECT buildingName from building")
        self.result = self.cursor.fetchall()
        for line in self.result:
            self.buildinglist.addItem(line["buildingName"])

        self.stationtext = QLabel("Station Name")

        self.stationlist = QComboBox()
        self.stationlist.addItem("None")
        self.cursor.execute("SELECT stationName from station")
        self.result = self.cursor.fetchall()
        for line in self.result:
            self.stationlist.addItem(line["stationName"])

        self.buildingtagtext = QLabel("Building Tag (contain)")

        self.buildingtagbox = QLineEdit()

        self.foodtrucknametext = QLabel("Food Truck Name (contain)")

        self.foodtrucknamebox = QLineEdit()

        self.foodnametext = QLabel("Food (contain)")

        self.foodnamebox = QLineEdit()

        self.filterbutton = QPushButton("Filter")
        self.filterbutton.clicked.connect(self.filter_result)

        self.selectlocation = QPushButton("Select As Current Location")
        self.selectlocation.clicked.connect(self.SelectAsLocation)

        # creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)

        query = f"CALL cus_filter_explore(NULL, NULL, NULL, NULL, NULL)"
        self.cursor.execute(query)
        self.cursor.execute(f"SELECT DISTINCT * FROM cus_filter_explore_result;")
        result = self.cursor.fetchall()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setRowCount(len(result))
        self.table_widget.setHorizontalHeaderLabels(["Station", "Building", "Food Truck(s)", "Food(s)"])
        header = self.table_widget.horizontalHeader()
        vheader = self.table_widget.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setVisible(False)
        self.table_widget.setSortingEnabled(False)

        for i in range(len(result)):
            rb = QRadioButton("", parent=self.table_widget)
            self.table_widget.setCellWidget(i, 0, rb)
            self.table_widget.setItem(i, 0, QTableWidgetItem("     " + str(list(result[i].values())[0])))
            rb.clicked.connect(self.onStateChanged)
            for j in range(1, 4):
                b = QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(str(list(result[i].values())[j])))
                self.table_widget.setItem(i, j, b)

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.buildingtext)
        self.hbox.addWidget(self.buildinglist)
        self.hbox.addWidget(self.stationtext)
        self.hbox.addWidget(self.stationlist)
        self.vbox.addLayout(self.hbox)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.buildingtagtext)
        self.hbox.addWidget(self.buildingtagbox)
        self.hbox.addWidget(self.foodtrucknametext)
        self.hbox.addWidget(self.foodtrucknamebox)
        self.vbox.addLayout(self.hbox)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.foodnametext)
        self.hbox.addWidget(self.foodnamebox)
        self.vbox.addLayout(self.hbox)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.filterbutton)
        self.vbox.addLayout(self.hbox)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.GoHome)
        self.hbox.addWidget(self.selectlocation)
        self.vbox.addLayout(self.hbox)
        self.hbox = QHBoxLayout()
        self.vbox.addWidget(self.table_widget)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def filter_result(self):

        try:
            self.vbox.removeWidget(self.table_widget)
            sip.delete(self.table_widget)
            self.table_widget = None
        except:
            pass

        if self.buildinglist.currentText() == "None":
            building = "null"
        else:
            building = f"'{self.buildinglist.currentText()}'"

        if self.stationlist.currentText() == "None":
            station = "null"
        else:
            station = f"'{self.stationlist.currentText()}'"

        if (not self.buildingtagbox.text()):
            buildingtag = "null"
        else:
            buildingtag = f"'{self.buildingtagbox.text()}'"

        if (not self.foodtrucknamebox.text()):
            foodtruckname = "null"
        else:
            foodtruckname = f"'{self.foodtrucknamebox.text()}'"

        if (not self.foodnamebox.text()):
            foodname = "null"
        else:
            foodname = f"'{self.foodnamebox.text()}'"

        query = f"CALL cus_filter_explore({building}, {station}, {buildingtag}, {foodtruckname}, {foodname})"
        self.cursor.execute(query)
        self.cursor.execute(f"SELECT DISTINCT * FROM cus_filter_explore_result;")
        result = self.cursor.fetchall()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setRowCount(len(result))
        self.table_widget.setHorizontalHeaderLabels(["Station", "Building", "Food Truck(s)", "Food(s)"])
        header = self.table_widget.horizontalHeader()
        vheader = self.table_widget.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setVisible(False)
        self.table_widget.setSortingEnabled(False)

        for i in range(len(result)):
            rb = QRadioButton("", parent=self.table_widget)
            self.table_widget.setCellWidget(i, 0, rb)
            self.table_widget.setItem(i, 0, QTableWidgetItem("     " + str(list(result[i].values())[0])))
            rb.clicked.connect(self.onStateChanged)
            for j in range(1, 4):
                b = QTableWidgetItem()
                b.setData(QtCore.Qt.EditRole, QtCore.QVariant(str(list(result[i].values())[j])))
                self.table_widget.setItem(i, j, b)

        self.vbox.addWidget(self.table_widget)
        self.setLayout(self.vbox)

    def onStateChanged(self):
        rb = self.sender()
        ix = self.table_widget.indexAt(rb.pos())
        self.stationindex = ix.row()
        self.station = self.table_widget.item(self.stationindex, 0).text().strip()

    def SelectAsLocation(self):
        query = f"CALL cus_select_location('{self.username}', '{self.station}')"
        self.cursor.execute(query)
        connection.commit()

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class CurrentInfo17B(QDialog):
    def __init__(self, username, loginrole):
        super(CurrentInfo17B, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Current Information")
        self.l1 = QLabel()
        self.l1.setText("Current Information")
        cursor = connection.cursor()
        query  = '''select balance from customer where username = "''' + self.username + '''";'''
        cursor.execute(query)
        data = cursor.fetchall()

        ### MUST HAVE FOOD TRUCK SELECTED##

        self.l2 = QLabel()
        self.stationname = "None"
        l2text = "Station:   " + self.stationname
        self.l2.setText(l2text)

        self.l3 = QLabel()
        self.buildingname = "None"
        l3text = "Building:   " + self.buildingname
        self.l3.setText(l3text)

        self.l4 = QLabel()
        self.tagnames = "None"
        l4text = "Building Tag(s):   " + self.tagnames
        self.l4.setText(l4text)

        self.l5 = QLabel()
        self.buildingdescription = "None"
        l5text = "Building Description:   " + self.buildingdescription
        self.l5.setText(l5text)

        self.l6 = QLabel()
        self.balance = str(data[0]["balance"])
        l6text = "Balance:   " + self.balance
        self.l6.setText(l6text)

        #creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l2)
        vbox.addWidget(self.l3)
        vbox.addWidget(self.l4)
        vbox.addWidget(self.l5)
        vbox.addWidget(self.l6)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class CurrentInfo17(QDialog):
    def __init__(self, username, loginrole):
        super(CurrentInfo17, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Current Information")
        self.l1 = QLabel()
        self.l1.setText("Current Information")
        self.foodtruckindex = None

        cursor = connection.cursor()
        cursor.execute('''call cus_current_information_basic("''' + self.username + '''");''')
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("SELECT * from cus_current_information_basic_result")
        data = cursor.fetchall()

        cursor = connection.cursor()
        cursor.execute('''call cus_current_information_foodTruck("''' + self.username + '''");''')
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("SELECT * from cus_current_information_foodTruck_result")
        self.data2 = cursor.fetchall()
        connection.commit()

        ### MUST HAVE FOOD TRUCK SELECTED##
        self.Order = QPushButton("Order")
        self.Order.setEnabled(False)
        self.Order.clicked.connect(self.OrderItem)

        self.l2 = QLabel()
        self.stationname = data[0]["stationName"]
        l2text = "Station:   " + self.stationname
        self.l2.setText(l2text)

        self.l3 = QLabel()
        self.buildingname = data[0]["buildingName"]
        l3text = "Building:   " + self.buildingname
        self.l3.setText(l3text)

        self.l4 = QLabel()
        self.tagnames = data[0]["tags"]
        l4text = "Building Tag(s):   " + self.tagnames
        self.l4.setText(l4text)

        self.l5 = QLabel()
        self.buildingdescription = data[0]["description"]
        l5text = "Building Description:   " + self.buildingdescription
        self.l5.setText(l5text)

        self.l6 = QLabel()
        self.balance = str(data[0]["balance"])
        l6text = "Balance:   " + self.balance
        self.l6.setText(l6text)

        self.table = QtWidgets.QTableWidget()
        #make this based of length of SQL Query
        self.table.setRowCount(len(self.data2))
        self.table.setColumnCount(3)
        columns = ["Food Truck", "Manager", "Food(s)"]
        self.table.setHorizontalHeaderLabels(columns)

        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            rb = QtWidgets.QRadioButton(self.data2[i]["foodTruckName"], parent=self.table)
            rb.clicked.connect(self.onStateChanged)
            self.table.setCellWidget(i, 0, rb)
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(self.data2[i]["managerName"]))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(self.data2[i]["foodNames"]))

        # creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.l2)
        vbox.addWidget(self.l3)
        vbox.addWidget(self.l4)
        vbox.addWidget(self.l5)
        vbox.addWidget(self.l6)
        vbox.addWidget(self.table)
        vbox.addWidget(self.Order)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def OrderItem(self):
        foodtrucktoorderfrom = self.data2[self.foodtruckindex]["foodTruckName"]
        screen18 = PlaceOrder18(self.username, self.loginrole,foodtrucktoorderfrom)
        self.close()
        screen18.exec()

    def onStateChanged(self):
        self.Order.setEnabled(True)
        rb = self.sender()
        ix = self.table.indexAt(rb.pos())
        self.foodtruckindex = ix.row()

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class PlaceOrder18(QDialog):
    def __init__(self, username, loginrole, foodtruckname):
        super(PlaceOrder18, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.resultschecked ={}
        self.resultsquantity = {}
        self.foodtruckname = foodtruckname
        self.setModal(True)
        self.date = str(datetime.date.today())
        cursor = connection.cursor()
        query = '''select price, foodName from MenuItem where foodtruckname ="''' + self.foodtruckname +'''";'''
        cursor.execute(query)

        self.data = cursor.fetchall()
        self.setWindowTitle("Customer Order")
        self.l1 = QLabel()
        self.l1.setText("Order")
        self.l2 = QLabel()
        foodtruckstring = "Food Truck:     " + foodtruckname
        self.l2.setText(foodtruckstring)
        self.l3 = QLabel()
        self.l3.setText("Date (YYYY-MM-DD):")
        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(3)
        columns = ["Food", "Price", "Purchase Quantity"]
        self.table.setHorizontalHeaderLabels(columns)
        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            ch = QtWidgets.QCheckBox(parent=self.table)
            ch.clicked.connect(self.onStateChanged)
            ch.setText(self.data[i]["foodName"])
            le = QLineEdit(parent =self.table)
            self.resultschecked[i] = False
            le.setValidator(QtGui.QIntValidator(1,99999))
            le.setText("0")
            le.textChanged.connect(self.onStateChangedle)
            self.table.setCellWidget(i, 2, le)
            self.table.setCellWidget(i, 0, ch)
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.data[i]["price"])))
            self.resultsquantity[i] = 0

        self.dateselected = QLineEdit()
        self.dateselected.setText(self.date)
        self.dateselected.textChanged.connect(self.change_date)

        ### MUST HAVE FOOD TRUCK SELECTED
        #goes back to current information
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.screen17)

        self.Submit = QPushButton("Submit")
        self.Submit.setEnabled(True)
        self.Submit.clicked.connect(self.submitO)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.l2)
        vbox.addWidget(self.table)
        vbox.addWidget(self.l3)
        vbox.addWidget(self.dateselected)
        vbox.addWidget(self.Submit)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def onStateChangedle(self):
        le = self.sender()
        ix = self.table.indexAt(le.pos())
        self.resultsquantity[ix.row()] = le.text()

    def onStateChanged(self):
        ch = self.sender()
        ix = self.table.indexAt(ch.pos())
        self.resultschecked[ix.row()] = ch.isChecked()

    def submitO(self):
        try:
            datetotest = self.date
            datetime_object = datetime.datetime.strptime(datetotest, '%Y-%m-%d').date()
            confirmation = False
            for i in range(0, len(self.data)):
                if self.resultschecked[i] == True and not (str(self.resultsquantity[i]) == "0"):
                    confirmation = True

            if confirmation:
                cursor = connection.cursor()
                query = '''call cus_order("''' + self.date + '''", "''' + self.username + '''");'''
                query2 = '''select max(orderID) from Orders where customerusername = "''' + self.username + '''";'''
                cursor.execute(query)
                connection.commit()
                cursor2 = connection.cursor()
                cursor2.execute(query2)
                orderID = str(cursor2.fetchall()[0]["max(orderID)"])
                # cursor.execute(query)
                for i in range(0, len(self.data)):
                    if self.resultschecked[i] == True:
                        food = self.data[i]["foodName"]
                        qty = str(self.resultsquantity[i])
                        query3 = '''CALL cus_add_item_to_order("''' + self.foodtruckname + '''", "''' + food + '''", ''' + qty + ''', ''' + orderID + ''');'''
                        cursor3 = connection.cursor()
                        cursor3.execute(query3)
                        connection.commit()
                        pass
                    else:
                        pass

                screen18 = PlaceOrder18(self.username, self.loginrole, self.foodtruckname)

                self.close()
                screen18.exec()
            else:
                pass
        except ValueError:
            self.dateselected.setText(str(datetime.date.today()))
            pass

    def change_date(self):
        self.date = self.dateselected.text()

    def screen17(self):
        screen17 = CurrentInfo17(self.username, self.loginrole)
        self.close()
        screen17.exec()

class OrderHistory19(QDialog):
    def __init__(self, username, loginrole):
        super(OrderHistory19, self).__init__()
        self.username = username
        self.loginrole = loginrole
        self.setModal(True)
        self.setWindowTitle("Customer Order History")
        self.l1 = QLabel()
        self.l1.setText("Order History")

        cursor = connection.cursor()
        query = '''call cus_order_history("'''+ self.username + '''");'''
        cursor.execute(query)
        connection.commit()
        query2 = '''select * from cus_order_history_result;'''
        cursor2 = connection.cursor()
        cursor2.execute(query2)
        self.data = cursor2.fetchall()

        self.table = QtWidgets.QTableWidget()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(5)
        columns = ["Date", "OrderID", "Order Total", "Food(s)", "Food Quantity"]
        self.table.setHorizontalHeaderLabels(columns)
        header = self.table.horizontalHeader()
        vheader = self.table.verticalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        vheader.setSectionResizeMode(QHeaderView.Stretch)

        for i in range(self.table.rowCount()):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(self.data[i]["date"])))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.data[i]["orderID"])))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(self.data[i]["orderTotal"])))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(self.data[i]["foodNames"])))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(self.data[i]["foodQuantity"])))

        #creates standard back home button based on usertype
        self.GoHome = QPushButton("Back")
        self.GoHome.setEnabled(True)
        self.GoHome.clicked.connect(self.BackHome)
        vbox = QVBoxLayout()
        vbox.addWidget(self.l1)
        vbox.addWidget(self.table)
        vbox.addWidget(self.GoHome)
        self.setLayout(vbox)

    def BackHome(self):
        logintype = self.loginrole
        if logintype == 'Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff':
            home = HomeScreenStaff(self.username, self.loginrole)
            self.close()
            home.exec ()
        elif logintype == 'Admin':
            home = HomeScreenAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Manager':
            home = HomeScreenManager(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Admin-Customer':
            home = HomeScreenCustomerAdmin(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype == 'Staff-Customer':
            home = HomeScreenCustomer(self.username, self.loginrole)
            self.close()
            home.exec()
        elif logintype ==  'Manager-Customer':
            home = HomeScreenCustomerManager(self.username, self.loginrole)
            self.close()
            home.exec()

class DbLoginDialog(QDialog):

    def __init__(self):
        super(DbLoginDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Login to MySQL Server")

        self.host = QLineEdit("localhost")
        self.user = QLineEdit("root")
        self.password = QLineEdit()
        self.db = QLineEdit("cs4400spring2020")

        form_group_box = QGroupBox("MySQL Server Login Credentials")
        layout = QFormLayout()
        layout.addRow(QLabel("Host:"), self.host)
        layout.addRow(QLabel("User:"), self.user)
        layout.addRow(QLabel("Password:"), self.password)
        layout.addRow(QLabel("Database:"), self.db)
        form_group_box.setLayout(layout)

        # Consider these 3 lines boiler plate for a standard Ok | Cancel dialog
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(form_group_box)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)
        self.password.setFocus()

class TableDialog(QDialog):
    def __init__(self, column_headers, rows):
        super(TableDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("")

        table = QTableWidget(len(rows), len(rows[0]), self)
        table.setHorizontalHeaderLabels(column_headers)
        for i, row in enumerate(rows):
            for j, field in enumerate(row):
                item = QTableWidgetItem(field)
                table.setItem(i, j, item)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(table)
        vbox_layout.addWidget(buttons)
        self.setLayout(vbox_layout)

class MainWindow(QWidget):

    def __init__(self, db):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MySQL Browser")
        cursor = connection.cursor()
        cursor.execute("show tables")
        vbox_layout = QVBoxLayout()
        for row in cursor:
            table = row[f"Tables_in_{db}"]
            vbox_layout.addWidget(self.make_button(db, table))
        self.setLayout(vbox_layout)

    def make_button(self, db, table):
        button = QPushButton(table, self)
        button.clicked.connect(lambda: self.display(db, table))
        return button

    def display(self, db, table):
        curs = connection.cursor()
        query = f"select * from {table}"
        curs.execute(query)
        rows = []
        first_row = curs.fetchone()
        column_headers = [str(k).strip() for k, v in first_row.items()]
        rows.append([str(v).strip() for k, v in first_row.items()])
        for row in curs:
            rows.append([str(v).strip() for k, v in row.items()])

        dlg = TableDialog(column_headers, rows)
        dlg.exec()

if __name__=='__main__':
    app = QApplication(sys.argv)
    login = DbLoginDialog()

    # This is how you check which button the user used to dismiss the dialog.
    if login.exec() == QDialog.Accepted:
        # connection is global so we can use it in any class, function, or method
        # defined in this module
        global connection
        try:
            connection = pymysql.connect(host=login.host.text(),
                                         user=login.user.text(),
                                         password=login.password.text(),
                                         db=login.db.text(),
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print(f"Couldn't log {login.user.text()} in to MySQL server on {login.host.text()}")
            print(e)
            qApp.quit()
            sys.exit()
        login = LoginScreen()
        login.exec()
        sys.exit(app.exec_())