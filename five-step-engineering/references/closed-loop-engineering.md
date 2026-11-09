# Closed-Loop Gate Resolution

Use this reference when a gate remains unresolved or feedback is slow or
inconclusive. Close the engineering loop with evidence that changes a decision,
while preserving its acceptance criteria and structural obligations.

## Contents

1. [The control criterion](#the-control-criterion)
2. [Effective feedback](#effective-feedback)
3. [Minimal loop state](#minimal-loop-state)
4. [Recursive recovery](#recursive-recovery)
5. [Development failures](#development-failures)
6. [Progress and stability](#progress-and-stability)
7. [Reframing and learning](#reframing-and-learning)
8. [Resolution and escalation](#resolution-and-escalation)
9. [Evidence base](#evidence-base)

## The control criterion

A gate controls accepting a candidate, scaling it, and work that depends on
its unverified assumptions. Preserve the five-step decision order while using
tests, measurements, and reversible prototypes at any stage to resolve the
owning decision. Re-evaluate that gate with the results before committing.

The working loop is:

`Hypothesis -> Representative probe -> Observe -> Keep, revise, or delete -> Recheck owning gate`

Before broad implementation, test the consequential unknown most likely to
change the design. A probe needs a question, a predicted distinguishing result,
and an observation sufficient for its scope. A clear small change can proceed
directly to implementation and relevant checks. Scale the five steps to
meaningful decisions rather than repeating them for every edit.

## Effective feedback

Use this engineering interpretation:

`Effective progress rate ≈ Verified progress per iteration / Complete feedback cycle time`

Compare the same outcome and quality criteria; disproving an important
assumption also produces learning. The expression is a reasoning aid, not a
universal law or a scoring protocol. In the
[November 6, 2026 interview](https://www.elonmuskarchive.org/video/baron-investment-conference-2026-11-06),
Musk linked iteration frequency with progress per iteration and proposed
reducing a research-fab cycle from roughly a year to a month. The latter was
an aspiration, not an achieved result or a guaranteed software speedup.

Observe elapsed time from the question through setup, implementation, checks,
waiting, interpretation, and the next decision. Reduce the dominant observed
delay with existing tools. Use available timings when useful; a small task
needs no timing log, fixed quota, or monitoring system.

Slice work into verifiable behavior and exercise the relevant integration
boundary early. Accumulating file-by-file fragments before any integrated
feedback defeats small batches
([DORA](https://dora.dev/capabilities/working-in-small-batches/)).
Use quick checks that discriminate the current hypothesis, integration checks
for affected contracts, and necessary full checks before completion
([DORA on fast and comprehensive feedback](https://dora.dev/capabilities/continuous-integration/)).
Keep the final acceptance criteria and expose the limits of substitutes or
simulations. After observing a result, keep, revise, or delete the candidate,
retire superseded paths, and recheck the parent behavior and structure.

Feedback operates throughout the five steps. Step 4 improves a feedback
process already justified by steps 1–3; reuse existing automation immediately,
and build new automation only when its necessity and lifecycle cost earn it.

## Minimal loop state

Keep enough context to return to the parent: its outcome, gate criterion,
discrepancy, assumptions, protected invariants, and the child's return
condition. Compare the predicted result of an action with the observed result
and state what changed. Scale effort to risk and information value.

Use the conversation or the project's existing decision record. A small task
may need one sentence. Update the reasoning when an assumption or criterion
changes; do not create a tracking system for it.

## Recursive recovery

1. **Hold commitment.** Keep acceptance, scaling, and dependent work pending
   while gathering evidence for the unresolved gate.
2. **Diagnose.** Distinguish a product defect from a faulty requirement,
   assumption, observation, test oracle, or environment.
3. **Shrink.** Select one discrepancy whose resolution can change the parent
   decision. Define a child with one deliverable and a strictly narrower
   decision boundary.
4. **Recurse.** Run Five-Step Engineering from step 1 on that child. Delete or
   revise its own invalid requirements before optimizing a remedy.
5. **Probe.** Predict what would distinguish the live explanations, then run
   the smallest representative, safe, and reversible experiment, inspection,
   or implementation.
6. **Observe.** Capture the actual result. A new explanation without a new
   signal is not evidence.
7. **Return.** Bring back only evidence, a decision, or a necessary artifact;
   discard temporary investigative complexity.
8. **Re-evaluate.** Run the owning parent gate again. Child success never
   implies parent success without recomposition and verification.

Prefer one active child that changes the parent decision over a tree of
interesting investigations. Keep an alternative available for consequential
choices; the locally closest action may have worse total cost or risk.

## Development failures

Read the actual failure from the project's test, compiler, architecture check,
or observed behavior. Check its assumptions and environment before trusting
the diagnosis. Fix the observation channel if it is invalid.

Apply the recursive loop to the smallest concrete discrepancy. Before adding a
guard, retry, or alternate path, inspect the representation, owning module,
contract, and requirement that produced the failure. Deleting duplicate state
or repairing a boundary may eliminate the entire failure class. Add a
mechanism only when a verified constraint rules out the simpler alternative.

Trace related callers and state owners far enough to repair the end-to-end
behavior. Remove superseded paths and investigative artifacts, then rerun the
owning check and relevant regressions. Inspect the retained structure even
when tests pass. Necessary compatibility paths still require real consumers,
an owner, and an exit condition.

Do not weaken a check or rewrite a justification to manufacture success.
Unresolved behavior or structure stays in this loop while safe experiments
and repairs continue.

## Progress and stability

Maintain both:

- **Invariant:** scope, authorization, safety, privacy, data integrity,
  compatibility, and other hard constraints remain true.
- **Progress measure:** a relevant uncertainty, unmet condition, risk,
  candidate explanation, or unnecessary mechanism strictly decreases; or
  new evidence falsifies and replaces a governing assumption.

Do not use token count, prose volume, or iteration count as progress. A failed
experiment that rules out a consequential explanation is useful evidence.
Describe repeated failures using the actual code, assumptions, evidence, and
action. Do not repeat the same failed attempt unless its evidence or retry
condition changes; no hashes or additional state registry are needed.

Avoid unstable correction:

- wait for an action's result at the expected observation latency before
  correcting the same state again;
- use tolerances for noisy measures instead of reacting to every fluctuation;
- do not let multiple child loops modify the same state concurrently;
- detect add/remove oscillation and repeated states;
- bound depth, time, cost, and blast radius according to risk and information
  value, not an arbitrary universal retry count.

When progress stalls, change the action, observation, representation, or frame.
More of the same is not persistence.

These practices make progress observable and bounded; they do not establish
control-theoretic convergence for an open-ended agent task.

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
