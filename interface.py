# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(600, 400)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.labelNom = QLabel(self.centralwidget)
        self.labelNom.setObjectName(u"labelNom")
        self.labelNom.setGeometry(QRect(50, 50, 100, 30))
        self.lineEditNom = QLineEdit(self.centralwidget)
        self.lineEditNom.setObjectName(u"lineEditNom")
        self.lineEditNom.setGeometry(QRect(160, 50, 200, 30))
        self.labelPrenom = QLabel(self.centralwidget)
        self.labelPrenom.setObjectName(u"labelPrenom")
        self.labelPrenom.setGeometry(QRect(50, 100, 100, 30))
        self.lineEditPrenom = QLineEdit(self.centralwidget)
        self.lineEditPrenom.setObjectName(u"lineEditPrenom")
        self.lineEditPrenom.setGeometry(QRect(160, 100, 200, 30))
        self.labelNumero = QLabel(self.centralwidget)
        self.labelNumero.setObjectName(u"labelNumero")
        self.labelNumero.setGeometry(QRect(50, 150, 100, 30))
        self.lineEditNumero = QLineEdit(self.centralwidget)
        self.lineEditNumero.setObjectName(u"lineEditNumero")
        self.lineEditNumero.setGeometry(QRect(160, 150, 200, 30))
        self.pushButtonAjouter = QPushButton(self.centralwidget)
        self.pushButtonAjouter.setObjectName(u"pushButtonAjouter")
        self.pushButtonAjouter.setGeometry(QRect(160, 200, 100, 40))
        self.labelResultat = QLabel(self.centralwidget)
        self.labelResultat.setObjectName(u"labelResultat")
        self.labelResultat.setGeometry(QRect(50, 260, 500, 60))
        self.labelResultat.setWordWrap(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 600, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Application Etudiant - Carte", None))
        self.labelNom.setText(QCoreApplication.translate("MainWindow", u"Nom :", None))
        self.labelPrenom.setText(QCoreApplication.translate("MainWindow", u"Prenom :", None))
        self.labelNumero.setText(QCoreApplication.translate("MainWindow", u"N° Carte :", None))
        self.pushButtonAjouter.setText(QCoreApplication.translate("MainWindow", u"Ajouter", None))
        self.labelResultat.setText(QCoreApplication.translate("MainWindow", u"Pret a ajouter un etudiant...", None))
    # retranslateUi