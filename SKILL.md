---
name: multi-advisor-runner
description: Use when the user wants to run the multi-advisor decision workflow with minimal manual prompt orchestration, generate Router→Agents→CEO run artifacts in one pass, or prepare OpenClaw-compatible decision payloads.
---

# Multi Advisor Runner

## Overview
This skill reduces multi-file manual orchestration into a single run command. It creates one run package with Router/Agents/CEO artifacts and an OpenClaw handoff payload.

## When To Use
- User asks to run one decision end-to-end with the multi-advisor architecture.
- User wants fewer manual prompt-file calls.
- User wants OpenClaw-compatible input/output for workflow automation.

## Workflow
1. Prepare input JSON (see `references/openclaw-input.example.json`).
2. Run `scripts/run_multi_advisor.py`.
3. Use generated artifacts under the run folder.
4. Optionally pass `07-one-shot-prompt.md` to one model call for compact execution.

## Command
```bash
python3 ~/.codex/skills/multi-advisor-runner/scripts/run_multi_advisor.py \
  --input /path/to/decision-input.json \
  --runs-root "/Users/chuen/多顾问决策系统/runs" \
  --owner "Elias"
```

## Artifacts
Per run, this skill creates:
- `01-decision-input.md`
- `02-router-output.yaml`
- `03-agent-outputs.yaml`
- `04-ceo-final.yaml`
- `05-decision-log.md`
- `06-review-summary.md`
- `07-one-shot-prompt.md`
- `openclaw-payload.json`

## Notes
- This script scaffolds deterministic structure.
- You can fill/refine advisor reasoning after generation, or run the one-shot prompt for a single-pass completion.

## Branding Switch (Claude/ChatGPT)
- Default profile is `agents/openai.yaml` (Claude style).
- For ChatGPT style, replace it with `agents/openai.chatgpt.yaml` content.
- Avatar assets are in `assets/` and can be replaced with official provider branding if needed.
