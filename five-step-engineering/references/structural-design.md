# Structural Design

Use this reference only when the task changes code structure, domain data,
interfaces, or architecture. Apply it inside Five-Step Engineering steps 1–3;
do not turn it into a pattern-first design phase.

## Contents

1. [The criterion](#the-criterion)
2. [Quality scenarios](#quality-scenarios)
3. [Data and state](#data-and-state)
4. [Boundaries and dependencies](#boundaries-and-dependencies)
5. [Patterns and abstractions](#patterns-and-abstractions)
6. [Robustness and compatibility](#robustness-and-compatibility)
7. [Architecture evidence](#architecture-evidence)
8. [Compact design record](#compact-design-record)
9. [Evidence base](#evidence-base)

## The criterion

A well-designed system has the minimum concepts needed to express its real
constraints. Its structure fits the problem, keeps important facts and
invariants explicit, hides volatile decisions, contains change and failure,
and stays explainable as a coherent whole.

Treat elegance as an outcome, not a decoration:

- **Fit:** the solution structure follows the current problem and constraints.
- **Integrity:** names, state, ownership, errors, and interfaces tell one
  consistent story.
- **Local reasoning:** a change or failure can be understood without loading
  the whole system into memory.
- **Economy:** every exposed concept pays for itself in current capability,
  quality, or learning speed.
- **Evidence:** claims such as robust, flexible, or scalable name an observable
  scenario and a check.

Fewer lines or classes are not sufficient. Redundancy, isolation, validation,
audit, and compatibility mechanisms are justified when a concrete quality
scenario earns their cost. Do not erase essential domain complexity; remove
accidental complexity around it.

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
coupling. Parnas grounds the information-hiding rule in
[decomposition criteria](https://doi.org/10.1145/361598.361623) and
[extension and contraction](https://doi.org/10.1109/TSE.1979.234169);
Garlan and colleagues show how reusable components can still create
[architectural mismatch](https://www.cs.cmu.edu/afs/cs/project/able/ftp/archmismatch-icse17/archmismatch-icse17.pdf).

## Patterns and abstractions

Treat a design pattern as a contextual hypothesis. Before introducing an
interface, layer, factory, strategy, plugin, service, event bus, framework, or
other indirection, record:

1. **Force:** the observed variation, repetition, coupling, failure, or quality
   scenario it addresses.
2. **Baseline:** the simplest direct design that meets current requirements.
3. **Delta:** the concepts, dependencies, runtime paths, and operational burden
   the abstraction adds.
4. **Benefit:** the evidence that the added structure improves the whole system.
5. **Fit:** whether the language, platform, existing component, and team already
   provide or understand the needed form.
6. **Exit:** the signal under which the abstraction should be removed.

Introduce only the pattern kernel required now. Grow toward a fuller pattern
through tested, behavior-preserving refactoring. A familiar pattern can be
cheaper than an original mechanism, but its name is not evidence. The original
[GoF catalog](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480/9780321700698)
describes recurring contextual solutions and their consequences; Gamma advises
[starting from concrete design pain](https://www.artima.com/articles/how-to-use-design-patterns),
while Norvig demonstrates that language features can
[absorb or simplify patterns](https://www.norvig.com/design-patterns/).

## Robustness and compatibility

At each consequential boundary, make the contract explicit: accepted input,
successful output, recoverable errors, side effects, ordering, atomicity,
idempotency, timeout, cancellation, and partial progress as applicable.

- Reject or deliberately normalize malformed and ambiguous input; do not let
  tolerance create an accidental protocol.
- Put the end-to-end guarantee at the layer with enough knowledge to verify it.
- Bound queues, retries, work, and resource use where overload is credible.
- Retry only an idempotent, retriable operation; use a budget, backoff, jitter,
  and one responsible layer.
- Keep source, wire, and semantic compatibility distinct for public APIs and
  persisted schemas. Test the cross-version combinations that can coexist.
- Keep failure paths observable and test them; rarely used recovery logic is
  still production logic.

Robustness does not mean accepting every input or implementing every failure
mechanism. [RFC 9413](https://www.rfc-editor.org/rfc/rfc9413.html) explains the
long-term cost of ambiguous tolerance; the
[Google SRE guidance](https://sre.google/sre-book/addressing-cascading-failures/)
shows why retries, graceful degradation, and overload controls must be bounded
and tested.

## Architecture evidence

Create only the view needed for a named audience, concern, or decision. At the
smallest useful scale, show key elements, relationships, external interfaces,
dependency direction, state ownership, and important data or control flow.
Multiple views must use consistent concepts.

For a likely change or failure, list the modules, interfaces, persisted state,
and operations affected. Compare this counterfactual with static dependencies,
tests, and repository co-change history. Treat metrics as diagnostic clues, not
universal thresholds.

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
Data, ownership, invariants, transitions:
Boundaries and dependency direction:
Failure and compatibility behavior:
Simplest direct design:
Chosen structure and earned trade-offs:
Checks, rollback, and review trigger:
```

## Evidence base

The synthesis also draws on:

- Brooks's distinction between essential and accidental complexity in
  [No Silver Bullet](https://www.cs.unc.edu/techreports/86-020.pdf).
- Dijkstra on simplicity and clarity as engineering necessities in
  [EWD648](https://www.cs.utexas.edu/~EWD/transcriptions/EWD06xx/EWD648.html).
- Alexander on fit between a problem's context and the form of its solution in
  [Notes on the Synthesis of Form](https://christopher-alexander-ces-archive.org/book/notes-on-the-synthesis-of-form/).
- Fowler's account of tested simple design and the price of speculative
  flexibility in [Is Design Dead?](https://martinfowler.com/articles/designDead.html)
  and [Beck's design rules](https://martinfowler.com/bliki/BeckDesignRules.html).
- Ousterhout on deep modules, information leakage, and obvious code in
  [A Philosophy of Software Design](https://web.stanford.edu/~ouster/cgi-bin/aposd.php).
- Saltzer, Reed, and Clark on placing guarantees where the necessary knowledge
  exists in [End-to-End Arguments in System Design](https://web.mit.edu/saltzer/www/publications/endtoend/endtoendA4.pdf).

These sources disagree on how much flexibility to build early and on the value
of particular patterns. The practical resolution is risk-scaled evidence:
design a seam for an observed source of change, but do not implement speculative
variants; analyze irreversible public, persisted, security, and topology
decisions earlier, while resolving local reversible choices through small
experiments.
