from controller import Robot, Motor, Camera
from image_processing import ImageProcessor
from motor_control import MotorControl
from sweeper_control import SweeperControl
from slider_control import SliderControl
from distance_sensor_util import DistanceSensorUtil, ObstacleMovementState


robot = Robot()
timestep = int(robot.getBasicTimeStep())

imageProcessor = ImageProcessor(robot=robot)
motorControl = MotorControl(robot=robot)
sweepControl = SweeperControl(robot=robot)
sliderControl = SliderControl(robot=robot)
distanceSensor = DistanceSensorUtil(robot=robot)



def wait(seconds: int):
    duration = seconds * 1000
    steps = int(duration / timestep)

    for i in range(steps):
        robot.step(timestep)


while robot.step(timestep) != -1:
    # imageProcessor.step()
    
    # continue
    # check for obstacle state
    obstacleStats = distanceSensor.getObstacleStatus()

    if obstacleStats.frontLeft or obstacleStats.frontRight:
        if obstacleStats.frontLeft and  obstacleStats.frontRight:
            motorControl.moveBackwardStep()
        if  obstacleStats.right == False:
            print('obstacle: turn right')
            motorControl.turnRightStep()
            continue
        if  obstacleStats.left==False:
            print('obstacle: turn left')
            motorControl.turnLeftStep()
            continue
        if  obstacleStats.right == True and obstacleStats.left==True:
            if not obstacleStats.backLeft and not obstacleStats.backRight:
                print('obstacle: move back')
                motorControl.moveBackwardStep()
                continue
            else:
                print('DEADLOCK')
                continue
    

    # else check if there is bottle
    imageProcessor.step()
    bottleX = imageProcessor.bottleX
    bottleY = imageProcessor.bottleY

    if bottleX:

        # if bottle check if it is in the center
        new_var = (bottleX < 0.45) or (bottleX > 0.57)
        
        if new_var:
            print('bottle not in line of sight')
            # if not align
            if (bottleX < 0.5):
                print('aligning left')
                motorControl.turnLeftStep()
            else:
                print('aligning right')
                motorControl.turnRightStep()
            continue

        # if aligned move forward step
        else:
            print('moving to bottle')
            motorControl.moveForwardStep()

            # check if bottle is within range
            isBottleInRange = bottleY >= 0.87
            
            if isBottleInRange:
                wait(2)
                print('bottle in range')
                # if so deploy the sweeper and move to bin
                sweepControl.sweep()
                wait(2)
                sliderControl.moveToBin()
            else:
                print('bottle not in range')
            continue

    else:
        print('is roaming')
        motorControl.moveForwardStep()

    pass
