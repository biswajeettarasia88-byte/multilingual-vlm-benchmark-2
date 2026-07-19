import pytest
from tools.license_checker import normalize_license

@pytest.mark.parametrize("raw, expected", [
    ("CC BY-SA 4.0", "CC-BY-SA-4.0"),
    ("  cc by 4.0  ", "CC-BY-4.0"),
    ("Public Domain", "PUBLIC-DOMAIN"),
    ("PUBLIC DOMAIN", "PUBLIC-DOMAIN"),
    ("CC0", "CC0-1.0"),
    ("CC_BY-SA_3.0", "CC-BY-SA-3.0"),
    ("Unknown License", "UNKNOWN-LICENSE")
])
def test_normalize_license(raw, expected):
    assert normalize_license(raw) == expected
