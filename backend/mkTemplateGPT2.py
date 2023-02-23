import cv2
import numpy as np
import os
import json



def Winner(cap, threshold, template, left_region, right_region):
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

        # Draw a rectangle around the detected template image and print the result
        if max_val_left > threshold:
            cv2.rectangle(frame, (left_region[0], left_region[1]), (left_region[2], left_region[3]), (0, 0, 255), 7)
            response = {"winner": "Left Side Wins"}
            return json.dumps(response)
        elif max_val_right > threshold:
            cv2.rectangle(frame, (right_region[0], right_region[1]), (right_region[2], right_region[3]), (0, 0, 255), 7)
            response = {"winner": "Right Side Wins"}
            return json.dumps(response)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    response = {"winner": "No Winner"}
    return json.dumps(response)
