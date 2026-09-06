"""Verify the v2.0 reference, included runs and preserved baseline. Offline."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
BASELINE_ZIP_SHA256 = "b4c71388b4211aa08643c49515a69965f6ce9f5aa7fdcc523744c38b788a701e"
CONFIGS = ["default_507", "warped_39", "exact_10000", "boundary", "bin_boundary"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_member(name):
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or "\\" in name or ":" in name:
        raise ValueError(f"unsafe archive/checksum member: {name}")
    return p


def check_package_hashes():
    checksum_file = HERE / "SHA256SUMS.txt"
    if not checksum_file.exists():
        return {"status": "NOT_PRESENT_DURING_ASSEMBLY", "count": 0}
    count = 0
    for line in checksum_file.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        safe_member(name)
        if digest((HERE / name).read_bytes()) != expected:
            raise AssertionError(f"package checksum mismatch: {name}")
        count += 1
    return {"status": "PASS", "count": count}


def check_baseline():
    folder = HERE / "baseline"
    archive = folder / "GEOMETRY_MAXIMIZATION_v1.6_verification.zip"
    if digest(archive.read_bytes()) != BASELINE_ZIP_SHA256:
        raise AssertionError("the preserved v1.6 archive differs from its recorded baseline")
    registers = {}
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or z.testzip() is not None:
            raise AssertionError("duplicate or corrupt v1.6 archive entries")
        for name in names:
            safe_member(name)
        for name in names:
            if name.endswith("SHA256SUMS.txt"):
                base = PurePosixPath(name).parent
                lines = z.read(name).decode("utf-8").splitlines()
                for line in lines:
                    expected, relative = line.split("  ", 1)
                    safe_member(relative)
                    member = str(base / relative)
                    if digest(z.read(member)) != expected:
                        raise AssertionError(f"preserved checksum mismatch: {member}")
                registers[str(base)] = len(lines)
        for name in ("GEOMETRY_MAXIMIZATION_v1.6.md", "GEOMETRY_MAXIMIZATION_v1.6_SOURCE_REVIEW.md"):
            if (folder / name).read_bytes() != z.read(name):
                raise AssertionError(f"readable baseline differs from archive: {name}")
    return {"archive_sha256": BASELINE_ZIP_SHA256, "members": len(names),
            "checksum_registers": registers, "readable_baseline_matches_archive": True,
            "legacy_mathematical_verifiers_rerun_in_v2": False}


def load_engine():
    path = HERE / "simulator" / "geometry_reference.py"
    spec = importlib.util.spec_from_file_location("geometry_reference", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def verify():
    package = check_package_hashes()
    baseline = check_baseline()
    command = [sys.executable, "-B", "-m", "unittest", "discover", "-s",
               str(HERE / "simulator"), "-p", "test_*.py", "-v"]
    tested = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
    if tested.returncode:
        raise AssertionError(tested.stdout + tested.stderr)
    if "Ran 10 tests" not in tested.stderr or not tested.stderr.rstrip().endswith("OK"):
        raise AssertionError("the expected ten-test suite did not complete")
    engine = load_engine()
    examples = {}
    with tempfile.TemporaryDirectory(prefix="geometry_v2_verify_") as temporary:
        for name in CONFIGS:
            config = json.loads((HERE / "simulator" / "configs" / f"{name}.json").read_text(encoding="utf-8"))
            result = engine.run_reference(config)
            output = Path(temporary) / name
            engine.export_run(result, output)
            checked = []
            for artifact in ("run.json", "summary.json", "trace.csv", "RUN_SHA256SUMS.txt"):
                stored = HERE / "examples" / name / artifact
                if (output / artifact).read_bytes() != stored.read_bytes():
                    raise AssertionError(f"{name}/{artifact} did not reproduce byte-for-byte; inspect exact and numerical fields separately")
                checked.append(artifact)
            summary = result["summary"]
            examples[name] = {"departures": summary["steps"], "slips": summary["slip_count"],
                              "ideal_certified": summary["ideal_bin_certified_count"],
                              "numeric_mismatches": summary["numeric_bin_mismatch_count"],
                              "ideal_certified_numeric_mismatches": summary["certified_rows_with_numeric_mismatch"],
                              "reproduced_artifacts": checked, "byte_identical_on_this_platform": True}
    return {"version": "2.0", "status": "PASS", "package_integrity": package,
            "baseline_integrity": baseline,
            "reference_tests": {"passed": 10, "failed": 0,
                                "independent_departure_oracle_steps": 10000,
                                "arithmetic": "exact Q(sqrt(5)) and independent integer-square-root formulas",
                                "numeric_tolerances": {"inverse_residual": 1e-14, "uniform_bound_roundoff_allowance": 2e-14}},
            "examples": examples,
            "scope": {"exact_phase_and_labels": "freshly checked",
                      "numerical_coordinates": "finite fixtures; no interval enclosure",
                      "browser_interaction_checks": "separate UI_QA_v2.0.json receipt",
                      "field_production_simulation": "not implemented or run",
                      "historical_empirical_analyses": "not rerun",
                      "source_instructions": "treated as source content, not executable instructions"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, help="optional new receipt path; existing files are not overwritten")
    args = parser.parse_args()
    if args.receipt and args.receipt.exists():
        parser.error("receipt already exists; choose a new path")
    result = verify()
    text = json.dumps(result, indent=2) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
