
################## green black
#18191d
#3d444b
#3fc1b0
#282e33

################## blue black
#0e1621
#242f3d
#5288c1
#17212b

################## white

#74b4e0
#f1f1f1
#419fd9
#ffffff






###########################################################

##################blue black
#0e1621
#242f3d
#5288c1
#17212b
dark_blue_style='''
/* ############ color 1 ############# */
QListWidget,#frame_29,#frame_49,#frame_40, QWidget,QTabBar::tab{
background-color: #0e1621 ;
}

/* ############ color 2 ############# */

#menuBar,#frame_2 ,
QTabBar::tab:selected, QTabBar::tab:hover ,QHeaderView {
	background-color: #242f3d;
}
#frame,#units_frame,#rm_frame,#frame_4{

background-color:#17212b;

}
#add_rm,#add_pm{
border-color:#17212b;

}
/* ############ color 3 ############# */
QToolButton:pressed,QPushButton:pressed,QToolTip {
background-color: #2b5278;

}

/* ############ color 4 ############# */

QLineEdit , QPushButton , QToolButton , QListWidget , QListWidget::item ,QListWidget::item:selected , QPushButton , QSpinBox ,  QComboBox  , QDateEdit
,#frame_7 ,#frame_9,QTextEdit,QProgressBar,QTableView,QToolTip
{border: 2px solid #242f3d;
}
QTableWidget{
	gridline-color: 2px solid #242f3d;

}
QTableView::item:selected,
QScrollBar:handle,QListWidget:item:hover,#products_list::item:selected
{
background-color: #5288c1 ;

}

/* ############ font color  ############# */

QWidget,QListWidget::item:selected{
color:rgb(200,200,200);

}

QToolButton,QPushButton,QListWidget:item{
	background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(89, 89, 89, 0));
}
'''

##########green black
#18191d background
#3d444b	navbar fonr
#3fc1b0 titles selected item check box
#282e33 unselected item
dark_green_style='''
/* ############ color 1 ############# */
QListWidget,#frame_29,#frame_49,#frame_40, QWidget,QTabBar::tab{
background-color: #18191d ;
}

/* ############ color 2 ############# */

#menuBar,#frame_2 ,
QTabBar::tab:selected, QTabBar::tab:hover ,QHeaderView {
	background-color: #3d444b;
}
#frame,#units_frame,#rm_frame,#frame_4{

background-color:#282e33;

}
#add_rm,#add_pm{
border-color:#17212b;

}
/* ############ color 3 ############# */
QToolButton:pressed,QPushButton:pressed,QToolTip {
background-color: #2b5278;

}

/* ############ color 4 ############# */

QLineEdit , QPushButton , QToolButton , QListWidget , QListWidget::item ,QListWidget::item:selected, QPushButton , QSpinBox ,  QComboBox  , QDateEdit
,#frame_7 ,#frame_9,QTextEdit,QProgressBar,QTableView,QToolTip
{border: 2px solid #3d444b;
}
QTableWidget{
	gridline-color: 2px solid #3d444b;

}
QTableView::item:selected,
QScrollBar:handle,QListWidget:item:hover,#products_list::item:selected
{
background-color: #3fc1b0 ;

}

/* ############ font color  ############# */

QWidget,QListWidget::item:selected{
color:rgb(200,200,200);

}

QToolButton,QPushButton,QListWidget:item{
	background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(89, 89, 89, 0));
}
'''




#################### white

#74b4e0 background
#f1f1f1 navbar fonr
#419fd9 selected titles selected item check box
#ffffff unselected items


