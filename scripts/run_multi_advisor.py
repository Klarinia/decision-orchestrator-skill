#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
from pathlib import Path

ROUTES = {
    "增长策略": ["Drucker", "Buffett", "Musk"],
    "产品/体验": ["Jobs", "KenyaHara", "Musk"],
    "重大决策": ["Munger", "Drucker", "Buffett", "Musk"],
    "执行停滞": ["Musk"],
}


def detect_category(problem_type: str, objective: str, context: str) -> str:
    text = f"{problem_type} {objective} {context}".lower()
    if any(k in text for k in ["拖延", "停滞", "还没开始", "delay", "stuck"]):
        return "执行停滞"
    if any(k in text for k in ["产品", "体验", "页面", "content", "ux", "ui"]):
        return "产品/体验"
    if any(k in text for k in ["招聘", "合作", "市场", "定价", "投资", "重大", "pricing", "hire"]):
        return "重大决策"
    return "增长策略"


def next_run_id(runs_root: Path, now: dt.datetime) -> str:
    day = now.strftime("%Y%m%d")
    pat = re.compile(rf"^run-{day}-(\d{{3}})$")
    max_n = 0
    if runs_root.exists():
        for p in runs_root.iterdir():
            if p.is_dir():
                m = pat.match(p.name)
                if m:
                    max_n = max(max_n, int(m.group(1)))
    return f"run-{day}-{max_n + 1:03d}"


