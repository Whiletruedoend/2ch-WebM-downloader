# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 710)
        Dialog.setWhatsThis("")
        Dialog.setStyleSheet("")
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(20, 610, 151, 41))
        self.startButton.setMinimumSize(QtCore.QSize(10, 10))
        self.startButton.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(16)
        self.startButton.setFont(font)
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.startButton.setStyleSheet("color:#008000;")
        self.startButton.setCheckable(False)
        self.startButton.setObjectName("startButton")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setEnabled(True)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 441, 401))
        self.textBrowser.setObjectName("textBrowser")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 670, 451, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressText = QtWidgets.QLabel(Dialog)
        self.progressText.setGeometry(QtCore.QRect(190, 607, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progressText.setFont(font)
        self.progressText.setObjectName("progressText")
        self.progressCount = QtWidgets.QLabel(Dialog)
        self.progressCount.setGeometry(QtCore.QRect(190, 627, 91, 31))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(8)
        self.progressCount.setFont(font)
        self.progressCount.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.progressCount.setLineWidth(0)
        self.progressCount.setTextFormat(QtCore.Qt.RichText)
        self.progressCount.setScaledContents(False)
        self.progressCount.setWordWrap(False)
        self.progressCount.setIndent(0)
        self.progressCount.setObjectName("progressCount")
        self.stopButton = QtWidgets.QPushButton(Dialog)
        self.stopButton.setGeometry(QtCore.QRect(290, 610, 151, 41))
        self.stopButton.setMinimumSize(QtCore.QSize(10, 10))
        self.stopButton.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("8514oem")
        font.setPointSize(16)
        self.stopButton.setFont(font)
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.stopButton.setAutoFillBackground(False)
        self.stopButton.setStyleSheet("color:#FF0000")
        self.stopButton.setCheckable(False)
        self.stopButton.setObjectName("stopButton")
        self.hideInTray = QtWidgets.QCheckBox(Dialog)
        self.hideInTray.setGeometry(QtCore.QRect(340, 480, 101, 17))
        self.hideInTray.setObjectName("hideInTray")
        self.optionsText = QtWidgets.QLabel(Dialog)
        self.optionsText.setGeometry(QtCore.QRect(170, 420, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.optionsText.setFont(font)
        self.optionsText.setObjectName("optionsText")
        self.webmText = QtWidgets.QLabel(Dialog)
        self.webmText.setGeometry(QtCore.QRect(40, 450, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.webmText.setFont(font)
        self.webmText.setObjectName("webmText")
        self.outputText = QtWidgets.QLabel(Dialog)
        self.outputText.setGeometry(QtCore.QRect(190, 450, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.outputText.setFont(font)
        self.outputText.setObjectName("outputText")
        self.otherText = QtWidgets.QLabel(Dialog)
        self.otherText.setGeometry(QtCore.QRect(360, 450, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.otherText.setFont(font)
        self.otherText.setObjectName("otherText")
        self.alreadyDownloaded = QtWidgets.QCheckBox(Dialog)
        self.alreadyDownloaded.setGeometry(QtCore.QRect(160, 480, 141, 21))
        self.alreadyDownloaded.setObjectName("alreadyDownloaded")
        self.clearAfterDownload = QtWidgets.QCheckBox(Dialog)
        self.clearAfterDownload.setGeometry(QtCore.QRect(160, 506, 161, 21))
        self.clearAfterDownload.setObjectName("clearAfterDownload")
        self.differentPaths = QtWidgets.QCheckBox(Dialog)
        self.differentPaths.setGeometry(QtCore.QRect(15, 480, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.differentPaths.setFont(font)
        self.differentPaths.setObjectName("differentPaths")
        self.nonStop = QtWidgets.QCheckBox(Dialog)
        self.nonStop.setGeometry(QtCore.QRect(340, 506, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.nonStop.setFont(font)
        self.nonStop.setObjectName("nonStop")
        self.mp4Download = QtWidgets.QCheckBox(Dialog)
        self.mp4Download.setGeometry(QtCore.QRect(15, 506, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.mp4Download.setFont(font)
        self.mp4Download.setObjectName("mp4Download")
        self.saveLikeName = QtWidgets.QCheckBox(Dialog)
        self.saveLikeName.setGeometry(QtCore.QRect(15, 532, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.saveLikeName.setFont(font)
        self.saveLikeName.setObjectName("saveLikeName")
        self.rememberHashes = QtWidgets.QCheckBox(Dialog)
        self.rememberHashes.setGeometry(QtCore.QRect(15, 558, 311, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.rememberHashes.setFont(font)
        self.rememberHashes.setObjectName("rememberHashes")
        self.textConlinueLOL = QtWidgets.QLabel(Dialog)
        self.textConlinueLOL.setGeometry(QtCore.QRect(16, 574, 151, 16))
        self.textConlinueLOL.setObjectName("textConlinueLOL")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "WebM Downloader v1.0"))
        self.startButton.setText(_translate("Dialog", "Start"))
        self.progressText.setText(_translate("Dialog", "Прогресс:"))
        self.progressCount.setText(_translate("Dialog", "   --/--"))
        self.stopButton.setText(_translate("Dialog", "Stop"))
        self.hideInTray.setText(_translate("Dialog", "Скрыть в трее"))
        self.optionsText.setText(_translate("Dialog", "Настройки"))
        self.webmText.setText(_translate("Dialog", "Файлы"))
        self.outputText.setText(_translate("Dialog", "Вывод"))
        self.otherText.setText(_translate("Dialog", "Общее"))
        self.alreadyDownloaded.setText(_translate("Dialog", "Существующие WebM"))
        self.clearAfterDownload.setText(_translate("Dialog", "Очистка при остановке"))
        self.differentPaths.setText(_translate("Dialog", "Всё в одной папке?"))
        self.nonStop.setText(_translate("Dialog", "Non-stop?"))
        self.mp4Download.setText(_translate("Dialog", "Загружать .mp4?"))
        self.saveLikeName.setText(_translate("Dialog", "Сохранять по имени?"))
        self.rememberHashes.setText(_translate("Dialog", "Запоминать и не скачивать"))
        self.textConlinueLOL.setText(_translate("Dialog", "в дальнейшем эти файлы"))

