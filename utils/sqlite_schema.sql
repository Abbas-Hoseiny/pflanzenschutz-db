-- BVL Pflanzenschutzmittel Database Schema
-- This schema defines all tables, views, and indexes for the BVL plant protection database

-- Meta information table
CREATE TABLE IF NOT EXISTS bvl_meta (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Sync log table
CREATE TABLE IF NOT EXISTS bvl_sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sync_start TEXT,
    sync_end TEXT,
    duration_seconds REAL,
    status TEXT,
    error_message TEXT,
    records_processed INTEGER DEFAULT 0
);

-- Main product table (Mittel)
CREATE TABLE IF NOT EXISTS bvl_mittel (
    kennr TEXT PRIMARY KEY,
    mittelname TEXT,
    zulassungsnummer TEXT,
    zulassungsende TEXT,
    zulassungsinhaber TEXT,
    parallelimporteur TEXT,
    formulierung TEXT,
    antragssteller TEXT,
    stand TEXT,
    zusatzinfo TEXT,
    auflage TEXT,
    payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_bvl_mittel_name ON bvl_mittel(mittelname);
CREATE INDEX IF NOT EXISTS idx_bvl_mittel_zulnr ON bvl_mittel(zulassungsnummer);
CREATE INDEX IF NOT EXISTS idx_bvl_mittel_inhaber ON bvl_mittel(zulassungsinhaber);

-- Application areas table (Anwendungsgebiete - AWG)
CREATE TABLE IF NOT EXISTS bvl_awg (
    awg_id TEXT PRIMARY KEY,
    kennr TEXT,
    awg_titel TEXT,
    awg_nr TEXT,
    gueltig_bis TEXT,
    payload_json TEXT,
    FOREIGN KEY (kennr) REFERENCES bvl_mittel(kennr)
);

CREATE INDEX IF NOT EXISTS idx_bvl_awg_kennr ON bvl_awg(kennr);

-- AWG culture table
CREATE TABLE IF NOT EXISTS bvl_awg_kultur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    awg_id TEXT,
    kultur_kode TEXT,
    kultur_text TEXT,
    FOREIGN KEY (awg_id) REFERENCES bvl_awg(awg_id)
);

CREATE INDEX IF NOT EXISTS idx_bvl_awg_kultur_awg ON bvl_awg_kultur(awg_id);
CREATE INDEX IF NOT EXISTS idx_bvl_awg_kultur_kode ON bvl_awg_kultur(kultur_kode);

-- AWG pest organism table
CREATE TABLE IF NOT EXISTS bvl_awg_schadorg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    awg_id TEXT,
    schadorg_kode TEXT,
    schadorg_text TEXT,
    FOREIGN KEY (awg_id) REFERENCES bvl_awg(awg_id)
);

CREATE INDEX IF NOT EXISTS idx_bvl_awg_schadorg_awg ON bvl_awg_schadorg(awg_id);
CREATE INDEX IF NOT EXISTS idx_bvl_awg_schadorg_kode ON bvl_awg_schadorg(schadorg_kode);

-- AWG application rates table
CREATE TABLE IF NOT EXISTS bvl_awg_aufwand (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    awg_id TEXT,
    aufwandmenge TEXT,
    aufwandmenge_einheit TEXT,
    aufwandmenge_min TEXT,
    aufwandmenge_max TEXT,
    wassermenge TEXT,
    wassermenge_einheit TEXT,
    FOREIGN KEY (awg_id) REFERENCES bvl_awg(awg_id)
);

CREATE INDEX IF NOT EXISTS idx_bvl_awg_aufwand_awg ON bvl_awg_aufwand(awg_id);

-- AWG waiting period table
CREATE TABLE IF NOT EXISTS bvl_awg_wartezeit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    awg_id TEXT,
    kultur_kode TEXT,
    wartezeit_tage INTEGER,
    wartezeit_text TEXT,
    FOREIGN KEY (awg_id) REFERENCES bvl_awg(awg_id)
);

CREATE INDEX IF NOT EXISTS idx_bvl_awg_wartezeit_awg ON bvl_awg_wartezeit(awg_id);

