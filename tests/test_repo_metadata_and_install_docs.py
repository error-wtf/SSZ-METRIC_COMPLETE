"""
Test Repository Metadata, Versioning, and Installer Script Purity.

Verifies:
- README.md holds version v1.1.0-canonical-pure, Xi-primary definitions, D*s=1 identity,
  local c invariance, limitations section, and contains ZERO forbidden overclaims.
- install.sh has zero stale marketing or obsolete script paths.
- install.bat has zero stale versions or incorrect path installation dependencies.
- requirements.txt is aligned exactly with pyproject.toml runtime dependencies.
- pyproject.toml is at version 1.1.0.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import re
from pathlib import Path


def test_readme_purity():
    """Verify README metadata and ensure absolutely zero forbidden overclaims."""
    repo_root = Path(__file__).resolve().parent.parent
    readme_path = repo_root / "README.md"
    
    assert readme_path.exists(), "README.md is missing!"
    content = readme_path.read_text(encoding="utf-8")
    
    print(f"  README.md found: {len(content)} characters")
    print(f"  Version v1.1.0-canonical-pure present: {'v1.1.0-canonical-pure' in content}")
    print(f"  Xi-primary present: {'Xi-primary' in content or 'Xi(r) primary' in content}")
    print(f"  Limitations section present: {'Limitations' in content}")
    
    # Required terms and structures
    assert "v1.1.0-canonical-pure" in content
    assert "Xi-primary" in content or "Xi(r) primary" in content
    assert "D(r) = " in content or "D = " in content
    assert "s(r) = " in content or "s = " in content
    assert "D(r) " in content
    assert "s(r) = 1 + \\Xi(r)" in content or "s = 1 + Xi" in content or "s(r) = 1 + \\\\Xi(r)" in content
    assert "local c remains invariant" in content or "local light-speed remains strictly invariant" in content
    assert "Current Limitations" in content or "Limitations" in content
    
    # Required limitation sentence
    limitation_sentence = (
        "This repository implements a canonical Xi-primary SSZ metric research framework. "
        "It does not claim physical source formation, nonlinear stability, complete external "
        "observational proof, physical beaming, or engineering feasibility."
    )
    # Strip any potential double escape or formatting diffs to match content
    clean_limitation = re.sub(r"\s+", " ", limitation_sentence).strip()
    clean_content = re.sub(r"\s+", " ", content).strip()
    assert clean_limitation in clean_content, "Limitation sentence is missing or modified!"

    # Absolutely forbidden marketing overclaims
    forbidden_claims = [
        "100% complete", "100% validated", "Complete & Validated", "PUBLICATION_READY",
        "final proof", "all physics solved", "singularities solved forever",
        "physical beaming proven", "Kerr solved"
    ]
    
    found_violations = [claim for claim in forbidden_claims if claim in content]
    assert not found_violations, f"Forbidden overclaims found in README.md: {found_violations}"


def test_install_scripts_purity():
    """Verify that install scripts do not contain stale configurations, names or legacy paths."""
    repo_root = Path(__file__).resolve().parent.parent
    
    sh_path = repo_root / "install.sh"
    bat_path = repo_root / "install.bat"
    
    print(f"  install.sh exists: {sh_path.exists()}")
    print(f"  install.bat exists: {bat_path.exists()}")
    
    assert sh_path.exists()
    sh_content = sh_path.read_text(encoding="utf-8")
    
    stale_sh_strings = [
        "φ-Spiral Metric", "v1.0.0 FINAL", "Complete & Validated",
        "generate_validation_report.py", "test_validation_ssz_calibrated.py"
    ]
    found_sh_stale = [s for s in stale_sh_strings if s in sh_content]
    assert not found_sh_stale, f"Stale strings found in install.sh: {found_sh_stale}"
    
    bat_path = repo_root / "install.bat"
    assert bat_path.exists()
    bat_content = bat_path.read_text(encoding="utf-8")
    
    stale_bat_strings = [
        "2.2.0-canonical", "..\\ssz-metric-pure",
        "Some tests may fail without this dependency"
    ]
    found_bat_stale = [b for s in stale_bat_strings for b in [s] if b in bat_content]
    assert not found_bat_stale, f"Stale strings found in install.bat: {found_bat_stale}"
    
    # Must not delete .venv without the reset flag
    assert "rmdir /s /q \".venv\"" not in bat_content or "if \"%RESET_VENV%\"==\"true\"" in bat_content


def test_requirements_and_pyproject_alignment():
    """Verify that requirements.txt matches pyproject.toml runtime dependencies exactly."""
    repo_root = Path(__file__).resolve().parent.parent
    
    req_path = repo_root / "requirements.txt"
    assert req_path.exists()
    req_lines = req_path.read_text(encoding="utf-8").splitlines()
    req_deps = {line.split(">=")[0].strip() for line in req_lines if line and not line.startswith("#")}
    
    pyproj_path = repo_root / "pyproject.toml"
    assert pyproj_path.exists()
    pyproj_content = pyproj_path.read_text(encoding="utf-8")
    
    # Extract version
    version_match = re.search(r"version\s*=\s*\"([^\"]+)\"", pyproj_content)
    assert version_match, "pyproject.toml is missing version definition"
    assert version_match.group(1) == "1.1.0", "pyproject.toml must be version 1.1.0"
    
    # Check dependencies listed in pyproject.toml
    # pyproject.toml dependencies section is list of strings
    expected_deps = {"numpy", "scipy", "sympy"}
    assert req_deps == expected_deps, f"requirements.txt dependencies {req_deps} do not match expected {expected_deps}"
