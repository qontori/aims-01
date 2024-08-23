from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.tools import multitask, run_task, wait
from listener import GetInput

# Set up all devices.
prime_hub = PrimeHub()
color_sensor = ColorSensor(Port.D)
color_sensor_2 = ColorSensor(Port.C)
distance_sensor = UltrasonicSensor(Port.E)
motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_2 = Motor(Port.B, Direction.CLOCKWISE)

# Initialize variables.
data = 1
JunctionDetected = 0

def JunctionCheck():
    return color_sensor_2.color() == Color.NONE and  color_sensor.color() == Color.NONE

def LineFollower():
    if  color_sensor.color() !=  color_sensor_2.color():
        if  color_sensor.color() == Color.NONE:
            motor_2.dc(25)
        else:
            motor.dc(25)
    else:
         StartMotors()

def Turn_Right():
    motor_2.hold()
    motor.run_angle(250, 540)

def CheckDistance():
    return distance_sensor.distance() <= 200

def CheckImage():
    print("getting input")
    value = GetInput()
    print(f"val {value}")
    if "l" in value:
        TurnLeft()
    elif "r" in value:
        Turn_Right()
    else:
        motor.hold()
        motor_2.hold()
    StartMotors()


def TurnLeft():
    motor.hold()
    motor_2.run_angle(250, 540)

def StartMotors():
    motor.dc(50)
    motor_2.dc(50)

def CheckEnd():
    if color_sensor.color() == Color.RED:
        multitask(motor.run_angle(500, 180), motor_2.run_angle(500, 180))
        return 1
    return 0

print("hub: starting")
StartMotors()
while True:
    LineFollower()
    CheckImage()
    print('loop end')
    #if JunctionCheck() and CheckDistance():
    if CheckEnd():
        break
