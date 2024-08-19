#raspi to open cam and detect. then send signal to hub when detect something
#libraries for raspi + computer vision 
from ultralytics import YOLO
import cv2 as cv
import cvzone
import math
import time
#lirbaries to connect to primehub
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Color, Icon
from pybricks.tools import wait

#opencv part
cap = cv.VideoCapture(0)  
cap.set(3, 1280) #width
cap.set(4, 720) #height
 
model = YOLO("../Yolo-Weights/yolov8n.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

prev_frame_time = 0
new_frame_time = 0

def getCam():
    while True:
        new_frame_time = time.time()
        img = cap.read()
        results = model(img, stream=True) 
        for r in results: #getting bounding box of each result
            boxes = r.boxes
            for box in boxes:
                #for opencv
                x1, y1, x2, y2 = box.xyxy[0] #find xy of each
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100
                # Class Name
                cls = int(box.cls[0])

                #display class name and confidence level. need to create a rectangle for the text
                #creating with openCV wont have any formatting capablities. text format will be messy, not auto
                cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

        cv.imshow("Image", img)
        cv.waitKey(1)
        if cv.waitKey(1) & 0xFF == ord('q'): #key q for quit
            break

#primehub part
hub = PrimeHub()
def hubSend(lines):
    if lines == 'left':
        hub.display.char("K")  
    elif lines == 'right':
        hub.display.char("R")  
    elif lines == 'forward':
        hub.display.char("F")  
    elif lines == 'backward':
        hub.display.char("B") 
    else:
        hub.display.icon(Icon.SAD) 
    wait(5000)

if __name__ == "__main__":
    getCam()
