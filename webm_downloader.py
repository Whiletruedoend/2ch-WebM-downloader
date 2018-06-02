# -*- coding: utf-8 -*-

#############################################################

host = "https://2ch.hk/" # Сайт для парсинга
board = "b" # Доска для парсинга webm, в данном случае /b/

#############################################################

import sys  # sys нужен для передачи argv в QApplication

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QMessageBox, QCheckBox, QSystemTrayIcon, \
	QSpacerItem, QSizePolicy, QMenu, QAction, QStyle, qApp

from PyQt5.QtCore import pyqtSignal, QObject, QThread, QSize
from PyQt5.QtGui import QIcon

import webm_menu  # Это наш конвертированный файл дизайна

import gevent
from gevent import monkey
monkey.patch_all()

import queue
import requests
import time
from time import strftime, localtime
import string, random

from urllib.request import urlopen
from urllib.parse import urljoin
import os, posixpath
import json, re
import sqlite3

class GetPostsThread( QThread ):

	threadSignal = pyqtSignal(str)
	progressSignal = pyqtSignal(int)
	LenSignal = pyqtSignal(int)
	ResBut = pyqtSignal(int)

	def __init__( self, CheckBox ):
		super().__init__()
		self.CheckBox = CheckBox

	def __del__( self ):
		self.wait()

	def createDb( self ):

		conn = sqlite3.connect( 'hash.db' )
		c = conn.cursor()

		c.execute('''CREATE TABLE hashes
				 (data text, hash text, count int)''')

		conn.commit()
		conn.close()

	def checkBd( self ):
		if not ( os.path.isfile( './hash.db' ) ):
			self.threadSignal.emit( 'База данных не найдена, создаём новую...' )
			self.createDb()

	# Получение списка webm'ок
	def getWebMList( self, board ):

		while True:

			try:
				catalog = urljoin( host, posixpath.join(board, "catalog_num.json") )
				catalog_data = json.loads( urlopen(catalog).read().decode('utf-8') )
				break
			except:
				self.threadSignal.emit( "Произошла ошибка при получении данных с сайта!" )
				time.sleep( 5 )
				continue

		webmthreads = []
		webms = []

		# Не помню откуда взял эту часть кода
		for thr in catalog_data['threads']:
			webmthreads.append( thr['num'] ) if re.match( r'^[^\.]*WEBM', thr['comment'], flags=re.IGNORECASE ) else False

		for thr in webmthreads:
			thr_url = urljoin( host, posixpath.join( board, "res", thr + ".json" ) )
			thr_data = json.loads( urlopen(thr_url).read().decode('utf-8') )
			for post in thr_data['threads'][0]['posts']:
				for attach in post['files']:
					params = attach['type'] == 6
					if ( self.CheckBox.get('mp4Download') ):
						params = params or attach['type'] == 10
					if ( ( params ) and ( attach['nsfw'] == 0 ) ):
						webms.append({'url': urljoin(host, attach['path']), 'fullname': attach['fullname'], 'md5': attach['md5']})
		return webms

	def checkWebmList( self, webmList ):

		self.checkBd()

		NewList = []

		conn = sqlite3.connect( 'hash.db' )
		c = conn.cursor()

		for i in webmList:
			sql = ( "SELECT * FROM `hashes` WHERE `hash` = '" + i.get( 'md5' ) + "'" )
			c.execute( sql )
			data = c.fetchall()

			if ( len(data) == 0 ):
				#i.update( {'isExistsInDb': False} )
				date = strftime( "%d.%m.%Y", localtime() )
				c.execute( "INSERT INTO `hashes` VALUES ( '"+ date + "' , '" + i.get( 'md5' ) + "', '1' )" )
				NewList.append(i)
			else:
				#i.update( {'isExistsInDb': True} )
				c.execute( "UPDATE `hashes` SET `count` = `count` + 1 WHERE `hash` =  '" + i.get( 'md5' ) + "'" )

		conn.commit()
		conn.close()

		return NewList

	def task( self, name, work_queue ):

		while not work_queue.empty():

			webm = work_queue.get()
			rawpath = webm.get('url').split('/')[-3:]

			if ( self.CheckBox.get('saveLikeName') ):
				namepass = webm.get('fullname')
			else:
				namepass = rawpath[-1]

			if ( self.CheckBox.get('differentPaths') ):
				ourpass = rawpath[-3] + '/'
				filepath = ourpass + namepass
				isPathExists = os.path.exists( ourpass )

				if not ( isPathExists ):
					os.makedirs(ourpass)
			else:

				ourpass = rawpath[-3] + '/' + rawpath[-2] + '/'
				filepath = ourpass + namepass
				isPathExists = os.path.exists( ourpass )

				if not ( isPathExists ):
					os.makedirs( ourpass )
					self.threadSignal.emit( "Создана папка: " + ourpass )

			if ( os.path.exists( filepath ) ):
				self.progressSignal.emit( True )
				if ( self.CheckBox.get('alreadyDownloaded') ):
					self.threadSignal.emit( filepath + " уже существует, пропускаем!" )
				continue

			r = requests.get( webm.get('url'), stream=True )

			with open( filepath, 'wb' ) as f:
				for chunk in r.iter_content( chunk_size=1024 ): 
					if ( chunk ):
						f.write( chunk )
				self.progressSignal.emit( True )
				self.threadSignal.emit( filepath + " успешно загружен!" )

	def run( self ):

		start_time = time.time()
		work_queue = queue.Queue()

		if ( self.CheckBox.get('rememberHashes') ):		
			webmList = self.checkWebmList( self.getWebMList( board ) )
		else:
			webmList = self.getWebMList( board )

		if ( self.CheckBox.get('nonStop') ):
			if ( len( webmList ) == 0 ):
				time.sleep( 10 )
				self.run()

		if not ( self.CheckBox.get('nonStop') ):
			self.threadSignal.emit( "Список файлов получен, начинаем загрузку!" )

		LenBar = len( webmList )
		self.LenSignal.emit( LenBar )

		for url in webmList:
			work_queue.put( url )

		# запуск задач
		tasks = [gevent.spawn( self.task, i, work_queue ) for i in range( 7 )]
		gevent.joinall( tasks )

		if ( self.CheckBox.get('nonStop') ):
			time.sleep( 10 )
			self.run()

		else:
			self.threadSignal.emit( "\n\nЗакачка файлов успешно завершена!")
			self.threadSignal.emit( "Общее время работы: %.5s секунд(ы)" % (time.time() - start_time) )
			self.ResBut.emit( True )

