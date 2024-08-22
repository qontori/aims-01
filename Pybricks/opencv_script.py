import asyncio

from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np
import os

camera = None
interpreter = None
class_names = None

def opencv_setup():
    global camera, interpreter, class_names
    # Load the TensorFlow Lite model
    interpreter = Interpreter(model_path="../training/model_unquant.tflite")
    interpreter.allocate_tensors()

    # Load the labels
    class_names = open("../training/labels.txt", "r").readlines()

    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    print("starting camera")

def process_image():
    global camera, interpreter
    ret, image = camera.read()
    if not ret:
        print("Failed to grab frame")
        return ""
    cv2.imshow("Webcam Image", image)
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_normalized = (image_array / 127.5) - 1.0
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], image_normalized)
    interpreter.invoke()
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    index = np.argmax(output_data)
    result = class_names[index]
    confidence_score = output_data[0][index]

    # Print prediction and confidence score
    print("Class:", result, end=" ")
    print("Confidence Score:", str(np.round(confidence_score * 100, 2)) + "%")

    #set the result to the global variable
    if confidence_score > 0.9:
        if '0' in result:
            return "lef\r\n"
        elif '1' in result:
            return "rig\r\n"
    return ""

def opencv_cleaup():
    global camera
    camera.release()
    cv2.destroyAllWindows()
    print("done")
    quit()
    print("exit scope")