# Pick the camera capture implementation
# ======================================
from .camera_process_shm import Camera      # Multi-process, shared_memory-based (>=Python 3.8)
# from .camera import Camera                # Single-process
