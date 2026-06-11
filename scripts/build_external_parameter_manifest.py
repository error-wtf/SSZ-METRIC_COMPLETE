#!/usr/bin/env python3
"""
SSZ External Parameter Manifest Generator CLI Script

Generates templates or clean parameter manifests declaring independent physical parameters
(M, R, distance, etc.) for targets.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import sys
import argparse
from ssz_metric_pure.external_fetch_common import write_json


def main():
    parser = argparse.ArgumentParser(description="Build independent target physical parameter manifests.")
    parser.add_argument("--template", action="store_true", help="Generate example template structure.")
    parser.add_argument("--output", type=str, default="external_validation/countertests/parameter_manifest.json",
                        help="Target file output path.")
    args = parser.parse_args()
    
    template_data = {
        "schema_version": "1.0",
        "created_utc": "2026-06-11T12:00:00Z",
        "targets": [
            {
                "target_id": "PSR_J0030_0451",
                "target_name": "PSR J0030+0451",
                "target_type": "neutron_star",
                "mass_kg": 1.4 * 1.989e30,
                "mass_solar": 1.4,
                "radius_m": 13000.0,
                "radius_km": 13.0,
                "distance_m": 1.018e19,
                "distance_pc": 330.0,
                "inclination_deg": 45.0,
                "systemic_velocity_km_s": 0.0,
                "reference_frequency_hz": 205.53,
                "position": {
                    "ra_deg": 7.58,
                    "dec_deg": 4.86
                },
                "independent_parameter_sources": [
                    {
                        "parameter": "mass",
                        "source_type": "independent_literature",
                        "citation_or_note": "NICER collaboration reference modeling prior (Riley et al. 2019)",
                        "model_dependency": "none",
                        "allowed_for_hard_gate": True
                    },
                    {
                        "parameter": "radius",
                        "source_type": "independent_literature",
                        "citation_or_note": "NICER collaboration reference modeling prior (Riley et al. 2019)",
                        "model_dependency": "none",
                        "allowed_for_hard_gate": True
                    }
                ],
                "allowed_observable_tests": [
                    "nicer_surface_redshift_proxy",
                    "nicer_clock_phase_proxy"
                ],
                "comparison_mode_preference": "EXACT_DERIVED_OBSERVABLE_MODE",
                "limitations": [
                    "model-dependent neutron star mass/radius parameters",
                    "spherical configuration assumed"
                ]
            },
            {
                "target_id": "M87_STAR",
                "target_name": "M87",
                "target_type": "compact_object",
                "mass_kg": 6.5e9 * 1.989e30,
                "mass_solar": 6.5e9,
                "radius_m": 1.919e13,
                "radius_km": 1.919e10,
                "distance_m": 5.184e23,
                "distance_pc": 1.68e7,
                "inclination_deg": 17.0,
                "systemic_velocity_km_s": 1300.0,
                "reference_frequency_hz": 230e9,
                "position": {
                    "ra_deg": 187.7,
                    "dec_deg": 12.3
                },
                "independent_parameter_sources": [
                    {
                        "parameter": "mass",
                        "source_type": "independent_literature",
                        "citation_or_note": "Event Horizon Telescope collaboration (Akiyama et al. 2019)",
                        "model_dependency": "none",
                        "allowed_for_hard_gate": True
                    }
                ],
                "allowed_observable_tests": [
                    "alma_frequency_shift",
                    "alma_line_velocity_proxy",
                    "alma_phase_path_integral",
                    "alma_light_travel_time"
                ],
                "comparison_mode_preference": "EXACT_DERIVED_OBSERVABLE_MODE",
                "limitations": [
                    "assumes central black hole mass scale standard references"
                ]
            }
        ]
    }
    
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    write_json(args.output, template_data)
    print(f"Parameter manifest template written successfully to: {args.output}")


if __name__ == "__main__":
    main()
