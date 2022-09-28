# this is the helper file for estimating the error of the gaussian fitting
#

import numpy as np


def rms_error(y, y_fit):
    """
    Calculates the root mean square error between two lists of values.

    Parameters
    ----------
    y : list or np.array
        The values to compare to, s['intensity']
    y_fit : list or np.array
        The values to compare, s['intensity_fit']

    Returns
    -------
    float
        root mean square error
    """
    return np.sqrt(np.mean((y - y_fit) ** 2))
