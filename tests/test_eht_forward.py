import numpy as np
from ssz_metric_pure.eht_forward import compare_gr_ssz, critical_impact_x, gr_lapse_x

def test_gr_photon_sphere():
    impact, photon = critical_impact_x(gr_lapse_x)
    assert abs(photon-1.5) < 0.01
    assert impact > photon

def test_shared_visibility_forward():
    result = compare_gr_ssz(mass_kg=4.3e6*1.98847e30, distance_m=8.2e3*3.085677581491367e16,
        baselines_wavelengths=[(1e9,0),(0,1e9),(-1e9,-1e9)])
    assert result['status'] == 'FORWARD_PREDICTIONS_BUILT'
    assert len(result['delta_visibility_amplitude']) == 3
