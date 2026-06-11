#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Riemann Curvature Tensor - φ-Spiral SSZ Metric

Symbolic computation of:
- Christoffel symbols Γ^ρ_μν
- Riemann tensor R^ρ_σμν
- Ricci tensor R_μν
- Ricci scalar R
- Verification of 2D identity: R_μν = (1/2) g_μν R

Requires: sympy

© 2025 Carmen N. Wrede & Lino Casu
Based on Lino's symbolic computation script
"""
import sys
import os

# UTF-8 encoding for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

import sympy as sp

print("\n" + "="*80)
print("RIEMANN CURVATURE - φ-Spiral SSZ Metric (2D)")
print("="*80)

# Symbole und Funktionen
T, r = sp.symbols('T r', real=True)
c = sp.symbols('c', positive=True)
phi = sp.Function('phi')(r)          # φ(r)
gamma = sp.cosh(phi)                 # γ = cosh φ
sech = 1/sp.cosh(phi)
tanh = sp.tanh(phi)

print("\nMetric in (T,r) diagonal form:")
print("  γ(r) = cosh(φ(r))")
print("  β(r) = tanh(φ(r))")
print("  sech(φ) = 1/cosh(φ)")

# Metrik g_{μν} in Koordinaten (T, r)
g = sp.Matrix([[-c**2/gamma**2, 0],
               [0,              gamma**2]])
g_inv = g.inv()

print("\nMetric tensor g_μν:")
sp.pprint(g)

print("\nInverse metric g^μν:")
sp.pprint(g_inv)

coords = [T, r]
dim = 2

# ========================================================================
# CHRISTOFFEL SYMBOLS
# ========================================================================
print("\n" + "="*80)
print("CHRISTOFFEL SYMBOLS Γ^ρ_μν")
print("="*80)

Gamma = [[ [sp.simplify(0) for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
for a in range(dim):
    for b in range(dim):
        for c_ in range(dim):
            s = 0
            for d in range(dim):
                s += g_inv[a,d]*(sp.diff(g[d,b], coords[c_]) +
                                 sp.diff(g[d,c_], coords[b]) -
                                 sp.diff(g[b,c_], coords[d]))
            Gamma[a][b][c_] = sp.simplify(sp.Rational(1,2)*s)

print("\nNon-zero components:")
print("\nΓ^T_Tr = Γ^T_rT:")
sp.pprint(sp.simplify(Gamma[0][0][1]))

print("\nΓ^r_TT:")
sp.pprint(sp.simplify(Gamma[1][0][0]))

print("\nΓ^r_rr:")
sp.pprint(sp.simplify(Gamma[1][1][1]))

# ========================================================================
# RIEMANN CURVATURE TENSOR
# ========================================================================
print("\n" + "="*80)
print("RIEMANN CURVATURE TENSOR R^ρ_σμν")
print("="*80)
print("\nComputing (this may take a moment)...")

Riem = [[[[sp.simplify(0) for _ in range(dim)] for _ in range(dim)]
         for _ in range(dim)] for _ in range(dim)]

for a in range(dim):
    for b in range(dim):
        for c_ in range(dim):
            for d in range(dim):
                term = sp.diff(Gamma[a][b][d], coords[c_]) - sp.diff(Gamma[a][b][c_], coords[d])
                for e in range(dim):
                    term += Gamma[a][e][c_]*Gamma[e][b][d] - Gamma[a][e][d]*Gamma[e][b][c_]
                Riem[a][b][c_][d] = sp.simplify(term)

# Count non-zero components
nonzero_count = 0
for a in range(dim):
    for b in range(dim):
        for c_ in range(dim):
            for d in range(dim):
                if Riem[a][b][c_][d] != 0:
                    nonzero_count += 1

print(f"\nFound {nonzero_count} non-zero components")

# Show key component
print("\nExample: R^r_TrT:")
sp.pprint(sp.simplify(Riem[1][0][1][0]))

# ========================================================================
# RICCI TENSOR
# ========================================================================
print("\n" + "="*80)
print("RICCI TENSOR R_μν")
print("="*80)

# Ricci R_{bd} = R^a_{ bad}
Ricci = sp.Matrix([[sp.simplify(0) for _ in range(dim)] for _ in range(dim)])
for b in range(dim):
    for d in range(dim):
        s = 0
        for a in range(dim):
            s += Riem[a][b][a][d]
        Ricci[b,d] = sp.simplify(s)

print("\nRicci tensor R_μν:")
sp.pprint(Ricci)

# ========================================================================
# RICCI SCALAR
# ========================================================================
print("\n" + "="*80)
print("RICCI SCALAR R")
print("="*80)

# Skalar R = g^{bd} R_{bd}
R_scalar = sp.simplify(sum(g_inv[b,d]*Ricci[b,d] for b in range(dim) for d in range(dim)))

print("\nScalar curvature R(r):")
sp.pprint(sp.simplify(R_scalar))

print("\n" + "-"*80)
print("Expanded form:")
print("-"*80)
R_expanded = sp.expand(R_scalar)
sp.pprint(R_expanded)

# ========================================================================
# 2D IDENTITY CHECK
# ========================================================================
print("\n" + "="*80)
print("2D IDENTITY: R_μν = (1/2) g_μν R")
print("="*80)

# 2D-Identität prüfen: R_{μν} ?= (1/2) g_{μν} R
lhs = Ricci
rhs = sp.simplify(sp.Rational(1,2)*R_scalar)*g
check = sp.simplify(lhs - rhs)

print("\nLeft hand side: R_μν")
sp.pprint(lhs)

print("\nRight hand side: (1/2) g_μν R")
sp.pprint(rhs)

print("\nDifference: R_μν - (1/2) g_μν R")
sp.pprint(check)

if check == sp.Matrix([[0, 0], [0, 0]]):
    print("\n✅ 2D IDENTITY CONFIRMED: R_μν = (1/2) g_μν R")
else:
    print("\n❌ WARNING: Identity not satisfied!")
    sys.exit(1)

# ========================================================================
# EXAMPLE: EXPLICIT φ(r) PROFILE
# ========================================================================
print("\n" + "="*80)
print("EXAMPLE: φ(r) = k·log(1 + r/r₀)")
print("="*80)

k, r0 = sp.symbols('k r0', positive=True)
phi_ex = k*sp.log(1 + r/r0)

print("\nProfile: φ(r) = k·log(1 + r/r₀)")
print(f"  First derivative: φ'(r) = k/(r₀ + r)")
print(f"  Second derivative: φ''(r) = -k/(r₀ + r)²")

# Substitute into R
phi_prime = sp.diff(phi_ex, r)
phi_double_prime = sp.diff(phi_ex, r, 2)

R_substituted = R_scalar.subs({
    phi: phi_ex,
    sp.diff(phi, r): phi_prime,
    sp.diff(phi, r, 2): phi_double_prime
})

R_ex = sp.simplify(R_substituted)

print("\nResulting R(r):")
sp.pprint(R_ex)

# Check limits (numerically to avoid symbolic issues)
print("\n" + "-"*80)
print("Limiting cases (with k=1, r0=1):")
print("-"*80)

# Substitute numerical values for limits
R_num = R_ex.subs({k: 1, r0: 1})

# r → 0
print("\nAs r → 0:")
R_at_zero = sp.limit(R_num, r, 0)
print(f"  R(0) = ", end="")
sp.pprint(R_at_zero)

# r → ∞
print("\nAs r → ∞:")
R_at_inf = sp.limit(R_num, r, sp.oo)
print(f"  R(∞) = ", end="")
sp.pprint(R_at_inf)

# ========================================================================
# PHYSICAL INTERPRETATION
# ========================================================================
print("\n" + "="*80)
print("PHYSICAL INTERPRETATION")
print("="*80)

print("""
🌀 KEY OBSERVATIONS:

