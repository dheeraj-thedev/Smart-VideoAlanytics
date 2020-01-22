from datetime import datetime
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import glob

from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QPixmap, QImage

from webbasket.ui.darknetUtils import DarkNetUtils
from webbasket.ui.sort import Sort
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
                             QInputDialog, QApplication, QFileDialog, QWidget)

def cleanDirectory(path):
    files = glob.glob(path + '/*.png')
    for f in files:
        os.remove(f)

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def ccw(A, B, C):
    return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

class Ui_Dialog(QWidget):
    tracker = Sort()
    memory = {}
    # Dheeraj: Actual Line
    line = [(43, 543), (550, 655)]
    counter = 0

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(740, 480)
        Dialog.setStyleSheet("\n"
                             "background-color: rgb(41, 26, 199);")
        self.topWidget = QtWidgets.QWidget(Dialog)
        self.topWidget.setGeometry(QtCore.QRect(0, 20, 741, 61))
        self.topWidget.setStyleSheet("background-color: rgb(98, 0, 238);")
        self.topWidget.setObjectName("topWidget")
        self.groupBoxCheck = QtWidgets.QGroupBox(self.topWidget)
        self.groupBoxCheck.setGeometry(QtCore.QRect(190, 0, 541, 51))
        self.groupBoxCheck.setStyleSheet("color: rgb(255, 255, 255);")
        self.groupBoxCheck.setObjectName("groupBoxCheck")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBoxCheck)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 20, 101, 20))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_3 = QtWidgets.QLabel(self.groupBoxCheck)
        self.label_3.setGeometry(QtCore.QRect(16, 20, 101, 20))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.btnSearchNumberPlate = QtWidgets.QPushButton(self.groupBoxCheck)
        self.btnSearchNumberPlate.setGeometry(QtCore.QRect(240, 20, 61, 23))
        self.btnSearchNumberPlate.setStyleSheet(
            "background-color: qlineargradient(sprea Bd:pad, x1:0.068, y1:0.966, x2:1, y2:0, stop:0.414773 rgba(0, 0, 200, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "\n"
            "color: rgb(255, 255, 255);")
        self.btnSearchNumberPlate.setObjectName("btnSearchNumberPlate")
        self.label_2 = QtWidgets.QLabel(self.topWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 61, 61))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font: 75 20pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self.topWidget)
        self.label_4.setGeometry(QtCore.QRect(70, 10, 101, 41))
        self.label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                   "font: 75 20pt \"MS Shell Dlg 2\";\n"
                                   "color: rgb(72, 126, 225);")
        self.label_4.setObjectName("label_4")
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setGeometry(QtCore.QRect(0, 80, 741, 401))
        self.widget_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_2.setObjectName("widget_2")
        ## time on button Search
        self.btnSearchNumberPlate.clicked.connect(self.timerEvent)
        self.timer = QBasicTimer()
        self.step = 0
        self.delay = 5000  # milliseconds
        sf = "Slides are shown {} seconds apart"
        #self.setWindowTitle(sf.format(self.delay / 10000.0))


        #####
        s = '<>' * 300
        self.labelImage =QtWidgets.QLabel(self.widget_2)
        self.labelImage.setGeometry(10, 10, 422, 228)
        self.labelImage.setStyleSheet("background-color: rgb(204, 204, 204);")


        self.textEdit = QtWidgets.QTextEdit(self.widget_2)
        self.textEdit.setGeometry(QtCore.QRect(0, 270, 741, 131))
        self.textEdit.setStyleSheet("background-color: rgb(39, 125, 255);color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.widget = QtWidgets.QWidget(self.widget_2)
        self.widget.setGeometry(QtCore.QRect(0, 250, 741, 20))
        self.widget.setStyleSheet("background-color: rgb(98, 0, 238);\n"
                                  "")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(330, 0, 81, 21))
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.widget_2)
        self.groupBox.setGeometry(QtCore.QRect(440, 9, 291, 231))
        self.groupBox.setStyleSheet("border-color: rgb(222, 143, 46);\n"
                                    "background-color: rgb(21, 162, 255);")
        self.groupBox.setObjectName("groupBox")
        self.btnStart = QtWidgets.QPushButton(self.groupBox)
        self.btnStart.setGeometry(QtCore.QRect(40, 200, 221, 23))
        self.btnStart.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.068, y1:0.966, x2:1, y2:0, stop:0.414773 rgba(0, 0, 200, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "\n"
            "color: rgb(255, 255, 255);")
        self.btnStart.setObjectName("btnStart")
        self.cmbSelectProgram = QtWidgets.QComboBox(self.groupBox)
        self.cmbSelectProgram.setGeometry(QtCore.QRect(88, 30, 191, 22))
        self.cmbSelectProgram.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cmbSelectProgram.setObjectName("cmbSelectProgram")
        self.cmbSelectProgram.addItem("")
        self.cmbSelectProgram.addItem("")
        self.cmbSelectProgram.addItem("")
        self.lblSelectWay = QtWidgets.QLabel(self.groupBox)
        self.lblSelectWay.setGeometry(QtCore.QRect(20, 30, 71, 21))
        self.lblSelectWay.setObjectName("lblSelectWay")
        self.lblSelectVideo = QtWidgets.QLabel(self.groupBox)
        self.lblSelectVideo.setGeometry(QtCore.QRect(20, 60, 71, 21))
        self.lblSelectVideo.setObjectName("lblSelectVideo")
        self.btnChooseInput = QtWidgets.QPushButton(self.groupBox)
        self.btnChooseInput.setGeometry(QtCore.QRect(230, 60, 51, 23))
        self.btnChooseInput.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.068, y1:0.966, x2:1, y2:0, stop:0.414773 rgba(0, 0, 200, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "\n"
            "color: rgb(255, 255, 255);")
        self.btnChooseInput.setObjectName("btnChooseInput")
        self.btnChooseInput.clicked.connect(self.openFileNameDialog)
        self.txtSelectVideoInput = QtWidgets.QLineEdit(self.groupBox)
        self.txtSelectVideoInput.setGeometry(QtCore.QRect(90, 60, 131, 20))
        self.txtSelectVideoInput.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.txtSelectVideoInput.setObjectName("lineEdit_3")
        self.txtSelectOutput = QtWidgets.QLineEdit(self.groupBox)
        self.txtSelectOutput.setGeometry(QtCore.QRect(91, 90, 131, 20))
        self.txtSelectOutput.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.txtSelectOutput.setObjectName("txtSelectOutput")
        self.lblSelectOutput = QtWidgets.QLabel(self.groupBox)
        self.lblSelectOutput.setGeometry(QtCore.QRect(20, 90, 71, 21))
        self.lblSelectOutput.setObjectName("lblSelectOutput")
        self.btnChooseOutput = QtWidgets.QPushButton(self.groupBox)
        self.btnChooseOutput.setGeometry(QtCore.QRect(230, 90, 51, 23))
        self.btnChooseOutput.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.068, y1:0.966, x2:1, y2:0, stop:0.414773 rgba(0, 0, 200, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "\n"
            "color: rgb(255, 255, 255);")
        self.btnChooseOutput.setObjectName("btnChooseOutput")
        self.btnChooseOutput.clicked.connect(self.saveFileDialog)
        self.lblSelectYolo = QtWidgets.QLabel(self.groupBox)
        self.lblSelectYolo.setGeometry(QtCore.QRect(20, 125, 61, 21))
        self.lblSelectYolo.setObjectName("lblSelectYolo")
        self.cmbSelectYolo = QtWidgets.QComboBox(self.groupBox)
        self.cmbSelectYolo.setGeometry(QtCore.QRect(90, 120, 191, 22))
        self.cmbSelectYolo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.cmbSelectYolo.setObjectName("cmbSelectYolo")
        self.cmbSelectYolo.addItem("")
        self.cmbSelectYolo.addItem("")
        self.cmbSelectYolo.addItem("")
        self.btnConfigureCam = QtWidgets.QPushButton(self.groupBox)
        self.btnConfigureCam.setGeometry(QtCore.QRect(40, 170, 221, 23))
        self.btnConfigureCam.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.068, y1:0.966, x2:1, y2:0, stop:0.414773 rgba(0, 0, 200, 255), stop:1 rgba(255, 255, 255, 255));\n"
            "\n"
            "color: rgb(255, 255, 255);")
        self.btnConfigureCam.setObjectName("btnConfigureCam")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def getFiles(self):
        f = []
        path = r'C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\output'
        for (dirpath, dirnames, filenames) in os.walk(path):
            f.extend(filenames)
            break
        nf = []
        for d in f:
            fPath = path + "\\" + d
            nf.append(fPath)
        return nf

    def timerEvent(self, e=None):
        try:
            self.image_files = self.getFiles()
            if self.step >= len(self.image_files):
                self.timer.stop()
                self.btnSearchNumberPlate.setText('Slide Show Finished')
                return
            self.timer.start(self.delay, self)
            file = self.image_files[self.step]
            image = QPixmap(file)
            image.setDevicePixelRatio(3.6)
            #self.labelImage.adjustSize()
            self.labelImage.setPixmap(image)
            self.setWindowTitle("{} --> {}".format(str(self.step), file))
            self.step += 1
        except  Exception as e:
            print(e)

    # pick image files you have in the working folder
    # or give full path name
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBoxCheck.setTitle(_translate("Dialog", "Number Plate Group"))
        self.label_3.setText(_translate("Dialog", "Search Number Plate"))
        self.btnSearchNumberPlate.setText(_translate("Dialog", "Search"))
        self.label_2.setText(_translate("Dialog", "WEB"))
        self.label_4.setText(_translate("Dialog", "BASKET"))
        self.label.setText(_translate("Dialog", "Output Console"))
        self.groupBox.setTitle(_translate("Dialog", "Control Group"))
        self.btnStart.setText(_translate("Dialog", "Start Analyze"))
        self.cmbSelectProgram.setItemText(0, _translate("Dialog", "Analyze"))
        self.cmbSelectProgram.setItemText(1, _translate("Dialog", "Main"))
        self.cmbSelectProgram.setItemText(2, _translate("Dialog", "Runner"))
        self.lblSelectWay.setText(_translate("Dialog", "Select Way"))
        self.lblSelectVideo.setText(_translate("Dialog", "Select Video"))
        self.btnChooseInput.setText(_translate("Dialog", "Choose"))
        self.lblSelectOutput.setText(_translate("Dialog", "Select Output"))
        self.btnChooseOutput.setText(_translate("Dialog", "Choose"))
        self.lblSelectYolo.setText(_translate("Dialog", "Select Yolo"))
        self.cmbSelectYolo.setItemText(0, _translate("Dialog", "YOLO"))
        self.cmbSelectYolo.setItemText(1, _translate("Dialog", "Common Object In Context"))
        self.cmbSelectYolo.setItemText(2, _translate("Dialog", "COCO"))
        self.btnConfigureCam.setText(_translate("Dialog", "Camera Configuration"))
        self.btnStart.clicked.connect(self.startAnalyze)

    def animate(self):
        pass

    def process(self,confidence= 0.5, threshold= 0.3, input="input/highway.mp4", yolo= "yolo-coco",output= os.getcwd()+'\\output\\' ):
        print("Test",output)
        args = {"confidence": confidence,
                    "threshold": threshold,
                    "input": input,#r"C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\input\highway.mp4",
                    "output": output,#r"C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\output\highway.avi",
                    "yolo": yolo}
        labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
        LABELS = open(labelsPath).read().strip().split("\n")
        # initialize a list of colors to represent each possible class label
        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(200, 3),
                                   dtype="uint8")

        # derive the paths to the YOLO weights and model configuration
        weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
        configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        print("[INFO] loading YOLO from disk...")
        self.textEdit.append("[INFO] loading YOLO from disk...")

        net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # initialize the video stream, pointer to output video file, and
        # frame dimensions
        vs = cv2.VideoCapture(args["input"])
        writer = None
        (W, H) = (None, None)

        frameIndex = 0

        # try to determine the total number of frames in the video file
        try:
            prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
                else cv2.CAP_PROP_FRAME_COUNT
            total = int(vs.get(prop))
            print("[INFO] {} total frames in video".format(total))
            self.textEdit.append(self.textEdit.toPlainText()+"[INFO] {} total frames in video".format(total))
        # an error occurred while trying to determine the total
        # number of frames in the video file
        except:
            self.textEdit.append(self.textEdit.toPlainText()+"[INFO] could not determine # of frames in video\n[INFO] no approx. completion time can be provided")
            print("[INFO] could not determine # of frames in video")
            print("[INFO] no approx. completion time can be provided")
            total = -1

        # loop over frames from the video file stream
        while True:
            # read the next frame from the file
            (grabbed, frame) = vs.read()
            # if the frame was not grabbed, then we have reached the end
            # of the stream
            if not grabbed:
                break
            # if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]
            # construct a blob from the input frame and then perform a forward
            # pass of the YOLO object detector, giving us our bounding boxes
            # and associated probabilities
            blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                         swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()

            # initialize our lists of detected bounding boxes, confidences,
            # and class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []

            # loop over each of the layer outputs
            for output in layerOutputs:
                # loop over each of the detections
                for detection in output:
                    # extract the class ID and confidence (i.e., probability)
                    # of the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > args["confidence"]:
                        # scale the bounding box coordinates back relative to
                        # the size of the image, keeping in mind that YOLO
                        # actually returns the center (x, y)-coordinates of
                        # the bounding box followed by the boxes' width and
                        # height
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top
                        # and and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates,
                        # confidences, and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
            # apply non-maxima suppression to suppress weak, overlapping
            # bounding boxes
            idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])
            dets = []
            if len(idxs) > 0:
                # loop over the indexes we are keeping
                for i in idxs.flatten():
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])
                    dets.append([x, y, x + w, y + h, confidences[i]])
            np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
            dets = np.asarray(dets)
            tracks = self.tracker.update(dets)
            boxes = []
            indexIDs = []
            c = []
            previous = self.memory.copy()
            self.memory = {}
            for track in tracks:
                boxes.append([track[0], track[1], track[2], track[3]])
                indexIDs.append(int(track[4]))
                self.memory[indexIDs[-1]] = boxes[-1]
            if len(boxes) > 0:
                i = int(0)
                for box in boxes:
                    # extract the bounding box coordinates
                    (x, y) = (int(box[0]), int(box[1]))
                    (w, h) = (int(box[2]), int(box[3]))
                    # draw a bounding box rectangle and label on the image
                    # color = [int(c) for c in COLORS[classIDs[i]]]
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    color = [int(c) for c in COLORS[indexIDs[i] % len(COLORS)]]
                    cv2.rectangle(frame, (x, y), (w, h), color, 4)
                    if indexIDs[i] in previous:
                        previous_box = previous[indexIDs[i]]
                        (x2, y2) = (int(previous_box[0]), int(previous_box[1]))
                        (w2, h2) = (int(previous_box[2]), int(previous_box[3]))
                        p0 = (int(x + (w - x) / 2), int(y + (h - y) / 2))
                        p1 = (int(x2 + (w2 - x2) / 2), int(y2 + (h2 - y2) / 2))
                        cv2.line(frame, p0, p1, color, 3)
                        if intersect(p0, p1, self.line[0], self.line[1]):
                            self.counter += 1
                    # text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                    text = "{}".format(indexIDs[i])
                    cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    i += 1
            # draw line
            cv2.line(frame, self.line[0], self.line[1], (0, 255, 255), 5)
            # draw counter
            cv2.putText(frame, str(self.counter), (100, 200), cv2.FONT_HERSHEY_DUPLEX, 5.0, (0, 255, 255), 10)
            # counter += 1
            # saves image file
            cv2.imwrite( args['output']+"frame-{}.png".format(frameIndex), frame)
            height, width, channel = frame.shape
            bytesPerLine=3 * width
            qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            image = QPixmap(qImg)
            image.setDevicePixelRatio(3.6)
            # self.labelImage.adjustSize()
            self.labelImage.setPixmap(image)

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(args["output"], fourcc, 30,(frame.shape[1], frame.shape[0]), True)

                # some information on processing single frame
                if total > 0:
                    elap = (end - start)
                    self.textEdit.append("[INFO] single frame took {:.4f} seconds".format(elap))
                    print("[INFO] single frame took {:.4f} seconds".format(elap))
                    self.textEdit.append("[INFO] estimated total time to finish: {:.4f}".format(elap * total))
                    print("[INFO] estimated total time to finish: {:.4f}".format(elap * total))
            # write the output frame to disk
            writer.write(frame)
            # increase frame index
            frameIndex += 1
        print("[INFO] cleaning up...")
        self.textEdit.append("[INFO] cleaning up...")
        vs.release()

    def startAnalyze(self, commandStr):
        try:
            args = {"confidence": 0.5,
                    "threshold": 0.3,
                    "input": self.txtSelectVideoInput.text() ,#r"C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\input\highway.mp4",
                    "output": self.txtSelectOutput.text(),#r"C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\output\highway.avi",
                    "yolo": r"C:\Users\dheer\PycharmProjects\Smart-Video-Analytics\webbasket\ui\yolo-coco"}
            dark = DarkNetUtils()
            if not args['output']:
                mainWindow = Thread(target=self.process, args=(args["confidence"],
                                                               args["threshold"],
                                                               args["input"],
                                                               args["yolo"]
                                                               ))
            else:
                mainWindow = Thread(target=self.process, args=(args["confidence"],
                                                          args["threshold"],
                                                          args["input"],
                                                          args["yolo"],
                                                          args["output"]
                                                          ))
            mainWindow.start()
        except(Exception) as e:
            print(e)

    def saveFileDialog(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
       # fileName, _ = QFileDialog.getSaveFileName()
        # (dlg = QFileDialog,"QFileDialog.getSaveFileName",  "All Files (*);Text Files (*.txt)", options=options)
        if file:
            self.txtSelectOutput.setText("{}/".format(file))

    def openFileNameDialog(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        # dlg.setFilter(r"Text files (*.mp4)")
        fileName = ''
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.txtSelectVideoInput.setText(filenames[0])
            print(filenames)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())