white_style='''

/* ############ color 1 ############# */
QListWidget,#frame_29,#frame_49,#frame_40, QWidget,QTabBar::tab{
background-color: #f1f1f1 ;
}

/* ############ color 2 ############# */

#menuBar,#frame_2 ,
QTabBar::tab:selected, QTabBar::tab:hover ,QHeaderView,
#frame,#units_frame,#rm_frame,#frame_4{

background-color:#206087;

}

/* ############ color 3 ############# */
QToolButton:pressed,QPushButton:pressed,QToolTip {
background-color: #2b5278;

}

/* ############ color 4 ############# */

QLineEdit , QPushButton , QToolButton , QListWidget , QListWidget::item,QListWidget::item:selected , QPushButton , QSpinBox ,  QComboBox  , QDateEdit
,#frame_7 ,#frame_9,QTextEdit,QProgressBar,QTableView,QToolTip
{border: 2px solid #419fd9;
}
QTableWidget{
	gridline-color: 2px solid #f1f1f1;

}
QTableView::item:selected,
QScrollBar:handle,QListWidget:item:hover,#products_list::item:selected
{
background-color: #419fd9 ;

}

/* ############ font color  ############# */

QWidget,QListWidget::item:selected{
color:rgb(10,10,10);

}

QToolButton,QPushButton{
	background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(50, 50, 50, 0.5));
}
#label,#label_6,#label_18,#label_10,#label_14{
color:rgb(255,255,255);
}
'''



main_style='''
/* ############ main tap widget ############# */
#frame,#frame_2,#frame,#units_frame,#rm_frame,#frame_4{
border-radius: 10px;}


QTabWidget::pane {
    border-top: 0px solid #C2C7CB;
}
QTabWidget::tab-bar {
    left: 20px;
margin-left:20px;
margin-right:20px;
}
QTabBar::tab {

    border: 0px solid rgb(0, 0, 0);
    min-width: 100px;
    padding: 09px;
	border-bottom-right-radius: 15px;
	border-bottom-left-radius: 15px;

}
#frame_54,QProgressBar,QLineEdit{
background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.243781 rgba(62, 62, 62, 0));
}
QTabBar::tab:selected, QTabBar::tab:hover {

border-bottom-right-radius: 15px;
border-bottom-left-radius: 15px;


}


QTabBar::tab:selected {
    border: 0px solid rgb(0, 0, 0);
}
QTabBar::tab:!selected {
    margin-bottom: 4px;
}
QTabBar::tab:selected {
    margin-left: -0px;
    margin-right: -0px;
}


/* ####################### */

QLabel,QCheckBox{
background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.243781 rgba(62, 62, 62, 0));
}


QLineEdit , QPushButton , QToolButton , QListWidget::item ,QRadioButton, QPushButton , QSpinBox , QDoubleSpinBox ,  QComboBox  , QDateEdit
,#frame_7 ,#frame_9,QTextEdit,QProgressBar
{
padding-left:6px;
padding-right:6px;

background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0.243781 rgba(62, 62, 62, 0));

border-radius: 4px;

}
QListWidget,#frame_29,#frame_49,#frame_40
{padding:6px;
padding:6px;
border-radius: 10px;
}

QListWidget:item{
margin:2;
}
QListWidget{
border-width:0px;
}


QPushButton , QToolButton,QLineEdit,QComboBox,QDateEdit
,QSpinBox{border-radius: 10px;}


QComboBox::drop-down {

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid;
    border-top-right-radius: 3px;
}






QListWidget {
padding-top:8px;

}
 QPushButton , QToolButton{

padding:0px;
}



QScrollBar{
width:5px;}


QScrollBar:hover{
width:10px;}




QHeaderView::section {

    padding: 4px;
    border-style: none;
	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0));

}



QTableView QTableCornerButton::section {

	color: rgb(255, 255, 255);
	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 0));


}
QTableView {
 border: 0px ;
    border-width: 10px ;
}



QToolTip{
border-radius: 7px;
border-width: 1px ;
}


QPushButton , QToolButton{ padding:5px;border-width:2px;}


QScrollBar::sub-page ,QScrollBar::add-page{
	background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 0));}

QScrollBar:vertical{
width:8px;
}

QScrollBar:horizontal{
height:8px;
}


QScrollBar:handle
{

border-radius: 4px;
}
 QListWidget::item {
border-width: 1px;
height:30px;

 }
QScrollBar::add-line ,QScrollBar::sub-line
{
      border: none;
      background: none;
      color: none;
}

#frame,#units_frame,#rm_frame,#frame_4{
border: 0px solid #f1f1f1;


}
QListView {
    outline: 0;
}


'''


styles={
	'Dark green':dark_green_style,
	'Dark blue':dark_blue_style,
	'White':white_style
}
