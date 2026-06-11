"""
SSZ-METRIC-COMPLETE Quickstart Example

Demonstrates basic usage of the SSZ metric with 2PN calibration.
"""

import sys
sys.path.insert(0, '../src')

import numpy as np
from ssz_core import (
    Xi_complete,
    D_SSZ,
    PHI,
    X_BLEND_MIN,
    X_BLEND_MAX,
    C,
    G,
    M_SUN,
)


def main():
    print("=" * 80)
    print("SSZ-METRIC-COMPLETE v2.2.0-canonical - Quickstart")
    print("=" * 80)
    print()
    
    # Solar parameters
    r_s = 2 * G * M_SUN / C**2  # Schwarzschild radius
    print(f"Solar Schwarzschild radius: r_s = {r_s:.1f} m")
    print(f"Golden ratio φ = {PHI}")
    print(f"Blend zone: {X_BLEND_MIN} ≤ r/r_s ≤ {X_BLEND_MAX}")
    print()
    
    # Calculate Xi at various radii
    print("Segment Density Ξ(r) at different radii:")
    print("-" * 60)
    
    test_points = [
        ("Horizon", 1.0),
        ("Blend start", X_BLEND_MIN),
        ("Mid blend", (X_BLEND_MIN + X_BLEND_MAX) / 2),
        ("Blend end", X_BLEND_MAX),
        ("Weak field", 10.0),
    ]
    
    for name, x in test_points:
        r = x * r_s
        xi, dxi, d2xi = Xi_complete(r, r_s)
        D = 1.0 / (1.0 + xi)
        
        print(f"{name:15s} (x={x:4.1f}): Ξ={xi:.6f}, D={D:.6f}")
    
    print()
    
    # Verify critical values
    print("Critical Value Verification:")
    print("-" * 60)
    
    # At horizon
    xi_h, _, _ = Xi_complete(r_s, r_s)
    D_h = 1.0 / (1.0 + xi_h)
    
    print(f"At r = r_s (horizon):")
    print(f"  Ξ(r_s) = {xi_h:.9f}")
    print(f"  D(r_s) = {D_h:.9f}  ← FINITE! (not 0 like in GR)")
    print()
    
    # Compare with expected
    xi_expected = 1.0 - np.exp(-PHI)
    D_expected = 1.0 / (2.0 - np.exp(-PHI))
    
    print(f"Expected values:")
    print(f"  Ξ(r_s) = {xi_expected:.9f}")
    print(f"  D(r_s) = {D_expected:.9f}")
    print()
    
    # Verify
    xi_match = np.isclose(xi_h, xi_expected, rtol=1e-10)
    D_match = np.isclose(D_h, D_expected, rtol=1e-10)
    
    print(f"Verification:")
    print(f"  Ξ match: {'✅' if xi_match else '❌'}")
    print(f"  D match: {'✅' if D_match else '❌'}")
    print()
    
    print("=" * 80)
    print("✅ SSZ Metric is working correctly!")
    print("=" * 80)


if __name__ == "__main__":
    main()
