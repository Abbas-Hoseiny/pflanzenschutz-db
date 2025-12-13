-- =============================================================================
-- BVL PSM Database Schema - ALL 41 API ENDPOINTS
-- All column names match the official BVL API 1:1
-- Reference: https://github.com/bundesAPI/pflanzenschutzmittelzulassung-api
-- =============================================================================

-- =============================================================================
-- CORE TABLES (10)
-- =============================================================================

-- 1. Stand (API status/date)
CREATE TABLE IF NOT EXISTS stand (
    id INTEGER PRIMARY KEY DEFAULT 1,
    stand TEXT,
    hinweis TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 2. Mittel (Plant protection products)
CREATE TABLE IF NOT EXISTS mittel (
    kennr TEXT PRIMARY KEY,
    mittelname TEXT,
    formulierung_art TEXT,
    zul_ende TEXT,
    zul_erstmalig_am TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 3. AWG (Application areas)
CREATE TABLE IF NOT EXISTS awg (
    awg_id INTEGER PRIMARY KEY,
    kennr TEXT REFERENCES mittel(kennr),
    antragnr TEXT,
    awgnr TEXT,
    anwendungsbereich TEXT,
    anwendungstechnik TEXT,
    einsatzgebiet TEXT,
    wirkungsbereich TEXT,
    anwendungen_anz_je_befall INTEGER,
    anwendungen_max_je_kultur INTEGER,
    anwendungen_max_je_vegetation INTEGER,
    stadium_kultur_von TEXT,
    stadium_kultur_bis TEXT,
    stadium_kultur_bem TEXT,
    stadium_kultur_kodeliste TEXT,
    stadium_schadorg_von TEXT,
    stadium_schadorg_bis TEXT,
    stadium_schadorg_bem TEXT,
    stadium_schadorg_kodeliste TEXT,
    kultur_erl TEXT,
    schadorg_erl TEXT,
    genehmigung TEXT,
    huk TEXT,
    aw_abstand_von REAL,
    aw_abstand_bis REAL,
    aw_abstand_einheit TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 4. AWG Kultur (cultures per AWG)
CREATE TABLE IF NOT EXISTS awg_kultur (
    awg_id INTEGER REFERENCES awg(awg_id),
    kultur TEXT,
    ausgenommen TEXT,
    sortier_nr INTEGER,
    PRIMARY KEY (awg_id, kultur)
);

-- 5. AWG Schadorg (pests per AWG)
CREATE TABLE IF NOT EXISTS awg_schadorg (
    awg_id INTEGER REFERENCES awg(awg_id),
    schadorg TEXT,
    ausgenommen TEXT,
    sortier_nr INTEGER,
    PRIMARY KEY (awg_id, schadorg)
);

-- 6. AWG Aufwand (application rates)
CREATE TABLE IF NOT EXISTS awg_aufwand (
    awg_id INTEGER REFERENCES awg(awg_id),
    aufwandbedingung TEXT,
    sortier_nr INTEGER,
    m_aufwand REAL,
    m_aufwand_einheit TEXT,
    w_aufwand_von REAL,
    w_aufwand_bis REAL,
    w_aufwand_einheit TEXT,
    PRIMARY KEY (awg_id, sortier_nr)
);

-- 7. AWG Wartezeit (waiting periods)
CREATE TABLE IF NOT EXISTS awg_wartezeit (
    awg_wartezeit_nr INTEGER PRIMARY KEY,
    awg_id INTEGER REFERENCES awg(awg_id),
    kultur TEXT,
    anwendungsbereich TEXT,
    gesetzt_wartezeit INTEGER,
    gesetzt_wartezeit_bem TEXT,
    erlaeuterung TEXT,
    sortier_nr INTEGER
);

-- 8. Wirkstoff (active substances)
CREATE TABLE IF NOT EXISTS wirkstoff (
    wirknr TEXT PRIMARY KEY,
    wirkstoffname TEXT,
    wirkstoffname_en TEXT,
    kategorie TEXT,
    genehmigt TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 9. Wirkstoff Gehalt (active substance content)
CREATE TABLE IF NOT EXISTS wirkstoff_gehalt (
    kennr TEXT REFERENCES mittel(kennr),
    wirknr TEXT REFERENCES wirkstoff(wirknr),
    wirkvar TEXT,
    gehalt_rein REAL,
    gehalt_rein_grundstruktur REAL,
    gehalt_einheit TEXT,
    gehalt_bio REAL,
    gehalt_bio_einheit TEXT,
    payload_json TEXT,
    PRIMARY KEY (kennr, wirknr, wirkvar)
);

-- 10. Mittel Vertrieb (product distributors)
CREATE TABLE IF NOT EXISTS mittel_vertrieb (
    kennr TEXT REFERENCES mittel(kennr),
    vertriebsfirma_nr INTEGER,
    PRIMARY KEY (kennr, vertriebsfirma_nr)
);

-- =============================================================================
-- EXTENDED TABLES (31)
-- =============================================================================

-- 11. Adresse (addresses)
CREATE TABLE IF NOT EXISTS adresse (
    adresse_nr INTEGER PRIMARY KEY,
    name TEXT,
    strasse TEXT,
    plz TEXT,
    ort TEXT,
    land TEXT,
    telefon TEXT,
    telefax TEXT,
    email TEXT,
    internet TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- 12. Antrag (applications)
CREATE TABLE IF NOT EXISTS antrag (
    kennr TEXT,
    antragnr TEXT,
    antragsteller_nr INTEGER,
    zulassungsinhaber_nr INTEGER,
    zulassungsnummer TEXT,
    zulassungsdatum TEXT,
    zul_ende TEXT,
    payload_json TEXT,
    PRIMARY KEY (kennr, antragnr)
);

-- 13. Auflage Redu (reduced requirements)
CREATE TABLE IF NOT EXISTS auflage_redu (
    auflagenr TEXT PRIMARY KEY,
    auflage TEXT,
    auflage_abstand_redu TEXT,
    auflage_abstand_redu_bem TEXT,
    payload_json TEXT
);

-- 14. Auflagen (requirements)
CREATE TABLE IF NOT EXISTS auflagen (
    kennr TEXT,
    antragnr TEXT,
    awg_id INTEGER,
    ebene TEXT,
    auflagenr TEXT,
    auflage TEXT,
    payload_json TEXT,
    PRIMARY KEY (kennr, awg_id, auflagenr)
);

-- 15. AWG Bemerkungen (AWG remarks)
CREATE TABLE IF NOT EXISTS awg_bem (
    awg_id INTEGER REFERENCES awg(awg_id),
    bem TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (awg_id, sortier_nr)
);

-- 16. AWG Partner (tank mix partners)
CREATE TABLE IF NOT EXISTS awg_partner (
    awg_id INTEGER REFERENCES awg(awg_id),
    kennr_partner TEXT,
    partner_typ TEXT,
    partner_bedingung TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (awg_id, kennr_partner)
);

-- 17. AWG Partner Aufwand (partner rates)
CREATE TABLE IF NOT EXISTS awg_partner_aufwand (
    awg_id INTEGER,
    kennr_partner TEXT,
    aufwandbedingung TEXT,
    sortier_nr INTEGER,
    m_aufwand REAL,
    m_aufwand_einheit TEXT,
    payload_json TEXT,
    PRIMARY KEY (awg_id, kennr_partner, sortier_nr)
);

-- 18. AWG Verwendungszweck (intended use)
CREATE TABLE IF NOT EXISTS awg_verwendungszweck (
    awg_id INTEGER REFERENCES awg(awg_id),
    verwendungszweck TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (awg_id, verwendungszweck)
);

-- 19. AWG Wartezeit Ausg Kultur (waiting period exceptions)
CREATE TABLE IF NOT EXISTS awg_wartezeit_ausg_kultur (
    awg_wartezeit_nr INTEGER,
    kultur TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (awg_wartezeit_nr, kultur)
);

-- 20. AWG Zeitpunkt (application timing)
CREATE TABLE IF NOT EXISTS awg_zeitpunkt (
    awg_id INTEGER REFERENCES awg(awg_id),
    zeitpunkt TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (awg_id, zeitpunkt)
);

-- 21. AWG Zulassung (AWG authorization)
CREATE TABLE IF NOT EXISTS awg_zulassung (
    awg_id INTEGER PRIMARY KEY REFERENCES awg(awg_id),
    zulassungsanfang TEXT,
    zulassungsende TEXT,
    aufbrauchfrist TEXT,
    payload_json TEXT
);

-- 22. GHS Gefahrenhinweise (hazard statements)
CREATE TABLE IF NOT EXISTS ghs_gefahrenhinweise (
    kennr TEXT,
    hinweis_kode TEXT,
    hinweis_text TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, hinweis_kode)
);

-- 23. GHS Gefahrensymbole (hazard symbols)
CREATE TABLE IF NOT EXISTS ghs_gefahrensymbole (
    kennr TEXT,
    symbol_kode TEXT,
    symbol_text TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, symbol_kode)
);

-- 24. GHS Sicherheitshinweise (safety statements)
CREATE TABLE IF NOT EXISTS ghs_sicherheitshinweise (
    kennr TEXT,
    hinweis_kode TEXT,
    hinweis_text TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, hinweis_kode)
);

-- 25. GHS Signalwörter (signal words)
CREATE TABLE IF NOT EXISTS ghs_signalwoerter (
    kennr TEXT PRIMARY KEY,
    signalwort TEXT,
    payload_json TEXT
);

-- 26. Hinweis (notices)
CREATE TABLE IF NOT EXISTS hinweis (
    kennr TEXT,
    hinweis_art TEXT,
    hinweis TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, hinweis_art, sortier_nr)
);

-- 27. Kodeliste (code lists)
CREATE TABLE IF NOT EXISTS kodeliste (
    kodeliste_nr INTEGER PRIMARY KEY,
    kodeliste_name TEXT,
    kodeliste_bem TEXT,
    payload_json TEXT
);

-- 28. Kodeliste Feldname (field names)
CREATE TABLE IF NOT EXISTS kodeliste_feldname (
    feld TEXT PRIMARY KEY,
    kodeliste_nr INTEGER,
    payload_json TEXT
);

-- 29. Kode (code values/lookups)
CREATE TABLE IF NOT EXISTS kode (
    kodeliste INTEGER,
    kode TEXT,
    sprache TEXT,
    kodetext TEXT,
    kodetext2 TEXT,
    payload_json TEXT,
    PRIMARY KEY (kodeliste, kode, sprache)
);

-- 30. Kultur Gruppe (culture groups)
CREATE TABLE IF NOT EXISTS kultur_gruppe (
    gruppe TEXT,
    kultur TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (gruppe, kultur)
);

-- 31. Mittel Abgelaufen (expired products)
CREATE TABLE IF NOT EXISTS mittel_abgelaufen (
    kennr TEXT PRIMARY KEY,
    mittelname TEXT,
    zul_ende TEXT,
    aufbrauchfrist TEXT,
    payload_json TEXT
);

-- 32. Mittel Abpackung (package sizes)
CREATE TABLE IF NOT EXISTS mittel_abpackung (
    kennr TEXT,
    abpackung_menge REAL,
    abpackung_einheit TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, sortier_nr)
);

