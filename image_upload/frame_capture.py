# Importing all necessary libraries
import cv2
import os
import time

# Read the video from specified path
cam = cv2.VideoCapture("search_for_red_car.mp4")

# Get number of frames per second for video 
frame_per_second = cam.get(cv2.CAP_PROP_FPS) 

try:
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')

# frame
currentframe = 0

while (True):
    # reading from frame
    ret, frame = cam.read()

    if ret:
        # capture every second 
        if currentframe % (3 * frame_per_second): 
            name = './data/frame' + str(currentframe) + '.jpg'
            print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
        currentframe += 1
    else:
        break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()