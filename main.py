import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from model import FaceDetectCameraModel
from view import FaceDetectCameraView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = FaceDetectCameraModel()
    view = FaceDetectCameraView(model)
    model.detect_faces()
    view.show()
    sys.exit(app.exec_())