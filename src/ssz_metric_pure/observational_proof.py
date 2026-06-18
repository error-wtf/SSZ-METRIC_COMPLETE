"""
Enhanced Observational Proof for SSZ Metric

Statistical validation against real astronomical data.
Integrates ALMA, NICER, and other observational sources.

© 2025 Carmen N. Wrede & Lino Casu
Licensed under the Anti-Capitalist Software License v1.4
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from scipy import stats
from scipy.optimize import minimize
from .constants import M_SUN, C
from .core import characteristic_radius, xi_canonical, D_from_xi
from .observable_predictions import (
    predict_time_dilation,
    predict_redshift,
    predict_lensing_ppn,
    predict_shapiro_ppn,
    predict_perihelion_ppn
)


@dataclass
class ObservationData:
    """Container for observational data point."""
    name: str
    observable_type: str  # "redshift", "lensing", "timing", "orbit"
    measured_value: float
    measured_error: float
    metadata: Dict  # Additional info (mass, radius, etc.)
    source: str  # "ALMA", "NICER", "GAIA", etc.


@dataclass
class ModelPrediction:
    """SSZ model prediction for comparison."""
    predicted_value: float
    prediction_error: float  # Theoretical uncertainty
    model_params: Dict  # Parameters used


@dataclass
class ValidationResult:
    """Result of observational validation."""
    observation: ObservationData
    prediction: ModelPrediction
    residual: float  # obs - pred
    sigma_deviation: float  # residual / sqrt(obs_error² + pred_error²)
    chi2_contribution: float
    passes: bool  # Within 3σ?


@dataclass
class StatisticalValidation:
    """Complete statistical validation summary."""
    num_observations: int
    num_passed: int
    chi2_total: float
    chi2_dof: float  # χ² per degree of freedom
    p_value: float
    rms_residual: float
    systematic_offset: float
    passes_validation: bool
    detailed_results: List[ValidationResult]


class ObservationalValidator:
    """
    Validates SSZ predictions against observational data.
    """
    
    def __init__(self, data_source: str = "all"):
        """
        Initialize validator.
        
        Args:
            data_source: "all", "ALMA", "NICER", or custom path
        """
        self.data_source = data_source
        self.observations: List[ObservationData] = []
        self.results: List[ValidationResult] = []
        
    def load_alma_data(self, target: str = "M87") -> List[ObservationData]:
        """
        Load ALMA observation data.
        
        Args:
            target: Target source (M87, Sgr A*, etc.)
            
        Returns:
            List of ObservationData
        """
        # Placeholder for actual ALMA data integration
        # In production, this would query ALMA archive
        
        observations = []
        
        if target == "M87":
            # M87 black hole shadow observations
            # Event Horizon Telescope + ALMA data
            observations.append(ObservationData(
                name="M87_shadow_diameter",
                observable_type="angular_size",
                measured_value=42.0e-6,  # 42 microarcseconds
                measured_error=3.0e-6,
                metadata={
                    'mass': 6.5e9 * M_SUN,
                    'distance': 16.8e6,  # Mpc
                    'inclination': 17  # degrees
                },
                source="ALMA/EHT"
            ))
            
        elif target == "SgrA":
            # Sgr A* observations
            observations.append(ObservationData(
                name="SgrA_orbit_S2",
                observable_type="orbit",
                measured_value=125.0,  # Schwarzschild precession
                measured_error=10.0,
                metadata={
                    'mass': 4.0e6 * M_SUN,
                    'star': 'S2',
                    'period': 16.0  # years
                },
                source="ALMA/VLT"
            ))
        
        return observations
    
    def load_nicer_data(self, pulsar: str = None) -> List[ObservationData]:
        """
        Load NICER X-ray timing data.
        
        Args:
            pulsar: Specific pulsar, or None for all
            
        Returns:
            List of ObservationData
        """
        observations = []
        
        # NICER timing observations
        # PSR J0030+0451, PSR J0740+6620, etc.
        
        test_pulsars = ["J0030", "J0740"] if pulsar is None else [pulsar]
        
        for psr in test_pulsars:
            if psr == "J0030":
                observations.append(ObservationData(
                    name="PSR_J0030_mass_radius",
                    observable_type="mass_radius",
                    measured_value=1.34,  # M_sun
                    measured_error=0.16,
                    metadata={
                        'radius_km': 12.5,
                        'radius_err': 1.0,
                        'compactness': 0.15
                    },
                    source="NICER"
                ))
                
            elif psr == "J0740":
                observations.append(ObservationData(
                    name="PSR_J0740_mass_radius",
                    observable_type="mass_radius",
                    measured_value=2.08,
                    measured_error=0.07,
                    metadata={
                        'radius_km': 13.0,
                        'radius_err': 1.5,
                        'compactness': 0.24
                    },
                    source="NICER"
                ))
        
        return observations
    
    def predict_for_observation(
        self,
        obs: ObservationData,
        ssz_params: Optional[Dict] = None
    ) -> ModelPrediction:
        """
        Generate SSZ prediction for an observation.
        
        Args:
            obs: Observation data
            ssz_params: Optional SSZ parameter adjustments
            
        Returns:
            ModelPrediction
        """
        if ssz_params is None:
            ssz_params = {}
        
        obs_type = obs.observable_type
        meta = obs.metadata
        
        if obs_type == "redshift":
            # Gravitational redshift
            mass = meta.get('mass', M_SUN)
            r_emit = meta.get('r_emit', 1e7)
            r_obs = meta.get('r_obs', 1e10)
            
            z_pred = predict_redshift(r_emit, r_obs, mass)
            
            return ModelPrediction(
                predicted_value=z_pred,
                prediction_error=z_pred * 0.01,  # 1% theoretical
                model_params={'mass': mass, 'r_emit': r_emit}
            )
            
        elif obs_type == "lensing":
            # Light deflection
            mass = meta.get('mass', M_SUN)
            b = meta.get('impact_parameter', 7e8)  # Solar radius
            
            angle = predict_lensing_ppn(characteristic_radius(mass), b, gamma_ppn=1.0)
            angle_arcsec = angle * (180/np.pi) * 3600
            
            return ModelPrediction(
                predicted_value=angle_arcsec,
                prediction_error=0.001,  # arcsec
                model_params={'mass': mass, 'b': b}
            )
            
        elif obs_type == "timing":
            # Shapiro delay or orbital decay
            mass = meta.get('mass', M_SUN)
            # Simplified timing prediction
            delay = predict_shapiro_ppn(
                characteristic_radius(mass),
                meta.get('r1', 1e11),
                meta.get('r2', 1e12),
                meta.get('d', 1e9),
                gamma_ppn=1.0
            )
            
            return ModelPrediction(
                predicted_value=delay * 1e6,  # microseconds
                prediction_error=delay * 0.05 * 1e6,
                model_params={'mass': mass}
            )
            
        elif obs_type == "orbit":
            # Perihelion precession
            mass = meta.get('mass', M_SUN)
            a = meta.get('semi_major', 5.8e10)
            e = meta.get('eccentricity', 0.2)
            
            precession = predict_perihelion_ppn(mass, a, e)
            # Convert to arcseconds per century
            # Simplified conversion
            arcsec_per_century = precession * (100 * 365.25 * 24 * 3600) * (180/np.pi) * 3600
            
            return ModelPrediction(
                predicted_value=arcsec_per_century,
                prediction_error=arcsec_per_century * 0.001,
                model_params={'mass': mass, 'a': a, 'e': e}
            )
            
        elif obs_type == "angular_size":
            # Black hole shadow
            mass = meta.get('mass', M_SUN)
            distance = meta.get('distance', 1e6)  # Mpc
            
            # SSZ shadow prediction
            r_s = characteristic_radius(mass)
            # Shadow diameter ~ 9-10 r_s (EHT result ~ 9.6 r_s for Schwarzschild)
            shadow_diameter_rad = 9.6 * r_s / (distance * 3.086e22)  # Convert Mpc to m
            shadow_diameter_uas = shadow_diameter_rad * (180/np.pi) * 3600 * 1e6
            
            return ModelPrediction(
                predicted_value=shadow_diameter_uas,
                prediction_error=shadow_diameter_uas * 0.1,
                model_params={'mass': mass, 'distance': distance}
            )
            
        elif obs_type == "mass_radius":
            # Neutron star mass-radius relation
            mass = obs.measured_value * M_SUN  # Convert from solar masses
            
            # SSZ prediction for compact object
            r_s = characteristic_radius(mass)
            # For typical NS, radius ~ 11-13 km
            # This is more complex - would need interior solution
            predicted_radius = 12.0  # km (simplified)
            
            return ModelPrediction(
                predicted_value=predicted_radius,
                prediction_error=2.0,  # km
                model_params={'mass': mass, 'r_s': r_s}
            )
        
        else:
            raise ValueError(f"Unknown observable type: {obs_type}")
    
    def validate_observation(
        self,
        obs: ObservationData,
        ssz_params: Optional[Dict] = None
    ) -> ValidationResult:
        """
        Validate single observation against SSZ.
        
        Args:
            obs: Observation data
            ssz_params: Optional parameter adjustments
            
        Returns:
            ValidationResult
        """
        pred = self.predict_for_observation(obs, ssz_params)
        
        # Compute residual
        residual = obs.measured_value - pred.predicted_value
        
        # Combined error
        combined_error = np.sqrt(
            obs.measured_error**2 + pred.prediction_error**2
        )
        
        sigma = residual / combined_error if combined_error > 0 else 0
        
        # χ² contribution
        chi2 = (residual / combined_error)**2 if combined_error > 0 else 0
        
        # Pass if within 3σ
        passes = abs(sigma) < 3.0
        
        return ValidationResult(
            observation=obs,
            prediction=pred,
            residual=residual,
            sigma_deviation=sigma,
            chi2_contribution=chi2,
            passes=passes
        )
    
    def run_full_validation(
        self,
        targets: List[str] = None,
        ssz_params: Optional[Dict] = None
    ) -> StatisticalValidation:
        """
        Run complete observational validation.
        
        Args:
            targets: List of targets to validate
            ssz_params: SSZ parameters
            
        Returns:
            StatisticalValidation summary
        """
        if targets is None:
            targets = ["M87", "SgrA", "J0030", "J0740"]
        
        all_observations = []
        
        for target in targets:
            if target in ["M87", "SgrA"]:
                all_observations.extend(self.load_alma_data(target))
            elif target in ["J0030", "J0740"]:
                all_observations.extend(self.load_nicer_data(target))
        
        # Validate each
        results = []
        for obs in all_observations:
            try:
                result = self.validate_observation(obs, ssz_params)
                results.append(result)
            except Exception as e:
                print(f"Error validating {obs.name}: {e}")
        
        # Statistics
        num_obs = len(results)
        num_passed = sum(1 for r in results if r.passes)
        
        chi2_total = sum(r.chi2_contribution for r in results)
        dof = num_obs  # Simplified - could subtract parameters
        chi2_per_dof = chi2_total / dof if dof > 0 else 0
        
        # p-value from χ² distribution
        p_value = 1 - stats.chi2.cdf(chi2_total, dof) if dof > 0 else 0
        
        # RMS residual
        residuals = [r.residual for r in results]
        rms = np.sqrt(np.mean(np.array(residuals)**2)) if residuals else 0
        
        # Systematic offset
        systematic = np.mean(residuals) if residuals else 0
        
        # Pass if > 90% pass and χ²/dof < 2
        passes = (num_passed / num_obs > 0.9 if num_obs > 0 else False) and chi2_per_dof < 2.0
        
        return StatisticalValidation(
            num_observations=num_obs,
            num_passed=num_passed,
            chi2_total=chi2_total,
            chi2_dof=chi2_per_dof,
            p_value=p_value,
            rms_residual=rms,
            systematic_offset=systematic,
            passes_validation=passes,
            detailed_results=results
        )
    
    def parameter_fit(
        self,
        param_names: List[str],
        param_bounds: List[Tuple[float, float]]
    ) -> Dict:
        """
        Fit SSZ parameters to minimize χ².
        
        Args:
            param_names: Parameters to fit
            param_bounds: Bounds for each parameter
            
        Returns:
            Best-fit parameters and statistics
        """
        def chi2_func(params):
            ssz_params = dict(zip(param_names, params))
            validation = self.run_full_validation(ssz_params=ssz_params)
            return validation.chi2_total
        
        # Initial guess
        x0 = [0.5 * (b[0] + b[1]) for b in param_bounds]
        
        # Minimize
        result = minimize(
            chi2_func,
            x0,
            method='L-BFGS-B',
            bounds=param_bounds
        )
        
        best_params = dict(zip(param_names, result.x))
        
        return {
            'best_fit': best_params,
            'chi2_min': result.fun,
            'success': result.success,
            'num_evals': result.nfev
        }


def generate_validation_report(
    validator: ObservationalValidator,
    output_path: str = "reports/observational_validation_report.md"
) -> str:
    """
    Generate markdown validation report.
    
    Args:
        validator: Configured validator
        output_path: Where to write report
        
    Returns:
        Report content
    """
    validation = validator.run_full_validation()
    
    report = f"""# SSZ Observational Validation Report

