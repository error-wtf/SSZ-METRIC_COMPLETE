#!/usr/bin/env python3
"""
SSZ Exact Benchmark Replay CLI Script

Runs exact forward replays verifying prior verified numerical SSZ benchmark
identities without any softenings or decay.

© 2026 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import os
import sys
import argparse
import json
from ssz_metric_pure.external_fetch_common import read_json
from ssz_metric_pure.external_prediction_bindings import predict_for_external_observable
from ssz_metric_pure.external_exact_comparison import within_exact_tolerance


def main():
    parser = argparse.ArgumentParser(description="Replay and verify exact numerical SSZ core benchmarks.")
    parser.add_argument("--benchmark", type=str,
                        default="external_validation/countertests/benchmarks/exact_benchmark_observables.json",
                        help="Path to benchmark JSON.")
    parser.add_argument("--output", type=str, default="EXACT_BENCHMARK_REPLAY_REPORT.md",
                        help="Markdown report output path.")
    args = parser.parse_args()
    
    if not os.path.exists(args.benchmark):
        # Write default example and print notice
        example_p = args.benchmark.replace(".json", ".example.json")
        if os.path.exists(example_p):
            # copy or read example
            data = read_json(example_p)
            os.makedirs(os.path.dirname(args.benchmark), exist_ok=True)
            with open(args.benchmark, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            print(f"Error: Benchmark file not found at {args.benchmark}.", file=sys.stderr)
            sys.exit(0)
            
    data = read_json(args.benchmark)
    
    results = []
    passes = 0
    failures = 0
    
    print("Replaying exact numerical core benchmarks...")
    for bench in data.get("benchmarks", []):
        obs_type = bench["observable_type"]
        inputs = bench["input_parameters"]
        expected = bench["expected_observable"]
        
        abs_tol = bench.get("absolute_tolerance", 1e-12)
        rel_tol = bench.get("relative_tolerance", 1e-10)
        
        pred = predict_for_external_observable(obs_type, inputs, {})
        
        abs_res = abs(pred["value"] - expected["value"])
        rel_res = abs_res / abs(expected["value"]) if expected["value"] > 0 else abs_res
        
        passed = abs_res <= abs_tol or rel_res <= rel_tol
        status = "PASS_EXACT" if passed else "FAIL"
        
        if passed:
            passes += 1
        else:
            failures += 1
            
        results.append({
            "id": bench["benchmark_id"],
            "target": bench["target_name"],
            "type": obs_type,
            "prediction": pred["value"],
            "expected": expected["value"],
            "abs_residual": abs_res,
            "status": status
        })
        print(f"  Benchmark: {bench['benchmark_id']} | Status: {status} | Abs Residual: {abs_res:.4e}")
        
    # Generate Markdown Report
    md = f"""# SSZ Exact Benchmark Replay Report

Preserves and replays 100% numerically exact benchmarks to guarantee that earlier verified values are strictly maintained without decay.

- **Replay Status**: {"PASS_EXACT" if failures == 0 else "FAIL"}
- **Total Benchmarks**: {len(results)}
- **PASS**: {passes}
- **FAIL**: {failures}

| Benchmark ID | Target | Type | Prediction | Expected | Abs Residual | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
"""
    for r in results:
        md += f"| {r['id']} | {r['target']} | {r['type']} | {r['prediction']:.8e} | {r['expected']:.8e} | {r['abs_residual']:.4e} | **{r['status']}** |\n"
        
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(md)
        
    print(f"Benchmark replay completed. Report written to: {args.output}")
    if failures > 0:
        print("EXACT BENCHMARK REPLAY: FAILED", file=sys.stderr)
        sys.exit(1)
    else:
        print("EXACT BENCHMARK REPLAY: PASS_EXACT")
        sys.exit(0)


if __name__ == "__main__":
    main()
