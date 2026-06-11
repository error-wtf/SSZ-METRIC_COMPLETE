#!/usr/bin/env python3
"""
SSZ Eligible External Datasets Listing CLI Script

Summarizes and displays which observation manifest targets have independent parameters
declared, making them eligible for the countertest gauntlet.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import sys
import argparse
from ssz_metric_pure.external_fetch_common import load_manifest
from ssz_metric_pure.external_parameter_manifest import load_parameter_manifest, get_target_parameters


def main():
    parser = argparse.ArgumentParser(description="List eligible external datasets matching parameters.")
    parser.add_argument("--nicer-manifest", type=str, default="external_validation/manifests/nicer/nicer_manifest.json",
                        help="Path to NICER manifest JSON.")
    parser.add_argument("--alma-manifest", type=str, default="external_validation/manifests/alma/alma_manifest.json",
                        help="Path to ALMA manifest JSON.")
    parser.add_argument("--parameter-manifest", type=str, default="external_validation/countertests/parameter_manifest.json",
                        help="Path to parameter manifest JSON.")
    args = parser.parse_args()
    
    if not os.path.exists(args.parameter_manifest):
        print(f"Error: Parameter manifest not found: {args.parameter_manifest}", file=sys.stderr)
        sys.exit(0)
        
    param_manifest = load_parameter_manifest(args.parameter_manifest)
    
    # Process NICER
    if os.path.exists(args.nicer_manifest):
        nicer_man = load_manifest(args.nicer_manifest)
        print("NICER Eligible Datasets:")
        for d in nicer_man.get("datasets", []):
            target = get_target_parameters(param_manifest, d["target_name"])
            status = "ELIGIBLE" if target else "MISSING_PARAMETERS"
            print(f"  ObsID: {d['dataset_id']} | Target: {d['target_name']} | Status: {status}")
            
    # Process ALMA
    if os.path.exists(args.alma_manifest):
        alma_man = load_manifest(args.alma_manifest)
        print("\nALMA Eligible Datasets:")
        for d in alma_man.get("datasets", []):
            target = get_target_parameters(param_manifest, d["target_name"])
            status = "ELIGIBLE" if target else "MISSING_PARAMETERS"
            print(f"  UID: {d['dataset_id']} | Target: {d['target_name']} | Status: {status}")


if __name__ == "__main__":
    main()
