"""
Data Transformers/Mappers for BVL API Records
Transforms raw API responses into database-ready records.
"""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def map_stand_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map stand (status) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "id": 1,  # Always use ID 1 for single stand record
        "stand": record.get("datum"),
        "hinweis": record.get("hinweis"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_mittel_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map mittel (product) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "kennr": record.get("kennr"),
        "mittelname": record.get("mittelname"),
        "zulassungsnummer": record.get("zulnr"),
        "zulassungsende": record.get("zulende"),
        "zulassungsinhaber": record.get("inhaber"),
        "parallelimporteur": record.get("parallelimporteur"),
        "formulierung": record.get("formulierung"),
        "antragssteller": record.get("antragsteller"),
        "stand": record.get("stand"),
        "zusatzinfo": record.get("zusatzinfo"),
        "auflage": record.get("auflage"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_awg_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG (application area) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "awg_id": record.get("awgId"),
        "kennr": record.get("kennr"),
        "awg_titel": record.get("awgTitel"),
        "awg_nr": record.get("awgnr"),
        "gueltig_bis": record.get("gueltigBis"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_awg_kultur_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG kultur (culture) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "awg_id": record.get("awgId"),
        "kultur_kode": record.get("kulturKode"),
        "kultur_text": record.get("kulturText")
    }


def map_awg_schadorg_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG schadorganismus (pest organism) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "awg_id": record.get("awgId"),
        "schadorg_kode": record.get("schadorgKode"),
        "schadorg_text": record.get("schadorgText")
    }


def map_awg_aufwand_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG aufwand (application rate) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "awg_id": record.get("awgId"),
        "aufwandmenge": record.get("aufwandmenge"),
        "aufwandmenge_einheit": record.get("aufwandmengeEinheit"),
        "aufwandmenge_min": record.get("aufwandmengeMin"),
        "aufwandmenge_max": record.get("aufwandmengeMax"),
        "wassermenge": record.get("wassermenge"),
        "wassermenge_einheit": record.get("wassermengeEinheit")
    }


def map_awg_wartezeit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG wartezeit (waiting period) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "awg_id": record.get("awgId"),
        "kultur_kode": record.get("kulturKode"),
        "wartezeit_tage": record.get("wartezeitTage"),
        "wartezeit_text": record.get("wartezeitText")
    }


def map_wirkstoff_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map wirkstoff (active substance) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "wirkstoff_kode": record.get("wirkstoffKode"),
        "wirkstoff_name": record.get("wirkstoffName"),
        "cas_nr": record.get("casNr"),
        "beschreibung": record.get("beschreibung"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_mittel_wirkstoff_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map mittel wirkstoff (product active substance) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "kennr": record.get("kennr"),
        "wirkstoff_kode": record.get("wirkstoffKode"),
        "wirkstoff_name": None,  # Will be enriched via lookup
        "gehalt": record.get("gehalt"),
        "gehalt_einheit": record.get("gehaltEinheit")
    }


def map_mittel_ghs_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map mittel GHS (product hazard statement) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "kennr": record.get("kennr"),
        "hinweis_kode": record.get("hinweisKode"),
        "hinweis_text": None  # Will be enriched via lookup
    }


def map_mittel_vertrieb_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map mittel vertrieb (product distributor) record.
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "kennr": record.get("kennr"),
        "hersteller_name": record.get("herstellerName"),
        "website": None,  # Will be enriched via lookup
        "rolle": record.get("rolle")
    }


# Registry of record mappers by endpoint name
RECORD_MAPPERS = {
    "stand": map_stand_record,
    "mittel": map_mittel_record,
    "awg": map_awg_record,
    "awg_kultur": map_awg_kultur_record,
    "awg_schadorg": map_awg_schadorg_record,
    "awg_aufwand": map_awg_aufwand_record,
    "awg_wartezeit": map_awg_wartezeit_record,
    "wirkstoff": map_wirkstoff_record,
    "mittel_wirkstoff": map_mittel_wirkstoff_record,
    "mittel_vertrieb": map_mittel_vertrieb_record
}


def get_mapper(endpoint_name: str):
    """
    Get mapper function for endpoint.
    
    Args:
        endpoint_name: Name of the endpoint
        
    Returns:
        Mapper function or None if not found
    """
    mapper = RECORD_MAPPERS.get(endpoint_name)
    if not mapper:
        logger.warning(f"No mapper found for endpoint: {endpoint_name}")
    return mapper
