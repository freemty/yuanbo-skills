# Worked Example: Parallel Decoding

Mode: `idea` with embedded `survey` evidence. Audience: ML researchers outside systems.

| Audience question | Slide claim | Evidence |
| --- | --- | --- |
| What happens during inference? | Prefill processes known context together; decode grows output one token at a time. | Direct prefill/decode process figure |
| Why is decode slow? | Low-batch decode streams large weights while leaving compute underused. | Bound comparison or roofline evidence |
| Why can parallel work help? | One weight stream can support several token decisions while spare FLOPs remain. | One sourced bottleneck figure + plain-language consequence |
| What do methods share? | MTP, diffusion, and speculative decoding all trade extra compute for fewer serial decisions. | Three-family map |
| What breaks? | Future positions lose dependence on the tokens actually sampled before them. | Minimal language example or paper evidence |
| How do papers repair it? | Training, refinement/block order, or target verification restore different amounts of causality. | Core paper method figures |
| What is the speculative contract? | A drafter proposes several tokens; the target verifies once and keeps only the accepted prefix. | Source-native draft/verify figure |
| What determines speed? | Longer drafts help only when acceptance stays high and draft/verification cost stays low. | Source scaling plot plus one interpretable latency equation |
| What should remain? | The frontier is useful accepted tokens per expensive pass, not raw proposal length. | Four-sentence takeaway |

This ordering is problem-driven. Paper names enter only after the audience understands the shared pressure.

## Speculative-decoding subsection

Introduce two trade-offs before the individual papers and recover them once at the subsection ending:

1. **Draft intelligence versus draft cost/length.** A stronger drafter may improve acceptance but erase the latency saved; a longer draft helps only if enough of it survives verification.
2. **Parallelism versus causality.** Predicting positions together is cheap but removes dependence on the sampled prefix; successful parallel drafters restore that dependence without returning to full autoregression.

Use the papers as answers to these tensions. Do not expose private labels such as `T1`, `T2`, or `T3` in the slide titles. Keep the SRAM/FlashAttention analogy in backup unless it is necessary to establish the memory-traffic premise.
