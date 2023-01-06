import enum


class StateCodes(enum.Enum):
    STATE_SEARCHING='STATE_SEARCHING'
    STATE_FETCHING_BOTTLE='STATE_FETCHING_BOTTLE'
    STATE_MOVING_TO_BIN= 'STATE_MOVING_TO_BIN'

class ReturnCodes(enum.Enum):
    OK='OK'
    FAIL='FAIL'
    REPEAT='REPEAT'

class ObstacleMovementState(enum.Enum):
    FORWARD=1
    BACKWARD=2
    LEFT=3
    RIGHT=4
    WAIT=5
