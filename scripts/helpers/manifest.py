"""
Manifest generation utilities.
"""

import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime
import sys

logger = logging.getLogger(__name__)


def calculate_sha256(file_path: str) -> str:
    """
    Calculate SHA256 hash of file.
    
    Args:
        file_path: Path to file
        
    Returns:
        Hex digest of SHA256 hash
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def generate_manifest(
    db_path: str,
    output_dir: str,
    compression_results: dict,
    table_counts: dict,
    build_info: dict,
    base_url: str = "https://abbas-hoseiny.github.io/pflanzenschutz-db"
) -> str:
    """
    Generate manifest.json with metadata about the build.
    
    Args:
        db_path: Path to database file
        output_dir: Output directory
        compression_results: Results from compression
        table_counts: Record counts per table
        build_info: Build information (start_time, end_time, etc.)
        base_url: Base URL for file downloads
        
    Returns:
        Path to manifest file
    """
    logger.info("Generating manifest.json")
    
    manifest = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "version": "1.0.0",
        "api_version": build_info.get('api_version', 'v1'),
        "generated_at": datetime.utcnow().isoformat() + 'Z',
        "files": [],
        "tables": table_counts,
        "build": {
            "start_time": build_info.get('start_time', ''),
            "end_time": build_info.get('end_time', ''),
            "duration_seconds": build_info.get('duration_seconds', 0),
            "python_version": sys.version.split()[0],
            "runner": build_info.get('runner', 'local')
        }
    }
    
    # Add database file info
    db_path_obj = Path(db_path)
    db_file_name = db_path_obj.name
    
    manifest['files'].append({
        "name": db_file_name,
        "url": f"{base_url}/{db_file_name}",
        "size": db_path_obj.stat().st_size,
        "sha256": calculate_sha256(db_path),
        "encoding": "none",
        "type": "sqlite"
    })
    
    # Add Brotli compressed file
    if 'brotli' in compression_results:
        brotli_path = Path(compression_results['brotli'])
        manifest['files'].append({
            "name": brotli_path.name,
            "url": f"{base_url}/{brotli_path.name}",
            "size": brotli_path.stat().st_size,
            "sha256": calculate_sha256(str(brotli_path)),
            "encoding": "brotli",
            "type": "sqlite"
        })
    
    # Add ZIP file
    if 'zip' in compression_results:
        zip_path = Path(compression_results['zip'])
        manifest['files'].append({
            "name": zip_path.name,
            "url": f"{base_url}/{zip_path.name}",
            "size": zip_path.stat().st_size,
            "sha256": calculate_sha256(str(zip_path)),
            "encoding": "zip",
            "type": "sqlite"
        })
    
    # Write manifest
    manifest_path = Path(output_dir) / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    logger.info(f"Manifest written to {manifest_path}")
    return str(manifest_path)
