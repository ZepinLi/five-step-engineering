# Five-Step Engineering

An evidence-first Agent Skill for Codex, Claude Code, and Cursor. It now applies
the same first-principles discipline to data models, design patterns, and
software architecture: model valid state first, hide volatile decisions, and
make every abstraction earn its concepts.

> **Do not optimize something that has not earned the right to exist.**

## Architecture

```mermaid
flowchart TB
    I["Proposed system or change"]
    subgraph P["Ordered evidence gates"]
        direction LR
        Q["1 · Question<br/>requirements"] -->|"pass"| D["2 · Delete"]
        D -->|"pass"| S["3 · Simplify<br/>data · boundaries · patterns"]
        S -->|"pass"| C["4 · Accelerate<br/>feedback"]
        C -->|"pass"| A["5 · Automate"]
    end
    I --> Q
    A --> O["Minimum sufficient system"]
    O --> R["Target · Evidence · Decision · Next"]
    Q -. "not resolved · hold" .-> H
    D -. "not resolved · hold" .-> H
    S -. "not resolved · hold" .-> H
    C -. "not resolved · hold" .-> H
    A -. "not resolved · hold" .-> H
    subgraph L["Recursive gate recovery"]
        direction LR
        H["Name discrepancy"] --> B["Shrink to one blocker"]
        B --> F["Run five steps"]
        F --> E["Act · observe · update"]
        E --> G["Re-evaluate owning gate"]
        G -->|"still open · new evidence"| H
    end
    G -->|"resolved"| V["Resume parent sequence"]

    classDef input fill:#f6f8fa,stroke:#57606a,color:#24292f;
    classDef gate fill:#0d1117,stroke:#58a6ff,color:#f0f6fc;
    classDef result fill:#dafbe1,stroke:#1a7f37,color:#116329;
    class I,H,B,F,E,G,V input;
    class Q,D,S,C,A gate;
    class O,R result;
    style P fill:#ffffff,stroke:#d0d7de,color:#24292f;
    style L fill:#f6f8fa,stroke:#afb8c1,color:#24292f;
```

Advance only when the current evidence gate is resolved. A failed gate holds
stage progression—not problem solving—while the smallest blocker is resolved
recursively and returned to its parent gate.

## Origins

The process comes from Elon Musk's explanation during Tim Dodd's
[2021 Starbase tour interview](https://www.youtube.com/watch?v=t705r8ICkRw),
later popularized as
[“The Algorithm”](https://www.inc.com/jeff-haden/elon-musks-algorithm-a-5-step-process-to-dramatically-improve-nearly-everything-is-both-simple-brilliant.html)
in Walter Isaacson's *Elon Musk*.
This skill adds explicit evidence gates, reversibility safeguards, and a
[closed-loop recovery protocol](five-step-engineering/references/closed-loop-engineering.md)
informed by risk-driven iteration, feedback control, recursive problem solving,
and evidence on agent self-correction.
Its [structural-design reference](five-step-engineering/references/structural-design.md)
distills primary work on data invariants, information hiding, quality scenarios,
and problem-first use of patterns.

## Install

Clone once:

```bash
git clone https://github.com/ZepinLi/five-step-engineering.git
cd five-step-engineering
```

Link the same skill into any client you use:

```bash
# Codex
mkdir -p ~/.codex/skills
ln -s "$PWD/five-step-engineering" ~/.codex/skills/five-step-engineering

# Claude Code
mkdir -p ~/.claude/skills
ln -s "$PWD/five-step-engineering" ~/.claude/skills/five-step-engineering

# Cursor
mkdir -p ~/.cursor/skills
ln -s "$PWD/five-step-engineering" ~/.cursor/skills/five-step-engineering
```

Restart the client or open a new agent session if the skill is not discovered
immediately. Cursor users can alternatively
[import the GitHub repository](https://cursor.com/docs/skills.md#installing-skills-from-github)
from **Customize → Rules → Add Rule → Remote Rule (GitHub)**.

## Use

| Client | Direct invocation |
| --- | --- |
| Codex | `$five-step-engineering evaluate whether we should add a cache.` |
| Claude Code | `/five-step-engineering evaluate whether we should add a cache.` |
| Cursor | `/five-step-engineering evaluate whether we should add a cache.` |

Codex uses explicit invocation. Claude Code and Cursor may also discover the
skill automatically from its description. It reports target, evidence,
decision, and next action; for action requests it keeps resolving safe,
in-scope blockers instead of stopping at the first failed gate.

## Structure

```text
five-step-engineering/
├── README.md
├── LICENSE
└── five-step-engineering/
    ├── SKILL.md
    ├── references/
    │   ├── closed-loop-engineering.md
    │   └── structural-design.md
    └── agents/
        └── openai.yaml
```

The inner `five-step-engineering/` directory is the self-contained skill.

## License

[MIT](LICENSE)
