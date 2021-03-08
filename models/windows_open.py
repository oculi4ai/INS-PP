
from tkinter import *
import sqlite3 as sq
import datetime
from models import functions
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from PyQt5.QtGui import QMovie
from models import INS
from models.languages import languages
from models.translation import *
import sys
import sh
import socket
import threading
import time
from qtwidgets import PasswordEdit
from PyQt5.QtWidgets import QFileDialog
from openpyxl import Workbook


#####################################################
############ product windows ########################
#####################################################
#>
def open_add_product_window(mw_ui):

	mw_ui.add_product_window = QtWidgets.QDialog()
	mw_ui.add_product_window.setWindowModality(QtCore.Qt.ApplicationModal)
	mw_ui.open_add_product_ui = uic.loadUi('windows/add_new_product_window.ui', mw_ui.add_product_window)
	mw_ui.open_add_product_ui.setStyleSheet(mw_ui.current_style)

	retranslateProduct(mw_ui.open_add_product_ui,mw_ui.current_language)
	mw_ui.add_product_window.setWindowTitle(mw_ui.current_language['Add Product'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.open_add_product_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.open_add_product_ui.setLayoutDirection(QtCore.Qt.LeftToRight)

	# view material types
	con=sq.connect(mw_ui.main_data_base)
	types=con.execute('select id,type from material_types').fetchall()
	current_type=[]
	for base_type in types :
		current_type=base_type
		for i in types:
			if i[1]==current_type[1] and i!=current_type :
				types.remove(i)
	for m_type in types:
		mw_ui.open_add_product_ui.matiral_type.addItem(m_type[1],m_type[0])


	mw_ui.open_add_product_ui.add.clicked.connect(lambda:functions.add_product(mw_ui))
	mw_ui.add_product_window.show()

def open_edit_product_window(mw_ui):

	mw_ui.edit_product_window = QtWidgets.QDialog()
	mw_ui.edit_product_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.open_edit_product_ui = uic.loadUi('windows/edit_product_window.ui', mw_ui.edit_product_window)
	mw_ui.open_edit_product_ui.setStyleSheet(mw_ui.current_style)

	retranslateProduct(mw_ui.open_edit_product_ui,mw_ui.current_language)
	mw_ui.edit_product_window.setWindowTitle(mw_ui.current_language['Edit Product'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.open_edit_product_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.open_edit_product_ui.setLayoutDirection(QtCore.Qt.LeftToRight)


	# view material types

	con=sq.connect(mw_ui.main_data_base)
	types=con.execute('select id,type from material_types').fetchall()
	current_type=[]
	for base_type in types :
		current_type=base_type
		for i in types:
			if i[1]==current_type[1] and i!=current_type :
				types.remove(i)
				pass
	for m_type in types:
		pass
		mw_ui.open_edit_product_ui.matiral_type.addItem(m_type[1],m_type[0])

	#view product info
	data=con.execute(f'select name,material_type,code from products where id = {mw_ui.products_list.currentItem().data(4)}').fetchall()[0]

	mw_ui.open_edit_product_ui.product_name.setText(data[0])
	mw_ui.open_edit_product_ui.product_code.setText(data[2])
	mw_ui.open_edit_product_ui.matiral_type.setCurrentText(data[1])


	mw_ui.open_edit_product_ui.edit_product.clicked.connect(lambda:functions.edit_product_f(mw_ui))
	mw_ui.open_edit_product_ui.delete_product.clicked.connect(lambda:functions.delete_product_f(mw_ui))

	mw_ui.edit_product_window.show()

#####################################################
############ raw mterials windows ###################
#####################################################
#>
def open_add_rm_window(mw_ui):

	mw_ui.add_rm_window = QtWidgets.QDialog()
	mw_ui.add_rm_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.open_add_rm_ui = uic.loadUi('windows/add_new_rm_window.ui', mw_ui.add_rm_window )
	mw_ui.open_add_rm_ui.setStyleSheet(mw_ui.current_style)

	retranslateRawMaterial(mw_ui.open_add_rm_ui,mw_ui.current_language)
	mw_ui.add_rm_window.setWindowTitle(mw_ui.current_language['Add Material'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.open_add_rm_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.open_add_rm_ui.setLayoutDirection(QtCore.Qt.LeftToRight)


	# view material types
	con=sq.connect(mw_ui.main_data_base)
	types=con.execute('select id,type from material_types').fetchall()
	current_type=[]
	for base_type in types :
		current_type=base_type
		for i in types:
			if i[1]==current_type[1] and i!=current_type :
				types.remove(i)
				pass
	for m_type in types:
		pass
		mw_ui.open_add_rm_ui.material_type.addItem(m_type[1],m_type[0])


	def view_rm_units():
		mw_ui.open_add_rm_ui.rm_units_combo.clear()
		units_id=tuple([ int(i[0]) for i in con.execute(f'select units_ids from material_types where type="{mw_ui.open_add_rm_ui.material_type.currentText()}" ').fetchall()])
		units =con.execute(f'select * from units where id in {units_id}').fetchall()

		for unit in units:
			mw_ui.open_add_rm_ui.rm_units_combo.addItem(unit[1],unit[0])
	view_rm_units()
	mw_ui.open_add_rm_ui.material_type.currentIndexChanged.connect(view_rm_units)



	mw_ui.open_add_rm_ui.add_rm.clicked.connect(lambda:functions.add_rm(mw_ui))

	mw_ui.add_rm_window.show()

def open_edit_rm_window(mw_ui):

	mw_ui.edit_rm_window = QtWidgets.QDialog()
	mw_ui.edit_rm_window .setWindowModality(QtCore.Qt.ApplicationModal)
	mw_ui.edit_rm_ui = uic.loadUi('windows/edit_rm_window.ui', mw_ui.edit_rm_window)
	mw_ui.edit_rm_ui.setStyleSheet(mw_ui.current_style)

	retranslateRawMaterial(mw_ui.edit_rm_ui,mw_ui.current_language)
	mw_ui.edit_rm_window.setWindowTitle(mw_ui.current_language['Edit Material'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.edit_rm_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.edit_rm_ui.setLayoutDirection(QtCore.Qt.LeftToRight)

	con=sq.connect(mw_ui.main_data_base)

	functions.view_rm(mw_ui)


	mw_ui.edit_rm_ui.edit_rm.clicked.connect(lambda:functions.edit_rm(mw_ui))
	mw_ui.edit_rm_ui.delete_rm.clicked.connect(lambda:functions.delete_rm(mw_ui))

	mw_ui.edit_rm_window.show()

#####################################################
############ packing mterials windows ###################
#####################################################
#>

def open_add_pm_window(mw_ui):

	mw_ui.add_pm_window =QtWidgets.QDialog()
	mw_ui.add_pm_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.add_pm_ui = uic.loadUi('windows/add_new_pm_window.ui', mw_ui.add_pm_window)
	mw_ui.add_pm_ui.setStyleSheet(mw_ui.current_style)

	retranslatePackingMaterial(mw_ui.add_pm_ui,mw_ui.current_language)
	mw_ui.add_pm_window.setWindowTitle(mw_ui.current_language['Add Material'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.add_pm_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.add_pm_ui.setLayoutDirection(QtCore.Qt.LeftToRight)


	mw_ui.add_pm_ui.add_pm.clicked.connect(lambda:functions.add_pm(mw_ui))

	con=sq.connect(mw_ui.main_data_base)
	mw_ui.add_pm_ui.rm_units_combo.clear()
	units=con.execute(f'select name,id from units where unit_id="PackingMaterial" ').fetchall()

	for unit in units:
		mw_ui.add_pm_ui.rm_units_combo.addItem(unit[0],unit[1])

	mw_ui.add_pm_window.show()

def open_edit_pm_window(mw_ui):

	mw_ui.edit_pm_window =  QtWidgets.QDialog()
	mw_ui.edit_pm_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.edit_pm_ui =uic.loadUi('windows/edit_pm_window.ui', mw_ui.edit_pm_window)
	mw_ui.edit_pm_ui.setStyleSheet(mw_ui.current_style)

	retranslatePackingMaterial(mw_ui.edit_pm_ui,mw_ui.current_language)
	mw_ui.edit_pm_window.setWindowTitle(mw_ui.current_language['Edit Material'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.edit_pm_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.edit_pm_ui.setLayoutDirection(QtCore.Qt.LeftToRight)

	con=sq.connect(mw_ui.main_data_base)
	units=con.execute(f'select name,id from units where unit_id="PackingMaterial" ').fetchall()

	for unit in units:
		mw_ui.edit_pm_ui.rm_units_combo.addItem(unit[0],unit[1])

	functions.view_pm(mw_ui)

	mw_ui.edit_pm_window.show()

	mw_ui.edit_pm_ui.edit_pm.clicked.connect(lambda:functions.edit_pm(mw_ui))
	mw_ui.edit_pm_ui.delete_pm.clicked.connect(lambda:functions.delete_pm(mw_ui))


#####################################################
############ unit windows ###########################
#####################################################
#>

def open_add_unit_window(mw_ui):

	mw_ui.add_unit_window =  QtWidgets.QDialog()
	mw_ui.add_unit_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.add_unit_ui = uic.loadUi('windows/add_new_unit_window.ui', mw_ui.add_unit_window)
	mw_ui.add_unit_ui.setStyleSheet(mw_ui.current_style)

	retranslateUnit(mw_ui.add_unit_ui,mw_ui.current_language)
	mw_ui.add_unit_window.setWindowTitle(mw_ui.current_language['Add Unit'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.add_unit_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.add_unit_ui.setLayoutDirection(QtCore.Qt.LeftToRight)


	mw_ui.add_unit_ui.add_unit.clicked.connect(lambda:functions.add_unit_f(mw_ui))

	units=mw_ui.current_product_units+ mw_ui.current_product_standard_units

	for unit in units:
		mw_ui.add_unit_ui.units_combo.addItem(unit[1] , unit[0])

	mw_ui.add_unit_window.show()

def open_edit_unit_window(mw_ui):

	mw_ui.edit_unit_window =  QtWidgets.QDialog()
	mw_ui.edit_unit_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.edit_unit_ui = uic.loadUi('windows/edit_unit_window.ui', mw_ui.edit_unit_window)
	mw_ui.edit_unit_ui.setStyleSheet(mw_ui.current_style)

	retranslateUnit(mw_ui.edit_unit_ui,mw_ui.current_language)
	mw_ui.edit_unit_window.setWindowTitle(mw_ui.current_language['Edit Unit'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.edit_unit_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.edit_unit_ui.setLayoutDirection(QtCore.Qt.LeftToRight)


	mw_ui.edit_unit_ui.edit_unit.clicked.connect(lambda:functions.edit_unit(mw_ui))
	mw_ui.edit_unit_ui.delete_unit.clicked.connect(lambda:functions.delete_unit(mw_ui))


	units=mw_ui.current_product_units+ mw_ui.current_product_standard_units

	for unit in units:
		mw_ui.edit_unit_ui.units_combo.addItem(unit[1] , unit[0])

	functions.view_unit(mw_ui)
	mw_ui.edit_unit_window.show()


#####################################################
############ product raw mterials windows ###########
#####################################################
#>

def open_add_p_rm_window(mw_ui):

	mw_ui.add_p_rm_window = QtWidgets.QDialog()
	mw_ui.add_p_rm_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.add_p_rm_ui = uic.loadUi('windows/add_product_rm_window.ui', mw_ui.add_p_rm_window)
	mw_ui.add_p_rm_ui.setStyleSheet(mw_ui.current_style)

	con=sq.connect(mw_ui.main_data_base)
	rm=con.execute('select name,id from raw_materials').fetchall()
	pm=con.execute('select name,id from packing_materials').fetchall()

	for material in rm:
		mw_ui.add_p_rm_ui.p_rm_combo.addItem(material[0],[material[1] , 'rm'])

	for material in pm:
		mw_ui.add_p_rm_ui.p_rm_combo.addItem(material[0],[material[1] , 'pm'])


	for unit in mw_ui.current_product_standard_units:
		mw_ui.add_p_rm_ui.p_rm_t_unit.addItem(unit[1] , unit[0])


	def get_m_unit():
		mw_ui.add_p_rm_ui.p_rm_m_unit.clear()
		m_data = mw_ui.add_p_rm_ui.p_rm_combo.itemData(mw_ui.add_p_rm_ui.p_rm_combo.currentIndex())
		if m_data[1]=='rm':
			m_type=con.execute(f'select type from raw_materials where id={m_data[0]}').fetchall()[0][0]
			units_id=tuple([ int(i[0]) for i in con.execute(f'select units_ids from material_types where type="{m_type}"').fetchall()])
			units=con.execute(f'select name,id from units where id in {units_id} ')
		else:
			unit_id=con.execute(f'select unit from packing_materials where id={m_data[0]}').fetchall()[0][0]
			units=con.execute(f'select name,id from units where id={unit_id}')

		for unit in units:
			mw_ui.add_p_rm_ui.p_rm_m_unit.addItem(unit[0], unit[1])



	get_m_unit()
	mw_ui.add_p_rm_ui.p_rm_combo.currentIndexChanged.connect(get_m_unit)
	mw_ui.add_p_rm_ui.add_p_rm.clicked.connect(lambda:functions.add_p_rm(mw_ui))

	mw_ui.add_p_rm_window.show()

def open_edit_p_rm_window(mw_ui):

	mw_ui.edit_p_rm_window = QtWidgets.QDialog()
	mw_ui.edit_p_rm_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.edit_p_rm_ui = uic.loadUi('windows/edit_product_rm_window.ui', mw_ui.edit_p_rm_window)
	mw_ui.edit_p_rm_ui.setStyleSheet(mw_ui.current_style)

	con=sq.connect(mw_ui.main_data_base)

	for unit in mw_ui.current_product_standard_units:
		mw_ui.edit_p_rm_ui.p_rm_t_unit.addItem(unit[1] , unit[0])

	material_id = con.execute(f'select material_id from product_raw_materials where id={mw_ui.p_rm_list.currentItem().data(4)}').fetchall()[0][0]
	m_data=[material_id , mw_ui.p_rm_list.currentItem().data(5)]
	if m_data[1]=='rm':
		m_type=con.execute(f'select type from raw_materials where id={m_data[0]}').fetchall()[0][0]
		units_id=tuple([ int(i[0]) for i in con.execute(f'select units_ids from material_types where type="{m_type}"').fetchall()])
		units=con.execute(f'select name,id from units where id in {units_id} ').fetchall()
	else:
		unit_id=con.execute(f'select unit from packing_materials where id={m_data[0]}').fetchall()[0][0]
		units=con.execute(f'select name,id from units where id={unit_id}').fetchall()
	for unit in units:
		mw_ui.edit_p_rm_ui.p_rm_m_unit.addItem(unit[0], unit[1])


	mw_ui.edit_p_rm_ui.edit_p_rm.clicked.connect(lambda:functions.edit_p_rm(mw_ui))
	mw_ui.edit_p_rm_ui.delete_item.clicked.connect(lambda:functions. delete_product_rm(mw_ui))


	functions.view_product_rm(mw_ui)


	mw_ui.edit_p_rm_window.show()


#####################################################
############ order windows ##########################
#####################################################
#>

def open_add_order_window(mw_ui):

	mw_ui.add_order_window = QtWidgets.QDialog()
	mw_ui.add_order_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.add_order_ui = uic.loadUi('windows/add_new_order_window.ui', mw_ui.add_order_window)
	mw_ui.add_order_ui.setStyleSheet(mw_ui.current_style)
	retranslateAddOrder(mw_ui.add_order_ui,mw_ui.current_language)
	mw_ui.add_order_window.setWindowTitle(mw_ui.current_language['Add Order'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.add_order_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.add_order_ui.setLayoutDirection(QtCore.Qt.LeftToRight)

	# view units


	con=sq.connect(mw_ui.main_data_base)
	m_units=	con.execute(f'select id,name from units where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()

	m_units +=mw_ui.current_product_standard_units
	for unit in m_units :
		mw_ui.add_order_ui.order_unit.addItem(unit[1] , unit[0])


	mw_ui.add_order_ui.add_order.clicked.connect(lambda:functions.add_product_order(mw_ui))

	#date_order_from
	mw_ui.add_order_ui.date_order_from.setDate(datetime.date.today())
	mw_ui.add_order_ui.date_order_to.setDate(datetime.date.today())

	mw_ui.add_order_window.show()

def open_edit_order_window(mw_ui):

	mw_ui.edit_order_window = QtWidgets.QDialog()
	mw_ui.edit_order_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.edit_order_ui = uic.loadUi('windows/edit_order_window.ui', mw_ui.edit_order_window)
	mw_ui.edit_order_ui.setStyleSheet(mw_ui.current_style)
	retranslateAddOrder(mw_ui.edit_order_ui,mw_ui.current_language)
	mw_ui.edit_order_window.setWindowTitle(mw_ui.current_language['Edit Order'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.edit_order_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.edit_order_ui.setLayoutDirection(QtCore.Qt.LeftToRight)

	con=sq.connect(mw_ui.main_data_base)
	m_units=	con.execute(f'select id,name from units where product_id="{mw_ui.products_list.currentItem().data(4)}"').fetchall()

	m_units +=mw_ui.current_product_standard_units
	for unit in m_units :
		mw_ui.edit_order_ui.order_unit.addItem(unit[1] , unit[0])

	functions.view_product_order(mw_ui)


	mw_ui.edit_order_ui.edit_order.clicked.connect(lambda:functions.edit_product_order(mw_ui))

	mw_ui.edit_order_window.show()

#####################################################
############ Excel windows ##########################
#####################################################
#>

def open_export_excell(mw_ui):

	def get_serial_letter(turn):

		alpha=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


		current_col=[0]

		numbers=[]

		int_turn=int(turn/27)+1

		for i in range(turn):
			for i in range(27):
				if i < 26:
					current_col[-1]=i
				else:
					done=False

					for a in range(len(current_col)):
						if current_col[-a-1]<25:
							current_col[-a-1]+=1
							done=True
							break
						else:
							current_col[-a-1]=0

					if not done:
						current_col.append(0)

				number=''

				for n_id in current_col:
					number+=alpha[n_id]
				numbers.append(number)

		return(numbers[:turn])



	def export_excell( e_e_UI):
		file_name = QFileDialog.getSaveFileName(mw_ui,"Export excel","","Excel Files (*.xlsx);;All Files (*)")

		con=sq.connect(mw_ui.main_data_base)
		e_e_UI.export_progress.setValue(0)

		# product export
		data=[[]]
		columns=[]



		if e_e_UI.selected_section=='products':

			items=()
			for i in range(e_e_UI.selected_section_list.count()):
				if(e_e_UI.selected_section_list.item(i).checkState()):
					items+=(e_e_UI.selected_section_list.item(i).data(4),)


			def get_data(items):
				data = []
				con = sq.connect(mw_ui.main_data_base)
				for row in items:
					bit = []

					if e_e_UI.product_name.checkState():
						name = con.execute(f"select name from products where id = {row}").fetchall()[0][0]
						bit.append(name)

					if e_e_UI.product_code.checkState():
						code = con.execute(f"select code from products where id = {row}").fetchall()[0][0]
						bit.append(code)

					if e_e_UI.product_material_type.checkState():
						material_types = con.execute(f"select material_type from products where id = {row}").fetchall()[0][0]
						bit.append(material_types)

					if e_e_UI.product_orders.checkState():
						orders_count = con.execute(f"select count(*) from orders where product_id = '{row}' ").fetchall()[0][0]
						for i in range(orders_count):
							text = con.execute(f"select name from orders where product_id = '{row}' ").fetchall()[0][0]
							if e_e_UI.orders_date.checkState():
							  text +=('\n From: '+ ' To:'.join( con.execute(f"select date_from,date_to from orders where product_id = '{row}' ").fetchall()[0]))

							if e_e_UI.orders_quantity.checkState():
							  text +=('\n Quantity: '+con.execute(f"select quantity from orders where product_id = '{row}' ").fetchall()[0][0])

							  unit_id = con.execute(f"select unit_id from orders where product_id = '{row}' ").fetchall()[0][0]
							  text += (con.execute(f"select name from units where id = {unit_id} ").fetchall()[0][0])
							bit.append(text)
					data.append(bit)
				return data
			data=get_data(items)



		elif e_e_UI.selected_section=='raw_materials':


			rm_items=()
			pm_items=()
			for i in range(e_e_UI.selected_section_list.count()):


				if (e_e_UI.rm_list.item(i).checkState()):
					if e_e_UI.rm_list.item(i).data(5)=='pm' :

						pm_items+=(int(e_e_UI.rm_list.item(i).data(4)),)
					elif e_e_UI.rm_list.item(i).data(5)=='rm':

						rm_items+=(int(e_e_UI.rm_list.item(i).data(4)),)



			def ex_rm():
				data = []
				con = sq.connect(mw_ui.main_data_base)

				items=()
				for i in range(e_e_UI.selected_section_list.count()):
					if(e_e_UI.selected_section_list.item(i).checkState()) and e_e_UI.selected_section_list.item(i).data(5)=='rm':
						items+=(e_e_UI.selected_section_list.item(i).data(4),)

				for row in items:
					bit = []

					if e_e_UI.rm_name.checkState():
						name = con.execute(f"select name from raw_materials where id = {row}").fetchall()[0][0]
						bit.append(name)
					if e_e_UI.rm_code.checkState():
						code = con.execute(f"select code from raw_materials where id = {row}").fetchall()[0][0]
						bit.append(code)
					if e_e_UI.rm_material_type.checkState():
						material_type = con.execute(f"select type from raw_materials where id = {row}").fetchall()[0][0]
						bit.append(material_type)
					if e_e_UI.rm_available_quantity.checkState():
						quantity = con.execute(f"select quantity from raw_materials where id = {row}").fetchall()[0][0]
						bit.append(quantity)
					if e_e_UI.rm_density.checkState():
						density = con.execute(f"select density from raw_materials where id = {row}").fetchall()[0][0]
						bit.append(density)


					data.append(bit)
				return data


			def ex_pm():
				data = []
				con = sq.connect(mw_ui.main_data_base)

				items=()
				for i in range(e_e_UI.selected_section_list.count()):
					if(e_e_UI.selected_section_list.item(i).checkState()) and e_e_UI.selected_section_list.item(i).data(5)=='pm':
						items+=(e_e_UI.selected_section_list.item(i).data(4),)

				for row in items:
					bit = []

					if e_e_UI.rm_name.checkState():
						name = con.execute(f"select name from packing_materials where id = {row}").fetchall()[0][0]
						bit.append(name)
					if e_e_UI.rm_code.checkState():
						code = con.execute(f"select code from packing_materials where id = {row}").fetchall()[0][0]
						bit.append(code)
					if e_e_UI.rm_available_quantity.checkState():
						quantity = con.execute(f"select quantity from packing_materials where id = {row}").fetchall()[0][0]
						bit.append(quantity)


					data.append(bit)
				return data

			if len(rm_items)>len(pm_items):
				data=ex_rm()
				e_e_UI.export_progress.setValue(10)
				data+=ex_pm()
				e_e_UI.export_progress.setValue(20)


			else:
				#ex_pm()
				#e_e_UI.export_progress.setValue(10)
				ex_rm()
				e_e_UI.export_progress.setValue(20)



		table_width=0
		for i in data :
			if len(i)>table_width:
				table_width=len(i)

		serial_letter=(get_serial_letter(table_width))
		workbook = Workbook()
		sheet = workbook.active

		t=80/len(data)# for progress
		v=20
		for raw in range(len(data)):
			v+=t
			e_e_UI.export_progress.setValue(v)

			for cell in range(len(data[raw])):
				sheet[f'{serial_letter[cell]}{raw+1}'] =  data[raw][cell]


		workbook.save(filename=file_name[0]+'.xlsx')



		e_e_UI.export_progress.setValue(100)


	def select_section_e_e(e_e_UI ,p ,rm  ):

		e_e_UI.product_frame.setEnabled(p)
		e_e_UI.rm_frame.setEnabled(rm)

		if p:
			e_e_UI.selected_section='products'
			e_e_UI.selected_section_list=e_e_UI.products_list


		if rm:
			e_e_UI.selected_section='raw_materials'
			e_e_UI.selected_section_list=e_e_UI.rm_list

	try:
		mw_ui.export_excell.close()
	except:
		pass

	mw_ui.export_excell = QtWidgets.QDialog()
	mw_ui.export_excell.setWindowModality(QtCore.Qt.ApplicationModal)
	mw_ui.export_excell_ui = uic.loadUi('windows/export_excel.ui', mw_ui.export_excell)
	mw_ui.export_excell_ui.setStyleSheet(mw_ui.current_style)

	retranslateExportExcel(mw_ui.export_excell_ui,mw_ui.current_language)
	mw_ui.export_excell.setWindowTitle(mw_ui.current_language['Export Excel'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.export_excell_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.export_excell_ui.setLayoutDirection(QtCore.Qt.LeftToRight)

	mw_ui.export_excell.show()

	# init functions



	con=sq.connect(mw_ui.main_data_base)
	products=con.execute('select name,id from products').fetchall()
	for product in products:
		item = QtWidgets.QListWidgetItem()
		item.setData(2,product[0])
		item.setData(4,product[1])
		item.setCheckState(QtCore.Qt.Checked)
		mw_ui.export_excell_ui.products_list.addItem(item)


	rms=con.execute('select name,id from raw_materials').fetchall()
	for rm in rms:
		item = QtWidgets.QListWidgetItem()
		item.setData(2,rm[0])
		item.setData(4,rm[1])
		item.setData(5,'rm')
		item.setCheckState(QtCore.Qt.Checked)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/Raw materials.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon)
		mw_ui.rm_list.addItem(mw_ui.item)
		mw_ui.export_excell_ui.rm_list.addItem(item)




	rms=con.execute('select name,id from packing_materials').fetchall()
	for rm in rms:
		item = QtWidgets.QListWidgetItem()
		item.setData(2,rm[0])
		item.setData(4,rm[1])
		item.setData(5,'pm')
		item.setCheckState(QtCore.Qt.Checked)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/Packing materials.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		item.setIcon(icon)
		mw_ui.rm_list.addItem(mw_ui.item)
		mw_ui.export_excell_ui.rm_list.addItem(item)




	mw_ui.export_excell_ui.product_frame.setEnabled(0)
	mw_ui.export_excell_ui.rm_frame.setEnabled(0)


	# connections

	select_section_e_e( mw_ui.export_excell_ui ,1,0)
	mw_ui.export_excell_ui.products.clicked.connect(lambda :select_section_e_e ( mw_ui.export_excell_ui ,1,0))
	mw_ui.export_excell_ui.raw_materials.clicked.connect(lambda: select_section_e_e ( mw_ui.export_excell_ui ,0,1))
	mw_ui.export_excell_ui.export_button.clicked.connect(lambda:export_excell ( mw_ui.export_excell_ui ))
	mw_ui.export_excell_ui.cancel.clicked.connect( lambda: mw_ui.export_excell.close() )



#####################################################
############ backup windows ##########################
#####################################################
#>


def open_backup_settings(mw_ui):




	mw_ui.backup_settings_window = QtWidgets.QDialog()
	mw_ui.backup_settings_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.backup_settings_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.backup_settings_ui = uic.loadUi('windows/backup_settings_window.ui', mw_ui.backup_settings_window)
	mw_ui.backup_settings_ui.setStyleSheet(mw_ui.current_style)

	retranslateBackupSettingsWindow(mw_ui.backup_settings_ui,mw_ui.current_language)
	mw_ui.backup_settings_window.setWindowTitle(mw_ui.current_language['Edit Order'])
	if mw_ui.current_language_name=='arabic':
		mw_ui.backup_settings_ui.setLayoutDirection(QtCore.Qt.RightToLeft)
	else:
		mw_ui.backup_settings_ui.setLayoutDirection(QtCore.Qt.LeftToRight)



	con=sq.connect(mw_ui.main_data_base)
	settings=con.execute('select backup_type , backup_year_time , backup_month_time , backup_day_time , backup_hour_time , location from backup_settings').fetchall()
	mw_ui.backup_settings_ui.manual_backup.setChecked(1)
	mw_ui.backup_settings_ui.auto_backup_frame.setEnabled(0)

	if len(settings)!=0:
		settings=settings[0]


		if settings[0] == 'AUTO':
			mw_ui.backup_settings_ui.auto_backup.setChecked(1)
			mw_ui.backup_settings_ui.auto_backup_frame.setEnabled(1)
			mw_ui.backup_settings_ui.auto_backup_path.setText(settings[5])


		mw_ui.backup_settings_ui.year_count.setValue(int(settings[1]))
		mw_ui.backup_settings_ui.month_count.setValue(int(settings[2]))
		mw_ui.backup_settings_ui.day_count.setValue(int(settings[3]))
		mw_ui.backup_settings_ui.hour_count.setValue(int(settings[4]))

	last_backup=con.execute('select date from backups').fetchall()
	if len(last_backup)>0:
		l=last_backup[-1][0][:16].replace('T',' (')+')'
		mw_ui.backup_settings_ui.last_backup_label.setText(f'Last backup : {l}')
	else:
		mw_ui.backup_settings_ui.last_backup_label.setText('')

	def save_settings():
		key1=''
		value1=''
		data=''
		if mw_ui.backup_settings_ui.auto_backup.isChecked():
			backup_type='AUTO'
			key1=', location'
			value1=', "'+mw_ui.backup_settings_ui.auto_backup_path.text()+'"'

		else:
		 	backup_type='MANUAL'

		if len(settings)==0:
			con.execute(f'insert into backup_settings (backup_type,backup_year_time , backup_month_time , backup_day_time , backup_hour_time {key1}) values ("{backup_type}" ,{mw_ui.backup_settings_ui.year_count.value()} ,{mw_ui.backup_settings_ui.month_count.value()},{mw_ui.backup_settings_ui.day_count.value()},{mw_ui.backup_settings_ui.hour_count.value()} {value1})')
			con.commit()

		else:
			if backup_type=='AUTO':
				data=key1+'='+value1[1:]
			con.execute(f'update backup_settings  set backup_type="{backup_type}" , backup_year_time={mw_ui.backup_settings_ui.year_count.value()}, backup_month_time={mw_ui.backup_settings_ui.month_count.value()}, backup_day_time={mw_ui.backup_settings_ui.day_count.value()} , backup_hour_time={mw_ui.backup_settings_ui.hour_count.value()}  {data} ')
			con.commit()

		mw_ui.backup_settings_window.close()


	def select_file_path():
		master = Tk()
		master.withdraw()
		return filedialog.asksaveasfilename( title='save backup' , filetypes=(('backup files','*.insppb'),))

	def select_folder_path():
		master = Tk()
		master.withdraw()
		return filedialog.askdirectory( title='save backup' )

	mw_ui.backup_settings_ui.view_folders.clicked.connect(lambda:mw_ui.backup_settings_ui.auto_backup_path.setText(select_folder_path()))
	mw_ui.backup_settings_ui.view_files.clicked.connect(lambda:mw_ui.backup_settings_ui.path.setText(select_file_path()))
	mw_ui.backup_settings_ui.manual_backup.clicked.connect(lambda: mw_ui.backup_settings_ui.auto_backup_frame.setEnabled(0))
	mw_ui.backup_settings_ui.auto_backup.clicked.connect(lambda: mw_ui.backup_settings_ui.auto_backup_frame.setEnabled(1))
	mw_ui.backup_settings_ui.manual_backup.clicked.connect(lambda: mw_ui.backup_settings_ui.frame_2.setEnabled(1))
	mw_ui.backup_settings_ui.auto_backup.clicked.connect(lambda: mw_ui.backup_settings_ui.frame_2.setEnabled(0))

	def c_b():
		functions.create_backup(mw_ui.backup_settings_ui.path.text(),mw_ui)
		mw_ui.backup_settings_window.close()

	mw_ui.backup_settings_ui.backup.clicked.connect(lambda: c_b() if mw_ui.backup_settings_ui.path.text()!='' else mw_ui.backup_settings_ui.path.setStyleSheet('border-color:rgb(255,0,0);'))
	mw_ui.backup_settings_ui.ok.clicked.connect(lambda:save_settings() if  mw_ui.backup_settings_ui.manual_backup.isChecked() or (mw_ui.backup_settings_ui.auto_backup.isChecked() and mw_ui.backup_settings_ui.auto_backup_path.text()!='' ) else mw_ui.backup_settings_ui.auto_backup_path.setStyleSheet('border-color:rgb(255,0,0);'))


	mw_ui.backup_settings_window.show()


def open_import_backup(mw_ui , path):


	mw_ui.import_backup_window =  QtWidgets.QDialog()
	mw_ui.import_backup_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.import_backup_ui = uic.loadUi('windows/import_backup_window.ui', mw_ui.import_backup_window)
	mw_ui.import_backup_ui.setStyleSheet(mw_ui.current_style)
	con=sq.connect(path)
	mw_ui.import_backup_ui.products_count.setText(str(con.execute('select count(*) from products').fetchall()[0][0]))
	mw_ui.import_backup_ui.raw_materials_count.setText(str(con.execute('select count(*) from raw_materials').fetchall()[0][0]))
	mw_ui.import_backup_ui.packing_materials_count.setText(str(con.execute('select count(*) from packing_materials').fetchall()[0][0]))
	mw_ui.import_backup_ui.orders_count.setText(str(con.execute('select count(*) from orders').fetchall()[0][0]))

	def import_backup_f():
		mw_ui.import_backup_ui.loading_gif.setText('loading...')
		con_main_db=sq.connect(mw_ui.main_data_base)

		for table in mw_ui.backup_tables.keys():
			con_main_db.execute(f'delete from {table}')
			new_data=con.execute(f'select {mw_ui.backup_tables[table]} from {table}').fetchall()
			for i in new_data:
				con_main_db.execute(f'insert into {table} ({mw_ui.backup_tables[table]}) values {str(i)}')
			con_main_db.commit()
		mw_ui.import_backup_window.close()
		functions.view_data(mw_ui)
		mw_ui.import_backup_ui.loading_gif.setText('')
		open_success_msg(mw_ui , 'Backup imported successfully' , f'Backup imported successfully \n from: {path}'  )

	mw_ui.import_backup_ui.import_b.clicked.connect(import_backup_f)

	def view_backup_data():
		mw_ui.import_backup_ui.loading_gif.setText('loading...')
		mw_ui.main_data_base=path
		functions.view_data(mw_ui)
		mw_ui.import_backup_ui.loading_gif.setText('')
	mw_ui.import_backup_ui.view_data.clicked.connect(view_backup_data)

	def cancel_importing():
		mw_ui.import_backup_ui.loading_gif.setText('loading...')
		mw_ui.main_data_base='main.db'
		functions.view_data(mw_ui)
		mw_ui.import_backup_ui.loading_gif.setText('')

	mw_ui.import_backup_ui.cancel.clicked.connect(cancel_importing)

	#mw_ui.import_backup_ui.movie = QMovie("icons/loading.gif")
	#mw_ui.import_backup_ui.loading_gif.setMovie(mw_ui.import_backup_ui.movie)


	mw_ui.import_backup_window.show()


#############################################
############# INS Windows ###################
#############################################


def open_login_window(mw_ui ):



	mw_ui.INS_login_window =  QtWidgets.QDialog()
	mw_ui.INS_login_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.INS_login_ui = uic.loadUi('windows/INS_login_window.ui', mw_ui.INS_login_window)
	mw_ui.INS_login_ui.setStyleSheet(mw_ui.current_style)
	mw_ui.login_GIF = QMovie("GIFs/connecting.gif")
	mw_ui.success_GIF = QMovie("GIFs/success.gif")
	mw_ui.INS_login_ui.label_4.setMovie(mw_ui.login_GIF)
	mw_ui.INS_login_ui.label_4.setMargin(14)
	mw_ui.login_GIF.start()
	mw_ui.success_GIF.start()
	mw_ui.INS_login_ui.label_4.setMovie(None)



	mw_ui.INS_login_ui.password = PasswordEdit(mw_ui.INS_login_ui.frame)
	mw_ui.INS_login_ui.password.setMinimumSize(QtCore.QSize(145, 24))
	mw_ui.INS_login_ui.password.setMaximumSize(QtCore.QSize(155, 24))
	mw_ui.INS_login_ui.password.setEchoMode(QtWidgets.QLineEdit.Password)
	mw_ui.INS_login_ui.password.setPlaceholderText("")
	mw_ui.INS_login_ui.password.setObjectName("password")
	mw_ui.INS_login_ui.gridLayout.addWidget(mw_ui.INS_login_ui.password, 4, 1, 1, 3)



	FORMAT='utf-8'
	HEADER=64



	mw_ui.client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	mw_ui.INS_login_window.show()
	threading.Thread(target=INS.scan ,args=(mw_ui,)).start()
	mw_ui.INS_login_ui.login.clicked.connect(lambda:INS.send_login_data(mw_ui))
	mw_ui.INS_login_ui.scan.clicked.connect(lambda:threading.Thread(target=INS.scan,args=(mw_ui,)).start())
	print(dir(mw_ui.INS_login_ui.scan))



def open_login_success_window(mw_ui ):



	mw_ui.INS_login_successfully_window =  QtWidgets.QDialog()
	mw_ui.INS_login_successfully_window.setWindowModality(QtCore.Qt.ApplicationModal)

	mw_ui.INS_login_success_ui = uic.loadUi('windows/INS_login_success_window.ui', mw_ui.INS_login_successfully_window)
	mw_ui.INS_login_success_ui.setStyleSheet(mw_ui.current_style)

	def disconnect():
		mw_ui.client.close()
		mw_ui.INS_login_successfully_window.close()


	mw_ui.INS_login_success_ui.host_status.valueChanged.connect(disconnect)
	mw_ui.INS_login_successfully_window.show()
