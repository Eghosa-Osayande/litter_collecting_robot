import cv2 as cv


class CameraController:

    # properties
    cam: cv.VideoCapture = None

    # constructor
    def __init__(self, source: int = 0):

        print('Opening camera: ', source)

        self.cam = cv.VideoCapture(source)

        if self.cam is None or not self.cam.isOpened():
            print('Warning: unable to open video source: ', source)
            exit()
        else:
            print('Opened camera: ', source)

    def get_image(self):
        _, image = self.cam.read()
        flippedImage = cv.flip(image, 2)
        return flippedImage
