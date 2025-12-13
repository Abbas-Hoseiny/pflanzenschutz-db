-- =============================================================================
-- BVL PSM Database Schema
-- All column names match the official BVL API 1:1
-- Reference: https://github.com/bundesAPI/pflanzenschutzmittelzulassung-api
-- =============================================================================

-- Stand (Datenstand / last update)
CREATE TABLE IF NOT EXISTS stand (
    id INTEGER PRIMARY KEY DEFAULT 1,
    stand TEXT,
    hinweis TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Mittel (Pflanzenschutzmittel / products)
CREATE TABLE IF NOT EXISTS mittel (
    kennr TEXT PRIMARY KEY,
    mittelname TEXT,
    formulierung_art TEXT,
    zul_ende TEXT,
    zul_erstmalig_am TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- AWG (Anwendungsgebiete / application areas)
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

-- AWG Kultur (cultures per AWG)
CREATE TABLE IF NOT EXISTS awg_kultur (
    awg_id INTEGER REFERENCES awg(awg_id),
    kultur TEXT,
    ausgenommen TEXT,
    sortier_nr INTEGER,
    PRIMARY KEY (awg_id, kultur)
);

-- AWG Schadorg (pest organisms per AWG)
CREATE TABLE IF NOT EXISTS awg_schadorg (
    awg_id INTEGER REFERENCES awg(awg_id),
    schadorg TEXT,
    ausgenommen TEXT,
    sortier_nr INTEGER,
    PRIMARY KEY (awg_id, schadorg)
);

-- AWG Aufwand (application rates per AWG)
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

-- AWG Wartezeit (waiting periods per AWG)
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

-- Wirkstoff (active substances)
CREATE TABLE IF NOT EXISTS wirkstoff (
    wirknr TEXT PRIMARY KEY,
    wirkstoffname TEXT,
    wirkstoffname_en TEXT,
    kategorie TEXT,
    genehmigt TEXT,
    payload_json TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Wirkstoff Gehalt (active substance content per product)
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

-- Mittel Vertrieb (product distributors)
CREATE TABLE IF NOT EXISTS mittel_vertrieb (
    kennr TEXT REFERENCES mittel(kennr),
    vertriebsfirma_nr INTEGER,
    PRIMARY KEY (kennr, vertriebsfirma_nr)
);

-- Indexes for faster queries
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
