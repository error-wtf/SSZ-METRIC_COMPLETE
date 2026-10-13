#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLOBAL_FORENSIC Phase G — Reparatur-Regressionstests (Version 2).

Struktur: GR-Kontrolle und SSZ laufen durch DIESELBEN Routinen wie der Code;
die Referenzwerte fuer GR kommen aus einer UNABHAENGIGEN mpmath-Rechnung
(exakte Stammfunktionen / GLOBAL_FORENSIC_V1-Validierungen), nicht aus dem Code.
"""
import sys
import numpy as np
from numpy.polynomial.legendre import leggauss
import mpmath as mp
import sympy as sp

sys.path.insert(0, '/home/error/physics/clones/SSZ-METRIC_COMPLETE/src')

from ssz_metric_pure.constants import C
from ssz_metric_pure import shapiro_exact, ppn, deflection_exact
from ssz_metric_pure.core import characteristic_radius

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name} {detail}")
    if not cond:
        FAILURES.append(name)


M_SUN = 1.98892e30
mass = M_SUN
r_s = characteristic_radius(mass)

# ---------- G1: Shapiro analytisch gegen sympy-Integral ----------
x = sp.symbols('x', positive=True)
Xi = sp.Rational(1) / (2 * x)                      # Einheiten r_s = 1
expr = sp.integrate(sp.expand((1 + Xi)**2 - 1), x)  # Stammfunktion von 2Xi + Xi^2
ref_sym = float((expr.subs(x, 1e6) - expr.subs(x, 1e5)))  # * r_s / c unten
ref = (ref_sym * r_s) / C
d_analytic = shapiro_exact.shapiro_delay_weak_field_exact(1e5 * r_s, 1e6 * r_s, mass)
rel = abs(d_analytic - ref) / ref
check("G1 shapiro == sympy-Int (2Xi+Xi^2)", rel < 1e-9, f"rel={rel:.2e}, Stammf={expr}")

# ---------- G2: numerisch vs analytisch ----------
d_num = shapiro_exact.shapiro_delay_numerical_exact(1e5 * r_s, 1e6 * r_s, mass, n_points=20000)
rel = abs(d_num - d_analytic) / d_analytic
check("G2 numeric vs analytic < 0.1%", rel < 1e-3, f"rel={rel:.2e}")

# ---------- G3: PPN aus der Metrik (Code-Routine) + ANALYTISCHE Kontrolle ----------
# Analytisch exakt (mpmath/sympy, unabhaengig): SSZ weak rho = r*exp(-1/(2r)) ->
#   -gtt/c^2 = (1+1/(2r))^-2 mit r = -W0(-rho e^{-rho}/2)... numerisch invertierbar:
#   serie: 1 - 1/rho + 5/(4 rho^2) + O(1/rho^3) => beta=5/2, gamma=1.
# GR: r = rho(1+1/(4rho))^2 => -gtt = ((1-1/4rho)/(1+1/4rho))^2 = 1-1/rho+1/(2rho^2)+...
#   => beta=1, gamma=1.
p = ppn.ppn_parameters_from_metric()
ssz, gr = p["ssz_weak_branch"], p["gr_control"]
print(f"    Code-PPN  SSZ: beta={ssz['beta_ppn']:.6f} gamma={ssz['gamma_ppn']:.6f} "
      f"rs_meas/in={ssz['rs_meas_over_rs_input']:.6f} res_gtt={ssz['fit_residual_gtt']:.2e} "
      f"res_grr={ssz['fit_residual_grr']:.2e}")
print(f"    Code-PPN  GR : beta={gr['beta_ppn']:.6f} gamma={gr['gamma_ppn']:.6f} "
      f"rs_meas/in={gr['rs_meas_over_rs_input']:.6f} res_gtt={gr['fit_residual_gtt']:.2e} "
      f"res_grr={gr['fit_residual_grr']:.2e}")

check("G3 SSZ beta = 5/2 (tol 2e-4)", abs(ssz["beta_ppn"] - 2.5) < 2e-4,
      f"beta={ssz['beta_ppn']:.6f}")
check("G3 SSZ gamma = 1 (tol 1e-4)", abs(ssz["gamma_ppn"] - 1.0) < 1e-4,
      f"gamma={ssz['gamma_ppn']:.6f}")
check("G3 SSZ Massen-Normierung rs_meas/rs_input=1 (tol 1e-3)",
      abs(ssz["rs_meas_over_rs_input"] - 1.0) < 1e-3)
check("G3 GR-Kontrolle beta=1 (tol 1e-4)", abs(gr["beta_ppn"] - 1.0) < 1e-4,
      f"beta={gr['beta_ppn']:.6f}")
check("G3 GR-Kontrolle gamma=1 (tol 1e-4)", abs(gr["gamma_ppn"] - 1.0) < 1e-4,
      f"gamma={gr['gamma_ppn']:.6f}")
check("G3 GR-Fitresiduen klein", gr["fit_residual_gtt"] < 1e-3 and gr["fit_residual_grr"] < 1e-3)

w = ppn.weak_field_expansion_coeffs(100 * r_s, mass)
check("G3b areale Koeffizienten (-2, 3 | 2, 1)",
      w["g_tt_coeff_order1"] == -2.0 and w["g_tt_coeff_order2"] == 3.0
      and w["g_rr_coeff_order1"] == 2.0 and w["g_rr_coeff_order2"] == 1.0)

# ---------- G4: Deflection — unabhaengige GR-Referenz (mpmath, check13-validiert) ----------
def delta_mp(b_over_rs):
    """GR delta via r=r0+t^2-Substitution, Gauss-Legendre — UNABHAENGIG vom Code."""
    b = mp.mpf(str(b_over_rs))
    A_t = lambda r: 1 - 1/r
    # Turning point: outermost root of 1 - (1-1/r) b^2/r^2 (radicand positive
    # OUTSIDE r0, negative inside -> f(mid) <= 0 means mid is past the root,
    # shrink hi). Previously the bisection direction was inverted and the
    # reference converged to the inner branch (delta ~ -pi).
    lo, hi = mp.mpf('1.0000001'), b * 2
    f = lambda r: 1 - A_t(r) * b**2 / r**2
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0: hi = mid
        else: lo = mid
    r0 = (lo + hi) / 2
    B = r0 / mp.sqrt(A_t(r0))
    fint = lambda t: (B * 2 * t) / (((r0 + t * t) ** 2) * mp.sqrt(f(r0 + t * t)))
    NODES, WEIGHTS = leggauss(200)
    total = mp.mpf('0')
    # tail split into log-spaced segments (a single [100, t_max] segment with
    # 200 Gauss nodes oscillates wildly on the 2B/t^3 tail); residual tail
    # beyond r_max=1e12 is ~2B/r_max ~ 2e-9 << tol 2e-6
    _tail = [(100.0, 316.0), (316.0, 1e3), (1e3, 3162.0), (3162.0, 1e4),
             (1e4, 3.16e4), (3.16e4, 1e5), (1e5, 3.16e5), (3.16e5, 1e6)]
    for a_, b_ in [(0, 0.5), (0.5, 1), (1, 3), (3, 10), (10, 100)] + _tail:
        for i in range(200):
            tm = 0.5 * (b_ - a_) * NODES[i] + 0.5 * (a_ + b_)
            w_ = 0.5 * (b_ - a_) * WEIGHTS[i]
            rr = r0 + mp.mpf(str(tm)) ** 2
            total += mp.mpf(str(w_)) * mp.re(fint(mp.mpf(str(tm))))
    return float(2 * total - mp.pi)

# GR-Selbsttest der Referenzroutine (check13-Validierung):
d_ref_1000 = delta_mp(1000.0)
check("G4 GR-Referenz delta(b=1000 r_s)=+0.002002", abs(d_ref_1000 - 0.0020019474) < 2e-6,
      f"delta={d_ref_1000:.10f}")

# Der reparierte Code ist SSZ (bewusst NICHT GR); wir pruefen: endlich, positiv,
# und asymptotisch gegen 2 r_s / b:
b100 = 100.0 * r_s
a_code = deflection_exact.deflection_numerical_exact(b100, mass, n_points=20000)
a_asym = 2.0 / 100.0
check("G4b SSZ Code endlich & positiv", np.isfinite(a_code) and 0 < a_code < 1.0,
      f"alpha(b=100 r_s)={a_code:.6f}")
check("G4c SSZ ~ 2r_s/b (5%) bei b=100 r_s", abs(a_code - a_asym) < 0.05 * a_asym,
      f"code={a_code:.8f} asym={a_asym:.8f}")

a_weak = deflection_exact.deflection_weak_field_exact(100 * r_s, mass)
check("G4d weak asymptotik exakt 2r_s/b", abs(a_weak - 2.0/100.0) < 1e-12)

print()
print("=" * 60)
if FAILURES:
    print(f"ERGEBNIS: {len(FAILURES)} FAIL -> {FAILURES}")
    sys.exit(1)
print("ERGEBNIS: ALLE REPARATUR-REGRESSIONSTESTS PASS")
sys.exit(0)
