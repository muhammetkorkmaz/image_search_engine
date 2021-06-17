from PyQt5.QtWidgets import *
from design import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QScrollArea
import sys, os, cv2
import numpy as np
import pymongo
from pymongo import MongoClient
import re
import urllib.request as urllib2
from urllib.request import Request, urlopen
class interface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.text=None
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ui.setupUi(self)
        self.grid = QGridLayout()
        self.ui.label.setLayout(self.grid)
        self.list_img=[]
        self.ui.pushButton.clicked.connect(self.search)
        #self.create_labels(self.list_img)
    def search(self):
        self.text=self.ui.textEdit.toPlainText()
        self.get_img_database(self.text)
        if (len(self.text)!=0):
            self.list_img = self.get_img_database(self.text)
            if (len(self.list_img)==0):
                QMessageBox.warning(self, 'Error', 'There is no image about search key')
            else:
                self.create_labels(self.list_img)
        else:
            QMessageBox.warning(self, 'Error', 'There is no search key')
    def location(self,i):
        y=int(i/4)
        x=int(i%4)
        return x,y
    def create_labels(self,list):
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        for i in range(0,len(list)):
            label1=QLabel()
            label1.setAlignment(Qt.AlignCenter)
            req = Request(list[i],headers={'User-Agent': 'Mozilla/5.0'})
            url_data = urllib2.urlopen(req).read()
            self.pm = QPixmap() #.scaled(250, 250, Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.pm.loadFromData(url_data)
            label1.setPixmap(self.pm)
            x,y=self.location(i)
            self.grid.addWidget(label1, y, x)
    def get_img_database(self,key):
        cluster = MongoClient("mongodb+srv://muho:84437**ayt@cluster0.m6sqp.mongodb.net/muho?retryWrites=true&w=majority")
        db = cluster["muho"]
        collection = db["images"]
        regx = re.compile("{}".format(key), re.IGNORECASE)
        collections = collection.find({"caption": regx})
        url_list=[]
        for x in collections:
            if "https" in x["url"]:
                if (len(url_list)<20):
                    url_list.append(x['url'])
        return url_list

app = QtWidgets.QApplication(sys.argv)
window = interface()
window.show()
#sys.exit(app.exec())
app.exec_()
