"""
Tests for common external fetch layer helpers and manifest handlers.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from tempfile import TemporaryDirectory
from ssz_metric_pure.external_fetch_common import (
    ensure_directory,
    write_json,
    read_json,
    estimate_total_size_gb,
    safe_download_allowed,
    collect_file_inventory,
    check_dependency_available
)


def test_manifest_read_write_directory():
    """Verify directories, manifest writing, and JSON reading helpers."""
    with TemporaryDirectory() as tmpdir:
        sub = os.path.join(tmpdir, "subdir")
        ensure_directory(sub)
        assert os.path.exists(sub)
        
        data = {"foo": "bar", "size": 1000}
        json_p = os.path.join(sub, "test.json")
        write_json(json_p, data)
        assert os.path.exists(json_p)
        
        read_data = read_json(json_p)
        assert read_data["foo"] == "bar"


def test_size_estimation():
    """Verify file size estimation helpers."""
    targets = [
        {"size": 1024 * 1024 * 1024},  # 1 GB
        {"estimated_size": 2 * 1024 * 1024 * 1024}  # 2 GB
    ]
    est = estimate_total_size_gb(targets)
    assert est == pytest.approx(3.0)


def test_download_authorization_guards():
    """Verify maximum size threshold and explicit transfer confirmation guards."""
    # Under limit, confirmed
    assert safe_download_allowed(2.5, max_gb=5.0, confirm_download=True) is True
    # Under limit, unconfirmed
    assert safe_download_allowed(2.5, max_gb=5.0, confirm_download=False) is False
    # Over limit, confirmed
    assert safe_download_allowed(12.5, max_gb=10.0, confirm_download=True) is False


def test_file_inventory():
    """Verify local files size/checksum indexing utilities."""
    with TemporaryDirectory() as tmpdir:
        f_path = os.path.join(tmpdir, "test.txt")
        with open(f_path, 'w') as f:
            f.write("hello ssz")
            
        inventory = collect_file_inventory(tmpdir)
        assert len(inventory) == 1
        assert inventory[0]["relative_path"] == "test.txt"
        assert inventory[0]["file_size_bytes"] == 9
        assert "sha256_checksum" in inventory[0]


def test_dependency_checking():
    """Verify external library imports check helpers."""
    assert check_dependency_available("os") is True
    assert check_dependency_available("non_existent_package_12345") is False
