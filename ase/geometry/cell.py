from __future__ import print_function, division
# Copyright (C) 2010, Jesper Friis
# (see accompanying license files for details).

import numpy as np
from numpy import pi, sin, cos, arccos, sqrt, dot
from numpy.linalg import norm


def unit_vector(x):
    """Return a unit vector in the same direction as x."""
    y = np.array(x, dtype='float')
    return y / norm(y)


def angle(x, y):
    """Return the angle between vectors a and b in degrees."""
    return arccos(dot(x, y) / (norm(x) * norm(y))) * 180. / pi


def cell_to_cellpar(cell):
    """Returns the cell parameters [a, b, c, alpha, beta, gamma] as a list.

    If an angle is undefined, it will be returned as None.  This will happen
    if not all there lattice vectors are defined.
    """
    lengths = np.linalg.norm(cell, axis=1)
    angles = []
    for i in range(3):
        j = i - 1
        k = i - 2
        ll = lengths[j] * lengths[k]
        if ll > 1e-16:
            x = np.dot(cell[j], cell[k]) / ll
            angle = 180.0 / pi * arccos(x)
        else:
            angle = None
        angles.append(angle)
    return lengths.tolist() + angles


def cellpar_to_cell(cellpar, ab_normal=(0, 0, 1), a_direction=None):
    """Return a 3x3 cell matrix from `cellpar` = [a, b, c, alpha,
    beta, gamma].  The returned cell is orientated such that a and b
    are normal to `ab_normal` and a is parallel to the projection of
    `a_direction` in the a-b plane.

    Default `a_direction` is (1,0,0), unless this is parallel to
    `ab_normal`, in which case default `a_direction` is (0,0,1).

    The returned cell has the vectors va, vb and vc along the rows. The
    cell will be oriented such that va and vb are normal to `ab_normal`
    and va will be along the projection of `a_direction` onto the a-b
    plane.

    Example:

    >>> cell = cellpar_to_cell([1, 2, 4, 10, 20, 30], (0, 1, 1), (1, 2, 3))
    >>> np.round(cell, 3)
    array([[ 0.816, -0.408,  0.408],
           [ 1.992, -0.13 ,  0.13 ],
           [ 3.859, -0.745,  0.745]])

    """
    if a_direction is None:
        if np.linalg.norm(np.cross(ab_normal, (1, 0, 0))) < 1e-5:
            a_direction = (0, 0, 1)
        else:
            a_direction = (1, 0, 0)

    # Define rotated X,Y,Z-system, with Z along ab_normal and X along
    # the projection of a_direction onto the normal plane of Z.
    ad = np.array(a_direction)
    Z = unit_vector(ab_normal)
    X = unit_vector(ad - dot(ad, Z) * Z)
    Y = np.cross(Z, X)

    # Express va, vb and vc in the X,Y,Z-system
    alpha, beta, gamma = 90., 90., 90.
    if isinstance(cellpar, (int, float)):
        a = b = c = cellpar
    elif len(cellpar) == 1:
        a = b = c = cellpar[0]
    elif len(cellpar) == 3:
        a, b, c = cellpar
        alpha, beta, gamma = 90., 90., 90.
    else:
        a, b, c, alpha, beta, gamma = cellpar
    alpha *= pi / 180.0
    beta *= pi / 180.0
    gamma *= pi / 180.0
    va = a * np.array([1, 0, 0])
    vb = b * np.array([cos(gamma), sin(gamma), 0])
    cx = cos(beta)
    cy = (cos(alpha) - cos(beta) * cos(gamma)) / sin(gamma)
    cz = sqrt(1. - cx * cx - cy * cy)
    vc = c * np.array([cx, cy, cz])

    # Convert to the Cartesian x,y,z-system
    abc = np.vstack((va, vb, vc))
    T = np.vstack((X, Y, Z))
    cell = dot(abc, T)
    return cell


def metric_from_cell(cell):
    """Calculates the metric matrix from cell, which is given in the
    Cartesian system."""
    cell = np.asarray(cell, dtype=float)
    return np.dot(cell, cell.T)


def crystal_structure_from_cell(cell, eps=1e-4):
    """Return the crystal structure as a string calculated from the cell.

    Supply a cell (from atoms.get_cell()) and get a string representing
    the crystal structure returned. Works exactly the opposite
    way as ase.dft.kpoints.get_special_points().

    Parameters:

    cell : numpy.array or list
        An array like atoms.get_cell()

    Returns:

    crystal structure : str
        'cubic', 'fcc', 'bcc', 'tetragonal', 'orthorhombic',
        'hexagonal' or 'monoclinic'
    """
    cellpar = np.array(cell_to_cellpar(cell))
    abc = cellpar[:3]
    angles = cellpar[3:] / 180 * pi
    a, b, c = abc
    alpha, beta, gamma = angles
    if abc.ptp() < eps and abs(angles - pi / 2).max() < eps:
        return 'cubic'
    elif abc.ptp() < eps and abs(angles - pi / 3).max() < eps:
        return 'fcc'
    elif abc.ptp() < eps and abs(angles - np.arccos(-1 / 3)).max() < eps:
        return 'bcc'
    elif abs(a - b) < eps and abs(angles - pi / 2).max() < eps:
        return 'tetragonal'
    elif abs(angles - pi / 2).max() < eps:
        return 'orthorhombic'
    elif (abs(a - b) < eps and
          abs(gamma - pi / 3 * 2) < eps and
          abs(angles[:2] - pi / 2).max() < eps):
        return 'hexagonal'
    elif (c >= a and c >= b and alpha < pi / 2 and
          abs(angles[1:] - pi / 2).max() < eps):
        return 'monoclinic'
    else:
        raise ValueError('Cannot find crystal structure')


def complete_cell(cell):
    """Calculate complete cell with missing lattice vectors.

    Returns a new 3x3 ndarray.
    """

    cell = np.array(cell, dtype=float)
    missing = np.nonzero(~cell.any(axis=1))[0]

    if len(missing) == 3:
        cell.flat[::4] = 1.0
    if len(missing) == 2:
        # Must decide two vectors:
        i = 3 - missing.sum()
        assert abs(cell[i, missing]).max() < 1e-16, "Don't do that"
        cell[missing, missing] = 1.0
    elif len(missing) == 1:
        i = missing[0]
        cell[i] = np.cross(cell[(i + 1) % 3], cell[(i + 2) % 3])
        cell[i] /= np.linalg.norm(cell[1])

    return cell


def is_orthorhombic(cell):
    return not (np.flatnonzero(cell) % 4).any()


def orthorhombic(cell):
    """Return cell as three box dimensions or raise ValueError."""
    if not is_orthorhombic(cell):
        raise ValueError('Not orthorhombic')
    return cell.diagonal().copy()
