from PyQt5.QtWidgets import QApplication, QWidget, QLabel
import sys

def createWindow():
   app = QApplication(sys.argv)
   w = QWidget()
   b = QLabel(w)
   b.setText("Chat helye")
   w.setGeometry(100,100,200,50)
   b.move(50,20)
   w.setWindowTitle("PyQt5")
   w.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    createWindow()
    