1. CURVATURE DEPENDS ONLY ON φ(r):
   All Riemann components ∝ φ', φ''
   → NOT classical Einstein curvature
   → Represents segment-rotation gradient

2. SPECIAL CASE φ = constant:
   If φ' = 0 and φ'' = 0 → R = 0
   → Flat spacetime, but ROTATED!
   → Gravitation = rotation, not curvature

3. 2D IDENTITY SATISFIED:
   R_μν = (1/2) g_μν R
   → Consistent with 2D differential geometry

4. WEAK FIELD (φ ≈ 0):
   R ≈ 2(φ')²
   → Quadratic in rotation gradient

5. PURE SSZ STRUCTURE:
   • No Einstein field equations needed
   • No external energy-momentum tensor
   • Gravitation = φ_G(r) rotation angle
   • Curvature = mathematical consequence,
     not physical cause!

FUNDAMENTAL DIFFERENCE from GR:
   GR:  Curvature → Gravitation
   SSZ: Rotation → Segments → "Effective curvature"
""")

# ========================================================================
# SUMMARY
# ========================================================================
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print("""
✅ COMPUTED:
   • Christoffel symbols (3 non-zero)
   • Riemann tensor R^ρ_σμν
   • Ricci tensor R_μν
   • Ricci scalar R(r)

✅ VERIFIED:
   • 2D identity R_μν = (1/2) g_μν R

✅ EXAMPLE:
   • Explicit R(r) for φ(r) = k·log(1 + r/r₀)
   • Limits: R(0) and R(∞) computed

🌀 PHYSICS:
   • Curvature from rotation gradient only
   • φ = const → R = 0 (flat but rotated)
   • Pure SSZ: No GR field equations
""")

print("="*80)
print("\n© 2025 Carmen N. Wrede & Lino Casu")
print("Based on Lino's symbolic computation\n")
