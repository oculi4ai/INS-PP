import sqlite3 as l
a=l.connect('main.db')
for i in a.execute('select * from history').fetchall():
	print(i)
