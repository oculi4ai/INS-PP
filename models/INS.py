
import sys, sh, socket, threading, time
from PyQt5 import QtCore, QtGui, QtWidgets 
import models.windows_open as windows

def add_network(ip_addr ,mw_ui ):
		item = QtWidgets.QListWidgetItem()
		item.setData(4,str(ip_addr))
		try:
			item.setData(2,socket.gethostbyaddr(ip_addr)[0])
		except:
			item.setData(2,'unknown host name')
		
		mw_ui.INS_login_ui.networks.addItem(item)
		print(f'finding network {ip_addr}')

def scan(mw_ui):
	    mw_ui.checked_ip=0
	    mw_ui.INS_login_ui.networks.clear()

	    mw_ui.INS_login_ui.label.setText('Searching for INS server...')
	    mw_ui.INS_login_ui.label_4.setMovie(mw_ui.login_GIF)
	    base_ip_address='.'.join(socket.gethostbyname(socket.gethostname()).split('.')[:3])
	    networks=[]

	    def pingloop(num):
	        ip = base_ip_address+'.'+str(num)  
	          
	        try:  
	            sh.ping(ip, "-c 1",_out="/dev/null")  
	            
	            try:
	            	print(f'pinged {ip} ')
	            	mw_ui.client.connect((ip,5555))
	            	mw_ui.client.shutdown(socket.SHUT_RDWR)
	            	mw_ui.client.close()
	            	print(f'hosting {ip} ')
	            	networks.append(ip)
	               	

	            except: 
	                pass

	        except:  
	            pass
	        mw_ui.checked_ip+=1

		

	    

	    for i in range(10,200):
	        a1=threading.Thread(target=pingloop , args=(i,))
	        a1.start()
	    while mw_ui.checked_ip<189:
	    	pass
	    for network in networks:
	    	add_network(network , mw_ui)
	    mw_ui.INS_login_ui.label.setText('')

	    mw_ui.INS_login_ui.label_4.clear()

def send(msg ,client ):
		FORMAT='utf-8'
		message = msg.encode(FORMAT)
		msg_length = len(message)
		send_length = str(msg_length).encode(FORMAT)
		send_length += b' ' * (64 - len(send_length))
		client.send(send_length)
		client.send(message)


def send_login_data(mw_ui ):
		FORMAT='utf-8'
		mw_ui.client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print((mw_ui.INS_login_ui.networks.currentItem().data(4),5555))
		mw_ui.client.connect((mw_ui.INS_login_ui.networks.currentItem().data(4),5555))
		mw_ui.INS_login_ui.label.setText('Loading')
		mw_ui.INS_login_ui.label_4.setMovie(mw_ui.login_GIF)
		def send_data():

			message =f'{mw_ui.INS_login_ui.username.text()},{mw_ui.INS_login_ui.password.text()}'
			send(message ,mw_ui.client )
			msg = mw_ui.client.recv(3).decode(FORMAT)
			print(msg)
			
			if msg=='1.1':
				mw_ui.INS_login_ui.label.setText('You are loged in')
				mw_ui.INS_login_ui.label_4.setMovie(mw_ui.success_GIF)
				mw_ui.INS_login_window.close()
				windows.open_login_success_window(mw_ui)
				mw_ui.INS_login_success_ui.host_status.hide()

			else:
				mw_ui.INS_login_ui.label.setText('Access denied')
				mw_ui.INS_login_ui.label_4.setPixmap(QtGui.QPixmap("icons/access_d.png"))
		threading.Thread(target=send_data).start()

		

def check_INS_status(mw_ui):
	try:
		servername=mw_ui.client.getpeername()
		send('test' ,mw_ui.client)
		send('test' ,mw_ui.client)
		return servername
	except:
		return False