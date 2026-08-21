# Closed-Loop Gate Resolution

Use this reference when an evidence gate does not resolve on its first pass.
The purpose is to close the parent engineering loop without weakening the gate,
repeating blind attempts, or growing a permanent orchestration system.

## Contents

1. [The control criterion](#the-control-criterion)
2. [Minimal loop state](#minimal-loop-state)
3. [Recursive recovery](#recursive-recovery)
4. [Progress and stability](#progress-and-stability)
5. [Reframing and learning](#reframing-and-learning)
6. [Resolution and escalation](#resolution-and-escalation)
7. [Evidence base](#evidence-base)

## The control criterion

A gate is a feedback control, not a stop sign. Its failure is an error signal:
the observed state does not yet justify the next commitment. Hold promotion to
later stages, diagnose the discrepancy, change the state or the model with an
evidence-producing action, and measure again.

A verdict alone is not a closed loop. A useful loop has:

- a parent outcome and gate criterion;
- an observation of the current state;
- a discrepancy that can change the parent decision;
- an authorized action capable of affecting or revealing that state; and
- feedback that returns to the same parent gate.

Do not claim control-theoretic convergence for an open-ended agent task. Use
the discipline to make progress observable and bounded.

## Minimal loop state

Keep only enough state to return cleanly to the parent:

```text
Gate frame
  parent outcome and owning gate
  criterion and observed discrepancy
  assumptions and hard invariants
  evidence digest and frame version
  progress measure and risk-scaled budget
  child deliverable and return condition

Attempt
  predicted result and chosen action
  actual observation and evidence delta
  disposition and retry condition
```

This is a reasoning record, not a requirement to add classes, storage, or a
workflow engine. For a small task it may be one sentence. Version the frame
only when a goal, constraint, boundary, success criterion, or material
assumption changes.

## Recursive recovery

1. **Hold.** Do not enter a later five-step stage while the owning gate is
   unresolved.
2. **Diagnose.** Distinguish a product defect from a faulty requirement,
   assumption, observation, test oracle, or environment.
3. **Shrink.** Select one discrepancy whose resolution can change the parent
   decision. Define a child with one deliverable and a strictly narrower
   decision boundary.
4. **Recurse.** Run Five-Step Engineering from step 1 on that child. Delete or
   revise its own invalid requirements before optimizing a remedy.
5. **Probe.** Predict what would distinguish the live explanations, then run
   the smallest safe and reversible experiment, inspection, or implementation.
6. **Observe.** Capture the actual result. A new explanation without a new
   signal is not evidence.
7. **Return.** Bring back only evidence, a decision, or a necessary artifact;
   discard temporary investigative complexity.
8. **Re-evaluate.** Run the owning parent gate again. Child success never
   implies parent success without recomposition and verification.

Prefer one active child that changes the parent decision over a tree of
interesting investigations. Keep an alternative available for consequential
choices; the locally closest action may have worse total cost or risk.

## Progress and stability

Maintain both:

- **Invariant:** scope, authorization, safety, privacy, data integrity,
  compatibility, and other hard constraints remain true.
- **Progress measure:** a relevant uncertainty, unmet condition, risk,
  candidate explanation, or unnecessary mechanism strictly decreases; or
  new evidence falsifies and replaces a governing assumption.

Do not use token count, prose volume, or another action taken as progress.
Normalize an attempted state by its frame version, gate, evidence, assumptions,
and action. Do not retry the same state and action after the same result unless
the retry condition or evidence has changed.

Avoid unstable correction:

- wait for the expected observation latency before acting again;
- use tolerances for noisy measures instead of reacting to every fluctuation;
- do not let multiple child loops modify the same state concurrently;
- detect add/remove oscillation and repeated states;
- bound depth, time, cost, and blast radius according to risk and information
  value, not an arbitrary universal retry count.

When progress stalls, change the action, observation, representation, or frame.
More of the same is not persistence.

## Reframing and learning

Use single-loop correction first: change an action while preserving the parent
goal and hard constraints. Return to step 1 and reframe when evidence rejects a
governing assumption, no valid action exists in the current problem space, or
different actions reproduce the same class of failure.

A reframe must change at least one of the goal, constraint, boundary, success
criterion, causal model, or test oracle, state why, and produce a falsifiable
next probe. Do not silently relax a gate to manufacture success. Changing a
user-owned outcome or hard constraint requires the user's decision.

After verified resolution, record only a conditional lesson: triggering
conditions, relevant assumptions, result, exceptions, and when retry becomes
valid. Do not generalize a lucky success into a universal rule.

## Resolution and escalation

A parent gate is resolved when one of these dispositions is evidenced:

- **Pass:** the criterion is satisfied.
- **Revise or delete:** the criterion or requirement is false, stale, or
  mis-scoped; restart from the step that owns it.
- **Abandon:** the candidate path is infeasible or dominated; evaluate a live
  alternative.
- **External decision:** an authorized owner decides a trade-off the agent
  cannot make.

Escalate only when the next meaningful state change requires unavailable
external facts or tools, new authority, an irreversible consequential choice,
or crossing a hard safety or resource boundary. Report the parent gate, exact
missing condition, evidence gathered, alternatives attempted, and smallest
request that makes resumption possible.

Difficulty, uncertainty, an initial failed test, or exhausted ideas inside one
frame are not external blockers. Reframe or find a new evidence channel first.

## Evidence base

This protocol is an engineering synthesis; no cited work proves that an
open-ended LLM agent will always converge.

- Boehm's risk-driven [Spiral Model](https://doi.org/10.1109/2.59) uses nested
  cycles and evidence-producing risk reduction before greater commitment.
- NASA defines iteration as repeating a process to correct discrepancies and
  directs verification failures through diagnosis, replanning, redesign, and
  reverification to closure in its [common technical processes](https://www.nasa.gov/reference/2-1-the-common-technical-processes-and-the-se-engine/)
  and [product verification process](https://www.nasa.gov/reference/5-3-product-verification/).
- Brun and colleagues treat feedback loops as first-class architectural
  elements and analyze nested controllers, latency, stability, and interaction
  in [Engineering Self-Adaptive Systems through Feedback Loops](https://doi.org/10.1007/978-3-642-02161-9_3).
- Newell, Laird, and Rosenbloom's [Soar architecture](https://doi.org/10.1016/0004-3702(87)90050-6)
  turns an impasse into a subgoal and returns its result to the parent context.
- Dijkstra's [guarded-command derivation](https://doi.org/10.1145/360933.360975)
  supplies the invariant-and-decreasing-variant discipline behind meaningful
  bounded recursion.
- Argyris distinguishes correction within a governing frame from changing the
  frame itself in [single- and double-loop learning](https://doi.org/10.2307/2391848).
- Counterexample-guided abstraction refinement separates a real defect from a
  faulty model and refines only relevant detail in
  [Clarke et al.](https://doi.org/10.1145/876638.876643); delta debugging
  narrows failure causes through controlled experiments in
  [Zeller and Hildebrandt](https://doi.org/10.1109/32.988498).
- ReAct interleaves reasoning, action, and environmental observation in
  [Yao et al.](https://openreview.net/forum?id=WE_vluYUL-X), but evidence on
  intrinsic self-correction warns against blind reflection: see
  [Huang et al.](https://openreview.net/forum?id=IkmD3fKBPQ) and the
  [Kamoi et al. critical survey](https://doi.org/10.1162/tacl_a_00713).
