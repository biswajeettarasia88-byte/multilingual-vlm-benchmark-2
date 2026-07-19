"""Unit tests for license validation."""
import unittest
from tools.license_checker import validate_license

class TestLicenseChecker(unittest.TestCase):
    def test_validate_license(self):
        self.assertTrue(validate_license("CC-BY-4.0"))
        self.assertFalse(validate_license("Unknown"))
        self.assertFalse(validate_license(""))
