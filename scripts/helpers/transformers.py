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
        "awg_id": record.get("awg_id"),
        "kennr": record.get("kennr"),
        "awg_nr": record.get("awgnr"),
        "anwendungsbereich": record.get("anwendungsbereich"),
        "anwendungen_je_kultur": record.get("anwendungen_max_je_vegetation"),
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
        "awg_id": record.get("awg_id"),
        "kultur_kode": record.get("kultur"),
        "ausgenommen": record.get("ausgenommen"),
        "sortier_nr": record.get("sortier_nr")
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
        "awg_id": record.get("awg_id"),
        "schadorg_kode": record.get("schadorg"),
        "ausgenommen": record.get("ausgenommen"),
        "sortier_nr": record.get("sortier_nr")
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
        "awg_id": record.get("awg_id"),
        "aufwand_bedingung": record.get("aufwandbedingung"),
        "sortier_nr": record.get("sortier_nr"),
        "mittel_aufwand": record.get("m_aufwand"),
        "mittel_aufwand_einheit": record.get("m_aufwand_einheit"),
        "wasser_aufwand_von": record.get("w_aufwand_von"),
        "wasser_aufwand_bis": record.get("w_aufwand_bis"),
        "wasser_aufwand_einheit": record.get("w_aufwand_einheit")
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
        "awg_id": record.get("awg_id"),
        "awg_wartezeit_nr": record.get("awg_wartezeit_nr"),
        "kultur": record.get("kultur"),
        "anwendungsbereich": record.get("anwendungsbereich"),
        "sortier_nr": record.get("sortier_nr"),
        "tage": record.get("gesetzt_wartezeit"),
        "bemerkung_kode": record.get("gesetzt_wartezeit_bem"),
        "erlaeuterung": record.get("erlaeuterung")
    }


def map_wirkstoff_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map wirkstoff (active substance) record.
    Maps data from BVL API endpoint /wirkstoff/
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "wirknr": record.get("WIRKNR") or record.get("wirknr"),
        "wirkstoffname": record.get("WIRKSTOFFNAME") or record.get("wirkstoffname"),
        "wirkstoffname_en": record.get("WIRKSTOFFNAME_EN") or record.get("wirkstoffname_en"),
        "kategorie": record.get("KATEGORIE") or record.get("kategorie"),
        "genehmigt": record.get("GENEHMIGT") or record.get("genehmigt"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_wirkstoff_gehalt_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map wirkstoff_gehalt (product active substance content) record.
    Maps data from BVL API endpoint /wirkstoff_gehalt/
    
    Args:
        record: Raw API record
        
    Returns:
        Mapped record for database
    """
    return {
        "kennr": record.get("KENNR") or record.get("kennr"),
        "wirknr": record.get("WIRKNR") or record.get("wirknr"),
        "wirkvar": record.get("WIRKVAR") or record.get("wirkvar"),
        "gehalt_rein": record.get("GEHALT_REIN") or record.get("gehalt_rein"),
        "gehalt_rein_grundstruktur": record.get("GEHALT_REIN_GRUNDSTRUKTUR") or record.get("gehalt_rein_grundstruktur"),
        "gehalt_einheit": record.get("GEHALT_EINHEIT") or record.get("gehalt_einheit"),
        "gehalt_bio": record.get("GEHALT_BIO") or record.get("gehalt_bio"),
        "gehalt_bio_einheit": record.get("GEHALT_BIO_EINHEIT") or record.get("gehalt_bio_einheit"),
        "payload_json": json.dumps(record, ensure_ascii=False)
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
    "wirkstoff_gehalt": map_wirkstoff_gehalt_record,
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
