# helper file for reading the data
import numpy as np


def read_data(
    filepath, start_string, stop_string, delimiter, line_endings, print_info=True
):
    """
    Reads the data from the file and returns the data as a numpy array.
    See the comments iside the function for more information.
    Will normally print the information about the data.

    Remember to put the correct values for the parameters.
    """
    # open the file in read mode, and closes f when the block is done
    with open(filepath, "r") as f:
        # read the file line by line
        lines = f.readlines()

        # remove the newline character from each line
        lines = [line.strip(line_endings) for line in lines]

        # find the start and stop index
        start_index = lines.index(start_string)
        stop_index = lines.index(stop_string)

        # the data contains stop_index - start_index - 1 lines of data
        number_of_data_points = stop_index - start_index - 1

        # make an empty list to store the data
        data = []

        # loop over the lines of data and split them into a list with floats
        for line in lines[start_index + 1 : stop_index]:
            data.append([float(x) for x in line.split(delimiter)])

        # convert the data to two numpy arrays
        raw_channels = np.array([x[0] for x in data])
        counts = np.array([x[1] for x in data])

    # optional print of the information about the data
    if print_info:
        print(f"Read {number_of_data_points} data points from {filepath}")
        print(f"First entry: {data[0]}\nLast entry: {data[-1]}")

    # returns the raw_channels and counts as numpy arrays
    return [raw_channels, counts]