class WebmMenu( QtWidgets.QDialog, webm_menu.Ui_Dialog ):

	tray_icon = None

	def __init__( self ):

		super().__init__()
		self.setupUi( self )

		if ( os.path.exists("favicon.ico") ): 
			self.setWindowIcon( QIcon('favicon.ico') )
		else:
			self.setWindowIcon( self.style().standardIcon(QStyle.SP_ComputerIcon) )

		self.resetButtons( True )
		self.startButton.clicked.connect( self.startThread )
		self.stopButton.clicked.connect( self.stopProcess )

	# Управление кнопками start/stop
	def resetButtons( self, value ):
		if ( value ):
			self.startButton.setEnabled( True )
			self.stopButton.setEnabled( False )
		else:
			self.startButton.setEnabled( False )
			self.stopButton.setEnabled( True )

	# Проверка галочек
	def getCheckBoxStatus( self ):

		Btns = {}

		Btns.update( {'nonStop': ( self.nonStop.isChecked() if 1 else 0 ) } )
		Btns.update( {'differentPaths': ( self.differentPaths.isChecked() if 1 else 0 )} )
		Btns.update( {'alreadyDownloaded': ( self.alreadyDownloaded.isChecked() if 1 else 0 )} )
		Btns.update( {'clearAfterDownload': ( self.clearAfterDownload.isChecked() if 1 else 0 )} )
		Btns.update( {'mp4Download': ( self.mp4Download.isChecked() if 1 else 0 )} )
		Btns.update( {'saveLikeName': ( self.saveLikeName.isChecked() if 1 else 0 )} )
		Btns.update( {'rememberHashes': ( self.rememberHashes.isChecked() if 1 else 0 )} )

		return Btns

	# Инициализия иконки и трея
	def minimize( self ):
		self.tray_icon = QSystemTrayIcon( self )
		if ( os.path.exists("favicon.ico") ):
			self.tray_icon.setIcon( QIcon('favicon.ico') )
		else:
			self.tray_icon.setIcon( self.style().standardIcon(QStyle.SP_ComputerIcon) )
		show_action = QAction( "Показать", self )
		quit_action = QAction( "Закрыть", self )
		hide_action = QAction( "Скрыть", self )
		show_action.triggered.connect( self.show )
		hide_action.triggered.connect( self.hide )
		quit_action.triggered.connect( qApp.quit )
		tray_menu = QMenu()
		tray_menu.addAction( show_action )
		tray_menu.addAction( hide_action )
		tray_menu.addAction( quit_action )
		self.tray_icon.setContextMenu( tray_menu )
		self.tray_icon.show()

	# Запуск парсинга с нового потока
	def startThread( self ):

		self.resetButtons( False )

		self.progressPoint = 0
		self.progressMax = 0

		self.CheckBox = self.getCheckBoxStatus()
		self.get_thread = GetPostsThread( self.CheckBox )
		self.get_thread.threadSignal.connect( self.update_data )
		self.get_thread.progressSignal.connect( self.update_progress )
		self.get_thread.LenSignal.connect( self.lenStatus )
		self.get_thread.ResBut.connect( self.resetButtons )
		self.get_thread.start()

	# Прогресс качанных webm'ок
	def lenStatus( self, value ):

		if ( value == 0 ):
			self.progressMax = 999999
			self.progressBar.setRange( 0, self.progressMax )
			self.progressCount.setText( ".../..." )
		else:
			self.progressMax = value
			self.progressBar.setRange( 0, self.progressMax )
			self.progressCount.setText( "0/" + str( self.progressMax ) )

	# Выводим полученный сигнал (лог)
	def update_data( self, value ):
		self.wtime = strftime( "%H:%M:%S", localtime() ) + ' | '
		self.textBrowser.append( self.wtime + str(value) )

	# Обновление прогресса
	def update_progress( self, value ):
		if ( value ):
			self.progressPoint = self.progressPoint + 1
			if ( self.progressPoint <= self.progressBar.maximum() ):
				self.progressCount.setText( str( self.progressPoint ) + '/' + str( self.progressMax ) )
				self.progressBar.setValue( self.progressPoint )

	# Остановка процесса
	def stopProcess( self ):
		# Нужно переделать на более "мягкую" остановку процесса
		self.get_thread.terminate()
		self.progressPoint = 0
		self.progressBar.setValue( self.progressPoint )
		self.progressCount.setText( '--/--' )
		if ( self.CheckBox.get('clearAfterDownload') ):
			self.textBrowser.clear()
			self.textBrowser.append( self.wtime + 'Операция была остановлена пользователем!')
		else:
			self.textBrowser.append('\n\nОперация была остановлена пользователем!')
		self.resetButtons(True)

	# События при закрытии программы
	def closeEvent( self, event ):
		if ( self.hideInTray.isChecked() ):
			if ( self.tray_icon is None ):
				self.minimize() # Инициализация в трее на первый раз
			event.ignore()
			self.hide()
			self.tray_icon.showMessage( "Приложение в трее", "Это приложение было скрыто в трее", QSystemTrayIcon.Information, 3000 )
		else:
			reply = QMessageBox.question( self, 'Подтверждение', "Вы действительно хотите закрыть программу?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No )
			if ( reply == QMessageBox.Yes ):
				event.accept()
			else:
				event.ignore()	

def main():

	app = QtWidgets.QApplication( sys.argv )
	window = WebmMenu() 
	window.show()
	sys.exit( app.exec_() )

if ( __name__ == '__main__' ):
	main()