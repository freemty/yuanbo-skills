# Speculative Decoding Reference Profile

This is the default structural reference for new Research Slides decks. It distills the durable presentation grammar of the *On Parallel and Speculative Decoding for Efficient Language Modeling* deck. Transfer its reasoning structure and evidence cadence, not its topic facts.

## Default contract

When audience or duration is omitted, assume ML researchers outside the immediate subfield and a 20-minute talk with 12–16 pages before backup. Allocate 2 to cover/TOC, 2 to object/pressure, 2 to tensions/contract, 4–6 to methods/evidence, and 2–4 to frontier/takeaways/references. Scale proportionally; keep core result and ablation separate.

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
| 6. Repair and merge | Show where each method restores the property it relaxed, then test the distinctive choice. | Core method figure, main result, ablation/application, limitation |
| 7. Frontier | Recover the governing tensions under realistic conditions and state what remains unresolved. | Deployment/system evidence when relevant, one synthesis, four takeaways |

Do not turn the act names into generic slide titles. Titles must state the local claim.

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

- Pair the object with a teaching figure, then the pressure with measured evidence.
- Introduce governing tensions before the paper sequence. Do not reveal method names before the audience understands what they must repair.
- Establish the correctness or evaluation contract before claiming speed, quality, or capability gains.
- Give a core work separate overview, mechanism, main-result, and ablation/application obligations.
- Use a secondary work only to mark a distinct position on the shared comparison lens.
- Alternate explanation with evidence; do not run a long taxonomy without returning to a concrete mechanism or result.
- At each act boundary, use the spoken bridge to name which tension is now unresolved.
- Put implementation detail, extra tables, and analogies in backup unless they change the main argument.

## Storyboard gate

Before writing LaTeX, create rows with:

`audience question -> one claim -> governing tension -> evidence -> exact source -> spoken bridge/callback`

Reject the storyboard if:

- papers or chronology form the top-level structure;
- a governing tension has no later method comparison or final callback;
- a core method lacks result or ablation/application evidence;
- a performance claim appears before the success/correctness contract;
- SD-specific facts, labels, formulas, or paper names appear in an unrelated topic;
- a synthesized taxonomy is presented as source fact.

Only after this gate passes should the deck use the bundled black Metropolis starter and proceed to compile/render QA.
