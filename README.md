# Canonical Pure SSZ Metric

**Version:** `v1.1.0-canonical-pure`  
**License:** Anti-Capitalist Software License v1.4  
**Authors:** Carmen N. Wrede & Lino Casu  

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
│       ├── nicer_fetch.py       # HEASARC catalog parser & downloader
│       ├── alma_fetch.py        # ALMA catalog parser & downloader
│       ├── external_parameter_manifest.py # Independent target parameter loading
│       ├── external_exact_comparison.py    # Metric exact comparison standard
│       ├── external_prediction_bindings.py # Canonical prediction bindings
│       ├── external_observable_derivation.py # Deterministic observable extraction
│       ├── external_countertests.py        # 10-rule anti-circular orchestrator
│       ├── external_countertest_report.py  # Report markdown & JSON compilers
│       └── repo_consistency.py  # Core purity verification engine
├── scripts/                     # CLI fetch and gauntlet runners
├── external_validation/         # Parameters, data manifests & benchmarks
├── comparison/                  # GR comparisons (isolated reference code)
├── legacy/                      # Legacy/comparison models (isolated)
├── tests/                       # Complete pytest suite (26 internal files)
├── tests_external/              # Astroquery contract tests (9 files)
├── tests_external_countertests/ # Exact countertest and negative controls (11 files)
└── pyproject.toml               # Unified PEP 517 build configuration
```

---

## 🛠️ Installation & Usage

### 1. Installation
Install the package locally in editable mode to bind the path structure:
```bash
python -m pip install -e .
```

To install optional developer, visualization, and external astroquery dependencies:
```bash
python -m pip install -e ".[dev,viz,external-data]"
```

### 2. Running Verification Tests
Execute the comprehensive verification test suite verifying all identities, determinants, weak-field PPN limits, and strict core isolation:
```bash
python -m pytest -q
```

To run the external pipeline contract and manifest-schema tests:
```bash
python -m pytest tests_external -q
```

---

## 🔭 Fetching & Validating NICER and ALMA Data

The framework contains optional pipelines to fetch public raw astrophysical files and test them forward in an anti-circular manner. Real external data are not downloaded automatically.

### 1. Querying & Manifesting Data
To search HEASARC's `nicermastr` catalog and generate a safe local dry-run manifest:
```bash
python scripts/fetch_nicer.py --target "PSR J0030+0451" --search-only
python scripts/fetch_nicer.py --target "PSR J0030+0451" --max-rows 3 --dry-run
```

To search ALMA Science Archive for high-resolution FITS products:
```bash
python scripts/fetch_alma.py --target "M87" --search-only --max-rows 10
python scripts/fetch_alma.py --target "M87" --product-type fits --max-files 5 --dry-run
```

### 2. Download Execution (Confirmations & Size Guards)
Downloading requires explicit authorizations (`--confirm-download`) and obeys size guards (`--max-gb`):
```bash
python scripts/fetch_nicer.py --manifest external_validation/manifests/nicer/j0030.json --download --confirm-download --max-gb 5
python scripts/fetch_alma.py --manifest external_validation/manifests/alma/m87_fits.json --download --confirm-download --max-gb 10
```

### 3. Running the Metric Countertest Gauntlet (Exact Mode)
To run exact forward replays verifying prior verified numerical SSZ benchmark identities:
```bash
python scripts/run_exact_benchmark_replay.py --benchmark external_validation/countertests/benchmarks/exact_benchmark_observables.json --output EXACT_BENCHMARK_REPLAY_REPORT.md
```

To execute the complete NICER/ALMA External Metric Countertest Gauntlet:
```bash
python scripts/run_external_metric_countertests.py --nicer-manifest external_validation/manifests/nicer/nicer_manifest.json --alma-manifest external_validation/manifests/alma/alma_manifest.json --parameter-manifest external_validation/countertests/parameter_manifest.json --observable all --comparison-mode exact --output EXTERNAL_METRIC_COUNTERTEST_REPORT.md
```

*Note: Real-data external validation gates can be marked as PASS only if data manifests exist, the anti-circular conditions are fully satisfied, and no fitting parameters are used. Otherwise, missing data produces a SKIP status.*

---

## ⚠️ Current Limitations

The kanonische SSZ-Metrik ist als Xi-primärer Core vollständig definiert und für die dokumentierten Observablenklassen forward/antizirkulär testbar. Für dynamische, rotierende, mehrkörper-, quanten- und engineeringbezogene Usecases ist sie ein Ausgangspunkt, aber noch keine vollständige Lösung.

This repository implements a canonical Xi-primary SSZ metric research framework. It does not claim physical source formation, nonlinear stability, complete external observational proof, physical beaming, or engineering feasibility.
