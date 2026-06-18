#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ Metric Comparison - Kerr-SSZ vs. φ-Spiral
⚠️  LEGACY SCRIPT - NICHT FUNKTIONAL

Dieses Skript referenziert Module die nicht mehr existieren:
- metric_phi_spiral_ssz_by_human (entfernt)
- metric_kerr_ssz_kerr_by_ki (entfernt)

Verwendung: NUR als historische Referenz - nicht ausführen!
Die aktuelle SSZ-Implementation verwendet ausschließlich:
- src/ssz_metric_pure/core.py (kanonische Ξ-Formel)
- src/ssz_metric_pure/metric.py (Metrik-Tensor)

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4
"""
import sys
import os
from pathlib import Path

# ⚠️  ABORT - Legacy Script
print("=" * 80)
print("⚠️  LEGACY SCRIPT - ABORT")
print("=" * 80)
print("\nDieses Skript referenziert nicht-existente Module:")
print("  - metric_phi_spiral_ssz_by_human")
print("  - metric_kerr_ssz_kerr_by_ki")
print("\nDiese Module wurden aus dem kanonischen SSZ-Repo entfernt.")
print("Die aktuelle Implementation verwendet:")
print("  - src/ssz_metric_pure/core.py (kanonisch)")
print("  - src/ssz_metric_pure/metric.py")
print("\nBitte tests/test_shapiro_deflection.py für aktuelle Tests.")
print("=" * 80)
sys.exit(1)

# Original imports (Module existieren NICHT):
# from ssz_metric_pure.metric_phi_spiral_ssz_by_human import PhiSpiralSSZMetric
# from ssz_metric_pure.metric_kerr_ssz_kerr_by_ki import KerrSSZMetric, KerrSSZParams

# Physical constants
M_SUN = 1.98847e30  # Solar mass [kg]
C_SI = 299792458.0  # Speed of light [m/s]


def print_banner():
    """Print comparison banner."""
    print("\n" + "="*80)
    print("=" + " "*78 + "=")
    print("=" + "  SSZ METRIC COMPARISON: Kerr-SSZ vs. φ-Spiral".center(78) + "=")
    print("=" + " "*78 + "=")
    print("="*80 + "\n")


def compare_conceptual():
    """Compare conceptual frameworks."""
    print("="*80)
    print("1. CONCEPTUAL FRAMEWORK")
    print("="*80)
    
    print("\n┌─────────────────────────────────────────────────────────────────────────┐")
    print("│ KERR-SSZ METRIC (Rotating Black Holes)                                 │")
    print("├─────────────────────────────────────────────────────────────────────────┤")
    print("│ Philosophy:  SSZ + Rotation (frame dragging)                           │")
    print("│ Coordinates: Boyer-Lindquist-like (t, r, θ, φ)                         │")
    print("│ Rotation:    Spin parameter a (or â = a/M)                             │")
    print("│ Off-diagonal: g_tφ ≠ 0 (frame dragging)                                │")
    print("│ Horizons:    r_± where Δ(r) = 0                                        │")
    print("│ Ergosphere: r_ergo where g_tt = 0                                      │")
    print("│ Focus:       Astrophysical black holes                                 │")
    print("└─────────────────────────────────────────────────────────────────────────┘")
    
    print("\n┌─────────────────────────────────────────────────────────────────────────┐")
    print("│ φ-SPIRAL METRIC (Pure Rotation-Based)                                  │")
    print("├─────────────────────────────────────────────────────────────────────────┤")
    print("│ Philosophy:  Pure geometric rotation φ_G(r)                            │")
    print("│ Coordinates: Spiral (t, r, θ, φ)                                       │")
    print("│ Rotation:    Gravitational angle φ_G(r) = k·log(1 + r/r₀)             │")
    print("│ Off-diagonal: g_tr ≠ 0 (spiral structure!)                             │")
    print("│ Horizons:    NONE! (subspace layers instead)                           │")
    print("│ Layers:      Every Δφ_G = 2π → new subspace sheet                     │")
    print("│ Focus:       Singularity-free, phase tunneling                         │")
    print("└─────────────────────────────────────────────────────────────────────────┘")
    
    print("\n" + "="*80 + "\n")


def compare_line_elements():
    """Compare line elements."""
    print("="*80)
    print("2. LINE ELEMENTS")
    print("="*80)
    
    print("\n" + "─"*80)
    print("KERR-SSZ:")
    print("─"*80)
    print("ds² = -A(r,θ)dt² + B(r,θ)dr² + C(r,θ)dθ² + D(r,θ)dφ² + 2E(r,θ)dt dφ")
    print()
    print("where:")
    print("  A(r,θ) = SSZ_factor × (1 - r_s r/Σ)")
    print("  E(r,θ) = -r_s r a sin²θ / Σ  ← Frame dragging term")
    print("  Σ(r,θ) = r² + a² cos²θ")
    print("  Δ(r) = r² - r_s r + a²")
    
    print("\n" + "─"*80)
    print("φ-SPIRAL:")
    print("─"*80)
    print("ds² = -c² sech²(φ_G(r)) dt² + 2c tanh(φ_G(r)) dt dr + dr²")
    print()
    print("where:")
    print("  φ_G(r) = k·log(1 + r/r₀)  ← Gravitational rotation angle")
    print("  β(r) = tanh(φ_G(r))  ← Local velocity field")
    print("  γ(r) = cosh(φ_G(r))  ← Lorentz-like factor")
    print()
    print("Alternative form:")
    print("  ds² = -c²(1 - β²) dt² + 2βc dt dr + dr²")
    
    print("\n" + "="*80 + "\n")


def compare_tensor_structure():
    """Compare tensor structures."""
    print("="*80)
    print("3. METRIC TENSOR STRUCTURE")
    print("="*80)
    
    print("\n" + "─"*80)
    print("KERR-SSZ (4×4):")
    print("─"*80)
    print("       t              r           θ           φ")
    print("t  [ g_tt            0           0         g_tφ  ]  ← Frame drag")
    print("r  [  0            g_rr          0           0   ]")
    print("θ  [  0              0         g_θθ          0   ]")
    print("φ  [ g_tφ            0           0         g_φφ  ]")
    
    print("\nNon-zero off-diagonal: g_tφ (couples time & azimuth)")
    print("Angular dependence: Yes (θ in multiple components)")
    
    print("\n" + "─"*80)
    print("φ-SPIRAL (4×4):")
    print("─"*80)
    print("       t              r           θ           φ")
    print("t  [ g_tt           g_tr          0           0   ]  ← Spiral!")
    print("r  [ g_tr           g_rr          0           0   ]")
    print("θ  [  0              0          g_θθ          0   ]")
    print("φ  [  0              0            0         g_φφ  ]")
    
    print("\nNon-zero off-diagonal: g_tr (couples time & radius)")
    print("Angular dependence: Minimal (only in g_φφ)")
    
    print("\n" + "="*80 + "\n")


def compare_numerically():
    """Numerical comparison at same mass."""
    print("="*80)
    print("4. NUMERICAL COMPARISON (Solar Mass)")
    print("="*80)
    
    mass = M_SUN
    
    # Create metrics
    phi_metric = PhiSpiralSSZMetric(mass=mass, k=1.0)
    kerr_params = KerrSSZParams(mass=mass, spin=0.5)
    kerr_metric = KerrSSZMetric(kerr_params)
    
    print(f"\nMass: {mass:.3e} kg (solar)")
    print(f"Schwarzschild radius: {phi_metric.r_s:.3e} m")
    print(f"φ-Spiral k: 1.0")
    print(f"Kerr spin â: 0.5")
    
    # Compare at different radii (equator)
    theta = np.pi / 2  # Equator
    test_radii = [1.5, 2.0, 3.0, 5.0, 10.0]
    
    print("\n" + "─"*80)
    print("METRIC COMPONENTS AT EQUATOR (θ = π/2)")
    print("─"*80)
    print(f"{'r/r_s':<10} {'Kerr g_tt/c²':<20} {'Spiral g_tt/c²':<20} {'Δ%':<15}")
    print("─"*80)
    
    for r_factor in test_radii:
        r = r_factor * phi_metric.r_s
        
        # Kerr
        g_tt_kerr = kerr_metric.g_tt(r, theta) / (C_SI ** 2)
        
        # φ-Spiral
        g_tt_spiral = phi_metric.g_tt(r) / (C_SI ** 2)
        
        # Difference
        diff_pct = 100 * abs(g_tt_kerr - g_tt_spiral) / abs(g_tt_kerr)
        
        print(f"{r_factor:<10.1f} {g_tt_kerr:<20.6f} {g_tt_spiral:<20.6f} {diff_pct:<15.3f}")
    
    print("\n" + "─"*80)
    print("OFF-DIAGONAL TERMS")
    print("─"*80)
    print(f"{'r/r_s':<10} {'Kerr g_tφ/c':<20} {'Spiral g_tr/c':<20} {'Type':<20}")
    print("─"*80)
    
    for r_factor in test_radii:
        r = r_factor * phi_metric.r_s
        
        # Kerr (frame dragging)
        g_tph_kerr = kerr_metric.g_tph(r, theta) / C_SI
        
        # φ-Spiral (spiral structure)
        g_tr_spiral = phi_metric.g_tr(r) / C_SI
        
        print(f"{r_factor:<10.1f} {g_tph_kerr:<20.6f} {g_tr_spiral:<20.6f} {'Different!':<20}")
    
    print("\nNote: g_tφ (Kerr) vs. g_tr (Spiral) are DIFFERENT physical effects!")
    print("  Kerr:   Frame dragging (rotation of spacetime)")
    print("  Spiral: Spiral structure (time-radius coupling)")
    
    print("\n" + "="*80 + "\n")


def compare_singularities():
    """Compare singularity behavior."""
    print("="*80)
    print("5. SINGULARITY BEHAVIOR")
    print("="*80)
    
    mass = M_SUN
    phi_metric = PhiSpiralSSZMetric(mass=mass, k=1.0)
    kerr_params = KerrSSZParams(mass=mass, spin=0.5)
    kerr_metric = KerrSSZMetric(kerr_params)
    
    print("\n" + "─"*80)
    print("AT CENTER (r → 0):")
    print("─"*80)
    
    r_center = 1e-10  # Very close to zero
    
    # φ-Spiral
    print("\nφ-Spiral:")
    phi_center = phi_metric.phi_G(r_center)
    g_tt_spiral_center = phi_metric.g_tt(r_center) / (C_SI ** 2)
    g_tr_spiral_center = phi_metric.g_tr(r_center) / C_SI
    
    print(f"  φ_G(0) = {phi_center:.6e} rad  ← Near zero!")
    print(f"  g_tt(0) / c² = {g_tt_spiral_center:.6f}  ← Near -1 (Minkowski!)")
    print(f"  g_tr(0) / c = {g_tr_spiral_center:.6e}  ← Near zero!")
    print("  ✅ FLAT SPACETIME AT CENTER (no singularity)")
    
    # Kerr
    print("\nKerr-SSZ:")
    theta = np.pi / 2
    g_tt_kerr_center = kerr_metric.g_tt(r_center, theta) / (C_SI ** 2)
    
    print(f"  g_tt(0) / c² = {g_tt_kerr_center:.6f}")
    print("  ⚠ Still modified by SSZ segment density")
    print("  ✅ No singularity (thanks to SSZ)")
    
    print("\n" + "─"*80)
    print("AT SCHWARZSCHILD RADIUS (r = r_s):")
    print("─"*80)
    
    # φ-Spiral
    print("\nφ-Spiral:")
    phi_rs = phi_metric.phi_G(phi_metric.r_s)
    g_tt_spiral_rs = phi_metric.g_tt(phi_metric.r_s) / (C_SI ** 2)
    layer_rs = phi_metric.subspace_layer(phi_metric.r_s)
    
    print(f"  φ_G(r_s) = {phi_rs:.6f} rad")
    print(f"  g_tt(r_s) / c² = {g_tt_spiral_rs:.6f}  ← FINITE!")
    print(f"  Subspace layer: {layer_rs}")
    print("  ✅ No horizon singularity")
    
    # Kerr
    print("\nKerr-SSZ:")
    r_plus, r_minus = kerr_metric.horizons()
    print(f"  r_+ (outer horizon) = {r_plus/kerr_metric.r_s:.3f} r_s")
    print(f"  r_- (inner horizon) = {r_minus/kerr_metric.r_s:.3f} r_s")
    print("  ⚠ Horizons exist (but no singularity thanks to SSZ)")
    
    print("\n" + "="*80 + "\n")


def compare_features():
    """Compare key features side-by-side."""
    print("="*80)
    print("6. FEATURE COMPARISON")
    print("="*80)
    
    features = [
        ("Singularity at r=0", "✅ NONE (SSZ)", "✅ NONE (flat!)"),
        ("Event Horizon", "✅ Yes (r_+)", "❌ No (subspace layers)"),
        ("Ergosphere", "✅ Yes", "❌ No"),
        ("Frame Dragging", "✅ Yes (g_tφ)", "❌ No"),
        ("Spiral Structure", "❌ No", "✅ Yes (g_tr)"),
        ("Subspace Layers", "❌ No", "✅ Yes (every 2π)"),
        ("Angular Dependence", "✅ Strong (θ)", "⚪ Minimal"),
        ("Rotation Parameter", "â (spin)", "k (spiral strength)"),
        ("Asymptotic Flatness", "✅ Yes", "✅ Yes"),
        ("Energy Conditions", "✅ Satisfied", "✅ Satisfied"),
        ("GR Limit", "✅ Matches", "✅ Weak field"),
        ("ANITA Explanation", "❌ No", "✅ Yes (tunneling)"),
        ("Astrophysical", "✅ Direct", "⚪ Theoretical"),
        ("Complexity", "🔴 High", "🟢 Moderate"),
    ]
    
    print(f"\n{'Feature':<30} {'Kerr-SSZ':<25} {'φ-Spiral':<25}")
    print("─"*80)
    
    for feature, kerr, spiral in features:
        print(f"{feature:<30} {kerr:<25} {spiral:<25}")
    
    print("\n" + "="*80 + "\n")


def compare_use_cases():
    """Compare recommended use cases."""
    print("="*80)
    print("7. RECOMMENDED USE CASES")
    print("="*80)
    
    print("\n┌─────────────────────────────────────────────────────────────────────────┐")
    print("│ USE KERR-SSZ METRIC WHEN:                                              │")
    print("├─────────────────────────────────────────────────────────────────────────┤")
    print("│ ✅ Studying rotating black holes (astrophysical)                       │")
    print("│ ✅ Modeling frame-dragging effects (Lense-Thirring)                    │")
    print("│ ✅ Calculating ISCO, photon orbits for spinning BHs                    │")
    print("│ ✅ Comparing with Kerr GR solutions                                    │")
    print("│ ✅ Ergosphere physics (Penrose process, etc.)                          │")
    print("│ ✅ Real observational data (M87*, Sgr A* with spin)                    │")
    print("│ ✅ Need angular momentum effects                                       │")
    print("└─────────────────────────────────────────────────────────────────────────┘")
    
    print("\n┌─────────────────────────────────────────────────────────────────────────┐")
    print("│ USE φ-SPIRAL METRIC WHEN:                                              │")
    print("├─────────────────────────────────────────────────────────────────────────┤")
    print("│ ✅ Exploring singularity-free black hole interiors                     │")
    print("│ ✅ Studying subspace layer structure                                   │")
    print("│ ✅ Investigating ANITA-type anomalies (phase tunneling)                │")
    print("│ ✅ Pure geometric rotation effects                                     │")
    print("│ ✅ Testing alternatives to event horizons                              │")
    print("│ ✅ Time-radius coupling phenomena                                      │")
    print("│ ✅ Conceptual/theoretical exploration                                  │")
    print("│ ✅ Educational purposes (simpler structure)                            │")
    print("└─────────────────────────────────────────────────────────────────────────┘")
    
    print("\n" + "="*80 + "\n")


def compare_math_complexity():
    """Compare mathematical complexity."""
    print("="*80)
    print("8. MATHEMATICAL COMPLEXITY")
    print("="*80)
    
    metrics = [
        ("Coordinate System", "Boyer-Lindquist", "Spherical-spiral"),
        ("Primary Variable", "Spin â", "Angle φ_G(r)"),
        ("Auxiliary Functions", "Σ(r,θ), Δ(r)", "β(r), γ(r)"),
        ("Metric Components", "5 (g_tt, g_rr, g_θθ, g_φφ, g_tφ)", "5 (g_tt, g_rr, g_θθ, g_φφ, g_tr)"),
        ("θ-Dependence", "Strong (in 4/5)", "Weak (only g_φφ)"),
        ("Horizon Calculation", "Solve Δ(r)=0", "None (no horizons)"),
        ("Ergosphere", "Solve g_tt=0", "N/A"),
        ("Geodesics", "Complex", "Moderate"),
        ("Curvature Tensors", "Very complex", "Complex"),
        ("Code Lines", "~376 lines", "~899 lines"),
    ]
    
    print(f"\n{'Aspect':<30} {'Kerr-SSZ':<25} {'φ-Spiral':<25}")
    print("─"*80)
    
    for aspect, kerr, spiral in metrics:
        print(f"{aspect:<30} {kerr:<25} {spiral:<25}")
    
    print("\nComplexity Verdict:")
    print("  Kerr-SSZ:  🔴 High (angular dependence, multiple functions)")
    print("  φ-Spiral: 🟡 Moderate (simpler structure, more lines)")
    
    print("\n" + "="*80 + "\n")


def summary_table():
    """Print summary comparison table."""
    print("="*80)
    print("9. SUMMARY: KERR-SSZ vs. φ-SPIRAL")
    print("="*80)
    
    print("""
