## Überblick

`pflanzenschutz-db-main` soll vollständig neu aufgesetzt werden. Der aktuelle Stand:

- Die letzte GHA-Pipeline scheiterte beim ersten Endpoint (`stand`), weil der BVL-Response kein `id`-Feld mehr enthält (`KeyError: 'id'` in `db.insert_records`).
- Frühere Builds liefen zwar durch, erzeugten aber eine leere SQLite-Datei, weil `urllib.parse.urljoin` jeden Pfad mit führendem `/` auf die falsche Route (`https://psm-api.bvl.bund.de/<pfad>`) leitete. Damit kamen zwar HTTP 200, aber ohne Daten.
- Das Frontend (SPA in diesem Repo) erwartet konkrete Tabellen, Lookup-Texte und Bio-Informationen. Bio-Filter greifen auf den View `bvl_mittel_extras` zu.

Der Coding-Agent erhält hiermit einen vollständigen Neuaufbauplan. Bitte jeden Schritt strikt einhalten.

## Zielbild

1. **API-Abdeckung**: Exakt 10 Endpoints (Stand, Mittel, AWG*, Wirkstoff*gehalt, Mittel**). Keine Attach-Imports, alles via Manifest & SQLite-Wasm.
2. **Bio-Daten**: Zusammenführung manueller CSV-Flags und Heuristiken in `bvl_mittel_enrichments` + View `bvl_mittel_extras`.
3. **Manifest & Artefakte**: SQLite, Brotli, optional ZIP + `manifest.json` mit Hashes, Counts, Versionsinfos.
4. **Tests**: Unit- und Integrationstests, die URL-Building, Mapper und End-to-End-Lauf absichern.
5. **CI/CD**: GitHub Actions Workflow baut täglich, veröffentlicht nach `gh-pages`, bricht bei Null-Daten oder Schemaabweichungen ab.

## Schritt-für-Schritt-Plan

### A. Repository vorbereiten

- Lege ein frisches Branch/Repo an (oder räume das alte auf). Entferne alte Artefakte und nicht genutzte Scripts.
- Behalte nützliche statische Daten und Helper (z. B. `data/static/*`, `helpers/compression.py`) – prüfe deren Kompatibilität zur neuen Struktur.

### B. Konfiguration & Schema

1. **Schema entwerfen** (`utils/sqlite_schema.sql` neu erzeugen):

- Tabellen: `bvl_mittel`, `bvl_awg`, `bvl_awg_kultur`, `bvl_awg_schadorg`, `bvl_awg_aufwand`, `bvl_awg_wartezeit`, `bvl_mittel_wirkstoff`, `bvl_mittel_ghs_gefahrenhinweis`, `bvl_mittel_vertrieb`, `bvl_wirkstoff`, `bvl_ghs_gefahrenhinweise`, `bvl_vertriebsfirma`, `bvl_mittel_enrichments`, `bvl_mittel_extras` (View), `bvl_meta`, `bvl_sync_log`.
- Primärschlüssel und Indizes entsprechend Frontend-Nutzung (siehe UI-Code). `bvl_mittel_extras` View muss `kennr`, `is_bio`, `certification_body`, `notes` liefern.
- Ergänze Felder, die das ETL später per Lookup anreichert: `bvl_mittel_wirkstoff` mit `wirkstoff_name`; `bvl_mittel_ghs_gefahrenhinweis` mit `hinweis_kode`, `hinweis_text`; `bvl_mittel_vertrieb` mit `hersteller_name`, `website`.

2. **Konfig-Datei** `configs/endpoints.yaml` komplett neu schreiben:

- `base_url: "https://psm-api.bvl.bund.de/ords/psm/api-v1/"` (Trailing Slash).
- Für jeden Endpoint `path` ohne führenden Slash, plus `name`, `table`, `primary_key` exakt wie Schema.
- Kommentar hinzufügen: „Pfad immer relativ ohne führenden Slash, sonst zerschießt urljoin die Basis-URL“.
- Abschnitt `static_sources` für CSV-Lookups belassen (GHS, Wirkstoffe, Vertriebsfirmen).

3. **Enrichment-Konfig** `configs/enrichments.yaml` anpassen:

- `bio_flags`, `bio_heuristics`, `manufacturer_urls`, `marketing_names`. Stelle sicher, dass Dateipfade existieren (`data/external/...`), Felder zu `bvl_mittel_enrichments` passen.

### C. HTTP & Mapper überarbeiten

1. **HTTP-Client (`scripts/helpers/http_client.py`)**:

- `get` und `fetch_paginated` so umbauen, dass `base_url.rstrip('/') + '/' + path.lstrip('/')` verwendet wird. Kein rohes `urljoin` mehr.
- Füge Logging hinzu (DEBUG-Level), das die endgültige URL ausgibt.
- Baue Timeout/Retry wie bisher, aber bei HTTP 204/empty `items` mit Warnung.

2. **Transformers (`scripts/helpers/transformers.py`)**:

- Mapper für alle 10 Endpoints konsolidieren. Besonders:
  - `map_stand_record`: gib `{"id": 1, "stand": record.get("datum"), "hinweis": record.get("hinweis"), "payload_json": ...}` zurück.
  - `map_mittel_record`, `map_awg_*` etc. gemäß Frontend-Feldern.
  - `map_wirkstoff_gehalt` -> `wirkstoff_name` Platzhalter (wird später angereichert).
  - `map_mittel_ghs_gefahrenhinweis` -> `hinweis_kode`, `hinweis_text` aus Lookup.
  - `map_mittel_vertrieb` -> `hersteller_name`, `website` via Lookup.
- Registry `RECORD_MAPPERS` aktualisieren.

### D. ETL-Pipeline (`scripts/fetch_bvl_data.py`) neu implementieren