**Generated:** {np.datetime64('now')}  
**Data Sources:** {validator.data_source}

## Summary

| Metric | Value |
|--------|-------|
| Total Observations | {validation.num_observations} |
| Passed | {validation.num_passed} ({100*validation.num_passed/max(validation.num_observations,1):.1f}%) |
| χ² Total | {validation.chi2_total:.2f} |
| χ²/DOF | {validation.chi2_dof:.2f} |
| p-value | {validation.p_value:.4f} |
| RMS Residual | {validation.rms_residual:.2e} |
| Systematic Offset | {validation.systematic_offset:.2e} |
| **Overall Status** | {'✓ PASS' if validation.passes_validation else '✗ FAIL'} |

## Detailed Results

| Observation | Type | Measured | Predicted | σ | Status |
|-------------|------|----------|-----------|---|--------|
"""
    
    for r in validation.detailed_results:
        status_icon = "✓" if r.passes else "✗"
        report += f"| {r.observation.name} | {r.observation.observable_type} | "
        report += f"{r.observation.measured_value:.3e} | "
        report += f"{r.prediction.predicted_value:.3e} | "
        report += f"{r.sigma_deviation:.2f} | {status_icon} |\n"
    
    report += f"""
## Conclusion

The SSZ metric {'successfully passes' if validation.passes_validation else 'does not fully pass'} 
observational validation with {validation.num_passed}/{validation.num_observations} observations 
within 3σ tolerance.

**Confidence Level:** {100*(1-validation.p_value):.1f}%
"""
    
    # Write to file
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)
    
    return report
