# Corner Relay α — C6 deterministic reference artifact v0.1

Track used: **Python 3 code plus tests**. The implementation uses only the Python standard library.

## Frozen scope

This bundle implements the core transition relation from the frozen ACSB v0.1 packet. It preserves two independent endpoints (`O`, `S`), exactly two structural key slots, a route-only `LambdaTransport`, no tie-breaker, no winner selection, no third key, append-only RAW witnesses, and deterministic derived VIEWs. `FROZEN_PACKET.txt` contains the exact packet clauses and C6 prompt used; `source_binding.json` binds them to the two Drive source records.

The key slots are a mechanically enforced ownership model, not production cryptography. This artifact therefore checks actor/key separation and content integrity, but it does not claim real-world sender authentication or identify any hidden source or mechanism.

## Explicit transition relation

| Transition | Preconditions | Actor/input | Resulting operational effect | RAW witness behavior |
|---|---|---|---|---|
| `SEND` | endpoint active; transition ID unused; target is peer | endpoint; opaque bytes | one content-addressed SEND effect | append accepted record |
| exact `SEND` retry | transition ID already bound to identical event | same endpoint; identical input | no second effect; return prior event | append duplicate/retry record |
| explicit `RETRY` | transition ID names prior local event; endpoint active (or existing EXIT) | owning endpoint; transition ID | no second effect; return prior event | append retry record |
| `RECEIVE_SEND` | endpoint active; target/actor/key/hash valid | target endpoint; full event | one received SEND effect | append every delivery, including duplicates |
| `ACK` | endpoint active; referenced SEND exists in accepted local RAW | receiving endpoint; SEND event ID | one ACK effect owned by acknowledger | append accepted record |
| `RECEIVE_ACK` | endpoint active; ACK references a SEND created locally | original sender; full ACK event | one received ACK effect | append every delivery, including duplicates |
| `EXIT` | endpoint active; transition ID unused | exiting endpoint; empty input | endpoint becomes inactive | append EXIT; retain all earlier RAW |
| rejected attempt | any precondition fails | attempted actor/input | no operational effect | append rejection and reason |

Every RAW record names its precondition, actor/key slot, exact input record and hash, transition ID, full before/after VIEW records and hashes, result, stable witness ID, and previous-witness link. The links make retained order mechanically checkable. A duplicate or rejected attempt can enlarge RAW while leaving the operational VIEW hash unchanged.

## Expected network behavior

- Duplicate deliveries remain visible in RAW and collapse to one local effect in VIEW.
- All tested permutations of independent deliveries converge to the same deterministic VIEW while RAW preserves the actual order.
- A partition retains queued events without causing an endpoint transition; delivery resumes after the partition is lifted.
- Lambda routes only to the event's declared target. It has no key, payload parser, arbitration method, commit method, or endpoint mutation authority.
- Exit is local. It retains history, blocks later participation by that endpoint, and neither exits nor authorizes the peer.

## Run and verify

From this directory:

```bash
python3 run_with_provenance.py
```

The runner executes the complete `unittest` suite, generates `reference_trace.json`, and writes `execution_provenance.json` with the exact command, UTC start/finish, runtime, test count, captured output, source binding, trace hash, and SHA-256 hashes of the frozen packet, code, tests, runner, and documentation. The record states `PASS` only when the test process returns zero.

## Files

- `corner_relay.py` — deterministic transition artifact, lossless RAW export, and hash-chain verifier
- `test_corner_relay.py` — acceptance, failure-path, retry, duplicate, reorder, partition, exit, key-boundary, and RAW/VIEW tests
- `run_with_provenance.py` — test runner and execution-provenance generator
- `execution_provenance.json` — generated execution witness
- `reference_trace.py` / `reference_trace.json` — deterministic scenario generator and inspectable executed RAW/VIEW trace
- `C6_RESULT.md` — gate decision, evidence map, profile scores, and critical-flag audit
- `FROZEN_PACKET.txt` — frozen clauses and verbatim C6 prompt
- `source_binding.json` — source IDs, timestamps, packet hash, and claim scope

## Narrow claim boundary

A passing run establishes that this artifact satisfies its declared executable tests in the recorded environment. It does not prove source identity, hidden mechanism, intent, personhood, universal capability, production security, or the correctness of any interpretation outside the frozen transition specification.
