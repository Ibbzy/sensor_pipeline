import cv2
import time

def capture_video(output_path, duration=5, fps=30):
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    
    # Get the default width and height of the video frame
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the codec and create a VideoWriter object to write frames to a file
    # Use 'mp4v' codec to create an MP4 file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    # Calculate the end time for the recording
    start_time = time.time()
    end_time = start_time + duration
    print(f"Recording started for {duration} seconds")
    while time.time() < end_time:
        
        ret, frame = cap.read()
        if ret:
            # Write the frame to the output video file
            out.write(frame)
        else:
            break
    print(f"Recording done")
    # Release resources
    cap.release()
    out.release()
