# Decision Orchestrator Skill（中文说明）

[English](./README.md) | 简体中文

这是一个将多顾问决策体系封装为“一次调用”的技能项目。核心目标是把分散的 Prompt 调用，统一为可复用、可追溯、可自动化的运行流程。

## 1. 项目定位

该项目用于在 Codex/Claude Code/OpenClaw 场景中执行标准化决策链路：

`Router -> Advisors -> CEO Final`

适用场景：
- 增长策略决策
- 产品/体验优化
- 招聘/合作/市场等重大决策
- 执行卡点推进

## 2. 架构说明

### Router（路由层）
- 负责问题分类与顾问调用顺序。
- 输出置信度、路由理由和信息缺口。
- 不直接给最终业务结论。

### Advisors（分析层）
- 按领域拆分职责，避免越界和重复分析。
- 每位顾问输出结构化 YAML，包含评分、风险、48小时动作。

### CEO Final（拍板层）
- 汇总冲突意见并做最终取舍。
- 输出最终决策、代价、行动计划、终止条件、复盘日期。

## 3. 每位 Agent / Prompt 的细化职责

- **Drucker**：客户是谁、价值是什么、是否可验证。
- **Jobs**：体验是否足够清晰流畅，是否存在多余内容。
- **Kenya Hara**：结构是否必要，能否删除/合并以降低认知成本。
- **Munger**：用多模型评估风险（经济学/心理学/概率）。
- **Buffett**：是否强化护城河，是否偏离核心战略。
- **Musk**：为何还没开始，如何在48小时内落地最小动作。

## 4. 运行产物

每次运行会生成完整工件：

- `01-decision-input.md`
- `02-router-output.yaml`
- `03-agent-outputs.yaml`
- `04-ceo-final.yaml`
- `05-decision-log.md`
- `06-review-summary.md`
- `07-one-shot-prompt.md`
- `openclaw-payload.json`

这使决策过程可审计、可复盘、可自动化接入。

## 5. 快速开始

```bash
python3 scripts/run_multi_advisor.py \
  --input references/openclaw-input.example.json \
  --runs-root "/Users/chuen/多顾问决策系统/runs" \
  --owner "Elias"
```

## 6. OpenClaw 使用方式

- 输入：兼容 `references/openclaw-input.example.json`。
- 输出：`openclaw-payload.json` 可直接用于下游节点。

## 7. 服务商头像与名称切换

当前仓库提供两套展示配置：
- Claude：`agents/openai.yaml`（默认）
- ChatGPT：`agents/openai.chatgpt.yaml`

若要切换为 ChatGPT：将 `openai.chatgpt.yaml` 内容覆盖到 `openai.yaml` 后提交即可。

## 8. 项目结构

```text
decision-orchestrator-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── agents/
├── assets/
├── references/
└── scripts/
```

## 9. 建议维护策略

- 路由规则改动需记录原因与影响。
- 每次优化至少做 3 个真实案例回放。
- 保持输出结构稳定，避免下游自动化断裂。

## 10. 详细 Prompt 规范

如需查看 Router/Agents/CEO Final 的输出契约，请参考 [docs/agents.md](./docs/agents.md)。
