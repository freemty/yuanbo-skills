# Adaptive Draft Length Proposal Sources

## Source P1 and Status

Supplied synthetic fixture: `../fixtures.md`, section P1. The only supplied motivation is that batching may change verification cost. No measured bottleneck, acceptance curve, benchmark score, speedup, or achieved improvement exists in the supplied evidence. Everything below is an explicitly proposed design or test.

## Model M1

K is the number of candidate tokens drafted for a request in a round. B is the number of active requests in the verification batch. A toy draft/verify round produces candidate tokens, verifies under the target model, and emits tokens under a specified output-distribution contract. The deck does not claim a concrete verifier implementation has already satisfied the contract.

## Contract C1

For each fixed input prompt c and decoding setting, let p(.|c) be the target-only output distribution and q(.|c) the output distribution with the tested draft-length policy. The desired contract is q(.|c)=p(.|c). Hold the target, draft model, verification/acceptance rule, prompts, decoding settings, and hardware fixed across length policies. Include controller and scheduling overhead in timing.

Proposed correctness checks: first use a finite-vocabulary, short-horizon toy where full output distributions can be enumerated. Compare target-only and speculative distributions with a prespecified numerical tolerance. Add sampled distribution regression checks on the larger serving workload. Finite tests cannot prove distribution equality for every possible prompt or implementation path. The proposal requires a valid verifier and checks that the length policy does not invalidate it.

## Hypothesis H1 and Mechanism M2

Hypothesis: the draft length with the lowest time per emitted token may depend on batch load. This claim remains untested.

Proposed mechanism: on calibration traces, estimate cost per emitted token for each candidate length and active batch size. At runtime, observe B, select K from the calibrated table, and use a fixed K as a fallback where data are insufficient. Lock the controller before the held-out comparison. This is a concrete hypothesis to test, not an endorsed production algorithm.

## Plan V1

The grid B in {1,4,16} and K in {1,2,4,8} is a proposed synthetic test design. It is not supplied benchmark data. Each cell is scheduled for measurement. Compare every fixed-length baseline during calibration, then lock a single calibrated fixed K and the adaptive policy for matched held-out load traces. Report the whole fixed-length sweep as context so that a weak baseline does not create an artificial win. Varying active batch count operationalizes batch load in this toy. A broader deployment test would also need arrival-process and scheduler definitions.

## Plan V2

Record end-to-end request latency, including queueing, with p50 and p95 in milliseconds. Record output-token throughput in tokens/s. Define draft acceptance as accepted draft tokens divided by proposed draft tokens. Also record batch count, chosen length, verification time, and controller overhead to explain any effect. Keep token budgets and prompt/output-length distributions matched. Use repeated paired load traces and report variability or confidence intervals, with the estimator and repetition count fixed before evaluation. No numerical gain target is asserted by this proposal.

## Falsifiers F1

Reject a policy that fails the token-distribution correctness check. Evidence against the performance hypothesis includes no useful load/length interaction, or no robust held-out latency-throughput improvement over the calibrated fixed baseline after controller overhead. A latency improvement that worsens throughput under the chosen acceptance criterion is a trade-off, not an unconditional win. The study must prespecify the operating point or trade-off criterion before interpreting results.
