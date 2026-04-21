---
name: paper-review
description: |
  Use when the user provides a paper PDF for academic peer review, mentions "review this
  paper", "write a review", "peer review", references OpenReview/CMT/HotCRP submission
  forms, shares reviewer guidelines, or wants to evaluate a paper for a specific venue
  (ECCV, NeurIPS, ICLR, CVPR, ACL, ICML, etc.). Also trigger when the user shares a
  paper folder path with a venue name, review form fields, or a target score.
---

# Paper Review

Multi-role academic peer review that produces submission-ready output matching venue form fields.

## Why Multi-Role

A single-pass review has blind spots. Four complementary expert lenses — domain, modeling, experiments, systems — catch different classes of issues. Cross-reviewing then surfaces what's consensus vs. disagreement, so the final review is calibrated rather than one-sided. Every claim in the output must trace to specific evidence in the paper (section, table, figure, equation).

## Phase 1: Read and Extract

Before anything else, read the full paper + supplementary. For PDFs > 10 pages, read in chunks using the `pages` parameter.

Extract and write down:

1. **Metadata**: title, venue, submission number, contribution type (CT) if declared
2. **Core idea**: one sentence
3. **Method pipeline**: 3-5 numbered technical components with specifics (model sizes, loss functions, key hyperparameters)
4. **Experimental setup**: datasets (with sizes), baselines (with years), metrics, ablations
5. **Key numbers**: reproduce important table rows with exact values — these go into subagent prompts since subagents cannot read PDFs
6. **Supplementary findings**: additional experiments, real-world results, acknowledged limitations

If the user provided venue guidelines or a review form, parse the required fields. See `references/venue-formats.md` for field mappings across OpenReview, CMT, and HotCRP venues. If no venue is specified, ask the user or default to NeurIPS/ICML style.

## Phase 2: Assign 4 Expert Roles

Select roles based on the paper's domain. The goal is non-overlapping analytical coverage.

| Paper Domain | Role A | Role B | Role C | Role D |
|---|---|---|---|---|
| 3D / Rendering | Domain (3D representations) | Paradigm (diffusion/AR/flow) | Evaluation methodology | Compute & scalability |
| NLP / LLM | Task domain | Architecture & training | Benchmark & statistics | Inference & serving |
| RL | Environment & reward | Algorithm & convergence | Reproducibility | Sample efficiency |
| Theory | Mathematical foundations | Proof techniques | Empirical validation | Connections to practice |
| Datasets | Data quality & bias | Annotation methodology | Benchmark utility | Scale & access |

Adapt freely: theory-heavy paper → replace systems with proof reviewer. Dataset paper → replace modeling with annotation quality. The point is 4 distinct lenses.

## Phase 3: Parallel Independent Reviews

Spawn all 4 reviewer subagents in a single message for concurrency. Use `subagent_type: "labmate:domain-expert"` if available; otherwise use the default general-purpose agent.

Each subagent prompt must be fully self-contained — it has no access to PDFs or conversation history. See `references/role-templates.md` for the required prompt structure: identity block, full paper summary with numbers, 4-6 pointed analytical questions, and output format.

**The single most important thing**: the paper summary block in each prompt must include concrete numbers from the extracted tables. A prompt saying "results are competitive" produces hollow reviews. A prompt saying "FID 5.68 vs L3DG's 8.49, 33% improvement" produces grounded ones.

Each reviewer outputs:
- **Strengths** (3-5): with specific evidence citations
- **Major Weaknesses** (3-5): issues that drive the score
- **Minor Weaknesses** (2-3): fixable, do not drive score
- **Score**: on the venue's scale
- **Key Questions** (2-3): what the authors should address in rebuttal

Under Concept & Feasibility CTs, reviewers should not penalize for lacking large-scale experiments — focus on novelty, soundness, and feasibility validation credibility.

## Phase 4: Cross-Review

After all 4 reviews return, build a consensus matrix:

```
| Issue | A | B | C | D | → Final |
|-------|---|---|---|---|---------|
| [specific issue] | Major | Major | Major | — | 3/4 → Major |
| [specific issue] | Minor | — | Major | Major | 2/4 Major → Final Major |
```

Classify each point:
- **Consensus** (3-4 reviewers): high confidence, include as-is
- **Majority** (2 reviewers): moderate confidence, include with nuance
- **Unique but compelling** (1 reviewer): include if well-argued with evidence
- **Disagreement**: present both sides explicitly in the final review

Record the score distribution (all 4 scores + median).

## Phase 5: Synthesize Final Review

Produce output matching the venue's form fields exactly. The default structure (use when no specific form is provided):

- **Title**: short descriptive review title
- **Paper Summary**: 2-4 sentences demonstrating understanding, not parroting the abstract
- **Strengths**: numbered, each with bold topic + evidence-grounded elaboration
- **Major Weaknesses**: numbered, same format — these justify the score
- **Minor Weaknesses**: numbered, fixable in revision
- **Recommendation**: score on venue scale
- **Justification**: 1-2 paragraphs weighing strengths vs weaknesses, referencing CT
- **Rebuttal Suggestions**: specific, actionable, realistic within rebuttal window
- **Confidence**: score + justification
- **Confidential AC Comments**: meta-observations, not scientific critique

### Score-Tone Calibration

If the user provided a target score, calibrate tone:

| Range | Lead with | Weakness framing |
|---|---|---|
| Accept (top tier) | Strengths | Constructive suggestions |
| Weak Accept | Balanced | Roughly equal weight |
| Borderline | Weaknesses slightly | Acknowledge potential |
| Reject | Fundamental issues | Strengths are secondary |

### Language

- Review content: academic English (this gets submitted)
- User communication: Chinese (中文)
- No filler ("it is worth noting...", "importantly...", "interestingly...")
- Every paragraph earns its place

## Common Mistakes

**Hollow subagent prompts.** Forgetting to include exact numbers from the paper in subagent prompts produces reviews that say "results are promising" without citing any actual results. Always reproduce key table rows in the prompt.

**Role collapse.** All 4 reviewers saying the same thing means the analytical focus questions were too generic. Each role's focus questions should reference different aspects of the paper — domain reviewer asks about representation quality, experiments reviewer asks about baseline fairness, etc.

**Overclaiming consensus.** Two reviewers mentioning "speed" in different contexts does not make it a consensus point. Match on the specific technical claim, not keywords.

**Venue format mismatch.** ECCV has Major/Minor weaknesses split; NeurIPS does not. CVPR uses 1-10 scale; ECCV uses 1-6. Always check `references/venue-formats.md` before formatting output.

**Score-tone inconsistency.** A Weak Accept score with language that reads like a Reject ("fundamental issues", "critically flawed") confuses authors and ACs. Calibrate language to match the numeric score.
