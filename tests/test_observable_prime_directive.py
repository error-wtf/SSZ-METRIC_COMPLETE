"""
Test of Observable Prime Directive Classification and Method Routing.

Verifies:
- Observable names are classified into NULL_LIGHT, TIMELIKE_STATIC, or TIMELIKE_ORBIT.
- Observable classes route to correct PPN_COMPLETION, XI_DIRECT, or PPN_ORBIT methods.
- Value evaluation using correct PPN factor completion.

© 2025 Carmen Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
from ssz_metric_pure import (
    classify_observable, method_for_observable, ObservableClass, MethodAssignment,
    SSZObservableSuite, M_SUN, C
)

def test_observable_classification_routing():
    """Verify that name routing and classifications are correctly allocated."""
    # 1. Null/Light path
    for name in ["lensing", "Lensing", "shapiro_delay", "vlbi_delay", "group_delay"]:
        cls = classify_observable(name)
        assert cls == ObservableClass.NULL_LIGHT
        assert method_for_observable(cls) == MethodAssignment.PPN_COMPLETION
        
    # 2. Timelike Static Clock
    for name in ["gravitational_redshift", "time_dilation", "gps_clock", "pound_rebka"]:
        cls = classify_observable(name)
        assert cls == ObservableClass.TIMELIKE_STATIC
        assert method_for_observable(cls) == MethodAssignment.XI_DIRECT
        
    # 3. Timelike Orbit
    for name in ["perihelion_advance", "precession_orbit", "frame_dragging"]:
        cls = classify_observable(name)
        assert cls == ObservableClass.TIMELIKE_ORBIT
        assert method_for_observable(cls) == MethodAssignment.PPN_ORBIT


def test_ppn_completion_evaluation():
    """Verify correct PPN completion factor (1 + gamma) is applied to light paths."""
    suite = SSZObservableSuite(M_SUN)
    
    # Shapiro delay evaluation: temporal piece should be doubled (PPN gamma = 1)
    xi_only = 1e-5
    completed = suite.null_ppn_completion(xi_only, gamma_ppn=1.0)
    assert completed == xi_only * 2.0
