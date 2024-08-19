from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.tools import multitask, run_task, wait
from linking import TEXT

# Set up all devices.
prime_hub = PrimeHub()
color_sensor = ColorSensor(Port.D)
color_sensor_2 = ColorSensor(Port.C)
color_sensor_3 = ColorSensor(Port.F)
distance_sensor = UltrasonicSensor(Port.E)
motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_2 = Motor(Port.B, Direction.CLOCKWISE)

# Initialize variables.
data = 1
JunctionDetected = 0

def JunctionCheck():
    global JunctionDetected
    print(color_sensor_2.color())
    print(color_sensor.color())
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

def Turn_RIght():
    motor_2.hold()
    multitask(motor.run_angle(250, 540))

def CheckImage():
    if  distance_sensor.distance() <= 200:
        if  TEXT == 'left':
             TurnLeft()
        elif  TEXT=='right':
             Turn_RIght()
        else:
            pass
    StartMotors()

def TurnLeft():
    motor.hold()
    multitask(motor_2.run_angle(250, 540))

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
