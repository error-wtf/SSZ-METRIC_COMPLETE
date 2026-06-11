"""
Contract verification tests for Astroquery HEASARC NICER fetching workflows.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from tempfile import TemporaryDirectory
from ssz_metric_pure.nicer_fetch import (
    search_nicer_observations,
    locate_nicer_data,
    build_nicer_manifest,
    download_nicer_data,
    verify_nicer_download
)


# Mock classes to isolate astroquery.heasarc queries from network
class MockHeasarc:
    def query_region(self, pos, catalog, radius):
        from astropy.table import Table
        t = Table(names=["name", "obsid", "ra", "dec", "time", "exposure"], dtype=['str', 'str', 'float', 'float', 'float', 'float'])
        t.add_row(["PSR J0030+0451", "3012010101", 7.58, 4.86, 58000.0, 15000.0])
        return t

    def query_object(self, target, catalog):
        return self.query_region(None, catalog, None)

    def locate_data(self, rows):
        from astropy.table import Table
        t = Table(names=["obsid", "access_url"], dtype=['str', 'str'])
        t.add_row(["3012010101", "https://heasarc.gsfc.nasa.gov/FTP/nicer/data/obs/30/3012010101/"])
        return t


def test_mocked_nicer_search_and_locate(monkeypatch):
    """Verify metadata searching, catalog selection and data location mapping contracts."""
    # Monkeypatch HEASARC query methods
    monkeypatch.setattr("astroquery.heasarc.Heasarc", MockHeasarc)
    
    # Try searching
    res = search_nicer_observations(target="PSR J0030+0451", radius_deg=0.1, min_exposure=5000)
    assert res["count"] == 1
    row = res["results"][0]
    assert row["obsid"] == "3012010101"
    assert row["exposure"] >= 5000
    
    # Try locating links
    links = locate_nicer_data(res["results"])
    assert len(links) == 1
    assert "access_url" in links[0]
    assert links[0]["obsid"] == "3012010101"


def test_nicer_manifest_generation(monkeypatch):
    """Verify JSON schema manifest generation for raw catalog query entries."""
    monkeypatch.setattr("astroquery.heasarc.Heasarc", MockHeasarc)
    
    res = search_nicer_observations(target="PSR J0030+0451")
    links = locate_nicer_data(res["results"])
    
    with TemporaryDirectory() as tmpdir:
        man_p = os.path.join(tmpdir, "nicer.json")
        build_nicer_manifest(res["results"], links, "PSR J0030+0451", man_p)
        assert os.path.exists(man_p)
        
        from ssz_metric_pure.external_fetch_common import load_manifest
        manifest = load_manifest(man_p)
        assert manifest["instrument"] == "NICER"
        assert len(manifest["datasets"]) == 1
        assert manifest["datasets"][0]["dataset_id"] == "3012010101"


def test_mocked_nicer_download_and_verify(monkeypatch):
    """Verify download constraints and directory checks."""
    monkeypatch.setattr("astroquery.heasarc.Heasarc", MockHeasarc)
    
    res = search_nicer_observations(target="PSR J0030+0451")
    links = locate_nicer_data(res["results"])
    
    with TemporaryDirectory() as tmpdir:
        man_p = os.path.join(tmpdir, "nicer.json")
        build_nicer_manifest(res["results"], links, "PSR J0030+0451", man_p)
        
        out_dir = os.path.join(tmpdir, "data")
        
        # Test dry run - must not create data files
        dry_res = download_nicer_data(man_p, out_dir, dry_run=True, confirm_download=True)
        assert dry_res["status"] == "DRY_RUN"
        assert not os.path.exists(out_dir)
        
        # Test unconfirmed download - must SKIP
        skip_res = download_nicer_data(man_p, out_dir, dry_run=False, confirm_download=False)
        assert skip_res["status"] == "SKIP"
        assert not os.path.exists(out_dir)
        
        # Test confirmed download - mock downloading file
        dl_res = download_nicer_data(man_p, out_dir, dry_run=False, confirm_download=True)
        assert dl_res["status"] == "DOWNLOADED"
        assert os.path.exists(out_dir)
        
        # Test checksum verification
        v_res = verify_nicer_download(out_dir, man_p)
        assert v_res["status"] == "VERIFIED"
        assert v_res["verified_datasets"] == 1
