"""
Rigorous Code Scanning Test for Banned Fitting Terms.

Verifies that no curve fitting, least-squares, parameter tuning, polyfit, or regression
is used inside the canonical validation pipelines.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import re
import pytest


def test_no_fitting_terms_in_canonical_paths():
    """Scan canonical source files and tests to assert zero usage of banned fitting terms."""
    banned_terms = [
        "curve_fit", "least_squares", "polyfit", "linregress", "minimize",
        "differential_evolution", "lmfit", "sklearn", "fit_params",
        "optimize_to_match", "tune_to_data", "calibrate_from_observed"
    ]
    
    scan_dirs = ["src/ssz_metric_pure", "tests"]
    violations = []
    
    for s_dir in scan_dirs:
        # Resolve path absolute
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", s_dir))
        if not os.path.exists(base_path):
            continue
            
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    # Ignore files defining or verifying the ban to prevent self-matching!
                    if "test_no_fitting_in_canonical_validation.py" in file or "forward_protocol.py" in file:
                        continue
                        
                    with open(filepath, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        
                    for idx, line in enumerate(lines, 1):
                        # Ignore comment lines and lines in testing checks
                        if line.strip().startswith("#"):
                            continue
                        for term in banned_terms:
                            if re.search(r"\b" + re.escape(term) + r"\b", line):
                                violations.append(f"{file}:{idx} - Term: {term} - {line.strip()}")
                                
    print(f"  Scanned for banned fitting terms")
    print(f"  Violations found: {len(violations)}")
    assert len(violations) == 0, f"Banned fitting terms detected in canonical files:\n" + "\n".join(violations)
