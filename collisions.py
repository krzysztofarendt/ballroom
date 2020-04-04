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
    x1: int,
    y1: int,
    x2: int,
    y2: int) -> Tuple[float, float, float, float]:
    """2D elastic collision of two balls (particles with non-zero radius).

    The model assumes the balls have non-zero radius.
    The resulting velocities depend not only on the
    initial velocities and masses, but also on the position
    of the balls at the moment of collision.

    Args:
        ux1: x-velocity of ball 1
        uy1: y-velocity of ball 1
        ux2: x-velocity of ball 2
        uy2: y-velocity of ball 2
        m1: mass of ball 1
        m2: mass of ball 2
        x1: x-coordinate of ball 1
        y1: y-coordinate of ball 1
        x2: x-coordinate of ball 2
        y2: y-coordinate of ball 2

    Return:
        resulting velocities (vx1, vy1, vx2, vy2)
    """
    # Reference: https://scipython.com/blog/two-dimensional-collisions/
    mtot = m1 + m2
    c1, c2 = np.array([x1, y1]), np.array([x2, y2])
    d = np.linalg.norm(c1 - c2) ** 2
    u1, u2 = np.array([ux1, uy1]), np.array([ux2, uy2])
    v1 = u1 - 2 * m2 / mtot * np.dot(u1 - u2, c1 - c2) / d * (c1 - c2)
    v2 = u2 - 2 * m1 / mtot * np.dot(u2 - u1, c2 - c1) / d * (c2 - c1)

    return (v1[0], v1[1], v2[0], v2[1])
