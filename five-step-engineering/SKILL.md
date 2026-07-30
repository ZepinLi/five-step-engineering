---
name: five-step-engineering
description: Apply the ordered Five-Step Engineering Process to redesign or optimize a system, codebase, pipeline, product, or workflow. Use when an agent should question requirements, remove unnecessary parts or processes before optimizing, simplify what remains, shorten feedback cycles, and automate only proven work.
---

# Five-Step Engineering

Use this ordered decision protocol, scaled to the decision at hand:

`Question requirements -> Delete -> Simplify and optimize -> Accelerate feedback -> Automate`

## Prime directive

**Do not optimize something that has not earned the right to exist.**

- Treat requirements as hypotheses, not facts.
- Require complexity to justify itself with current evidence.
- Use deletion as a search operator to reveal the system's real constraints, dependencies, and value.
- Treat unknown mechanisms as investigation candidates, not deletion candidates.
- Do not count moving complexity, risk, or manual work to users, downstream systems, or operations as deletion.
- Seek the minimum sufficient system, not maximum deletion.
- Keep the order mandatory. If a later step invalidates an assumption, restart at step 1.

## Scope and safeguards

Before starting:

1. Define the outcome, measurable success, and decision boundary.
2. Separate hard constraints from the proposed solution; name unacceptable failures.
3. Scale evidence and reversibility to blast radius, irreversibility, and uncertainty.

- Stay within the requested scope. For a narrow change, note broader deletion opportunities without turning them into an unsolicited redesign.
- During an incident, restore service first; analyze the design afterward.
- For public APIs, persisted formats, schemas, and unknown external consumers, analyze compatibility and deprecate safely instead of removing them abruptly.
- Preserve legal, safety, security, privacy, and data-integrity outcomes. Question their assumptions and implementation, not the protected outcome.
- If consequential behavior is unknown and cannot be tested reversibly, investigate or ask; do not delete.

## Apply the five gates

### 1. Question every requirement

- Within the decision boundary, trace each requirement to an accountable owner or verifiable artifact: issue, PR, spec, test, benchmark, or compliance clause.
- Ask what outcome it protects, what would fail without it, and whether it is stale, mis-scoped, or over-specified.
- Do not treat a department, convention, authority, or "best practice" as evidence. Seniority does not reduce error.
- If neither owner nor artifact exists, inspect first; ask the user when the answer would change a consequential decision. Do not treat absence of evidence as permission to delete.

**Gate:** Support or reject every requirement driving the decision with evidence. Let an unresolved unknown that could change the decision block the gate.

### 2. Delete the part or process

- Prefer removing a whole component, abstraction, step, handoff, state, flag, or config over improving it.
- Ask: "If this did not exist, what concrete failure would occur?" Answer with a check, not intuition.
- Count net system cost. Treat a deletion that exports work or failure modes elsewhere as a possible regression.
- Keep changes narrow and separable. For risky changes, use a bounded, observable experiment with rollback; never alter unrelated user work or create commits unless asked.
- Use "roughly 10% gets added back" only as a calibration prompt across repeated low-risk experiments, never as a quota or universal law.

**Gate:** Delete on evidence of net benefit, retain on evidence of necessity, and investigate consequential uncertainty.

### 3. Simplify and optimize

- Simplify structure, interfaces, state, dependencies, and special cases before tuning anything.
- Optimize only a measured bottleneck in what survived.
- Verify the end-to-end outcome; a better local metric can hide a worse system.

**Gate:** Make the simplest remaining mechanism meet the outcome and constraints.

### 4. Accelerate the cycle

- Shorten the path from change to trustworthy real-world feedback.
- Cut batch size, handoffs, waiting, and validation latency.
- Measure the full cycle; do not trade nominal speed for rework, hidden risk, or weaker signal.

**Gate:** Make learning measurably faster without reducing signal quality.

### 5. Automate

- Automate only work proven necessary, stable, repetitive, and understood.
- Keep observability, failure handling, rollback, and a manual escape path.
- Reject automation that only makes waste run faster.

**Gate:** Make automation lower total lifecycle cost and risk, not just manual effort.

## Require evidence

- **Purpose and reachability:** Search references repository-wide, including entry points, config strings, and dynamic dispatch; inspect history, specs, issues, and tests.
- **Actual behavior:** Use tests, coverage, logs, metrics, traces, or a representative workload.
- **Actual cost:** Benchmark or profile end-to-end. Do not claim a bottleneck from code reading alone.
- **Removal:** Run the smallest reversible counterfactual and relevant checks; use CI or real workloads only when available and authorized.
- Do not equate "not observed" with "cannot occur." State sampling limits.
- If evidence is unavailable, mark the conclusion unverified and state which decision that blocks.

## Maintain decision discipline

- Stop at the first gate that does not pass; do not recommend later-stage work yet.
- Treat ending at step 2 or 3 as a valid success.
- Prefer a cheap experiment over an argument.
- If complexity or exception count grows again, return to step 1 instead of adding another mechanism.

## Example

Request: "Add a cache to speed up this legacy adapter."

- Do not begin by designing cache keys, eviction, and invalidation.
- First trace consumers and runtime traffic. If migration is complete and a contract inventory confirms no external users, deprecate and delete the adapter. If it remains necessary, measure it before simplifying or caching it.

## Produce the decision

Return only what helps the decision:

1. **Target:** State the outcome, boundary, success measure, and hard constraints.
2. **Evidence:** State what is known, tested, and still unknown.
3. **Decision:** State what to delete, keep, or investigate; name the first unresolved gate.
4. **Next:** Give the smallest action that resolves the highest-value uncertainty.

Omit empty sections. Mention deferred optimization or automation only when doing so prevents wasted work now.
