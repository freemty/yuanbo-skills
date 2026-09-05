# Forward-Test Storyboards

All three decks use `idea` mode with different evidence kinds. The theory obligations in `paper-slide-patterns.md` also apply to the theorem. The self-contained black `beamer-colors.tex` and `layout-metropolis.tex` starter is the visual reference. No paper, benchmark, measurement, or citation is invented. Each short talk omits TOC and section-divider pages.

## Task 1: Queue Explanation

Audience: ML researchers. Duration: 5 minutes. Objective: distinguish service time from system time and explain the role of spare capacity under the stated model. Evidence kind: explanatory example and labeled calculation. Source: `fixtures.md#q1-single-server-queue`; local calculation details in `queue/source-notes.md`. Delivery: five-page Beamer PDF.

Governing tension: higher utilization versus waiting. This is a model explanation, not a serving measurement or optimization proposal.

| Page / seconds | Audience question | Slide claim | Governing tension | Evidence | Exact source | Spoken bridge / callback |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / 10 | What will I understand? | Waiting grows as a server approaches capacity | Utilization versus waiting | Minimal title | Q1 | The important distinction is the time to serve a job versus its total time in the system. |
| 2 / 65 | What is the system? | Random arrivals share one server | Utilization versus waiting | Named process and stationary M/M/1 assumptions | Q1; assumptions A1 | Rates describe averages, so spare capacity does not imply that every arrival sees an idle server. |
| 3 / 80 | What does 0.25 seconds contain? | System time includes 0.15 seconds of waiting | Same tension | W=1/(mu-lambda)=0.25 s, service=0.10 s, waiting=0.15 s | Q1; calculation D1 | Keeping service speed fixed, let us change only arrival rate. |
| 4 / 85 | How fast does delay grow? | Less spare capacity produces sharply higher delay | Same tension | Four-row sensitivity table at fixed mu=10 jobs/s | Calculation D2 | The service time stays at 0.10 seconds. The extra system time comes from waiting. |
| 5 / 60 | What generalizes from the example? | Near capacity, the model's mean waiting diverges | Same tension recovered | Wq=lambda/[mu(mu-lambda)] and lambda tending to mu from below | Derivation D3; scope A1 | Utilization alone cannot summarize delay, and this stationary mean is not a tail guarantee or deployment result. |

Storyboard gate: PASS. Four substantive pages fit the short duration. The supplied formula supports model calculations. No SD-specific fact or method family appears. The conclusion returns to the utilization/waiting tension.

## Task 2: Midpoint Theory

Audience: ML researchers comfortable with vectors but not assumed to know this identity. Duration: 12 minutes. Objective: prove a unique global minimizer and identify exactly which geometry the proof uses. Evidence kind: theoretical result, full algebraic proof, worked example, scope contrast. Source: `fixtures.md#t1-midpoint-theorem`; derivations in `midpoint/source-notes.md`. Delivery: eight-page Beamer PDF.

Governing tension: the two endpoint distances compete as x moves, while the recentered objective isolates a nonnegative excess loss. Proof versus illustration is kept explicit.

