from controller import Robot, Motor, Camera
import numpy as np
import cv2 
import camera as cam

# cv2.startWindowThread()
# cv2.namedWindow("preview")



robot = Robot()
timestep = int(robot.getBasicTimeStep())
cam.startCameraFeed(robot)

r1= robot.getDevice('wheel_right1')
r2= robot.getDevice('wheel_right2')
l1= robot.getDevice('wheel_left1')
l2= robot.getDevice('wheel_left2')
sweeper= robot.getDevice('sweeper_motor')
distanceSensorLeft= robot.getDevice('distance_sensor_center')
distanceSensorLeft.enable(timestep)
distanceSensorLeft2= robot.getDevice('distance_sensor_center_2')
distanceSensorLeft2.enable(timestep)

# camera = robot.getDevice('camera')
# camera.enable(100)

slab_linear = robot.getDevice('slab_linear_motor')
slat_rotational= robot.getDevice('slab_rotational_motor')
slab_linear.setPosition(0.0)
slab_linear.setVelocity(0.1)
# slat_rotational.setPosition(-(22/7)/2)
# slat_rotational.setVelocity(0.5)



while robot.step(timestep) != -1:
    print(distanceSensorLeft.getValue(),distanceSensorLeft2.getValue())
    sweeper_speed=0
    left=0
    right=left
    # slab_linear.setPosition(0.8)
    # slab_linear.setVelocity(0.1)
    sweeper.setPosition(float('inf'))
    sweeper.setVelocity(sweeper_speed)
    
    r1.setPosition(float('inf'))
    r1.setVelocity(right)
    
    r2.setPosition(float('inf'))
    r2.setVelocity(right)
    
    l1.setPosition(float('inf'))
    l1.setVelocity(left)
    
    l2.setPosition(float('inf'))
    l2.setVelocity(left)
    
    # cameraData=camera.getImage()
    # image = np.frombuffer(cameraData, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    
    # pass


