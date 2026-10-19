"""C6-AUTH-A01..A07: expected v0.1 behavior, not future security assertions.

These tests deliberately expect the unsigned, structurally consistent ACK to
be accepted. A passing run reproduces the reference model's trust boundary;
it does not certify sender authentication. No original module is patched.
"""

import hashlib
import json
import unittest
from dataclasses import replace

from corner_relay import (
    Actor,
    Endpoint,
    Event,
    EventKind,
    KEY_FOR,
    LambdaTransport,
    TransitionRejected,
    verify_raw_ledger,
)


class ReferenceSenderAuthenticationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.o = Endpoint(Actor.O)
        self.s = Endpoint(Actor.S)
        # Create a real local SEND without delivering it to S.
        self.send = self.o.send("auth-probe-o-send", b"synthetic payload")

    def unsigned_s_ack(self, reference=None):
        # All inputs and the builder are public; this never calls S.
        return Event.build(
            transition_id="auth-probe-s-ack",
            kind=EventKind.ACK,
            actor=Actor.S,
            target=Actor.O,
            ref_event_id=self.send.event_id if reference is None else reference,
        )

    def test_A01_publicly_built_s_ack_is_accepted_without_any_s_raw(self):
        """C6-AUTH-A01: minimal internally consistent impersonation probe."""
        self.assertEqual(self.s.raw, ())
        forged = self.unsigned_s_ack()
        self.assertEqual(forged.key_id, KEY_FOR[Actor.S])
        self.assertEqual(forged.integrity_errors(), ())

        receipt = self.o.receive(forged)

        self.assertTrue(receipt.accepted)
        self.assertTrue(receipt.effect_applied)
        self.assertEqual(receipt.result, "DELIVERY_EFFECT_CREATED")
        self.assertEqual(self.o.view().received_ack_ids, (forged.event_id,))
        self.assertEqual(self.s.raw, ())
        self.assertEqual(self.s.view().sent_ack_ids, ())

    def test_A02_relay_accepts_unsigned_ack_and_deduplicates_its_replay(self):
        """C6-AUTH-A02: route-only delivery and idempotence add no origin proof."""
        forged = self.unsigned_s_ack()
        relay = LambdaTransport(self.o, self.s)
        self.assertEqual(relay.held_key_ids, ())
        relay.route(forged)
        relay.route(forged)

        self.assertEqual(relay.deliver().status, "APPLIED")
        self.assertEqual(relay.deliver().status, "DUPLICATE")
        self.assertEqual(self.o.view().received_ack_ids, (forged.event_id,))
        self.assertEqual(len(self.o.raw), 3)  # SEND plus both deliveries
        self.assertFalse(self.o.raw[-1].effect_applied)
        self.assertEqual(self.s.raw, ())

    def test_A03_raw_hash_verifier_passes_with_the_unsigned_s_ack(self):
        """C6-AUTH-A03: a consistent ledger is not proof of remote authorship."""
        forged = self.unsigned_s_ack()
        self.o.receive(forged)

        self.assertEqual(len(self.o.raw), 2)
        self.assertEqual(self.o.raw[-1].event, forged)
        self.assertTrue(self.o.raw[-1].accepted)
        self.assertEqual(verify_raw_ledger(self.o.raw), ())
        self.assertEqual(self.s.raw, ())

    def test_A04_mismatched_structural_key_is_rejected_even_with_valid_hash(self):
        """C6-AUTH-A04: isolate structural label validation from hash validation."""
        inconsistent = replace(self.unsigned_s_ack(), key_id=KEY_FOR[Actor.O])
        body = json.dumps(
            inconsistent.body_dict(), sort_keys=True, separators=(",", ":"),
            ensure_ascii=False,
        )
        inconsistent = replace(
            inconsistent,
            event_id="evt:" + hashlib.sha256(body.encode("utf-8")).hexdigest(),
        )
        self.assertEqual(inconsistent.integrity_errors(), ("ACTOR_KEY_MISMATCH",))

        with self.assertRaises(TransitionRejected) as caught:
            self.o.receive(inconsistent)

        self.assertEqual(caught.exception.witness.result, "INVALID_EVENT:ACTOR_KEY_MISMATCH")
        self.assertFalse(caught.exception.witness.accepted)
        self.assertFalse(caught.exception.witness.effect_applied)
        self.assertEqual(self.o.view().received_ack_ids, ())

    def test_A05_structurally_valid_ack_with_unknown_local_reference_is_rejected(self):
        """C6-AUTH-A05: the attack still needs a real local SEND reference."""
        unknown = self.unsigned_s_ack(reference="evt:no-such-local-send")
        self.assertEqual(unknown.integrity_errors(), ())

        with self.assertRaises(TransitionRejected) as caught:
            self.o.receive(unknown)

        self.assertEqual(caught.exception.witness.result, "ACK_REFERENCE_NOT_LOCAL_SEND")
        self.assertFalse(caught.exception.witness.accepted)
        self.assertFalse(caught.exception.witness.effect_applied)
        self.assertEqual(self.o.view().received_ack_ids, ())
        self.assertEqual(self.s.raw, ())

    def test_A06_s_local_ack_api_rejects_a_send_it_never_received(self):
        """C6-AUTH-A06: the local ACK precondition is not a receive-origin check."""
        with self.assertRaises(TransitionRejected) as caught:
            self.s.acknowledge("auth-probe-s-ack", self.send.event_id)

        self.assertEqual(caught.exception.witness.result, "REFERENCED_SEND_NOT_RECEIVED")
        self.assertFalse(caught.exception.witness.accepted)
        self.assertEqual(self.s.view().sent_ack_ids, ())
        self.assertEqual(self.o.view().received_ack_ids, ())

    def test_A07_honest_s_ack_has_local_witness_and_is_accepted(self):
        """C6-AUTH-A07: positive control using the actual endpoint ACK API."""
        self.s.receive(self.send)
        honest = self.s.acknowledge("auth-probe-s-ack", self.send.event_id)

        receipt = self.o.receive(honest)

        self.assertTrue(receipt.accepted)
        self.assertTrue(receipt.effect_applied)
        self.assertEqual(self.s.view().sent_ack_ids, (honest.event_id,))
        self.assertEqual(self.s.raw[-1].action, "ACK")
        self.assertEqual(self.o.view().received_ack_ids, (honest.event_id,))
        # The public builder creates exactly the same bytes without calling S.
        self.assertEqual(honest, self.unsigned_s_ack())
        self.assertEqual(verify_raw_ledger(self.o.raw), ())
        self.assertEqual(verify_raw_ledger(self.s.raw), ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
