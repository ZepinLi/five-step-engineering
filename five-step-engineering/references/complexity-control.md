# Executable Complexity Control

Use this reference when a code repository opts into the complexity guard, when
the guard reports an unresolved transition, or when changing its policy. The
guard turns structural growth into an explicit decision without pretending
that a metric can decide whether a design is good.

## Contents

1. [Invariant and boundary](#invariant-and-boundary)
2. [Observed complexity](#observed-complexity)
3. [Project policy](#project-policy)
4. [Run the guard](#run-the-guard)
5. [Resolve a failed check](#resolve-a-failed-check)
6. [Automation boundary](#automation-boundary)
7. [Evidence base](#evidence-base)

## Invariant and boundary

Let `O` be the structure visible to the configured checks and let `U_O(S)` be
the positive structural deltas in repository state `S` that lack a current,
matching justification. Promotion is allowed only when:

```text
Accept(S -> S') iff
  U_O(S') is empty
  and no temporary item is overdue
  and every declared hard check passes
```

If the initial accepted state satisfies the condition and every promoted
transition preserves it, observable unearned complexity cannot accumulate in
that state sequence. This is an inductive safety invariant, not a proof that the
program is globally minimal.

The guarantee is conditional on complete observation at the chosen promotion
boundary, policy integrity, honest evidence, and a correct evaluator. General
program semantics cannot be reduced to a decidable minimality test: non-trivial
semantic properties are undecidable in general, and shortest descriptions are
not computable in the unrestricted case. Keep those limits visible rather than
turning proxy metrics into a false theorem.

## Observed complexity

Reason about a vector, not a weighted score:

```text
concepts and responsibilities
legal states and independent truth sources
dependencies, cycles, and change propagation
public interfaces and configuration dimensions
exceptional, compatibility, and duplicate paths
runtime coordination, failure, and operational surfaces
temporary investigative or migration structure
```

The language-independent guard can directly observe only part of this vector.
It compares Git trees and reports:

- tracked text files and non-blank lines;
- added, deleted, modified, and renamed paths;
- changes to configured manifests, workflows, migrations, or other sensitive
  paths;
- normalized Shannon entropy of churn across changed files; and
- whether the guard policy or temporary-item registry changed.

File growth and sensitive-path changes require an earned-complexity decision.
Line count and change entropy are diagnostics only. A distributed change may
reveal a cross-cutting concern, but a broad rename can be healthy; short or
compressed code can be harder to understand than longer direct code.

Supply language- or architecture-specific results as external checks. The
guard consumes JSON; it never executes commands found in project policy.

## Project policy

`complexity_guard.py init --write` creates only
`.five-step-engineering.json`. It refuses to overwrite an existing policy.
Review its proposed output without `--write` first.

The policy has one current decision. Git history is the audit log, so decision
files do not accumulate:

```json
{
  "schema_version": 1,
  "scope": {
    "include": ["**"],
    "exclude": ["vendor/**", "**/vendor/**", "dist/**", "**/dist/**"],
    "sensitive": [
      ".github/workflows/**",
      "migrations/**",
      "**/migrations/**",
      "pyproject.toml",
      "**/pyproject.toml"
    ]
  },
  "external_hard_checks": ["dependency-cycles"],
  "temporary_items": [],
  "last_decision": null
}
```

Exclude only generated, vendored, or otherwise non-owned material. Changing
scope, exclusions, sensitive paths, external checks, or temporary items is
itself governed. Never weaken policy merely to clear a failure.

An earned decision must match the evaluated base commit and every observed
structural delta exactly:

```json
{
  "id": "consumer-export-contract",
  "base_commit": "FULL_40_CHARACTER_COMMIT",
  "target": "Provide the verified consumer export contract",
  "force": "The named consumer cannot represent the required data otherwise",
  "simplest_rejected_alternative": "The current response omits a required field",
  "observed_deltas": [
    {"id": "tracked_files", "before": 42, "after": 43}
  ],
  "evidence": ["The integration test exercises the consumer contract"],
  "owner": "The export module owns the contract and its lifecycle",
  "lifecycle": "permanent",
  "removal_or_review_condition": "Review when the consumer contract is retired"
}
```

For `temporary` decisions, add an entry with a unique id, owner, affected
paths, ISO review date, removal condition, and originating `decision_id`.
Crossing the review date blocks promotion. Renewal is a new governed decision,
not a silent date edit.

External tools write a separate report:

```json
{
  "schema_version": 1,
  "checks": [
    {
      "id": "dependency-cycles",
      "status": "pass",
      "evidence": "The repository-native architecture check found no cycles"
    }
  ]
}
```

Every id in `external_hard_checks` must be present. Missing or malformed input
is an evaluator error; a reported `fail` is an unresolved gate.

## Run the guard

Set the path to the installed skill once for local use:

```bash
FIVE_STEP_SKILL=/path/to/five-step-engineering

python3 "$FIVE_STEP_SKILL/scripts/complexity_guard.py" \
  inspect --repo . --base origin/main --head HEAD
```

`inspect` reports the transition without blocking on an unresolved decision.
Use its exact `unearned_deltas` when preparing a decision. After the code is
committed, validate and record that decision:

```bash
python3 "$FIVE_STEP_SKILL/scripts/complexity_guard.py" \
  accept --repo . --base origin/main --head HEAD --decision /tmp/decision.json

git add .five-step-engineering.json
git commit -m "Record earned complexity decision"

python3 "$FIVE_STEP_SKILL/scripts/complexity_guard.py" \
  check --repo . --base origin/main --head HEAD
```

The commands return:

- `0`: the invariant is satisfied;
- `2`: a product or evidence discrepancy remains; and
- `3`: the evaluator, configuration, Git baseline, or required input is
  invalid.

The stable JSON report includes observations, unearned deltas, overdue items,
hard-check failures, diagnostics, a failure fingerprint, and the exact rerun
command. Do not compare prose or screen-scrape console output.

## Resolve a failed check

A non-zero result blocks promotion, not development:

1. For exit `3`, repair the evaluator first: verify refs, history depth,
   configuration, declared external inputs, and report schema.
2. For exit `2`, select one unresolved delta that can change the verdict.
3. Apply the five steps recursively. Prefer deleting a new path, merging a
   duplicate truth, or using the direct baseline before writing a decision.
4. If the structure is necessary, provide concrete evidence and a bounded
   lifecycle; never use a pattern name or checked box as evidence.
5. Remove superseded code and temporary investigative structure, then rerun
   the original command.

If the failure fingerprint is unchanged, change code, evidence, observation,
or policy rationale before retrying. Escalate only when the next meaningful
state change needs external facts, authority, or an irreversible trade-off.

## Automation boundary

The guard is a local executable and does not install or mandate CI, remote
actions, branch protection, pull-request templates, secrets, or repository
settings. A project may call it from its own automation, but that integration
belongs to the project and remains outside this skill.

Whatever invokes the guard must preserve the same boundary: provide complete
Git refs and declared external reports, treat evaluator errors as invalid
observations, and never weaken policy merely to manufacture a pass.

## Evidence base

This mechanism combines established results; no source proves that a prompt or
metric makes all future software minimal.

- [Rice](https://doi.org/10.2307/1990888) bounds general semantic decision
  procedures. [Rissanen's minimum-description-length
  work](https://doi.org/10.1016/0005-1098(78)90005-5) motivates accounting for
  both mechanism and exceptions, not minimizing source lines alone.
- [Weyuker](https://doi.org/10.1109/32.6178) and
  [Briand, Morasca, and Basili](https://doi.org/10.1109/32.481535) show why one
  universal complexity number or ungrounded correlation is insufficient.
- Lehman and Ramil frame continuing maintenance as software evolution rather
  than a one-time optimization
  ([2003 synthesis](https://doi.org/10.1016/S0020-0190(03)00382-X)); Eick and
  colleagues found change data can expose decay in a long-lived system
  ([IEEE TSE](https://doi.org/10.1109/32.895984)).
- Harrison applied information entropy as a software-complexity measure
  ([IEEE TSE](https://doi.org/10.1109/32.177371)); Hassan used change-history
  entropy to predict fault potential
  ([ICSE](https://doi.org/10.1109/ICSE.2009.5070510)). These support diagnostic
  use, not entropy as a standalone acceptance rule.
- Lamport's inductive-assertion method grounds preservation of invariants
  ([IEEE TSE](https://doi.org/10.1109/TSE.1977.229904)). Schneider characterizes
  execution-monitor enforcement of safety properties
  ([ACM TISSEC](https://doi.org/10.1145/353323.353382)); translation validation
  checks each produced transformation rather than trusting a translator in the
  abstract ([Pnueli, Siegel, and
  Singerman](https://weizmann.esploro.exlibrisgroup.com/esploro/outputs/conferenceProceeding/Translation-validation/993262143603596)).
- C-Reduce preserves a chosen observable predicate while reducing a test case
  ([Regehr et al.](https://doi.org/10.1145/2254064.2254104)), illustrating both
  the power and the boundary of oracle-driven minimization.
- [SlopCodeBench](https://arxiv.org/abs/2603.24755) is recent, direct evidence
  of structural erosion in iterative coding-agent trajectories. Treat it as an
  evolving preprint, not as the foundation of the invariant.
