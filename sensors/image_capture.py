import cv2

def capture_image(output_path):
    """Capture a single image from the default camera and save it to the output path."""
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        raise Exception("Could not open the camera.")
    
    # Read a frame from the camera
    ret, frame = cap.read()
    
    if ret:
        # Write the frame (image) to the output path
        cv2.imwrite(output_path, frame)
        print(f"Image captured and saved to {output_path}")
    else:
        raise Exception("Failed to capture image from camera.")
    
    # Release the camera resource
    cap.release()
