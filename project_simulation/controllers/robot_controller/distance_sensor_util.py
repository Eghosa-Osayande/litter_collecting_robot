from enums import ObstacleMovementState
class ObstacleStatus():

    def __init__(self, left: bool, right: bool, front: bool, back: bool):
        self.right: bool = right
        self.left: bool = left
        self.front: bool = front
        self.back: bool = back

    def getMovementState(self):
        if not self.front:
            return ObstacleMovementState.FORWARD
        elif not self.right:
            return ObstacleMovementState.RIGHT
        elif not self.left:
            return ObstacleMovementState.LEFT
        elif not self.back:
            return ObstacleMovementState.BACKWARD
        else:
            return ObstacleMovementState.WAIT


class DistanceSensorUtil:

    def __init__(self, robot):
        time_step = int(robot.getBasicTimeStep())

        self.sensorBottle = robot.getDevice('distance_sensor_center')
        self.sensorBottle.enable(time_step)

        self.sensorBottle2 = robot.getDevice('distance_sensor_center_2')
        self.sensorBottle2.enable(time_step)

        self.sensorFrontWall = robot.getDevice('distance_sensor_left')
        self.sensorFrontWall.enable(time_step)

        self.sensorFrontWall2 = robot.getDevice('distance_sensor_right')
        self.sensorFrontWall2.enable(time_step)

        self.sensorLeftWall = robot.getDevice('distance_sensor_left_wall')
        self.sensorLeftWall.enable(time_step)

        self.sensorRightWall = robot.getDevice('distance_sensor_right_wall')
        self.sensorRightWall.enable(time_step)

        self.sensorBackWall = robot.getDevice('distance_sensor_back_wall')
        self.sensorBackWall.enable(time_step)

        self.sensorBackWall2 = robot.getDevice('distance_sensor_back_wall_2')
        self.sensorBackWall2.enable(time_step)

        robot.step(time_step)

    def getObstacleStatus(self) -> ObstacleStatus:
        front = self.sensorFrontWall.getValue()
        front2 = self.sensorFrontWall2.getValue()

        back = self.sensorBackWall.getValue()
        back2 = self.sensorBackWall2.getValue()

        left = self.sensorLeftWall.getValue()
        right = self.sensorRightWall.getValue()

        return ObstacleStatus(
            front=front < 100 or front2 < 100,
            back=back < 100 or back2 < 100,
            left=left < 100,
            right=right < 100,
        )

    def isBottleInRange(self) -> bool:
        center1 = self.sensorBottle.getValue()
        center2 = self.sensorBottle.getValue()
        if center1 < 13.7 or center2 < 13.7:
            return True
        else:
            return False
