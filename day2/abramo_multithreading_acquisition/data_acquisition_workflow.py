# Camera acquisition workflow based on OpenCV
# The workflow is composed of three threads:
# 1. grab_frame: grabs frames from the camera and puts them in a deque
# 2. process_frame: processes the frames in the deque and puts them in another deque
# 3. view_image: displays the frames in the deque
# Author: Jacopo Abramo, 26.09.2023

import cv2
import time
from collections import deque
from napari.qt.threading import thread_worker

@thread_worker
def grab_frame(out_q: deque) -> None:
    camera = cv2.VideoCapture(0) # on laptops, opens the default integrated camera
    prev_time = 0
    while True:
        ret, img = camera.read() # OpenCV in Python returns a flag - confirming if the image was captured - and the captured image
        out_q.append(img)
        curr_time = time.time()
        fps = 1.0 / (curr_time - prev_time)
        if ret:
            print("Frame rate: ", fps)
        else:
            print("Frame lost!")
        prev_time = curr_time

@thread_worker
def process_frame(in_q: deque, out_q: deque) -> None:
    while True:
        try:
            image = in_q.pop()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            out_q.append(image)
        except IndexError: # thrown by calling in_q.pop() in case the deque is empty
            pass

# note how we are NOT using thread_worker
# for this method...
def view_image(in_q: deque) -> None:
    
    while True:
        try:
            image = in_q.pop()
            cv2.imshow("input", image)
            
            key = cv2.waitKey(1)
            if key == 27:
                break
        except KeyboardInterrupt:
            break
        except IndexError:
            pass

grab_to_process = deque([])
process_to_view = deque([])

grabber = grab_frame(grab_to_process)
processer = process_frame(grab_to_process, process_to_view)

grabber.start()
processer.start()

view_image(process_to_view)

processer.quit()
grabber.quit()
            