from PyQt5.QtWidgets import QApplication, QPushButton, QPlainTextEdit, QMainWindow, QScrollArea, QLabel, QSizePolicy, QWidget, QGridLayout
from PyQt5.QtCore import Qt

import sys
import time
#https://www.color-hex.com/color-palette/28392


class appWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.prev_message_y = 20
        self.num_messages = 0
        
        
        #create a fixed size window
        self.setWindowTitle("Recipe summarizer")
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
        self.setStyleSheet("background-color: #7573b6;")
        

        #create the input textbox
        self.textbox = QPlainTextEdit(self)
        self.textbox.move(20, 680)
        self.textbox.resize(1050,100)
        self.textbox.setStyleSheet("background-color: #70acb4; font-size: 20px; color: #ffffff; border-radius: 10px; padding: 10px; border: 2px solid #ffffff;")

        #create the chat window
        self.scroller = QScrollArea(self)
        self.chat = QWidget(self.scroller)
        self.vbox = QGridLayout()
        self.vbox.setSpacing(20)


        self.scroller.setWidgetResizable(True)
        self.scroller.move(20,20)
        self.scroller.resize(1160,650)
        self.scroller.setMinimumHeight(300)
        self.scroller.setFixedWidth(1160)
        self.scroller.setStyleSheet("background-color: #80b2a3; border-radius: 10px;")

        self.chat.move(20, 20)
        self.chat.setMinimumWidth(1120)
        self.chat.setMinimumHeight(650)
        
        self.chat.setStyleSheet("background-color: #80b2a3; font-size: 20px; border-radius: 10px; padding: 10px; height: auto")
        self.chat.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        #create the send button
        self.button = QPushButton("", self) 
        self.button.clicked.connect(lambda x:self.communication_lol(self.textbox.toPlainText()))
        self.button.setGeometry(1116, 708, 64, 64) 
        self.button.setStyleSheet("background-image : url(resources/images/send-message.png);") 

        #sample message
        self.message = QLabel("Hello, welcome to my app! I am a recipe summarizer. I can help you summarize recipes and make them easier to follow. Just paste in a link to a recipe and I will do the rest!")
        self.message.setWordWrap(True)
        self.message.setStyleSheet("background-color: #90d2c3; font-size: 30px; color: #ffffff; border-radius: 10px; border: 2px solid #ffffff; max-width: 600px; ")
        #self.message.move(20, self.prev_message_y+20)
        self.vbox.addWidget(self.message,0,0,1,1,Qt.AlignLeft)
        self.num_messages += 1
        self.message.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.chat.setLayout(self.vbox)
        #self.prev_message_y += (20 + self.message.height())
        self.scroller.setWidget(self.chat)
        

    def send_message(self):
        print(self.textbox.toPlainText())
        self.textbox.setPlainText("")
    
    def communication_lol(self,text):
        if text == "":
            return
        self.add_message(text,"right")
        self.add_message("I am a bot","left")

    def add_message(self,text,side):
        message = QLabel(text)

        #correct style
        if(side == "left"):
            message.setStyleSheet("background-color: #90d2c3; font-size: 30px; color: #ffffff; border-radius: 10px; padding: 10px; border: 2px solid #ffffff; max-width: 600px;")
            self.vbox.addWidget(message,self.num_messages,0,Qt.AlignLeft)
        else:
            self.vbox.addWidget(message,self.num_messages,1,Qt.AlignRight)
            message.setStyleSheet("background-color: #70acb4; font-size: 30px; color: #ffffff; border-radius: 10px; padding: 10px; border: 2px solid #ffffff; max-width: 600px;")
        #setup correct size
        message.setWordWrap(True)
        message.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.num_messages += 1 
        
        self.textbox.setPlainText("")
        print(self.chat.height())
    
        self.scroller.verticalScrollBar().setValue(self.scroller.verticalScrollBar().maximum())

        
if __name__ == '__main__':
    APP = QApplication(sys.argv)
    APP.setStyle('Fusion')
    window = appWindow()
    window.show()
    sys.exit(APP.exec_())
    