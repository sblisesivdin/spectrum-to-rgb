import numpy as np
import pandas as pd

"""
Example 2 - Two Narrow Gaussian Peaks

MIT License

Copyright (c) 2025 by Beyza Lisesivdin and Sefer Bora Lisesivdin

Full license information can be found in LICENSE.md

Usage:
$ python Example2_Two_Narrow_Gaussian.py

"""

# Generating synthetic spectrum with two narrow Gaussian peaks
wavelengths_gaussian = np.arange(380, 781, 1)  # Wavelengths from 380 nm to 780 nm

# Two narrow Gaussian peaks at 520 nm and 600 nm
intensity_gaussian = (
    np.exp(-0.5 * ((wavelengths_gaussian - 520) / 10)**2) +  # Peak at 520 nm
    np.exp(-0.5 * ((wavelengths_gaussian - 600) / 10)**2)    # Peak at 600 nm
)

# Normalize intensity to [0, 1]
intensity_gaussian = intensity_gaussian / np.max(intensity_gaussian)

# Saving the spectrum to a CSV
gaussian_data = pd.DataFrame({'Wavelength (nm)': wavelengths_gaussian, 'Intensity': intensity_gaussian})
gaussian_file_path = "Two_Narrow_Gaussian_Spectrum.csv"
gaussian_data.to_csv(gaussian_file_path, index=False)

gaussian_file_path