-- Active substances table
CREATE TABLE IF NOT EXISTS bvl_wirkstoff (
    wirkstoff_kode TEXT PRIMARY KEY,
    wirkstoff_name TEXT,
    cas_nr TEXT,
    beschreibung TEXT,
    payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_bvl_wirkstoff_name ON bvl_wirkstoff(wirkstoff_name);

-- Product active substance relationship table
CREATE TABLE IF NOT EXISTS bvl_mittel_wirkstoff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kennr TEXT,
    wirkstoff_kode TEXT,
    wirkstoff_name TEXT,
    gehalt REAL,
    gehalt_einheit TEXT,
    FOREIGN KEY (kennr) REFERENCES bvl_mittel(kennr),
    FOREIGN KEY (wirkstoff_kode) REFERENCES bvl_wirkstoff(wirkstoff_kode)
);

CREATE INDEX IF NOT EXISTS idx_bvl_mittel_wirkstoff_kennr ON bvl_mittel_wirkstoff(kennr);
CREATE INDEX IF NOT EXISTS idx_bvl_mittel_wirkstoff_kode ON bvl_mittel_wirkstoff(wirkstoff_kode);

-- GHS hazard statements reference table
CREATE TABLE IF NOT EXISTS bvl_ghs_gefahrenhinweise (
    hinweis_kode TEXT PRIMARY KEY,
    hinweis_text TEXT,
    beschreibung TEXT
);

-- Product GHS hazard statements relationship table
CREATE TABLE IF NOT EXISTS bvl_mittel_ghs_gefahrenhinweis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kennr TEXT,
    hinweis_kode TEXT,
    hinweis_text TEXT,
    FOREIGN KEY (kennr) REFERENCES bvl_mittel(kennr),
    FOREIGN KEY (hinweis_kode) REFERENCES bvl_ghs_gefahrenhinweise(hinweis_kode)
);

CREATE INDEX IF NOT EXISTS idx_bvl_mittel_ghs_kennr ON bvl_mittel_ghs_gefahrenhinweis(kennr);
CREATE INDEX IF NOT EXISTS idx_bvl_mittel_ghs_kode ON bvl_mittel_ghs_gefahrenhinweis(hinweis_kode);

-- Distributor/manufacturer reference table
CREATE TABLE IF NOT EXISTS bvl_vertriebsfirma (
    firma_name TEXT PRIMARY KEY,
    website TEXT,
    adresse TEXT,
    kontakt TEXT
);

-- Product distributor relationship table
CREATE TABLE IF NOT EXISTS bvl_mittel_vertrieb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kennr TEXT,
    hersteller_name TEXT,
    website TEXT,
    rolle TEXT,
    FOREIGN KEY (kennr) REFERENCES bvl_mittel(kennr),
    FOREIGN KEY (hersteller_name) REFERENCES bvl_vertriebsfirma(firma_name)
);

CREATE INDEX IF NOT EXISTS idx_bvl_mittel_vertrieb_kennr ON bvl_mittel_vertrieb(kennr);
CREATE INDEX IF NOT EXISTS idx_bvl_mittel_vertrieb_hersteller ON bvl_mittel_vertrieb(hersteller_name);

-- Bio/organic enrichment table
CREATE TABLE IF NOT EXISTS bvl_mittel_enrichments (
    kennr TEXT PRIMARY KEY,
    is_bio INTEGER DEFAULT 0,
    certification_body TEXT,
    notes TEXT,
    source TEXT,
    FOREIGN KEY (kennr) REFERENCES bvl_mittel(kennr)
);

CREATE INDEX IF NOT EXISTS idx_bvl_mittel_enrichments_bio ON bvl_mittel_enrichments(is_bio);

-- View for bio/organic products with extras
CREATE VIEW IF NOT EXISTS bvl_mittel_extras AS
SELECT 
    m.kennr,
    m.mittelname,
    m.zulassungsnummer,
    m.zulassungsende,
    m.zulassungsinhaber,
    COALESCE(e.is_bio, 0) AS is_bio,
    e.certification_body,
    e.notes,
    e.source
FROM bvl_mittel m
LEFT JOIN bvl_mittel_enrichments e ON m.kennr = e.kennr;

-- Stand (status/date) table for API metadata
CREATE TABLE IF NOT EXISTS bvl_stand (
    id INTEGER PRIMARY KEY,
    stand TEXT,
    hinweis TEXT,
    payload_json TEXT
);
