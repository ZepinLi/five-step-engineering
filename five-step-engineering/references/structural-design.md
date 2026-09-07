# Structural Design

Use this reference only when the task changes code structure, domain data,
interfaces, or architecture. Apply it inside Five-Step Engineering steps 1–3;
do not turn it into a pattern-first design phase.

## Contents

1. [Minimum-sufficient design](#minimum-sufficient-design)
2. [Earned complexity](#earned-complexity)
3. [Complexity as controlled information](#complexity-as-controlled-information)
4. [Quality scenarios](#quality-scenarios)
5. [Data and state](#data-and-state)
6. [Boundaries and dependencies](#boundaries-and-dependencies)
7. [Robustness and compatibility](#robustness-and-compatibility)
8. [Architecture evidence](#architecture-evidence)
9. [Compact design record](#compact-design-record)
10. [Evidence base](#evidence-base)

## Minimum-sufficient design

A well-designed system uses the minimum independently meaningful concepts
needed to satisfy its real constraints. It keeps important invariants and
ownership explicit, hides volatile decisions behind narrow boundaries,
contains change and failure, and remains explainable.

Structural beauty is coherence, not decoration:

- **Fit:** the structure follows real domain and operational forces rather than
  framework fashion.
- **Integrity:** names, data, control flow, ownership, errors, and boundaries
  tell one consistent story; similar cases look similar and real differences
  stay visible.
- **Local reasoning:** a change or failure can be understood without loading
  the whole system into memory.
- **Economy:** every exposed concept pays for itself in current capability,
  quality, or learning speed.
- **Evidence:** claims such as robust, flexible, or scalable name an observable
  scenario and a check.

Elegance must lower explanation and reasoning cost. It never excuses cleverness
or an extra abstraction.

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
local reasoning rather than an objective beauty metric.

## Earned complexity

Complexity is an immediate and recurring cost. Flexibility is an option whose
benefit arrives only if a relevant change occurs. A seam is worthwhile when it
localizes a credible source of change or failure and its expected value exceeds
its construction and carrying costs; modularity is not free
([Baldwin and Clark](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=312404),
[Sullivan et al.](https://doi.org/10.1145/503209.503224)).

Before adding an interface, layer, factory, strategy, plugin, service, queue,
cache, replica, configuration option, control plane, framework, or other
indirection, record:

1. **Force:** the required semantic, invariant, observed variation, failure,
   scale threshold, or quality scenario it addresses.
2. **Baseline:** the simplest end-to-end design that meets current needs.
3. **Delta:** the concepts, state, dependencies, coordination, deployment,
   failure modes, and operational work the mechanism adds.
4. **Payoff:** what capability, containment, independent evolution, or measured
   system-level outcome the added structure buys.
5. **Evidence:** the test, experiment, incident, change history, or credible
   high-impact scenario supporting the trade.
6. **Lifecycle:** its owner, review trigger, and condition for removal.

If the case is uncertain, buy the cheaper option: a narrow local seam, an
experiment, a migration test, or a recorded decision. Design earlier for
hard-to-reverse public contracts, persisted data, trust boundaries,
consistency and partitioning choices, safety constraints, and destructive
migrations; defer local, observable, reversible choices.

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

## Complexity as controlled information

Treat structural disorder as unexplained degrees of freedom, not as a physical
substance. Thermodynamic entropy supplies a useful warning that unattended
systems tend to lose order, but it does not prove that a repository must grow.
Shannon entropy measures uncertainty in a distribution; for code, it can show
how widely a change is dispersed without saying whether the change is good.
Minimum description length suggests counting both a mechanism and the
exceptions or data needed to make it fit, but the shortest source text is not
necessarily the clearest or safest design
([Rissanen](https://doi.org/10.1016/0005-1098(78)90005-5)).

Use this structural vector instead of one weighted score:

- independently meaningful concepts and responsibilities;
- legal states, transitions, and authoritative sources of truth;
- dependency edges, cycles, and likely change propagation;
- public contracts, configuration dimensions, and compatibility variants;
- exceptional or duplicated paths;
- runtime coordination, failure modes, and operational surfaces; and
- temporary investigative, migration, and rollout structure.

A positive delta is earned only when it names a present force, shows why the
simple baseline fails, supplies relevant evidence, has one lifecycle owner,
and states when it is removed or reviewed. Before closing the parent change,
recompose it: delete superseded implementations, collapse parallel truths,
remove probes and scaffolding, and bound any compatibility path that must
remain. Required complexity may grow; unowned or unexplained complexity may
not.

No computable metric can establish unrestricted semantic minimality. Rice's
theorem rules out deciding every non-trivial semantic program property in
general ([Rice](https://doi.org/10.2307/1990888)). Proposed complexity measures
also encode different assumptions: Weyuker's evaluation shows why no common
measure satisfies every desirable property
([Weyuker](https://doi.org/10.1109/32.6178)), while property-based measurement
requires theoretical justification beyond correlation
([Briand, Morasca, and Basili](https://doi.org/10.1109/32.481535)). Therefore:

- never make LOC, token entropy, cyclomatic complexity, coupling, or churn a
  universal beauty threshold;
- use a signal to locate a concrete design question, then inspect the named
  invariant, boundary, or change scenario;
- let a project-specific hard check enforce only what it can observe reliably;
  and
- require an explicit decision for positive structural transitions rather than
  claiming the checker understands semantic necessity.

Long-lived systems often require deliberate work to preserve or reduce their
complexity as they evolve
([Lehman and Ramil](https://doi.org/10.1016/S0020-0190(03)00382-X)), but studies
and measures differ across systems. For repositories that opt into executable
transition checks, read
[complexity-control.md](complexity-control.md).

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
   fact; identify caches and derived views rather than creating competing truth.
2. State ownership, lifecycle, legal states, and legal transitions.
3. State the invariant that every construction and mutation must preserve.
4. Name the required lookup, update, ordering, uniqueness, and scale properties;
   choose the simplest representation that meets them and measure hot paths.
5. Distinguish absence, unknown, invalid, failed, and not-yet-loaded when those
   meanings change behavior.
6. Prefer a simple representation where invalid combinations cannot be
   constructed; use distinct types or tagged alternatives only when they
   remove a real ambiguity.
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

## Architecture evidence

Create only the view needed for a named audience, concern, or decision. At the
smallest useful scale, show key elements, relationships, external interfaces,
dependency direction, state ownership, and important data or control flow.
Multiple views must use consistent concepts.

For a likely change or failure, list the modules, interfaces, persisted state,
and operations affected. Compare this counterfactual with static dependencies,
tests, and repository co-change history. Treat metrics as diagnostic clues, not
universal thresholds. Useful system-level proxies include explanation and
onboarding time, deployed configuration diversity, dependency cycles, fanout,
retry amplification, blast radius, and restore or rollback effort
([Google SRE](https://sre.google/workbook/simplicity/)).

Compare a scale or performance mechanism with a competent simple baseline and
absolute resource use, not only its scaling curve. The COST study found that
many published data-parallel systems needed hundreds of cores to outperform a
single-threaded implementation, or never did in the reported range
([McSherry et al.](https://www.usenix.org/conference/hotos15/workshop-program/presentation/mcsherry)).

Record an ADR only for a decision with lasting structural, quality, dependency,
interface, data, or operational consequences. Capture context, decision,
alternatives, consequences, confidence, and a review trigger. Architecture
views serve stakeholder concerns under
[ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html); the SEI
[Views and Beyond](https://www.sei.cmu.edu/library/views-and-beyond-collection/)
approach likewise selects only relevant views.

## Compact design record

Scale this down for small changes and expand it only with evidence:

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

## Evidence base

The synthesis also draws on these primary and influential sources:

- Brooks on conceptual integrity in
  [The Mythical Man-Month](https://www.informit.com/content/images/9780201835953/samplepages/0201835959.pdf)
  and essential versus accidental complexity in
  [No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf).
- Dijkstra on simplicity and clarity as engineering necessities in
  [EWD648](https://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD648.html).
- Jackson on preserving the distinction between problem-world obligations and
  machine design in [The World and the Machine](https://doi.org/10.1145/225014.225041).
- Lampson on interfaces that capture the minimum essentials while balancing
  simplicity, completeness, performance, and change in
  [Hints for Computer System Design](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/acrobat-17.pdf).
- Parnas and Clements on keeping design rationale coherent despite an iterative
  process in [A Rational Design Process](https://doi.org/10.1109/TSE.1986.6312940).
- Wirth on separating essential capability from accumulated software bulk in
  [A Plea for Lean Software](https://doi.org/10.1109/2.348001).
- Alexander on fit between a problem's context and the form of its solution in
  [Notes on the Synthesis of Form](https://christopher-alexander-ces-archive.org/book/notes-on-the-synthesis-of-form/).
- Fowler's account of tested simple design and the price of speculative
  flexibility in [Is Design Dead?](https://martinfowler.com/articles/designDead.html)
  and [Beck's design rules](https://martinfowler.com/bliki/BeckDesignRules.html).
- Ousterhout on deep modules, information leakage, and obvious code in
  [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php).
- Saltzer, Reed, and Clark on placing guarantees where the necessary knowledge
  exists in [End-to-End Arguments in System Design](https://web.mit.edu/saltzer/www/publications/endtoend/endtoendA4.pdf).
- Saltzer and Schroeder on economy of mechanism together with fail-safe
  defaults, complete mediation, and least privilege in
  [The Protection of Information in Computer Systems](https://doi.org/10.1109/PROC.1975.9939).
- Yin et al.'s study of 546 real-world configuration errors, which grounds the
  operational cost of unnecessary or weakly governed configuration, in
  [SOSP 2011](https://doi.org/10.1145/2043556.2043572).

These sources disagree on how much flexibility to build early and on the value
of particular patterns. The practical resolution is risk-scaled evidence:
design a seam for an observed source of change, but do not implement speculative
variants; analyze irreversible public, persisted, security, and topology
decisions earlier, while resolving local reversible choices through small
experiments.
