from tflite_runtime.interpreter import Interpreter
import cv2
import numpy as np

camera = None
interpreter = None
class_names = None

def opencv_setup():
    global camera, interpreter, class_names
    #load the tensor flow lite model
    interpreter = Interpreter(model_path="../training/model_unquant.tflite")
    interpreter.allocate_tensors()
    #load the labels for the model
    class_names = open("../training/labels.txt", "r").readlines()
    #gets the first index camera, probably the webcam
    camera = cv2.VideoCapture(0)zed = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_normalized = (image_array / 127.5) - 1.0
    #interpret
    print("starting camera")

def process_image():
    global camera, interpreter
    #pulls a image from the web cam
    ret, image = camera.read()
    if not ret:
        print("Failed to grab frame")
        return b"12345"
    #shows a preview window for the webcam
    cv2.imshow("Webcam Image", image)
    #condition the image for tensorflow interpreter
    image_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_normalized = (image_array / 127.5) - 1.0
    #interpret
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], image_normalized)
    interpreter.invoke()
    output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    index = np.argmax(output_data)
    #the results
    result = class_names[index]
    confidence_score = output_data[0][index]
    #print("Class:", result, end=" ")
    #print("Confidence Score:", str(np.round(confidence_score * 100, 2)) + "%")
    #decide what to do with result, in this case only send a left right message if confidence > 90%
    if confidence_score > 0.9:
        if '0' in result:
            print("left")
            return b"lef\r\n"zed = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_normalized = (image_array / 127.5) - 1.0
    #interpret

def opencv_cleaup():
    global camera
    camera.release()
    cv2.destroyAllWindows()
    print("done")
    quit()