from controller import Robot, Motor, Camera
import numpy as np
import cv2 
import camera as cam
from motor_control import MotorControl
from sweeper_control import SweeperControl
from slider_control import SliderControl
from distance_sensor_util import DistanceSensorUtil

# cv2.startWindowThread()
# cv2.namedWindow("preview")



robot = Robot()
timestep = int(robot.getBasicTimeStep())
cam.startCameraFeed(robot)
motorControl= MotorControl(robot=robot)
sweepControl = SweeperControl(robot=robot)
sliderControl = SliderControl(robot=robot)
distanceSensor= DistanceSensorUtil(robot=robot)


# camera = robot.getDevice('camera')
# camera.enable(100)



# motorControl.moveBackwardStep()
# sweepControl.sweep()
# sliderControl.moveToBin()

distanceSensor.getObstacleStatus()
while robot.step(timestep) != -1:
    v=distanceSensor.getObstacleStatus()
    motorControl.moveForwardStep()
    print(v.getMovementState())
    # cameraData=camera.getImage()
    # image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    
    pass

