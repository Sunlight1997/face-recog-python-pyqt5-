import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

class Model:
    def __init__(self):
        self.image = None

    def loadImage(self, image_path):
        self.image = cv2.imread(image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return self.image

    def detectFace(self):
        if self.image is not None:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            return self.image

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.m_widCentral = QWidget()
        self.setCentralWidget(self.m_widCentral)

        self.layout = QVBoxLayout()
        self.m_widCentral.setLayout(self.layout)

        self.m_lblImage = QLabel()
        self.layout.addWidget(self.m_lblImage)

        self.m_btnImgLoad = QPushButton("Load Image")
        self.m_btnDetect = QPushButton("Detect Faces")
        self.layout.addWidget(self.m_btnImgLoad)
        self.layout.addWidget(self.m_btnDetect)
        self.m_btnImgLoad.clicked.connect(self.loadImage)
        self.m_btnDetect.clicked.connect(self.detectFace)

    def displayImage(self, image):
        if image is not None:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.m_lblImage.setPixmap(pixmap)
            self.m_lblImage.setScaledContents(True)
            self.m_lblImage.setAlignment(Qt.AlignCenter)
            self.m_lblImage.resize(600,400)

    def loadImage(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.jpg *.png *.bmp);;All Files (*)", options=options)
        if file_path:
            controller.loadImage(file_path)

    def detectFace(self):
        image_with_faces = controller.detectFace()
        self.displayImage(image_with_faces)

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def loadImage(self, image_path):
        image = self.model.loadImage(image_path)
        self.view.displayImage(image)

    def detectFace(self):
        return self.model.detectFace()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec_())
