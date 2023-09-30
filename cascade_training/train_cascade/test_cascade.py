import cv2 as cv
from time import time
from camera_controller import CameraController
from vision import Vision
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))

cascade_limestone = cv.CascadeClassifier('cascade2/cascade.xml')
vision_limestone = Vision(None)

folder: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder)

def loop(srcFolder: str, ):

    

    for file in os.listdir(srcFolder):
        # Checking if the file is present in the list

        oldName = os.path.join(folder, srcFolder, file)
        img = cv.imread(oldName)
        flippedImage = img

        # do object detection
        rectangles = cascade_limestone.detectMultiScale(flippedImage)

        # draw the detection results onto the original image
        detection_image = vision_limestone.draw_rectangles(
            flippedImage, rectangles)

        

        # display the images
        cv.imshow('Matches', detection_image)

        # press 'q' with the output window focused to exit.
        key = cv.waitKey(1000)
        if key == ord('q'):
            cv.destroyAllWindows()
            return

        
loop('positive')


print('Done.')
