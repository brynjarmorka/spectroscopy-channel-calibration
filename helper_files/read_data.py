# helper file for reading the data
# contains the functions read_lines, read_xy_data and read_only_y_data

import numpy as np


def read_lines(filepath, start_string, stop_string, line_endings, print_info=True):
    """
    Reads the data from the file and returns the data as a numpy array.
    See the comments iside the function for more information.
    Will normally print the information about the data.

    Remember to put the correct values for the parameters.

    Parameters
    ----------
    filepath : string / path
        path to the file
    start_string : string
        the line above the data starts
    stop_string : string
        the line after the data ends
    line_endings : string
        line endings in the file, often '\n' or ', \n'
    print_info : bool, optional
        printing a summary at the end, by default True

    Returns
    -------
    list of strings
        list of the lines in the file
    """
    # open the file in read mode, and closes f when the block is done
    # encoding='cp1252' is for the special characters in the .mca file
    with open(filepath, "r", encoding='cp1252') as f:
        # read the file line by line
        lines = f.readlines()

        if print_info:
            print(f"Reading {filepath}")
            print(f"The first line looks like this: {repr(lines[0])}")

        # remove the line endings, specified by line_endings
        lines = [line.rstrip(line_endings) for line in lines]

        # find the start and stop index
        try:
            start_index = lines.index(start_string)
            stop_index = lines.index(stop_string)
        # if the start or stop string is not found
        except ValueError:
            print(
                f"Could not find {start_string} or {stop_string} in the file, returning None."
            )
            return None

        if print_info:
            print(f"Reading from line {start_index} to {stop_index}.")

        start_index = lines.index(start_string)
        stop_index = lines.index(stop_string)

        # the data contains stop_index - start_index - 1 lines of data
        # number_of_data_points = stop_index - start_index - 1

    # return the data as a list of strings, to be used by one of the functions below
    return lines[start_index + 1 : stop_index]


def read_xy_data(
    filepath, start_string, stop_string, delimiter, line_endings, print_info=True
):
    """
    Reading a file with two columns of data, and returns the data as a 2d numpy array.
    See the comments iside the function for more information.

    NB! The firste entries might not be the actual 0, which we have to solve later.

    Parameters
    ----------
    filepath : string / path
        path to the file
    start_string : string
        the line above the data starts
    stop_string : string
        the line after the data ends
    delimiter : string
        the delimiter between the x and y data
    line_endings : string
        line endings in the file, often '\n' or ', \n'
    print_info : bool, optional
        printing a summary at the end, by default True

    Returns
    -------
    np.array of two np.arrays
        array with the channels and counts
    """

    # read the lines only containing the data
    lines = read_lines(filepath, start_string, stop_string, line_endings, print_info)

    # make an empty list to store the data
    data = []

    # loop over the lines of data and split them into a list with floats
    for line in lines:
        data.append([float(x) for x in line.split(delimiter)])

    # convert the data to two numpy arrays
    raw_channels = np.array([x[0] for x in data])
    counts = np.array([x[1] for x in data])

    # optional print of the information about the data
    if print_info:
        print(
            f"{len(lines)} data points, first entry = {data[0]}, last entry = {data[-1]}\n"
        )

    # returns the raw_channels and counts as numpy arrays
    return np.array([raw_channels, counts])


def read_only_y_data(
    filepath, start_string, stop_string, line_endings=None, print_info=True
):
    """
    Reading a file with only one column of data, and returns the data as a 2d numpy array.
    Channels are just the index of the data point, since there are no channels in the file.
    See the comments iside the function for more information.

    NB! The firste entries might not be the actual 0, which we have to solve later.

    Parameters
    ----------
    filepath : string / path
        path to the file
    start_string : string
        the line above the data starts
    stop_string : string
        the line after the data ends
    line_endings : string
        line endings in the file, often '\n' or ', \n'
    print_info : bool, optional
        printing a summary at the end, by default True

    Returns
    -------
    np.array of two np.arrays
        array with the channels and counts
    """

    # read the lines only containing the data
    lines = read_lines(filepath, start_string, stop_string, line_endings, print_info)

    # make an empty list to store the data
    counts = []

    # loop over the lines of y data and turn the strings into floats
    try:
        for line in lines:
            counts.append(float(line))
    except ValueError:
        print("Could not convert the data to floats, returning None.")
        return None

    # making the channels, just the index of the data point
    channels = np.arange(len(counts))

    # put [counts, channels]
    data = np.array([channels, counts])

    # optional print of the information about the data
    if print_info:
        print(f"{len(lines)} data points, first entry = {data.T[0]}, last entry = {data.T[-1]}\n")

    # returns the data, which is only raw counts and channels
    return data
