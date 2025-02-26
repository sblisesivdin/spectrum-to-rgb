import numpy as np
import pandas as pd

"""
Example 3 - Incandecent Light source

MIT License

Copyright (c) 2025 by Beyza Lisesivdin and Sefer Bora Lisesivdin

Full license information can be found in LICENSE.md

Usage:
$ python Example3_Incandecent.py

"""
# Generating synthetic spectral profile for an incandescent light source
# The profile follows a Planckian distribution with a more complex curve to simulate realistic incandescent behavior.

def planckian_distribution(wavelengths, temperature=2700):
    """Generate a Planckian distribution for a given temperature."""
    h = 6.626e-34  # Planck's constant, J*s
    c = 3.0e8      # Speed of light, m/s
    k = 1.38e-23   # Boltzmann's constant, J/K
    wavelengths_m = wavelengths * 1e-9  # Convert nm to meters
    return (2 * h * c**2) / (wavelengths_m**5) / (np.exp(h * c / (wavelengths_m * k * temperature)) - 1)

# Wavelength range (380 nm to 780 nm)
wavelengths_incandescent = np.arange(380, 781, 1)

# Simulate incandescent light with some noise and smoothing for more complexity
intensity_incandescent = planckian_distribution(wavelengths_incandescent, temperature=2700)
intensity_incandescent = intensity_incandescent / np.max(intensity_incandescent)  # Normalize to [0, 1]

# Adding minor peaks and smoothing
noise = 0.02 * np.random.rand(len(intensity_incandescent))  # Random noise
extra_peaks = (
    0.1 * np.exp(-0.5 * ((wavelengths_incandescent - 480) / 15)**2) +
    0.05 * np.exp(-0.5 * ((wavelengths_incandescent - 620) / 20)**2)
)
intensity_incandescent = intensity_incandescent + noise + extra_peaks
intensity_incandescent = intensity_incandescent / np.max(intensity_incandescent)  # Renormalize to [0, 1]

# Saving the incandescent light spectrum to a CSV
incandescent_data = pd.DataFrame({'Wavelength (nm)': wavelengths_incandescent, 'Intensity': intensity_incandescent})
incandescent_file_path = "Incandescent_Light_Spectrum.csv"
incandescent_data.to_csv(incandescent_file_path, index=False)

