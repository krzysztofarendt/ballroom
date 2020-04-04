from typing import Tuple
import numpy as np


def particle_elastic_collision(
    ux1: float,
    uy1: float,
    ux2: float,
    uy2: float,
    m1: float,
    m2: float) -> Tuple[float, float, float, float]:
    """2D elastic collision of two particles.

    The model assumes the particles have zero radius. The larger
    the particles are, the less accurate this model is.

    Args:
        ux1: x-velocity of particle 1
        uy1: y-velocity of particle 1
        ux2: x-velocity of particle 2
        uy2: y-velocity of particle 2
        m1: mass of particle 1
        m2: mass of particle 2

    Return:
        resulting velocities (vx1, vy1, vx2, vy2)
    """
    vx1 = (ux1 * (m1 - m2) / (m1 + m2)) + (ux2 * 2 * m2 / (m1 + m2))
    vx2 = (ux1 * 2 * m1 / (m1 + m2)) + (ux2 * (m2 - m1) / (m1 + m2))
    vy1 = (uy1 * (m1 - m2) / (m1 + m2)) + (uy2 * 2 * m2 / (m1 + m2))
    vy2 = (uy1 * 2 * m1 / (m1 + m2)) + (uy2 * (m2 - m1) / (m1 + m2))

    return (vx1, vy1, vx2, vy2)


def ball_elastic_collision(
    ux1: float,
    uy1: float,
    ux2: float,
    uy2: float,
    m1: float,
    m2: float,
    x1: float,
    y1: float,
    x2: float,
    y2: float) -> Tuple[float, float, float, float]:
    """2D elastic collision of two balls (non-zero radius).

    The model assumes the particles have non-zero radius.
    The resulting velocities depend not only on the
    initial velocities and masses, but also on the position
    of the balls at the moment of collision.

    Args:
        ux1: x-velocity of particle 1
        uy1: y-velocity of particle 1
        ux2: x-velocity of particle 2
        uy2: y-velocity of particle 2
        m1: mass of particle 1
        m2: mass of particle 2

    Return:
        resulting velocities (vx1, vy1, vx2, vy2)
    """
    pass  # TODO
