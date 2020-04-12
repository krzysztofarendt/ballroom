"""Process-based class for camera capture.

This class is based on the `multiprocessing.Array` class.
It is deprecated. You should use the implementation from `camera.camera_process_shm`.
"""
import ctypes
import multiprocessing as mp
import cv2
import numpy as np


class CameraProcess(mp.Process):

    def __init__(self, width, height):
        super().__init__()

        # Preferres resolution
        self.pref_size = (width, height)
        self.channels = 3

        # Create shared array
        self.shared_arr = self.alloc_array(width, height, self.channels)

    def alloc_array(self, width, height, channels):
        # Shared, can be used from multiple processes
        arr = mp.Array(ctypes.c_double, width * height * channels)

        return arr

    def capture_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        # BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # If size not equal to the preferred -> resize
        if (frame.shape[0] != self.pref_size[1]) \
            and (frame.shape[1] != self.pref_size[0]):
            frame = cv2.resize(frame, self.pref_size)

        # Swap axes to be compatible with pygame format (width, height, channel)
        frame = np.swapaxes(frame, 0, 1)

        return frame

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

            with self.shared_arr.get_lock():
                self.shared_arr[:] = frame.flatten()[:]

    def from_shared_arr(self):
        # Get 1D array from buffer (arr and self.shared_arr share the same memory)
        arr = np.frombuffer(self.shared_arr.get_obj())
        # Reshape to 2D (frame and arr share the same memory)
        frame = arr.reshape((self.pref_size[0], self.pref_size[1], self.channels))

        return frame
    

class Camera:

    def __init__(self, width, height):
        self.cam_proc = CameraProcess(width, height)
        self.cam_proc.start()
        self.frame = None

    def capture_frame(self):
        self.frame = self.cam_proc.from_shared_arr()
        return self.frame

    def __del__(self):
        self.cam_proc.terminate()
        self.cam_proc.join()
        cv2.destroyAllWindows()
