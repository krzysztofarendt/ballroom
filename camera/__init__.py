# Pick the camera capture implementation
# ======================================
from .camera_process_shm import Camera  # Multi-process (>=Python 3.8)
# from .camera import Camera            # Single-process