-- 33. Mittel Gefahrensymbol (old hazard symbols)
CREATE TABLE IF NOT EXISTS mittel_gefahren_symbol (
    kennr TEXT,
    gefahren_symbol TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, gefahren_symbol)
);

-- 34. Mittel Wirkbereich (effect areas)
CREATE TABLE IF NOT EXISTS mittel_wirkbereich (
    kennr TEXT,
    wirkbereich TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, wirkbereich)
);

-- 35. Parallelimport Abgelaufen (expired parallel imports)
CREATE TABLE IF NOT EXISTS parallelimport_abgelaufen (
    kennr TEXT PRIMARY KEY,
    parallelimport_kennr TEXT,
    referenzmittel_kennr TEXT,
    zul_ende TEXT,
    payload_json TEXT
);

-- 36. Parallelimport Gültig (valid parallel imports)
CREATE TABLE IF NOT EXISTS parallelimport_gueltig (
    kennr TEXT PRIMARY KEY,
    parallelimport_kennr TEXT,
    referenzmittel_kennr TEXT,
    zul_ende TEXT,
    payload_json TEXT
);

-- 37. Schadorg Gruppe (pest groups)
CREATE TABLE IF NOT EXISTS schadorg_gruppe (
    gruppe TEXT,
    schadorg TEXT,
    sortier_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (gruppe, schadorg)
);

