"""Print a deterministic synthetic witness of the reference-model boundary."""

import json

from corner_relay import Actor, Endpoint, Event, EventKind, LambdaTransport, verify_raw_ledger


def build_observation():
    o, s = Endpoint(Actor.O), Endpoint(Actor.S)
    send = o.send("auth-probe-o-send", b"synthetic payload")
    before_o, before_s = o.view().to_dict(), s.view().to_dict()
    # This is adversary-controlled construction, not S.acknowledge().
    forged = Event.build(
        transition_id="auth-probe-s-ack",
        kind=EventKind.ACK,
        actor=Actor.S,
        target=Actor.O,
        ref_event_id=send.event_id,
    )
    relay = LambdaTransport(o, s)
    relay.route(forged)
    delivery = relay.deliver()
    return {
        "schema": "corner-relay-c6/unsigned-ack-observation/v1",
        "implementation": "original reference v0.1; no authentication added",
        "construction": "public Event.build; S never receives or acknowledges SEND",
        "event": forged.to_dict(),
        "event_integrity_errors": list(forged.integrity_errors()),
        "delivery_status": delivery.status,
        "delivery_result": delivery.result,
        "O_view_before": before_o,
        "O_view_after": o.view().to_dict(),
        "O_RAW_after": [record.to_dict() for record in o.raw],
        "S_view_before": before_s,
        "S_view_after": s.view().to_dict(),
        "S_RAW_before": [],
        "S_RAW_after": [record.to_dict() for record in s.raw],
        "O_ledger_verification_errors": list(verify_raw_ledger(o.raw)),
        "claim_boundary": "Observed label/hash consistency and acceptance; no authenticated S origin.",
    }


if __name__ == "__main__":
    print(json.dumps(build_observation(), indent=2, ensure_ascii=False))
