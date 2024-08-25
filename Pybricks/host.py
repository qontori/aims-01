import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient
import cv2
import time

import opencv_script
#defaults the ml result to 5 random bytes
#IMPT: stdin read is blocking, so it must read 5 bytes if not it will become stucked
current_result = b"12345"

#ble protocol uuid for pybricks to write into the stdin stream of the hub
PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"
#IMPT: name must match the pybricks hub name
HUB_NAME = "Banana"
main_task = None
client = None
start_time = None
sending = False

#callback for bleak client to know when it disconnected
def handle_disconnect(_):
    global main_task
    print(f"Hub was disconnected. Connected for {time.time() - start_time}s")

#callback for when the pi recieves any changes on the hub
async def handle_rx(_, data: bytearray):
    #TODO: this block stops more than 1 handle_rx from running concurrently
    #my cpp brain tells me got thread racing trying to write at the same time to the stdin stream for the hub
    #can leave it or can investigate if this is true
    global sending
    if sending == False:
        sending = True
    else:
        return
    if data[0] == 0x01:  # "write stdout" event (0x01)
        payload = data[1:]
        print(f"payload: {payload}")
        #if stdout stream in the hub has 'rdy' characters in it, means its asking for data to  be sent
        if b"rdy" in payload:
            if client:
                for attempt in range(3):  # Retry up to 3 times
                    try:
                        #sned a command of \x06(write to stdin) with current result
                        await client.write_gatt_char(
                            PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                            b"\x06" + current_result,
                            response=True
                        )
                        print(f"Sent: {current_result}")
                        break
                    except Exception as e:  #attempt again if failed, TODO: not sure if needed
                        print(f"Attempt {attempt + 1} failed: {e}")
                        await asyncio.sleep(1)  # Wait before retrying
            else:
                print("Client is not initialized.")
        else:
            print("Received:", payload)
    sending = False

async def hub_setup():
    global client, current_result, start_time
    #first find if the device is available
    print(f"Searching for {HUB_NAME}...")
    device = await BleakScanner.find_device_by_name(HUB_NAME)
    if device is None:
        print(f"Could not find hub with name: {HUB_NAME}, please check if variable HUB_NAME name is correct")
        exit()

    #otherwise we found a device that we want to connect to
    print(f"Found device {device}")
    start_time = time.time()
    #creates a bleakclient object that connects to the hub
    #timeout controls how long before the pi gives up on trying
    try:
        async with BleakClient(device, disconnected_callback=handle_disconnect, timeout=10) as connected_client:
            print("Connected to hub")
            client = connected_client
            print("Setting up opencv")
            opencv_script.opencv_setup()
            print("Press button to start program")

            # Main loop to keep the program running
            while True:
                await asyncio.sleep(0.1)
                #process the image
                current_result = opencv_script.process_image()
                #TODO: not sure if we need to keep getting notifications
                await client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, handle_rx)
                #exit condition
                key = cv2.waitKey(50)
                if key == 27:  # ESC key
                    print("Exiting...")
                    break
    except Exception as e:
        print(f"{e}")
        exit()

async def main():
    global main_task
    main_task = asyncio.current_task()

    print("Setting up hub")
    #establish a connection with the hub and run the logic loop
    await hub_setup()
    #once function is executed it should exit
    opencv_script.opencv_cleaup()
    exit()
    

# Run the main async program
if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())
