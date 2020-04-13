"""Process-based class for camera capture.

This class is based on the `shared_memory` module from `multiprocessing` (new in Python 3.8).
This implementation is considerably faster than the previous one using `multiprocessing.Array`.
"""
import ctypes
import multiprocessing as mp
from multiprocessing import shared_memory
import cv2
import numpy as np
import logging


class CameraProcess(mp.Process):

    def __init__(self, width, height, shared_frame):
        super().__init__()
        logging.debug(f"Initializing {self.name}")

        # Preferres resolution
        self.pref_size = (width, height)
        self.channels = 3

        # Shared memory block
        self.shared_frame = shared_frame

    def run(self):
        logging.debug("Run CameraProcess in a separate process")
        logging.debug(f"self.shared_frame: {self.shared_frame}")

        # Choose Driver Show driver and initialize
        camera_driver = cv2.CAP_DSHOW
        cap = cv2.VideoCapture(0, camera_driver)

        # Set resolution
        # (if it isn't supported, it will take the default resolution)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.pref_size[0])
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.pref_size[1])

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # If size not equal to the preferred -> resize
            if (frame.shape[0] != self.pref_size[1]) \
                and (frame.shape[1] != self.pref_size[0]):
                frame = cv2.resize(frame, self.pref_size)

            # Swap axes to be compatible with pygame format (width, height, channel)
            frame = np.swapaxes(frame, 0, 1)

            # Write to shared memory
            # Lock not needed, because only one process writes to shared memory
            self.shared_frame.put_array(frame)


class Camera:

    multiprocessing = True

    def __init__(self, width, height, shared_frame):
        logging.debug("Initializing Camera")
        self.cam_proc = CameraProcess(width, height, shared_frame)
        self.cam_proc.start()
        self.shared_frame = shared_frame

    def capture_frame(self):
        return self.shared_frame.get_array()

    def __del__(self):
        logging.debug(f"Terminating {self.cam_proc.name}")
        self.cam_proc.terminate()
        self.cam_proc.join()
