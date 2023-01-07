from controller import Display
import numpy as np
import cv2


class ImageProcessor:

    bottleX = None
    bottleY = None

    def __init__(self, robot):
        time_step = int(robot.getBasicTimeStep())
        self.robot = robot
        self.camera = robot.getDevice('camera')
        self.camera.enable(time_step)
        self.camHeight = self.camera.getHeight()
        self.camWidth = self.camera.getWidth()
        if self.camera.hasRecognition():
            self.camera.recognitionEnable(time_step)
        self.display = robot.getDevice('camera_display')

    def step(self):
        cameraData = self.camera.getImage()

        self.previewImage = np.frombuffer(
            cameraData, np.uint8).reshape((self.camWidth, self.camHeight, 4))
        self.detectBottles()

        if cameraData:
            ir = self.display.imageNew(
                self.previewImage.tobytes(), Display.BGRA, self.camWidth, self.camHeight)
            self.display.imagePaste(ir, 0, 0, False)
            self.display.imageDelete(ir)

    def detectBottles(self):
        objects: list = self.camera.getRecognitionObjects()
        if len(objects) > 0:
            bottle = objects[0]
            y_check=None
            for object in objects:
                if not y_check:
                    _,y_check=list(bottle.getPositionOnImage())
                    bottle=object
                    continue
                _,y2= list(bottle.getPositionOnImage())
                if y2>y_check:
                    bottle=object

            w, h = list(bottle.getSizeOnImage())
            x, y = list(bottle.getPositionOnImage())
            norm_x = (x/self.camWidth)
            norm_y = (y/self.camHeight)
            self.bottleX, self.bottleY = norm_x, norm_y
            cv2.rectangle(self.previewImage, (x-w, y-h),
                          (x+w, y+h), (255, 255, 255), 1)
        else:
            self.bottleX = None
            self.bottleY = None
        print(self.bottleX,self.bottleY)
