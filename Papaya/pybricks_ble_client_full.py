from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.tools import multitask, run_task, wait

import listener

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X, broadcast_channel=0, observe_channels=[1])
color_sensor = ColorSensor(Port.D)
color_sensor_2 = ColorSensor(Port.C)
distance_sensor = UltrasonicSensor(Port.E)
motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_2 = Motor(Port.B, Direction.CLOCKWISE)

# Initialize variables.
data = ""
JunctionDetected = 0
turn = 0

async def JunctionCheck():
    global JunctionDetected
    await wait(1)
    if await color_sensor_2.color() == Color.NONE and await color_sensor.color() == Color.NONE and True:
        #print('Junction Detected', JunctionDetected)
        JunctionDetected = JunctionDetected + 1
        await CheckImage()

async def LineFollower():
    await wait(1)
    if await color_sensor.color() != await color_sensor_2.color():
        if await color_sensor.color() == Color.NONE:
            motor_2.dc(25)
        else:
            motor.dc(25)
    else:
        await StartMotors()

async def Turn_RIght():
    await wait(1)
    motor_2.hold()
    await multitask(motor.run_angle(250, 540))

async def CheckImage():
    global data
    await wait(1)
    if await distance_sensor.distance() <= 200:
        if data == b"rig\r\n":
            await Turn_RIght()
        elif data == b"lef\r\n":
            await TurnLeft()
        else:
            print(data)
    await StartMotors()

async def TurnLeft():
    await wait(1)
    motor.hold()
    await multitask(motor_2.run_angle(250, 540))

async def StartMotors():
    await wait(1)
    motor.dc(50)
    motor_2.dc(50)

async def subtask():
    global data
    while True:
        await listener.GetInput()
        print(listener.test)

async def Run():
    await wait(1)
    print("run")
    await StartMotors()
    while True:
        await wait(1)
        await LineFollower()
        await JunctionCheck()
        if await CheckEnd():
            break

async def CheckEnd():
    await wait(1)
    if await color_sensor.color() == Color.RED:
        await multitask(motor.run_angle(500, 180), motor_2.run_angle(500, 180))
        return 1
    return 0

async def main():
    await multitask(subtask(), Run())


run_task(main())