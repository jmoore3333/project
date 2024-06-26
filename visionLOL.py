import cv2
import numpy as np
import os

def calculate_percent_difference(image_path1, image_path2):
    # Load the two images
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)

    # Check if images were successfully loaded
    if image1 is None or image2 is None:
        print("Error: Could not load images.")
        return None
    
    # Ensure both images have the same shape
    if image1.shape != image2.shape:
        print("Error: Images must have the same dimensions.")
        return None
    
    # Convert images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

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
        print("Error: Could not open video.")
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
            # Append the frame to the list
            frames.append(frame)
        
        frame_count += 1
    
    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
    
    return frames

# Example usage:
image_path1 = '/Users/jakemoore/Downloads/image1.jpeg'
image_path2 = '/Users/jakemoore/Downloads/image2.jpeg'
percent_diff = calculate_percent_difference(image_path1, image_path2)


if percent_diff is not None:
    print(f"Percent Difference: {percent_diff:.2f}%")
