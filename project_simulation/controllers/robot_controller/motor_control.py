from math import pi

_SPEED: int = 10
INF = float('inf')

wheelRadius = 0.05
wheelPerimeter = 2 * pi * wheelRadius

def calculateRadianDistanceFromLinearDistace(distance: float):
    return distance/wheelRadius


class MotorControl:
    r1 = None
    r2 = None
    l1 = None
    l2 = None
    robot = None

    def __init__(self, robot) -> None:
        self.r1 = robot.getDevice('wheel_right1')
        self.r2 = robot.getDevice('wheel_right2')
        self.l1 = robot.getDevice('wheel_left1')
        self.l2 = robot.getDevice('wheel_left2')
        self.robot = robot
        pass

    def _rightMove(self, position: float, speed: int = _SPEED, ):
        self.r1.setPosition(position)
        self.r1.setVelocity(speed)
        self.r2.setPosition(position)
        self.r2.setVelocity(speed)

    def _leftMove(self, position: float, speed: int = _SPEED):
        self.l1.setPosition(position)
        self.l1.setVelocity(speed)
        self.l2.setPosition(position)
        self.l2.setVelocity(speed)

    def _move(self, position: float, speed: int = _SPEED):
        self._leftMove(position=position, speed=speed)
        self._rightMove(position=position, speed=speed)

    def _turn(self, right: int, left: int):
        '''
        right or left should take these values -1, 1 or 0
        '''
        radianDistance = calculateRadianDistanceFromLinearDistace(0.05)
        duration = (radianDistance/_SPEED) * 1000
        time_step = int(self.robot.getBasicTimeStep())

        steps = int(duration / time_step)

        for i in range(steps):
            self._rightMove(position=INF, speed=_SPEED*right)
            self._leftMove(position=INF, speed=_SPEED*left)
            self.robot.step(time_step)
        self.stop()

    

    def stop(self):
        self._move(position=INF, speed=0)

    def moveForwardStep(self):
        self._turn(right=1,left=1)

    def moveBackwardStep(self):
        self._turn(right=-1,left=-1)

    def turnLeftStep(self):
        self._turn(right=1,left=0)

    def turnRightStep(self):
        self._turn(right=0,left=1)
