#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ_GLOBAL_FORENSIC Phase B/C — Symbolische Referenzableitung (SymPy, exakt).
Referenzfall (Carmens Vorgabe):
    Xi = u = GM/(r c^2) = rs/(2r)
    A_t = (1+u)^{-2},  B_r = (1+u)^2,  C = r^2
Geprüft wird:
  (1) isotrope Transformation r(rho) als Serienansatz bis O(U^3)
      mit TOTALER Ableitung d r(rho)/drho (rs/(2rho) ist rho-abhaengig!);
      Konformflachheit: B_r*(dr/drho)^2 = (r/rho)^2  [C=r^2]
  (2) -g_tt/c^2 und g_rhorho-Entwicklung in U=GM/(rho c^2)=rs/(2rho)
  (3) PPN: gamma aus g_rr-Fuehrungskoeffizienten, beta aus g_tt-U^2
  (4) Shapiro radial exakt: dt/dr = (1+u)^2/c -> Zusatzlaufzeit 2u+u^2
  (5) Photonensphaere: d/dr [C/A_t] = d/dr[r*(1+u)^2] = 0
Kein Wert hartkodiert; alle Koeffizienten aus der Rechnung.
"""
import sympy as sp

rho, rs, r = sp.symbols('rho rs r', positive=True)
U = sp.Symbol('U', positive=True)   # rs/(2 rho)
a1, a2, a3 = sp.symbols('a1 a2 a3')

u_of_r = rs/(2*r)
A_t = (1 + u_of_r)**-2
B_r = (1 + u_of_r)**2

# ---------- (1) isotrope Transformation: totale Ableitung! ----------
r_of_rho = rho*(1 + a1*U + a2*U**2 + a3*U**3)
dr_drho = sp.diff(r_of_rho.subs(U, rs/(2*rho)), rho).subs(rs/(2*rho), U)
#  -> totale Ableitung: 1 + a1*U - 2*a1*U + ... sauber via Kettenregel:
dr_tot = sp.diff(rho*(1 + a1*rs/(2*rho) + a2*(rs/(2*rho))**2 + a3*(rs/(2*rho))**3), rho)
dr_tot = dr_tot.subs(rs, 2*rho*U)
cond = sp.expand((B_r.subs(r, r_of_rho)*dr_tot**2 - (r_of_rho/rho)**2).subs(rs, 2*rho*U))
num = sp.Poly(sp.expand(sp.together(cond).as_numer_denom()[0]), U)
eqs = [sp.Eq(sp.factor(num.coeff_monomial(U**k)), 0) for k in (1, 2, 3)]
sol = sp.solve(eqs, [a1, a2, a3], dict=True)[0]
print("(1) isotrope Transformation  r = rho*(1 + a1*U + a2*U^2 + a3*U^3)")
print("    a1 =", sol[a1], "  a2 =", sol[a2], "  a3 =", sol[a3])
gr_check = sp.solve(
    [sp.Eq(sp.Poly(sp.expand(sp.together(
        ((1-2*u_of_r)**-1).subs(r, r_of_rho)*dr_tot**2 - (r_of_rho/rho)**2
    ).as_numer_denom()[0].subs(rs, 2*rho*U)), U).coeff_monomial(U**k), 0)
     for k in (1, 2, 3)], [a1, a2, a3], dict=True)[0]
print("    GR-Referenz (g_rr=(1-2u)^-1): a1 =", gr_check[a1],
      " a2 =", gr_check[a2], " [bekannt: 1, 1/4]")

# ---------- (2) g_tt in isotropen Koordinaten ----------
g_tt = sp.expand(A_t.subs(r, r_of_rho).subs(sol).subs(rs, 2*rho*U))
g_tt_ser = sp.series(g_tt, U, 0, 4).removeO()
g_tt_ser = sp.simplify(sp.expand(sp.together(g_tt_ser)))
num_t, den_t = sp.together(g_tt_ser).as_numer_denom()
num_t = sp.Poly(sp.expand(num_t), U)
den_t = sp.expand(den_t)
c1 = sp.simplify(num_t.coeff_monomial(U**1)/den_t.coeff(U, 0))
c2 = sp.simplify(num_t.coeff_monomial(U**2)/den_t.coeff(U, 0))
print("\n(2) -g_tt/c^2 = 1 + (%s) U + (%s) U^2 + O(U^3)" % (c1, c2))
beta_gtt = sp.simplify(c2/2)
gamma_gtt = sp.simplify(-c1/2)

# ---------- (3) g_rhorho ----------
g_rr = sp.expand(B_r.subs(r, r_of_rho).subs(sol)*(dr_tot.subs(sol)**2)
                 .subs(rs, 2*rho*U))
# ---------- (3) g_rhorho: konformflach per Konstruktion -> g_rr = (r/rho)^2 ----------
# Identitaet numerisch verifizieren (B*dr^2 = (r/rho)^2 nach geloester Transformation):
ident = sp.simplify((B_r.subs(r, r_of_rho)*dr_tot**2 - (r_of_rho/rho)**2).subs(sol).subs(rs, 2*rho*U))
print("    Konformflachheit-Residuum (symbolisch 0?):", sp.simplify(ident) == 0)
g_rr_series = sp.expand((r_of_rho/rho).subs(sol)**2)
d1 = sp.expand(g_rr_series).coeff(U, 1)
print("    g_rhorho    = 1 + (%s) U + O(U^2)" % d1)
gamma_grr = sp.simplify(d1/2)

# ---------- (4) Shapiro ----------
extra = sp.expand(sp.simplify(sp.sqrt(B_r/A_t)) - 1)
sh_ok = sp.simplify(extra - (2*u_of_r + u_of_r**2)) == 0
x, x1, x2 = sp.symbols('x x1 x2', positive=True)
I_ssz = sp.integrate(1/x + sp.Rational(1, 4)/x**2, (x, x1, x2))   # Zusatzlaufzeit, x=r/rs
GR_ref = sp.log((x2-1)/(x1-1))
vals = {x1: sp.Rational(23, 10), x2: sp.Rational(100)}
ratio = sp.N(I_ssz.subs(vals)/GR_ref.subs(vals), 10)
# Code im Repo: Integral Xi dr = (1/2) ln(x2/x1)
I_code = sp.log(x2/x1)/2
ratio_code = sp.N(I_code.subs(vals)/GR_ref.subs(vals), 10)
print("\n(4) Shapiro: dt/dr-1 = 2u+u^2 ?", sh_ok)
print("    metrisch/GR (2.3->100 r_s) =", ratio, "   code(∫Ξdr)/GR =", ratio_code)

# ---------- (5) Photonensphaere ----------
W = sp.simplify(r/A_t)   # r*(1+u)^2
dW = sp.simplify(sp.diff(W, r))
crit = sp.solve(sp.Eq(sp.numer(sp.together(dW)), 0), r)
print("\n(5) Photonensphaere: d/dr[r*(1+u)^2] = 0 -> Lsungen:", crit)

# ---------- Zusammenfassung ----------
print("\n=== PPN-Referenzfall (Xi=u, A_t=(1+u)^-2, B_r=(1+u)^2, C=r^2) ===")
print("gamma_PPN (g_rr) =", gamma_grr, " | gamma_PPN (g_tt) =", gamma_gtt)
print("beta_PPN  (g_tt) =", beta_gtt)
ok = (gamma_grr == 1) and (beta_gtt == sp.Rational(5, 2)) and (gamma_gtt == 1)
print("Erwartung Carmen: gamma=1, beta=5/2 ->",
      "BESTAETIGT (exakt, symbolisch)" if ok else "NICHT bestaetigt!")
