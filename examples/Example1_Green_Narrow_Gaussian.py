import numpy as np
import pandas as pd

"""
Example 2 - Green Narrow Gaussian Peak

MIT License

Copyright (c) 2025 by Beyza Lisesivdin and Sefer Bora Lisesivdin

Full license information can be found in LICENSE.md

Usage:
$ python Example1_Green_Narrow_Gaussian.py

"""

# Generating synthetic data for Example 1: Narrow Gaussian peak at 550 nm
wavelengths_example1 = np.arange(380, 781, 1)  # Wavelengths from 380 nm to 780 nm
intensity_example1 = np.exp(-0.5 * ((wavelengths_example1 - 550) / 10)**2)  # Gaussian centered at 550 nm

# Saving Example 1 to a CSV
example1_data = pd.DataFrame({'Wavelength (nm)': wavelengths_example1, 'Intensity': intensity_example1})
example1_file_path = "Narrow_Green_Gaussian_Spectrum.csv"
example1_data.to_csv(example1_file_path, index=False)

