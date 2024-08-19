import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    # Convert to grayscale for easier processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and improve contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges in the image using Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edges image
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Approximate the contour
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

        # Use the length of the contour approximation to identify shapes
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            # Compute the bounding box of the contour and use it to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            # A square will have an aspect ratio that is approximately equal to one, otherwise, the shape is a rectangle
            shape = "Square" if aspectRatio >= 0.95 and aspectRatio <= 1.05 else "Rectangle"
        elif len(approx) > 4:
            shape = "Circle"
        else:
            shape = "Unidentified"

        # Draw the contour and shape name on the original frame
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        x, y = approx[0][0]
        cv2.putText(frame, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Object Detection', frame)

    # Break the loop if the user presses the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
