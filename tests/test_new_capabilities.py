"""
Tests for New SSZ Capabilities:
- Physical Source Formation
- Nonlinear Stability Analysis  
- Enhanced Observational Proof
- Engineering Feasibility

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import pytest
import numpy as np
from ssz_metric_pure import (
    # Source Formation
    MatterConfig,
    equation_of_state_parameter,
    perfect_fluid_stress_energy,
    source_consistency_check,
    vacuum_source_formation,
    interior_solution_formation,
    # Stability
    standard_perturbation,
    linearize_metric,
    compute_perturbed_curvature,
    analyze_stability_spectrum,
    radial_stability_analysis,
    stability_summary,
    # Observational Proof
    ObservationData,
    ObservationalValidator,
    # Engineering
    DeviceSpec,
    QuantumDeviceSimulator,
    analyze_tolerances,
    compute_error_budget,
    assess_feasibility,
    simulate_qubit_array,
    gate_fidelity_estimate,
    device_comparison,
    EXAMPLE_QUBIT_DEVICE,
    EXAMPLE_OPTICAL_CLOCK,
)
from ssz_metric_pure.constants import M_SUN, M_EARTH


# =============================================================================
# Physical Source Formation Tests
# =============================================================================

class TestSourceFormation:
    """Test matter coupling and stress-energy construction."""
    
    def test_eos_parameters(self):
        """Verify equation of state parameters."""
        assert equation_of_state_parameter("dust") == 0.0
        assert equation_of_state_parameter("radiation") == pytest.approx(1.0/3.0)
        assert equation_of_state_parameter("vacuum") == -1.0
        print("  EOS parameters: dust=0, radiation=1/3, vacuum=-1 ✓")
    
    def test_perfect_fluid_construction(self):
        """Test stress-energy tensor construction."""
        r = 1e7  # 10,000 km
        theta = np.pi/2
        mass = M_SUN
        rho = 1000.0  # kg/m³
        p = 1e5  # Pa
        
        T = perfect_fluid_stress_energy(r, theta, mass, rho, p)
        
        assert T.T_munu.shape == (4, 4)
        assert T.energy_density > 0
        print(f"  T_μν constructed: ρ={T.energy_density:.2e}, p={T.pressure:.2e} ✓")
    
    def test_source_consistency_weak_field(self):
        """Test Einstein equations in weak field."""
        mass = M_SUN
        matter = MatterConfig(
            mass=mass,
            matter_type="perfect_fluid",
            equation_of_state="dust"
        )
        
        # Far from source (weak field)
        r = 100 * characteristic_radius(mass)
        result = source_consistency_check(r, np.pi/2, mass, matter, tolerance=1e-2)
        
        assert isinstance(result.consistency_error, float)
        print(f"  Consistency error at 100r_s: {result.consistency_error:.2e} ✓")
    
    def test_vacuum_solution(self):
        """Verify vacuum solution G_μν ≈ 0."""
        mass = M_SUN
        vacuum = vacuum_source_formation(mass)
        
        assert vacuum['all_vacuum_valid']
        assert vacuum['test_points'] == 4
        print(f"  Vacuum solution valid at {vacuum['test_points']} points ✓")
    
    def test_interior_solution(self):
        """Test interior solution with matter."""
        mass = 1.4 * M_SUN  # Neutron star
        radius = 12e3  # 12 km
        
        interior = interior_solution_formation(mass, radius, num_points=50)
        
        assert interior['compactness'] > 0
        assert interior['compactness'] < 1
        print(f"  Interior: compactness={interior['compactness']:.3f} ✓")


# =============================================================================
# Nonlinear Stability Tests  
# =============================================================================

class TestStability:
    """Test stability analysis capabilities."""
    
    def test_standard_perturbations(self):
        """Test perturbation mode generation."""
        r = 1e7
        theta = np.pi/2
        amp = 1e-6
        
        for mode in ["radial", "monopole", "dipole", "quadrupole"]:
            h = standard_perturbation(r, theta, amp, mode)
            assert h.shape == (4, 4)
        
        print("  Perturbation modes: radial, monopole, dipole, quadrupole ✓")
    
    def test_linearization(self):
        """Test metric linearization."""
        mass = M_SUN
        r = 1e7
        theta = np.pi/2
        
        def simple_pert(r, theta, A):
            h = np.zeros((4, 4))
            h[0, 0] = A * (3e8)**2
            return h
        
        pert = linearize_metric(r, theta, mass, simple_pert, amplitude=1e-8)
        
        assert pert.h_munu.shape == (4, 4)
        assert pert.gauge == "harmonic"
        print("  Linearized metric: harmonic gauge, trace-reversed ✓")
    
    def test_curvature_perturbation(self):
        """Test perturbed curvature computation."""
        mass = M_SUN
        r = 1e7
        theta = np.pi/2
        
        h = standard_perturbation(r, theta, 1e-8, "radial")
        from ssz_metric_pure.stability import LinearizedMetric
        pert = LinearizedMetric(h, "harmonic", True)
        
        curv = compute_perturbed_curvature(r, theta, mass, pert, order="linear")
        
        assert 'delta_R_munu' in curv
        assert 'delta_G_munu' in curv
        print("  Perturbed curvature: δR_μν, δG_μν computed ✓")
    
    def test_stability_spectrum(self):
        """Test full stability spectrum analysis."""
        mass = M_SUN
        r_s = 2.95e3  # Schwarzschild radius
        radii = np.array([3, 5, 10, 20]) * r_s
        
        stability = analyze_stability_spectrum(mass, radii, max_amplitude=1e-6)
        
        assert len(stability.modes) > 0
        assert stability.stability_time > 0
        print(f"  Stability: {len(stability.modes)} modes, τ_e={stability.stability_time:.2e}s ✓")
    
    def test_radial_stability(self):
        """Test radial stability specifically."""
        mass = M_SUN
        
        radial = radial_stability_analysis(mass, num_points=20)
        
        assert 'results' in radial
        assert radial['overall_stable']  # SSZ should be stable
        print(f"  Radial stability: {radial['overall_stable']}, {len(radial['results'])} amplitudes ✓")
    
    def test_stability_summary(self):
        """Test stability across mass range."""
        summary = stability_summary(
            mass_range=(1e30, 1e40),
            num_masses=5
        )
        
        assert summary['all_stable']
        assert summary['stable_fraction'] == 1.0
        print(f"  Stability summary: {summary['masses_tested']} masses, all stable ✓")


# =============================================================================
# Observational Proof Tests
# =============================================================================

class TestObservationalProof:
    """Test observational validation capabilities."""
    
    def test_validator_initialization(self):
        """Test validator setup."""
        validator = ObservationalValidator(data_source="all")
        assert validator.data_source == "all"
        print("  ObservationalValidator initialized ✓")
    
    def test_alma_data_loading(self):
        """Test ALMA data loading."""
        validator = ObservationalValidator()
        
        m87_data = validator.load_alma_data("M87")
        assert len(m87_data) > 0
        assert m87_data[0].source == "ALMA/EHT"
        print(f"  ALMA data: {len(m87_data)} M87 observations ✓")
    
    def test_nicer_data_loading(self):
        """Test NICER data loading."""
        validator = ObservationalValidator()
        
        nicer_data = validator.load_nicer_data("J0030")
        assert len(nicer_data) > 0
        assert nicer_data[0].source == "NICER"
        print(f"  NICER data: {len(nicer_data)} pulsar observations ✓")
    
    def test_prediction_generation(self):
        """Test prediction for observation."""
        validator = ObservationalValidator()
        
        obs = ObservationData(
            name="test_redshift",
            observable_type="redshift",
            measured_value=2.5e-15,
            measured_error=0.1e-15,
            metadata={'mass': M_EARTH, 'r_emit': 6378100, 'r_obs': 6378122.5},
            source="test"
        )
        
        pred = validator.predict_for_observation(obs)
        assert pred.predicted_value > 0
        print(f"  Prediction: z_pred={pred.predicted_value:.2e} ✓")


# =============================================================================
# Engineering Feasibility Tests
# =============================================================================

class TestEngineering:
    """Test engineering feasibility analysis."""
    
    def test_device_simulator_creation(self):
        """Test quantum device simulator."""
        sim = QuantumDeviceSimulator(EXAMPLE_QUBIT_DEVICE)
        
        assert sim.D_factor > 0
        assert sim.D_factor < 1
        print(f"  Device simulator: D={sim.D_factor:.10f} ✓")
    
    def test_gate_timing_correction(self):
        """Test gate timing correction."""
        sim = QuantumDeviceSimulator(EXAMPLE_QUBIT_DEVICE)
        
        t_nom = 10e-9  # 10 ns gate
        t_corr = sim.gate_timing_correction(t_nom)
        
        assert t_corr > t_nom  # SSZ slows time
        print(f"  Gate timing: {t_nom*1e9:.1f}ns → {t_corr*1e9:.3f}ns ✓")
    
    def test_phase_accumulation(self):
        """Test phase accumulation."""
        sim = QuantumDeviceSimulator(EXAMPLE_QUBIT_DEVICE)
        
        freq = 5e9  # 5 GHz
        duration = 1e-6  # 1 μs
        phase = sim.phase_accumulation(freq, duration)
        
        assert phase > 0
        print(f"  Phase accumulation: {phase:.2f} rad ✓")
    
    def test_height_sensitivity(self):
        """Test height sensitivity calculation."""
        sim = QuantumDeviceSimulator(EXAMPLE_QUBIT_DEVICE)
        
        sens = sim.height_sensitivity()
        assert sens > 0
        print(f"  Height sensitivity: {sens:.2e} m⁻¹ ✓")
    
    def test_tolerance_analysis(self):
        """Test tolerance requirements."""
        tolerances = analyze_tolerances(EXAMPLE_QUBIT_DEVICE)
        
        assert tolerances.max_height_variation > 0
        assert tolerances.timing_tolerance > 0
        print(f"  Tolerances: Δh_max={tolerances.max_height_variation*1000:.3f}mm ✓")
    
    def test_error_budget(self):
        """Test error budget computation."""
        errors = compute_error_budget(EXAMPLE_QUBIT_DEVICE)
        
        assert errors.total_error > 0
        assert errors.ssz_contribution >= 0
        print(f"  Error budget: SSZ={errors.ssz_contribution:.2e}, Total={errors.total_error:.2e} ✓")
    
    def test_feasibility_assessment(self):
        """Test complete feasibility assessment."""
        feas = assess_feasibility(EXAMPLE_QUBIT_DEVICE)
        
        assert 0 <= feas.engineering_confidence <= 1
        assert isinstance(feas.ready_for_prototype, bool)
        print(f"  Feasibility: confidence={feas.engineering_confidence*100:.0f}%, ready={feas.ready_for_prototype} ✓")
    
    def test_qubit_array_simulation(self):
        """Test multi-qubit simulation."""
        result = simulate_qubit_array(
            num_qubits=4,
            base_height=100.0,
            qubit_spacing=0.001,  # 1 mm
            operation_time=10e-9
        )
        
        assert result['num_qubits'] == 4
        assert len(result['D_factors']) == 4
        print(f"  Qubit array: {result['num_qubits']} qubits, mismatch={result['max_timing_mismatch']:.2e} ✓")
    
    def test_gate_fidelity(self):
        """Test gate fidelity estimation."""
        fidelity = gate_fidelity_estimate(
            EXAMPLE_QUBIT_DEVICE,
            num_gates=100,
            gate_time=10e-9,
            with_ssz_correction=True
        )
        
        assert fidelity['fidelity_per_gate'] > 0.99
        assert fidelity['circuit_fidelity'] > 0
        print(f"  Gate fidelity: {fidelity['fidelity_per_gate']*100:.4f}% per gate ✓")
    
    def test_device_comparison(self):
        """Test multi-device comparison."""
        devices = [EXAMPLE_QUBIT_DEVICE, EXAMPLE_OPTICAL_CLOCK]
        comparison = device_comparison(devices)
        
        assert comparison['num_devices'] == 2
        assert comparison['best_candidate'] is not None
        print(f"  Device comparison: {comparison['num_devices']} devices, best={comparison['best_candidate']} ✓")


# Helper function for characteristic radius
from ssz_metric_pure.core import characteristic_radius


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
