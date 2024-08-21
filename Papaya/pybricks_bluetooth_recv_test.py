from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.tools import multitask, run_task, wait

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X, broadcast_channel=0, observe_channels=[1])
motor = Motor(Port.A)

async def subtask():
    while True:
        await wait(1)
        test = prime_hub.ble.observe(1)
        print(test)
        if test != None:
            motor.run_time(360, 2000)
        await wait(1000)

async def subtask2():
    while True:
        await wait(1)
        await prime_hub.ble.broadcast([1])

async def subtask3():
    while True:
        await wait(1)
        print('Waiting for Connection')
        await wait(5000)

async def main():
    await multitask(subtask(), subtask2(), subtask3())


run_task(main())
