
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.connectors.registry import ConnectorRegistry
from tools.connectors.plugins.funsd_connector import FUNSDConnector

class TestConnectors(unittest.TestCase):
    def test_registry(self):
        reg = ConnectorRegistry()
        reg.register("FUNSD", FUNSDConnector)
        self.assertIsNotNone(reg.get_connector("FUNSD"))
        
    def test_base_connector(self):
        conn = FUNSDConnector()
        self.assertTrue(conn.connect())
        info = conn.get_dataset_information()
        self.assertEqual(info["dataset_name"], "FUNSD")
        self.assertEqual(conn.get_license_information(), "CC-BY-4.0")
        
    def test_enumeration_capability(self):
        conn = FUNSDConnector()
        cap, reason = conn.enumeration_capability()
        self.assertEqual(cap, "ENUMERATION_REQUIRES_DOWNLOAD")
        
if __name__ == '__main__':
    unittest.main()
