#!/usr/bin/python2

import cv
import time
import numpy as np
import logging
import random241arg as arg
import random241sensor as sensor
import random241osc as osc

showStream = False
stop_key = 0
capture = True
camNumber = 1
time_delta = 60 * 60 / 2
logging.basicConfig(filename='random241.log',
                    format='%(asctime)s %(message)s',
                    filemode='w', level=logging.INFO)
last_time = time.time()

# Read parameters
params = arg.read_params()
# Define which cam to use, etc.
#cam = sensor.capture(params['-c'], showStream)

# Get frame and size information from camera
cam = cv.CaptureFromCAM(camNumber)
frame = cv.QueryFrame(cam)
if frame is not None:
    frame_size = cv.GetSize(frame)
    logging.info('Grabbing random numbers from: %dx%dpx.',
                 frame_size[0], frame_size[1])

    # Get matrix with values from frame
    mat = cv.GetMat(frame)
    frame_values = np.asarray(mat)
    # Create grayscale image
    gray_values = sensor.bgr2gray(frame_values)

    # Define the time to run the test
    time_delta = time_delta + time.time()

    # Setup OSC
    #osc.connect_to_server('beagleclone', 57120)
    osc.connect_to_server('127.0.0.1', 57120)

    # Main loop for accessing the camera and calculating random numbers from it
    #while True:
    while time_delta > time.time():
#        last_time = time.time()
        img = cv.QueryFrame(cam)
        # Get a numpy array with rgb values
        mat_from_frame = sensor.frame_to_mat(img)
        gray_mat = sensor.bgr2gray(mat_from_frame)
        randomness = sensor.harvest_entropy(gray_mat)
        if randomness is not None:
            delta = time.time() - last_time
            last_time = time.time()
            osc.send_msg(delta, randomness)
        if showStream:
            while stop_key != ord("q"):
                cv.ShowImage("Americium 241", img)
                key = cv.WaitKey(2)

    #time.sleep(5)
    #random241sensor.set_capture(False)
else:
    logging.error('Connect camera %d first!', camNumber)
