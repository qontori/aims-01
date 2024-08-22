import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient
import numpy as np
import os

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
current_result = ""
# Replace this with the name of your hub if you changed
# it when installing the Pybricks firmware.
HUB_NAME = "Banana"

ready_event = asyncio.Event()

def handle_disconnect(_):
        print("Hub was disconnected.")
        if not main_task.done():
            main_task.cancel()
async def handle_rx(_, data: bytearray):
    global ready_event
    print("Get handle_rx")
    print(data)
    if data[0] == 0x01:  # "write stdout" event (0x01)
        payload = data[1:]
        if payload == b"rdy\r\n":
            print("Ready")
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + current_result,  # prepend "write stdin" command (0x06)
                response=True)
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
        
async def main():
    main_task = asyncio.current_task()
    await hub_setup()
    while True:
        try:
            pass
        except Exception as e:
            print(e)
    

# Run the main async program.
if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())

