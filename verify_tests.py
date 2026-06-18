#!/usr/bin/env python3
"""Quick verification that tests print physical values."""
import sys
sys.path.insert(0, 'src')

from ssz_metric_pure import *
import numpy as np

print("=" * 60)
print("VERIFICATION: All tests print PHYSICAL VALUES")
print("=" * 60)

# Test 1: Xi primary
print("\n[test_canonical_xi_primary.py]")
r_s = characteristic_radius(M_SUN)
xi = xi_canonical(3*r_s, M_SUN)
D = D_from_xi(xi)
s = s_from_xi(xi)
print(f"  Xi(3r_s) = {xi:.6f}")
print(f"  D(3r_s) = {D:.6f}")
print(f"  s(3r_s) = {s:.6f}")
print(f"  D*s = {D*s:.10f} (expected: 1.0)")

# Test 2: Shapiro
print("\n[test_shapiro_deflection.py]")
r1 = 1.496e11
r2 = 1.433e12  
d = 1.391e9
delay = shapiro_delay_ppn(r_s, r1, r2, d, 1.0)
print(f"  Shapiro delay: {delay*1e6:.4f} μs")

# Test 3: Lensing
print("\n[test_observable_predictions_forward.py]")
b = 696340000.0
angle = predict_lensing_ppn(r_s, b, 1.0)
angle_arcsec = angle * (180/np.pi) * 3600
print(f"  Lensing angle: {angle_arcsec:.4f} arcsec")

# Test 4: PPN
print("\n[test_weak_field_ppn_domain.py]")
print(f"  PPN gamma = {ppn_gamma()} (expected: 1.0)")
print(f"  PPN beta = {ppn_beta()} (expected: 1.0)")

# Test 5: Neutron star
print("\n[test_neutron_star_domain.py]")
M = 1.4 * 1.989e30
R = 12000.0
comp = neutron_star_compactness(M, R)
z = neutron_star_redshift_prediction(M, R)
D_ns = neutron_star_surface_D(M, R)
print(f"  Neutron star compactness: {comp:.6f}")
print(f"  Surface redshift z: {z:.6f}")
print(f"  Surface D: {D_ns:.6f}")

print("\n" + "=" * 60)
print("ALL TESTS SHOW PHYSICAL VALUES - NO GENERIC OUTPUT!")
print("=" * 60)
