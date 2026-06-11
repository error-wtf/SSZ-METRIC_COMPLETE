#!/usr/bin/env python3
"""
ALMA Astroquery Fetch CLI Script

Enables searching, dry-run manifesting, download and checksum verification
for ALMA public interferometric files through ALMA science archives.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import sys
import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Fetch and manifest public ALMA datasets.")
    parser.add_argument("--target", type=str, help="Astronomical object name (resolved via coordinates).")
    parser.add_argument("--ra", type=float, help="RA coordinate in degrees.")
    parser.add_argument("--dec", type=float, help="DEC coordinate in degrees.")
    parser.add_argument("--radius-deg", type=float, default=0.02, help="Search cone radius in degrees.")
    parser.add_argument("--project-code", type=str, help="Search by ALMA project code.")
    parser.add_argument("--band", type=str, help="Search by ALMA frequency band.")
    parser.add_argument("--tap-query", type=str, help="Direct Tap query SQL statement.")
    parser.add_argument("--public-only", action="store_true", default=True, help="Include public data rights only.")
    parser.add_argument("--science-only", action="store_true", default=True, help="Include science observations only.")
    parser.add_argument("--max-rows", type=int, help="Limit observation result rows.")
    parser.add_argument("--product-type", type=str, default="fits", choices=["fits", "readme", "tar", "all"],
                        help="Product download type.")
    parser.add_argument("--include-readme", action="store_true", default=True, help="Include readme files.")
    parser.add_argument("--max-files", type=int, help="Limit files filtered.")
    parser.add_argument("--manifest", type=str, default="external_validation/manifests/alma/alma_manifest.json",
                        help="Target path for manifest JSON.")
    parser.add_argument("--output-dir", type=str, default="external_validation/data/alma",
                        help="Output directory for downloaded raw files.")
    parser.add_argument("--cache-dir", type=str, default="external_validation/cache/alma",
                        help="Cache directory.")
    parser.add_argument("--dry-run", action="store_true", help="Perform simulation and write dry-run policies.")
    parser.add_argument("--search-only", action="store_true", help="Only query metadata catalog, do not write manifest.")
    parser.add_argument("--download", action="store_true", help="Initiate physical file retrieval.")
    parser.add_argument("--verify-only", action="store_true", help="Execute local directory integrity checks.")
    parser.add_argument("--confirm-download", action="store_true", help="Explicitly authorize network file transfer.")
    parser.add_argument("--max-gb", type=float, default=10.0, help="Maximum allowed transfer size in GB.")
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

    from ssz_metric_pure.alma_fetch import (
        search_alma_observations,
        extract_alma_uids,
        get_alma_data_info,
        filter_alma_products,
        build_alma_manifest,
        download_alma_products,
        verify_alma_download
    )

    if args.verify_only:
        if not os.path.exists(args.manifest):
            print(f"Error: Manifest not found at {args.manifest}.", file=sys.stderr)
            print("FETCH: SKIP", file=sys.stderr)
            sys.exit(0)
        report = verify_alma_download(args.output_dir, args.manifest)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Verification completed: status={report['status']}")
            print(f"Verified datasets: {report['verified_datasets']}/{report['total_datasets']}")
        sys.exit(0)

    if args.download:
        if not os.path.exists(args.manifest):
            print(f"Error: Manifest not found at {args.manifest}.", file=sys.stderr)
            print("FETCH: FAILED", file=sys.stderr)
            sys.exit(1)
        res = download_alma_products(
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            cache_location=args.cache_dir,
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

    if not args.target and coords is None and not args.project_code and not args.tap_query:
        parser.print_help()
        sys.exit(0)

    # Perform search
    print(f"Searching ALMA catalog...")
    try:
        search_res = search_alma_observations(
            target=args.target,
            coordinates=coords,
            radius_deg=args.radius_deg,
            project_code=args.project_code,
            public_only=args.public_only,
            max_rows=args.max_rows,
            query_tap=args.tap_query
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
            for row in search_res["results"][:10]:
                print(f"UID: {row.get('member_ous_uid')} | Target: {row.get('target_name')} | Project: {row.get('project_code')}")
            print("FETCH: PASS")
        sys.exit(0)

    # Filter files and build manifest
    print("Extracting Member UIDs...")
    uids = extract_alma_uids(search_res["results"])
    print(f"Extracted {len(uids)} unique member UIDs. Locating data info...")
    
    info = get_alma_data_info(uids)
    selected_urls = filter_alma_products(
        data_info=info,
        product_type=args.product_type,
        include_readme=args.include_readme,
        max_files=args.max_files
    )
    print(f"Selected {len(selected_urls)} download URLs based on product_type={args.product_type}.")

    os.makedirs(os.path.dirname(args.manifest), exist_ok=True)
    manifest = build_alma_manifest(
        observation_table=search_res["results"],
        data_info=info,
        selected_urls=selected_urls,
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
