# helperfile for making the spectrum dictionary

import numpy as np

from helper_files.read_data import read_xy_data, read_only_y_data


# the '*' argument is that all arguments (after) must be named (kwarg) and not just positional arguments
def init_known_spectrum(
    *,
    name,
    filepath,
    start_str,
    stop_str,
    line_endings,
    delimiter=None,
    peaks_keV=None,
    peaks_names=None,
    peaks_channel=None,
):
    """
    initializing the spectrum dictionary. 
    Must have a name, filepath, start and stop string, and line endings to read the data.
    Can have peaks_keV, peaks_names, peaks_channel.

    Parameters
    ----------
    name : string
        Name of the spectrum, used in plots
    filepath : string
        relative path to the data file
    start_str : string
        string that marks the start of the data
    stop_str : string
        string that marks the end of the data
    line_endings : string
        string that marks the end of each line
    delimiter : string, optional
        string that splits the data, only to be used on eg .emsa files with x&y, by default None
    peaks_keV : list of floats, optional
        theoretical values of peaks used in calibration, by default None
    peaks_names : list of string, optional
        names of the peaks, by default None
    peaks_channel : list of int, optional
        channel values of the peaks, first a guess then corrected after fitting, by default None

    Returns
    -------
    dictionary
        spectrum dictionary
    """

    # if the file is with x and y, delimiter must be specified
    if delimiter:
        data_raw = read_xy_data(filepath, start_str, stop_str, delimiter, line_endings)
        keV_uncalibrated = data_raw[0]  # unused. Not needed, but could be for xy-data in the future
    else:
        data_raw = read_only_y_data(filepath, start_str, stop_str, line_endings)
        keV_uncalibrated = None
    if data_raw is None:
        print(
            "ERROR: could not read the data properly, please check the parameters for reading the file"
        )
        return None

    # this is the data set we will be working with.
    #       - y: counts normalized to the maximum peak
    #       - x: channels
    intensity = data_raw[1] / data_raw[1].max()
    channels = np.arange(0, len(intensity), 1)

    # making the dictionary we will work with
    spectrum = {
        "name": name,
        "filepath": filepath,
        "channel": channels,
        "intensity": intensity,
        "counts": data_raw[1],
        "peaks_keV": peaks_keV,
        "peaks_names": peaks_names,
        "peaks_channel": peaks_channel,
        "dispersion": None,
        "offset": None,
        "kev_calibrated": None,
        "fit_params": None,
        "fit_cov": None,
        "intensity_fit": None,
        "start_str": start_str,
        "stop_str": stop_str,
        "line_endings": line_endings,
        "delimiter": delimiter
    }
    return spectrum


def init_unknown_spectrum_with_known(*, known_spectrum, name, filepath, start_str=None, stop_str=None, line_endings=None, delimiter=None, peaks_keV=None, peaks_names=None, peaks_channel=None):
    """
    initializing a unknown spectrum dictionary, from a calibrated spectrum.
    assuming the same dispersion and offset as the known spectrum
    must be the same amout of channels, else the calibration will obviously be wrong

    Parameters
    ----------
    known_spectrum : dictionary
        a calibrated spectrum dictionary, since we will use the dispersion and offset
    name : string
        Name of the spectrum, used in plots
    filepath : string
        relative path to the data file
    start_str : string
        string that marks the start of the data
    stop_str : string
        string that marks the end of the data
    line_endings : string
        string that marks the end of each line
    delimiter : string, optional
        string that splits the data, only to be used on eg .emsa files with x&y, by default None
    peaks_keV : list of floats, optional
        theoretical values of peaks used in calibration, by default None
    peaks_names : list of string, optional
        names of the peaks, by default None
    peaks_channel : list of int, optional
        channel values of the peaks, first a guess then corrected after fitting, by default None

    Returns
    -------
    dictionary
        spectrum dictionary, with the same dispersion and offset as the known spectrum
    """

    # stop if the known spectrum are not calibrated
    if known_spectrum['dispersion'] is not None and known_spectrum['offset'] is not None and known_spectrum['kev_calibrated']is not None:
        print(f"Calibrating '{name}' with '{known_spectrum['name']}' using:")
        print(f"\tDispersion = {known_spectrum['dispersion']}")
        print(f"\tOffset = {known_spectrum['offset']}")
        print(f"\tAnd the calibrated keV x-axis from {known_spectrum['name']}")
    # this else runs if dispersion, offset or kev_calibrated are noe set in the known_spectrum
    else:
        print(f"ERROR: the known_spectrum {known_spectrum['name']} lacks either dispersion, offset or kev_calibrated!")
        print(f"Dispersion={known_spectrum['dispersion']}, offset={known_spectrum['offset']}, kev_calibrated: {known_spectrum['kev_calibrated']}")
        print('Returned None')
        return None

    # assuming the filetype is the same as the known spectrum, we just use the same values
    if start_str is None:
        start_str = known_spectrum["start_str"]
    if stop_str is None:
        stop_str = known_spectrum["stop_str"]
    if line_endings is None:
        line_endings = known_spectrum["line_endings"]
    if delimiter is None:
        delimiter = known_spectrum["delimiter"]
    
    # if the file is with x and y, delimiter must be specified
    if delimiter:
        data_raw = read_xy_data(filepath, start_str, stop_str, delimiter, line_endings)
        keV_uncalibrated = data_raw[0]  # unused
    else:
        data_raw = read_only_y_data(filepath, start_str, stop_str, line_endings)
        keV_uncalibrated = None
    if data_raw is None:
        print(
            "ERROR: could not read the data properly, please check the parameters for reading the file. Returning None"
        )
        return None
    
    # this is the data set we will be working with.
    #       - y: counts normalized to the maximum peak
    #       - x: channels
    intensity = data_raw[1] / data_raw[1].max()
    channels = np.arange(0, len(intensity), 1)

    # checking if the calibrated spectrum has the same length as the new one
    if len(channels) != len(known_spectrum['channel']):
        print(f"ERROR! The calibrated spectrum has {len(known_spectrum['channel'])} data points, while the new one has {len(channels)} data points")
        print("Returned the new dict as None")
        return None
    
    # if we get this far, everything should be ok
    # thus we make the new dictionary
    spectrum = {
        "name": name,
        "filepath": filepath,
        "channel": channels,
        "intensity": intensity,
        "counts": data_raw[1],
        "peaks_keV": peaks_keV,
        "peaks_names": peaks_names,
        "peaks_channel": peaks_channel,
        "dispersion": known_spectrum["dispersion"],
        "offset": known_spectrum["offset"],
        "kev_calibrated": known_spectrum["kev_calibrated"],
        "fit_params": None,
        "fit_cov": None,
        "intensity_fit": None,
    }

    print(f"Success! {spectrum['filepath']} was read into a dictionary\n")
    return spectrum
    