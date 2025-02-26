import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

"""
spectrum-to-rgb.py
------------------
Python-based tool for converting spectral power distributions (SPDs) to RGB colors using the CIE 1931 color space.

MIT License

Copyright (c) 2025 by Beyza Lisesivdin and Sefer Bora Lisesivdin

Full license information can be found in LICENSE.md

Usage:
$ ./spectrum-to-rgb.py <filename>

"""

def load_csv(file_path):
    """
    Load a CSV file with automatic delimiter detection.
    Returns a numpy array of the data.
    """
    with open(file_path, 'r') as file:
        # Detect delimiter
        sample = file.read(1024)
        file.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",\t ")
        delimiter = dialect.delimiter
        print(f"Detected delimiter in {file_path}: '{delimiter}'")

    # Load data
    return np.genfromtxt(file_path, delimiter=delimiter)

def load_spectrum(csv_file):
    """
    Load the spectrum data from a CSV file.
    The first column should be wavelength in nm,
    and the second column should be intensity.
    """
    data = load_csv(csv_file)
    if data.ndim != 2 or data.shape[1] != 2:
        raise ValueError(f"Invalid spectrum file format: {csv_file}. Expected two columns.")
    return data[:, 0], data[:, 1]

def xyz_to_rgb(x, y, z):
    """
    Convert CIE XYZ color space to sRGB in the range 0-255.
    """
    # Transformation matrix for sRGB
    mat = np.array([
        [3.2406, -1.5372, -0.4986],
        [-0.9689,  1.8758,  0.0415],
        [0.0557, -0.2040,  1.0570]
    ])

    # Convert XYZ to linear RGB
    rgb = np.dot(mat, [x, y, z])

    # Debug: Linear RGB before clamping
    print(f"Linear RGB before clamping: {rgb}")

    # Clip negative values
    rgb = np.clip(rgb, 0, None)

    # Normalize to the brightest channel
    max_val = np.max(rgb)
    if max_val > 0:  # Avoid division by zero
        rgb /= max_val

    # Debug: Normalized linear RGB
    print(f"Normalized linear RGB: {rgb}")

    # Apply gamma correction
    def gamma_correct(value):
        if value <= 0.0031308:
            return 12.92 * value
        else:
            return 1.055 * (value ** (1 / 2.4)) - 0.055

    rgb = [gamma_correct(c) for c in rgb]

    # Debug: Gamma-corrected RGB
    print(f"Gamma-corrected RGB: {rgb}")

    # Scale to 0-255
    rgb_255 = [int(round(c * 255)) for c in rgb]

    # Debug: Final RGB
    print(f"Final RGB (0-255): {rgb_255}")

    return rgb_255



def spectrum_to_xyz(wavelengths, intensities, cie_file):
    """
    Convert a spectrum to CIE 1931 XYZ values.
    """
    cie_data = load_csv(cie_file)
    cie_wavelengths = cie_data[:, 0]
    cie_x = cie_data[:, 1]
    cie_y = cie_data[:, 2]
    cie_z = cie_data[:, 3]

    # Interpolate color matching functions to the input wavelengths
    x_interp = interp1d(cie_wavelengths, cie_x, bounds_error=False, fill_value=0)
    y_interp = interp1d(cie_wavelengths, cie_y, bounds_error=False, fill_value=0)
    z_interp = interp1d(cie_wavelengths, cie_z, bounds_error=False, fill_value=0)

    # Debug: Print interpolated values
    print(f"Interpolated x̄: {x_interp(wavelengths)}")
    print(f"Interpolated ȳ: {y_interp(wavelengths)}")
    print(f"Interpolated z̄: {z_interp(wavelengths)}")

    x = np.sum(intensities * x_interp(wavelengths))
    y = np.sum(intensities * y_interp(wavelengths))
    z = np.sum(intensities * z_interp(wavelengths))

    # Debug: Print XYZ values
    print(f"Computed XYZ: X={x}, Y={y}, Z={z}")
    return x, y, z

def plot_chromaticity_diagram(xy_point, cie_file):
    """
    Plot the CIE 1931 xy chromaticity diagram and mark the given xy point.
    """
    cie_data = load_csv(cie_file)
    cie_x = cie_data[:, 1]
    cie_y = cie_data[:, 2]
    cie_z = cie_data[:, 3]

    # Normalize to get xy values
    total = cie_x + cie_y + cie_z
    chromaticity_x = cie_x / total
    chromaticity_y = cie_y / total

    plt.figure(figsize=(8, 8))
    plt.plot(chromaticity_x, chromaticity_y, label='CIE 1931 Boundary', color='black')
    plt.scatter(*xy_point, color='red', label='Input Spectrum', zorder=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('CIE 1931 xy Chromaticity Diagram')
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    import sys

    # Expect exactly one command-line argument (the spectrum CSV)
    if len(sys.argv) != 2:
        print("Usage: python spectrum-to-rgb.py <spectrum_file.csv>")
        sys.exit(1)

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Paths for CIE file and input spectrum file
    cie_file = os.path.join(script_dir, 'CIE_xyz_1931_2deg.csv')
    #csv_file = os.path.join(script_dir, input("Enter the name of the spectrum CSV file (in the same folder): "))
    csv_file = sys.argv[1]  # The user-specified spectrum filename
    if not os.path.exists(csv_file):
        print(f"Error: file '{csv_file}' not found.")
        sys.exit(1)
    
    try:
        # Load spectrum data
        wavelengths, intensities = load_spectrum(csv_file)
        print("Spectrum Data Loaded:", wavelengths, intensities)

        if wavelengths.size == 0 or intensities.size == 0:
            raise ValueError("Spectrum file is empty or improperly formatted.")

        # Normalize intensities
        max_intensity = np.max(intensities)
        if max_intensity > 0:
            intensities = intensities / max_intensity
        else:
            raise ValueError("Spectrum intensities are all zero.")

        intensities = intensities / np.max(intensities)
        # Convert spectrum to XYZ
        x, y, z = spectrum_to_xyz(wavelengths, intensities, cie_file)

        # Normalize to xy chromaticity
        total = x + y + z
        if total == 0:
            raise ValueError("Spectrum produces zero total intensity in XYZ space.")

        chromaticity_x = x / total
        chromaticity_y = y / total

        # Convert XYZ to RGB
        rgb = xyz_to_rgb(x, y, z)

        print(f"Chromaticity (x, y): ({chromaticity_x:.4f}, {chromaticity_y:.4f})")
        print(f"RGB Value (0-255): {rgb}")

        # Plot the CIE xy chromaticity diagram
        plot_chromaticity_diagram((chromaticity_x, chromaticity_y), cie_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
