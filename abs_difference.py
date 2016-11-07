#####################################################################

# Example : simple image differencing and contrast via multiplication
# from a video file specified on the command line (e.g. python FILE.py video_file)
# or from an attached web camera

# Author : Toby Breckon, toby.breckon@durham.ac.uk

# Copyright (c) 2015 School of Engineering & Computing Science,
#                    Durham University, UK
# License : LGPL - http://www.gnu.org/licenses/lgpl.html

# version: 0.2

#####################################################################

import cv2
import sys

#####################################################################

keep_processing = True;
use_greyscale = False;
camera_to_use = 0; # 0 if you have one camera, 1 or > 1 otherwise

#####################################################################

# this function is called as a call-back everytime the trackbar is moved
# (here we just do nothing)

def nothing(x):
    pass

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

# define display window name

windowName = "Live Camera Input"; # window name
windowName2 = "Difference Image"; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached H/W camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use))):

    # create windows by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);
    cv2.namedWindow(windowName2, cv2.WINDOW_NORMAL);

    # add some track bar controllers for settings

    contrast = 1;
    cv2.createTrackbar("contrast", windowName2, contrast, 30, nothing);

    fps = 25;
    cv2.createTrackbar("fps", windowName2, fps, 25, nothing);

    threshold = 0;
    cv2.createTrackbar("threshold", windowName2, threshold, 255, nothing);


    # if video file successfully open then read frame from video

    if (cap.isOpened):
            ret, frame = cap.read();

    # make a deep copy of this (as all camera frames otherwise reside
    # in the same portion of allocated memory)

    prev_frame = frame.copy();

    while (keep_processing):

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

        if (use_greyscale):
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
            # if the previous frame we stored also has 3 channels (colour)
            if (len(prev_frame.shape) == 3):
                # convert it, otherwise absdiff() will break
                prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY);

        # performing absolute differencing between consecutive frames

        diff_img = cv2.absdiff(prev_frame, frame);

        # retrieve the contrast setting from the track bar

        contrast = cv2.getTrackbarPos("contrast",windowName2);

        # multiple the result to increase the contrast (so we can see small pixel changes)

        brightened_img = diff_img * contrast;

        # display images

        cv2.imshow(windowName, frame);

        # threshold the image if its in grayscale and we have a valid threshold

        threshold = cv2.getTrackbarPos("threshold",windowName2);

        if (use_greyscale and (threshold > 0)):

            # display thresholded image if threshold > 0
            # thresholding : if pixel > (threshold value) set to 255 (white), otherwise set to 0 (black)

            ret, thresholded_img = cv2.threshold(brightened_img, 127, 255, cv2.THRESH_BINARY);
            cv2.imshow(windowName2, thresholded_img);
        else:
            # otherwise just display the non-thresholded one

            cv2.imshow(windowName2, brightened_img);

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)

        fps = cv2.getTrackbarPos("fps",windowName2);
        key = cv2.waitKey(int(1000 / max(1,fps))) & 0xFF; # wait T ms (i.e. 1000ms / 25 fps = 40 ms)

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;

        elif (key == ord('g')):

            # toggle grayscale usage (when they press 'g')

            use_greyscale = not(use_greyscale);

            # if the previous frame we stored also has 3 channels (colour)
            if (len(prev_frame.shape) != 3):
                # convert it to just copying the gray information to all of the
                # three channels (this is a hack), otherwise absdiff() will break
                prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_GRAY2BGR);
        else:

            # make a deep copy of the current frame (as all camera frames otherwise reside
            # in the same portion of allocated memory)
            prev_frame = frame.copy();

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

#####################################################################