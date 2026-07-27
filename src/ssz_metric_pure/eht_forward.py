"""Static spherical GR/SSZ EHT visibility forward model for SSZ-METRIC-COMPLETE."""
from __future__ import annotations
import math
from scipy.optimize import brentq
from scipy.special import j0
from .constants import C, G, M_SUN
from .core import xi_canonical, D_from_xi, characteristic_radius

def gr_lapse_x(x):
    if x <= 1.0:
        raise ValueError("GR lapse requires x > 1")
    return math.sqrt(1.0 - 1.0 / float(x))

def ssz_lapse_x(x):
    rs = characteristic_radius(M_SUN)
    return float(D_from_xi(xi_canonical(float(x) * rs, M_SUN)))

def _derivative(fn, x):
    h = 1e-5 * max(1.0, abs(x))
    return (fn(x + h) - fn(x - h)) / (2.0 * h)

def photon_sphere_x(lapse):
    def f(x):
        return 2.0 * lapse(x) ** 2 - x * _derivative(lambda r: lapse(r) ** 2, x)
    grid = [1.01 + (30.0 - 1.01) * i / 2000.0 for i in range(2001)]
    for left, right in zip(grid, grid[1:]):
        if f(left) * f(right) <= 0.0:
            return brentq(f, left, right)
    raise ValueError("no photon sphere found")

def critical_impact_x(lapse):
    x = photon_sphere_x(lapse)
    return x / lapse(x), x

def angular_scale(mass_kg, distance_m):
    return G * float(mass_kg) / (C * C * float(distance_m))

def predict_visibility(model, *, mass_kg, distance_m, baselines_wavelengths,
                       hotspot_fraction=0.15, hotspot_offset_rg=(1.0, 0.4)):
    if model == "GR":
        lapse = gr_lapse_x
    elif model == "SSZ":
        lapse = ssz_lapse_x
    else:
        raise ValueError("model must be GR or SSZ")
    impact_x, photon_x = critical_impact_x(lapse)
    theta_g = angular_scale(mass_kg, distance_m)
    ring = impact_x * theta_g
    offset = (hotspot_offset_rg[0] * theta_g, hotspot_offset_rg[1] * theta_g)
    vis = []
    for u, v in baselines_wavelengths:
        q = math.hypot(u, v)
        phase = -2.0 * math.pi * (u * offset[0] + v * offset[1])
        ring_vis = j0(2.0 * math.pi * q * ring)
        vis.append(complex((1.0 - hotspot_fraction) * ring_vis + hotspot_fraction * math.cos(phase),
                           hotspot_fraction * math.sin(phase)))
    return {"model": model, "photon_sphere_x": photon_x, "critical_impact_x": impact_x,
            "ring_radius_rad": ring, "visibility": vis,
            "visibility_amplitude": [abs(z) for z in vis],
            "claim_boundary": "static spherical shared-emission prototype; not observational evidence"}

def compare_gr_ssz(*, mass_kg, distance_m, baselines_wavelengths,
                   hotspot_fraction=0.15, hotspot_offset_rg=(1.0, 0.4)):
    gr = predict_visibility("GR", mass_kg=mass_kg, distance_m=distance_m,
        baselines_wavelengths=baselines_wavelengths, hotspot_fraction=hotspot_fraction,
        hotspot_offset_rg=hotspot_offset_rg)
    ssz = predict_visibility("SSZ", mass_kg=mass_kg, distance_m=distance_m,
        baselines_wavelengths=baselines_wavelengths, hotspot_fraction=hotspot_fraction,
        hotspot_offset_rg=hotspot_offset_rg)
    def cp(values):
        z = complex(1.0, 0.0)
        for value in values:
            z *= value
        return math.atan2(z.imag, z.real)
    return {"status": "FORWARD_PREDICTIONS_BUILT", "gr": gr, "ssz": ssz,
            "delta_visibility_amplitude": [a-b for a,b in zip(ssz["visibility_amplitude"], gr["visibility_amplitude"])],
            "delta_closure_phase_rad": cp(ssz["visibility"]) - cp(gr["visibility"]),
            "claim_boundary": "shared static emission comparison; no observed target was scored"}
