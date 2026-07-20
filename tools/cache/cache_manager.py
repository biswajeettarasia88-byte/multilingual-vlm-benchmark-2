import json
import os
import hashlib

class VerificationCache:
    def __init__(self, cache_file="verification_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load()
        
    def _load(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}
        
    def _save(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2)
            
    def _hash_meta(self, meta):
        s = json.dumps(meta, sort_keys=True)
        return hashlib.md5(s.encode()).hexdigest()
        
    def get(self, url, meta):
        h = self._hash_meta(meta)
        entry = self.cache.get(url)
        if entry and entry.get("meta_hash") == h:
            return entry
        return None
        
    def set(self, url, meta, result):
        h = self._hash_meta(meta)
        result["meta_hash"] = h
        self.cache[url] = result
        self._save()
