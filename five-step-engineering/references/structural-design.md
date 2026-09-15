# Structural Design

Use this reference only when the task changes code structure, domain data,
interfaces, or architecture. Read it before structural design and apply it
through implementation and verification within the five steps; do not turn it
into a separate design or governance process.

## Contents

1. [Minimum-sufficient design](#minimum-sufficient-design)
2. [Earned complexity](#earned-complexity)
3. [Entropy and measurement](#entropy-and-measurement)
4. [Structural invariants and their limits](#structural-invariants-and-their-limits)
5. [Quality scenarios](#quality-scenarios)
6. [Data and state](#data-and-state)
7. [Boundaries and dependencies](#boundaries-and-dependencies)
8. [Robustness and compatibility](#robustness-and-compatibility)
9. [Development and retirement](#development-and-retirement)
10. [Architecture evidence](#architecture-evidence)
11. [Compact design record](#compact-design-record)

## Minimum-sufficient design

A well-designed system uses the minimum independently meaningful concepts
needed to satisfy its real constraints. It keeps important invariants and
ownership explicit, hides volatile decisions behind narrow boundaries,
contains change and failure, and remains explainable.

Structural beauty is coherence, not decoration:

- **Fit:** the structure follows real domain and operational forces rather than
  framework fashion, echoing Alexander's
  [context–form relationship](https://christopher-alexander-ces-archive.org/book/notes-on-the-synthesis-of-form/).
- **Integrity:** names, data, control flow, ownership, errors, and boundaries
  tell one consistent story; similar cases look similar and real differences
  stay visible.
- **Local reasoning:** a change or failure can be understood without loading
  the whole system into memory.
- **Economy:** every exposed concept pays for itself in current capability,
  quality, or learning speed.
- **Evidence:** claims such as robust, flexible, or scalable name an observable
  scenario and a check.

Treat clarity as an engineering constraint
([Dijkstra](https://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD648.html)).
Elegance must lower reasoning cost, never excuse cleverness or an extra abstraction.

Minimum-sufficient does not mean the fewest lines, modules, services, or
features. Distinguish three states:

- **Under-designed:** required states, invariants, ownership, failure behavior,
  or irreversible risks are implicit or uncovered.
- **Minimum-sufficient:** removing a remaining concept loses a required
  capability, breaks a quality scenario, exposes a volatile decision, or
  creates unacceptable coupling.
- **Over-designed:** a mechanism has no present responsibility and no credible,
  evidence-backed option value; its indirection, state, coordination, or
  operating cost exceeds the problem it removes.

Do not erase essential domain complexity to make a diagram small. Remove
accidental complexity around it, and add redundancy, isolation, validation,
audit, or compatibility only when a concrete scenario earns the cost. This is
a synthesis of problem fidelity, conceptual integrity, information hiding, and
local reasoning. Brooks distinguishes essential and accidental complexity in
[No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf); his
[conceptual-integrity argument](https://www.informit.com/content/images/9780201835953/samplepages/0201835959.pdf)
also motivates making the design tell one coherent story.

## Earned complexity

Complexity is an immediate and recurring cost. Flexibility is an option whose
benefit arrives only if a relevant change occurs. A seam is worthwhile when it
localizes a credible source of change or failure and its expected value exceeds
its construction and carrying costs; modularity is not free
([Baldwin and Clark](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=312404),
[Sullivan et al.](https://doi.org/10.1145/503209.503224)).

Before adding an abstraction, state, dependency, configuration option, or
defensive mechanism, answer:

1. What current behavior, quality scenario, or observed maintenance problem
   requires it?
2. Why is directly changing the existing implementation insufficient? Check
   what the language, platform, or existing module already provides.
3. What concepts, coordination, failure handling, and operating costs does it
   add and remove? Which test, measurement, or architectural fact supports that
   trade?

An explanation is a claim to examine, not proof of necessity. A small change
needs no form or file. For lasting decisions, use the project's existing record
and identify the owner and removal or review condition. Do not impose a
one-in/one-out rule: a necessary boundary may increase code while reducing
reasoning cost across the system.

If the case is uncertain, buy the cheaper option: a narrow local seam, an
experiment, a migration test, or a recorded decision. Design earlier for
hard-to-reverse public contracts, persisted data, trust boundaries,
consistency and partitioning choices, safety constraints, and destructive
migrations; defer local, observable, reversible choices. Fowler's
[YAGNI](https://martinfowler.com/bliki/Yagni.html) defers speculative capability
while explicitly supporting refactoring that keeps present code easy to change.

Treat these as over-design signals, not automatic verdicts:

- a pass-through layer, generic envelope, extension point, or configuration
  option with no current user or independently varying responsibility;
- a distributed boundary with no demonstrated need for independent ownership,
  deployment, scaling, security, or fault containment;
- coordination without a named invariant, or redundancy without an independent
  fault domain;
- duplicated retries, validation, caches, or sources of truth whose interaction
  is harder to reason about than the original problem;
- local simplicity that exports ambiguity, global reasoning, or operational
  burden to callers and operators.

Correct over-design by deleting, merging, narrowing, or localizing the
mechanism, then re-run the five steps against the owning requirement. Preserve
only the smallest seam that keeps a valuable choice open. A pattern name is not
evidence; the original [GoF catalog](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780321700698)
describes contextual forces and consequences, and Gamma advises
[starting from concrete design pain](https://www.artima.com/articles/how-to-use-design-patterns).

Judge the whole system rather than its box count. An added component can reduce
net complexity when it centralizes a hard responsibility behind a narrow
contract: Chubby added a coarse-grained lock service so every client did not
have to implement consensus independently
([Burrows](https://www.usenix.org/conference/osdi-06/presentation/chubby-lock-service-loosely-coupled-distributed-systems)).
Within its model, the I-confluence result makes the coordination test precise:
coordinate when independently valid operations could combine to violate a
named invariant, not merely because distribution feels risky
([Bailis et al.](https://doi.org/10.14778/2735508.2735509)).

## Entropy and measurement

Keep three ideas distinct:

- **Thermodynamic entropy:** a physical concept. Applying its name to software
  disorder is a metaphor, not a law proving inevitable code growth.
- **Shannon entropy:** uncertainty in a specified probability distribution
  ([Shannon, 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)).
  Change dispersion can be defined this way; it does not reveal whether the
  change is necessary. Hassan's study found predictive value for change
  complexity in six projects, while noting that refactoring can also increase
  dispersion ([ICSE 2009](https://sail.cs.queensu.ca/data/pdfs/ICSE2009_PredictingFaultsUsingTheComplexityOfCodeChanges.pdf)).
- **Minimum description length:** model selection by description cost
  ([Rissanen, 1978](https://research.ibm.com/publications/modeling-by-shortest-data-description)).
  The design analogy is to consider a mechanism together with its interfaces,
  configuration, exceptions, and caller obligations. Compressing source text
  does not establish a better design.

Review concepts, state and truth sources, dependencies, interfaces and
configuration, exceptional paths, operational failure surfaces, and temporary
structure separately. A useful simplification removes an invalid state
combination, duplicate truth, implicit dependency, needless exception, or
obsolete path. It needs no universal entropy score.

Weyuker found that none of four evaluated syntactic complexity measures met all
nine proposed properties ([1988](https://doi.org/10.1109/32.6178)). Briand,
Morasca, and Basili require measures to have theoretically justified properties
([1996](https://www.cs.umd.edu/~basili/publications/journals/J58.pdf)). These
results motivate explicit measurement assumptions, not rejection of every
metric. Use existing metrics to locate a design question; verify the relevant
state, boundary, or failure scenario. Never pursue low counts by compressing
code, hiding coupling, or concentrating unrelated work in a large function.

## Structural invariants and their limits

For explicit requirements and scope `R`, define concrete properties `I_R` of
the design: legal states and transitions, authoritative data sources, or
allowed dependency directions. The proof framework is:

```text
I_R holds initially
and every accepted transformation preserves I_R
=> I_R holds after every accepted transformation
```

This follows the invariant discipline of
[Dijkstra, 1975](https://www.cs.utexas.edu/~EWD/transcriptions/EWD04xx/EWD472.html)
and [Lamport, 1977](https://www.microsoft.com/en-us/research/?p=338279).
The implication requires a precise model, a valid initial state, and proof of
preservation. Tests and natural-language review usually provide evidence rather
than that proof. A written explanation cannot define its own claim as true.

- Establish the relevant initial properties. If existing code violates them,
  resolve the affected scope; do not assume the whole repository is sound.
- Check changes at the operations and boundaries that can violate the property.
  Explicit representations and controlled mutation can exclude particular
  failure classes within their stated assumptions.
- Revisit assumptions when requirements or the environment change. Do not
  redefine a property merely to conceal a violation.
- Separate exploratory intermediate states from retained implementations.
  Preserve safety and data integrity throughout; resolve unfinished structural
  work before declaring completion.

[Rice, 1953](https://www.ams.org/journals/tran/1953-074-02/S0002-9947-1953-0053041-6/S0002-9947-1953-0053041-6.pdf)
limits general decision procedures for nontrivial semantic program properties.
It does not rule out useful syntactic checks or proofs in restricted models.
Neither that theorem nor an invariant argument turns "never over-designed"
into a proven property of an arbitrary codebase. State exactly which property
was established, for which scope, and by what evidence.

## Quality scenarios

Replace a quality adjective with:

`stimulus + environment + affected artifact + response + measurable bound`

Example: replace "the worker must be robust" with "if a dependency times out
during peak load, the worker releases the lease, makes no duplicate mutation,
and reports a retryable error within 2 seconds."

Prioritize the one to three scenarios that can change the design. For each
mechanism, state which scenario it improves, what it makes worse, and how the
claim will be checked. This follows the scenario and trade-off discipline in
the [SEI quality-attribute work](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/)
and [ATAM](https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/).

## Data and state

Start with the information model, not classes or endpoints:

1. Name the domain values, identities, units, and authoritative owner for each
   fact; give caches and derived views explicit update or invalidation rules.
2. State ownership, lifecycle, legal states, and legal transitions.
3. State the invariant that every construction and mutation must preserve.
4. Name the required lookup, update, ordering, uniqueness, and scale properties;
   choose the simplest representation that meets them and measure hot paths.
5. Distinguish absence, unknown, invalid, failed, and not-yet-loaded when those
   meanings change behavior.
6. Prefer a simple representation where invalid combinations cannot be
   constructed. Three mutually exclusive states, for example, need one state
   value rather than three independent booleans with eight possible
   combinations. Use distinct types or tagged alternatives for real ambiguity.
7. Keep representation private. Do not leak mutable internal state or make
   callers reproduce validation rules.
8. Validate untrusted data once at the trust boundary, then convert it to a
   valid internal value. Types complement rather than replace boundary checks.

Formal abstraction functions are unnecessary for trivial transfer objects.
Use the discipline where invariants, mutation, persistence, concurrency, or a
public contract make representation errors consequential. The foundations are
[Liskov and Zilles on abstract data types](https://doi.org/10.1145/800233.807045),
[Hoare on representation correctness](https://ora.ox.ac.uk/objects/uuid%3A496c86ab-dbfd-4901-b2dd-e94fc4f42e51),
and [Meyer on explicit contracts](https://se.inf.ethz.ch/~meyer/publications/computer/contract.pdf).

## Boundaries and dependencies

For each non-trivial module, answer:

- What coherent responsibility does it own?
- What difficult or volatile design decision does it hide?
- What is the smallest interface that gives callers the required capability?
- Which data, control, and failure semantics cross the boundary?
- What concrete change would stay inside it?

Investigate a module that only forwards calls, renames values, exposes control
flags, passes a broad record for a few fields, or shares mutable state. Merge or
delete it unless it hides meaningful complexity. Prefer intentional,
directional dependencies; explain or remove architecture-level cycles.

Static imports are not the whole architecture. Protocol, data ownership,
lifecycle, deployment, and repeated cross-boundary co-change can reveal hidden
coupling. A runtime boundary must also justify its lifecycle surface: separate
deployment, versioning, security, observability, capacity, recovery, and
on-call ownership. Prefer an in-process module when those costs buy no real
autonomy, scale, or containment.

Lampson's [interface guidance](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/acrobat-17.pdf)
balances minimum essentials with completeness, performance, and change.
Share code when it expresses the same knowledge and should change for the same
reason. Similar syntax alone does not justify a common abstraction across
independent responsibilities. Ousterhout's
[deep-module guidance](https://web.stanford.edu/~ouster/cgi-bin/aposd.php)
likewise favors interfaces that hide substantial implementation complexity.

Parnas grounds the information-hiding rule in
[decomposition criteria](https://doi.org/10.1145/361598.361623) and
[extension and contraction](https://doi.org/10.1109/TSE.1979.234169);
Garlan and colleagues show how reusable components can still create
[architectural mismatch](https://www.cs.cmu.edu/afs/cs/project/able/ftp/archmismatch-icse17/archmismatch-icse17.pdf).

## Robustness and compatibility

At each consequential boundary, make the contract explicit: accepted input,
successful output, recoverable errors, side effects, ordering, atomicity,
idempotency, timeout, cancellation, and partial progress as applicable.

- Reject or deliberately normalize malformed and ambiguous input; do not let
  tolerance create an accidental protocol.
- Put the end-to-end guarantee at the layer with enough knowledge to verify it.
- State the fault model and user-facing objective before adding replication,
  failover, consensus, fallback, or recovery machinery; test the protection
  mechanism and the independence of its fault domains
  ([Avižienis et al.](https://doi.org/10.1109/TDSC.2004.2)).
- Bound queues, retries, work, and resource use where overload is credible.
- Retry only an idempotent, retriable operation; use a budget, backoff, jitter,
  and one responsible layer.
- Keep source, wire, and semantic compatibility distinct for public APIs and
  persisted schemas. Test the cross-version combinations that can coexist.
- Keep failure paths observable and test them; rarely used recovery logic is
  still production logic.

Before adding validation, hashing, retry, or fallback, name the boundary,
failure, or security requirement it protects. Keep necessary input and
authorization checks. Avoid repeatedly checking established internal facts or
silently recovering from an invalid model. A later change of trust, mutation,
or permissions may require checking again; explain that concrete reason.

For ordinary local state, prefer direct comparison or existing project
capabilities. Use SHA-256 or other cryptographic mechanisms only for an actual
integrity, security, or content-addressing requirement. Complexity review and
remembering failed attempts do not need cryptographic identities.

This applies [Saltzer and Schroeder's economy of mechanism](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html)
alongside their other protection principles. The
[end-to-end argument](https://web.mit.edu/saltzer/www/publications/endtoend/endtoendA4.pdf)
also asks which layer has enough knowledge to provide the intended guarantee;
it does not prohibit lower-layer checks that serve a demonstrated purpose.

Robustness does not mean accepting every input or implementing every failure
mechanism. Remote calls cannot hide latency, concurrency, and partial failure
behind local-call semantics
([Waldo et al.](https://scholar.harvard.edu/files/waldo/files/waldo-94.pdf)).
[RFC 9413](https://www.rfc-editor.org/rfc/rfc9413.html) explains the long-term
cost of ambiguous tolerance; the
[Google SRE guidance](https://sre.google/sre-book/addressing-cascading-failures/)
shows why retries, graceful degradation, and overload controls must be bounded
and tested. An OSDI study of 198 production failures found that most
catastrophic cases could have been prevented through simple testing of error
handling, a reminder to exercise the smallest credible failure schedules
before adding elaborate recovery machinery
([Yuan et al.](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/yuan)).

## Development and retirement

Apply these decisions within the five steps, using the current code and the
project's existing tests, analysis, and review tools:

1. Before adding a mechanism, evaluate the direct solution and the force that
   makes it insufficient.
2. After a meaningful implementation step, inspect what was added, moved, or
   retired against the original outcome. Include affected callers, state,
   configuration, and dependencies; a small diff can leave a large design debt.
3. Follow related modules until the behavior and ownership are coherent. Fix
   the cause at its responsible boundary before adding another local patch.
   Stop expanding once this problem is resolved; unrelated cleanup and explicit
   user scope limits still matter.
4. When replacing code, update consumers and remove superseded branches,
   duplicate truth, obsolete flags, and exploratory artifacts. For necessary
   coexistence, identify actual consumers, the owner, and the retirement
   condition through the project's existing practice. Do not erase required
   compatibility to satisfy a cleanup target.
5. Run relevant behavior and regression checks, then inspect the retained
   structure. A failed check or unresolved design question returns to
   [closed-loop resolution](closed-loop-engineering.md); success requires both
   verified behavior and completed structural work.

Lehman and Ramil's account of E-type software evolution describes increasing
complexity unless deliberate work maintains or reduces it
([2003](https://doi.org/10.1016/S0020-0190(03)00382-X)). This is empirical
evolution research, not a thermodynamic theorem. It supports making
simplification part of development rather than postponing it indefinitely.
Wirth's [A Plea for Lean Software](https://doi.org/10.1109/2.348001) similarly
distinguishes essential capability from accumulated software bulk.

[SlopCodeBench, 2026, section 4.3](https://arxiv.org/html/2603.24755v1#S4.SS3)
reports that quality-focused prompts improved starting quality without
significantly changing degradation slopes in its prompt-intervention study.
Treat this recent preprint as bounded evidence about those evaluated models,
tasks, and measures. These skill rules are an engineering proposal to evaluate
through repeated use, not a demonstrated cure for long-term agent degradation.

## Architecture evidence

Create only the view needed for a named audience, concern, or decision. At the
smallest useful scale, show key elements, relationships, external interfaces,
dependency direction, state ownership, and important data or control flow.
Multiple views must use consistent concepts.

Check the view against actual callers, state ownership, and dependencies.
[Software Reflexion Models](https://www.cs.ubc.ca/~murphy/papers/rm/fse95.html)
compares an intended high-level model with an implementation mapping: a box
diagram or directory inventory alone cannot establish conformance.

For a likely change or failure, list the modules, interfaces, persisted state,
and operations affected. Compare this counterfactual with static dependencies,
tests, and repository co-change history. Treat metrics as diagnostic clues, not
universal thresholds. Useful system-level proxies include explanation and
onboarding time, deployed configuration diversity, dependency cycles, fanout,
retry amplification, blast radius, and restore or rollback effort
([Google SRE](https://sre.google/workbook/simplicity/)).
Yin et al.'s [study of 546 configuration errors](https://doi.org/10.1145/2043556.2043572)
also motivates examining configuration's operational cost, not just its size.

Compare a scale or performance mechanism with a competent simple baseline and
absolute resource use, not only its scaling curve. The COST study found that
many published data-parallel systems needed hundreds of cores to outperform a
single-threaded implementation, or never did in the reported range
([McSherry et al.](https://www.usenix.org/conference/hotos15/workshop-program/presentation/mcsherry)).

Record an ADR only for a decision with lasting structural, quality, dependency,
interface, data, or operational consequences. Capture context, decision,
alternatives, consequences, confidence, and a review trigger; keep rationale
coherent as implementation evolves
([Parnas and Clements](https://doi.org/10.1109/TSE.1986.6312940)).
Architecture views serve stakeholder concerns under
[ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html); the SEI
[Views and Beyond](https://www.sei.cmu.edu/library/views-and-beyond-collection/)
approach likewise selects only relevant views.

## Compact design record

For a lasting decision, use the project's existing record. These prompts may
help; small changes need no fixed template or new file:

```text
Outcome and quality scenarios:
Essential constraints and accepted risks:
Data, ownership, invariants, transitions:
Boundaries and dependency direction:
Failure and compatibility behavior:
Simplest useful end-to-end baseline:
Chosen mechanisms, carrying cost, owner, and exit:
Checks, rollback, and review trigger:
```
