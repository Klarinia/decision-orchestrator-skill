# Decision Orchestrator Skill

English | [简体中文](./README.zh-CN.md)

A production-oriented skill that runs a full **Router -> Advisors -> CEO Final** decision workflow in one command.

Designed for:
- Codex workflows
- Claude Code workflows
- OpenClaw pipeline handoff

## 1. Why This Skill

Manual multi-prompt orchestration is slow and inconsistent. This skill turns it into a deterministic run package:

- Standardized structure
- Traceable decision artifacts
- Faster execution from idea to action
- OpenClaw-compatible payload output

## 2. Workflow Architecture

```text
Input JSON
   |
   v
Router (classify + route)
   |
   v
Advisor Chain (domain-specific analysis)
   |
   v
CEO Final (conflict merge + final decision + action plan)
   |
   v
Run Artifacts + OpenClaw Payload
```

### Routing Logic (default)

- Growth Strategy: `Drucker -> Buffett -> Musk`
- Product/Experience: `Jobs -> KenyaHara -> Musk`
- High-Impact Decision: `Munger -> Drucker -> Buffett -> Musk`
- Execution-Stuck: `Musk`

## 3. Advisor/Prompt Responsibilities

### Router Prompt / 路由器
- Goal: classify case type, route advisors, identify data gaps.
- Output: category/confidence/route/handoff notes.
- Constraint: no final business decision.

### Drucker / 德鲁克 (Value Definition)
- Focus: customer identity and value clarity.
- Checks: customer-fit, value proposition, evidence quality.
- Hard stop: no clear customer value.

### Jobs / 乔布斯 (Experience Quality)
- Focus: user flow clarity and decision friction.
- Checks: flow coherence, message clarity, content reduction.
- Hard stop: user cannot understand value quickly.

### Kenya Hara / 原研哉 (System Simplicity)
- Focus: structural necessity and cognitive load.
- Checks: remove/merge/rename for minimal complexity.
- Hard stop: complexity increases without clarity gain.

### Munger / 芒格 (Multi-Model Decision)
- Focus: cross-model risk decomposition.
- Checks: economics + psychology + probability consistency.
- Hard stop: key assumptions untestable or tail risk unmanaged.

### Buffett / 巴菲特 (Moat and Focus)
- Focus: strategic moat reinforcement.
- Checks: moat gain, imitation risk, opportunity cost.
- Hard stop: clear strategic drift from core positioning.

### Musk / 马斯克 (Execution Velocity)
- Focus: move from analysis to immediate execution.
- Checks: 48-hour launchable action plan, measurable criteria.
- Hard stop: no owner or no measurable deliverable.

### CEO Final Prompt / 最终拍板层
- Goal: merge conflicting advisor outputs and finalize decision.
- Output: final decision, tradeoffs, 48h/7d actions, kill criteria.
- Constraint: explicit accountability and review date.

## 4. Run Artifacts

Each run folder includes:

- `01-decision-input.md`
- `02-router-output.yaml`
- `03-agent-outputs.yaml`
- `04-ceo-final.yaml`
- `05-decision-log.md`
- `06-review-summary.md`
- `07-one-shot-prompt.md`
- `openclaw-payload.json`

## 5. Quick Start

```bash
python3 scripts/run_multi_advisor.py \
  --input references/openclaw-input.example.json \
  --runs-root ./runs \
  --owner "Decision Owner"
```

## 6. OpenClaw Integration

Use the same input schema as `references/openclaw-input.example.json`.

Output `openclaw-payload.json` can be passed directly to downstream nodes for:
- artifact indexing
- post-processing
- notification/reporting

## 7. UI Profile Config (Not GitHub Account Identity)

This section controls only **skill UI display metadata** inside `agents/openai*.yaml`.
It does **not** control your GitHub commit account name/avatar.

- Default profile: `agents/openai.yaml`
- Alternate profile: `agents/openai.chatgpt.yaml`

To switch profile style, copy the alternate file content into `agents/openai.yaml` and commit.

## 8. Repository Structure

```text
decision-orchestrator-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
│   ├── openai.yaml
│   └── openai.chatgpt.yaml
├── assets/
├── references/
│   └── openclaw-input.example.json
├── docs/
│   └── agents.md
└── scripts/
    └── run_multi_advisor.py
```

## 9. Versioning Guidance

- Use semantic tags for workflow/runtime changes.
- Keep prompt-structure changes backward-compatible where possible.
- Log routing or scoring logic changes in commit messages.

## 10. License

Use and adapt freely for your own workflow repository.

## 11. Detailed Prompt Spec

For a strict output contract by role, see [docs/agents.md](./docs/agents.md).
