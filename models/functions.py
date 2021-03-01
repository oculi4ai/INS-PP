from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pyqtgraph import PlotWidget, plot
import sqlite3 as sq
import os
import datetime
import sys
from calendar import monthrange
import openpyxl
from models.windows_open import *
from models.INS import *
from models.translation import setTextMW_UI
from models.languages import languages
import json
import pyqtgraph as pg
import random
import threading
import time
from models.styles import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from models.styles import styles ,main_style
from models.messages import *



def init(mw_ui,mw):# mw_ui = (main window UI)



	mw_ui.orders_table_year.setDate( datetime.date.today() )
	check_main_db(mw_ui )
	view_data(mw_ui)
	connections(mw_ui,mw)


	con=sq.connect(mw_ui.main_data_base)
	t=con.execute('select backup_type from backup_settings').fetchall()[0][0]
	if t=='AUTO':
		mw_ui.backup_timer=threading.Thread(target=lambda:auto_backup_timer(mw_ui))
		mw_ui.backup_timer.start()



	style=con.execute('select name from style').fetchall()[0][0]
	mw_ui.current_style=styles[style]+main_style
	mw.setStyleSheet(mw_ui.current_style)

	language=con.execute('select name from language').fetchall()[0][0]
	change_language(language,mw)
	con.close()

def change_language(language,mw_ui):
	con=sq.connect(mw_ui.main_data_base)
	con.execute(f'update language set name="{language}"')
	con.commit()
	mw_ui.current_language=languages[language]
	mw_ui.current_language_name=language
	setTextMW_UI(mw_ui,languages[language])
	mw_ui.current_msg_language=messages[language]
	if language=='arabic':
		mw_ui.setLayoutDirection(Qt.RightToLeft)
	else:
		mw_ui.setLayoutDirection(Qt.LeftToRight)


def view_data(mw_ui ):
	view_products(mw_ui)
	view_rms(mw_ui)
	view_all_orders(mw_ui)
	home_page_info(mw_ui,1,1,1,1)

def connections(mw_ui,mw):
	def oib():
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(mw_ui,"QFileDialog.getSaveFileName()","","Backup Files (*.insppb);;All Files (*)", options=options)
		if fileName:
			open_import_backup(mw_ui  , fileName )

	def change_style(style):
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f'update style set name="{style}"')
		con.commit()
		mw_ui.current_style=styles[style]+main_style
		mw.setStyleSheet(mw_ui.current_style)




	mw_ui.actionEnglish.triggered.connect(lambda:change_language('english',mw_ui))
	mw_ui.actionArabic.triggered.connect(lambda:change_language('arabic',mw_ui))

	mw_ui.actionDarkGreen.triggered.connect(lambda:change_style('Dark green'))
	mw_ui.actionDarkBlue.triggered.connect(lambda:change_style('Dark blue'))
	mw_ui.actionWhite.triggered.connect(lambda:change_style('White'))
	mw_ui.import_backup.triggered.connect(oib)
	mw_ui.add_rm.clicked.connect(lambda:open_add_rm_window(mw_ui))
	mw_ui.products_list.clicked.connect(lambda:view_product(mw_ui))
	mw_ui.add_pm.clicked.connect(lambda: open_add_pm_window(mw_ui))
	mw_ui.p_rm_list.clicked.connect(lambda:open_edit_p_rm_window(mw_ui))
	mw_ui.units_list.clicked.connect(lambda:open_edit_unit_window(mw_ui))
	mw_ui.add_product.clicked.connect(lambda:open_add_product_window(mw_ui))
	mw_ui.orders_list.clicked.connect(lambda: open_edit_order_window(mw_ui))
	mw_ui.orders_table_year.dateChanged.connect(lambda: view_all_orders(mw_ui))
	mw_ui.actionBackup.triggered.connect(lambda: open_backup_settings(mw_ui))
	mw_ui.export_excell_button.triggered.connect(lambda: open_export_excell(mw_ui))
	mw_ui.actionINS.triggered.connect(lambda: open_login_success_window(mw_ui) if check_INS_status(mw_ui) else open_login_window(mw_ui))
	mw_ui.rm_list.clicked.connect(lambda:open_edit_pm_window(mw_ui) if mw_ui.rm_list.currentItem().data(5) in ('7','8','9') else open_edit_rm_window(mw_ui))
	mw_ui.add_unit.clicked.connect(lambda:open_add_unit_window(mw_ui) if mw_ui.products_list.currentRow() >= 0 else QtWidgets.QMessageBox.critical(mw_ui, mw_ui.current_msg_language['NoSelectedProduct'] , mw_ui.current_msg_language['SelectProduct2AddUnit'] , QtWidgets.QMessageBox.Ok))
	mw_ui.add_order.clicked.connect(lambda:open_add_order_window(mw_ui) if mw_ui.products_list.currentRow() >= 0 else QtWidgets.QMessageBox.critical(mw_ui, mw_ui.current_msg_language['NoSelectedProduct'] , mw_ui.current_msg_language['SelectProduct2AddOrder'] , QtWidgets.QMessageBox.Ok))
	mw_ui.add_p_rm.clicked.connect(lambda:open_add_p_rm_window(mw_ui) if mw_ui.products_list.currentRow() >= 0 else QtWidgets.QMessageBox.critical(mw_ui, mw_ui.current_msg_language['NoSelectedProduct'] , mw_ui.current_msg_language['SelectProduct2AddRawMaterial'] , QtWidgets.QMessageBox.Ok))
	mw_ui.delete_product.clicked.connect(lambda:delete_product_f(mw_ui) if mw_ui.products_list.currentRow() >= 0 else QtWidgets.QMessageBox.critical(mw_ui, mw_ui.current_msg_language['NoSelectedProduct'] , mw_ui.current_msg_language['SelectProduct2Delete'] , QtWidgets.QMessageBox.Ok))
	mw_ui.edit_product.clicked.connect(lambda:open_edit_product_window(mw_ui) if mw_ui.products_list.currentRow() >= 0 else QtWidgets.QMessageBox.critical(mw_ui, mw_ui.current_msg_language['NoSelectedProduct'] , mw_ui.current_msg_language['SelectProduct2Edit'] , QtWidgets.QMessageBox.Ok))

def home_page_info(mw_ui,rm,pm,p,o):
		con=sq.connect(mw_ui.main_data_base)
		#get raw materials count
		con=sq.connect(mw_ui.main_data_base)
		rm_count=con.execute('select count(*) from raw_materials').fetchall()[0][0]
		mw_ui.rm_count_home.setText(str(rm_count))

		#get packing materials count
		con=sq.connect(mw_ui.main_data_base)
		pm_count=con.execute('select count(*) from packing_materials').fetchall()[0][0]
		mw_ui.pm_count_home.setText(str(pm_count))

		#get products count
		p_count=con.execute('select count(*) from products').fetchall()[0][0]
		mw_ui.products_count_home.setText(str(p_count))

		#get active orders count
		orders=con.execute('select date_from,date_to from orders').fetchall()
		action_order=0

		for order in orders:
			now=datetime.date.today()
			date_from=datetime.date.fromisoformat(order[0])
			date_to=datetime.date.fromisoformat(order[1])


			if date_from <= now <= date_to:
				action_order+=1

		mw_ui.action_orders_count.setText(str(action_order))
		con.close()

