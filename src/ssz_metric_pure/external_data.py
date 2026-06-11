"""
SSZ External Data Validation Common Module

Defines schemas, load, and manifest checking helpers for external observational validation gates.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
from .external_fetch_common import load_manifest, write_manifest


def load_external_manifest(path: str) -> dict:
    """Load standard NICER or ALMA fetch manifest."""
    return load_manifest(path)


def validate_manifest_schema(manifest: dict) -> bool:
    """
    Validate that the loaded manifest dict conforms to the required common schema.
    """
    required_keys = ["schema_version", "created_utc", "created_by", "instrument", "datasets"]
    if not all(k in manifest for k in required_keys):
        return False
        
    for dataset in manifest.get("datasets", []):
        dataset_required_keys = [
            "dataset_id", "target_name", "obs_id_or_project_code", "archive",
            "access_url", "local_path", "validation_category", "model_dependency"
        ]
        if not all(k in dataset for k in dataset_required_keys):
            return False
            
    return True
