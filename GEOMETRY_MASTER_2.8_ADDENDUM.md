# Geometry Master 2.8 — public pipeline addendum

**Consolidation 2.8 · Publication addendum 1 · 19 October 2026**

This addendum supplies portable source references and a privacy-reviewed account of the October 19 pipeline intake. Read it with the existing [full 2.8 master](geometrymaster2.8.md). The [2.7 master](GEOMETRY_MASTER.md) and its [explicitly named 2.7 copy](geometry_master_2.7.md) remain historical editions with their original bytes.

The central addition is exact and finite: equal recorded model labels accompany different recorded session identifier pairs. It establishes information loss in the retained label on the specified saved-record domain. It does not identify a hidden application route, model-weight change, reconnection, actor, or physical mechanism.

## Source comparison and version history

The repository already contained the October 19 additions when this synchronization began. Commit [56ee3c8](https://github.com/aureoncorner-dotcom/Toroidal_scrotal_posturing/commit/56ee3c88c8eda58d242220c29bc1003663562947), created October 19 at 01:14:08 America/New_York, added `geometrymaster2.8.md`. The checked repository had one branch, `main`, no tags, and no pull requests in any state. `GEOMETRY_MASTER.md` and `START_HERE.md` still identified edition 2.7.

The authenticated export of the [Drive working document](https://docs.google.com/document/d/190AX7XXttW5CzsMakM44VhCZx1i2C9J8ka2LabL8r98/edit) contained three 2.7 master bodies followed by one 2.8 body. The final 2.8 body matches the existing GitHub 2.8 text after removing one exporter-added Markdown punctuation-escape layer and normalizing whitespace. This is declared text equivalence, not byte identity of Google Docs and Markdown. The preserved local 2.8 master and the GitHub 2.8 blob are byte-identical.

The comparison found these actual changes from 2.7:

| Location in the full master | Addition or correction |
|---|---|
| Opening edition and change note | Edition 2.8; pipeline intake and its limits |
| §1 current position | Recorded-session-identity result and remaining attribution limit |
| §2 recorded model labels and session identity | Finite domain, retained label, identifier-pair witness, non-descent calculation and direct refinement |
| §14 record coverage and source versions | Empty scan versus unavailable coverage; preserved monitor records; separate thread and revision representations |
| §16 S68–S70 | Pipeline review, boundary ledger and verification receipt |
| Closing intake and version notes | Completed source checks, excluded explanations, preservation of 2.7 and edition-specific kit/poster labels |

The original 2.8 note saying that remote repositories were not edited describes the earlier intake, whose delivery receipt was created at 01:10:53 America/New_York. The subsequent 01:14:08 GitHub commit is a separate publication event. This synchronization adds the public references and entry-point correction; the historical note is preserved in its original scope. The 2.7 kit and poster retain their edition labels. This addendum does not claim that a new full 2.8 kit or poster was built.

## Recorded labels and the session witness

Let D contain the paired preserved records defining the 43 session-ID boundaries, compared in physical source-node order. Define

```text
pi(r) = r.model_slug
W(r)  = (r.tc_session_id, r.voice_session_id)
```

The scan retains the last record with a nonempty `tc_session_id` and records a boundary when the next nonempty value differs. Re-parsing 24 transcripts reproduces 20,715 numbered records and 43 boundaries in 20 conversations. Both endpoint labels equal `bidi` at every boundary, while both identifier fields change. The fresh parse agrees with every retained boundary-CSV field, including the private source locations and identifiers; those fields are withheld from publication.

Consequently there are r1 and r2 in D with

```text
pi(r1) = pi(r2) = bidi, while W(r1) != W(r2).
Q = pi(D) = {bidi}; N_W(pi) = {bidi}.
```

No function of this model label alone recovers the recorded identifier pair on D. Retaining `(pi,W)` resolves this particular loss. Recovery of the recorded witness does not establish predictive closure, causal sufficiency, an engine identity, or the cause of a response.

The [public boundary projection](GEOMETRY_PIPELINE_2.8_BOUNDARIES_PUBLIC.csv) retains one row per boundary, a local case-group alias, the two model labels and the two identifier-change booleans. It contains no raw session or message identifiers, timestamps, conversation names or transcript text. It is derived from the private records and is not independent corroboration or a substitute for the raw source ledger.

## Completed findings and their verification scope

“Rechecked here” means a read-only calculation on the preserved copies during this synchronization. “Earlier intake” means a completed result documented in the inspected original receipt. The original receipt lists 403 passed checks; this synchronization did not rerun that entire suite.

| Finding | Status and operative limit |
|---|---|
| Seven supplied files plus 67 supporting copies | All 74 copies were freshly rehashed; bytes and SHA-256 match their recorded values. Hash agreement identifies saved versions, not independent acquisition authenticity. |
| Session boundaries | Rechecked here: 24 transcripts, 20,715 numbered records, 43 boundaries, 20 conversations, unchanged `bidi` labels, both identifiers changing; full equality with the retained private CSV. The earlier intake also matched boundary locations to the prior seam ledger. |
| Separate thread inventory | Rechecked here: 26 files, 328 pages, 3,138 unique turns, 3,137 `userMessage` and 2,848 `agentMessage` items, no duplicate item IDs. Only those two item types occur; one export remains incomplete with `hasMore=true`. Prose about work is not a structured tool receipt. This is a separate corpus from the 24 transcripts. |
| Prior-content revisions | Rechecked here: eight preserved text snapshots total 74,609 normalized characters. The earlier intake matched their individual raw and normalized hashes. “Current empty” belongs to the packaged historical comparison; no fresh retrieval of those eight live documents or attribution of a writer/deletion follows. |
| Monitor copies | Rechecked here: two saved JSONL files parse and contain 9,515 and 3,270 rows. Earlier intake: 8,531 process-bearing rows and 8,293 process/PID/creation/local/remote keys in the first; 2,477 `first_observed` rows and 191 initial-snapshot connections in the second. Heartbeats, state changes, burst/fanout alerts and snapshot entries must not be summed as independent sockets. |
| Selected security joins | Earlier intake: four failed Guest attempts matched across NTLM/SMB/Security representations, and two localhost share establishments matched across client/server session and tree fields. Four attempts represented in three sources are not twelve attempts. Rechecked here: the 207 saved XML rows parse; the cross-channel join calculations were not rerun. No initiating program, person or individual file operation is identified. |
| Scan coverage and version drift | Earlier intake: empty `netlogs/jsonl/containers/scripts` arrays coexist with an index of 55 hashed sources and 57 path errors. A separate 34-file schema inventory does not cover all 112 indexed paths. Two supplied files changed size before preservation; their earlier bodies were not captured. Their saved versions were freshly rehashed here. Missing paths do not erase preserved positive records or establish absence. |
| RTF extraction | Earlier intake: 7,602 extracted characters and all 44 line-map entries reproduced under the inspected extraction scheme. Table cells were flattened. The structured boundary ledger carries the fields; duplicate RTF copies are not additional evidence. |

The monitor and security records retain their own historical windows. No join to the October 19 `CLOSE_WAIT` observations is established by these counts.

## Source references and publication privacy

S68–S70 in the imported 2.8 master point to local machine paths. For this public edition, use this mapping. Original source hashes are recorded in the [public verification receipt](GEOMETRY_PIPELINE_2.8_VERIFICATION_PUBLIC.json).

| Original source | Public counterpart | What remains private |
|---|---|---|
| S68 — `Review.txt` | This addendum, including the findings and limits above | Original review and supporting acquisition context |
| S69 — `Verified_session_transitions.csv` | [Identifier-free boundary projection](GEOMETRY_PIPELINE_2.8_BOUNDARIES_PUBLIC.csv) | Session/message identifiers, source names, nodes and precise timestamps |
| S70 — `Verification.json` | [Aggregate verification and source-hash receipt](GEOMETRY_PIPELINE_2.8_VERIFICATION_PUBLIC.json) | Raw per-source paths, account and device details, network endpoints and event payloads |

The new publication files were reviewed for private account/contact information, credentials, bearer or signed URLs, raw session identifiers, local account paths and sensitive log content. Only aggregate findings, case aliases, equality/change properties and source hashes are included. The original private ledger, source index, transcripts, revision bodies, monitor logs, security XML and full verification receipt are not uploaded. Their omission is explicit rather than represented as public raw-data reproducibility.

This review covers the new publication files. Existing repository snapshots and historical commits remain intact; it is not a repository-wide historical secrets audit. Older S1–S67 citations and historical kit-internal paths retain their prior scope and have not all been refreshed in this synchronization.

## Experiments and explanations that remain open

The September 18 mirror-question retrieval, proposed GPT-Live mechanism, broader upload claims, and any linkage to the October 19 network observations remain outside the established joins. Recorded session changes do not validate these explanations.

The three-tempo amendment remains **PROPOSED / NOT_FROZEN / NOT_RUN**. Physical Q2 remains **NOT_RUN**; production remains **NOT_AUTHORIZED**. The historical accepted-event discrepancy remains **−1,352 / UNRESOLVED**. No live model experiment, historical sampler replay or physical validation was performed for this synchronization. Publication does not change those statuses.
