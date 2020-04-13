from multiprocessing import shared_memory, Lock
import logging
import numpy as np


class SharedFrame:
    """Shared memory block for video frame storage.

    The shared array is initialized with zeros.

    Args:
        width (int): frame width in pixels
        height (int): frame height in pixels
        channels (int): number of channels
        dtype (type): data type, default `np.uint8`

    Attributes:
        shm: shared memory block
    """
    def __init__(self, width, height, channels=3, dtype=np.uint8):
        logging.debug("Initializing SharedFrame")
        self.width = width
        self.height = height
        self.channels = channels
        self.dtype = dtype
        self.shm, self.frame = self._alloc_array(width, height, channels)
        self.lock = Lock()

    def _alloc_array(self, width, height, channels):
        """Creates a shared memory block and initialize with zeros.

        Args:
            width (int): array's first dimension
            height (int): array's second dimension
            channels (int): array's third dimension

        Return:
            tuple(shared_memory.SharedMemory, np.ndarray)
        """
        a = np.zeros(shape=(width, height, channels), dtype=self.dtype)
        shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
        np_array = np.ndarray(a.shape, dtype=self.dtype, buffer=shm.buf)
        np_array[:] = a[:]  # Copy the original data into shared memory
        logging.debug(f"Allocated shared memory: {shm}")

        return shm, np_array

    def get_array(self):
        """Gets array from the shared memory.

        Return:
            np.ndarray
        """
        np_array = np.ndarray(
            (self.width, self.height, self.channels),
            dtype=self.dtype,
            buffer=self.shm.buf
        )
        return np_array

    def put_array(self, arr):
        """Puts array to the shared memory.

        Args:
            arr (np.ndarray): array

        Return:
            None
        """
        # Lock not needed, if only one process
        # is supposed to write to shared memory
        # (it cannot be guaranteed though)
        self.lock.acquire()
        shared_arr = np.ndarray(
            (self.width, self.height, self.channels),
            dtype=self.dtype,
            buffer=self.shm.buf
        )
        shared_arr[:] = arr[:]
        self.lock.release()

    def __del__(self):
        logging.debug(f"Unlinking {self.shm} and deleting {self}")
        self.shm.close()
        self.shm.unlink()