| Page / seconds | Audience question | Slide claim | Governing tension | Evidence | Exact source | Spoken bridge / callback |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / 15 | What is the target result? | The midpoint minimizes squared distance | Two endpoint distances | Minimal title | T1 | We will establish the global statement before using a numerical example. |
| 2 / 75 | What can vary, and what is fixed? | One location determines both squared distances | Two endpoint distances | x,a,b in R^d; d>=1; a,b fixed; unconstrained x; objective F | T1; definitions A1 | A plausible center is not yet a proof of optimality or uniqueness. |
| 3 / 90 | What precisely is the theorem? | The midpoint is the unique minimizer | Balance versus excess loss | m=(a+b)/2, argmin F={m}, minimum value ||a-b||^2/2 | T1; statement T2 | The identity will convert every competitor into an explicit gap from m. |
| 4 / 120 | Why center at the midpoint? | Centering gives equal and opposite offsets | Balance versus excess loss | y=x-m, v=(b-a)/2; x-a=y+v and x-b=y-v | Proof D1 | Opposite offsets make the cross terms cancel. |
| 5 / 135 | Where does the identity come from? | The cross terms cancel exactly | Balance versus excess loss | Inner-product expansions and substitution | Proof D2 | Only a nonnegative squared displacement now depends on x. |
| 6 / 90 | Why is the optimum unique and global? | A nonnegative gap proves global uniqueness | Excess loss | F(x)-F(m)=2||x-m||^2, equality iff x=m | Proof D3 | The numerical example can now illustrate a theorem that has already been proved. |
| 7 / 90 | What happens for a=0, b=2? | The excess loss is 2(x-1)^2 | Excess loss in one dimension | Formula and five-point exact table | Example E1 | The square and the Euclidean geometry are doing real work. |
| 8 / 105 | Which changes break the guarantee? | The guarantee depends on squared Euclidean geometry | Scope callback | Unsquared distance has every point in [0,2] as a minimizer; arbitrary metrics need not admit the vector midpoint or identity | Scope S1 | The proof earns a unique global midpoint for this objective, not a geometry-independent rule. |

Storyboard gate: PASS. All assumptions, a precise statement, the complete proof, a worked example, uniqueness, and scope are retained. No experiment or paper figure is inserted to mimic an empirical deck.

## Task 3: Adaptive Draft Length Proposal

Audience: ML researchers interested in serving. Duration: 8 minutes. Objective: turn one engineering concern into a falsifiable proposal without presenting a gain as observed. Evidence kind: untested proposal. Source: `fixtures.md#p1-adaptive-draft-length-proposal`; authored design choices in `adaptive/source-notes.md`. Delivery: seven-page Beamer PDF.

Governing tensions: more drafted tokens versus the work needed to obtain accepted output; request latency versus aggregate throughput under batch load. Both are proposed evaluation lenses, not measured phenomena in this fixture.

| Page / seconds | Audience question | Slide claim | Governing tension | Evidence | Exact source | Spoken bridge / callback |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / 15 | What is being proposed? | Adaptive draft length under batch load | Both lenses | Title explicitly says proposal | P1 | We have one concern and no measurements yet. |
| 2 / 65 | What might change under batching? | Batching may change verification cost | Draft length versus useful work | Toy draft/verify process, K and B definitions, unmeasured-concern label | P1; model M1 | Before optimizing that cost, the output distribution must stay correct. |
| 3 / 70 | What must a speed comparison preserve? | Every comparison must preserve the target distribution | Correctness versus optimization | Target p, emitted distribution q, q=p contract; fixed verifier and decoding settings | P1; contract C1 | A legal length policy can still be a bad performance policy. |
| 4 / 70 | What would the adaptive policy do? | The useful draft length may depend on load | Draft length versus useful work | Labeled hypothesis and proposed calibration-based length choice | Hypothesis H1; mechanism M2 | We need a crossed experiment to learn whether the load/length interaction exists. |
| 5 / 95 | What can isolate that interaction? | A crossed experiment tests load against draft length | Both lenses | Proposed B by K grid; fixed-length baselines; held-out load traces | Plan V1 | The comparison must report request and system outcomes together. |
| 6 / 85 | What would count as evidence? | Latency and throughput need a shared evaluation setting | Latency versus throughput | Metric definitions for latency, throughput, acceptance; repeated trials and conditions | Plan V2 | A policy that changes the distribution or loses after overhead fails this test. |
| 7 / 80 | What could reject the idea? | The proposal can fail even when drafting is faster | Both lenses recovered | Correctness failure, no robust held-out trade-off gain, overhead erases benefit | Falsifiers F1 | Only future measurements and correctness checks can earn a performance claim. |

Storyboard gate: PASS. The setup concern, hypothesis, proposed mechanism, baseline, correctness contract, planned measurements, and falsifiers are explicit. All numeric grid values are proposed design choices. There are no scores or implied achieved gains.
