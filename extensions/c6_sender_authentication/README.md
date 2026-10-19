# Corner Relay C6 sender-authentication boundary extension

This extension adds reproducible adversarial coverage to reference v0.1. It
changes no protocol code, acceptance test, frozen packet, original result record,
historical execution receipt, or reference archive. No cryptographic
authentication is implemented here.

## Check for newer work

On October 19, 2026, the live default branch `main` resolved to
[`56ee3c88c8eda58d242220c29bc1003663562947`](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/commit/56ee3c88c8eda58d242220c29bc1003663562947).
The repository advertised one branch and no pull requests in any state. The
complete, non-truncated Git tree contained 305 files. Inspection of the Python
files found no authenticated C6 implementation. Git history records the last
change to the protocol, original tests, and reference ZIP at
[`2f79d834c28f7fc6595798989d68605823d99f0e`](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/commit/2f79d834c28f7fc6595798989d68605823d99f0e)
on September 1, 2026. Their current Git blob bytes match the files in the frozen
ZIP. No fix to this boundary was present in the checked revision. This check
does not cover unpublished work, forks, or changes after the recorded snapshot.

`baseline.json` records the commit, check time, and SHA-256 hashes. All nine
packaged file hashes listed in the original execution receipt were verified.
The repository's current root README describes another project; the C6 claim
boundary is in the **README inside the original reference ZIP**, which remains
untouched. That README explicitly limits the artifact to structural key slots
and content integrity and disclaims real-world sender authentication.

## Minimal reproduction

From the repository root, using Python 3.10 or newer:

```python
from corner_relay import Actor, Endpoint, Event, EventKind

o, s = Endpoint(Actor.O), Endpoint(Actor.S)
send = o.send("auth-probe-o-send", b"synthetic payload")
forged = Event.build(
    transition_id="auth-probe-s-ack",
    kind=EventKind.ACK,
    actor=Actor.S,
    target=Actor.O,
    ref_event_id=send.event_id,
)
assert forged.integrity_errors() == ()
assert s.raw == ()
receipt = o.receive(forged)
assert receipt.accepted and receipt.effect_applied
assert o.view().received_ack_ids == (forged.event_id,)
assert s.raw == ()
```

The attacker controls only the constructed inbound Event and knows the public
SEND reference. The test does not call S, read a secret, mutate endpoint
internals, replace a verifier, or patch the implementation. S's empty local RAW
is independently visible test-fixture ground truth, rather than a production
mechanism available to O. A public reference is enough to satisfy the existing
ACK-reference check; the attack does not require a fabricated local SEND at O.

## Run the tests and retain evidence

Keep the original acceptance suite separate:

```text
python -B -m unittest -v test_corner_relay
python -B -m unittest -v extensions.c6_sender_authentication.test_sender_authentication
```

For both suites, a deterministic probe trace, source preservation checks, and a
new execution receipt, run:

```text
python -B -m extensions.c6_sender_authentication.run_review --output work/c6-auth-review-001
```

Use a fresh output directory for each run. This runner never invokes the original
`run_with_provenance.py`, which would regenerate historical output files. It
checks the pinned original bytes before testing and again afterward. A Windows
checkout that automatically converts LF to CRLF will fail the byte guard;
use a separate checkout preserving Git blob bytes, or the extracted runnable
kit. Do not update the frozen source-binding hashes to accommodate conversion.

Print just the probe trace with:

```text
python -B -m extensions.c6_sender_authentication.reproduce_unsigned_ack
```

## Test meanings

All seven additional tests are **characterization assertions for the original
model**. None is skipped, expected to fail, or described as a verified future
security control.

| ID | Input or control | Expected original-model behavior |
|---|---|---|
| C6-AUTH-A01 | Internally consistent S ACK; real O SEND; S RAW empty before and after | Accept and apply at O |
| C6-AUTH-A02 | Same unsigned ACK through Lambda, delivered twice | APPLIED then DUPLICATE; S RAW remains empty |
| C6-AUTH-A03 | O ledger containing that accepted ACK | Hash/link verifier returns no errors |
| C6-AUTH-A04 | S actor with O key label; event hash recomputed consistently | Reject ACTOR_KEY_MISMATCH |
| C6-AUTH-A05 | Valid structural ACK with unknown local SEND reference | Reject ACK_REFERENCE_NOT_LOCAL_SEND |
| C6-AUTH-A06 | Actual S.acknowledge call before S receives the SEND | Reject REFERENCED_SEND_NOT_RECEIVED |
| C6-AUTH-A07 | Honest S receives SEND and generates its own ACK | Accept, with S local ACK witness |

A07 also shows that the public builder can produce an Event exactly equal to
the honestly generated ACK. Its event ID cannot distinguish those origins.
A02 records duplicate suppression, which does not establish authenticated replay
protection. A03 verifies only what the existing ledger checker checks.

The original 20 tests remain intact, including its mismatched actor/key test.
Passing A01-A03 reproduces the sender-origin limitation; it does not turn that
limitation into a desirable property for an authenticated successor. Preserve
these assertions as the v0.1 characterization suite when creating that successor.

## Precise missing authorization check

In the pinned [`Event.build`](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/blob/56ee3c88c8eda58d242220c29bc1003663562947/corner_relay.py#L68),
the key label, payload hash, and event ID are computed from public data.
[`integrity_errors`](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/blob/56ee3c88c8eda58d242220c29bc1003663562947/corner_relay.py#L123)
compares the actor/key labels and recomputes content hashes; it verifies no
signature, secret-dependent MAC, or authenticated peer channel.
[`Endpoint.receive`](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/blob/56ee3c88c8eda58d242220c29bc1003663562947/corner_relay.py#L638)
checks structural consistency, route, allowed transport kind, activity, and
whether an ACK references O's own SEND. Before applying the ACK, it never checks
that the exact event was authorized using a credential independently controlled
by the configured S endpoint.

The missing check is a verified binding from **the exact ACK and its context**
to **S's independently controlled credential**, with the verification key
selected from O's trusted peer configuration. Matching the string
`corner-relay:key:S`, recomputing a hash, or checking a self-supplied public key
cannot establish that binding. S's local ACK-generation precondition does not
protect O's inbound receive path. The ledger verifier checks record consistency,
not remote authorship.

See [AUTHENTICATED_EXTENSION_PROPOSAL.md](AUTHENTICATED_EXTENSION_PROPOSAL.md) for
the separate, unimplemented security requirements. See the accompanying run
receipt for observed counts, logs, and the complete synthetic RAW/VIEW witness.

## Sources and disposition

- [October 19 integration note, v7.1b](https://docs.google.com/document/d/1Ip-xkbq-eMueQqwLVs5oITQ9KAC6EMLZCE2YF3kL1Ts/edit), read in the authenticated browser; its reported results are distinct from this run.
- [Pinned original implementation](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/blob/56ee3c88c8eda58d242220c29bc1003663562947/corner_relay.py).
- [Pinned original acceptance tests](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/blob/56ee3c88c8eda58d242220c29bc1003663562947/test_corner_relay.py#L154).
- [Original reference archive](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/blob/56ee3c88c8eda58d242220c29bc1003663562947/Corner_Relay_Alpha_C6_Reference_v0.1.zip), SHA-256 `5392666c1892a4fd0d47aed04bfadcf92091d5c5f06a8899da88fb9e5e60b01b`.

This is a demonstrated boundary under a stronger adversarial threat model. It
does not establish failure of the reference artifact's declared acceptance
requirements and does not amend its original result record. Authentication,
credential custody, distributed liveness, durable provenance, and production
deployment remain separate claims requiring implementation and verification.
