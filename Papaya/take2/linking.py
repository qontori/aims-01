import tensorflow as tf
import cv2
import numpy as np


# Load the TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="/home/robothink/Desktop/raspi2prime/training/model_unquant.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load the labels
class_names = open("/home/robothink/Desktop/raspi2prime/training/labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

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
        #print("Class:", class_name.strip()[2:])
        print("Confidence Score:", confidence_score)
        
        value = class_name.strip()[2:]

        with open('link2.py','w') as file:
            file.write('TEXT = ', value)
            

        # with open(value, "w") as file:
        #     file.write(1)
        #     if value == "left" and os.path.isfile("right"):
        #         os.remove("right")
        #     elif value == "right" and os.path.isfile("left"):
        #         os.remove("left")
            
        


        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the Esc key on your keyboard.
        if keyboard_input == 27:
            break

finally:
    # Release the camera and close all windows
    camera.release()
    cv2.destroyAllWindows()
