# spectrum-to-color

`spectrum-to-color` is a Python-based tool for converting spectral power distributions (SPDs) to RGB colors using the CIE 1931 color space. This repository accompanies the article titled _A Python-Based Approach for Converting Spectral Power Distributions to RGB Colors Using the CIE 1931 Color Space_ (in press).

The script leverages widely available libraries (`numpy`, `pandas`, `matplotlib`, and `scipy`) to:

1. Read and parse spectral data (CSV files)
2. Interpolate the CIE 1931 color-matching functions
3. Compute XYZ tristimulus values
4. Convert XYZ values to sRGB (0–255) via gamma correction
5. Optionally visualize the result on a CIE xy chromaticity diagram

---

## Features

- **Flexible Input**: Handles CSV files with comma, tab, or space delimiters.
- **Robust Interpolation**: Aligns custom wavelength ranges to standard CIE 1931 color-matching functions.
- **Automatic Normalization**: Ensures results stay within valid sRGB ranges.
- **Visualization**: Includes a sample script to plot CIE xy chromaticity diagrams.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/spectrum-to-color.git
   ```
   
or Download ZIP and extract.

2. Install dependencies:
	```bash
     pip install numpy pandas matplotlib scipy
	```

## Usage
Place your spectral data in a CSV file with two columns:

Column 1: Wavelengths (in nanometers)
Column 2: Intensities (in arbitrary units)

Run the main script:

```bash
   python spectrum_to_rgb.py input spectrum.csv
```

The script outputs the computed RGB value and optionally displays a chromaticity diagram.

## Project Structure
- **spectrum_to_rgb.py**: Main Python script.
- **CIE_xyz_1931_2deg.csv**: Contains the CIE 1931 color-matching functions.
- **examples/**: Folder with Python script that produces example data in the related article.

## License
This project is licensed under the [MIT License](https://github.com/sblisesivdin/spectrum-to-rgb/blob/main/LICENSE). You are free to modify and distribute it as described by the license terms.