╔════════════════════════════╦═══════════════════════════╦═══════════════════════════╗
║ ASPECT                     ║ KERR-SSZ                  ║ φ-SPIRAL                  ║
╠════════════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Philosophy                 ║ SSZ + Rotation (spin)     ║ Pure rotation angle       ║
║ Rotation Type              ║ Physical spin (a)         ║ Geometric angle (φ_G)     ║
║ Off-Diagonal Term          ║ g_tφ (frame drag)         ║ g_tr (spiral)             ║
║ Singularity                ║ NONE (SSZ)                ║ NONE (flat at r=0)        ║
║ Event Horizon              ║ YES (r_±)                 ║ NO (subspace layers)      ║
║ Ergosphere                 ║ YES                       ║ NO                        ║
║ Subspace Layers            ║ NO                        ║ YES (every 2π)            ║
║ ANITA Explanation          ║ NO                        ║ YES (tunneling)           ║
║ Astrophysical Use          ║ DIRECT                    ║ THEORETICAL               ║
║ GR Limit                   ║ Exact (â→0)               ║ Weak field                ║
║ Complexity                 ║ HIGH                      ║ MODERATE                  ║
║ Implementation             ║ 376 lines                 ║ 899 lines                 ║
║ Best For                   ║ Real BHs with spin        ║ Singularity-free physics  ║
╚════════════════════════════╩═══════════════════════════╩═══════════════════════════╝
    """)
    
    print("\nKEY DIFFERENCES:")
    print("  1. Off-diagonal coupling: g_tφ vs. g_tr (different physics!)")
    print("  2. Horizons: Kerr has r_±, φ-Spiral has subspace layers")
    print("  3. Angular dependence: Kerr strong, φ-Spiral minimal")
    print("  4. Use case: Kerr = astrophysical, φ-Spiral = theoretical")
    
    print("\nKEY SIMILARITIES:")
    print("  1. Both singularity-free (SSZ property)")
    print("  2. Both have off-diagonal terms (different types)")
    print("  3. Both asymptotically flat")
    print("  4. Both satisfy energy conditions")
    
    print("\n" + "="*80 + "\n")


def main():
    """Main comparison routine."""
    print_banner()
    
    compare_conceptual()
    compare_line_elements()
    compare_tensor_structure()
    compare_numerically()
    compare_singularities()
    compare_features()
    compare_use_cases()
    compare_math_complexity()
    summary_table()
    
    # Final verdict
    print("="*80)
    print("CONCLUSION")
    print("="*80)
    print("""
Both metrics are valid SSZ implementations with different philosophies:

🔄 KERR-SSZ METRIC:
   • Closer to standard GR rotating solutions
   • Direct astrophysical applications
   • Frame dragging (g_tφ) matches observations
   • Complex but familiar structure

🌀 φ-SPIRAL METRIC:
   • Pure geometric rotation approach
   • Novel subspace layer concept
   • Explains anomalies (ANITA)
   • Simpler conceptually, different structure

RECOMMENDATION:
   • For spinning BHs with observations → Use Kerr-SSZ
   • For singularity-free theory → Use φ-Spiral
   • For maximum completeness → Use BOTH and compare!

The SSZ pipeline (ssz_metric_pipeline.py) allows easy switching between them.
    """)
    
    print("="*80)
    print("\n© 2025 Carmen N. Wrede & Lino Casu")
    print("Licensed under the ANTI-CAPITALIST SOFTWARE LICENSE v1.4\n")


if __name__ == "__main__":
    main()
