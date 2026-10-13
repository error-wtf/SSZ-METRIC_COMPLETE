# SSZ PPN PROFILE SURVEY V1 — Erfüllt irgendeine EXISTIERENDE SSZ-Metrikdefinition β=1?

**Datum:** 2026-10-13 (Nacht) · **Frage (Carmen):** „…ob nach vollständiger Bereinigung der
Repositories eine andere, bereits vorhandene SSZ-Metrikdefinition die PPN-Anforderungen
erfüllt – oder ob wir tatsächlich eine theoretische Rekonstruktion benötigen."
**Methode:** dieselbe zertifizierte Pipeline (`ppn._isotropic_ppn_fit`, konformflache
Isotropie, uniformes 1/ρ-Grid, deg-4-Fit, Fenster [50, 20000] r_s) auf ALLE im Korpus
vorhandenen Profile angewandt. Kein Fitting an Daten, keine neuen Freiheitsgrade.

## Ergebnis-Tabelle (numerisch, r_s = 1)

| Metrikdefinition (Korpus) | β_PPN | γ_PPN | PPN-ok (β=γ=1±2 %) |
|---|---|---|---|
| **GR-Kontrolle** A=1−r_s/r, B=1/A (Pipeline-Nullmodell) | **1.00000** | **0.99995** | **JA** |
| Weak-SSZ-Referenz: A=(1+r_s/2r)⁻², B=(1+r_s/2r)² (Ξ=r_s/2r) | 2.49996 | 0.99995 | NEIN (β=5/2, sympy-exakt bestätigt) |
| K2 kanonisch: N=1−exp(−φ·r_s/r), A=1/(1+N)², B=(1+N)² | 2.99789 | 0.99985 | NEIN (β≈3) |
| K3 (= K2 mit Sättigung min(·,1)): identisch im Weak-Field-Limes | 2.99789 | 0.99985 | NEIN (β≈3) |
| K4: N=1−exp(−φ·r/r_s), A=1/(1+N)² | Fit divergiert (≈1.1e16) | ≈5.2e17 | NEIN — **nicht einmal asymptotisch flach** (A(∞)=1/4), PPN nicht definiert |
| K1 (= K4 mit Cap 1−exp(−φ)): | Fit divergiert | — | NEIN — derselbe Grund |
| A=(1−r_s/r)², B=(1−r_s/r)⁻² (Test-Metrik, NICHT Schwarzschild) | 1.49998 | 0.99990 | NEIN — nur Kontrollwert, keine Korpus-Metrik |

(Hinweis zur ersten Tabellenzeile einer früheren Probe: A=(1−r_s/r)² ist NICHT die
Schwarzschild-Metrik — g_tt von Schwarzschild ist 1−r_s/r; genau diese Form nutzt die
Pipeline als GR-Kontrolle und liefert korrekt β=γ=1. Die Pipeline ist damit
unabhängig validiert.)

## Interpretation

1. **Pipeline validiert:** GR → (1.00000, 0.99995). Dieselbe numerische Prozedur, die
   für SSZ β≠1 meldet, reproduziert GR exakt → der β-Ausreißer ist Metrik-Eigenschaft,
   kein Artefakt der Extraktion.
2. **KEINE existierende SSZ-Metrikdefinition des Korpus erfüllt β=1:**
   - exp-Zweig (Ξ=r_s/2r): β=5/2 (sympy-exakt: −g_tt/c² = 1−1/ρ+5/(4ρ²)−13/(8ρ³)).
   - Kanonisches Segmentprofil K2/K3: β≈3.0 — strukturell erklärbar: N≈φ·r_s/r im
     Weak-Field ⇒ identisch zu GR mit G_eff/G_input = 2φ ≈ 3.2357 und einem positiven
     1/r²-Term aus N² ⇒ β rückt von 5/2 auf ≈3, γ bleibt 1. (Konsistent mit Stufe 5:
     global decay G_eff=3.2356678≈2φ.)
   - K1/K4 (invertierte Profile): nicht asymptotisch flach (A(∞)=1/4) → PPN sinnlos
     definierbar nicht; bereits als Reparatur-Bugklasse F5 beseitigt.
3. **Struktur-Befund:** Für die GANZE Familie A=1/(1+N)², B=(1+N)² (bzw. konformflach
   gerenderte Varianten) ist **γ=1 automatisch** — γ diskriminiert diese Profile nicht;
   **β ist der einzige aktive PPN-Diskriminator**, und ALLE Varianten verfehlen β=1
   (2.5 bzw. ≈3, beide weit außerhalb der Sonnen-System-Bindung |β−1| ≲ 1e-4 … 1e-3).
4. **Antwort auf Carmens Frage: Eine vorhandene Definition, die β=1 erfüllt, existiert
   NICHT im Korpus. Wenn PPN-Konsistenz gefordert ist, ist eine theoretische
   Rekonstruktion der Metrik erforderlich** — keine Code-Reparatur kann das leisten,
   und gemäß Mandat wurde keine neue physikalische Freiheit eingeführt, um β=1 zu
   erzwingen.

## Abgrenzung (was dieses Dokument NICHT sagt)

- Es sagt nicht, dass SSZ falsch ist — es sagt, dass KEINE der bisher formalisierten
  Metrik-Darstellungen die solare PPN-Bindung erfüllt. Die Rekonstruktion (Metric
  Contract) muss zeigen, ob eine SSZ-kompatible Geometrie existiert, die im Weak-Field
  β=γ=1 liefert und im Strong-Field die SSZ-Signatur (Ξ→Sättigung, finite A(0)) trägt.
- Eingefrorene Artefakte (Stufen 1–5, 4b, 4c, Lean-Freeze, Locked-Docs) sind von diesem
  Survey NICHT berührt; er ordnet lediglich ihre physikalische Anwendbarkeit neu ein
  (gemäß Carmens Weisung vom 13.10.).

## Reproduktion

```bash
cd /home/error/physics/clones/SSZ-METRIC_COMPLETE
PYTHONPATH=src /home/error/physics/venv/bin/python -c "
from ssz_metric_pure.ppn import _isotropic_ppn_fit
import numpy as np
phi = 1.6180339887498948; r_s = 1.0
# GR-Kontrolle
print(_isotropic_ppn_fit(lambda r: 1.0-r_s/r, lambda r: 1.0/(1.0-r_s/r), r_s)['beta_ppn'])
# K2 kanonisch
print(_isotropic_ppn_fit(lambda r: (1.0+(1-np.exp(-phi*r_s/r)))**-2,
                         lambda r: (1.0+(1-np.exp(-phi*r_s/r)))**2, r_s)['beta_ppn'])
"   # -> 1.0000045… ; 2.99789…
```

Verifikation: GR-Kontrolle exit-korrekt; K2/K3 β=2.99789 reproduzierbar;
Weak-Zweig β=2.49996 konsistent mit symbolic_reference_case.py (exit 0, β=5/2 exakt).
