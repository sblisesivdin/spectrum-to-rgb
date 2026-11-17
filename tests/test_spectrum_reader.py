from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
load_spectrum = runpy.run_path(str(REPO_ROOT / 'spectrum-to-rgb.py'))['load_spectrum']


class SpectrumReaderTests(unittest.TestCase):
    def test_example_header_and_headerless_files(self):
        with TemporaryDirectory() as directory:
            spectrum = Path(directory) / 'spectrum.csv'
            for delimiter in (',', '\t', ' '):
                rows = delimiter.join(('450.25', '1e-5')) + '\n'
                rows += delimiter.join(('510.5', '0.7')) + '\n'
                for header in ('', f'Wavelength (nm){delimiter}Intensity\n'):
                    with self.subTest(delimiter=delimiter, header=header):
                        spectrum.write_text(header + rows, encoding='utf-8')
                        wavelengths, intensities = load_spectrum(spectrum)
                        np.testing.assert_array_equal(wavelengths, [450.25, 510.5])
                        np.testing.assert_array_equal(intensities, [1e-5, 0.7])

    def test_invalid_numeric_row_is_not_treated_as_a_header(self):
        with TemporaryDirectory() as directory:
            spectrum = Path(directory) / 'spectrum.csv'
            spectrum.write_text('450,nan\n510,0.7\n', encoding='utf-8')
            wavelengths, intensities = load_spectrum(spectrum)
            np.testing.assert_array_equal(wavelengths, [450, 510])
            np.testing.assert_array_equal(intensities, [np.nan, 0.7])
