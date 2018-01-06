# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets, uic

import sys
import time
import socket
import select


port = '9009'
host = 'localhost'
qtCreatorFile = "widget.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.Chat_reader.setReadOnly(True)
        self.Chat_reader.setText("Welcome to Quade's LAN-Chatter")
        self.name = ''
        
        
        self.clear_chat.clicked.connect(lambda: window.Chat_reader.clear())
        self.Set_button.clicked.connect(self.chat_connect)
        self.red = ""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        #inputs controls
        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        self.show()



    def recurring_timer(self):
        self.red = self.chat_input.toPlainText()
        
        msg = self.name + ": " + self.red[:-1]

        #pushes things to the chat box and server
        if self.red.endswith("\n"):
            self.Chat_reader.append(msg)
            try:
                self.s.send(msg)
            except:
                self.Chat_reader.append("Failed to send message")


            self.chat_input.clear()
        
        #limits length of message
        if len(self.red) >= 25:
            self.chat_input.setText(self.red[:24])



    def chat_connect(self):
        self.name = self.Chat_name.toPlainText()
        port = self.Port_location.toPlainText()
        

        #connection to remote host

        try :
            self.s.connect((host, int(port)))
        except :
            self.Chat_reader.append('Unable to connect') 
            print(dir(self.update.stop))
            return
        self.Chat_reader.append('Connected to remote host. You can start sending messages') 

        #setting up interval to read messages
        self.update = QtCore.QTimer()
        self.update.setInterval(1000)
        self.update.timeout.connect(self.updater)
        self.update.start()

        

    def updater(self):
        '''
        select.select needs a file entity to operate so instead of 
        sys.stdin which requires terminal entry
        created a small file that negates that
        not ideal solution though

        '''
        f = open('test.txt', 'r')
        socket_list = [self.s,f]
        ready_to_read,ready_to_write,in_error = select.select(
        socket_list , [], [])
        

        
        for sock in ready_to_read:
            if sock == self.s:
                data = sock.recv(4096)
                if not data :
                    self.Chat_reader.append('Disconnected from chat server')
                    self.update.stop()
                    return
                else :
                    #print data
                    self.Chat_reader.append(data)

            else: 
                pass
                #user input
                    




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    
    sys.exit(app.exec_())
    

