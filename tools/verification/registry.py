from tools.verification.http_verifier import HttpVerifier

class VerifierRegistry:
    def __init__(self):
        self.verifiers = {
            "http_raw": HttpVerifier()
        }
        
    def get_verifier(self, download_method: str):
        return self.verifiers.get(download_method, self.verifiers["http_raw"])
