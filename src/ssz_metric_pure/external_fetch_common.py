"""
SSZ Common External Data Fetch Layer

Provides unified classes, enums, path handling, checksumming, dependency checks,
and manifest helper utilities for astrophysical raw data-retrieval pipelines.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import json
import hashlib
from enum import Enum
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any, Optional, Union


class FetchStatus(Enum):
    SEARCH_ONLY = "SEARCH_ONLY"
    DRY_RUN = "DRY_RUN"
    SKIP = "SKIP"
    DOWNLOADED = "DOWNLOADED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"
    PARTIAL = "PARTIAL"


@dataclass
class FetchResult:
    instrument: str
    target_name: str
    dataset_id: str
    status: str
    query: Dict[str, Any] = field(default_factory=dict)
    selected_files: List[str] = field(default_factory=list)
    estimated_size_gb: float = 0.0
    downloaded_files: List[str] = field(default_factory=list)
    manifest_path: Optional[str] = None
    output_dir: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    anti_circularity_note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serialize FetchResult into standard dictionary format."""
        d = asdict(self)
        d["status"] = str(self.status)
        return d


def ensure_directory(path: str) -> str:
    """Ensure directory exists recursively and return absolute normalized path."""
    abs_path = os.path.abspath(path)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def write_json(path: str, data: Any) -> None:
    """Safely write serializable data to JSON file with indentation."""
    ensure_directory(os.path.dirname(path))
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json(path: str) -> Any:
    """Read data from standard JSON file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"JSON manifest file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def table_to_serializable(table) -> List[Dict[str, Any]]:
    """Convert an astropy Table into a standard serializable list of dictionaries."""
    if table is None:
        return []
    # If it's already a list or dict, return it
    if isinstance(table, (list, dict)):
        return table
    try:
        # Convert columns to lists
        data_list = []
        colnames = table.colnames
        for row in table:
            row_dict = {}
            for col in colnames:
                val = row[col]
                # Convert astropy/numpy types to python native types
                if hasattr(val, "item"):
                    val = val.item()
                elif hasattr(val, "decode"):
                    val = val.decode('utf-8')
                row_dict[col] = val
            data_list.append(row_dict)
        return data_list
    except Exception:
        # Fallback
        return []


def estimate_total_size_gb(rows_or_urls: List[Any]) -> float:
    """Estimate total size of download targets in gigabytes."""
    # Dummy placeholder/heuristic: estimate based on list elements or size keys if dict
    total_bytes = 0
    for item in rows_or_urls:
        if isinstance(item, dict):
            size_val = item.get("size") or item.get("estimated_size") or item.get("file_size") or 0
            if isinstance(size_val, (int, float)):
                total_bytes += size_val
            elif isinstance(size_val, str):
                try:
                    total_bytes += float(size_val)
                except ValueError:
                    pass
        else:
            # Assume constant small placeholder 100MB per file if no size is specified
            total_bytes += 100 * 1024 * 1024
    return float(total_bytes / (1024 ** 3))


def safe_download_allowed(estimated_size_gb: float, max_gb: float, confirm_download: bool) -> bool:
    """Determine if a download is authorized under the given size and confirmation policy."""
    if estimated_size_gb > max_gb:
        return False
    return confirm_download


def write_manifest(path: str, manifest: Dict[str, Any]) -> None:
    """Write standard manifest dictionary to specified file path."""
    write_json(path, manifest)


def load_manifest(path: str) -> Dict[str, Any]:
    """Load manifest dictionary from specified file path."""
    return read_json(path)


def sha256_file(path: str) -> str:
    """Generate SHA256 checksum for a file on disk."""
    if not os.path.exists(path) or os.path.isdir(path):
        return ""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def collect_file_inventory(directory: str) -> List[Dict[str, Any]]:
    """Build inventory list of files in directory with relative paths, sizes and checksums."""
    inventory = []
    abs_dir = os.path.abspath(directory)
    if not os.path.exists(abs_dir):
        return []
    for root, _, files in os.walk(abs_dir):
        for f in files:
            p = os.path.join(root, f)
            rel_p = os.path.relpath(p, abs_dir)
            size = os.path.getsize(p)
            checksum = sha256_file(p)
            inventory.append({
                "relative_path": rel_p,
                "file_size_bytes": size,
                "sha256_checksum": checksum
            })
    return inventory


def check_dependency_available(package_name: str) -> bool:
    """Check if external dependency is importable."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def require_external_dependencies() -> None:
    """Enforce import of core astroquery/astropy packages or raise helpful ImportError."""
    missing = []
    for pkg in ["astroquery", "astropy"]:
        if not check_dependency_available(pkg):
            missing.append(pkg)
    if missing:
        raise ImportError(
            f"Missing required external-data dependencies: {missing}. "
            "Please run 'pip install -e \".[external-data]\"' to enable external fetching."
        )