-- 38. Stärkungsmittel (plant strengtheners)
CREATE TABLE IF NOT EXISTS staerkung (
    kennr TEXT PRIMARY KEY,
    mittelname TEXT,
    antragsteller_nr INTEGER,
    listung_ende TEXT,
    payload_json TEXT
);

-- 39. Stärkungsmittel Vertrieb (strengthener distributors)
CREATE TABLE IF NOT EXISTS staerkung_vertrieb (
    kennr TEXT,
    vertriebsfirma_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, vertriebsfirma_nr)
);

-- 40. Zusatzstoff (adjuvants)
CREATE TABLE IF NOT EXISTS zusatzstoff (
    kennr TEXT PRIMARY KEY,
    mittelname TEXT,
    antragsteller_nr INTEGER,
    zul_ende TEXT,
    payload_json TEXT
);

-- 41. Zusatzstoff Vertrieb (adjuvant distributors)
CREATE TABLE IF NOT EXISTS zusatzstoff_vertrieb (
    kennr TEXT,
    vertriebsfirma_nr INTEGER,
    payload_json TEXT,
    PRIMARY KEY (kennr, vertriebsfirma_nr)
);

-- =============================================================================
-- INDEXES for faster queries
-- =============================================================================

-- Core indexes
CREATE INDEX IF NOT EXISTS idx_awg_kennr ON awg(kennr);
CREATE INDEX IF NOT EXISTS idx_awg_kultur_awg_id ON awg_kultur(awg_id);
CREATE INDEX IF NOT EXISTS idx_awg_kultur_kultur ON awg_kultur(kultur);
CREATE INDEX IF NOT EXISTS idx_awg_schadorg_awg_id ON awg_schadorg(awg_id);
CREATE INDEX IF NOT EXISTS idx_awg_schadorg_schadorg ON awg_schadorg(schadorg);
CREATE INDEX IF NOT EXISTS idx_awg_aufwand_awg_id ON awg_aufwand(awg_id);
CREATE INDEX IF NOT EXISTS idx_awg_wartezeit_awg_id ON awg_wartezeit(awg_id);
CREATE INDEX IF NOT EXISTS idx_wirkstoff_gehalt_kennr ON wirkstoff_gehalt(kennr);
CREATE INDEX IF NOT EXISTS idx_wirkstoff_gehalt_wirknr ON wirkstoff_gehalt(wirknr);
CREATE INDEX IF NOT EXISTS idx_mittel_vertrieb_kennr ON mittel_vertrieb(kennr);
CREATE INDEX IF NOT EXISTS idx_mittel_zul_ende ON mittel(zul_ende);
CREATE INDEX IF NOT EXISTS idx_mittel_mittelname ON mittel(mittelname);