def check_main_db(mw_ui ):
	con=sq.connect(mw_ui.main_data_base)
	tables=con.execute("SELECT name FROM sqlite_master WHERE type ='table' ").fetchall()


	if ('style',) not in tables:
		con.execute('''create table style (name)''')
		con.execute('insert into style (name) values ("blue")')
		con.commit()

	if ('language',) not in tables:
		con.execute('''create table language (name)''')
		con.execute('insert into language (name) values ("english")')
		con.commit()


	if ('products',) not in tables:
		con.execute('''create table products (id integer primary key autoincrement,name,code,material_type)''')

	if ('raw_materials',) not in tables:
		con.execute('create table raw_materials (id integer primary key autoincrement,name,type,code,quantity,unit,density) ')

	if ('packing_materials',) not in tables:
		con.execute('create table packing_materials (id integer primary key autoincrement,name,code,quantity,unit) ')

	if ('product_raw_materials',) not in tables:
		con.execute('create table product_raw_materials (id integer primary key autoincrement,product_id,material_id,t_quantity,t_unit,m_quantity,m_unit, percentage) ') # t_quantity = total quantity | m_quantity = material quantity

	if ('orders',) not in tables:
		con.execute('create table orders (id integer primary key autoincrement,name,product_id,quantity,unit_id,done,date_from,date_to) ')

	if ('backups',) not in tables:
		con.execute('create table backups (date,location) ')

	if ('backup_settings',) not in tables:
		con.execute('create table backup_settings (backup_type,backup_year_time , backup_month_time , backup_day_time , backup_hour_time ,location) ')
		con.execute('insert into backup_settings  (backup_type,backup_year_time , backup_month_time , backup_day_time , backup_hour_time ,location) values  ("",0 , 0 , 0 , 0 ,"")')
		con.commit()

	if ('history',) not in tables:
		con.execute('create table history (id integer primary key autoincrement , operation , "table" , "values" , date_and_time) ')

	if ('material_types',) not in tables:
		con.execute('create table material_types (id integer primary key autoincrement,type,units_ids) ')

		data=[
		['Solid','1'],
		['Solid','2'],
		['Solid','3'],
		['Solid','4'],

		['Liquid','5'],
		['Liquid','6'],

		['Gas','5'],
		['Gas','6']]

		for bit in data:
			con.execute(f"insert into material_types (type,units_ids) values ('{bit[0]}','{bit[1]}')")

		con.commit()




	if ('units',) not in tables:
		con.execute('''create table units (id integer primary key autoincrement , name , product_id , value,unit_id , is_standard )''')

		units=[

			["Milligram  (mg)"	,-1	,0.001			,2					,1],
			["Gram       (g)"  	,-1	,1				,'base'				,1],
			["Kilogram   (kg)"	,-1	,1000			,2					,1],
			["Tonne      (t)"	,-1	,1000000		,2					,1],
			["Liter      (l)"	,-1	,1				,'base'				,1],
			["Milliliter (ml)"	,-1	,0.001			,6					,1],
			["Piece"			,-1	,1				,'PackingMaterial'	,1],
			["Kilogram"			,-1	,1				,'PackingMaterial'	,1],
			["Metre"			,-1	,1				,'PackingMaterial'	,1],

		]
		for unit in units:

			con.execute('insert into units (name,product_id,value,unit_id,is_standard) values ("{}","{}","{}","{}","{}")'.format(unit[0],unit[1],unit[2],unit[3],unit[4]))
		con.commit()



	con.close()


##############################################
##############################################
######################### add Items (widget) >

def add_item_to_listWidget(title,listWidget,**data):
	item = QtWidgets.QListWidgetItem()
	item.setData(2,title)

	for bit in data.keys():#  data ={ data_4:2 , data_5:'rm' } 	data_4 for id / data_5 for material type
		item.setData(int(bit[-1]),data[bit])

	listWidget.addItem(item)

def add_header_to_tableWidget(title,tableWidget,**data):
	tableWidget.setRowCount(tableWidget.rowCount()+1)
	item = QtWidgets.QTableWidgetItem()
	item.setText(title)
	for bit in data.keys():
		item.setData(int(bit[-1]),data[bit])

	tableWidget.setVerticalHeaderItem(tableWidget.rowCount()-1, item)

