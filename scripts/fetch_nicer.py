#!/usr/bin/env python3
"""
NICER Astroquery Fetch CLI Script

Enables searching, dry-run manifesting, download and checksum verification
for NICER neutron star observation datasets through HEASARC archives.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import sys
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Fetch and manifest public NICER datasets.")
    parser.add_argument("--target", type=str, help="Astronomical object name (resolved via coordinates).")
    parser.add_argument("--ra", type=float, help="RA coordinate in degrees.")
    parser.add_argument("--dec", type=float, help="DEC coordinate in degrees.")
    parser.add_argument("--radius-deg", type=float, default=0.1, help="Search cone radius in degrees.")
    parser.add_argument("--min-exposure", type=float, default=0.0, help="Minimum exposure threshold in seconds.")
    parser.add_argument("--max-rows", type=int, help="Limit observation result rows.")
    parser.add_argument("--manifest", type=str, default="external_validation/manifests/nicer/nicer_manifest.json",
                        help="Target path for manifest JSON.")
    parser.add_argument("--output-dir", type=str, default="external_validation/data/nicer",
                        help="Output directory for downloaded raw files.")
    parser.add_argument("--host", type=str, default="heasarc", choices=["heasarc", "aws", "sciserver"],
                        help="Hosting download server.")
    parser.add_argument("--dry-run", action="store_true", help="Perform simulation and write dry-run policies.")
    parser.add_argument("--search-only", action="store_true", help="Only query metadata catalog, do not write manifest.")
    parser.add_argument("--download", action="store_true", help="Initiate physical file retrieval.")
    parser.add_argument("--confirm-download", action="store_true", help="Explicitly authorize network file transfer.")
    parser.add_argument("--max-gb", type=float, default=5.0, help="Maximum allowed transfer size in GB.")
    parser.add_argument("--verify", action="store_true", help="Execute local directory checksum and size checks.")
    parser.add_argument("--json", action="store_true", help="Print structured CLI dictionary output to stdout.")

    args = parser.parse_args()

    # Dynamic dependency verification before execution
    try:
        from ssz_metric_pure.external_fetch_common import require_external_dependencies
        require_external_dependencies()
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("FETCH: SKIP (missing dependencies)", file=sys.stderr)
        sys.exit(0)

    from ssz_metric_pure.nicer_fetch import (
        search_nicer_observations,
        locate_nicer_data,
        build_nicer_manifest,
        download_nicer_data,
        verify_nicer_download
    )

    if args.verify:
        if not os.path.exists(args.manifest):
            print(f"Error: Manifest not found at {args.manifest}.", file=sys.stderr)
            print("FETCH: SKIP", file=sys.stderr)
            sys.exit(0)
        report = verify_nicer_download(args.output_dir, args.manifest)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Verification completed: status={report['status']}")
            print(f"Verified datasets: {report['verified_datasets']}/{report['total_datasets']}")
        sys.exit(0)

    if args.download:
        if not os.path.exists(args.manifest):
            print(f"Error: Manifest not found at {args.manifest}. Please run search or build manifest first.", file=sys.stderr)
            print("FETCH: FAILED", file=sys.stderr)
            sys.exit(1)
        res = download_nicer_data(
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            host=args.host,
            max_gb=args.max_gb,
            confirm_download=args.confirm_download,
            dry_run=args.dry_run
        )
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"Download completed: status={res['status']}")
            print(f"Downloaded files: {len(res['downloaded_files'])}")
            print(f"FETCH: {res['status']}")
        sys.exit(0)

    # Coordinates payload
    coords = None
    if args.ra is not None and args.dec is not None:
        coords = (args.ra, args.dec)

    if not args.target and coords is None:
        parser.print_help()
        sys.exit(0)

    # Perform search
    print(f"Searching nicermastr catalog for target: {args.target or coords}...")
    try:
        search_res = search_nicer_observations(
            target=args.target,
            coordinates=coords,
            radius_deg=args.radius_deg,
            min_exposure=args.min_exposure,
            max_rows=args.max_rows
        )
    except Exception as e:
        print(f"Search failed: {e}", file=sys.stderr)
        print("FETCH: FAILED", file=sys.stderr)
        sys.exit(1)

    print(f"Found {search_res['count']} matching observation records.")

    if args.search_only:
        if args.json:
            print(json.dumps(search_res, indent=2))
        else:
            for row in search_res["results"]:
                print(f"ObsID: {row.get('obsid') or row.get('OBSID')} | Target: {row.get('name') or row.get('NAME')} | Exposure: {row.get('exposure') or row.get('EXPOSURE')}s")
            print("FETCH: PASS")
        sys.exit(0)

    # Resolve links and build manifest
    print("Locating data download endpoints...")
    links = locate_nicer_data(search_res["results"])
    
    os.makedirs(os.path.dirname(args.manifest), exist_ok=True)
    manifest = build_nicer_manifest(
        table_results=search_res["results"],
        links_results=links,
        target_name=args.target or "UnknownCoords",
        output_path=args.manifest
    )

    print(f"Manifest written successfully to: {args.manifest}")
    if args.json:
        print(json.dumps(manifest, indent=2))
    else:
        print("FETCH: PASS")


if __name__ == "__main__":
    main()
