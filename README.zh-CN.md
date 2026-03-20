# Multi Advisor Runner Skill（中文说明）

[English](./README.md) | 简体中文

这个项目把多顾问决策流程封装成一次调用，避免手动拼接多个 Prompt 文件。

## 核心能力

每次运行会自动生成完整决策工件：

- `01-decision-input.md`
- `02-router-output.yaml`
- `03-agent-outputs.yaml`
- `04-ceo-final.yaml`
- `05-decision-log.md`
- `06-review-summary.md`
- `07-one-shot-prompt.md`
- `openclaw-payload.json`

## 快速开始

```bash
python3 scripts/run_multi_advisor.py \
  --input references/openclaw-input.example.json \
  --runs-root "/Users/chuen/多顾问决策系统/runs" \
  --owner "Elias"
```

## 品牌与头像切换

- 默认是 Claude 风格：`agents/openai.yaml`
- 若要 ChatGPT 风格：把 `agents/openai.chatgpt.yaml` 的内容覆盖到 `agents/openai.yaml`

## 适用场景

- 增长策略决策
- 产品与体验决策
- 招聘/合作/市场等重大决策
- 执行停滞推进
