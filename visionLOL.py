import cv2
import numpy as np

def calculate_percent_difference(image1, image2):
    # Resize image1 to match image2's dimensions if they are not the same
    if image1.shape[:2] != image2.shape[:2]:
        image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))

    # Normalize images to range [0, 1]
    norm_image1 = image1.astype(np.float32) / 255.0
    norm_image2 = image2.astype(np.float32) / 255.0
    
    # Calculate absolute difference
    abs_diff = np.abs(norm_image1 - norm_image2)
    
    # Calculate percent difference
    percent_difference = np.mean(abs_diff) * 100.0
    
    return percent_difference

def extract_frames(video_path):
    frames = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video at {video_path}.")
        return frames
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_skip = int(fps)
    frame_count = 120
    success = True
    
    while success:
        success, frame = cap.read()
        
        if frame_count % frame_skip == 0 and success:
            if frame is None:
                print(f"Error: Frame {frame_count} is empty.")
                continue
            
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray_frame)
        
        frame_count += 1
    
    cap.release()
    return frames

def find_minimap_in_frame(frame, minimap_template):
    # Resize the template to match different sizes
    sizes = np.linspace(0.5, 1.5, 10)  # Example: Resize factors from 50% to 150%
    found = False
    best_match = None
    best_match_location = None

    for size in sizes:
        resized_template = cv2.resize(minimap_template, (0, 0), fx=size, fy=size)
        
        # Check if resized template is smaller than frame
        if resized_template.shape[0] > frame.shape[0] or resized_template.shape[1] > frame.shape[1]:
            continue  # Skip if template is larger than frame
        
        result = cv2.matchTemplate(frame, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if not best_match or max_val > best_match:
            best_match = max_val
            best_match_location = max_loc
            found = True

    if found:
        # Get the coordinates of the matched region
        h, w = resized_template.shape[:2]
        top_left = best_match_location
        bottom_right = (top_left[0] + w, top_left[1] + h)
        
        # Draw a rectangle around the matched region (optional)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        
        # Crop the minimap region from the frame
        minimap_region = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        return minimap_region
    else:
        return None

video_path = '/Users/jakemoore/Desktop/project/League of Legends_06-25-2024_20-50-39-443.mp4'
images = extract_frames(video_path)

if not images:
    print(f"Error: No frames extracted from {video_path}.")
    exit()

# Load or create the minimap template
minimap_template_path = '/Users/jakemoore/Desktop/project/minimap.png'
minimap_template = cv2.imread(minimap_template_path, cv2.IMREAD_GRAYSCALE)

# Assume using the first frame for demonstration
orig_frame = images[1]
height, width = orig_frame.shape[:2]
start_row = int(height * 0.50)
start_col = int(width * 0.75)
frame = orig_frame[start_row:, start_col:]

# Find and extract the minimap region from frame
minimap_region = find_minimap_in_frame(frame, minimap_template)

if minimap_region is not None:
    # Display the result (optional)
    cv2.imshow('Original image', frame)
    cv2.imshow('Minimap Region', minimap_region)
    cv2.imshow('Template', minimap_template)

    percent_diff = calculate_percent_difference(minimap_region, minimap_template)
    print(f"Percent Difference between Frames: {percent_diff:.2f}%")

    # Wait for a key press (waitKey returns the ASCII value of the key pressed or -1 if no key is pressed)
    cv2.waitKey(0)

# Close all OpenCV windows
cv2.destroyAllWindows()
