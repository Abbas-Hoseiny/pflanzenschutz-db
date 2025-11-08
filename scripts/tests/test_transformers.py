"""
Unit tests for transformers/mappers.
"""

import pytest
import json
from scripts.helpers.transformers import (
    map_stand_record,
    map_mittel_record,
    map_awg_record,
    map_mittel_wirkstoff_record,
    map_mittel_ghs_record,
    get_mapper
)


def test_map_stand_record():
    """Test stand record mapping."""
    raw = {
        "datum": "2024-01-15",
        "hinweis": "Test hinweis",
        "extra": "ignored"
    }
    
    result = map_stand_record(raw)
    
    assert result["id"] == 1
    assert result["stand"] == "2024-01-15"
    assert result["hinweis"] == "Test hinweis"
    assert "payload_json" in result
    
    # Check JSON is valid
    payload = json.loads(result["payload_json"])
    assert payload["datum"] == "2024-01-15"


def test_map_mittel_record():
    """Test mittel record mapping."""
    raw = {
        "kennr": "024123-00",
        "mittelname": "Test Produkt",
        "zulnr": "Z123",
        "zulende": "2025-12-31",
        "inhaber": "Test Firma"
    }
    
    result = map_mittel_record(raw)
    
    assert result["kennr"] == "024123-00"
    assert result["mittelname"] == "Test Produkt"
    assert result["zulassungsnummer"] == "Z123"
    assert result["zulassungsende"] == "2025-12-31"
    assert result["zulassungsinhaber"] == "Test Firma"


def test_map_awg_record():
    """Test AWG record mapping."""
    raw = {
        "awgId": "AWG-001",
        "kennr": "024123-00",
        "awgTitel": "Test Application",
        "awgnr": "1",
        "gueltigBis": "2025-12-31"
    }
    
    result = map_awg_record(raw)
    
    assert result["awg_id"] == "AWG-001"
    assert result["kennr"] == "024123-00"
    assert result["awg_titel"] == "Test Application"


def test_map_mittel_wirkstoff_record():
    """Test mittel wirkstoff mapping."""
    raw = {
        "kennr": "024123-00",
        "wirkstoffKode": "WS001",
        "gehalt": 10.5,
        "gehaltEinheit": "g/l"
    }
    
    result = map_mittel_wirkstoff_record(raw)
    
    assert result["kennr"] == "024123-00"
    assert result["wirkstoff_kode"] == "WS001"
    assert result["wirkstoff_name"] is None  # Will be enriched
    assert result["gehalt"] == 10.5
    assert result["gehalt_einheit"] == "g/l"


def test_map_mittel_ghs_record():
    """Test mittel GHS mapping."""
    raw = {
        "kennr": "024123-00",
        "hinweisKode": "H400"
    }
    
    result = map_mittel_ghs_record(raw)
    
    assert result["kennr"] == "024123-00"
    assert result["hinweis_kode"] == "H400"
    assert result["hinweis_text"] is None  # Will be enriched


def test_get_mapper():
    """Test mapper registry."""
    assert get_mapper("stand") == map_stand_record
    assert get_mapper("mittel") == map_mittel_record
    assert get_mapper("awg") == map_awg_record
    assert get_mapper("nonexistent") is None


def test_missing_fields():
    """Test that mappers handle missing fields gracefully."""
    raw = {}
    
    result = map_mittel_record(raw)
    
    # Should not raise exception
    assert result["kennr"] is None
    assert result["mittelname"] is None
