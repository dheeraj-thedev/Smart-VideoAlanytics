import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication


class Slides(QWidget):

    def __init__(self, image_files, parent=None):
        QWidget.__init__(self, parent)
        self.image_files = image_files
        s = '<>'*300
        self.label = QLabel(s, self)
        self.label.setGeometry(10, 30, 640, 480)
        self.button = QPushButton("Start Slide Show",self)
        self.button.setGeometry(10, 10, 140, 30)
        self.button.clicked.connect(self.timerEvent)
        self.timer = QBasicTimer()
        self.step = 0
        self.delay = 5000  # milliseconds
        sf = "Slides are shown {} seconds apart"
        self.setWindowTitle(sf.format(self.delay/10000.0))
    def timerEvent(self, e=None):
        if self.step >= len(self.image_files):
            self.timer.stop()
            self.button.setText('Slide Show Finished')
            return
        self.timer.start(self.delay, self)
        file = self.image_files[self.step]
        image = QPixmap(file)
        self.label.setPixmap(image)
        self.setWindowTitle("{} --> {}".format(str(self.step), file))
        self.step += 1
# pick image files you have in the working folder
# or give full path name

if __name__ == '__main__':
    f = []
    path = r'C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\output'
    for (dirpath, dirnames, filenames) in os.walk(path):
        f.extend(filenames)
        break
    nf = []
    for d in f:
        fPath = path + "\\" + d
        nf.append(fPath)
    print(nf)
    app = QApplication([])
    w = Slides(nf)
    # setGeometry(x, y, w, h)  x,y = upper left corner coordinates
    w.setGeometry(100, 100, 700, 500)
    w.show()
    app.exec_()