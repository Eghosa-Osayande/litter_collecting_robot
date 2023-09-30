import cv2 as cv
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

positiveDir= 'positive'
negativeDir= 'negative'

if not os.path.exists(positiveDir):
    os.mkdir(positiveDir)
if not os.path.exists(negativeDir):
    os.mkdir(negativeDir)

source=1
print('Opening camera: ',source)

cam = cv.VideoCapture(source) 

# key value
# cam.set(3 , 640  ) # width        
# cam.set(4 , 480  ) # height       
# cam.set(10, 120  ) # brightness     min: 0   , max: 255 , increment:1  
# cam.set(11, 50   ) # contrast       min: 0   , max: 255 , increment:1     
# cam.set(12, 70   ) # saturation     min: 0   , max: 255 , increment:1
# cam.set(13, 13   ) # hue         
# cam.set(14, 50   ) # gain           min: 0   , max: 127 , increment:1
# cam.set(15, -3   ) # exposure       min: -7  , max: -1  , increment:1
# cam.set(17, 5000 ) # white_balance  min: 4000, max: 7000, increment:1
# cam.set(28, 0    ) # focus          min: 0   , max: 255 , increment:5

if cam is None or not cam.isOpened():
    print('Warning: unable to open video source: ', source)
    exit()
else:
    print('Opened camera: ',source)

positiveCounter = 1
negativeCounter = 1

while True:
    _, image = cam.read()
    flippedImage = cv.flip(image, 2)
    cv.imshow('Image', flippedImage)

    # press 'q' with the output window focused to exit.
    # press 'g' to save screenshot as a positive image,
    # press 'j' to save as a negative image.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('g'):
        cv.imwrite(f'{positiveDir}/{positiveCounter}.jpg', flippedImage)
        positiveCounter+=1
    elif key == ord('j'):
        cv.imwrite(f'{negativeDir}/{negativeCounter}.jpg', flippedImage)
        negativeCounter+=1

print('Done.')