-- Extended indexes
CREATE INDEX IF NOT EXISTS idx_antrag_kennr ON antrag(kennr);
CREATE INDEX IF NOT EXISTS idx_auflagen_kennr ON auflagen(kennr);
CREATE INDEX IF NOT EXISTS idx_auflagen_awg_id ON auflagen(awg_id);
CREATE INDEX IF NOT EXISTS idx_awg_bem_awg_id ON awg_bem(awg_id);
CREATE INDEX IF NOT EXISTS idx_awg_partner_awg_id ON awg_partner(awg_id);
CREATE INDEX IF NOT EXISTS idx_ghs_gefahrenhinweise_kennr ON ghs_gefahrenhinweise(kennr);
CREATE INDEX IF NOT EXISTS idx_ghs_gefahrensymbole_kennr ON ghs_gefahrensymbole(kennr);
CREATE INDEX IF NOT EXISTS idx_ghs_sicherheitshinweise_kennr ON ghs_sicherheitshinweise(kennr);
CREATE INDEX IF NOT EXISTS idx_hinweis_kennr ON hinweis(kennr);
CREATE INDEX IF NOT EXISTS idx_kode_kodeliste ON kode(kodeliste);
CREATE INDEX IF NOT EXISTS idx_kultur_gruppe_gruppe ON kultur_gruppe(gruppe);
CREATE INDEX IF NOT EXISTS idx_schadorg_gruppe_gruppe ON schadorg_gruppe(gruppe);
