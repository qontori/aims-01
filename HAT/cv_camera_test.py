import cv2

def check_camera(index=0):
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Camera {index} is connected.")
        cap.release()
        return True
    else:
        print(f"Camera {index} is not connected.")
        return False
    
def test_camera_properties(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Error: Camera at index {index} could not be opened.")
        return
    
    # Print the current resolution
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Current resolution: {width}x{height}")

    # Test setting the resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    # Print the updated resolution
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Updated resolution: {width}x{height}")

    cap.release()

def show_camera_preview(index=0):
    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        print(f"Error: Camera {index} could not be opened.")
        return

    # Set the frame width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Display the resulting frame
        cv2.imshow('Camera Preview', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_index = 0  # Adjust if necessary
    if check_camera(camera_index):
        test_camera_properties(camera_index)
        show_camera_preview(camera_index)