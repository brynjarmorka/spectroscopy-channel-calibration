# this is the helper file for the gaussian fitting

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import norm


def gaussian(x, amp, mu, std):
    """
    Returns the value of a gaussian function with amplitude amp, mean mu and standard deviation std at x.

    Parameters
    ----------
    x : list
        x values to evaluate the gaussian at
    amp : float
        amplitude of the gaussian
    mu : float
        center of the gaussian
    std : float
        standard deviation of the gaussian

    Returns
    -------
    list
        list with the values of the gaussian at x
    """

    return amp * np.exp(-((x - mu) ** 2) / (2 * std**2))


def n_gaussians(x, *args):
    """
    Generates a sum of n gaussians, if you know n peaks are in the spectrum.
    Uses the gaussian function.

    Parameters
    ----------
    x : list or np.array
        The channel values where the gaussian is made, must cover all peaks.
    *args : list or np.array
        The parameters for the gaussians, must be in the order:
        [amp1, peak1, std1, amp2, peak2, std2, ...]

    Returns
    -------
    List or np.array
        The n gaussian function with the given parameters over the given x values.
    """
    n = int(len(args) / 3)
    y = np.zeros(len(x))
    for i in range(n):
        y += gaussian(x, args[3 * i], args[3 * i + 1], args[3 * i + 2])
    return y


# now we need a functions which fits peak guesses to gaussian curves
def fit_n_peaks_to_gaussian(
    x,
    y,
    guessed_peaks,
    guessed_std=1,
    guessed_amp=1,
):
    """
    Fits n peaks to n gaussians, given an array and the guessed centers.
    Returns the fitted param [[amp, peak, std], covar].

    Uses curve_fit from scipy.optimize. This is a non-linear least squares,
    which means that it tries to find the parameters that minimize the sum of the squares of the residuals.
    The residuals are the difference between the data and the model.
    The model is the sum of the gaussians, and the parameters are the amplitudes, means and standard deviations of the gaussians.

    Parameters
    ----------
    x : list
        x values to fit the gaussians to
    raw_y : np.array
        The raw y data of the spectrum with n peaks
    guessed_peaks : list or np.array of int
        Inital guesses of the n peaks
    guessed_amp : int, optional
        Initial guess of the amplitude, and not that important, by default 1
    guess_wid : int, optional
        Initial guess of the width, and not that important, by default 1
    Returns
    -------
    np.array
        The fitted param [[amp, peak, std], covar].
    """
    # the std and amp are usually fine as 1 in the initial guess
    if guessed_std == 1:
        guessed_std = np.ones(len(guessed_peaks))
    if guessed_amp == 1:
        guessed_amp = np.ones(len(guessed_peaks))

    # making the list of the initial guesses
    for i in range(len(guessed_peaks)):
        if i == 0:
            init_vals = [guessed_amp[i], guessed_peaks[i], guessed_std[i]]
        else:
            init_vals += [guessed_amp[i], guessed_peaks[i], guessed_std[i]]
    # fitting the data to the gaussians
    fit_vals, covar = curve_fit(n_gaussians, x, y, p0=init_vals)
    return [fit_vals, covar]


def area_under_peak(peak_channel, peak_sigma, peak_height):
    """Calculates the area under the peak, using the peak sigma and height.
    The area is calculated using the cumulative distribution function of a normal distribution,
    calculating the area between peak-3*sigma and peak+3*sigma.
    """
    integrate_area = 3 * peak_sigma
    area = norm.cdf(
        peak_channel + integrate_area, loc=peak_channel, scale=peak_sigma
    ) - norm.cdf(peak_channel - integrate_area, peak_channel, peak_sigma)
    area *= peak_height
    return area
