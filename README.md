# Canonical Pure SSZ Metric

**Version:** `v1.1.0-canonical-pure`  
**License:** Anti-Capitalist Software License v1.4  
**Authors:** Carmen Wrede & Lino Casu  

---

## 📖 Overview

This repository implements a canonical Xi-primary SSZ metric kernel and multi-scale usecase framework from Planck-/fine-structure-adjacent segmentation through phase/frequency, EM/clock, weak-field PPN, strong-field compact-object, and neutron-star domains.

The framework is complete as a structured implementation scaffold for the declared domains. It does not claim complete quantum gravity, complete matter-source formation, complete nonlinear stability, complete external observational proof, or engineering feasibility.

Unlike hybrid approaches that disguise standard General Relativity (GR) solutions with external scaling parameters, this codebase is designed from first principles around the **segment density field representation of gravity**, completely isolated from Kerr, Schwarzschild, or General Relativity scaffolding in the core package.

The canonical core tests verify internal mathematical identities, Xi-primary construction, metric determinant/inverse consistency, no-freeze tensor behavior, observable method routing, and forbidden-scaffold isolation within the implemented test domain.

---

## 📐 Mathematical Formulation

### 1. Primary Field $\\Xi(r)$
The segment density $\\Xi(r)$ is a dimensionless, non-negative scalar field representing the primary physical quantity:
- Far from a source, segmentation vanishes: $\\Xi(r) \\to 0$ as $r \\to \\infty$.
- Near compact objects, segmentation increases but remains finite: $\\Xi(r_s) = 1 - e^{-\\varphi} \\approx 0.8017118$ (at $r = r_s$, where $\\varphi \\approx 1.6180339887$ is the Golden Ratio).

### 2. Operational Scaling Factors
The reciprocal clock scaling $D(r)$ and radial scaling $s(r)$ are derived directly from the primary segment density field $\\Xi(r)$:
- Time dilation: $D(r) = \\frac{1}{1 + \\Xi(r)}$
- Radial stretching: $s(r) = 1 + \\Xi(r)$

These scaling factors satisfy the reciprocal coupling identity:
$$D(r) \\cdot s(r) = 1$$

### 3. Canonical SSZ Metric (Diagonal Form)
The static, spherically symmetric diagonal line element in coordinate time $T$ is written as:
$$ds^2 = -\\frac{c^2}{(1 + \\Xi(r))^2} dT^2 + (1 + \\Xi(r))^2 dr^2 + r^2(d\\theta^2 + \\sin^2\\theta d\\varphi^2)$$

### 4. Local $c$ Invariance
Under radial null propagation ($ds^2 = 0$), the coordinate speed of light is $dr/dT = c \\cdot D(r)^2$. However, in a local orthonormal frame with $d\\hat{r} = s(r) dr$ and $d\\hat{t} = D(r) dT$, we obtain:
$$\\frac{d\\hat{r}}{d\\hat{t}} = \\frac{s(r) dr}{D(r) dT} = c$$
Thus, local light-speed remains strictly invariant and equal to $c$.

---

## 📦 Package Structure

```text
├── src/
│   └── ssz_metric_pure/         # Core API package (strictly pure SSZ)
│       ├── __init__.py          # Version & exports
│       ├── constants.py         # Gravitational & Golden Ratio constants
│       ├── core.py              # Canonical Xi potentials, regimes, and splines
│       ├── segmentation.py      # Operational segment scaling, distance, local c checks
│       ├── metric.py            # Diagonal and flow-form metric tensors derived from Xi
│       ├── tensor.py            # Numeric & symbolic connection/curvature engines
│       ├── observables.py       # Observables mapper (Postulate 5 assignments)
│       ├── validation.py        # Validation helpers (D*s=1)
│       ├── kinematics.py        # Kinematics and coordinate light speed
│       ├── electromagnetism.py  # Refractive index and phase velocity
│       ├── ppn.py               # Parameterized Post-Newtonian parameters
│       ├── strong_field.py      # Photon sphere and strong-field limits
│       ├── energy.py            # Energy conditions (WEC, SEC)
│       ├── frequency.py         # Clock ratios and radial wave phase
│       ├── falsification.py     # Astrophysical constraints and bounds
│       └── repo_consistency.py  # Core purity verification engine
├── comparison/                  # GR comparisons (isolated reference code)
├── legacy/                      # Legacy/comparison models (isolated)
├── tests/                       # Complete pytest suite
└── pyproject.toml               # Unified PEP 517 build configuration
```

---

## 🛠️ Installation & Usage

### 1. Installation
Install the package locally in editable mode to bind the path structure:
```bash
python -m pip install -e .
```

To install optional developer and visualization dependencies:
```bash
python -m pip install -e ".[dev,viz]"
```

### 2. Running Verification Tests
Execute the comprehensive verification test suite verifying all identities, determinants, weak-field PPN limits, and strict core isolation:
```bash
python -m pytest -q
```

---

## ⚠️ Current Limitations

The kanonische SSZ-Metrik ist als Xi-primärer Core vollständig definiert und für die dokumentierten Observablenklassen forward/antizirkulär testbar. Für dynamische, rotierende, mehrkörper-, quanten- und engineeringbezogene Usecases ist sie ein Ausgangspunkt, aber noch keine vollständige Lösung.

This repository implements a canonical Xi-primary SSZ metric research framework. It does not claim physical source formation, nonlinear stability, complete external observational proof, physical beaming, or engineering feasibility.
