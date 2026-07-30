# Five-Step Engineering

An evidence-first Codex skill for improving systems in the right order.

> **Do not optimize something that has not earned the right to exist.**

## Architecture

```mermaid
flowchart TB
    I["Proposed system or change"]
    subgraph P["Ordered evidence gates"]
        direction LR
        Q["1 · Question<br/>requirements"] -->|"pass"| D["2 · Delete"]
        D -->|"pass"| S["3 · Simplify<br/>and optimize"]
        S -->|"pass"| C["4 · Accelerate<br/>feedback"]
        C -->|"pass"| A["5 · Automate"]
    end
    I --> Q
    A --> O["Minimum sufficient system"]
    O --> R["Target · Evidence · Decision · Next"]
    U["Unknown or invalid<br/>assumption"] -. "investigate or restart" .-> Q

    classDef input fill:#f6f8fa,stroke:#57606a,color:#24292f;
    classDef gate fill:#0d1117,stroke:#58a6ff,color:#f0f6fc;
    classDef result fill:#dafbe1,stroke:#1a7f37,color:#116329;
    class I,U input;
    class Q,D,S,C,A gate;
    class O,R result;
    style P fill:#ffffff,stroke:#d0d7de,color:#24292f;
```

Advance only when the current evidence gate passes. Stop at the first
consequential unknown; if an assumption breaks, restart at step 1.

## Origins

The process comes from Elon Musk's explanation during Tim Dodd's
[2021 Starbase tour interview](https://www.youtube.com/watch?v=t705r8ICkRw),
later popularized as
[“The Algorithm”](https://www.inc.com/jeff-haden/elon-musks-algorithm-a-5-step-process-to-dramatically-improve-nearly-everything-is-both-simple-brilliant.html)
in Walter Isaacson's *Elon Musk*.
This skill adds explicit evidence gates, reversibility safeguards, and a
decision-focused output for agentic engineering work.

## Install

```bash
git clone https://github.com/ZepinLi/five-step-engineering.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/five-step-engineering/five-step-engineering" \
  ~/.codex/skills/five-step-engineering
```

Restart Codex after installation.

## Use

```text
Use $five-step-engineering to evaluate whether we should add a cache to this service.
```

The skill uses explicit invocation and returns only the target, evidence,
decision, and smallest useful next step.

## Structure

```text
five-step-engineering/
├── README.md
├── LICENSE
└── five-step-engineering/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

The inner `five-step-engineering/` directory is the self-contained skill.

## License

[MIT](LICENSE)
