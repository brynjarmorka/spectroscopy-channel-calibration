# spectroscopy-channel-calibration

Made by Brynjar Morka Mæhlum for the subject TFY4255, as a part of Brynjars "TFY4520 Nanoteknologi, fordypningsprosjekt".

---

Use the Binder link below to open this repository in an online and interactive way:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/brynjarmorka/spectroscopy-channel-calibration/HEAD)

---

## Goal of this notebook:

**Use a spectrum with at least two known peaks to calibrate the channel width of a detector, and then use the calibration to plot an unknown spectrum.**

To calibrate a spectrum we calculate:

- dispersion [keV / channel], which is the width of each channel
- offset [channels], which is the distance from first data entry to keV=0

When we have calibrated a spectrum, we could also find:

- energy resolution
- quantities of each element by area under the peak
  - bear in mind: this is dependent on signal-to-background, efficiency of the detector, ...
- ... ?

---

## What we will do:

1. Read in the data of a known spectrum
2. Fit the data to a gaussian
3. Calibrate the x-axis
4. Plot the calibrated data
5. Use the calibrated x-axis on an unknown spectrum from the same source

---

## Organisation of the repository

This is the file tree:

```cmd
│   .gitignore
│   channel_calibration.ipynb
│   Ex1_EDS_GaAs_30kV.emsa
│   Ex2_NiO_on_Mo_not_calibrated.msa
│   Ex3_Cu.mca
│   LICENSE
│   README.md
│   requirements.yml
│
└───helper_files
    │   calibration.py
    │   gaussian_fitting.py
    │   plotting.py
    │   read_data.py
    │   spectrum_dict.py
    │   __init__.py
```

The main notebook is called "channel_calibration.ipynb", which contains a step-by-step calibration of a known spectrum, and then using that on an unknown spectrum.

To make the notebooks shorter and more understandable, I've made the folder "helper_files" with functions that you will use. The helper functions are documented with NumPy docstrings, which you can read by running a cell with the function name followed by a questionmark:

```python
function_name?
```

```
>>> prints the docstring of function_name
```

---

## Example data files

- Ex1_EDS_GaAs_30kV.emsa
  - Aquired at the SEM Apreo at NTNU NanoLab, 6. September 2022
- Ex2_NiO_on_Mo_not_calibrated.msa
  - Aquired by Ton?
- Ex3_Cu.mca
  - Aquired by Ton?
- Info on the other files will come soon

---

## Challenges I've had

- What is the actual zero / start of the data? (solved)
  - What to do with the zero-peak which some instruments have?
  - Some (or all?) spectra starts measuring before 0. How do I set the 0 right?
- Some datasets (eg. .emsa of GaAs_30keV) starts with negative keV values. (solved)
- Not possible to recognize all peaks, since some are low.
  - Without bg removal one peak is usually fitted in the middle as the bg with a very high std
- For some reason it did not work to use the raw x values from .emsa when fitting, while using channels as int worked.
  - Also fitting is slower / worse with non-normalized values.
    - Might be because it is easier to guess correct amp, mu, and std with normalized values
  - workaround: fit with channels and intensity normalized to 1
