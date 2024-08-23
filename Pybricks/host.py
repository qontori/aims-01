import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient
import cv2
import time

import opencv_script  # Ensure this is correctly imported

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
HUB_NAME = "BananaBrick"
main_task = None
client = None
start_time = time.time()
sending = False
running = True

def handle_disconnect(_):
    global main_task
    print(f"Hub was disconnected. {time.time() - start_time}s")
    #get them to retry?
    if main_task and not main_task.done():
        main_task.cancel()

async def handle_rx(_, data: bytearray):
    global sending
    if sending == False:
        sending = True
    else:
        return
    if data[0] == 0x01:  # "write stdout" event (0x01)
        payload = data[1:]
        print(f"payload: {payload}")
        if b"rdy" in payload:
            if client:
                for attempt in range(3):  # Retry up to 3 times
                    try:
                        await client.write_gatt_char(
                            PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                            b"\x06" + opencv_script.current_result,
                            response=True
                        )
                        print(f"Sent: {opencv_script.current_result}")
                        break
                    except Exception as e:
                        print(f"Attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(1)  # Wait before retrying
            else:
                print("Client is not initialized.")
        else:
            print("Received:", payload)
    sending = False

async def hub_setup():
    global client
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if device is None:
        print(f"Could not find hub with name: {HUB_NAME}")
        return

    print(f"Found device {device}")
    async with BleakClient(device, disconnected_callback=handle_disconnect, timeout=10) as connected_client:
        client = connected_client
        print("Connected to hub")
        await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)
        print("Subscribed to notifications")
        print("Press button to start program")

        # Start OpenCV thread if needed
        thread = opencv_script.cvThread(1, "Thread 1")
        thread.start()
        while True:
            await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)
            if not running:
                break
        thread.join()

async def main():
    global main_task, running
    main_task = asyncio.current_task()

    print("Setting up hub")
    await hub_setup()

    # Main loop to keep the program running
    while True:
        key = cv2.waitKey(50)
        if key == 27:  # ESC key
            print("Exiting...")
            running = True
            break

# Run the main async program
if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())
