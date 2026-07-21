
class MockOCRAdapter:
    def __init__(self):
        self.name = "MockOCRAdapter"
        self.version = "1.0"
    def infer(self, asset_path):
        return "mock prediction text"

class ReferenceAdapter:
    def __init__(self):
        self.name = "ReferenceAdapter"
        self.version = "1.0"
    def infer(self, asset_path):
        return "reference output"
