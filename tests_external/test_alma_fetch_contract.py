"""
Contract verification tests for Astroquery ALMA fetching workflows.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import pytest
from tempfile import TemporaryDirectory
from ssz_metric_pure.alma_fetch import (
    search_alma_observations,
    extract_alma_uids,
    get_alma_data_info,
    filter_alma_products,
    build_alma_manifest,
    download_alma_products,
    verify_alma_download
)


# Mock ALMA client implementation
class MockAlma:
    def __init__(self):
        self.cache_location = None

    def query_object(self, target):
        from astropy.table import Table
        t = Table(names=["target_name", "project_code", "member_ous_uid", "band_list", "frequency", "data_rights"], dtype=['str', 'str', 'str', 'str', 'float', 'str'])
        t.add_row(["M87", "2018.1.01234.S", "uid://A001/X12a/X3b", "6", 230.0, "Public"])
        return t

    def query_region(self, pos, radius):
        return self.query_object(None)

    def query_tap(self, query):
        return self.query_object(None)

    def query(self, payload):
        return self.query_object(None)

    def get_data_info(self, uids, expand_tarfiles=True):
        from astropy.table import Table
        t = Table(names=["member_ous_uid", "access_url", "file_name", "size", "product_type"], dtype=['str', 'str', 'str', 'int', 'str'])
        t.add_row(["uid://A001/X12a/X3b", "https://almascience.eso.org/data/member.uid_A001_X12a_X3b.fits", "member.uid_A001_X12a_X3b.fits", 500000, "FITS"])
        t.add_row(["uid://A001/X12a/X3b", "https://almascience.eso.org/data/member.uid_A001_X12a_X3b.README", "README", 500, "README"])
        return t

    def download_files(self, urls, cache=True):
        return urls


def test_mocked_alma_search_and_locate(monkeypatch):
    """Verify metadata searching, catalog selection and data location mapping contracts."""
    monkeypatch.setattr("astroquery.alma.Alma", MockAlma)
    
    res = search_alma_observations(target="M87", radius_deg=0.02)
    assert res["count"] == 1
    
    uids = extract_alma_uids(res["results"])
    assert len(uids) == 1
    assert uids[0] == "uid://A001/X12a/X3b"
    
    info = get_alma_data_info(uids)
    assert len(info) == 2
    
    filtered_urls = filter_alma_products(info, product_type="fits")
    assert len(filtered_urls) == 2  # FITS url + README url (automatically included)
    assert any(".fits" in url for url in filtered_urls)


def test_alma_manifest_generation(monkeypatch):
    """Verify JSON schema manifest generation for ALMA product URLs."""
    monkeypatch.setattr("astroquery.alma.Alma", MockAlma)
    
    res = search_alma_observations(target="M87")
    uids = extract_alma_uids(res["results"])
    info = get_alma_data_info(uids)
    selected_urls = filter_alma_products(info, product_type="fits")
    
    with TemporaryDirectory() as tmpdir:
        man_p = os.path.join(tmpdir, "alma.json")
        build_alma_manifest(res["results"], info, selected_urls, "M87", man_p)
        assert os.path.exists(man_p)
        
        from ssz_metric_pure.external_fetch_common import load_manifest
        manifest = load_manifest(man_p)
        assert manifest["instrument"] == "ALMA"
        assert len(manifest["datasets"]) == 2


def test_mocked_alma_download_and_verify(monkeypatch):
    """Verify ALMA download options and file checks."""
    monkeypatch.setattr("astroquery.alma.Alma", MockAlma)
    
    res = search_alma_observations(target="M87")
    uids = extract_alma_uids(res["results"])
    info = get_alma_data_info(uids)
    selected_urls = filter_alma_products(info, product_type="fits")
    
    with TemporaryDirectory() as tmpdir:
        man_p = os.path.join(tmpdir, "alma.json")
        build_alma_manifest(res["results"], info, selected_urls, "M87", man_p)
        
        out_dir = os.path.join(tmpdir, "data")
        cache_dir = os.path.join(tmpdir, "cache")
        
        # Test dry-run
        dry_res = download_alma_products(man_p, out_dir, cache_dir, dry_run=True, confirm_download=True)
        assert dry_res["status"] == "DRY_RUN"
        
        # Test confirmed download
        dl_res = download_alma_products(man_p, out_dir, cache_dir, dry_run=False, confirm_download=True)
        assert dl_res["status"] == "DOWNLOADED"
        
        # Verify
        v_res = verify_alma_download(out_dir, man_p)
        assert v_res["status"] == "VERIFIED"
        assert v_res["verified_datasets"] == 2
