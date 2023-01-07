from math import pi

_SPEED: int = 2.5
INF = float('inf')


class SweeperControl:
    sweeper = None
    position_sensor= None

    def __init__(self, robot) -> None:
        time_step = int(robot.getBasicTimeStep())
        self.sweeper = robot.getDevice('sweeper_motor')
        self.position_sensor = robot.getDevice('sweeper_position_sensor')
        self.position_sensor.enable(time_step)
        self.robot = robot
        # the next line is necessary tto initialize the position_sensor value
        self.robot.step(time_step)
        pass

    def _turn(self, position: float, speed: int = _SPEED, ):
        self.sweeper.setPosition(position)
        self.sweeper.setVelocity(speed)

    def sweep(self):
        
        radianDistance = 3 * pi  # to turn 2pi we set this higher than like 3pi
        duration = (radianDistance/_SPEED) * 1000
        time_step = int(self.robot.getBasicTimeStep())

        steps = int(duration / time_step)
        pos = self.position_sensor.getValue() + (2 * pi)

        for i in range(steps):
            self._turn(position= pos, speed=_SPEED)
            self.robot.step(time_step)

        
