#for raspi
#from gpt
#includes arrow dectect and list4en for signal from hub
import cv2
import numpy as np
import bluetooth  # PyBluez library for Bluetooth communication

# Function to detect left or right arrow
def detect_arrow():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

            if len(approx) == 7:  # 7-sided polygon often corresponds to an arrow
                # Bounding box around the detected arrow
                x, y, w, h = cv2.boundingRect(contour)
                arrow_roi = frame[y:y+h, x:x+w]
                arrow_direction = "Unidentified"

                # Assuming that a left arrow will have more white pixels on the left half, and vice versa
                mid_x = w // 2
                left_part = arrow_roi[:, :mid_x]
                right_part = arrow_roi[:, mid_x:]

                if np.sum(left_part) > np.sum(right_part):
                    arrow_direction = "Left"
                else:
                    arrow_direction = "Right"

                # Display the result and return the direction
                cv2.putText(frame, arrow_direction, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)

                cap.release()
                cv2.destroyAllWindows()
                return arrow_direction

        # Show the live frame
        cv2.imshow('Arrow Detection', frame)

        # Press 'q' to exit the detection loop manually
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# Function to listen for a signal from Spike Prime Hub
def listen_for_signal():
    # Example Bluetooth setup (replace with your setup):
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_socket.bind(("", port))
    server_socket.listen(1)

    print("Waiting for connection from Spike Prime Hub...")
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")

    while True:
        # Receive data from Spike Prime
        data = client_socket.recv(1024)
        if data.decode('utf-8') == "START":
            print("Signal received. Starting arrow detection...")
            direction = detect_arrow()
            if direction:
                print(f"Detected arrow direction: {direction}")
                client_socket.send(direction.encode('utf-8'))
        elif data.decode('utf-8') == "STOP":
            print("Stopping...")
            break

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    listen_for_signal()
