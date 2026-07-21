
VALID = {"APPROVE", "REJECT", "REVISION_REQUIRED", "NEEDS_MORE_INFORMATION"}
def validate_decision(dec):
    return dec in VALID
