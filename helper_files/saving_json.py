# Saving and loading the spectrum-dictionary to a file

import json
import numpy as np


def save_spectrum_to_json(s):
    """
    Save a spectrum dict to a json file.
    ndarrays are converted to lists.
    Saves the file to the folder Lab3_data_calibrated, adding the suffix _calibrated to the filename.

    Parameters
    ----------
    s : dict
        spectrum dictionary
    """

    # first make a dictionary where the ndarrays are converted to lists
    s_list = {}
    for key in s.keys():
        if type(s[key]) == np.ndarray:
            s_list[key] = s[key].tolist()
        else:
            s_list[key] = s[key]

    filename = f"Lab3_data_calibrated/{s['filepath'].split('/')[-1].split('.')[0]}_calibrated.json"
    print(f"Saved the spectrum to: {filename}")

    # then save the dictionary to a file
    with open(filename, "w") as f:
        f.write(json.dumps(s_list, indent=4))


def read_saved_spectrum_from_json(filename):
    """
    Reading a spectrum dictionary from a json file.

    Parameters
    ----------
    filename : string
        which file to read

    Returns
    -------
    dict
        spectrum dictionary
    """

    # keys that should be ndarrays
    ndarray_keys = [
        "channel",
        "intensity",
        "counts",
        "kev_calibrated",
        "peaks_channel",
        "fit_params",
        "fit_cov",
        "intensity_fit",
    ]
    with open(filename, "r") as f:
        s = json.load(f)

    # convert the lists back to ndarrays
    for key in s.keys():
        if key in ndarray_keys:
            s[key] = np.array(s[key])

    print(f"Read the spectrum from: {filename}")
    return s
