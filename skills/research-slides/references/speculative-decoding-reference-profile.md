# Speculative Decoding Reference Profile

This is the default structural reference for new Research Slides decks. It distills the durable presentation grammar of the *On Parallel and Speculative Decoding for Efficient Language Modeling* deck. Transfer its reasoning structure and evidence cadence, not its topic facts.

## Default contract

The black Metropolis visual identity is the default; the act map and page budget
are adjustable teaching defaults. Evidence honesty is a completion boundary.

When audience or duration is omitted, assume ML researchers outside the immediate
subfield and a 20-minute talk with roughly 12–16 pages before backup. One possible
budget is 2 for cover/navigation, 2 for object/pressure, 2 for tensions/contract,
4–6 for methods/evidence, and 2–4 for ending/source index. This is not a quota.
For a five-minute talk, 3–5 substantive pages with a combined opening, one tension,
and one or two takeaways may be enough; omit TOC and section dividers if they only
consume time. Combine evidence on one legible page when its distinct questions
remain clear. Preserve the reasoning, not the original page count.

Infer `paper`, `idea`, or `survey` mode, but apply this profile before mode-specific compression. For an `idea + survey` request, use the idea causal spine with survey evidence unless comparing the field is the primary objective; then use the survey spine.

Build the deck around a small set of governing tensions. Two to four is typical; use four only when the sources support four. Each later method must occupy, move, or repair one of those tensions, and the conclusion must return to them.

## Durable act map

| Act | Audience-model update | Required evidence |
| --- | --- | --- |
| 1. Object | Define the process, interface, or system before its jargon. | Direct teaching figure, source architecture, or minimal example |
| 2. Pressure | Show the measured bottleneck or surprising fact that makes change necessary. | System measurement, scaling plot, failure trace, or formal limitation |
| 3. Governing tensions | State the reusable dials that organize the rest of the talk. | Sourced comparison or clearly labeled synthesis |
| 4. Contract and incumbent | Establish what must remain correct, how success is judged, and why the baseline still matters. | Formula/process for the contract plus baseline evidence |
| 5. Expand the solution space | Introduce method families as different relaxations of the incumbent assumption. | One consistent comparison lens; papers are evidence, not section names |
| 6. Repair and merge | Show how the approach meets its contract and what supports the distinctive choice. | Mechanism plus evidence appropriate to the claim kind below |
| 7. Frontier | Recover the governing tensions under relevant conditions and state what remains unresolved. | Scope/limitations, deployment evidence when relevant, a concise synthesis |

Do not turn the act names into generic slide titles. Titles must state the local claim.

## Evidence contract by claim kind

| Kind | What earns the claim | What must not be substituted |
| --- | --- | --- |
| Empirical | Measurements with baseline, metric, conditions and uncertainty; ablation or other relevant analysis for a causal design claim | An overview diagram is not a measured gain; correlation alone does not isolate the cause |
| Theory | Defined objects, assumptions, precise statement, proof or explicitly bounded proof sketch, example and scope | Do not require an experimental ablation or source figure for a theorem; an example alone is not proof |
| Explanation | Traceable source or labeled derivation/toy example with its assumptions | A toy calculation is not an observed deployment result |
| Proposal | Existing observation or motivation, labeled hypothesis, mechanism, planned comparison, falsifier and evaluation contract | Expected improvement is not achieved improvement; an engineering concern is not a measured bottleneck |

Use multiple kinds when appropriate and label the transition. If evidence is
missing, narrow the claim or mark it unverified rather than fill an empty slot.

## The SD instantiation

The reference deck used four global dials:

1. **Memory bandwidth versus idle compute** — why extra parallel work can be cheap.
2. **Draft quality versus draft cost** — accurate proposals can erase their own speed advantage.
3. **Causality versus parallelism** — simultaneous guesses lose dependencies that serial generation preserves.
4. **Per-request speed versus system throughput** — the locally longest verification may be globally wasteful under load.

Its refined speculative-decoding subsection compresses these into two local tensions: draft intelligence/cost/length and parallelism/causality. This is not a contradiction: global system dials may collapse into fewer local tensions inside one act.

Use these four only for SD-related material. For another topic, derive topic-specific dials from its sources.

## Cross-topic slot mapping

| SD reference slot | Question to answer in a new topic |
| --- | --- |
| Memory-bound decode | Which resource, assumption, or interface creates the observed pressure? |
| Draft/verify contract | What correctness, evaluation, or safety contract must survive optimization? |
| Autoregressive drafter | What incumbent baseline is credible, and what structural limit blocks it? |
| Parallel proposals | Which method families relax the limiting assumption in distinct ways? |
| Causality repair | Where does each method restore the information, constraint, or control it removed? |
| Serving frontier | When do local gains reverse under scale, load, deployment, or evaluation conditions? |

If a slot has no source-backed analogue, omit it. Never fabricate a symmetry merely to resemble the reference.

## Evidence and reveal cadence

- Pair the object with a teaching figure/example, then the pressure with a supported observation, formal limitation, or explicitly untested concern.
- Introduce governing tensions before the paper sequence. Do not reveal method names before the audience understands what they must repair.
- Establish the correctness or evaluation contract before claiming speed, quality, or capability gains.
- Give a core work a mechanism and evidence fitting its claim kind. Separate result and causal analysis when both need space; do not demand nonexistent experiments in theory or proposals.
- Use a secondary work only to mark a distinct position on the shared comparison lens.
- Alternate explanation with evidence; do not run a long taxonomy without returning to a concrete mechanism or result.
- At each act boundary, use the spoken bridge to name which tension is now unresolved.
- Put implementation detail, extra tables, and analogies in backup unless they change the main argument.

## Storyboard gate

Before writing LaTeX, create rows with:

`audience question -> one claim -> governing tension -> evidence -> exact source -> spoken bridge/callback`

Reject the storyboard if:

- paper names replace the argument (chronology is useful only when it explains the field);
- a governing tension has no later method comparison or final callback;
- a claim lacks the evidence its kind requires, or planned evidence is phrased as an achieved result;
- a performance claim appears before the success/correctness contract;
- SD-specific facts, labels, formulas, or paper names appear in an unrelated topic;
- a synthesized taxonomy is presented as source fact.

Only after this gate passes should the deck use the bundled black Metropolis starter and proceed to compile/render QA.
