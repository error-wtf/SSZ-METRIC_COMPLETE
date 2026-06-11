#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metric Compatibility Check - φ-Spiral SSZ Metric

Verifies that ∇_a g_bc = 0 (metric compatibility)
and computes the Riemann curvature tensor to show it depends
only on φ_G rotation, not classical GR curvature.

Requires: sympy

© 2025 Carmen N. Wrede & Lino Casu
"""
import sympy as sp
from sympy import symbols, Function, diff, simplify, sqrt, cosh, sinh, tanh
import sys

print("\n" + "="*80)
print("METRIC COMPATIBILITY CHECK - φ-Spiral SSZ")
print("="*80)

# Define symbols
r, T = symbols('r T', real=True)
c = symbols('c', positive=True)

# Define φ_G(r) as a function
phiG = Function('phiG')(r)

# Metric functions
gamma = cosh(phiG)
beta = tanh(phiG)
sech2 = 1 / gamma**2

print("\nMetric in diagonal (T,r) form:")
print("  g_TT = -c²/γ² = -c²·sech²(φ_G)")
print("  g_rr = γ² = cosh²(φ_G)")
print("  g_Tr = 0 (diagonal!)")

# Metric tensor (2D: T, r)
g = sp.Matrix([
    [-c**2 / gamma**2, 0],
    [0, gamma**2]
])

print("\nMetric tensor g_μν:")
sp.pprint(g)

# Inverse metric
g_inv = g.inv()

print("\nInverse metric g^μν:")
sp.pprint(g_inv)

# Coordinate array
coords = [T, r]

# ========================================================================
# CHRISTOFFEL SYMBOLS
# ========================================================================
print("\n" + "="*80)
print("CHRISTOFFEL SYMBOLS")
print("="*80)

Gamma = [[[0 for _ in range(2)] for _ in range(2)] for _ in range(2)]

# Compute Christoffel symbols: Γ^ρ_μν = (1/2) g^ρσ (∂_μ g_νσ + ∂_ν g_μσ - ∂_σ g_μν)
for rho in range(2):
    for mu in range(2):
        for nu in range(2):
            Gamma[rho][mu][nu] = sp.Rational(1, 2) * sum(
                g_inv[rho, sigma] * (
                    diff(g[nu, sigma], coords[mu]) +
                    diff(g[mu, sigma], coords[nu]) -
                    diff(g[mu, nu], coords[sigma])
                )
                for sigma in range(2)
            )
            Gamma[rho][mu][nu] = simplify(Gamma[rho][mu][nu])

# Print non-zero components
coord_names = ['T', 'r']
print("\nNon-zero Christoffel symbols:")

for rho in range(2):
    for mu in range(2):
        for nu in range(2):
            if Gamma[rho][mu][nu] != 0:
                print(f"  Γ^{coord_names[rho]}_{coord_names[mu]}{coord_names[nu]} = ", end="")
                sp.pprint(Gamma[rho][mu][nu])

# ========================================================================
# METRIC COMPATIBILITY: ∇_a g_bc = 0
# ========================================================================
print("\n" + "="*80)
print("METRIC COMPATIBILITY: ∇_a g_bc = 0")
print("="*80)

print("\nComputing ∇_a g_bc for all combinations...")

all_zero = True

for a in range(2):
    for b in range(2):
        for c in range(2):
            # ∇_a g_bc = ∂_a g_bc - Γ^d_ab g_dc - Γ^d_ac g_bd
            covariant_deriv = diff(g[b, c], coords[a])
            
            for d in range(2):
                covariant_deriv -= Gamma[d][a][b] * g[d, c]
                covariant_deriv -= Gamma[d][a][c] * g[b, d]
            
            covariant_deriv = simplify(covariant_deriv)
            
            if covariant_deriv != 0:
                print(f"  ∇_{coord_names[a]} g_{coord_names[b]}{coord_names[c]} = {covariant_deriv}")
                all_zero = False

if all_zero:
    print("\n✅ ALL COMPONENTS: ∇_a g_bc = 0")
    print("   Metric compatibility CONFIRMED!")
else:
    print("\n❌ ERROR: Some components non-zero!")
    sys.exit(1)

# ========================================================================
# RIEMANN CURVATURE TENSOR
# ========================================================================
print("\n" + "="*80)
print("RIEMANN CURVATURE TENSOR")
print("="*80)

print("\nComputing R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ")
print("(This may take a moment...)")

Riemann = [[[[0 for _ in range(2)] for _ in range(2)] for _ in range(2)] for _ in range(2)]

for rho in range(2):
    for sigma in range(2):
        for mu in range(2):
            for nu in range(2):
                # R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ
                R = diff(Gamma[rho][nu][sigma], coords[mu]) - diff(Gamma[rho][mu][sigma], coords[nu])
                
                for lam in range(2):
                    R += Gamma[rho][mu][lam] * Gamma[lam][nu][sigma]
                    R -= Gamma[rho][nu][lam] * Gamma[lam][mu][sigma]
                
                Riemann[rho][sigma][mu][nu] = simplify(R)

# Find non-zero components
print("\nNon-zero Riemann tensor components:")
found_nonzero = False

for rho in range(2):
    for sigma in range(2):
        for mu in range(2):
            for nu in range(2):
                if Riemann[rho][sigma][mu][nu] != 0:
                    found_nonzero = True
                    print(f"  R^{coord_names[rho]}_{coord_names[sigma]}{coord_names[mu]}{coord_names[nu]} =")
                    sp.pprint(simplify(Riemann[rho][sigma][mu][nu]))

if not found_nonzero:
    print("  ALL ZERO → Flat spacetime!")

# ========================================================================
# RICCI TENSOR AND SCALAR
# ========================================================================
print("\n" + "="*80)
print("RICCI TENSOR AND SCALAR")
print("="*80)

# Ricci tensor: R_μν = R^ρ_μρν
Ricci = [[0 for _ in range(2)] for _ in range(2)]

for mu in range(2):
    for nu in range(2):
        for rho in range(2):
            Ricci[mu][nu] += Riemann[rho][mu][rho][nu]
        Ricci[mu][nu] = simplify(Ricci[mu][nu])

print("\nRicci tensor R_μν:")
Ricci_matrix = sp.Matrix(Ricci)
sp.pprint(Ricci_matrix)

# Ricci scalar: R = g^μν R_μν
R_scalar = 0
for mu in range(2):
    for nu in range(2):
        R_scalar += g_inv[mu, nu] * Ricci[mu][nu]

R_scalar = simplify(R_scalar)

print("\nRicci scalar R:")
sp.pprint(R_scalar)

# ========================================================================
# INTERPRETATION
# ========================================================================
print("\n" + "="*80)
print("PHYSICAL INTERPRETATION")
print("="*80)

print("""
✅ METRIC COMPATIBILITY CONFIRMED:
   ∇_a g_bc = 0 for all components
   → The connection is Levi-Civita
   → Pure SSZ structure preserved

🌀 CURVATURE DEPENDS ONLY ON φ_G:
   All Riemann components ∝ derivatives of φ_G(r)
   → NOT classical Einstein curvature
   → Represents segment-rotation gradient
   
📊 KEY OBSERVATION:
   If φ_G(r) = constant → R^ρ_σμν = 0
   → Flat spacetime, but rotated!
   → Gravitation = rotation field, not curvature

⚙️ PURE SSZ INTERPRETATION:
   • No Einstein field equations needed
   • No external energy-momentum source
   • Gravitation = rotation angle φ_G(r)
   • Curvature tensor = mathematical consequence
     of rotation gradient (not its cause!)

This is FUNDAMENTALLY DIFFERENT from GR:
   GR:  Curvature → Gravitation
   SSZ: Rotation → Segment structure → "Effective curvature"
""")

print("="*80)
print("\n© 2025 Carmen N. Wrede & Lino Casu\n")
