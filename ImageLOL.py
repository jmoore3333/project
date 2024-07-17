# ImageLOL.py

import cv2

def extract_frames(video_path):
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    images = []
    while success:
        images.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        success, image = vidcap.read()
    vidcap.release()
    return images

def calculate_percent_difference(image1, image2):
    if image1 is None or image2 is None:
        return 100.0  # Return 100% difference if any image is None

    resized_image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))
    difference = cv2.absdiff(image1, resized_image2)
    percent_diff = (cv2.countNonZero(difference) / float(image1.size)) * 100
    return percent_diff
