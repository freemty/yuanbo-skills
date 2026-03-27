# Style Principles

Five executable writing principles distilled from Jiajun Wu, Alexei Efros, Ruoshi Liu, Bill Freeman, and Phillip Isola.

These are not templates — they are thinking tools. Apply them during brainstorming to shape the story, and during polishing to verify the writing landed.

## Principle 1: Question-First

Open with a question or phenomenon that makes the reader curious. Never open with "Recent advances in X..."

The opening paragraph sells the *problem*, not your solution. The reader should finish paragraph 1 thinking "I want to know the answer to that."

**Exemplars:**
- Wu: "What are the levels of abstraction needed by AI systems in their representations, and where do they come from?" — traces to the origin of the question itself
- Isola: "How can intelligence emerge from 'scratch', without imitating another intelligence's cultural artifacts?" — points at the fundamental mystery
- Freeman: "What can we learn from hitting everything with a drumstick?" — a concrete, almost absurd action that opens into serious science

**Test:** Read your first paragraph aloud. If it sounds like it could open any paper in your subfield, it's too generic. If a curious non-expert would keep reading, you're on track.

## Principle 2: One Killer Metaphor

Find one cross-disciplinary image for your core insight. One is enough — more turns academic writing into creative writing.

The metaphor should compress your paper's core idea into something a reader can *see*. It becomes the paper's identity.

**Exemplars:**
- Liu: "Humans as Light Bulbs" — thermal radiation reconstruction compressed into three words
- Freeman: "A big world of tiny motions" — oxymoron creates tension between scale and subtlety
- Isola: "Language as a Camera" — reframes language as a viewfinder that selects what to see
- Freeman: "Feathers, Wings, and the Future of Computer Vision" — biomimicry as lens for CV research direction

**Test:** If the metaphor needs a sentence of explanation to make sense, find another one. The best metaphors are immediately vivid and only reveal their depth on reflection.

**Constraint:** One core metaphor per paper. It should appear in the intro hook, echo in the method motivation, and close the loop in the conclusion. Different sections may use small illustrative analogies, but the *identity metaphor* is singular.

## Principle 3: Intellectual Lineage

Make the reader feel your work stands on giants' shoulders, woven naturally into the narrative.

This is NOT citation-stacking ([1-15]). It's showing the reader the *thread of ideas* that leads to yours — who asked the question first, who changed direction, where the current thinking breaks down.

**Exemplars:**
- Wu: Project names as tributes — Galileo (physics-based vision), MarrNet (David Marr's computational vision theory)
- Efros: Temporal markers — "autoregressive image generation — since 1999; visual data scaling — since 2007" — timeline implies pioneering without saying "I was first"
- Isola: Conceptual ancestry — "Platonic Representation Hypothesis" connects to Plato's theory of forms

**How to apply:** In the brainstorm phase, ask "Who first thought about this problem? What were the turning points?" Use the answers to structure your Prior Art paragraph as a *journey*, not a list.

## Principle 4: Concrete-to-Abstract Bridge

Start with something specific and perceivable, then zoom out to the technical problem.

The reader enters through a *scene* — a physical phenomenon, a human experience, a vivid example — and only then encounters the abstraction. This is the opposite of "Task X is important because..."

**Exemplars:**
- Freeman: "What can we learn from hitting everything with a drumstick?" → visual vibration analysis of materials
- Isola: "Language as a Camera" → language as a mechanism for selecting and framing world observations
- Liu: "What You Can Reconstruct from a Shadow" → shape-from-shadow reconstruction, framed as detective work
- Freeman: "Revealing Invisible Changes in the World" → computational photography that amplifies imperceptible motion

**How to apply:** During brainstorming Q4, ask "What does your work remind you of?" If the user gives a concrete image, that's your bridge. If not, search for analogies from physics, biology, cognitive science, or everyday experience that map onto the technical core.

## Principle 5: Restrained Voice

Warm but not sentimental. Opinionated but not boastful. Present but not performative.

Academic writing with voice means: choosing which question to open with (opinion), which metaphor to use (taste), which work to cite as lineage (stance). It does NOT mean exclamation marks, superlatives, or self-congratulation.

**Exemplars:**
- Efros: "I (try to) practice Slow Science" — a quiet manifesto in parentheses
- Efros: "still remembered in lovely Oxford" — warmth through adjective choice, not through grand statements
- Wu: "drawing inspiration from nature, i.e., the physical world itself, and from human cognition" — precise and philosophical, no filler

**Anti-patterns (hard rules):**
- "remarkably", "significantly outperforms", "impressive results" — let numbers speak
- "It is worth noting that..." — filler, cut it
- "Our method achieves state-of-the-art performance" in paragraph 1 — no suspense, too early
- "Recent advances in X have achieved remarkable progress" — the most generic opening in ML papers

## Anti-Pattern Quick Reference

| Pattern | Problem | Fix |
|---------|---------|-----|
| "Recent advances in X..." opening | Generic, zero curiosity | Replace with question, phenomenon, or concrete scene |
| Metaphor pileup (2+ per paragraph) | Reads like creative writing, not academic | One core metaphor per paper, small analogies sparingly |
| Citation bombing [1-15] | Lazy, no intellectual thread | Weave 3-5 key works into a narrative of ideas |
| "In this paper, we propose..." in ¶1 | Reveals solution before establishing tension | Move to ¶4-5, after the gap is felt |
| Passive voice wall | Drains energy from the writing | Mix active and passive; use active for claims and contributions |
| "Furthermore/Moreover/Additionally" chain | Mechanical connectors signal AI or lazy writing | Use cause-effect, contrast, or refinement transitions |
| Every paragraph = topic-detail-summary | Predictable structure numbs the reader | Vary paragraph shapes: some build, some contrast, some zoom in |
