import opencv_script

import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient

from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
import os

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
# Replace this with the name of your hub if you changed
# it when installing the Pybricks firmware.
#IMPT: CHANGE NAME OF THE HUB TO THE PYBRICKS
HUB_NAME = "BananaBrick"

async def handle_rx(_, data: bytearray):
    print(f"handle_rx")
    if data[0] == 0x01:  # "write stdout" event (0x01)
        payload = data[1:]
        print(f"payload: {payload}")
        if b"rdy" in payload:
            print("Ready, reading 1 frame")
            try:
                print(f"result: {opencv_script.current_result}")
            except Exception as e:
                print(e)
            print(f"sending {opencv_script.current_result}")
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + opencv_script.current_result,  # prepend "write stdin" command (0x06)
                response=True)
            print("sent")
        else:
            print("Received:", payload)

async def hub_setup():
    global client
    device = await BleakScanner.find_device_by_name(HUB_NAME)

    if device is None:
        print(f"could not find hub with name: {HUB_NAME}")
        return

    print(f"found device {device}")

    # Connect to the hub.
    async with BleakClient(device) as client:
        print("connecting to hub")
        # Subscribe to notifications from the hub.
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)
        print("subbed to noti")
        # Shorthand for sending some data to the hub.
        print("press button to start program")
        
async def main():
    main_task = asyncio.current_task()
    global current_result
    print("setting up hub")
    await hub_setup()
    #start the cv thread
    thread = opencv_script.cvThread(1, "Thread 1")
    thread.start()
    thread.join()
    
    while True:
        key = cv2.waitKey(50)
        if key == 27:
            break
    

# Run the main async program.
if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())

