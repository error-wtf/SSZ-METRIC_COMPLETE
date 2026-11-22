# ERRATA & STATUS-UPDATE — 23.11.2026

**Autor:** Bingsi (Hermes Agent) im Auftrag von Lino Casu
**Anlass:** P5-Wurzelläulösung (C₆/c₂-Fehlerkette) und Grid-Adjudikation vom 22./23.11.2026
**Charakter:** Append-only Erratum. Die historischen Dokumente dieses Repos bleiben
unverändert als Prüfspur stehen. Dieses Dokument markiert, welche Interpretationen
überholt sind und wo die maßgeblichen aktuellen Dokumente liegen.

---

## 1. D_min = 0.555 — Uhren-Konzept, KEIN räumlicher Mindestradius

In mehreren Dokumenten dieses Repos wird D(r_s) ≈ 0.555 als „Abbrechregel" der
SSZ referenziert. Präzisierung vom 22.11.2026:

- **D = 1/(1+Ξ) ist der Dilatationsfaktor (Uhrenverhältnis)** bei r = r_s.
- D_min = 0.555 ist eine Aussage über das **Skalierungsverhalten**, nicht eine
  untere Schranke des arealen Radius.
- **Es existiert bislang keine dokumentierte Herleitung eines physikalischen
  Innenrandes (r_min > 0) aus den SSZ-Segmentpostulaten.** Die numerischen
  Gittergrenzen (r_min = 0.05 bzw. r₀ = 0.01) sind Integrations-/Grid-Wahlen,
  keine physikalischen Ränder.
- Jede Verwendung von D_min als Argument für eine räumliche Randbedingung ist
  bis zur Herleitung aus einer erzeugenden Segmentdynamik (offen, P3.4)
  **unzulässig**.

## 2. P5-Kette (22.11.2026): C₆-Implementierungsfehler nachgewiesen

Der Hintergrundgenerator der P5-V5-Kette verwendete in C₆
G₄,φ statt G₄,φφ (arXiv 2301.10362, Gl. 2.10). Für die neutrale Kopplung
(G₄,φ = −1/2, G₄,φφ = 0) fügt der Fehler den unzulässigen Term ΔC₆ = h(φ′)² hinzu.

Konsequenzen (alle maschinell verifiziert, siehe SSZ_FINAL_CLOSURE_20261122
und /home/error/physics/work/p5_v5_action_audit/):

- Der archivierte P5-Hintergrund ist **off shell** (max |E_tt| ≈ 1.91·10⁻³ vs.
  Integrator-Genauigkeit 5·10⁻¹⁴).
- Der zusätzliche „schnelle Zweig" des archivierten Operators hat **keinen
  physikalischen Kegel** der deklarierten Wirkung (analytisch: Hauptsymbol,
  5 Polarisationen auf dem metrischen Nullkegel, modellkonkret für G₂=X).
- Die isolierte c₂-Korrektur (fehlender Appendix-A-Beitrag) verschiebt die
  auffällige Wurzel am Knoten 2000 von 15.70 auf 0.64.
- **Historische Interpretationen der Velocity-Zweige (15.7×, 31.6×) beruhen
  auf fehlerhaften Gleichungen und sind als physikalische Entdeckungen
  zurückzuziehen.** Die reproduzierbare Zahl war eine Eigenschaft des
  fehlerbehafteten Codes, nicht der Wirkung.

## 3. Grid-Adjudikation (23.11.2026)

Die Diskrepanz 56 vs. 1751 negativer kinetischer Richtungen auf dem korrigierten
Hintergrund ist als **GRID_SAMPLING_DIFFERENCE: VERIFIED** klassifiziert (das
NPZ-Archiv-Grid ist radial ~50× feiner als das uniforme Vergleichsgitter).
Die Klassifikation der Zusatz-Richtungen als NUMERICAL_ARTIFACT ist
**noch nicht abgeschlossen** (NOT YET PROVEN); der Konvergenztest an identischen
Radien steht aus. Keine Ghost-Instabilität der Wirkung: Im Einstein-Frame
(F>0, Z_E>0 verifiziert) ist die Wirkung minimal, alle even-Freiheitsgrade
haben positive zeitliche Kinetik per Konstruktion.

## 4. Maßgebliche aktuelle Dokumente

- `/home/error/physics/SSZ_FINAL_CLOSURE_20261122/` — Abschlussarchiv (17 Final-Reports)
- `/home/error/physics/work/p5_v5_action_audit/` — C₆/c₂-Adjudikation, FLUX_NOGO_ERRATUM
- `/home/error/physics/work/p5_root_cause_repair/` — Phase 1 (Root-Cause-Diagnose)
- `/home/error/physics/work/phase2_action_reconstruction/` — Phase 2 (Inertia-Gate,
  Grid-Auflösung, Eliminierungs-Identitäts-Audit, Einstein-Frame-Kinetik)
- `FORSCHUNGSGRUNDLAGE_VERBINDLICH.md` (im SSZ_FULL_AUDIT_20261105-Archiv) —
  bindende Trennung historisch/Postulat/bewiesen

## 5. Grundsatz

Die Mathematik entscheidet, nicht die Autorität früherer Texte. Dieses Repo ist
ein historischer Stand (13./14.10.2026, heads 737644a bzw. 4f54020). Errata
werden append-only geführt; zurückgenommene Behauptungen werden gekennzeichnet,
nicht gelöscht.

Copyright Lino Casu. Anti-Capitalist License.
