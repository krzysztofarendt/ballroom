# Pick the face detection implementation
# ======================================
from .dlib_process import FaceDetector  # Multi-process (>=Python 3.8)
# from .dlib import FaceDetector        # Single-process
