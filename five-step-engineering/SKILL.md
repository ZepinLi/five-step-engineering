---
name: five-step-engineering
description: Apply the ordered Five-Step Engineering Process to design, build, redesign, or optimize a system, codebase, data model, architecture, pipeline, product, or workflow. Use when an agent should question requirements, remove unnecessary parts before optimizing, keep data and dependencies clear, justify patterns and abstractions with evidence, resolve failed gates through bounded evidence-producing recursion, shorten feedback cycles, and automate only proven work.
---

# Five-Step Engineering

Use this ordered decision protocol, scaled to the decision at hand:

`Question requirements -> Delete -> Simplify and optimize -> Accelerate feedback -> Automate`

## Prime directive

**Do not optimize something that has not earned the right to exist.**

- Treat requirements as hypotheses, not facts.
- Require complexity to justify itself with current evidence.
- Use deletion as a search operator to reveal the system's real constraints, dependencies, and value.
- Prefer eliminating an invalid state or implicit contract over adding another branch or check for it.
- Treat every pattern, layer, service, and extension point as a design hypothesis, not a target.
- Treat unknown mechanisms as investigation candidates, not deletion candidates.
- Do not count moving complexity, risk, or manual work to users, downstream systems, or operations as deletion.
- Seek the minimum sufficient system, not maximum deletion.
- Keep the order mandatory. A failed gate blocks promotion, not problem solving.
- If a later step invalidates an assumption, open a nested five-step loop around that assumption, resolve it, then return to the gate that owns it.

## Scope and safeguards

Before starting:

1. Define the outcome, measurable success, and decision boundary.
2. Separate hard constraints from the proposed solution; name unacceptable failures.
3. Scale evidence and reversibility to blast radius, irreversibility, and uncertainty.

- Stay within the requested scope. For a narrow change, note broader deletion opportunities without turning them into an unsolicited redesign.
- During an incident, restore service first; analyze the design afterward.
- For public APIs, persisted formats, schemas, and unknown external consumers, analyze compatibility and deprecate safely instead of removing them abruptly.
- Preserve legal, safety, security, privacy, and data-integrity outcomes. Question their assumptions and implementation, not the protected outcome.
- Preserve essential domain complexity and model it plainly; delete accidental complexity instead of hiding real constraints.
- If consequential behavior is unknown and cannot be tested reversibly, investigate or ask; do not delete.

## Apply the five gates

### 1. Question every requirement

- Within the decision boundary, trace each requirement to an accountable owner or verifiable artifact: issue, PR, spec, test, benchmark, or compliance clause.
- Ask what outcome it protects, what would fail without it, and whether it is stale, mis-scoped, or over-specified.
- Translate qualities such as "robust," "elegant," "scalable," or "maintainable" into a concrete stimulus, environment, response, and measurable bound.
- Do not treat a department, convention, authority, or "best practice" as evidence. Seniority does not reduce error.
- If neither owner nor artifact exists, inspect first; ask the user when the answer would change a consequential decision. Do not treat absence of evidence as permission to delete.

**Gate:** Support or reject every requirement driving the decision with evidence. Let an unresolved unknown that could change the decision block the gate.

### 2. Delete the part or process

- Prefer removing a whole component, abstraction, step, handoff, state, flag, or config over improving it.
- Delete speculative layers, wrappers, patterns, services, and extension points; first check whether the language, platform, or existing component already provides the capability.
- Ask: "If this did not exist, what concrete failure would occur?" Answer with a check, not intuition.
- Count net system cost. Treat a deletion that exports work or failure modes elsewhere as a possible regression.
- Keep changes narrow and separable. For risky changes, use a bounded, observable experiment with rollback; never alter unrelated user work or create commits unless asked.
- Use "roughly 10% gets added back" only as a calibration prompt across repeated low-risk experiments, never as a quota or universal law.

**Gate:** Delete on evidence of net benefit, retain on evidence of necessity, and investigate consequential uncertainty.

### 3. Simplify and optimize

- For code, data-model, or architecture work, read [references/structural-design.md](references/structural-design.md) and scale its checks to the decision.
- Design what survived in this order: legal data and state transitions; ownership and boundaries; dependency direction and failure behavior; then patterns or frameworks.
- Name the authoritative source and owner for each fact; mark caches and derived views as such. Make important invariants explicit, keep representations private, and validate untrusted data at the boundary before converting it to a valid domain value.
- Give each non-trivial module one coherent purpose and a design decision or source of volatility to hide. Prefer a small, stable interface over control flags, broad records, mutable internals, or hypothetical options.
- Before adding a pattern or abstraction, name the concrete force, the simplest direct solution, the added concepts and liabilities, and the evidence that earns them. Introduce only its smallest useful form.
- Make control flow, data flow, state ownership, and dependency direction explainable. Add a diagram or decision record only when it answers a named concern.
- State relevant errors, side effects, ordering, idempotency, compatibility, and partial-failure behavior; do not call a design robust without a failure scenario and check.
- Optimize only a measured bottleneck in what survived.
- Verify the end-to-end outcome; a better local metric can hide a worse system.