1. **Initialisierung**:

- `DatabaseManager.init_schema` ruft neues Schema.
- `load_static_lookups.py` erweitert werden, um Lookups in die Exporttabellen einzuspielen (nicht nur Staging).

2. **Fetch-Logik**:

- Jeder Endpoint verwendet Mapper. Nach Insert `record_count` loggen.
- Wenn `records == 0`, Fehler werfen (Pipeline abbrechen), außer Endpoint ist optional.
- Raw-Download optional (Flag `--skip-raw`).

3. **Bio-Enrichment**:

- `load_static_lookups` oder neues Modul, das CSV `bio_flags.csv` (manuell) plus Heuristik anwendet.
- Ergebnis in `bvl_mittel_enrichments`, anschließend `CREATE VIEW IF NOT EXISTS bvl_mittel_extras AS ...`.

4. **Postprocessing**:

- `enrich_tables_with_lookups`: Fülle `wirkstoff_name`, `hinweis_kode`, `hinweis_text`, `hersteller_name`, `website` in Payload-Spalten.
- `validate_database`: Integritätscheck, Table-Counts, Meta-Werte (`lastSyncIso`, `apiStand`, `dataSource`, `dataSourceType`, `lastSyncCounts`).
- `compress_database`: Brotli + ZIP.
- `generate_manifest`: Enthält `$schema`, `version`, `api_version`, `files` (Name, URL, Größe, Hash, Encoding), `tables`, `build` (Start, Ende, Dauer, python_version, runner).

5. **Logging**: Alle Schritte mit klaren Logs. Bei Fehlern Stacktrace + Eintrag in `stats`.

### E. Tests

1. **Unit-Tests** (`scripts/tests/`):

- `test_http_client.py`: neuer Test `test_build_url_with_or_without_slash`.
- `test_transformers.py`: Abdeckung für `map_stand_record`, `map_mittel_record`, Bio-Mappings.
- `test_database.py`: Prüfe, dass Schema Tabellen/Indizes enthält, `bvl_mittel_extras` View existiert.

2. **Integrationstest** (`test_integration.py`):

- Initialisiere DB, lade statische Lookups, führe `ETLPipeline` mit Dummy-Daten (Mock-Client) durch, verifiziere `lastSyncCounts`, `bvl_mittel_extras` etc.

3. **Validate Script** (`scripts/validate_export.py`):

- Aktualisieren für neue Felder (`wirkstoff_name`, `hinweis_text`, `hersteller_name`).
- Prüft, dass Bio-Produkte `certification_body` oder `notes` haben.

### F. Continuous Integration

1. **GitHub Actions Workflow** (`.github/workflows/build-and-publish.yml` neu):

- Jobs: `lint/test`, `build`.
- `build`: setup python 3.11, install dependencies, `pytest`, `python scripts/fetch_bvl_data.py --output-dir data/output --skip-raw`, `python scripts/validate_export.py data/output/pflanzenschutz.sqlite`.
- Wenn `manifest.json` existiert, `sha256sum` erzeugen, Artefakte uploaden, `gh-pages` aktualisieren.
- Run nur erfolgreich, wenn Counts > 0 (Validierung enforced).

### G. Manuelle QA

1. Lokal `python scripts/fetch_bvl_data.py --output-dir data/output --skip-raw` ausführen.
2. `sqlite3 data/output/pflanzenschutz.sqlite 'SELECT COUNT(*) FROM bvl_mittel;'` (soll >0 sein).
3. `sqlite3 ... 'SELECT COUNT(*) FROM bvl_mittel_extras WHERE is_bio = 1;'` – sicherstellen, dass Bio-Produkte vorhanden sind oder CSV/Heuristik leer melden.
4. Frontend testen: Manifest-URL auf lokale Ausgabe setzen, Sync durchführen, Filter (Bio, Kultur, Schadorg) ausprobieren.

## Risiken & Abfangmaßnahmen

- **API-Änderungen (weitere Feld-Umbenennungen)**: Mapper defensiv schreiben (z. B. `record.get("datum")`). Falls Pflichtfeld fehlt, klaren Fehler werfen.
- **Null-Daten**: Validierung blockiert Release, `stats` protokolliert Endpoints mit 0 Ergebnissen.
- **CSV veraltet**: Tool `scripts/generate_static_csvs.py` aktualisieren, um aus Voll-Lauf neue CSVs zu erzeugen; README entsprechend anpassen.

## Ablieferungen

- Aktualisierte Projekte unter `pflanzenschutz-db-main`:
  - `configs/`, `scripts/`, `data/static/`, `data/external/`, `utils/sqlite_schema.sql`, `.github/workflows/build-and-publish.yml`.
  - Neue Tests, validiertes Manifest, SQLite/Brotli/ZIP im `data/output/` (für Commit oder Release-Upload).
- Dokumentation: README-Abschnitt „Datenquellen & Bio-Handling“ aktualisieren, `IMPLEMENTATION_SUMMARY.md` mit Verweis auf diesen Task.

## Akzeptanzkriterien

- Tests (`pytest scripts/tests`) laufen grün.
- `python scripts/fetch_bvl_data.py --output-dir data/output --skip-raw` produziert nicht leere Tabellen (Counts in Manifest).
- `python scripts/validate_export.py data/output/pflanzenschutz.sqlite` gibt OK.
- Manifest enthält korrekte URLs (`https://abbas-hoseiny.github.io/pflanzenschutz-db/...`) und Hashes.
- Frontend-Sync zeigt Daten, Bio-Filter funktioniert, Wirkstoff- und Gefahrenhinweis-Texte erscheinen im UI.
- GitHub Actions Workflow läuft ohne Fehler durch und veröffentlicht Artefakte.
