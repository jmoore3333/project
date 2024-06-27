import cv2
import numpy as np
from PIL import Image

def calculate_percent_difference(image1, image2):
    if len(image1.shape) > 2:
        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    else:
        gray_image1 = image1
    
    if len(image2.shape) > 2:
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    else:
        gray_image2 = image2

    diff_image = cv2.absdiff(gray_image1, gray_image2)
    different_pixels = np.count_nonzero(diff_image)
    total_pixels = gray_image1.shape[0] * gray_image1.shape[1]
    percent_difference = (different_pixels / total_pixels) * 100

    return percent_difference

def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}.")
        return None
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_skip = int(fps)
    frame_count = 0
    success = True
    
    while success:
        success, frame = cap.read()
        
        if frame_count % frame_skip == 0 and success:
            if frame is None:
                print(f"Error: Frame {frame_count} is empty.")
                continue
            frames.append(frame)
        
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    return frames

def extract_bottom_right_corner(frame):
    height, width, _ = frame.shape
    bottom_right_corner = frame[int(height/1.32):height, int(width/1.17):width]
    return bottom_right_corner

video_path = '/Users/jakemoore/Desktop/League of Legends_06-25-2024_20-50-39-443.mp4'
images = extract_frames(video_path)

frame1 = images[0]
frame2 = images[49]

bottom_right1 = extract_bottom_right_corner(frame1)
bottom_right2 = extract_bottom_right_corner(frame2)

pil_bottom_right1 = Image.fromarray(cv2.cvtColor(bottom_right1, cv2.COLOR_BGR2RGB))
pil_bottom_right2 = Image.fromarray(cv2.cvtColor(bottom_right2, cv2.COLOR_BGR2RGB))

pil_bottom_right1.show()
pil_bottom_right2.show()

#print(bottom_right1)
#print(bottom_right2)

percent_diff = calculate_percent_difference(bottom_right1, bottom_right2)
print(f"Percent Difference between Frames: {percent_diff:.2f}%")
