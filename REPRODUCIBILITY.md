# Reproducibility Guide

**Version:** `v1.1.0-canonical-pure`  
**License:** Anti-Capitalist Software License v1.4  

---

This document provides exact steps to reproduce all mathematical, numerical, and structural verification results of the **Canonical Pure SSZ Metric** research framework.

## 🌀 Environment Setup

### 1. Requirements
- **Operating System:** Linux, macOS, or Windows
- **Python:** Version `>= 3.9`
- **Compiler/Build Tools:** Only standard Python pip setup

### 2. Isolation Sandbox
We highly recommend running all verification steps inside a clean virtual environment to prevent package version pollution:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
```

### 3. Installation
Install the package in editable mode with all development and testing utilities:

```bash
python -m pip install -e ".[dev,viz]"
```

Verify that only the core dependencies (`numpy`, `scipy`, `sympy`) are registered as runtime dependencies:
```bash
python -c "import ssz_metric_pure; print('Core imported successfully!')"
```

---

## 📐 Reproducing Mathematical and Structural Verification

### 1. Canonical Core Test Suite

Run the full canonical test suite verification:

```bash
python -m pytest -q
```

*Note: No external data is required for canonical core tests. All verification checks run purely from the closed-form analytical definitions.*

### 2. Forward / Anti-Circular Observable Validation Suite

To run only the forward observable validation and anti-circular protocols:

```bash
python -m pytest tests/test_observable_predictions_forward.py tests/test_forward_anticircular_protocol.py tests/test_no_fitting_in_canonical_validation.py -q
```

### 3. Optional Domain-Specific Verification Commands

To verify specific multi-scale scale domains individually, you can execute targeted pytest modules:

```bash
# Verify Multi-Scale Usecase Matrix Integration
python -m pytest tests/test_multiscale_usecase_matrix.py -q

# Verify Neutron Star Scale Domain Usecases
python -m pytest tests/test_neutron_star_domain.py -q

# Verify Quantum Frequency & Phase Transport Scale Domain Usecases
python -m pytest tests/test_phase_frequency_domain.py -q
```

### 4. Guidelines on External Observational Data

- **External Data Tests**: Any actual observational data validation tests added in the future must live inside `tests_data/` to keep them cleanly separated from the core analytical identities.
- **LIGO / GW / Template-Bound Data Warning**: Exploratory analysis of gravitational wave events or rotating black hole candidates cannot be classified as canonical validation if it relies on general relativistic templates or template-derived posterior parameter values. Doing so introduces circular template bias. Genuine alternative-metric validation in these domains requires full, raw strain analysis under an independent, anti-circular raw pipeline. Until then, these items remain strictly exploratory.

---

## 🔍 Independent Numerical Auditing

You can independently audit the critical numerical qualities of the SSZ core metric using Python:

### 1. Verification of the Algebraic Dilation-Dehnung Identity ($D \cdot s = 1.0$)
Run the following script to verify that the reciprocal scaling condition holds to double-precision machine epsilon across all compactness regimes:

```python
import numpy as np
from ssz_metric_pure import segment_density, D_from_xi, s_from_xi

r_vals = np.logspace(0, 6, 1000)
for r in r_vals:
    xi = segment_density(r, 1.989e30)  # solar mass
    D = D_from_xi(xi)
    s = s_from_xi(xi)
    product = D * s
    assert np.isclose(product, 1.0, rtol=1e-15, atol=1e-15)

print("Algebraic coupling identity (D * s == 1) holds perfectly!")
```

### 2. Verification of the Metric Determinant $\det(g) = -c^2 r^4 \sin^2\theta$
Run this script to verify that the determinant of the generated metric matches the analytical prediction exactly:

```python
import numpy as np
from ssz_metric_pure import metric_diagonal, det_metric_diagonal, C

coords = (1.0, 50000.0, np.pi/3.0, 0.5)
g = metric_diagonal(coords, 1.989e30)
numerical_det = np.linalg.det(g)
analytical_det = det_metric_diagonal(coords, 1.989e30)

assert np.isclose(numerical_det, analytical_det, rtol=1e-12)
print("Metric determinant is perfectly verified!")
```
