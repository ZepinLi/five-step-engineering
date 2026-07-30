# Five-Step Engineering

An evidence-first Codex skill for redesigning or optimizing systems, codebases,
pipelines, products, and workflows in the right order:

> Question requirements → Delete → Simplify and optimize → Accelerate feedback → Automate

The central rule is simple: **do not optimize something that has not earned the
right to exist.**

## What it does

The skill turns the five-step engineering process into an ordered decision
protocol. It helps Codex:

- distinguish hard constraints from proposed solutions;
- challenge requirements with owners, artifacts, tests, and measurements;
- look for safe deletion before adding or optimizing;
- stop at the first unresolved evidence gate;
- protect compatibility, safety, privacy, and data integrity;
- automate only work proven necessary, stable, repetitive, and understood.

The skill is configured for explicit invocation so it does not silently steer
unrelated tasks.

## Install

Clone the repository and copy or link the skill directory into your Codex
skills directory:

```bash
git clone https://github.com/ZepinLi/five-step-engineering.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/five-step-engineering/five-step-engineering" \
  ~/.codex/skills/five-step-engineering
```

Restart Codex after installation.

## Use

Invoke the skill explicitly:

```text
Use $five-step-engineering to evaluate whether we should add a cache to this service.
```

The response focuses on four things: the target, the evidence, the decision,
and the smallest useful next step.

## Repository layout

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

## 中文简介

这是一个面向 Codex 的“五步工程法”技能。它要求严格按以下顺序处理系统、代码、
流程或产品的改造问题：

> 质疑需求 → 删除 → 简化与优化 → 加速反馈 → 最后自动化

它强调以证据通过每一道决策门槛，并在首个未解决的不确定性处停止，避免过早优化、
盲目自动化或把复杂度转嫁给用户和下游系统。

## License

[MIT](LICENSE)
