"""
Test of strict isolation of the SSZ-Core package.

Guarantees that no forbidden General Relativity, Schwarzschild, or Kerr Boyer-Lindquist
scaffolding terms or functions are present in the core package source files.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import re
from pathlib import Path

def strip_comments_and_docstrings(source: str) -> str:
    """Remove comments and docstrings from Python source code."""
    # Remove single line comments
    source = re.sub(r'#.*', '', source)
    # Remove triple-quoted strings (docstrings)
    source = re.sub(r'""".*?"""', '', source, flags=re.DOTALL)
    source = re.sub(r"'''.*?'''", '', source, flags=re.DOTALL)
    return source

def test_no_kerr_in_core():
    """Verify that forbidden GR/Kerr scaffolding words are completely absent from core files."""
    forbidden_terms = [
        "Kerr", "Boyer", "Boyer-Lindquist", "Schwarzschild", "Sigma", "Delta", "ergosphere",
        "r_plus", "r_minus", "g_tphi", "A_GR", "1 - r_s/r", "1-r_s/r", "metric_kerr", "KerrSSZ", "SSZKerr"
    ]
    
    # Use portable relative path
    repo_root = Path(__file__).resolve().parent.parent
    core_dir = repo_root / "src" / "ssz_metric_pure"
    
    # Compile checking regex (case-insensitive)
    regex = re.compile("|".join(re.escape(term) for term in forbidden_terms), re.IGNORECASE)
    
    violations = []
    
    # We scan all canonical core files
    core_files = ["core.py", "metric.py", "tensor.py", "observables.py", "validation.py"]
    
    for file_name in core_files:
        path = core_dir / file_name
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Strip comments and docstrings before checking purity
            cleaned_content = strip_comments_and_docstrings(content)
            
            # Look for matches
            matches = regex.findall(cleaned_content)
            if matches:
                violations.append((file_name, list(set(matches))))
                
    print(f"  Scanned {len(core_files)} core files for forbidden terms")
    print(f"  Violations found: {len(violations)}")
    assert not violations, f"Forbidden GR/Kerr scaffolds found in pure core executive code: {violations}"
