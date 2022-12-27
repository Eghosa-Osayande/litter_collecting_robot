
from controller import Robot, Motor, Camera
import numpy as np
import cv2 

# cv2.startWindowThread()
# cv2.namedWindow("preview")

robot = Robot()

r1= robot.getDevice('wheelr1')
r2= robot.getDevice('wheelr2')
l1= robot.getDevice('wheell1')
l2= robot.getDevice('wheell2')

camera = robot.getDevice('camera')
camera.enable(100)




timestep = int(robot.getBasicTimeStep())


while robot.step(timestep) != -1:
    r1.setPosition(float('inf'))
    r1.setVelocity(1)
    
    r2.setPosition(float('inf'))
    r2.setVelocity(1)
    
    l1.setPosition(float('inf'))
    l1.setVelocity(1)
    
    l2.setPosition(float('inf'))
    l2.setVelocity(1)
    
    cameraData=camera.getImage()
    image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    
    pass


