
def parse_license(license_str):
    if "CC-BY" in license_str: return "CC-BY-4.0"
    return "UNKNOWN"