def dump(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def format_constraints_md(constraints: dict) -> str:
    if not constraints:
        return "- 无"
    return "\n".join(f"- {k}：{v}" for k, v in constraints.items())


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one decision-orchestrator run package")
    parser.add_argument("--input", required=True, help="Path to decision input JSON")
    parser.add_argument("--runs-root", default="./runs", help="Runs output root")
    parser.add_argument("--run-id", default="", help="Optional explicit run id")
    parser.add_argument("--owner", default="Decision Owner", help="Decision owner")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    data = json.loads(input_path.read_text(encoding="utf-8"))

    now = dt.datetime.now()
    runs_root = Path(args.runs_root).expanduser().resolve()
    runs_root.mkdir(parents=True, exist_ok=True)

    run_id = args.run_id or next_run_id(runs_root, now)
    run_dir = runs_root / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    problem_type = data.get("problem_type", "")
    objective = data.get("objective", "")
    context = data.get("context", "")
    constraints = data.get("constraints", {})
    metrics = data.get("success_metrics", [])
    options = data.get("options", [])
    risks = data.get("known_risks", [])

    category = detect_category(problem_type, objective, context)
    route = ROUTES[category]

    decision_input = f"""# Decision Input - {run_id}

- 决策ID：{run_id}
- 日期：{now.strftime('%Y-%m-%d')}
- 发起人：{args.owner}
- 问题类型：{problem_type or category}

## 目标与背景
- 单一目标：{objective}
- 场景描述：{context}

## 约束条件
{format_constraints_md(constraints)}

## 成功标准（量化）
{chr(10).join(f'- {m}' for m in metrics) if metrics else '- 无'}

## 候选方案
{chr(10).join(f'- {o}' for o in options) if options else '- 无'}

## 已知风险
{chr(10).join(f'- {r}' for r in risks) if risks else '- 无'}
"""

    router_lines = [
        f"category: {category}",
        "confidence: 88",
        "scores:",
        "  category_fit: 4",
        "  input_completeness: 4",
        "  route_stability: 4",
        "route:",
    ]
    for agent in route:
        router_lines.append(f"  - agent: {agent}")
        router_lines.append("    reason: 按标准路由执行")
    router_lines.extend([
        "data_gaps:",
        "  - 如无写\"无\"",
        "hard_stop: false",
        "hard_stop_reason: 无",
        "handoff_notes:",
        "  - 先完成标准链路，再做扩展分析",
    ])
    router_output = "\n".join(router_lines)

    agent_chunks = []
    for agent in route:
        agent_chunks.append(
            f"""{agent}:
  agent: {agent}
  decision: 待分析
  scores:
    dimension_1: 0-5
    dimension_2: 0-5
    dimension_3: 0-5
    dimension_4: 0-5
  reasons:
    - 待补充
  risks:
    - 待补充
  missing_data:
    - 待补充
  action_48h:
    - 待补充
"""
        )
    agent_output = "\n".join(agent_chunks).rstrip() + "\n"

    ceo_output = f"""decision_owner: {args.owner}
final_decision: 待拍板
scores:
  strategic_alignment: 0-5
  execution_feasibility: 0-5
  risk_controllability: 0-5
  evidence_quality: 0-5
why:
  - 待补充
conflicts:
  - point: 待补充
    options: [方案A, 方案B]
    choose: 待补充
    tradeoff: 待补充
rejected_options:
  - 待补充
risks:
  - 风险: 待补充
    缓解: 待补充
action_48h:
  - 待补充
action_7d:
  - 待补充
kill_criteria:
  - 待补充
review_date: {now.strftime('%Y-%m-%d')}
hard_stop: false
hard_stop_reason: 无
"""

    decision_log = f"""# Decision Log - {run_id}

- 日期：{now.strftime('%Y-%m-%d')}
- 记录人：{args.owner}

## 路由结果
- 分类：{category}
- 调用顺序：{' -> '.join(route)}

## 顾问摘要
- 待补充

## {args.owner} 最终拍板
- 结论：待补充
- 取舍理由：待补充

## 48小时行动
- [ ] 待补充

## 7天复盘指标
- 待补充
"""

    review_summary = f"""# 复盘摘要 - {run_id}

## 结论
待补充

## 做对了什么
- 待补充

## 暴露问题
- 待补充

## 下轮优化
1. 待补充
"""

    one_shot_prompt = (
        "你是 Decision Orchestrator 执行器。请基于以下输入，按 Router -> Agents -> CEO Final 一次性完成输出。\n\n"
        f"# 输入\n{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"
        "# 要求\n"
        "1. 先输出 Router YAML（category/confidence/route/data_gaps）。\n"
        "2. 再输出 Agents YAML（按路由顺序）。\n"
        "3. 最后输出 CEO Final YAML（包含48h/7d动作和kill_criteria）。\n"
        "4. 输出必须可直接写入以下文件：\n"
        "- 02-router-output.yaml\n"
        "- 03-agent-outputs.yaml\n"
        "- 04-ceo-final.yaml\n"
    )

    payload = {
        "run_id": run_id,
        "owner": args.owner,
        "category": category,
        "route": route,
        "run_dir": str(run_dir),
        "artifacts": {
            "decision_input": str(run_dir / "01-decision-input.md"),
            "router_output": str(run_dir / "02-router-output.yaml"),
            "agent_outputs": str(run_dir / "03-agent-outputs.yaml"),
            "ceo_final": str(run_dir / "04-ceo-final.yaml"),
            "decision_log": str(run_dir / "05-decision-log.md"),
            "review_summary": str(run_dir / "06-review-summary.md"),
            "one_shot_prompt": str(run_dir / "07-one-shot-prompt.md"),
        },
    }

    dump(run_dir / "01-decision-input.md", decision_input)
    dump(run_dir / "02-router-output.yaml", router_output)
    dump(run_dir / "03-agent-outputs.yaml", agent_output)
    dump(run_dir / "04-ceo-final.yaml", ceo_output)
    dump(run_dir / "05-decision-log.md", decision_log)
    dump(run_dir / "06-review-summary.md", review_summary)
    dump(run_dir / "07-one-shot-prompt.md", one_shot_prompt)
    dump(run_dir / "openclaw-payload.json", json.dumps(payload, ensure_ascii=False, indent=2))

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
