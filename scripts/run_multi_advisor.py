#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import re
from pathlib import Path

ROUTES = {
    "growth_strategy": ["Drucker", "Buffett", "Musk"],
    "product_experience": ["Jobs", "KenyaHara", "Musk"],
    "high_impact_decision": ["Munger", "Drucker", "Buffett", "Musk"],
    "execution_stuck": ["Musk"],
}

CATEGORY_LABELS = {
    "zh": {
        "growth_strategy": "增长策略",
        "product_experience": "产品/体验",
        "high_impact_decision": "重大决策",
        "execution_stuck": "执行停滞",
    },
    "en": {
        "growth_strategy": "Growth Strategy",
        "product_experience": "Product/Experience",
        "high_impact_decision": "High-Impact Decision",
        "execution_stuck": "Execution-Stuck",
    },
}


def detect_category(problem_type: str, objective: str, context: str) -> str:
    text = f"{problem_type} {objective} {context}".lower()
    if any(k in text for k in ["拖延", "停滞", "还没开始", "delay", "stuck", "execution"]):
        return "execution_stuck"
    if any(k in text for k in ["产品", "体验", "页面", "content", "ux", "ui", "product", "experience"]):
        return "product_experience"
    if any(k in text for k in ["招聘", "合作", "市场", "定价", "投资", "重大", "pricing", "hire", "partnership", "market"]):
        return "high_impact_decision"
    return "growth_strategy"


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


def format_constraints_md(constraints: dict, lang: str) -> str:
    if not constraints:
        return "- None" if lang == "en" else "- 无"
    sep = ":" if lang == "en" else "："
    return "\n".join(f"- {k}{sep} {v}" for k, v in constraints.items())


