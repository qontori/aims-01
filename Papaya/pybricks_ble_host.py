# SPDX-License-Identifier: MIT
# Copyright (c) 2020 Henrik Blidh
# Copyright (c) 2022-2023 The Pybricks Authors

"""
Example program for computer-to-hub communication.

Requires Pybricks firmware >= 3.3.0.
"""

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
HUB_NAME = "Banana"

async def main():
    main_task = asyncio.current_task()

    def handle_disconnect(_):
        print("Hub was disconnected.")

        # If the hub disconnects before this program is done,
        # cancel this program so it doesn't get stuck waiting
        # forever.
        if not main_task.done():
            main_task.cancel()

    ready_event = asyncio.Event()

    def handle_rx(_, data: bytearray):
        if data[0] == 0x01:  # "write stdout" event (0x01)
            payload = data[1:]

            if payload == b"rdy\r\n":
                ready_event.set()
            else:
                print("Received:", payload)

    # Do a Bluetooth scan to find the hub.
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
        async def send(data):
            # Wait for hub to say that it is ready to receive data.
            await ready_event.wait()
            # Prepare for the next ready event.
            ready_event.clear()
            # Send the data to the hub.
            await client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + data,  # prepend "write stdin" command (0x06)
                response=True
            )

        # Tell user to start program on the hub.
        print("Start the program on the hub now with the button.")

        #run open cv stuff
        os.chdir(os.path.dirname(__file__))
        # Load the TensorFlow Lite model
        interpreter = Interpreter(model_path="training/model_unquant.tflite")
        interpreter.allocate_tensors()

        # Get input and output tensors
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Load the labels
        class_names = open("training/labels.txt", "r").readlines()

        # CAMERA can be 0 or 1 based on default camera of your computer
        camera = cv2.VideoCapture(0)

        print("starting camera")

        try:
            while True:
                # Grab the webcam's image.
                ret, image = camera.read()

                if not ret:
                    print("Failed to grab frame")
                    break

                # Resize the raw image into (224-height, 224-width) pixels
                image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

                # Show the image in a window
                cv2.imshow("Webcam Image", image)

                # Make the image a numpy array and reshape it to the model's input shape.
                image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)

                # Normalize the image array
                image_normalized = (image_array / 127.5) - 1.0

                # Set the tensor to be passed as input to the model
                interpreter.set_tensor(input_details[0]['index'], image_normalized)

                # Run inference
                interpreter.invoke()

                # Get the output from the model
                output_data = interpreter.get_tensor(output_details[0]['index'])
                index = np.argmax(output_data)
                class_name = class_names[index]
                confidence_score = output_data[0][index]

                # Print prediction and confidence score
                print("Class:", class_name.strip()[0], end=" ")
                print("Confidence Score:", str(np.round(confidence_score * 100, 2)) + "%")

                #set the result to the global variable
                if confidence_score > 0.9:
                    if class_name.strip()[0] == '0':
                        print("Left")
                        await send(b"lef\r\n")
                    elif class_name.strip()[0] == '1':
                        print("Right")
                        await send(b"rig\r\n")

                # Listen to the keyboard for presses.
                keyboard_input = cv2.waitKey(1)

                # 27 is the ASCII for the Esc key on your keyboard.
                if keyboard_input == 27:
                    break

        finally:
            # Release the camera and close all windows
            camera.release()
            cv2.destroyAllWindows()
            await send(b"bye")
            print("done")
            quit()
    # Hub disconnects here when async with block exits.
    print("exit scope")


# Run the main async program.
if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())

