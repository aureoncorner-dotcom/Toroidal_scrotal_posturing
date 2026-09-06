# Geometry Maximization v2.0

The exact phase model is now packaged as a concise document and a working reference simulator. The field-theory and simulation documents have matching, scoped amendments.

**Start here:** open [EXPLORER.html](EXPLORER.html) in a browser. It works offline and shows the supplied exact runs, the coordinate approximation, slip events and any numerical label mismatches. No installation is needed to explore those runs.

## Read

- [Geometry Maximization v2.0](GEOMETRY_MAXIMIZATION_v2.0.md): the operational core.
- [Field Theory Update v0.3](FIELD_THEORY_UPDATE_v0.3.md): the applicable toroidal changes.
- [Simulation Protocol v0.5](SIMULATION_PROTOCOL_v0.5.md): inputs, outputs, error contract and future field requirements.
- [Technical appendix](TECHNICAL_APPENDIX_v2.0.md): formulas and a map to the preserved proofs.
- [Release report](RELEASE_REPORT_v2.0.md): what was checked and what remains unresolved.
- [Change log](CHANGELOG_v2.0.md) and [evidence ledger](EVIDENCE_LEDGER_v2.0.json).

## Generate your own run

Use Python 3.10 or later; only its standard library is required. From this extracted package folder:

```text
python -B simulator/geometry_reference.py --config simulator/configs/default_507.json --out my_runs/default_507
```

On Windows, `py -3` can replace `python` if that is how your Python installation is launched. The executable refuses to overwrite an existing run. Choose a new output folder for a new run.

To change the start, length or warp, copy one of the small configuration files and edit its three values. For example:

```json
{
  "steps": 507,
  "theta0": "1/7",
  "epsilon": "0.01"
}
```

Phases are cycles, `steps` counts departures, and decimal values in exact fields use quotes. `theta0` can also be `{"a":"-29/26","b":"1/2"}` to start exactly at the slip threshold divided by 39. The [protocol](SIMULATION_PROTOCOL_v0.5.md) lists all limits.

Each run creates `run.json`, `summary.json`, `trace.csv` and checksums. Load its `run.json` with the explorer's **Load a run** button. The browser displays generated data; it does not certify a file's provenance or recompute the exact dynamics.

## Reproduce the release checks

```text
python -B verify_release.py
```

This runs the ten reference tests, checks the preserved baseline archive and regenerates all five included runs in temporary folders. It compares the exact states and labels, and checks numerical reproducibility on the executing platform. To save a new receipt outside the frozen release files:

```text
python -B verify_release.py --receipt my_verification.json
```

The command performs no network calls and launches no field production job. Minor numerical-library differences on another platform can affect floating boundary labels; any such discrepancy must be reported and examined, while exact phase labels should reproduce unchanged.

## Interpret the result

Exact phase labels and the telescoping slip-count identity are the reference. The ideal approximation certificate has a proved error bound. The actual floating coordinate trajectory is a separate numerical check, with its mismatches visible. The package does not establish deconfinement, a critical exponent, a physical central charge or a new empirical success.

The full [v1.6 document](baseline/GEOMETRY_MAXIMIZATION_v1.6.md), [source review](baseline/GEOMETRY_MAXIMIZATION_v1.6_SOURCE_REVIEW.md) and [verification archive](baseline/GEOMETRY_MAXIMIZATION_v1.6_verification.zip) are preserved byte-for-byte. Your original source files and previous releases remain separate and unchanged.
