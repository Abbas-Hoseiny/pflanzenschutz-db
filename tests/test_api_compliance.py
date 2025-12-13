#!/usr/bin/env python3
"""
Test: Verify pflanzenschutz-db matches official BVL API 1:1
"""

import unittest
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.helpers.transformers import RECORD_MAPPERS


class TestAPICompliance(unittest.TestCase):
    """Test that all field names match official BVL API"""

    def test_mapper_exists_for_each_endpoint(self):
        """Test that we have a mapper for each API endpoint"""
        required = ["stand", "mittel", "awg", "awg_kultur", "awg_schadorg",
                   "awg_aufwand", "awg_wartezeit", "wirkstoff", "wirkstoff_gehalt"]
        for ep in required:
            self.assertIn(ep, RECORD_MAPPERS, f"Missing mapper for: {ep}")

    def test_awg_kultur_uses_kultur_not_kultur_kode(self):
        """API uses 'kultur' NOT 'kultur_kode'"""
        mapper = RECORD_MAPPERS["awg_kultur"]
        result = mapper({"awg_id": 123, "kultur": "TRZAW"})
        self.assertIn("kultur", result)
        self.assertNotIn("kultur_kode", result)
        self.assertEqual(result["kultur"], "TRZAW")

    def test_awg_schadorg_uses_schadorg_not_schadorg_kode(self):
        """API uses 'schadorg' NOT 'schadorg_kode'"""
        mapper = RECORD_MAPPERS["awg_schadorg"]
        result = mapper({"awg_id": 123, "schadorg": "SEPTTR"})
        self.assertIn("schadorg", result)
        self.assertNotIn("schadorg_kode", result)
        self.assertEqual(result["schadorg"], "SEPTTR")

    def test_awg_aufwand_uses_m_aufwand_not_mittel_aufwand(self):
        """API uses 'm_aufwand' NOT 'mittel_aufwand'"""
        mapper = RECORD_MAPPERS["awg_aufwand"]
        result = mapper({"awg_id": 123, "m_aufwand": 1.5, "m_aufwand_einheit": "l/ha"})
        self.assertIn("m_aufwand", result)
        self.assertIn("m_aufwand_einheit", result)
        self.assertNotIn("mittel_aufwand", result)
        self.assertNotIn("mittel_aufwand_einheit", result)

    def test_awg_wartezeit_uses_gesetzt_wartezeit_not_tage(self):
        """API uses 'gesetzt_wartezeit' NOT 'tage'"""
        mapper = RECORD_MAPPERS["awg_wartezeit"]
        result = mapper({"awg_wartezeit_nr": 1, "awg_id": 123, "gesetzt_wartezeit": 28})
        self.assertIn("gesetzt_wartezeit", result)
        self.assertNotIn("tage", result)
        self.assertEqual(result["gesetzt_wartezeit"], 28)

    def test_mittel_uses_zul_ende_not_zulassungsende(self):
        """API uses 'zul_ende' NOT 'zulassungsende'"""
        mapper = RECORD_MAPPERS["mittel"]
        result = mapper({"kennr": "024213-73", "mittelname": "Test", "zul_ende": "2025-12-31"})
        self.assertIn("zul_ende", result)
        self.assertIn("kennr", result)
        self.assertNotIn("zulassungsende", result)
        self.assertNotIn("zulnr", result)

    def test_awg_kultur_table_has_kultur_column(self):
        """Verify awg_kultur table uses 'kultur' column"""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "utils", "sqlite_schema.sql"
        )
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        # Find awg_kultur table definition
        match = re.search(r'CREATE TABLE.*?awg_kultur\s*\((.*?)\);', schema, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(match, "awg_kultur table not found")
        
        table_def = match.group(1).lower()
        # Must have 'kultur' column (word boundary check)
        self.assertRegex(table_def, r'\bkultur\b')
        # Must NOT have 'kultur_kode' as a column (exact match, not part of another word)
        columns = [c.strip().split()[0] for c in table_def.split(',')]
        self.assertNotIn('kultur_kode', columns)

    def test_awg_schadorg_table_has_schadorg_column(self):
        """Verify awg_schadorg table uses 'schadorg' column"""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "utils", "sqlite_schema.sql"
        )
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        match = re.search(r'CREATE TABLE.*?awg_schadorg\s*\((.*?)\);', schema, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(match, "awg_schadorg table not found")
        
        table_def = match.group(1).lower()
        self.assertRegex(table_def, r'\bschadorg\b')
        columns = [c.strip().split()[0] for c in table_def.split(',')]
        self.assertNotIn('schadorg_kode', columns)

    def test_awg_aufwand_table_has_m_aufwand_columns(self):
        """Verify awg_aufwand table uses 'm_aufwand' columns"""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "utils", "sqlite_schema.sql"
        )
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        match = re.search(r'CREATE TABLE.*?awg_aufwand\s*\((.*?)\);', schema, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(match, "awg_aufwand table not found")
        
        table_def = match.group(1).lower()
        self.assertIn('m_aufwand', table_def)
        self.assertIn('m_aufwand_einheit', table_def)
        columns = [c.strip().split()[0] for c in table_def.split(',')]
        self.assertNotIn('mittel_aufwand', columns)

    def test_awg_wartezeit_table_has_gesetzt_wartezeit(self):
        """Verify awg_wartezeit table uses 'gesetzt_wartezeit' column"""
        schema_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "utils", "sqlite_schema.sql"
        )
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        match = re.search(r'CREATE TABLE.*?awg_wartezeit\s*\((.*?)\);', schema, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(match, "awg_wartezeit table not found")
        
        table_def = match.group(1).lower()
        self.assertIn('gesetzt_wartezeit', table_def)
        columns = [c.strip().split()[0] for c in table_def.split(',')]
        self.assertNotIn('tage', columns)


if __name__ == "__main__":
    print("=" * 60)
    print("BVL API Compliance Test")
    print("Verifying pflanzenschutz-db matches official API 1:1")
    print("=" * 60)
    unittest.main(verbosity=2)
