from math import pi

_SLIDE_SPEED: int = 0.1
_ANGLE_SPEED: int = 1
INF = float('inf')


class SliderControl:
    slider = None
    rotation_motor= None
    rotation_position_sensor= None
    slider_position_sensor= None

    def __init__(self, robot) -> None:
        time_step = int(robot.getBasicTimeStep())
        self.rotation_motor = robot.getDevice('slab_rotational_motor')
        self.rotation_position_sensor = robot.getDevice('slab_rotational_position')
        self.slider = robot.getDevice('slab_linear_motor')
        self.slider_position_sensor = robot.getDevice('slider_position')
        self.slider_position_sensor.enable(time_step)
        self.rotation_position_sensor.enable(time_step)
        self.robot = robot
        # the next line is necessary tto initialize the position_sensor value
        self.robot.step(time_step)
        pass

    def _turn(self, position: float, speed: int ):
        self.rotation_motor.setPosition(position)
        self.rotation_motor.setVelocity(speed)

    def _slide(self, position: float, speed: int, ):
        self.slider.setPosition(position)
        self.slider.setVelocity(speed)

    def moveToBin(self):
        time_step = int(self.robot.getBasicTimeStep())
        slideDistance = 0.5  # to turn 2pi we set this higher than like 3pi
        duration = (slideDistance/_SLIDE_SPEED) * 1000
        slideSteps = int(duration / time_step)

        angleDistance = pi  # to turn 2pi we set this higher than like 3pi
        duration = (angleDistance/_ANGLE_SPEED) * 1000
        angleSteps = int(duration / time_step)

        # step 1: slide up
        pos = self.slider_position_sensor.getValue()
        if pos< 0.3:
            pos=0.3
            for i in range(slideSteps):
                self._slide(position= pos, speed=_SLIDE_SPEED)
                self.robot.step(time_step)
        
        # step 2: rotate clockwise
        pos2= self.rotation_position_sensor.getValue()
        if pos2 > -(pi/2):
            pos2=-(pi/2)
            for i in range(angleSteps):
                self._turn(position= pos2, speed=_ANGLE_SPEED)
                self.robot.step(time_step)
        
        # step 3: rotate counter clockwise
        pos3= self.rotation_position_sensor.getValue()
        if pos3 <= -(pi/2):
            pos3=0
            for i in range(angleSteps):
                self._turn(position= pos3, speed=_ANGLE_SPEED)
                self.robot.step(time_step)

        # step 4: slide down
        pos4 = self.slider_position_sensor.getValue()
        if pos4 >= 0.3:
            pos4=0
            for i in range(slideSteps):
                self._slide(position= pos4, speed=_SLIDE_SPEED)
                self.robot.step(time_step)
