from typing import Tuple

import numpy as np


def random_color() -> Tuple[int, int, int]:
    """Return random color (R, G, B)."""
    return np.random.randint(0, 256, 3).tolist()

def random_position(screen_dim: Tuple[int, int], margin: int = 0) -> Tuple[int, int]:
    """Return random position (int, int) within the screen dimensions.

    Args:
        screen_dim: (width, height)
        margin: width of the strip around the screen that cannot be allocated

    Return:
        random position (x, y)
    """
    screen_width = screen_dim[0]
    screen_height = screen_dim[1]
    x = np.random.randint(0 + margin, screen_width - margin, 1)[0]
    y = np.random.randint(0 + margin, screen_height - margin, 1)[0]
    return (x, y)
