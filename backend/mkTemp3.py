#In this version the ImageProcessor class encapsulates the image processing logic, making the winner() function simpler and more readable. The detect_winner() method of the ImageProcessor class takes a frame as input and returns the name of the region where the template image was detected

##It also reloads from the browser unlike the other.

import cv2
import numpy as np
import os
import json
from flask import Flask, Response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

class ImageProcessor:
    def __init__(self, template_path, detection_regions, threshold):
        self.template_path = template_path
        self.detection_regions = detection_regions
        self.threshold = threshold
        self.template = None
        self.load_template()
    
    def load_template(self):
        template = cv2.imread(self.template_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise ValueError("Could not read template image")
        scale_percent = 60
        width = int(template.shape[1] * scale_percent / 100)
        height = int(template.shape[0] * scale_percent / 100)
        dim = (width, height)
        self.template = cv2.resize(template, dim, interpolation = cv2.INTER_AREA)
    
    def detect_winner(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for region_name, region_coords in self.detection_regions.items():
            region = gray[region_coords[1]:region_coords[3], region_coords[0]:region_coords[2]]
            res = cv2.matchTemplate(region, self.template, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(res)
            if max_val > self.threshold:
                return region_name
        return None

@app.route("/mk")
def winner():
    # Define the detection regions for the left and right sides
    detection_regions = {
        "left": (0, 0, 422, 20),
        "right": (480, 0, 580, 20)
    }
    
    # Set the threshold value for detecting the template image
    threshold = 0.75
    
    # Set up the video capture object
    cap = cv2.VideoCapture('backend/video/MK11video.mov', 0)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Print the size of the frame
    print(f'Frame size: {width} x {height}')
    
    # Initialize the image processor
    template_path = os.path.join("backend", "assets", "superMiniDots.png")
    processor = ImageProcessor(template_path, detection_regions, threshold)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If the frame was not grabbed, break
        if not ret:
            break

        # Detect the winner
        winner = processor.detect_winner(frame)
        if winner is not None:
            print(f"{winner.capitalize()} Side Wins")
            result = {"winner": winner}

            # Encode the resulting frame as JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)
            response = img_encoded.tobytes()
            cap.release()
            cv2.destroyAllWindows()
            return Response(response=winner, status=200, content_type='image/jpeg')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    response = {"winner": "No Winner"}
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
