# spectroscopy-channel-calibration

Made by Brynjar Morka Mæhlum for the subject "TFY4255 Materialfysikk", as a part of Brynjars "TFY4520 Nanoteknologi, fordypningsprosjekt".

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
│   environment.yml
│   LICENSE
│   README.md
│
├───helper_files
│   │   calibration.py
│   │   gaussian_fitting.py
│   │   plotting.py
│   │   read_data.py
│   │   saving_json.py
│   │   spectrum_dict.py
│   │   __init__.py
│
├───Lab3_data
│       SEM_known_Cu.msa
│       SEM_known_NiO_on_Mo.msa
│       SEM_unknown.msa
│       TEM_known_NiO_on_Mo_A.emsa
│       TEM_known_NiO_on_Mo_B.emsa
│       TEM_unknown.msa
│       XRF_known_Cu.mca
│       XRF_known_Pb.mca
│       XRF_no_sample.mca
│       XRF_unknown.mca
│       XRF_unknown_2nd.mca
│
├───Lab3_data_calibrated
│       SEM_known_Cu_calibrated.json  # example of a plot
│
└───plots
        SEM_known_Cu_calibrated.html  # example of a plot
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

## Info on the data files

- SEM_known_Cu.msa

  - Bulk Cu
  - Collected on Hitatchi TM4000 at 15 kV

- SEM_unknown.msa

  - 0.3 mm thick unknown
  - Hitatchi TM4000 at 15 kV

- TEM_known_NiO_on_Mo.emsa

  - NiO calibration specimen [6]
  - Collected at Jeol 2100 at 200 kV using a Oxford Instrument 80mm2 SDD

- TEM_unknown.msa

  - Unknown material crushed and deposited on a 300 mesh Cu TEM grid with a holey 20 nm C-support
  - Data collected at Jeol 2100 at 200 kV using a Oxford Instrument 80mm2 SDD

- XRF_known_Cu.msa

  - Bulk Cu
  - MoK X-ray source, AmpTek® energy dispersive detector

- XRF_unknown.msa

  - unknown material, 0.3 mm thick
  - MoK X-ray source AmpTek® energy dispersive detector

- ***

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
