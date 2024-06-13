from PyQt5.QtWidgets import QApplication, QPushButton, QPlainTextEdit, QMainWindow, QScrollArea, QLabel, QSizePolicy, QWidget, QVBoxLayout, QGridLayout, QSpacerItem, QTextEdit
from PyQt5.QtCore import Qt, QRunnable, pyqtSlot,  QThread, pyqtSignal, QTimer

import sys
import time
import messager as m
#https://www.color-hex.com/color-palette/28392


class Worker(QThread):
    responseGenerated = pyqtSignal((str,str))

    def __init__(self, text, side, num_messages):
        super(Worker, self).__init__()
        self.text = text
        self.side = side
        self.num_messages = num_messages
        self.messageManager = m.messageManager()

    @pyqtSlot()
    def run(self):
        print("running")
        if(self.side == "left"):
            self.get_message(self.text)
        else:
            self.send_message(self.text)

    def add_message(self,text,side):
        print("returning side and message")
        self.responseGenerated.emit(text,side)

    def send_message(self,text):
        if text == "":
            return
        self.add_message(text,"right")
        

    def get_message(self,text):
        res = self.messageManager.generate_response(text)
        self.add_message(res,"left")
        

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
        self.vbox = QVBoxLayout()
        self.vbox.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


        self.scroller.setWidgetResizable(True)
        self.scroller.move(20,20)
        self.scroller.resize(1160,650)
        self.scroller.setMinimumHeight(300)
        self.scroller.setFixedWidth(1160)
        self.scroller.setStyleSheet("background-color: #80b2a3; border-radius: 10px;")
        #self.scroller.verticalScrollBar().valueChanged.connect(lambda x:print(self.scroller.verticalScrollBar().value()))

        self.chat.move(20, 20)
        self.chat.setMinimumWidth(1120)
        self.chat.setMinimumHeight(650)
        
        self.chat.setStyleSheet("background-color: #80b2a3; font-size: 20px; border-radius: 10px; padding: 10px; height: auto")
        self.chat.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        #create the send button
        self.button = QPushButton("", self) 
        self.button.clicked.connect(self.handle_button_click)
        self.button.setGeometry(1116, 708, 64, 64) 
        self.button.setStyleSheet("background-image : url(resources/images/send-message.png);") 

        #sample message
        self.message = QLabel("Hello, welcome to my app! I am a recipe summarizer. I can help you summarize recipes and make them easier to follow. Just paste in a link to a recipe and I will do the rest!")
        self.message.setWordWrap(True)
        self.message.setStyleSheet("background-color: #90d2c3; font-size: 30px; color: #ffffff; border-radius: 10px; border: 2px solid #ffffff; max-width: 600px; ")

        #add the message to the chat
        self.vbox.addWidget(self.message)
        self.num_messages += 1

        #setup correct size and layout
        self.message.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.chat.setLayout(self.vbox)
        self.scroller.setWidget(self.chat)
        

    def handle_button_click(self):
        text = self.textbox.toPlainText().strip()
        if text:
            self.communication(text) 
    
    def communication(self,text):
        worker1 = Worker(text,"right",self.num_messages)
        #worker1.finished.connect(lambda:self.vbox.addWidget(worker1.message,self.num_messages,0,Qt.AlignRight))
        worker1.finished.connect(lambda:worker1.quit())
        worker1.responseGenerated.connect(self.handle_response,Qt.QueuedConnection)

        worker2 = Worker(text,"left",self.num_messages)
        #worker2.finished.connect(lambda:self.vbox.addWidget(worker2.message,self.num_messages,1,Qt.AlignLeft))
        worker2.finished.connect(lambda:worker2.quit())
        worker2.responseGenerated.connect(self.handle_response,Qt.QueuedConnection)
        
        worker1.start()
        worker2.start()

        

    def handle_response(self,text,side):
        print(text,side)

        message = QLabel(text)

        #correct style
        
        if(side == "left"):
            message.setStyleSheet("background-color: #90d2c3; font-size: 30px; color: #ffffff; border-radius: 10px; border: 2px solid #ffffff; padding: 10px;")
        else:
            message.setStyleSheet("background-color: #70acb4; font-size: 30px; color: #ffffff; border-radius: 10px; border: 2px solid #ffffff; padding: 10px;")
        
        message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            

        #setup correct size
        #message.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        message.setWordWrap(True)
        
        message.setMinimumHeight(80)
        message.setMaximumHeight(4000)      
        print(self.num_messages) 
        print("szelesseg",message.sizeHint().width())
        print("magassag",message.sizeHint().height())

        message.setFixedWidth(message.sizeHint().width()+20)
        message.setFixedHeight(message.sizeHint().height()+20)       
        print("valodi",message.width(),message.height())

        self.textbox.setPlainText("")
        if side == "left":
            self.vbox.addWidget(message,alignment=Qt.AlignLeft)
        else:
            self.vbox.addWidget(message,alignment=Qt.AlignRight)
        
        #self.vbox.addWidget(label,self.num_messages,1,Qt.AlignRight)
        self.num_messages += 1  
        self.scroller.updateGeometry()
        QApplication.processEvents()
        QTimer.singleShot(0, lambda: self.scroller.verticalScrollBar().setValue(self.scroller.verticalScrollBar().maximum()))

        print("done")
        

        
        
if __name__ == '__main__':
    APP = QApplication(sys.argv)
    APP.setStyle('Fusion')
    window = appWindow()
    window.show()
    sys.exit(APP.exec_())    