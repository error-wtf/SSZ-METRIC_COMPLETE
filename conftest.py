"""
Pytest configuration - NO FAKER ALLOWED.
This file runs before any tests and ensures faker is never loaded.
"""
import sys
import pytest

# Block faker from being imported ever
class FakerBlocker:
    """Blocks faker imports to prevent reputation damage."""
    def find_module(self, fullname, path=None):
        if 'faker' in fullname.lower():
            raise ImportError(f"FAKER IS FORBIDDEN: {fullname} - "
                            "This project uses ONLY calculated physical values, "
                            "never fake/generated data!")
        return None

# Install the blocker
sys.meta_path.insert(0, FakerBlocker())

# Also remove faker from pytest plugins if it was loaded
if 'faker' in sys.modules:
    del sys.modules['faker']
if 'Faker' in sys.modules:
    del sys.modules['Faker']

print("[OK] Anti-Faker blocker installed - faker is FORBIDDEN in this project")


def _ssz_explanation(nodeid):
    """Return a bilingual evidence contract for every Complete-Metric test."""
    key = nodeid.lower()
    if "external" in key or "fetch" in key or "manifest" in key:
        return (
            "EXTERNE DATEN- UND PROVENIENZPRÜFUNG", "EXTERNAL DATA AND PROVENANCE CHECK",
            "Prüft Datenvertrag, Herkunft, Trennung von Vorhersage und Beobachtung sowie Anti-Zirkularität.",
            "Checks the data contract, provenance, prediction/observation separation, and anticircularity.",
            "Bestätigt den erklärten Daten- oder Schnittstellenvertrag innerhalb der Testeingaben.",
            "Verifies the declared data or interface contract within the test inputs.",
            "Ein bestandener Vertrag ersetzt keine unabhängige wissenschaftliche Replikation des Quelldatensatzes.",
            "A passing contract does not replace independent scientific replication of the source dataset.")
    if "tensor" in key or "curvature" in key or "source" in key or "stability" in key:
        return (
            "SSZ-TENSOR-/QUELLEN-/STABILITÄTSREGRESSION", "SSZ TENSOR/SOURCE/STABILITY REGRESSION",
            "Prüft die aus der vollständigen SSZ-Metrik berechnete geometrische oder dynamische Struktur.",
            "Checks geometric or dynamical structure calculated from the complete SSZ metric.",
            "Bestätigt Formelstruktur, numerische Ausführung und die im Einzeltest angegebenen Invarianten.",
            "Verifies formula structure, numerical execution, and the invariants declared by the individual test.",
            "Tensor- oder Stabilitätskonsistenz ist eine Modellprüfung und allein keine empirische Bestätigung der Natur.",
            "Tensor or stability consistency is a model check and alone is not empirical confirmation of nature.")
    if "shapiro" in key or "deflection" in key or "observable" in key or "ppn" in key:
        return (
            "SSZ-OBSERVABLEN- UND METHODENPRÜFUNG", "SSZ OBSERVABLE AND METHOD CHECK",
            "Prüft Observable→Klasse→SSZ-Methode sowie den daraus vorwärts berechneten Referenzwert.",
            "Checks observable-to-class-to-SSZ-method routing and the resulting forward reference value.",
            "Bestätigt die kanonische SSZ-Auswertungsroute und das jeweils deklarierte Toleranzfenster.",
            "Verifies the canonical SSZ evaluation route and the declared tolerance window.",
            "PPN-Übereinstimmung im gemeinsamen Grenzbereich beweist keine eindeutige Abgrenzung gegenüber Alternativmodellen.",
            "PPN agreement in a shared limiting regime does not prove unique separation from alternative models.")
    if "metric" in key or "christoffel" in key or "geodes" in key:
        return (
            "VOLLSTÄNDIGE SSZ-METRIKREGRESSION", "COMPLETE SSZ METRIC REGRESSION",
            "Prüft Metrikkomponenten, Ableitungen, Verbindung, Inverse oder Determinante aus dem Primärfeld Xi.",
            "Checks metric components, derivatives, connection, inverse, or determinant generated from primary Xi.",
            "Bestätigt die im Einzeltest benannte mathematische Eigenschaft der vollständigen SSZ-Metrik.",
            "Verifies the mathematical property of the complete SSZ metric named by the individual test.",
            "Eine Metrikidentität ist interne Modellkonsistenz; experimentelle Gültigkeit benötigt unabhängige Observable.",
            "A metric identity is internal model consistency; empirical validity requires independent observables.")
    if "phase" in key or "frequency" in key or "clock" in key or "qubit" in key or "em_" in key:
        return (
            "SSZ-PHASEN-/FREQUENZREGRESSION", "SSZ PHASE/FREQUENCY REGRESSION",
            "Prüft die SSZ-Kette Xi→D/s→Frequenz, Phase, Uhr oder elektromagnetische Skalierung.",
            "Checks the SSZ chain Xi to D/s to frequency, phase, clock, or electromagnetic scaling.",
            "Bestätigt die berechnete Phasen- oder Ratengleichung für die ausgegebenen Eingaben.",
            "Verifies the calculated phase or rate equation for the printed inputs.",
            "Ein synthetischer oder abgeleiteter Phasenwert ist ohne unabhängige Messung keine empirische Validierung.",
            "A synthetic or derived phase value is not empirical validation without an independent measurement.")
    if "strong" in key or "neutron" in key or "energy" in key:
        return (
            "SSZ-STARKFELD-/KOMPAKTHEITSDIAGNOSTIK", "SSZ STRONG-FIELD/COMPACTNESS DIAGNOSTIC",
            "Prüft endliche SSZ-Grenzwerte, Kompaktheit oder ausdrücklich als Proxy deklarierte Energiebedingungen.",
            "Checks finite SSZ limits, compactness, or energy conditions explicitly declared as proxies.",
            "Bestätigt den implementierten SSZ-Modellwert und seine numerische Aussagegrenze.",
            "Verifies the implemented SSZ model value and its numerical scope.",
            "Diagnostik und Modellregression sind keine unabhängige Starkfeld- oder Neutronensternmessung.",
            "Diagnostics and model regressions are not independent strong-field or neutron-star measurements.")
    return (
        "SSZ-KERN-/INTEGRITÄTSPRÜFUNG", "SSZ CORE/INTEGRITY CHECK",
        "Prüft den durch die Test-ID und den Testtitel bezeichneten kanonischen SSZ-Vertrag.",
        "Checks the canonical SSZ contract identified by the test ID and title.",
        "Bestätigt die Assertions und berechneten Werte des Einzeltests.",
        "Verifies the assertions and calculated values of the individual test.",
        "PASS gilt ausschließlich für die gedruckten Eingaben, Formeln, Toleranzen und Evidenzklasse.",
        "PASS applies only to the printed inputs, formulas, tolerances, and evidence class.")


