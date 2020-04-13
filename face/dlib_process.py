import logging
from multiprocessing import Process, Queue
import queue
import dlib
import numpy as np


class FaceDetectorProcess(Process):

    def __init__(self, shared_frame):
        super().__init__()
        self.skip_frames = 10
        self.shared_frame = shared_frame
        self.queue = Queue(maxsize=0)

    def run(self):
        logging.debug(f"{self.name} started")
        detector = dlib.get_frontal_face_detector()
        frame_counter = 0

        while True:
            # Get frame from shared memory
            frame = self.shared_frame.get_array()
            # Put detections to queue
            frame_counter += 1

            if frame_counter >= self.skip_frames:
                frame_counter = 0
                # Swap axes to be compatible with dlib format
                frame = np.swapaxes(np.array(frame), 0, 1)
                # Detect
                dets = detector(frame, 1)
                # Conver detections to array
                dets_list = [[d.left(), d.top(), d.right(), d.bottom()] for d in dets]
                logging.debug(f"Detections: {dets_list}")
                # Add dets to queue
                self.queue.put(dets_list)


class FaceDetector:

    multiprocessing = True

    def __init__(self, shared_frame):
        logging.debug("Initializing FaceDetector")
        self.face_det_proc = FaceDetectorProcess(shared_frame)
        self.face_det_proc.start()
        self.prev_dets = np.array([])

    def detect(self, frame):
        """Detect faces.

        Args:
            frame: ignored (left for compatibility with
                face.dlib.FaceDetector)
        """
        try:
            # Read from queue
            detections = self.face_det_proc.queue.get(block=False)
            detections = np.array(detections)
            if detections.size > 0:
                self.prev_dets = detections
        except queue.Empty as e:
            # If queue empty, return previous detections
            logging.warning("Queue empty! Returning last known detections")
            detections = self.prev_dets
        return detections

    def __del__(self):
        logging.debug(f"Terminating {self.face_det_proc.name}")
        self.face_det_proc.terminate()
        self.face_det_proc.join()
