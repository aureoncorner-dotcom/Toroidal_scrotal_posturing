"""Run the two suites separately, preserve baseline bytes, write a new receipt."""

import argparse
import hashlib
import importlib
import io
import json
import platform
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_baseline(manifest):
    result = {}
    for name, expected in manifest["source_sha256"].items():
        path = ROOT / name
        actual = sha256(path) if path.is_file() else None
        result[name] = {"expected": expected, "observed": actual, "match": actual == expected}
    return result


def run_suite(module, output):
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromName(module)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    log = stream.getvalue()
    output.write_text(log, encoding="utf-8", newline="\n")
    return {
        "module": module,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "unexpected_successes": len(result.unexpectedSuccesses),
        "all_passed_without_skips": bool(result.testsRun) and result.wasSuccessful()
            and not result.skipped and not result.expectedFailures,
        "output_file": output.name,
        "output_sha256": sha256(output),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new directory for this run")
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        parser.error("--output must be a new directory; previous receipts are preserved")
    out.mkdir(parents=True)
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(ROOT))
    manifest = json.loads((HERE / "baseline.json").read_text(encoding="utf-8"))
    receipt = {
        "schema": "corner-relay-c6/adversarial-execution/v1",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_commit": manifest["upstream_commit"],
        "runtime": {"python": sys.version, "platform": platform.platform(), "executable": sys.executable},
        "invocation": sys.argv,
        "baseline_before": check_baseline(manifest),
        "extension_sha256": {p.name: sha256(p) for p in sorted(HERE.iterdir()) if p.is_file()},
        "authentication_implementation_status": "NOT_IMPLEMENTED_NOT_VERIFIED",
        "claim_boundary": "Passing adversarial tests characterize reference behavior; they do not certify authentication.",
    }
    valid = all(row["match"] for row in receipt["baseline_before"].values())
    if valid:
        receipt["original_acceptance"] = run_suite("test_corner_relay", out / "original_acceptance.txt")
        receipt["adversarial_extension"] = run_suite(
            "extensions.c6_sender_authentication.test_sender_authentication",
            out / "adversarial_extension.txt",
        )
        probe = importlib.import_module("extensions.c6_sender_authentication.reproduce_unsigned_ack")
        observation = probe.build_observation()
        observation_path = out / "unsigned_ack_observation.json"
        observation_path.write_text(json.dumps(observation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        receipt["observation_sha256"] = sha256(observation_path)
        trace = importlib.import_module("reference_trace")
        # Use a scratch destination; do not overwrite the frozen reference trace.
        with tempfile.TemporaryDirectory(prefix="c6-auth-trace-") as scratch:
            regenerated = Path(scratch) / "reference_trace.json"
            trace.write_reference_trace(regenerated)
            # The original uses platform text newlines; compare canonical LF bytes.
            regenerated_lf = regenerated.read_bytes().replace(b"\r\n", b"\n")
            receipt["reference_trace_matches_frozen_lf_bytes"] = regenerated_lf == (ROOT / "reference_trace.json").read_bytes()
        valid = (
            receipt["original_acceptance"]["all_passed_without_skips"]
            and receipt["original_acceptance"]["tests_run"] == 20
            and receipt["adversarial_extension"]["all_passed_without_skips"]
            and receipt["adversarial_extension"]["tests_run"] == 7
            and receipt["reference_trace_matches_frozen_lf_bytes"]
        )
    receipt["baseline_after"] = check_baseline(manifest)
    valid = valid and all(row["match"] for row in receipt["baseline_after"].values())
    receipt["status"] = "REFERENCE_BOUNDARY_REPRODUCED" if valid else "REVIEW_FAILED"
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    receipt_path = out / "execution_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "receipt": str(receipt_path)}, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
