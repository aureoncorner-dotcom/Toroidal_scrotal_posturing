# Proposed authenticated C6 successor — requirements only

Status: **not implemented, not adversarially verified, not production authentication**.
These are proposed design requirements. The executable tests beside this file
characterize the original v0.1 model and do not test this proposal.

## Narrow implementation boundary

Add a separately versioned `AuthenticatedEndpoint` and signed envelope format.
Retain v0.1 and its acceptance suite as frozen reference material. Put the new
security suite in a different module and require its stronger assertions to
pass normally. Do not invert the existing characterization assertions or mark
missing controls as passing through mocks, skips, or expected failures.

Each endpoint generates and exclusively controls its own signing private key.
O has only O's signing capability; S has only S's. Neither the other endpoint nor
Lambda receives that private key. Each recipient pins the peer's public
verification key through an independently authenticated provisioning step.
The sender's label or an envelope-supplied public key must not establish trust.
Using one shared signing secret for both endpoints would allow O to produce an
S-authenticating tag and would not meet independent credential control.

One candidate is Ed25519 through a maintained cryptographic library, with
conformance tests drawn from [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032).
Private keys must be generated randomly, rather than derived from `Actor.S`,
`KEY_FOR`, transition IDs, payloads, repository fixtures, or other public data.
Test-only keys must be synthetic and separate from deployed credentials.

## Authenticated envelope and receive gate

Define a versioned signed envelope containing the complete original event,
including its event ID, and the additional authenticated context:

- fixed protocol/domain identifier and envelope version;
- signing endpoint, intended recipient, and provisioned credential epoch;
- recipient-established session/challenge identifying the active exchange;
- a unique message nonce scoped to that sender, epoch, and session.

Specify the exact bytes signed and verified. A possible choice is a fixed domain
prefix followed by UTF-8 JSON canonicalized under
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), restricted to the envelope's
defined types. Cover actor, target, kind, transition ID, reference, payload,
payload hash, event ID, and every context field. Reject malformed/duplicate
fields, unknown schemas, unsupported algorithms, invalid encodings, and extra
unsigned fields before state effects. Publish cross-implementation test vectors.
Keep the original Event's hashes unchanged inside the new envelope; an event
hash continues to mean content identity, not authorization.

At O, before accepting an ACK or recording an accepted state effect:

1. Parse and validate the complete envelope and original event strictly.
2. Select the trusted S verification key from local configuration for this peer
   and credential epoch. Do not trust a key merely carried with the message.
3. Verify S's signature over the complete canonical envelope. Missing, malformed,
   wrong-key, and invalid signatures fail closed, without fallback to v0.1.
4. Require that the signer is the configured peer authorized to ACK the
   referenced local SEND, that target is O, and that the session/challenge is
   active for that SEND. A cryptographically valid signature from O or an
   unrelated key is insufficient for an ACK claiming S.
5. Apply explicit nonce/replay rules, then the existing reference, activity, and
   transition checks. Atomically persist authentication/replay evidence with
   the state transition. A rejection may append a rejection witness but must
   not produce an accepted ACK effect.

An honest S signs an ACK only after its own local accepted SEND-receipt check.
The signing API must be bound to S's identity and operation policy; a generic
caller must not be able to ask O's signer to sign an S event. Protect local
EXIT invocation with the owning endpoint's credential/control boundary. A
transported EXIT remains disallowed, as in v0.1; a remote signed EXIT must not
become a way for one endpoint to exit the other.

Lambda carries opaque envelopes and holds no signing credential. Verification
and authorization stay at the receiving endpoint, including any alternate
delivery API. Expose no externally reachable bypass to the legacy `receive`.

## Replay, audit, and lifecycle rules to implement explicitly

Preserve idempotent transport retry by accepting an exact, previously verified
envelope in the same permitted session as a duplicate with no new effect.
Reuse of the same sender/epoch/session nonce with different event bytes is a
conflict. Old-session or retired-epoch envelopes are rejected even if their
signatures remain mathematically valid. Do not use a simple highest-sequence
rule that silently breaks the original allowance for reordering.

Persist replay state across restart and coordinate concurrent deliveries
atomically. Define authenticated session setup, retirement, key rotation,
revocation, recovery, and late delivery after EXIT before claiming those cases
are covered. Local endpoint activity checks remain necessary after verification.

Retain the full signed envelope, verification decision, credential fingerprint,
credential epoch, session, and rejection reason in new RAW records. Public hash
chains alone do not prevent complete history rewriting. Durable storage and
independent anchoring are separate extensions when required by the deployment.

A valid signature would establish authorization by the pinned credential under
the stated key-custody assumptions. It would not by itself prove a human
identity, honest S execution, actual SEND receipt, S's local logging, or
Byzantine safety. A malicious or compromised S signer can sign a false ACK.
Do not claim those additional properties from this extension.

## Future adversarial acceptance matrix — all unexecuted

| ID | Case | Required future behavior |
|---|---|---|
| C6-AUTH-F01 | A01's public S-labelled ACK, without a signature | Reject; no accepted ACK effect |
| C6-AUTH-F02 | Genuine S receipt and ACK signed by independently held S key | Accept once; verify retained signed evidence |
| C6-AUTH-F03 | Consistent S labels signed with O's key or an attacker key | Reject, including when an attacker supplies a matching public key |
| C6-AUTH-F04 | Change each signed field independently, then recompute public event hashes | Reject; content rehashing must not restore signature validity |
| C6-AUTH-F05 | Missing/truncated signature, malformed envelope, unknown schema/algorithm, duplicate field | Reject safely; no downgrade to unsigned receive |
| C6-AUTH-F06 | Exact verified retry delivered twice, reordered, and concurrently | One accepted effect; duplicates retained consistently |
| C6-AUTH-F07 | Reuse nonce with different content; replay across session/recipient/credential epoch; restart receiver | Reject unauthorized replay/conflict; persist replay protection |
| C6-AUTH-F08 | Valid S signature but unknown SEND, wrong target/peer, or inactive receiver | Reject through authorization and original transition checks |
| C6-AUTH-F09 | Caller holding only O's credential attempts S SEND/ACK/EXIT; relay attempts signing | No S signing capability; no unauthorized state effects |
| C6-AUTH-F10 | Forged SEND and transported EXIT, through every ingress API | Enforce sender credentials for SEND; reject transported EXIT |
| C6-AUTH-F11 | Retired/revoked key and unauthorized rebinding/rotation request | Reject according to the implemented lifecycle policy |
| C6-AUTH-F12 | Entire honest retry/duplicate/reorder/partition/exit suite under signed transport | Preserve declared transition behavior with authenticated evidence |

F01-F05 are the minimum evidence for the narrow ACK-origin fix. F06-F12 address
the surrounding bypass, replay, and lifecycle conditions required before a
broader authentication claim. Implementation and this matrix are still future
work; no result in the current execution receipt certifies them.