**Gate:** Make the simplest coherent mechanism meet the outcome and quality scenarios. A reviewer must be able to explain its valid state, ownership, boundaries, dependencies, failure behavior, and why each abstraction is cheaper than the direct alternative.

### 4. Accelerate the cycle

- Shorten the path from change to trustworthy real-world feedback.
- Cut batch size, handoffs, waiting, and validation latency.
- Prefer a small behavior-preserving refactor or throwaway spike over a speculative framework; keep each structural decision reversible where practical.
- Measure the full cycle; do not trade nominal speed for rework, hidden risk, or weaker signal.

**Gate:** Make learning measurably faster without reducing signal quality.

### 5. Automate

- Automate only work proven necessary, stable, repetitive, and understood.
- Keep observability, failure handling, rollback, and a manual escape path.
- Retry only operations known to be retriable and idempotent; bound attempts, use backoff with jitter, and avoid retries at multiple layers.
- Reject automation that only makes waste run faster.

**Gate:** Make automation lower total lifecycle cost and risk, not just manual effort.

## Require evidence

- **Purpose and reachability:** Search references repository-wide, including entry points, config strings, and dynamic dispatch; inspect history, specs, issues, and tests.
- **Actual behavior:** Use tests, coverage, logs, metrics, traces, or a representative workload.
- **Actual cost:** Benchmark or profile end-to-end. Do not claim a bottleneck from code reading alone.
- **Removal:** Run the smallest reversible counterfactual and relevant checks; use CI or real workloads only when available and authorized.
- **Structural integrity:** Test invalid construction, legal and illegal state transitions, boundary values, aliasing, error paths, and serialization round trips where relevant.
- **Change locality:** Exercise one likely change or failure and inspect which modules, interfaces, data, and operations it crosses; use dependency and co-change history as clues, not universal scores.
- **Compatibility:** For public or persisted contracts, test relevant old/new producer-consumer combinations and distinguish source, wire, and semantic compatibility.
- Do not equate "not observed" with "cannot occur." State sampling limits.
- If evidence is unavailable, mark the conclusion unverified and make the missing evidence the next child problem. It blocks stage promotion, not the task.

## Resolve failed gates recursively

When a gate does not resolve on the first pass, read [references/closed-loop-engineering.md](references/closed-loop-engineering.md). Hold later stages and keep working on the current gate:

1. Name the discrepancy: the gate criterion, observed evidence, remaining uncertainty, and consequence of being wrong.
2. Check the evaluator before changing the product. Locate the failure in the requirement, assumption, evidence, test or environment, or implementation.
3. Make the highest-value unresolved discrepancy a strictly narrower child problem. Apply all five steps to it from step 1.
4. State a prediction and take the smallest safe, reversible action that can distinguish alternatives. Observe the result and update the evidence.
5. Return only the new evidence, decision, or necessary artifact to the parent. Re-evaluate the same parent gate and resume from it when resolved.
6. If it remains unresolved, choose a different evidence-producing action, shrink the problem again, or question the governing requirement, measure, test oracle, or boundary. Never repeat an unchanged attempt without new evidence.

Each cycle must preserve hard constraints and produce semantic progress: reduce a relevant uncertainty, eliminate an alternative, satisfy a missing condition, simplify the mechanism, or revise a falsified assumption. Wait for an action's result before correcting again; avoid concurrent loops that change the same state.

Continue autonomously while a safe, in-scope, authorized action can change the decision state. Escalate only when progress depends on unavailable external state, authority, an irreversible trade-off, or a hard safety or resource boundary. Return a resumable record of the evidence, attempts, exact missing condition, and smallest unblocking request.

A gate is resolved when it passes; its criterion is revised or deleted with evidence; the candidate path is shown infeasible and abandoned; or an authorized external decision closes it. Ending at step 2 or 3 is success only when the requested outcome is met and later steps are unnecessary—not when a resolvable gate was left open.

## Example

Request: "Add a cache to speed up this legacy adapter."

- Do not begin by designing cache keys, eviction, and invalidation.
- First trace consumers and runtime traffic. If migration is complete and a contract inventory confirms no external users, deprecate and delete the adapter. If it remains necessary, measure it before simplifying or caching it.

## Produce the decision

Return only what helps the decision:

1. **Target:** State the outcome, boundary, success measure, and hard constraints.
2. **Evidence:** State what is known, tested, and still unknown.
3. **Decision:** State what was deleted, kept, revised, or abandoned and how each reached gate was resolved. For structural work, include the data invariants, boundaries and dependencies, failure behavior, and simplest rejected alternative needed to justify the design.
4. **Next:** For an action request, perform the next safe in-scope action and keep re-evaluating; do not hand resolvable work back to the user. If genuinely blocked, give the exact external condition, evidence and attempts so far, and smallest unblocking request.

Omit empty sections. Mention deferred optimization or automation only when doing so prevents wasted work now.
