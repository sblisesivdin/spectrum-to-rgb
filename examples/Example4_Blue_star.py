import numpy as np
import pandas as pd

"""
Example 4 - Blue star emission

MIT License

Copyright (c) 2025 by Beyza Lisesivdin and Sefer Bora Lisesivdin

Full license information can be found in LICENSE.md

Usage:
$ python Example4_Blue_star.py

"""

def planckian_blue_star_spectrum(
    wavelength_min=380,
    wavelength_max=780,
    temperature=15000,  # Typical color temperature for a hot, blue star
    noise_level=0.01,
    filename="Blue_Star_Spectrum.csv"
):

    # Physical constants
    h = 6.62607015e-34  # Planck's constant (J*s)
    c = 3.0e8           # Speed of light (m/s)
    kB = 1.380649e-23   # Boltzmann constant (J/K)
    
    # Create an array of wavelengths in meters
    wavelengths_nm = np.arange(wavelength_min, wavelength_max + 1, 1)
    wavelengths_m = wavelengths_nm * 1e-9  # convert nm to m
    
    # Compute Planck's law (arbitrary units)
    # B(λ, T) = (2hc^2 / λ^5) * 1 / [exp(hc/(λkBT)) - 1]
    radiance = (2 * h * c**2) / (wavelengths_m**5) / (
        np.exp((h * c) / (wavelengths_m * kB * temperature)) - 1
    )
    
    # Normalize peak to 1
    radiance /= np.max(radiance)
    
    # Add small random noise for realism
    noise = noise_level * np.random.rand(len(radiance))
    radiance += noise
    
    # Re-normalize to ensure max remains 1
    radiance /= np.max(radiance)
    
    # Create a DataFrame
    df = pd.DataFrame({
        "Wavelength (nm)": wavelengths_nm,
        "Intensity": radiance
    })
    
    # Save to CSV
    df.to_csv(filename, index=False)
    
    print(f"Planckian 'blue star' spectrum saved to '{filename}'")

if __name__ == "__main__":
    planckian_blue_star_spectrum()
