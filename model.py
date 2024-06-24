import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, QObject

class FaceDetectCameraModel(QObject):
    display_frame = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self.video_capture = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.detect_faces)

    def start_webcam(self):
        self.video_capture = cv2.VideoCapture(0)  # 0 corresponds to the default webcam
        self.timer.start(50)  # Set the timer to trigger every 100 ms (adjust as needed)

    def stop_webcam(self):
        if self.video_capture is not None:
            self.video_capture.release()
            self.timer.stop()

    def set_display_frame_signal(self, callback):
        self.display_frame.connect(callback)

    def detect_faces(self):
        if self.video_capture is not None:
            ret, frame = self.video_capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                faceCacade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = faceCacade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                self.display_frame.emit(frame)