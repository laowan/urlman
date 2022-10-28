# -*- coding: UTF-8 -*-

from fileinput import filename
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QToolBar
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction
from PyQt5.QtWidgets import QListWidget, QFileDialog

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super(QMainWindow, self).__init__(parent)
        self.appName = "urlman"
        self.setWindowTitle(self.appName)
        self.resize(640, 640)
        self.listWidget = QListWidget()
        self.setCentralWidget(self.listWidget)
        self.addItems()
        self.createMenuBar()
        self.createToolBars()

    def createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")
        
    def createToolBars(self):
        fileToolBar = self.addToolBar("File")
        #editToolBar = QToolBar("Edit", self)
        self.addToolBar(editToolBar)
        #helpToolBar = QToolBar("Help", self)
        #self.addToolBar(Qt.LeftToolBarArea, helpToolBar)

    def addItems(self):
        self.listWidget.addItem('aaaa')
        self.listWidget.addItem('bbbb')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())