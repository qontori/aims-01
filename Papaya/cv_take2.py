from ultralytics import YOLO
import cv2 as cv
import cvzone
import math
import time
 
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
 
while True:
    new_frame_time = time.time()
    success, img = cap.read()
    results = model(img, stream=True) 
    for r in results: #getting bounding box of each result
        boxes = r.boxes
        for box in boxes:
            #for opencv
            x1, y1, x2, y2 = box.xyxy[0] #find xy of each
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)

            #for cvzone (looks fancy)
            #w, h = x2-x1, y2-y1
            #bbox = int(x1), int(y1), int(w), int(h)
            #cvzone.cornerRect(img,bbox)

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])

            #display class name and confidence level. need to create a rectangle for the text
            #creating with openCV wont have any formatting capablities. text format will be messy, not auto
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)
 
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print(fps)
 
    cv.imshow("Image", img)
    cv.waitKey(1)