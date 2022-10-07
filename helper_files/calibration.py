# helper file for calibration


def calibrate_channel_width_two_peaks(peaks_channel, peaks_keV):
    """
    Calibration of the channel width and offset using two peaks.
    Remember that the two first peaks in s['peaks_channel'] are the peaks used.

    Parameters
    ----------
    peaks_channel : list
        s['peaks_channel']
    peaks_keV : list
        s['peaks_keV']

    Returns
    -------
    tuple
        dispersion, offset
    """

    # figure out the distances between the peaks
    channel_distance = peaks_channel[1] - peaks_channel[0]
    kev_distance = peaks_keV[1] - peaks_keV[0]

    # dispersion = (p1_keV - p0_keV) / (p1_channel - p0_channel)
    dispersion = kev_distance / channel_distance  # kev_per_channel

    # finding the 0 offset
    # dispersion = (p0_kev - 0.0 keV) / (p0_channel - offset)
    # offset = p0_channel - p0_kev / dispersion
    offset = peaks_channel[0] - peaks_keV[0] / dispersion  # calibrated_zero_channel

    print(
        f"The calibration factor is: {dispersion:.07f} keV/channel, with {offset:.03f} channels zero offset"
    )

    return (dispersion, offset)


def channel_to_keV(spectrum=None, value=None, array=None, use_offset=True):
    """
    Convert either single value or array of values from channel to keV.
    ( Value - offset ) * dispersion

    Parameters
    ----------
    spectrum : dict
        spectrum dictionary
    value : int
        single value to convert
    array : list
        array of values to convert

    Returns
    -------
    int or list
        converted value or array
    """

    # sometimes the offset is not used, eg when calculating the FWHM from std in channels
    if use_offset:
        offset = spectrum["offset"]
    else:
        offset = 0
    
    if spectrum is None:
        raise ValueError("No spectrum dictionary provided to chennel_to_keV()")

    if value is not None:
        return (value - offset) * spectrum["dispersion"]
    if array is not None:
        return [(x - offset) * spectrum["dispersion"] for x in array]

    else:
        raise ValueError("No value or array provided to chennel_to_keV()")
