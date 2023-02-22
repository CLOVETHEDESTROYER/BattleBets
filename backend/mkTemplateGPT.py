import cv2
import numpy as np
import os

# Load the template image
template_path = os.path.join("backend", "assets", "superMiniDots.png")
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

# Resize image and template
scale_percent = 60 # percent of original size
width = int(template.shape[1] * scale_percent / 100)
height = int(template.shape[0] * scale_percent / 100)
dim = (width, height)
template = cv2.resize(template, dim, interpolation = cv2.INTER_AREA)

# Define the detection region variables
left_region = (0, 0, 422, 20)
right_region = (480, 0, 580, 20)

# Define the threshold value for detecting the template image
threshold = 0.7

# Set up the video capture object
cap = cv2.VideoCapture('backend/video/MK11video.mov', 0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Print the size of the frame
print(f'Frame size: {width} x {height}')

def draw_rectangle(frame, region, color):
    x, y, w, h = region
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 7)

def Winner():
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame was not grabbed, break
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the template image in the left and right regions
        left = gray[left_region[1]:left_region[3], left_region[0]:left_region[2]]
        right = gray[right_region[1]:right_region[3], right_region[0]:right_region[2]]
        res_left = cv2.matchTemplate(left, template, cv2.TM_CCOEFF_NORMED)
        res_right = cv2.matchTemplate(right, template, cv2.TM_CCOEFF_NORMED)

        # Find the maximum correlation coefficient in each region
        max_val_left = np.max(res_left)
        max_val_right = np.max(res_right)

        # Draw a rectangle around the detected template image
        if max_val_left > threshold:
            draw_rectangle(frame, left_region, (0, 0, 255))
            print("Left Side Wins")
            return "Left Side Wins"
        elif max_val_right > threshold:
            draw_rectangle(frame, right_region, (0, 0, 255))
            print("Right Side Wins")
            return "Right Side Wins"
        
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

Winner()
