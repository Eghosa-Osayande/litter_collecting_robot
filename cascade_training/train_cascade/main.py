import cv2 as cv
from time import time
from camera_controller import CameraController
from vision import Vision
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))

cascade_limestone = cv.CascadeClassifier('cascade/cascade.xml')
vision_limestone = Vision(None)

loop_time = time()


cap = CameraController()


while True:
    flippedImage = cap.get_image()

    # do object detection
    rectangles = cascade_limestone.detectMultiScale(flippedImage)

    # draw the detection results onto the original image
    detection_image = vision_limestone.draw_rectangles(
        flippedImage, rectangles)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # display the images
    cv.imshow('Matches', detection_image)

    # press 'q' with the output window focused to exit.
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break


print('Done.')
