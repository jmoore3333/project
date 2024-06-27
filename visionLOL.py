import cv2
import numpy as np
from PIL import Image

def calculate_percent_difference(image1, image2):
    # Convert images to grayscale if they are not already
    if len(image1.shape) > 2:
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    else:
        gray_image1 = image1
    
    if len(image2.shape) > 2:
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    else:
        gray_image2 = image2

    # Compute absolute difference between the two images
    diff_image = cv2.absdiff(gray_image1, gray_image2)

    # Count non-zero pixels in the difference image
    different_pixels = np.count_nonzero(diff_image)

    # Calculate percent difference based on total pixels in gray_image1
    total_pixels = gray_image1.shape[0] * gray_image1.shape[1]  # Assuming images are 2D

    percent_difference = (different_pixels / total_pixels) * 100

    return percent_difference

def extract_frames(video_path):
    frames = []  # List to store frames
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}.")
        return None
    
    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the number of frames to skip to get 1 frame per second
    frame_skip = int(fps)
    
    # Initialize variables
    frame_count = 0
    success = True
    
    # Loop through the video frames
    while success:
        success, frame = cap.read()
        
        # Skip frames to get 1 frame per second
        if frame_count % frame_skip == 0 and success:
            # Check if frame is valid
            if frame is None:
                print(f"Error: Frame {frame_count} is empty.")
                continue
            
            # Append the frame to the list
            frames.append(frame)
        
        frame_count += 1
    
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
    
    return frames

# Example usage:
video_path = '/Users/jakemoore/Desktop/League of Legends_06-25-2024_20-50-39-443.mp4'

# Extract frames from the video
images = extract_frames(video_path)

if images is not None:
    print(f"Number of frames extracted: {len(images)}")
else:
    print("Frame extraction failed. Check the video path and ensure the video file is valid.")

# Choose two frames to compare (for example, first and 50th frames)
frame1 = images[0]
pil_image1 = Image.fromarray(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for PIL

frame2 = images[49]
pil_image2 = Image.fromarray(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for PIL

pil_image1.show()
pil_image2.show()
# Calculate percent difference between the frames
percent_diff = calculate_percent_difference(frame1, frame2)

print(f"Percent Difference between Frames: {percent_diff:.2f}%")
