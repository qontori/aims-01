from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.tools import multitask, run_task, wait


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
    global JunctionDetected
    if  color_sensor_2.color() == Color.NONE and  color_sensor.color() == Color.NONE:
        #print('Junction Detected', JunctionDetected)
        JunctionDetected = JunctionDetected + 1
        CheckImage()

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

def CheckImage():
    if  distance_sensor.distance() <= 200:
        try:
            file = open("link2.py", "rb")
            print("woo")
        except OSError as e:
            print(e)
        from link2 import TEXT
        print(TEXT)
        if TEXT == 0:
            TurnLeft()
        elif TEXT == 1:
            Turn_Right()

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

StartMotors()
while True:
    LineFollower()
    JunctionCheck()
    if CheckEnd():
        break
