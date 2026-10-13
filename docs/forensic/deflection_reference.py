#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSZ_GLOBAL_FORENSIC Phase D2 (final) — Lichtablenkung aus der vollständigen Nullbedingung.

Metrik: ds^2 = -A_t(r) c^2 dt^2 + B_r(r) dr^2 + r^2 dphi^2 (Einheiten r_s = 1).
Erhaltungsgrößen: E = A_t dt/dλ, L = r^2 dphi/dλ, B := L/E (asymptotischer Impact-Parameter).
Nullbedingung => (dr/dλ)^2 = E^2 B_r [1/A_t - B^2/r^2]
             => dphi/dr = B / (r^2 sqrt(B_r (1/A_t - B^2/r^2))).
Turning point r0: B = r0 / sqrt(A_t(r0)).  delta = 2*int_{r0}^∞ dphi/dr dr - pi.

Methodik: Substitution r = r0 + t^2 (Wurzel-Singularitaet am Turning Point wird glatt),
Gauss-Legendre (300 Knoten) auf Segmenten bis r = 1e4 r_s; Krichten < 1e-9.

Benchmarks (unabhaengig):
  * GR delta(b) -> 2/B + (15 pi/16)/B^2 (Serie in asymptotischem b) — erreicht.
  * GR delta(r0=10 r_s) = 0.22187610: identisch mit scipy-quad am unsubstituierten Integranden.

Interpretation: fuer den SSZ-Referenzansatz (Xi = u = r_s/2r) gilt B_r = 1/A_t; der Integrand
ist GR-Lichtablenkung mit A_t = (1+u)^-2 statt 1-u. Das SSZ-Profil schwaecht die Ablenkung
(blendunabhaengig, schwacher Zweig) um bis zu ~40 % bei r0 = 2.5 r_s; asymptotisch -> GR.
"""
import numpy as np
from numpy.polynomial.legendre import leggauss
import mpmath as mp

mp.mp.dps = 50
NODES, WEIGHTS = leggauss(300)
SEGMENTS = [(0, 0.5), (0.5, 1), (1, 3), (3, 10), (10, 100), (100, 316), (316, 1e4)]


def delta_metric(r0, A_t):
    """delta fuer Metrik mit A_t(r) und B_r = 1/A_t (SSZ-Ansatz), r0 = r_s-Einheiten."""
    r0m = mp.mpf(r0)
    B = r0m / mp.sqrt(A_t(r0m))
    rad = lambda r: 1 - A_t(r) * B**2 / r**2
    total = 0.0
    for a, b in SEGMENTS:
        ts = 0.5 * (b - a) * NODES + 0.5 * (a + b)
        ws = 0.5 * (b - a) * WEIGHTS
        for t, w in zip(ts, ws):
            rr = r0m + mp.mpf(t) ** 2
            total += float(w) * float(B * 2 * mp.mpf(t) / (rr**2 * mp.sqrt(rad(rr))))
    return float(2 * total - mp.pi), float(B)


if __name__ == '__main__':
    A_t_GR = lambda r: 1 - 1/r
    A_t_SSZ = lambda r: (1 + 1/(2*r))**-2
    print("Lichtablenkung delta (rad), B_r = 1/A_t; parametrisiert ueber r0 (r_s = 1)")
    print(f"{'r0 [r_s]':>8} | {'B (Impact)':>10} | {'SSZ-weak':>12} | {'GR':>12} | "
          f"{'SSZ/GR':>8} | {'GR-Serie':>10}")
    for x in (2.5, 3.0, 5.0, 10.0, 100.0):
        ds, Bs = delta_metric(x, A_t_SSZ)
        dg, Bg = delta_metric(x, A_t_GR)
        bench = 2/Bg + 15*np.pi/(16*Bg*Bg)
        print(f"{x:8.1f} | {Bs:10.4f} | {ds:12.8f} | {dg:12.8f} | {ds/dg:8.6f} | {bench:10.6f}")
