from PyQt5.QtWidgets import QApplication, QPushButton, QPlainTextEdit, QMainWindow, QScrollArea, QWidget, QLabel
import sys
#https://www.color-hex.com/color-palette/28392
class appWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
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

        #create the send button
        self.button = QPushButton("", self) 
        self.button.clicked.connect(self.send_message)
        self.button.setGeometry(1116, 708, 64, 64) 
        self.button.setStyleSheet("background-image : url(resources/images/send-message.png);") 

        #create the chat window
        self.chat = QScrollArea(self)
        self.chat.move(20, 20)
        self.chat.resize(1160, 650)
        self.chat.setStyleSheet("background-color: #80b2a3; font-size: 20px; border-radius: 10px; padding: 10px")

        #sample message
        self.message = QLabel(self.chat)
        self.message.setText("Hello")
        self.message.move(20, 20)
        self.message.setStyleSheet("background-color: #90d2c3; font-size: 20px; color: #ffffff; border-radius: 10px; padding: 10px; border: 2px solid #ffffff;")

        #sample message2        
        self.message2 = QLabel(self.chat)
        self.message2.setText("Hello")
        mwidth = self.message2.geometry().x()

        self.message2.move(1100-mwidth-40,50)
        self.message2.setStyleSheet("background-color: #70acb4; font-size: 20px; color: #ffffff; border-radius: 10px; padding: 10px; border: 2px solid #ffffff;")

        self.show()
        sys.exit(app.exec_())

    def send_message(self):
        print(self.textbox.toPlainText())
        self.textbox.setPlainText("")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = appWindow()
    