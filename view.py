from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

from model import FaceDetectCameraModel

class FaceDetectCameraView(QMainWindow):
    def __init__(self, model: FaceDetectCameraModel):
        super().__init__()
        self.model = model
        self.model.set_display_frame_signal(self.display_frame)

        self.setWindowTitle("Face Detection App")
        self.setGeometry(100, 100, 800, 600)

        self.widCentral = QWidget()
        self.setCentralWidget(self.widCentral)

        self.layout = QVBoxLayout()
        self.widCentral.setLayout(self.layout)

        self.lblImage = QLabel()
        self.layout.addWidget(self.lblImage)

        self.btnDetect = QPushButton("Start Webcam")
        self.layout.addWidget(self.btnDetect)
        self.btnDetect.clicked.connect(self.toogle_webcamera)

    def display_frame(self, frame):
        if frame is not None:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.lblImage.setPixmap(pixmap)
            self.lblImage.setAlignment(Qt.AlignCenter)

    def toogle_webcamera(self):
        if self.model.video_capture is None:
            self.model.start_webcam()
            self.btnDetect.setText("Stop Webcam")
        else:
            self.model.stop_webcam()
            self.btnDetect.setText("Start Webcam")