def add_order_to_orders_tables(mw_ui,date_from,date_to ,title , tooltip,current_year ,y):

	mw_ui.all_orders.setSpan(y,(date_from-datetime.date(current_year,1,1)).days  , 1 ,(date_to - date_from).days+1)
	current_col=(date_to - date_from).days

	item = QtWidgets.QTableWidgetItem()
	item.setText(title)


	now=datetime.date.today()

	if date_from <= now <= date_to:

		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(f"icons/active.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon)
	item.setTextAlignment(QtCore.Qt.AlignCenter)

	item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
	item.setToolTip(tooltip)
	mw_ui.all_orders.setItem(mw_ui.all_orders.rowCount()-1 , (date_from-datetime.date(current_year,1,1)).days , item)


##############################################
##############################################
############################  view functions >

def view_products(mw_ui):

	con=sq.connect(mw_ui.main_data_base)
	products=con.execute('SELECT * FROM products').fetchall()
	mw_ui.products_list.clear()
	for product in products:
		add_item_to_listWidget( title=f"{product[1]}	({product[2]})",data_4=product[0],listWidget=mw_ui.products_list )
	con.close()

def view_product(mw_ui):
		con=sq.connect(mw_ui.main_data_base)

		m_type = con.execute(f'select material_type from  products where id={mw_ui.products_list.currentItem().data(4)}').fetchall()[0][0]
		s_unit_ids=tuple([ int(i[0]) for i in  con.execute(f'select units_ids from material_types where type="{m_type}" ').fetchall() ])
		mw_ui.current_product_standard_units = con.execute(f'select * from units where id in {s_unit_ids} ').fetchall()

		mw_ui.current_product_units=con.execute(f'select * from units where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()
		mw_ui.units_list.clear()
		for unit in mw_ui.current_product_units:
			add_item_to_listWidget( title=unit[1],data_4=unit[0],listWidget=mw_ui.units_list )

		view_product_rms(mw_ui)
		view_product_orders(mw_ui)
		con.close()

def view_unit(mw_ui):
	con=sq.connect(mw_ui.main_data_base)
	mw_ui.edit_unit_ui.unit_name.setText(mw_ui.units_list.currentItem().text())

	data=con.execute(f" select value,unit_id from units where id='{mw_ui.units_list.currentItem().data(4)}' ").fetchall()[0]

	unit_f=con.execute(f" select name from units where id='{data[1]}' ").fetchall()[0][0]

	mw_ui.edit_unit_ui.unit_value.setValue(float(data[0]))
	mw_ui.edit_unit_ui.units_combo.setCurrentText(unit_f)
	con.close()

def view_rms(mw_ui): # rms (Raw Materials)
	con=sq.connect(mw_ui.main_data_base)
	items=con.execute('select name,quantity,unit,id from raw_materials').fetchall()
	items.sort(key=lambda x:x[0])
	items+=(con.execute('select name,quantity,unit,id from packing_materials').fetchall())


	mw_ui.rm_list.clear()
	for item in items:
		mw_ui.item = QtWidgets.QListWidgetItem()
		try:
			unit=con.execute(f'select name from units where id={item[2]}').fetchall()[0][0]
		except:
			unit=item[2]

		try:
			unit=unit.split('(')[1].replace(")","")
		except:
			pass

		icon = QtGui.QIcon()
		if item[2]=='7' or item[2]=='8' or item[2]=='9':
			icon.addPixmap(QtGui.QPixmap("icons/Packing materials.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		else:
			icon.addPixmap(QtGui.QPixmap("icons/Raw materials.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		add_item_to_listWidget( title=f'{item[0]}	({item[1]} {unit})' , data_1=icon ,data_4=item[3] , data_5=item[2] ,listWidget=mw_ui.rm_list )

	con.close()

def view_rm(mw_ui):

		con=sq.connect(mw_ui.main_data_base)
		item=con.execute(f'select name,type,code,quantity,unit,density from raw_materials where id=={mw_ui.rm_list.currentItem().data(4)}').fetchall()[0]
		unit=con.execute(f'select name from units where id={item[4]}').fetchall()[0][0]

		mw_ui.edit_rm_ui.material_name.setText(item[0])
		mw_ui.edit_rm_ui.r_material_type.setText(item[1])

		mw_ui.edit_rm_ui.rm_units_combo.clear()
		units_id=tuple([ int(i[0]) for i in con.execute(f'select units_ids from material_types where type="{mw_ui.edit_rm_ui.r_material_type.text()}" ').fetchall()])
		units =con.execute(f'select * from units where id in {units_id}').fetchall()

		for m_unit in units:
			mw_ui.edit_rm_ui.rm_units_combo.addItem(m_unit[1],m_unit[0])


		mw_ui.edit_rm_ui.material_code.setText(item[2])
		mw_ui.edit_rm_ui.rm_quantity.setValue(float(item[3]))
		mw_ui.edit_rm_ui.rm_units_combo.setCurrentText(unit)
		mw_ui.edit_rm_ui.rm_density.setValue(float(item[5]))

def view_pm(mw_ui):

		con=sq.connect(mw_ui.main_data_base)
		item=con.execute(f'select name,code,quantity,unit from packing_materials where id=={mw_ui.rm_list.currentItem().data(4)}').fetchall()[0]
		unit=con.execute(f'select name from units where id={item[3]}').fetchall()[0][0]

		mw_ui.edit_pm_ui.material_name.setText(item[0])
		mw_ui.edit_pm_ui.material_code.setText(item[1])
		mw_ui.edit_pm_ui.rm_quantity.setValue(float(item[2]))
		mw_ui.edit_pm_ui.rm_units_combo.setCurrentText(unit)

def view_product_rms(mw_ui):
	con=sq.connect(mw_ui.main_data_base)
	items=con.execute(f'select * from product_raw_materials where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()
	mw_ui.p_rm_list.clear()
	icon = QtGui.QIcon()
	for item in items:

		if item[7]==None:
			data 	= con.execute(f'select name,id from packing_materials where id={item[2]} ').fetchall()[0]
			unit_1	= con.execute(f'select name from units where id={item[4]}').fetchall()[0][0]
			unit_2_id=con.execute(f'select unit from packing_materials where id={item[2]}').fetchall()[0][0]
			unit_2	= con.execute(f'select name from units where id={ unit_2_id }').fetchall()[0][0]
			icon.addPixmap(QtGui.QPixmap("icons/Packing materials.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

			add_item_to_listWidget( title=f'{data[0]}	Every {item[3]} {unit_1.split("(")[1].replace(")","") } Packing in {item[5]} {unit_2} ' , data_1=icon , data_4=item[0] ,  data_5='pm' , data_6=data[1] ,listWidget=mw_ui.p_rm_list )

		else:
			data =con.execute(f'select name,id from raw_materials where id={item[2]} ').fetchall()[0]
			icon.addPixmap(QtGui.QPixmap("icons/Raw materials.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

			add_item_to_listWidget( title=f"{data[0]}	{item[7]}%" , data_1=icon , data_4=item[0] , data_5='rm' , data_6=data[1] ,listWidget=mw_ui.p_rm_list )

def view_product_rm(mw_ui):
		con=sq.connect(mw_ui.main_data_base)
		item=con.execute(f'select * from product_raw_materials where id="{mw_ui.p_rm_list.currentItem().data(4)}"').fetchall()[0]

		material_id = con.execute(f'select material_id from product_raw_materials where id={mw_ui.p_rm_list.currentItem().data(4)}').fetchall()[0][0]
		m_data=[material_id , mw_ui.p_rm_list.currentItem().data(5)]

		if item[7]==None:
			m_name=con.execute(f'select name from packing_materials where id={item[2]}').fetchall()[0][0]
		else:
			m_name=con.execute(f'select name from raw_materials where id={item[2]}').fetchall()[0][0]

		t_unit=con.execute(f'select name from units where id={item[4]}').fetchall()[0][0]
		m_unit=con.execute(f'select name from units where id={item[6]}').fetchall()[0][0]

		mw_ui.edit_p_rm_ui.p_rm_name.setText(m_name)
		mw_ui.edit_p_rm_ui.p_rm_t_quantity.setValue(float(item[3]))
		mw_ui.edit_p_rm_ui.p_rm_t_unit.setCurrentText(t_unit)
		mw_ui.edit_p_rm_ui.p_rm_m_quantity.setValue(float(item[5]))
		mw_ui.edit_p_rm_ui.p_rm_m_unit.setCurrentText(m_unit)

def view_product_orders(mw_ui):
	con=sq.connect(mw_ui.main_data_base)
	items=con.execute(f' select * from orders where product_id="{mw_ui.products_list.currentItem().data(4)}"')
	mw_ui.orders_list.clear()
	for item in items:
		unit=con.execute(f'select name from units where id={item[4]}').fetchall()[0][0]


		icon=None
		if datetime.date.fromisoformat(item[6])<= datetime.date.today() <=datetime.date.fromisoformat(item[7]):
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap(f"icons/active.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		add_item_to_listWidget( title=item[1] , data_1=icon , data_4=item[0] ,listWidget=mw_ui.orders_list )

def view_all_orders(mw_ui):

	mw_ui.all_orders.setRowCount(0)
	mw_ui.all_orders.setColumnCount(0)

	add_header_to_tableWidget(title='Month',tableWidget=mw_ui.all_orders)


	current_year=mw_ui.orders_table_year.date().year()
	monthes_names=['Jan' ,'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

	year_days_count=(datetime.date(current_year,12,monthrange(current_year , 12)[1])-datetime.date(current_year,1,1)).days+1
	mw_ui.all_orders.setColumnCount(year_days_count)

	for i in range(year_days_count):
		item = QtWidgets.QTableWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignCenter)
		mw_ui.all_orders.setItem(0, i, item)

	current_col=0



	for month in range(1,13):
		current_month_days=monthrange(current_year , month)[1]

		mw_ui.all_orders.setSpan(0,current_col,1,current_month_days)



		mw_ui.all_orders.item(0 , current_col).setText(f'{monthes_names[month-1]} ({current_month_days} DAY)')

		current_col+=current_month_days



	con=sq.connect(mw_ui.main_data_base)
	products=con.execute('select name,id from products').fetchall()




	y=1
	for product in products:
		add_header_to_tableWidget(title=product[0],tableWidget=mw_ui.all_orders,data_4=product[1])

		orders=con.execute(f'select * from orders where product_id="{product[1]}"').fetchall()

		current_col=0
		for order in orders:
			add_order_to_orders_tables(mw_ui,datetime.date.fromisoformat(order[6]),datetime.date.fromisoformat(order[7]) ,order[1] , f'{order[1]} \n from {order[6]} \n to {order[7]} \n ',current_year ,y)



		y+=1

def view_product_order(mw_ui):
	con=sq.connect(mw_ui.main_data_base)
	item=con.execute(f' select * from orders where id={mw_ui.orders_list.currentItem().data(4)}').fetchall()[0]
	mw_ui.current_order_unit=item[4]
	mw_ui.current_order_quantity=float(item[3])
	unit=con.execute(f' select name from units where id={item[4]}').fetchall()[0][0]

	mw_ui.edit_order_ui.order_name.setText(item[1])
	mw_ui.edit_order_ui.order_quantity.setValue(float(item[3]))
	mw_ui.edit_order_ui.order_unit.setCurrentText(unit)
	mw_ui.edit_order_ui.date_order_from.setDate(datetime.date.fromisoformat(item[6]))
	mw_ui.edit_order_ui.date_order_to.setDate(datetime.date.fromisoformat(item[7]))

##############################################
##############################################
############################   add functions >

def add_product(mw_ui):
	mw_ui.add_product_window.close()
	con=sq.connect(mw_ui.main_data_base)
	ch=con.execute(f'select name from products where name=?',(mw_ui.open_add_product_ui.product_name.text(),)).fetchall()
	ch_2=con.execute(f'select code from products where code=?',(mw_ui.open_add_product_ui.product_code.text(),)).fetchall()

	m=QtWidgets.QMessageBox.Yes

	if len(ch)>0 or len(ch_2)>0 :
		msg= mw_ui.current_msg_language['There are']

		if len(ch)>0:
			msg+=f"{len(ch)}  { mw_ui.current_msg_language['product with name']} ( {ch[0][0]} ) \n\n"

		if len(ch)>0 and len(ch_2)>0:
			msg+=' '+ mw_ui.current_msg_language['and']+' '

		if len(ch_2)>0:
			msg+=f"{len(ch_2)} { mw_ui.current_msg_language['product with code']} ( {ch_2[0][0]} )"

		msg+='\n\n'+  mw_ui.current_msg_language['Do you still want to add this product?']+'\n'
		m=QtWidgets.QMessageBox.question(mw_ui.open_add_product_ui,mw_ui.current_msg_language['ConfirmAddProduct'],msg)


	if m==QtWidgets.QMessageBox.Yes:
		con.execute("INSERT into products (name,'code','material_type') values (?,?,?)" ,(mw_ui.open_add_product_ui.product_name.text() , mw_ui.open_add_product_ui.product_code.text() ,mw_ui.open_add_product_ui.matiral_type.currentText() ))
		con.commit()
		product_id=con.execute('select id from products').fetchall()[-1][0]
		save_command( operation='insert' , table='products',  db=mw_ui.main_data_base ,id=product_id,name=mw_ui.open_add_product_ui.product_name.text() , code=mw_ui.open_add_product_ui.product_code.text() , material_type=mw_ui.open_add_product_ui.matiral_type.currentText())

		#add item to products list
		product_id=con.execute('select id from products').fetchall()[-1][0]
		add_item_to_listWidget( title=f'{mw_ui.open_add_product_ui.product_name.text()}	({mw_ui.open_add_product_ui.product_code.text()})',data_4=product_id,listWidget=mw_ui.products_list )

		#add product row in orders table
		add_header_to_tableWidget(title=mw_ui.open_add_product_ui.product_name.text(),tableWidget=mw_ui.all_orders,data_4=product_id)

		#update home info
		mw_ui.products_count_home.setText(str( int(mw_ui.products_count_home.text())+1 ))

	con.close()

def add_unit_f(mw_ui):
		mw_ui.add_unit_window.close()
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f'insert into units (name,product_id,value,unit_id,is_standard) values ("{mw_ui.add_unit_ui.unit_name.text()}","{mw_ui.products_list.currentItem().data(4)}","{mw_ui.add_unit_ui.unit_value.value()}","{mw_ui.add_unit_ui.units_combo.itemData(mw_ui.add_unit_ui.units_combo.currentIndex())}",0)')
		con.commit()
		save_command( operation='insert' , table='units',  db=mw_ui.main_data_base , name=mw_ui.add_unit_ui.unit_name.text() , product_id=mw_ui.products_list.currentItem().data(4) , value=mw_ui.add_unit_ui.unit_value.value() , unit_id=mw_ui.add_unit_ui.units_combo.itemData(mw_ui.add_unit_ui.units_combo.currentIndex()) , is_standard='0')

		#add unit item to list
		item = QtWidgets.QListWidgetItem()
		item.setData(2,mw_ui.add_unit_ui.unit_name.text())
		item.setData(4,con.execute('select id from units').fetchall()[-1][0])
		mw_ui.units_list.addItem(item)

		con.close()

def add_rm(mw_ui): # rm (Raw material)+
	mw_ui.add_rm_window.close()
	con=sq.connect(mw_ui.main_data_base)
	con.execute(f'insert into raw_materials (name,type,code,quantity,unit,density) values ("{mw_ui.open_add_rm_ui.material_name.text()}","{mw_ui.open_add_rm_ui.material_type.currentText()}","{mw_ui.open_add_rm_ui.material_code.text()}","{mw_ui.open_add_rm_ui.rm_quantity.value()}","{mw_ui.open_add_rm_ui.rm_units_combo.itemData(mw_ui.open_add_rm_ui.rm_units_combo.currentIndex()) }","{mw_ui.open_add_rm_ui.rm_density.value()}") ')
	con.commit()
	material_id=con.execute('select id from raw_materials').fetchall()[-1][0]
	con.close()
	save_command( operation='insert' , table='raw_materials',  db=mw_ui.main_data_base , id=material_id ,name=mw_ui.open_add_rm_ui.material_name.text(), type=mw_ui.open_add_rm_ui.material_type.currentText(),code=mw_ui.open_add_rm_ui.material_code.text() , quantity=mw_ui.open_add_rm_ui.rm_quantity.value() , unit=mw_ui.open_add_rm_ui.rm_units_combo.itemData(mw_ui.open_add_rm_ui.rm_units_combo.currentIndex()) , density=mw_ui.open_add_rm_ui.rm_density.value())
	view_rms(mw_ui)


def add_pm(mw_ui): # pm (Packing material)+
	mw_ui.add_pm_window.close()
	con=sq.connect(mw_ui.main_data_base)
	con.execute(f'insert into packing_materials (name,code,quantity,unit) values ("{mw_ui.add_pm_ui.material_name.text()}","{mw_ui.add_pm_ui.material_code.text()}","{mw_ui.add_pm_ui.rm_quantity.value()}","{mw_ui.add_pm_ui.rm_units_combo.itemData(mw_ui.add_pm_ui.rm_units_combo.currentIndex()) }") ')
	con.commit()
	material_id=con.execute('select id from packing_materials').fetchall()[-1][0]
	save_command( operation='insert' , table='packing_materials',  db=mw_ui.main_data_base ,id=material_id , name=mw_ui.add_pm_ui.material_name.text() , code=mw_ui.add_pm_ui.material_code.text() , quantity=mw_ui.add_pm_ui.rm_quantity.value() , unit=mw_ui.add_pm_ui.rm_units_combo.itemData(mw_ui.add_pm_ui.rm_units_combo.currentIndex()))
	con.close()
	view_rms(mw_ui)
	home_page_info(mw_ui,0,1,0,0)

def add_p_rm(mw_ui):

		if mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())[1]=='rm':
			con=sq.connect(mw_ui.main_data_base)
			percentages=[ i[0] for i in con.execute(f'select percentage from product_raw_materials where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()]
			total_percentage =0
			for percentage in percentages:
				try:
					total_percentage+=float(percentage)
				except:
					pass

			product_type=con.execute(f'select material_type from products where id={mw_ui.products_list.currentItem().data(4)}').fetchall()[0][0]
			material_type=con.execute(f'select type,density from raw_materials where id={mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())[0]}').fetchall()[0]

			total_current_value=mw_ui.add_p_rm_ui.p_rm_t_quantity.value()*get_unit_value(mw_ui,mw_ui.add_p_rm_ui.p_rm_t_unit.itemData(mw_ui.add_p_rm_ui.p_rm_t_unit.currentIndex()))
			material_current_value=mw_ui.add_p_rm_ui.p_rm_m_quantity.value()*get_unit_value(mw_ui,mw_ui.add_p_rm_ui.p_rm_m_unit.itemData(mw_ui.add_p_rm_ui.p_rm_m_unit.currentIndex()))
			current_percentage=100*material_current_value/total_current_value


			if product_type =="Solid" and (material_type[0] == 'Liquid' or material_type[0] == 'Gas') :
				material_current_value*=float(material_type[1])

			elif material_type[0] =="Solid" and (product_type == 'Liquid' or product_type == 'Gas') :
				material_current_value/=float(material_type[1])





			if total_percentage+current_percentage<=100 :

				con.execute(f'''insert into product_raw_materials (product_id , material_id , t_quantity , t_unit , m_quantity , m_unit ,percentage) values ("{mw_ui.products_list.currentItem().data(4)}","{mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())[0]}","{mw_ui.add_p_rm_ui.p_rm_t_quantity.value()}","{mw_ui.add_p_rm_ui.p_rm_t_unit.itemData(mw_ui.add_p_rm_ui.p_rm_t_unit.currentIndex())}","{mw_ui.add_p_rm_ui.p_rm_m_quantity.value()}","{mw_ui.add_p_rm_ui.p_rm_m_unit.itemData(mw_ui.add_p_rm_ui.p_rm_m_unit.currentIndex())}","{current_percentage}")''')
				con.commit()
				material_id=con.execute('select id from product_raw_materials').fetchall()[-1][0]
				save_command( operation='insert' , table='product_raw_materials',id=material_id ,  db=mw_ui.main_data_base ,product_id=mw_ui.products_list.currentItem().data(4) ,
																										material_id=mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())[0] ,
																										t_quantity=mw_ui.add_p_rm_ui.p_rm_t_quantity.value() ,
																										t_unit=mw_ui.add_p_rm_ui.p_rm_t_unit.itemData(mw_ui.add_p_rm_ui.p_rm_t_unit.currentIndex()) ,
																										m_quantity=mw_ui.add_p_rm_ui.p_rm_m_quantity.value() ,
																										m_unit=mw_ui.add_p_rm_ui.p_rm_m_unit.itemData(mw_ui.add_p_rm_ui.p_rm_m_unit.currentIndex()) ,
																										percentage=current_percentage)
				view_product_rms(mw_ui)
				mw_ui.add_p_rm_window.close()
			else:
				msg=mw_ui.current_msg_language["you have only {}% from ptoduct to add raw materials \n you are trying to add {}% of {}"].format(100-total_percentage , current_percentage , mw_ui.add_p_rm_ui.p_rm_combo.currentText())
				QtWidgets.QMessageBox.critical(mw_ui.add_p_rm_ui,mw_ui.current_msg_language['Big quantity'],msg)

		else:
			con=sq.connect(mw_ui.main_data_base)

			con.execute(f'''insert into product_raw_materials (product_id , material_id , t_quantity , t_unit , m_quantity , m_unit ) values ("{mw_ui.products_list.currentItem().data(4)}","{mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())[0]}","{mw_ui.add_p_rm_ui.p_rm_t_quantity.value()}","{mw_ui.add_p_rm_ui.p_rm_t_unit.itemData(mw_ui.add_p_rm_ui.p_rm_t_unit.currentIndex())}","{mw_ui.add_p_rm_ui.p_rm_m_quantity.value()}","{mw_ui.add_p_rm_ui.p_rm_m_unit.itemData(mw_ui.add_p_rm_ui.p_rm_m_unit.currentIndex())}")''')
			con.commit()
			material_id=con.execute('select id from product_raw_materials').fetchall()[-1][0]
			save_command( operation='insert' , table='product_raw_materials',id=material_id ,  db=mw_ui.main_data_base ,product_id=mw_ui.products_list.currentItem().data(4) ,
																									material_id=mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())[0] ,
																									t_quantity=mw_ui.add_p_rm_ui.p_rm_t_quantity.value() ,
																									t_unit=mw_ui.add_p_rm_ui.p_rm_t_unit.itemData(mw_ui.add_p_rm_ui.p_rm_t_unit.currentIndex()) ,
																									m_quantity=mw_ui.add_p_rm_ui.p_rm_m_quantity.value() ,
																									m_unit=mw_ui.add_p_rm_ui.p_rm_m_unit.itemData(mw_ui.add_p_rm_ui.p_rm_m_unit.currentIndex()))
			mw_ui.add_p_rm_window.close()
			view_product_rms(mw_ui)

def add_product_order(mw_ui):


		con=sq.connect(mw_ui.main_data_base)
		order_value=mw_ui.add_order_ui.order_quantity.value()*get_unit_value(mw_ui,mw_ui.add_order_ui.order_unit.itemData(mw_ui.add_order_ui.order_unit.currentIndex()))
		materials=con.execute(f'select material_id , t_quantity , t_unit , m_quantity , m_unit, percentage from product_raw_materials where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()

		status=True
		for material in materials:
			if material[5] == None:
				rm_data=con.execute(f'select quantity from packing_materials where id={material[0]}').fetchall()[0]

				if float(rm_data[0]) <   float(material[3])*order_value / (float(material[1])*get_unit_value(mw_ui, material[2] )):
					status=False

			else:
				rm_data=con.execute(f'select quantity,unit,type from raw_materials where id={material[0]}').fetchall()[0]

				if  float(rm_data[0])*get_unit_value(mw_ui, rm_data[1] )  < order_value*float(material[5])/100:
					status=False

		if status:
			mw_ui.add_order_window.close()

			con.execute(f''' insert into orders (name , product_id , quantity , unit_id , date_from , date_to) values ("{mw_ui.add_order_ui.order_name.text()}","{mw_ui.products_list.currentItem().data(4)}","{mw_ui.add_order_ui.order_quantity.value()}","{mw_ui.add_order_ui.order_unit.itemData(mw_ui.add_order_ui.order_unit.currentIndex())}","{mw_ui.add_order_ui.date_order_from.date().toPyDate()}","{mw_ui.add_order_ui.date_order_to.date().toPyDate()}")''')
			con.commit()
			order_id=con.execute('select id from orders').fetchall()[-1][0]
			save_command( operation='insert' , table='orders',db=mw_ui.main_data_base ,id=order_id , name=mw_ui.add_order_ui.order_name.text() ,
																			product_id=mw_ui.products_list.currentItem().data(4) ,
																			quantity=mw_ui.add_order_ui.order_quantity.value() ,
																			unit_id=mw_ui.add_order_ui.order_unit.itemData(mw_ui.add_order_ui.order_unit.currentIndex()) ,
																			date_from=mw_ui.add_order_ui.date_order_from.date().toPyDate().isoformat() ,
																			date_to=mw_ui.add_order_ui.date_order_to.date().toPyDate().isoformat())


			for material in materials:
				if material[5] == None:
					rm_data		=	con.execute(f'select quantity,unit from packing_materials where id={material[0]}').fetchall()[0]
					new_quantity = float(rm_data[0]) -   float(material[3])*order_value / (float(material[1])*get_unit_value(mw_ui, material[2] ))
					con.execute(f'update packing_materials set quantity="{new_quantity}" where id={material[0]}')
					con.commit()
					save_command( operation='update' , table='packing_materials', db=mw_ui.main_data_base ,quantity=new_quantity , where_id=material[0])

				else:
					rm_data		=	con.execute(f'select quantity,unit,type from raw_materials where id={material[0]}').fetchall()[0]
					m_value 	=float(rm_data[0])
					m_unit_value=get_unit_value(mw_ui,int(rm_data[1]))


					new_quantity=( (m_value*m_unit_value) - (order_value*float(material[5])/100) )/m_unit_value

					con.execute(f'update raw_materials set quantity="{new_quantity}" where id={material[0]}')
					con.commit()
					save_command( operation='update' , table='raw_materials', db=mw_ui.main_data_base ,quantity=new_quantity , where_id=material[0])




			view_product_orders(mw_ui)
			view_rms(mw_ui)
			view_all_orders(mw_ui)
			home_page_info(mw_ui,0,0,0,1)
		else:
			QtWidgets.QMessageBox.critical(mw_ui.add_order_window , mw_ui.current_msg_language['NoEnoughMaterialsQuantity'] , mw_ui.current_msg_language['NoEnoughQuantity2AddOrder'] , QtWidgets.QMessageBox.Ok)
		con.close()

##############################################
##############################################
############################  edit functions >


def edit_product_f(mw_ui):
		mw_ui.edit_product_window.close()
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f''' update products set 	name='{mw_ui.open_edit_product_ui.product_name.text()}' ,
		 										code='{mw_ui.open_edit_product_ui.product_code.text()}'
												  where id={mw_ui.products_list.currentItem().data(4)} ''')
		con.commit()
		save_command( operation='update' , table='products', db=mw_ui.main_data_base ,name=mw_ui.open_edit_product_ui.product_name.text(),code=mw_ui.open_edit_product_ui.product_code.text(),where_id=mw_ui.products_list.currentItem().data(4) )
		con.close()
		mw_ui.products_list.currentItem().setText(f'{mw_ui.open_edit_product_ui.product_name.text()}	({mw_ui.open_edit_product_ui.product_code.text()})')
		view_all_orders(mw_ui)

def edit_unit(mw_ui):
		mw_ui.edit_unit_window.close()
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f''' update units set 	name='{mw_ui.edit_unit_ui.unit_name.text()}',
											value='{mw_ui.edit_unit_ui.unit_value.value()}',
											unit_id='{mw_ui.edit_unit_ui.units_combo.itemData(mw_ui.edit_unit_ui.units_combo.currentIndex())}'
											where id='{mw_ui.units_list.currentItem().data(4)}' ''')
		con.commit()
		save_command( operation='update' , table='units', db=mw_ui.main_data_base ,name=mw_ui.edit_unit_ui.unit_name.text(),
											value=mw_ui.edit_unit_ui.unit_value.value(),
											unit_id=mw_ui.edit_unit_ui.units_combo.itemData(mw_ui.edit_unit_ui.units_combo.currentIndex()),
											where_id=mw_ui.units_list.currentItem().data(4))

		mw_ui.units_list.currentItem().setText(mw_ui.edit_unit_ui.unit_name.text())


def edit_rm(mw_ui):
		mw_ui.edit_rm_window.close()
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f'''update raw_materials set name="{mw_ui.edit_rm_ui.material_name.text()}"
												,code="{mw_ui.edit_rm_ui.material_code.text()}"
												,quantity="{mw_ui.edit_rm_ui.rm_quantity.value()}"
												,unit="{mw_ui.edit_rm_ui.rm_units_combo.itemData(mw_ui.edit_rm_ui.rm_units_combo.currentIndex())}"
												,density="{mw_ui.edit_rm_ui.rm_density.value()}"
													where id=={mw_ui.rm_list.currentItem().data(4)} ''')
		con.commit()
		save_command( operation='update' , table='raw_materials', db=mw_ui.main_data_base ,name=mw_ui.edit_rm_ui.material_name.text()
												,code=mw_ui.edit_rm_ui.material_code.text()
												,quantity=mw_ui.edit_rm_ui.rm_quantity.value()
												,unit=mw_ui.edit_rm_ui.rm_units_combo.itemData(mw_ui.edit_rm_ui.rm_units_combo.currentIndex())
												,density=mw_ui.edit_rm_ui.rm_density.value(),
												where_id=mw_ui.rm_list.currentItem().data(4))
		#view_rms(mw_ui)
		unit=mw_ui.edit_rm_ui.rm_units_combo.currentText().split('(')[1].replace(')','')
		title=f'{mw_ui.edit_rm_ui.material_name.text()}	({mw_ui.edit_rm_ui.rm_quantity.value()} {unit})'
		mw_ui.rm_list.currentItem().setText(title)



def edit_pm(mw_ui):
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f'''update packing_materials set name="{mw_ui.edit_pm_ui.material_name.text()}"
												,code="{mw_ui.edit_pm_ui.material_code.text()}"
												,quantity="{mw_ui.edit_pm_ui.rm_quantity.value()}"
													where id=={mw_ui.rm_list.currentItem().data(4)} ''')
		con.commit()
		save_command( operation='update' , table='raw_materials', db=mw_ui.main_data_base ,name=mw_ui.edit_pm_ui.material_name.text()
												,code=mw_ui.edit_pm_ui.material_code.text()
												,quantity=mw_ui.edit_pm_ui.rm_quantity.value()
												,where_id=mw_ui.rm_list.currentItem().data(4))
		#view_rms(mw_ui)
		title=f'{mw_ui.edit_pm_ui.material_name.text()}	({mw_ui.edit_pm_ui.rm_quantity.value()} { mw_ui.edit_pm_ui.rm_units_combo.currentText() })'
		mw_ui.rm_list.currentItem().setText(title)
		mw_ui.edit_pm_window.close()

def edit_p_rm(mw_ui):
		mw_ui.edit_p_rm_window.close()

		con=sq.connect(mw_ui.main_data_base)
		last_percentage=con.execute(f'select percentage from product_raw_materials where id="{mw_ui.p_rm_list.currentItem().data(4)}"').fetchall()[0][0]
		if last_percentage !=None:

			percentages=[ (i[0]) for i in con.execute(f'select percentage from product_raw_materials where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()]
			total_percentage =0
			for percentage in percentages:
				try:
					total_percentage+=percentage
				except:
					pass

			material_type=con.execute(f'select type from raw_materials where id={mw_ui.p_rm_list.currentItem().data(6)}').fetchall()[0][0]

			total_current_value=mw_ui.edit_p_rm_ui.p_rm_t_quantity.value()*get_unit_value(mw_ui,mw_ui.edit_p_rm_ui.p_rm_t_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_t_unit.currentIndex()))
			material_current_value=mw_ui.edit_p_rm_ui.p_rm_m_quantity.value()*get_unit_value(mw_ui,mw_ui.edit_p_rm_ui.p_rm_m_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_m_unit.currentIndex()))
			current_percentage=100*material_current_value/total_current_value



			try:
				last_percentage=float(last_percentage)
			except:
				pass

			if  total_percentage+current_percentage-last_percentage<=100:
				con.execute(f'''update product_raw_materials set
															 material_id ="{mw_ui.p_rm_list.currentItem().data(6)}"
															, t_quantity ="{mw_ui.edit_p_rm_ui.p_rm_t_quantity.value()}"
															, t_unit ="{mw_ui.edit_p_rm_ui.p_rm_t_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_t_unit.currentIndex())}"
															, m_quantity="{mw_ui.edit_p_rm_ui.p_rm_m_quantity.value()}"
															, m_unit="{mw_ui.edit_p_rm_ui.p_rm_m_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_m_unit.currentIndex())}"
															, percentage="{current_percentage}"
															 where id={mw_ui.p_rm_list.currentItem().data(4)} ''')
				con.commit()
				save_command( operation='update' , table='product_raw_materials', db=mw_ui.main_data_base , material_id =mw_ui.p_rm_list.currentItem().data(6)
															, t_quantity =str(mw_ui.edit_p_rm_ui.p_rm_t_quantity.value())
															, t_unit =mw_ui.edit_p_rm_ui.p_rm_t_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_t_unit.currentIndex())
															, m_quantity=str(mw_ui.edit_p_rm_ui.p_rm_m_quantity.value())
															, m_unit=mw_ui.edit_p_rm_ui.p_rm_m_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_m_unit.currentIndex())
															, percentage=str(current_percentage)
															, where_id=mw_ui.p_rm_list.currentItem().data(4))
				mw_ui.p_rm_list.currentItem().setText(f'{mw_ui.edit_p_rm_ui.p_rm_name.text()}	{current_percentage}%')
		else:
			i=mw_ui.p_rm_list.currentIndex()
			con.execute(f'''update product_raw_materials set
															 material_id ="{mw_ui.p_rm_list.currentItem().data(6)}"
															, t_quantity ="{mw_ui.edit_p_rm_ui.p_rm_t_quantity.value()}"
															, t_unit ="{mw_ui.edit_p_rm_ui.p_rm_t_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_t_unit.currentIndex())}"
															, m_quantity="{mw_ui.edit_p_rm_ui.p_rm_m_quantity.value()}"
															, m_unit="{mw_ui.edit_p_rm_ui.p_rm_m_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_m_unit.currentIndex())}"
															 where id={mw_ui.p_rm_list.currentItem().data(4)} ''')
			con.commit()
			save_command( operation='update' , table='product_raw_materials', db=mw_ui.main_data_base , material_id =mw_ui.p_rm_list.currentItem().data(6)
															, t_quantity =str(mw_ui.edit_p_rm_ui.p_rm_t_quantity.value())
															, t_unit =mw_ui.edit_p_rm_ui.p_rm_t_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_t_unit.currentIndex())
															, m_quantity=str(mw_ui.edit_p_rm_ui.p_rm_m_quantity.value())
															, m_unit=mw_ui.edit_p_rm_ui.p_rm_m_unit.itemData(mw_ui.edit_p_rm_ui.p_rm_m_unit.currentIndex())
															, where_id=mw_ui.p_rm_list.currentItem().data(4))

			view_product_rms(mw_ui)
			mw_ui.p_rm_list.setCurrentIndex(i)

def edit_product_order(mw_ui):
	mw_ui.edit_order_window.close()
	con=sq.connect(mw_ui.main_data_base)


	new_values=''
	if mw_ui.edit_order_ui.order_quantity.value() != mw_ui.current_order_quantity or mw_ui.edit_order_ui.order_unit.itemData(mw_ui.edit_order_ui.order_unit.currentIndex()) != mw_ui.current_order_unit:
		pass



	con.execute(f''' update orders set
					name="{mw_ui.edit_order_ui.order_name.text()}",
					quantity="{mw_ui.edit_order_ui.order_quantity.value()}",
					unit_id="{mw_ui.edit_order_ui.order_unit.itemData(mw_ui.edit_order_ui.order_unit.currentIndex())}",
					date_from="{mw_ui.edit_order_ui.date_order_from.date().toPyDate()}",
					date_to="{mw_ui.edit_order_ui.date_order_to.date().toPyDate()}"
					where id={mw_ui.orders_list.currentItem().data(4)}''')
	con.commit()
	save_command( operation='update' , table='orders', db=mw_ui.main_data_base ,name=mw_ui.edit_order_ui.order_name.text(),
					quantity=mw_ui.edit_order_ui.order_quantity.value(),
					unit_id=mw_ui.edit_order_ui.order_unit.itemData(mw_ui.edit_order_ui.order_unit.currentIndex()),
					date_from=mw_ui.edit_order_ui.date_order_from.date().toPyDate().isoformat(),
					date_to=mw_ui.edit_order_ui.date_order_to.date().toPyDate().isoformat(),
					where_id=mw_ui.orders_list.currentItem().data(4))


	mw_ui.orders_list.currentItem().setText(mw_ui.edit_order_ui.order_name.text())
	view_all_orders(mw_ui)


##############################################
##############################################
############################  delete functions >

def delete_product_f(mw_ui):

		a=QtWidgets.QMessageBox.question(mw_ui,mw_ui.current_msg_language['DeleteProductConfirm'],mw_ui.current_msg_language['AskDeleteProductConfirm'])
		if a==QtWidgets.QMessageBox.Yes:

			con=sq.connect(mw_ui.main_data_base)

			commands=[]

			con.execute(f''' DELETE FROM products where id=={mw_ui.products_list.currentItem().data(4)} ''')
			con.execute(f''' DELETE FROM orders where product_id=="{mw_ui.products_list.currentItem().data(4)}" ''')
			con.execute(f''' DELETE FROM product_raw_materials where product_id=="{mw_ui.products_list.currentItem().data(4)}" ''')
			con.execute(f''' DELETE FROM units where product_id=="{mw_ui.products_list.currentItem().data(4)}" ''')
			con.commit()

			save_command( operation='delete' , table='products', db=mw_ui.main_data_base ,where_id=mw_ui.products_list.currentItem().data(4))
			save_command( operation='delete' , table='orders', db=mw_ui.main_data_base ,where_product_id=mw_ui.products_list.currentItem().data(4))
			save_command( operation='delete' , table='product_raw_materials', db=mw_ui.main_data_base ,where_product_id=mw_ui.products_list.currentItem().data(4))
			save_command( operation='delete' , table='units', db=mw_ui.main_data_base ,where_product_id=mw_ui.products_list.currentItem().data(4))


			mw_ui.products_list.takeItem(mw_ui.products_list.currentRow())# remove product item


			view_all_orders(mw_ui)
			home_page_info(mw_ui,0,0,1,0)
			con.close()

			try:
				mw_ui.edit_product_window.close()
			except:
				pass

def delete_unit(mw_ui):
		m=QtWidgets.QMessageBox.question(mw_ui , mw_ui.current_msg_language['DeleteUnitConfirm'] ,mw_ui.current_msg_language['AskDeleteUnitConfirm'])
		if m==QtWidgets.QMessageBox.Yes:
			con=sq.connect(mw_ui.main_data_base)
			m=''
			r_units=con.execute(f'select * from units where unit_id="{mw_ui.units_list.currentItem().data(4)}" ').fetchall()
			if len(r_units)>0:
				m=QtWidgets.QMessageBox.question(mw_ui , mw_ui.current_msg_language['DeleteUnitConfirm'] ,mw_ui.current_msg_language["this unit is base for {} other units \n do you want to delete all this units?"].format(str(len(r_units))))





			if m=='yes' or len(r_units)==0:

					con.execute(f'delete from units where id={mw_ui.units_list.currentItem().data(4)}')
					con.execute(f'delete from units where unit_id="{mw_ui.units_list.currentItem().data(4)}"')

					con.commit()
					save_command( operation='delete' , table='units', db=mw_ui.main_data_base ,where_id=mw_ui.units_list.currentItem().data(4))
					save_command( operation='delete' , table='units', db=mw_ui.main_data_base ,where_unit_id=mw_ui.units_list.currentItem().data(4))
					mw_ui.edit_unit_window.close()
					view_product(mw_ui)




def delete_rm(mw_ui):
		a=QtWidgets.QMessageBox.question(mw_ui , mw_ui.current_msg_language['DeleteMaterialConfirm'] ,mw_ui.current_msg_language['AskDeleteMaterialConfirm'])
		if a==QtWidgets.QMessageBox.Yes:
			con=sq.connect(mw_ui.main_data_base)
			con.execute(f'delete from raw_materials where id={mw_ui.rm_list.currentItem().data(4)}')
			con.execute(f'delete from product_raw_materials where material_id="{mw_ui.rm_list.currentItem().data(4)}"')
			con.commit()
			save_command( operation='delete' , table='raw_materials', db=mw_ui.main_data_base ,where_id=mw_ui.rm_list.currentItem().data(4))
			save_command( operation='delete' , table='product_raw_materials', db=mw_ui.main_data_base ,where_material_id=mw_ui.rm_list.currentItem().data(4))
			view_rms(mw_ui)
			mw_ui.edit_rm_window.close()



def delete_pm(mw_ui):
		a=QtWidgets.QMessageBox.question(mw_ui , mw_ui.current_msg_language['DeleteMaterialConfirm'] ,mw_ui.current_msg_language['AskDeleteMaterialConfirm'])
		if a==QtWidgets.QMessageBox.Yes:
			con=sq.connect(mw_ui.main_data_base)
			con.execute(f'delete from packing_materials where id="{mw_ui.rm_list.currentItem().data(4)}"')
			con.execute(f'delete from product_raw_materials where material_id="{mw_ui.rm_list.currentItem().data(4)}"')
			con.commit()
			save_command( operation='delete' , table='packing_materials', db=mw_ui.main_data_base ,where_id=mw_ui.rm_list.currentItem().data(4))
			save_command( operation='delete' , table='product_raw_materials', db=mw_ui.main_data_base ,where_id=mw_ui.rm_list.currentItem().data(4))

			view_rms(mw_ui)
			mw_ui.edit_pm_window.close()


def delete_product_rm(mw_ui):
		a=QtWidgets.QMessageBox.question(mw_ui , mw_ui.current_msg_language['DeleteMaterialConfirm'] ,mw_ui.current_msg_language['AskDeleteMaterialConfirm'])
		if a==QtWidgets.QMessageBox.Yes:
			con=sq.connect(mw_ui.main_data_base)
			con.execute(f'delete from product_raw_materials where id={mw_ui.p_rm_list.currentItem().data(4)}')
			con.commit()
			save_command( operation='delete' , table='product_raw_materials', db=mw_ui.main_data_base ,where_id=mw_ui.p_rm_list.currentItem().data(4))
			view_product_rms(mw_ui)
			mw_ui.edit_p_rm_window.close()

def delete_product_order(mw_ui):
	a=QtWidgets.QMessageBox.question(mw_ui , mw_ui.current_msg_language['DeleteOrderConfirm'] ,mw_ui.current_msg_language['AskDeleteOrderConfirm'])
	if a==QtWidgets.QMessageBox.Yes:
		con=sq.connect(mw_ui.main_data_base)
		con.execute(f''' delete from orders where id={mw_ui.orders_list.currentItem().data(4)}''')
		con.commit()
		save_command( operation='delete' , table='product_raw_materials', db=mw_ui.main_data_base ,where_id=mw_ui.p_rm_list.currentItem().data(4))
		view_product_orders(mw_ui)
		view_all_orders(mw_ui)
	view_all_orders(mw_ui)
	mw_ui.edit_order_window.close()






def get_unit_value(mw_ui,unit_id):
	con=sq.connect(mw_ui.main_data_base)
	unit_value=1
	while True:
		try:
			unit=con.execute(f'select value,unit_id  from units where id={unit_id}').fetchall()[0]

			if unit[1]=='base':
				break
			else:
				unit_id=int(unit[1])
				unit_value*=float(unit[0])
		except:
			pass

	return unit_value

def create_backup(path, mw_ui):

	con_main_db=sq.connect(mw_ui.main_data_base)
	con_backup_db=sq.connect(path)

	for table in mw_ui.backup_tables.keys():
		con_backup_db.execute(f'create table {table} (id integer primary key autoincrement,{mw_ui.backup_tables[table]}) ')
		data=con_main_db.execute(f'select {mw_ui.backup_tables[table]} from {table}').fetchall()
		for bit in data:
			bit=str(bit).replace('None','""')
			con_backup_db.execute(f'insert into {table} ({mw_ui.backup_tables[table]}) values {bit}')
	con_backup_db.commit()
	con_main_db.execute(f'insert into backups (date,location) values ("{datetime.datetime.now().isoformat()}","{path}")')
	con_main_db.commit()
	con_main_db.close()
	con_backup_db.close()
	open_success_msg(mw_ui , 'Backup created successfully' , f'New backup created successfully \n\n Path: {path}'  )

def auto_backup_timer(mw_ui ):
	print('timer started')
	con=sq.connect(mw_ui.main_data_base)
	settings=con.execute('select backup_year_time , backup_month_time , backup_day_time , backup_hour_time from backup_settings').fetchall()[0]
	lastbackup=None
	backups=con.execute('select date from backups ').fetchall()
	if len(backups)>0:
		lastbackup=backups[-1][0]

	if lastbackup==None:
		r_time=0

	else:
		delta=(datetime.datetime.now() - datetime.datetime.fromisoformat(lastbackup)).total_seconds()
		r_time= ((settings[0]*1892160000) + (settings[1]*2592000) + (settings[2]*86400) + (settings[3]*3600)) - delta

	for i in range(int(r_time/6)):
		if mw_ui.open:
			print(f'backup after {int(r_time/60)-i} min')
			time.sleep(60)

		else:
			break
	if mw_ui.open:

		create_backup(os.path.join(con.execute('select location from backup_settings').fetchall()[0][0], datetime.datetime.now().isoformat() + ".insppb"), mw_ui)
		auto_backup_timer(mw_ui )

def save_command(db=None , table='' , operation='' , **values ):
	con=sq.connect(db)
	print(values)
	con.execute(f"insert into history ( 'table' , operation , 'values' , date_and_time) values (?,?,?,?)", ( table , operation , json.dumps(values) , datetime.datetime.now().isoformat() ))
	con.commit()
	con.close()
