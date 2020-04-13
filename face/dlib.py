import logging
import dlib
import numpy as np


class FaceDetector:

    multiprocessing = False

    def __init__(self):
        self.multiprocessing = False
        self.detector = dlib.get_frontal_face_detector()
        self.skip_frames = 30
        self.frame_counter = 0
        self.prev_dets = np.array([])

    def detect(self, frame):
        self.frame_counter += 1

        if self.frame_counter >= self.skip_frames:
            self.frame_counter = 0
            # Swap axes to be compatible with dlib format
            frame = np.swapaxes(np.array(frame), 0, 1)
            # Detect
            dets = self.detector(frame, 0)
            # Conver detections to array
            dets_list = [[d.left(), d.top(), d.right(), d.bottom()] for d in dets]
            dets = np.array(dets_list)
            # Save dets to buffer
            self.prev_dets = dets
        else:
            # Return previous detections
            dets = self.prev_dets

        return dets
