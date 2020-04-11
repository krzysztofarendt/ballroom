import numpy as np
import cv2


class Camera:

    def __init__(self, width, height):
        # Preferres resolution
        self.pref_size = (width, height)

        # Choose Driver Show driver and initialize
        camera_driver = cv2.CAP_DSHOW
        self.cap = cv2.VideoCapture(0, camera_driver)

        # Set resolution
        # (if it isn't supported, it will take the default resolution)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(width))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(height))

    def capture_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        # BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # If size not equal to the preferred -> resize
        if (frame.shape[0] != self.pref_size[1]) \
            and (frame.shape[1] != self.pref_size[0]):
            frame = cv2.resize(frame, self.pref_size)

        # Swap access to be compatible with pygame format (width, height, channel)
        frame = np.swapaxes(frame, 0, 1)

        return frame

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
