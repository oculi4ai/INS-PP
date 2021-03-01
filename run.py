from PyQt5 import QtCore, QtGui, QtWidgets, uic
from models import functions
import sys
from types import MethodType
import threading
from PyQt5.QtWidgets import QApplication  ,QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt , QTimer , QThread
from models.styles import styles
app = QtWidgets.QApplication(sys.argv)


MainWindow = QtWidgets.QMainWindow()
ui2 =uic.loadUi('windows/main_window.ui', MainWindow)
ui2.main_data_base='main.db'

functions.init(ui2 ,MainWindow)

MainWindow.showMaximized()
MainWindow.show()

#ui2.setStyleSheet('')

ui2.backup_tables={
				'products' 				:'name,code,material_type',
				'raw_materials'			:'name,type,code,quantity,unit,density',
				'packing_materials'		:'name,code,quantity,unit',
				'product_raw_materials'	:'product_id,material_id,t_quantity,t_unit,m_quantity,m_unit, percentage',
				'orders'				:'name,product_id,quantity,unit_id,done,date_from,date_to',
				'backup_settings'		:'backup_type,backup_year_time , backup_month_time , backup_day_time , backup_hour_time ,location',
				'units'					:'name,product_id,value,unit_id,is_standard ',
				'material_types'		:'type,units_ids',
				'backups'				:'date,location'}



ui2.open=True

def exit_app():
	ui2.open=False



def closeEvent(self, event):
            close = QtWidgets.QMessageBox.question(self,
                                         "QUIT",
                                         "Are you sure want to QUIT?",
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
                for window in app.allWindows():

                    window.close()
            else:
                event.ignore()

MainWindow.closeEvent = MethodType(closeEvent,MainWindow)

app.aboutToQuit.connect(exit_app)
sys.exit(app.exec_())
