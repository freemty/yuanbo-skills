# Venue-Specific Review Formats

## OpenReview Venues (ECCV, NeurIPS, ICLR, EMNLP)

### Common Fields
- Title (short review title)
- Paper Summary
- Strengths (structured)
- Weaknesses — often split into Major/Minor
- Preliminary Recommendation (numeric scale)
- Justification of Recommendation
- Suggestions for Rebuttal
- Confidence Level (1-5)
- Ethics Review Flag (Yes/No)
- Confidential Comments to AC

### ECCV Contribution Types
- Algorithms/General
- Theory/Foundational
- Applied/Systems
- Datasets/Benchmarks
- Concept & Feasibility

When a paper declares Concept & Feasibility:
- Evaluate on: novelty, soundness, claim-evidence alignment, feasibility validation, clarity
- Do NOT treat as weaknesses: lack of large-scale experiments, not achieving SOTA, missing exhaustive ablations, limited deployment

### ECCV Score Scale
- 6: Accept
- 5: Weak Accept
- 4: Borderline Accept
- 3: Borderline Reject
- 2: Weak Reject
- 1: Reject

### NeurIPS Score Scale
- 10: Top 5% of accepted papers
- 8: Top 15-50% of accepted papers
- 6: Marginally above acceptance threshold
- 5: Marginally below acceptance threshold
- 3: Clear reject
- 1: Trivial or wrong

### ICLR Score Scale
- 10: Strong Accept
- 8: Accept
- 6: Weak Accept
- 5: Weak Reject
- 3: Reject
- 1: Strong Reject

### Confidence Scale (most venues)
- 5: Expert
- 4: High confidence
- 3: Moderate confidence
- 2: Low confidence
- 1: Not confident

## CMT Venues (CVPR, AAAI)

### CVPR Fields
- Summary
- Strengths
- Weaknesses
- Questions for Authors
- Overall Rating (1-10)
- Confidence (1-5)
- Recommendation to AC

## HotCRP Venues (ACL, NAACL)

### ACL Fields
- Paper Summary
- Strengths
- Weaknesses
- Questions
- Limitations
- Ethics
- Soundness (1-4)
- Presentation (1-4)
- Contribution (1-4)
- Overall Assessment (1-5)
- Confidence (1-5)

## Adapting to Unknown Venues

If the user pastes a review form you haven't seen before:
1. Parse the field names and required/optional markers
2. Map each field to the closest default field
3. Preserve the exact field names and ordering from the form
4. Ask the user about any ambiguous fields
