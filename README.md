# Multi Advisor Runner Skill

English | [简体中文](./README.zh-CN.md)

Run a full multi-advisor decision workflow in one command:
Router -> Advisors -> CEO Final.

This skill is designed for Codex/Claude Code workflows and can be integrated into OpenClaw pipelines.

## What It Generates

For each run, it creates:

- `01-decision-input.md`
- `02-router-output.yaml`
- `03-agent-outputs.yaml`
- `04-ceo-final.yaml`
- `05-decision-log.md`
- `06-review-summary.md`
- `07-one-shot-prompt.md`
- `openclaw-payload.json`

## Quick Start

```bash
python3 scripts/run_multi_advisor.py \
  --input references/openclaw-input.example.json \
  --runs-root "/Users/chuen/多顾问决策系统/runs" \
  --owner "Elias"
```

## Provider Branding

Default profile is Claude style in `agents/openai.yaml`.

If you want ChatGPT style:

1. Open `agents/openai.chatgpt.yaml`
2. Copy content into `agents/openai.yaml`
3. Commit and push

## Use Cases

- Strategy and growth decisions
- Product and UX decisions
- High-impact hiring/partnership/market decisions
- Execution-stuck cases

## License

Use and modify in your own workflow repo.
