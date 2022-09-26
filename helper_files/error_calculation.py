# this is the helper file for estimating the error of the gaussian fitting
#

import numpy as np


def rms_error(y, y_fit):
    """
    Calculates the root mean square error between two lists of values.

    Parameters
    ----------
    y : list
        list of values
    y_fit : list
        list of values

    Returns
    -------
    float
        root mean square error
    """
    return np.sqrt(np.mean((y - y_fit) ** 2))
