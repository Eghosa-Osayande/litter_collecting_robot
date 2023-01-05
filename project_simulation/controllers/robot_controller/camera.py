from controller import Camera

def startCameraFeed(robot):
    camera = robot.getDevice('camera')
    camera.enable(100)