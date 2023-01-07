from enums import ObstacleMovementState


class ObstacleStatus():

    def __init__(
        self, left: bool, right: bool, frontRight: bool, frontLeft: bool, backRight: bool, backLeft: bool,
    ):
        self.right: bool = right
        self.left: bool = left
        self.frontRight: bool = frontRight
        self.frontLeft: bool = frontLeft
        self.backRight: bool = backRight
        self.backLeft: bool = backLeft


class DistanceSensorUtil:

    def __init__(self, robot):
        time_step = int(robot.getBasicTimeStep())

        self.sensorBottle = robot.getDevice('distance_sensor_center')
        self.sensorBottle.enable(time_step)

        self.sensorBottle2 = robot.getDevice('distance_sensor_center_2')
        self.sensorBottle2.enable(time_step)

        self.sensorFrontWallLeft = robot.getDevice('distance_sensor_left')
        self.sensorFrontWallLeft.enable(time_step)

        self.sensorFrontWallRight = robot.getDevice('distance_sensor_right')
        self.sensorFrontWallRight.enable(time_step)

        self.sensorLeftWall = robot.getDevice('distance_sensor_left_wall')
        self.sensorLeftWall.enable(time_step)

        self.sensorRightWall = robot.getDevice('distance_sensor_right_wall')
        self.sensorRightWall.enable(time_step)

        self.sensorBackWallRight = robot.getDevice(
            'distance_sensor_back_wall_right')
        self.sensorBackWallRight.enable(time_step)

        self.sensorBackWallLeft = robot.getDevice(
            'distance_sensor_back_wall_left')
        self.sensorBackWallLeft.enable(time_step)

        robot.step(time_step)

    def getObstacleStatus(self) -> ObstacleStatus:
        frontLeft = self.sensorFrontWallLeft.getValue()
        frontRight = self.sensorFrontWallRight.getValue()

        backLeft = self.sensorBackWallRight.getValue()
        backRight = self.sensorBackWallLeft.getValue()

        left = self.sensorLeftWall.getValue()
        right = self.sensorRightWall.getValue()

        return ObstacleStatus(
            frontRight=frontRight < 100,
            frontLeft=frontLeft < 100,
            backRight=backRight < 100,
            backLeft=backLeft < 100,
            left=left < 100,
            right=right < 100,
        )
