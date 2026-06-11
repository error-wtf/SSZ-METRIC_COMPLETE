"""
SSZ Repository Consistency Engine

Utility to programmatically ensure that no forbidden GR or Kerr scaffolding
has crept into the pure core package files.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import re
from pathlib import Path


def verify_core_purity() -> bool:
    """
    Check all active core files in the pure core package for forbidden terms.
    """
    forbidden_terms = [
        "Kerr", "Boyer", "Boyer-Lindquist", "Schwarzschild", "Sigma", "Delta", "ergosphere",
        "r_plus", "r_minus", "g_tphi", "A_GR", "1 - r_s/r", "1-r_s/r", "metric_kerr", "KerrSSZ", "SSZKerr"
    ]
    
    repo_root = Path(__file__).resolve().parent.parent.parent
    core_dir = repo_root / "ssz_metric_pure"
    
    regex = re.compile("|".join(re.escape(term) for term in forbidden_terms), re.IGNORECASE)
    
    core_files = ["core.py", "metric.py", "tensor.py", "observables.py", "validation.py", "segmentation.py"]
    
    for file_name in core_files:
        path = core_dir / file_name
        if path.exists():
            content = path.read_text(encoding="utf-8")
            # Strip comments and docstrings
            content = re.sub(r'#.*', '', content)
            content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
            
            if regex.search(content):
                return False
                
    return True