def labels(lang: str) -> dict:
    if lang == "en":
        return {
            "decision_id": "Decision ID",
            "date": "Date",
            "owner": "Owner",
            "problem_type": "Problem Type",
            "objective_context": "Objective & Context",
            "single_objective": "Single Objective",
            "scenario": "Scenario",
            "constraints": "Constraints",
            "success_metrics": "Success Metrics",
            "options": "Options",
            "known_risks": "Known Risks",
            "none": "None",
            "pending": "Pending",
            "pending_fill": "To be completed",
            "risk": "Risk",
            "mitigation": "Mitigation",
            "decision_log": "Decision Log",
            "recorded_by": "Recorded By",
            "routing_result": "Routing Result",
            "category": "Category",
            "route_order": "Route Order",
            "advisor_summary": "Advisor Summary",
            "final_decision_section": "Final Decision",
            "conclusion": "Conclusion",
            "tradeoff_reason": "Tradeoff Reason",
            "actions_48h": "48h Actions",
            "review_metrics_7d": "7-day Review Metrics",
            "review_summary": "Review Summary",
            "what_went_right": "What Went Right",
            "issues": "Issues Found",
            "next_optimization": "Next Optimization",
            "router_reason": "Standard routing applied",
            "data_gap_placeholder": "None (or add missing data)",
            "handoff_placeholder": "Complete standard chain first, then extend",
            "one_shot_role": "You are a Decision Orchestrator executor. Based on the input below, complete Router -> Agents -> CEO Final in one pass.",
            "one_shot_input": "Input",
            "one_shot_req": "Requirements",
            "req1": "First output Router YAML (category/confidence/route/data_gaps).",
            "req2": "Then output Agents YAML (in route order).",
            "req3": "Finally output CEO Final YAML (including 48h/7d actions and kill_criteria).",
            "req4": "Output must be directly writable into:",
        }
    return {
        "decision_id": "决策ID",
        "date": "日期",
        "owner": "发起人",
        "problem_type": "问题类型",
        "objective_context": "目标与背景",
        "single_objective": "单一目标",
        "scenario": "场景描述",
        "constraints": "约束条件",
        "success_metrics": "成功标准（量化）",
        "options": "候选方案",
        "known_risks": "已知风险",
        "none": "无",
        "pending": "待分析",
        "pending_fill": "待补充",
        "risk": "风险",
        "mitigation": "缓解",
        "decision_log": "决策日志",
        "recorded_by": "记录人",
        "routing_result": "路由结果",
        "category": "分类",
        "route_order": "调用顺序",
        "advisor_summary": "顾问摘要",
        "final_decision_section": "最终拍板",
        "conclusion": "结论",
        "tradeoff_reason": "取舍理由",
        "actions_48h": "48小时行动",
        "review_metrics_7d": "7天复盘指标",
        "review_summary": "复盘摘要",
        "what_went_right": "做对了什么",
        "issues": "暴露问题",
        "next_optimization": "下轮优化",
        "router_reason": "按标准路由执行",
        "data_gap_placeholder": "如无写\"无\"",
        "handoff_placeholder": "先完成标准链路，再做扩展分析",
        "one_shot_role": "你是 Decision Orchestrator 执行器。请基于以下输入，按 Router -> Agents -> CEO Final 一次性完成输出。",
        "one_shot_input": "输入",
        "one_shot_req": "要求",
        "req1": "先输出 Router YAML（category/confidence/route/data_gaps）。",
        "req2": "再输出 Agents YAML（按路由顺序）。",
        "req3": "最后输出 CEO Final YAML（包含48h/7d动作和kill_criteria）。",
        "req4": "输出必须可直接写入以下文件：",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one decision-orchestrator run package")
    parser.add_argument("--input", required=True, help="Path to decision input JSON")
    parser.add_argument("--runs-root", default="./runs", help="Runs output root")
    parser.add_argument("--run-id", default="", help="Optional explicit run id")
    parser.add_argument("--owner", default="Decision Owner", help="Decision owner")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Output language")
    args = parser.parse_args()

    lang = args.lang
    l = labels(lang)

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

    category_key = detect_category(problem_type, objective, context)
    category_label = CATEGORY_LABELS[lang][category_key]
    route = ROUTES[category_key]
    problem_type_display = category_label if lang == "en" else (problem_type or category_label)

    decision_input = f"""# Decision Input - {run_id}

- {l['decision_id']}：{run_id}
- {l['date']}：{now.strftime('%Y-%m-%d')}
- {l['owner']}：{args.owner}
- {l['problem_type']}：{problem_type_display}

## {l['objective_context']}
- {l['single_objective']}：{objective}
- {l['scenario']}：{context}

## {l['constraints']}
{format_constraints_md(constraints, lang)}

## {l['success_metrics']}
{chr(10).join(f'- {m}' for m in metrics) if metrics else f"- {l['none']}"}

## {l['options']}
{chr(10).join(f'- {o}' for o in options) if options else f"- {l['none']}"}

## {l['known_risks']}
{chr(10).join(f'- {r}' for r in risks) if risks else f"- {l['none']}"}
"""

    router_lines = [
        f"category: {category_label}",
        "confidence: 88",
        "scores:",
        "  category_fit: 4",
        "  input_completeness: 4",
        "  route_stability: 4",
        "route:",
    ]
    for agent in route:
        router_lines.append(f"  - agent: {agent}")
        router_lines.append(f"    reason: {l['router_reason']}")
    router_lines.extend([
        "data_gaps:",
        f"  - {l['data_gap_placeholder']}",
        "hard_stop: false",
        f"hard_stop_reason: {l['none']}",
        "handoff_notes:",
        f"  - {l['handoff_placeholder']}",
    ])
    router_output = "\n".join(router_lines)

    agent_chunks = []
    for agent in route:
        agent_chunks.append(
            f"""{agent}:
  agent: {agent}
  decision: {l['pending']}
  scores:
    dimension_1: 0-5
    dimension_2: 0-5
    dimension_3: 0-5
    dimension_4: 0-5
  reasons:
    - {l['pending_fill']}
  risks:
    - {l['pending_fill']}
  missing_data:
    - {l['pending_fill']}
  action_48h:
    - {l['pending_fill']}
"""
        )
    agent_output = "\n".join(agent_chunks).rstrip() + "\n"

    ceo_output = f"""decision_owner: {args.owner}
final_decision: {l['pending_fill']}
scores:
  strategic_alignment: 0-5
  execution_feasibility: 0-5
  risk_controllability: 0-5
  evidence_quality: 0-5
why:
  - {l['pending_fill']}
conflicts:
  - point: {l['pending_fill']}
    options: [OptionA, OptionB]
    choose: {l['pending_fill']}
    tradeoff: {l['pending_fill']}
rejected_options:
  - {l['pending_fill']}
risks:
  - {l['risk']}: {l['pending_fill']}
    {l['mitigation']}: {l['pending_fill']}
action_48h:
  - {l['pending_fill']}
action_7d:
  - {l['pending_fill']}
kill_criteria:
  - {l['pending_fill']}
review_date: {now.strftime('%Y-%m-%d')}
hard_stop: false
hard_stop_reason: {l['none']}
"""

    decision_log = f"""# {l['decision_log']} - {run_id}

- {l['date']}：{now.strftime('%Y-%m-%d')}
- {l['recorded_by']}：{args.owner}

## {l['routing_result']}
- {l['category']}：{category_label}
- {l['route_order']}：{' -> '.join(route)}

## {l['advisor_summary']}
- {l['pending_fill']}

## {l['final_decision_section']}
- {l['conclusion']}：{l['pending_fill']}
- {l['tradeoff_reason']}：{l['pending_fill']}

## {l['actions_48h']}
- [ ] {l['pending_fill']}

## {l['review_metrics_7d']}
- {l['pending_fill']}
"""

    review_summary = f"""# {l['review_summary']} - {run_id}

## {l['conclusion']}
{l['pending_fill']}

## {l['what_went_right']}
- {l['pending_fill']}

## {l['issues']}
- {l['pending_fill']}

## {l['next_optimization']}
1. {l['pending_fill']}
"""

    one_shot_prompt = (
        f"{l['one_shot_role']}\n\n"
        f"# {l['one_shot_input']}\n{json.dumps(data, ensure_ascii=False, indent=2)}\n\n"
        f"# {l['one_shot_req']}\n"
        f"1. {l['req1']}\n"
        f"2. {l['req2']}\n"
        f"3. {l['req3']}\n"
        f"4. {l['req4']}\n"
        "- 02-router-output.yaml\n"
        "- 03-agent-outputs.yaml\n"
        "- 04-ceo-final.yaml\n"
    )

    payload = {
        "run_id": run_id,
        "owner": args.owner,
        "lang": lang,
        "category": category_label,
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
