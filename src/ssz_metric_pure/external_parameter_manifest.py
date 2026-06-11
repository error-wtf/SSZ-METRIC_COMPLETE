"""
SSZ External Parameter Manifest Module

Loads and validates independent physical target parameters (M, R, distance, etc.)
required for forward non-circular calculations.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
from typing import Optional
from .external_fetch_common import read_json


def load_parameter_manifest(path: str) -> dict:
    """Load parameter manifest and verify its structure."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Parameter manifest file not found: {path}")
    data = read_json(path)
    if not validate_parameter_manifest_schema(data):
        raise ValueError(f"Invalid parameter manifest schema: {path}")
    return data


def validate_parameter_manifest_schema(data: dict) -> bool:
    """Verify conformity of the parameter manifest schema."""
    required_keys = ["schema_version", "targets"]
    if not all(k in data for k in required_keys):
        return False
    for target in data.get("targets", []):
        target_keys = ["target_id", "target_name", "target_type", "allowed_observable_tests"]
        if not all(k in target for k in target_keys):
            return False
    return True


def get_target_parameters(manifest: dict, target_name: str) -> Optional[dict]:
    """Retrieve target entry from manifest by name (case-insensitive)."""
    for t in manifest.get("targets", []):
        if t["target_name"].strip().lower() == target_name.strip().lower():
            return t
    return None
