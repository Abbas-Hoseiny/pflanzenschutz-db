"""
Data Transformers/Mappers for BVL API Records

Transforms raw API responses into database-ready records.
IMPORTANT: All field names must match the official BVL API 1:1!
See: https://github.com/bundesAPI/pflanzenschutzmittelzulassung-api
"""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def map_stand_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map stand (status) record.
    API: /stand/
    """
    return {
        "id": 1,
        "stand": record.get("datum"),
        "hinweis": record.get("hinweis"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_mittel_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map mittel (product) record.
    API: /mittel/
    
    Official API fields:
    - kennr: Primary key (9 chars, e.g. "024213-73")
    - mittelname: Product name
    - formulierung_art: Formulation type code
    - zul_ende: Authorization end date
    - zul_erstmalig_am: First authorization date
    """
    return {
        "kennr": record.get("kennr"),
        "mittelname": record.get("mittelname"),
        "formulierung_art": record.get("formulierung_art"),
        "zul_ende": record.get("zul_ende"),
        "zul_erstmalig_am": record.get("zul_erstmalig_am"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_awg_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG (application area) record.
    API: /awg/
    
    Official API fields - ALL preserved 1:1
    """
    return {
        "awg_id": record.get("awg_id"),
        "kennr": record.get("kennr"),
        "antragnr": record.get("antragnr"),
        "awgnr": record.get("awgnr"),
        "anwendungsbereich": record.get("anwendungsbereich"),
        "anwendungstechnik": record.get("anwendungstechnik"),
        "einsatzgebiet": record.get("einsatzgebiet"),
        "wirkungsbereich": record.get("wirkungsbereich"),
        "anwendungen_anz_je_befall": record.get("anwendungen_anz_je_befall"),
        "anwendungen_max_je_kultur": record.get("anwendungen_max_je_kultur"),
        "anwendungen_max_je_vegetation": record.get("anwendungen_max_je_vegetation"),
        "stadium_kultur_von": record.get("stadium_kultur_von"),
        "stadium_kultur_bis": record.get("stadium_kultur_bis"),
        "stadium_kultur_bem": record.get("stadium_kultur_bem"),
        "stadium_kultur_kodeliste": record.get("stadium_kultur_kodeliste"),
        "stadium_schadorg_von": record.get("stadium_schadorg_von"),
        "stadium_schadorg_bis": record.get("stadium_schadorg_bis"),
        "stadium_schadorg_bem": record.get("stadium_schadorg_bem"),
        "stadium_schadorg_kodeliste": record.get("stadium_schadorg_kodeliste"),
        "kultur_erl": record.get("kultur_erl"),
        "schadorg_erl": record.get("schadorg_erl"),
        "genehmigung": record.get("genehmigung"),
        "huk": record.get("huk"),
        "aw_abstand_von": record.get("aw_abstand_von"),
        "aw_abstand_bis": record.get("aw_abstand_bis"),
        "aw_abstand_einheit": record.get("aw_abstand_einheit"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_awg_kultur_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG kultur (culture) record.
    API: /awg_kultur/
    
    Official API fields:
    - awg_id: FK to AWG
    - kultur: EPPO code (NOT kultur_kode!)
    - ausgenommen: J/N
    - sortier_nr: Sort order
    """
    return {
        "awg_id": record.get("awg_id"),
        "kultur": record.get("kultur"),
        "ausgenommen": record.get("ausgenommen"),
        "sortier_nr": record.get("sortier_nr")
    }


def map_awg_schadorg_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG schadorganismus (pest organism) record.
    API: /awg_schadorg/
    
    Official API fields:
    - awg_id: FK to AWG
    - schadorg: EPPO code (NOT schadorg_kode!)
    - ausgenommen: J/N
    - sortier_nr: Sort order
    """
    return {
        "awg_id": record.get("awg_id"),
        "schadorg": record.get("schadorg"),
        "ausgenommen": record.get("ausgenommen"),
        "sortier_nr": record.get("sortier_nr")
    }


def map_awg_aufwand_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG aufwand (application rate) record.
    API: /awg_aufwand/
    
    Official API fields:
    - awg_id: FK to AWG
    - aufwandbedingung: Condition
    - sortier_nr: Sort order
    - m_aufwand: Product amount (NOT mittel_aufwand!)
    - m_aufwand_einheit: Product unit
    - w_aufwand_von: Water amount from
    - w_aufwand_bis: Water amount to
    - w_aufwand_einheit: Water unit
    """
    return {
        "awg_id": record.get("awg_id"),
        "aufwandbedingung": record.get("aufwandbedingung"),
        "sortier_nr": record.get("sortier_nr"),
        "m_aufwand": record.get("m_aufwand"),
        "m_aufwand_einheit": record.get("m_aufwand_einheit"),
        "w_aufwand_von": record.get("w_aufwand_von"),
        "w_aufwand_bis": record.get("w_aufwand_bis"),
        "w_aufwand_einheit": record.get("w_aufwand_einheit")
    }


def map_awg_wartezeit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map AWG wartezeit (waiting period) record.
    API: /awg_wartezeit/
    
    Official API fields:
    - awg_wartezeit_nr: Primary key
    - awg_id: FK to AWG
    - kultur: EPPO code
    - anwendungsbereich: Application area code
    - gesetzt_wartezeit: Waiting period in days (NOT tage!)
    - gesetzt_wartezeit_bem: Remark code
    - erlaeuterung: Explanation
    - sortier_nr: Sort order
    """
    return {
        "awg_wartezeit_nr": record.get("awg_wartezeit_nr"),
        "awg_id": record.get("awg_id"),
        "kultur": record.get("kultur"),
        "anwendungsbereich": record.get("anwendungsbereich"),
        "gesetzt_wartezeit": record.get("gesetzt_wartezeit"),
        "gesetzt_wartezeit_bem": record.get("gesetzt_wartezeit_bem"),
        "erlaeuterung": record.get("erlaeuterung"),
        "sortier_nr": record.get("sortier_nr")
    }


def map_wirkstoff_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map wirkstoff (active substance) record.
    API: /wirkstoff/
    
    Official API fields:
    - wirknr: Primary key (max 4 chars)
    - wirkstoffname: German name
    - wirkstoffname_en: English name
    - kategorie: Category
    - genehmigt: Approved (J/N)
    """
    return {
        "wirknr": record.get("wirknr"),
        "wirkstoffname": record.get("wirkstoffname"),
        "wirkstoffname_en": record.get("wirkstoffname_en"),
        "kategorie": record.get("kategorie"),
        "genehmigt": record.get("genehmigt"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_wirkstoff_gehalt_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map wirkstoff_gehalt (product active substance content) record.
    API: /wirkstoff_gehalt/
    
    Official API fields:
    - kennr: FK to mittel
    - wirknr: FK to wirkstoff
    - wirkvar: Variant
    - gehalt_rein: Pure content
    - gehalt_rein_grundstruktur: Base structure content
    - gehalt_einheit: Unit
    - gehalt_bio: Bio content
    - gehalt_bio_einheit: Bio unit
    """
    return {
        "kennr": record.get("kennr"),
        "wirknr": record.get("wirknr"),
        "wirkvar": record.get("wirkvar"),
        "gehalt_rein": record.get("gehalt_rein"),
        "gehalt_rein_grundstruktur": record.get("gehalt_rein_grundstruktur"),
        "gehalt_einheit": record.get("gehalt_einheit"),
        "gehalt_bio": record.get("gehalt_bio"),
        "gehalt_bio_einheit": record.get("gehalt_bio_einheit"),
        "payload_json": json.dumps(record, ensure_ascii=False)
    }


def map_mittel_vertrieb_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map mittel vertrieb (product distributor) record.
    API: /mittel_vertrieb/
    """
    return {
        "kennr": record.get("kennr"),
        "vertriebsfirma_nr": record.get("vertriebsfirma_nr")
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
    """Get mapper function for endpoint."""
    mapper = RECORD_MAPPERS.get(endpoint_name)
    if not mapper:
        logger.warning(f"No mapper found for endpoint: {endpoint_name}")
    return mapper