def pytest_runtest_setup(item):
    category_de, category_en, why_de, why_en, verified_de, verified_en, boundary_de, boundary_en = _ssz_explanation(item.nodeid)
    title = (getattr(item, "obj", None).__doc__ or item.name).strip().replace("\n", " ")
    print(f"\n  {'=' * 116}")
    print(f"  SSZ-EINZELTEST / SSZ INDIVIDUAL TEST: {item.nodeid}")
    print(f"  TITEL / TITLE: {title}")
    print(f"  TYP / TYPE: {category_de} / {category_en}")
    print("  EINGABEN UND BERECHNETE WERTE / INPUTS AND CALCULATED VALUES:")
    print("  (Das originale Testprotokoll folgt unverändert. / The original test output follows unchanged.)")
    print(f"  {'-' * 116}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    category_de, category_en, why_de, why_en, verified_de, verified_en, boundary_de, boundary_en = _ssz_explanation(item.nodeid)
    status = "PASS" if report.passed else ("SKIP" if report.skipped else "FAIL")
    print(f"  {'-' * 116}")
    print(f"  ERGEBNIS / RESULT: {status}")
    print(f"  WARUM (DE): {why_de}")
    print(f"  WHY (EN): {why_en}")
    print(f"  GEPRÜFTE AUSSAGE (DE): {verified_de}")
    print(f"  VERIFIED STATEMENT (EN): {verified_en}")
    print(f"  AUSSAGEGRENZE (DE): {boundary_de}")
    print(f"  CLAIM BOUNDARY (EN): {boundary_en}")
    print(f"  {'=' * 116}")
