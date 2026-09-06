# Toroidal Geometry v1.0

**Consolidated mathematics, exact lattice validation, and curved-throat kinematics**  
6 September 2026

Start with [the core update](00_TOROIDAL_GEOMETRY_v1.0.md). This release turns the toroidal corrections in Geometry Maximization v2.0 into one coordinated reference packet, with runnable examples and preserved sources.

The new executable checks finite toroidal currents, membranes, sectors and operator records. The throat executable checks a circular curved tube against conservation and material tangency. These are mathematical reference computations. Q1, Q2, Q3 and the empirical throat comparison remain `NOT_RUN` in this release.

| Open | Purpose |
|---|---|
| [Core update](00_TOROIDAL_GEOMETRY_v1.0.md) | What changed and what the results mean |
| [Field theory](01_Field_Theory_Update_v0.4_Consolidated.md) | One set of definitions for winding, sources and ensembles |
| [Protocol](02_Simulation_Protocol_v0.6_Consolidated.md) | Run the validator; understand its limits and production requirements |
| [Exact lattice appendix](03_Appendix_A_v0.3_Exact_Lattice.md) | Proofs, rectangular tori and modular currents |
| [Accessibility appendix](04_Appendix_B_v0.3_Accessibility_Mixing.md) | Paths, clocks, closure and counterexamples |
| [Curved throat](05_TTSC_1_v0.4_Curved_Throat.md) | Metric, corrected velocity, material and fixed-radius charts |
| [Integration manifest](15_Integration_Manifest_v0.3.md) | Every successor and its predecessor |
| [Verification receipt](VERIFICATION_RESULTS.json) | Actual test counts, example comparisons and numerical residuals |

## Run locally

Python 3.10 or later; the validator, throat computations and verification suite use only the standard library. The optional figure generator uses Matplotlib. Open a terminal in this extracted release folder. Replace `python` with your Python executable if needed. Output folders must not already exist.

```text
python -B reference/lattice_validator.py --config configs/rectangular.json --out my-lattice-run
python -B reference/lattice_validator.py --state examples/rectangular/state_input.json --out my-state-check
python -B reference/throat.py --config configs/throat.json --out my-throat-run
python -B verify_release.py
```

The last command checks packaged hashes, runs the tests, and reproduces the six included examples in a temporary folder. It leaves frozen examples untouched. Extra user output folders are allowed; unexpected files are listed, while unexpected executable code on the reference import path fails verification. Exit status zero means the declared reference checks passed. It does not certify a physical field theory.

Three lattice fixtures cover a cube, a rectangular torus and a translated reference origin. Three throat fixtures cover the throat, flat control and translated throat. The [figure](figures/curved_throat.png) summarizes the baseline throat profile; its numbers are in [the CSV](examples/throat/throat_profile.csv).

The intact [Geometry Maximization v2.0 archive](baseline/GEOMETRY_MAXIMIZATION_v2.0.zip) preserves the earlier phase explorer, reference simulator, proofs and nested source archives. Selected readable baseline documents and fifteen original toroidal documents are also included. Use the intact archive for the baseline documents' original link context. Original files were not edited. Hashes establish which bytes are present; they do not supply an external pre-output trust anchor.
