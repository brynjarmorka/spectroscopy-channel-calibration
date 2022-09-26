# spectroscopy-channel-calibration

Calibrating raw data from EDS spectroscopy in jupyter notebooks

### Challenges I've had

- What is the actual zero / start of the data?
  - What to do with the zero-peak which some instruments have?
  - Some (or all?) spectra starts measuring before 0. How do I set the 0 right?
- Some datasets (eg. .emsa of GaAs_30keV) starts with negative keV values.
- Not possible to recognize all peaks, since some are low.
  - Without bg removal one peak is usually fitted in the middle as the bg with a very high std
- For some reason it did not work to use the raw x values from .emsa when fitting, while using channels as int worked.
  - Also fitting is slower / worse with non-normalized values.
    - Might be because it is easier to guess correct a, peak, and std with normalized values

### Example data files

- Ex1_EDS_GaAs_30kV.emsa
  - Aquired at the SEM Apreo at NTNU NanoLab, 6. September 2022
- Ex2_NiO_on_Mo_not_calibrated.msa
  - Aquired by Ton?
- Ex3_Cu.mca
  - Aquired by Ton?
