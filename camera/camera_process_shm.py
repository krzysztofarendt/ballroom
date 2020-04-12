"""Process-based class for camera capture.

This clas is based on the `shared_memory` module from `multiprocessing` (new in Python 3.8).
This implementation is considerably faster than the one using `multiprocessing.Array`.
"""
import ctypes
import multiprocessing as mp
from multiprocessing import shared_memory
import cv2
import numpy as np


class CameraProcess(mp.Process):

    def __init__(self, width, height):
        super().__init__()

        # Preferres resolution
        self.pref_size = (width, height)
        self.channels = 3

        # Create shared array
        self.shm, self.shared_arr = self.alloc_array(width, height, self.channels)

    def alloc_array(self, width, height, channels):
        a = np.zeros(shape=(width, height, channels), dtype=np.int64)
        shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
        np_array = np.ndarray(a.shape, dtype=np.int64, buffer=shm.buf)
        np_array[:] = a[:]  # Copy the original data into shared memory
        return shm, np_array

    def run(self):
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
            np_array = np.ndarray(
                (self.pref_size[0], self.pref_size[1], self.channels),
                dtype=np.int64,
                buffer=self.shm.buf
            )
            np_array[:] = frame[:]  

    def from_shared_arr(self):
        np_array = np.ndarray(
            (self.pref_size[0], self.pref_size[1], self.channels),
            dtype=np.int64,
            buffer=self.shm.buf
        )
        return np_array


class Camera:

    def __init__(self, width, height):
        self.cam_proc = CameraProcess(width, height)
        self.cam_proc.start()
        self.frame = None

    def capture_frame(self):
        self.frame = self.cam_proc.from_shared_arr()
        return self.frame

    def __del__(self):
        self.cam_proc.shm.close()
        self.cam_proc.shm.unlink()
        self.cam_proc.terminate()
        self.cam_proc.join()
