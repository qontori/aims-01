from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import multitask, run_task, wait

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X, broadcast_channel=0, observe_channels=[1])

async def subtask():
    while True:
        await wait(1)
        print(prime_hub.ble.observe(1))
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

return